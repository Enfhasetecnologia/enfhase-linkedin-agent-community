"""Prepare a deterministic, allowlisted release candidate; never publish or install."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_VERSION = '0.4.4'
SKILL_FILES = (
    'SKILL.md', 'agents/openai.yaml', 'references/workflows.md',
    'references/tools.md', 'references/precision.md', 'scripts/editorial.py',
)
DOCUMENTS = ('README.md', 'INSTALL.md', 'PRIVACY.md', 'SECURITY.md', 'ORIGINALITY.md', 'SUPPORT.md', 'TERMS.md')
SOURCE_COMMIT = '093f3c3e5949f14c07b73f3f467f91a666e03ae2'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def reviewed_file(root, relative):
    path = root
    for part in PurePosixPath(relative).parts:
        if part in ('..', '.') or PurePosixPath(relative).is_absolute():
            raise ValueError('unsafe source path')
        path = path / part
        if path.is_symlink():
            raise ValueError('symlink source forbidden')
    data = path.read_bytes()  # Missing allowlisted files fail closed.
    if len(data) > (5 * 1024 * 1024 if relative.endswith('.png') else 500_000):
        raise ValueError('source too large')
    return data


def archive_bytes(entries):
    import io
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(entries.items()):
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or '\\' in name:
                raise ValueError('unsafe archive path')
            info = zipfile.ZipInfo(name, (2026, 11, 4, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return stream.getvalue()


def candidate_entries(root=ROOT):
    template_prefix = 'distribution/' if (root/'distribution').is_dir() else ''
    skill = {name: reviewed_file(root, 'native/enfhase-linkedin-agent/' + name)
             for name in SKILL_FILES}
    # Normalize host metadata without changing workflow instructions or helper code.
    metadata_path = template_prefix+'agents-openai.yaml' if template_prefix else 'native/enfhase-linkedin-agent/agents/openai.yaml'
    skill['agents/openai.yaml'] = reviewed_file(root, metadata_path)
    version = re.search(rb"^VERSION = '([0-9.]+)'$", skill['scripts/editorial.py'], re.M)
    if not version:
        raise ValueError('missing helper version')
    version = version.group(1).decode('ascii')
    template = reviewed_file(root, template_prefix+'plugin.json' if template_prefix else 'plugin/plugin.json')
    plugin = json.loads(template)
    if plugin['version'] != PACKAGE_VERSION or plugin['name'] != 'enfhase-linkedin-agent':
        raise ValueError('plugin/helper identity mismatch')
    if set(plugin) - {'$schema', 'name', 'version', 'description', 'author', 'extensions', 'license'}:
        raise ValueError('unexpected plugin capability')
    extension = plugin['extensions']['com.openai']
    if not {'interface'} <= set(extension) <= {'interface', 'review', 'publication'} or set(plugin['extensions']) != {'com.openai'}:
        raise ValueError('only presentation metadata allowed')
    docs = {name: reviewed_file(root, template_prefix + name) for name in DOCUMENTS}
    license_data = reviewed_file(root, template_prefix+'LICENSE')
    entries = dict(docs)
    entries['.gitignore'] = b'dist/\n__pycache__/\n*.py[cod]\n.env\n.env.*\n'
    entries['LICENSE'] = license_data
    icon = reviewed_file(root, template_prefix+'assets/icon.png')
    entries['assets/icon.png'] = icon
    entries['.github/workflows/security.yml'] = reviewed_file(root, template_prefix+'security.yml' if template_prefix else '.github/workflows/security.yml')
    entries['tools/verify_distribution.py'] = reviewed_file(root, template_prefix+'verify_distribution.py' if template_prefix else 'tools/verify_distribution.py')
    entries['tools/build_public_distribution.py'] = reviewed_file(root, 'tools/build_public_distribution.py')
    entries.update({'native/enfhase-linkedin-agent/' + name: data for name, data in skill.items()})
    entries['plugin/plugin.json'] = template
    entries['tests/test_native_workflows.py'] = reviewed_file(root, 'tests/test_native_workflows.py')
    entries['tests/test_public_distribution.py'] = reviewed_file(root, 'tests/test_public_distribution.py')

    # Keep original code/instructions byte-for-byte. License notices accompany each ZIP.
    claude = {'enfhase-linkedin-agent/' + name: data for name, data in skill.items()
              if not name.startswith('agents/')}
    claude['enfhase-linkedin-agent/LICENSE'] = license_data
    chatgpt = {'plugin.json': template, 'LICENSE': license_data, 'PRIVACY.md': docs['PRIVACY.md'], 'assets/icon.png': icon}
    chatgpt.update({'skills/enfhase-linkedin-agent/' + name: data for name, data in skill.items()})
    packages = {
        f'packages/enfhase-linkedin-agent-claude-{PACKAGE_VERSION}.zip': archive_bytes(claude),
        f'packages/enfhase-linkedin-agent-chatgpt-{PACKAGE_VERSION}.zip': archive_bytes(chatgpt),
    }
    entries.update(packages)
    entries['SHA256SUMS'] = ''.join(f'{digest(data)}  {name}\n' for name, data in sorted(packages.items())).encode()
    status = {
        'state': 'owner_approved_pending_release_checks',
        'helper_version': version, 'source_commit': SOURCE_COMMIT,
        'package_version': PACKAGE_VERSION,
        'includes_git_history': False, 'includes_api_backend': False,
        'license': 'MIT; owner approved native distribution; original repository LICENSE unchanged',
        'github_distribution': 'public; private vulnerability reporting, secret scanning and push protection enabled; main protected',
        'blockers': ['import of the new Claude archive and end-user use of the saved ChatGPT plugin',
                     'ChatGPT Chat and iPhone acceptance tests',
                     'OpenAI business publisher verification, portal validation and review for directory installation'],
    }
    entries['RELEASE_STATUS.json'] = (json.dumps(status, indent=2) + '\n').encode()
    for name, data in entries.items():
        if name.endswith(('.zip', '.png')):
            continue
        text = data.decode('utf-8')
        private = (r'https://(?:claude\.ai/chat/|chatgpt\.com/c/)',
                   r'skill_[0-9A-Za-z]{12,}', r'skill-[a-f0-9]{32}',
                   r'(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_-]{20,}',
                   r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
        if any(re.search(pattern, text) for pattern in private):
            raise ValueError('private marker or credential pattern: ' + name)
    manifest = {'package_version': PACKAGE_VERSION, 'helper_version': version, 'files': {name: digest(data) for name, data in sorted(entries.items())}}
    entries['MANIFEST.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    return entries


def main():
    entries = candidate_entries()
    destination = ROOT / 'dist/public-candidate'
    destination.parent.mkdir(exist_ok=True)
    if destination.exists():
        raise SystemExit('Candidate already exists; inspect or move it before rebuilding.')
    with tempfile.TemporaryDirectory(prefix='public-candidate-', dir=destination.parent) as stage:
        staged = Path(stage) / 'candidate'
        staged.mkdir()
        for name, data in entries.items():
            path = staged / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        staged.rename(destination)
    print(json.dumps({'state': 'private_candidate', 'files': len(entries),
                      'manifest_sha256': digest(entries['MANIFEST.json'])}))


if __name__ == '__main__':
    main()
