"""Verify the release inventory and all distributed file hashes, offline."""
import hashlib
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root/'MANIFEST.json').read_text())
for name, expected in manifest['files'].items():
    path = Path(name)
    if path.is_absolute() or '..' in path.parts:
        raise SystemExit('Unsafe manifest path')
    source = root/path
    if source.is_symlink() or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise SystemExit('Distribution integrity mismatch: ' + name)
for package in (root/'packages').glob('*.zip'):
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise SystemExit('Duplicate archive entry')
        for entry in archive.infolist():
            path = Path(entry.filename)
            if path.is_absolute() or '..' in path.parts or (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise SystemExit('Unsafe archive entry')
print('PASS: release file hashes and archive paths verified')
