"""Release boundaries: exclude private history and reject unsafe package inputs."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('public_distribution', ROOT/'tools/build_public_distribution.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PublicDistributionChecks(unittest.TestCase):
    def test_repository_sync_uses_only_the_canonical_skill_without_new_capabilities(self):
        entries = builder.candidate_entries()
        codex = json.loads(entries['.agents/plugins/marketplace.json'])
        claude = json.loads(entries['.claude-plugin/marketplace.json'])
        self.assertEqual(len(codex['plugins']), 1)
        self.assertEqual(len(claude['plugins']), 1)
        path = './native/enfhase-linkedin-agent'
        self.assertEqual(codex['plugins'][0]['source'], {'source': 'local', 'path': path})
        self.assertEqual(claude['plugins'][0]['source'], path)
        self.assertEqual(codex['plugins'][0]['policy']['installation'], 'AVAILABLE')
        self.assertNotIn('pluginId', codex['plugins'][0])
        manifest = json.loads(entries['native/enfhase-linkedin-agent/.claude-plugin/plugin.json'])
        self.assertEqual(set(manifest), {'name', 'version', 'description', 'author', 'license', 'skills'})
        self.assertEqual(manifest['skills'], ['./'])
        self.assertEqual(manifest['version'], builder.PACKAGE_VERSION)
        self.assertEqual(entries['native/enfhase-linkedin-agent/scripts/editorial.py'],
                         (ROOT/'native/enfhase-linkedin-agent/scripts/editorial.py').read_bytes())

    def test_plugin_metadata_has_short_subtitle_and_no_dangling_icons(self):
        entries = builder.candidate_entries()
        plugin = json.loads(entries['plugin/plugin.json'])
        interface = plugin['extensions']['com.openai']['interface']
        self.assertLessEqual(len(interface['shortDescription']), 30)
        self.assertEqual(plugin['extensions']['com.openai']['review']['commerce'], False)
        self.assertEqual(plugin['extensions']['com.openai']['publication']['countries'], [])
        for key in ('logo', 'composerIcon'):
            self.assertEqual(interface[key], './assets/icon.png')
            self.assertIn('assets/icon.png', entries)
        metadata = entries['native/enfhase-linkedin-agent/agents/openai.yaml'].decode()
        self.assertNotIn('icon_small:', metadata)
        self.assertNotIn('icon_large:', metadata)
        self.assertNotIn('products:', metadata)
        self.assertIn('allow_implicit_invocation: true', metadata)

    def test_only_allowlisted_files_are_exported(self):
        entries = builder.candidate_entries()
        for name in entries:
            self.assertFalse(any(part in {'.git', 'eval', 'tmp', 'src', '.env'} for part in Path(name).parts), name)
        self.assertNotIn('docs/CLAUDE_VALIDATION.json', entries)
        self.assertEqual(json.loads(entries['RELEASE_STATUS.json'])['state'],
                         'owner_approved_pending_release_checks')
        if (ROOT/'distribution').is_dir():
            self.assertTrue((ROOT/'LICENSE').read_text().startswith('Copyright'))
            self.assertIn('without written authorization', (ROOT/'LICENSE').read_text())
        else:
            self.assertTrue((ROOT/'LICENSE').read_text().startswith('MIT License'))

    def test_archives_contain_identical_reviewed_helper_and_license(self):
        entries = builder.candidate_entries()
        source = (ROOT/'native/enfhase-linkedin-agent/scripts/editorial.py').read_bytes()
        for name, data in entries.items():
            if not name.endswith('.zip'):
                continue
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = archive.namelist()
                helper = [p for p in names if p.endswith('/scripts/editorial.py')]
                self.assertEqual(len(helper), 1)
                self.assertEqual(archive.read(helper[0]), source)
                self.assertTrue(any(p.endswith('LICENSE') for p in names))
                for path in names:
                    self.assertNotIn('..', Path(path).parts)
                    self.assertFalse(Path(path).is_absolute())
                    self.assertFalse(any(x in path for x in ('.git/', 'eval/', '.env', 'mcp.json', 'hooks/')))
                if 'chatgpt' in name:
                    self.assertIn('plugin.json', names)
                    self.assertIn('skills/enfhase-linkedin-agent/SKILL.md', names)
                else:
                    self.assertIn('enfhase-linkedin-agent/SKILL.md', names)

    def test_build_is_reproducible_and_hashes_cover_exact_content(self):
        first, second = builder.candidate_entries(), builder.candidate_entries()
        self.assertEqual(first, second)
        manifest = json.loads(first['MANIFEST.json'])
        self.assertEqual(set(manifest['files']), set(first)-{'MANIFEST.json'})
        for path, digest in manifest['files'].items():
            self.assertEqual(hashlib.sha256(first[path]).hexdigest(), digest)

    def test_missing_source_and_symlink_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(FileNotFoundError):
                builder.candidate_entries(root)
            (root/'link').symlink_to(ROOT/'LICENSE')
            with self.assertRaises(ValueError):
                builder.reviewed_file(root, 'link')
            (root/'parent').symlink_to(ROOT, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.reviewed_file(root, 'parent/LICENSE')
        with self.assertRaises(ValueError):
            builder.reviewed_file(ROOT, '../LICENSE')

    def test_private_trace_or_credential_pattern_is_not_exported(self):
        original = builder.reviewed_file
        def contaminated(root, path):
            data = original(root, path)
            if path in ('distribution/README.md', 'README.md'):
                synthetic_private_url = b'https://' + b'claude.ai' + b'/chat/' + b'synthetic-private-conversation'
                return data + b'\n' + synthetic_private_url
            return data
        with patch.object(builder, 'reviewed_file', side_effect=contaminated):
            with self.assertRaisesRegex(ValueError, 'private marker'):
                builder.candidate_entries()

    def test_injected_plugin_capability_is_rejected(self):
        original = builder.reviewed_file
        def contaminated(root, path):
            data = original(root, path)
            if path in ('distribution/plugin.json', 'plugin/plugin.json'):
                value = json.loads(data)
                value['extensions']['com.openai']['hooks'] = './hooks/hooks.json'
                return json.dumps(value).encode()
            return data
        with patch.object(builder, 'reviewed_file', side_effect=contaminated):
            with self.assertRaisesRegex(ValueError, 'presentation'):
                builder.candidate_entries()

    def test_path_traversal_zip_is_rejected(self):
        for path in ('../file', '/file', 'folder\\file'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                builder.archive_bytes({path: b'content'})


if __name__ == '__main__':
    unittest.main()
