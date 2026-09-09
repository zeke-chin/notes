#!/usr/bin/env python3
"""Create a portable Release ZIP with verified fonts; exclude machine backups."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', default='1.0.0')
    args = parser.parse_args()
    if not args.version or any(c not in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-' for c in args.version):
        parser.error('Version must contain only letters, digits, dots and hyphens.')
    fonts = json.loads((ROOT / 'fonts-manifest.json').read_text())
    rpm = next(s for s in json.loads((ROOT / 'sources.json').read_text()) if s['file'].endswith('.rpm'))
    checked = [(ROOT / 'fonts' / f['path'], f['sha256']) for f in fonts]
    checked.append((ROOT / 'assets' / rpm['file'], rpm['sha256']))
    for path, expected in checked:
        if not path.is_file() or digest(path) != expected:
            raise SystemExit(f'Checksum mismatch or missing asset: {path}')
    files = [ROOT / n for n in ['README.md', '.gitignore', 'manage.py', 'prepare-fonts.py',
             'verify-font-trial.py', 'package-release.py', 'sources.json', 'fonts-manifest.json']]
    files += [p for p, _ in checked]
    for folder in ['config', 'licenses']:
        files += [p for p in (ROOT / folder).rglob('*') if p.is_file()]
    files += [ROOT / 'verification' / n for n in ['qt-font-preview.png', 'pango-font-preview.png',
              'qt-glyph-runs.json', 'font-matches.json', 'retest.json']]
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    archive = dist / f'fedora-kde-apple-front-v{args.version}.zip'
    temporary = archive.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out:
        for path in sorted(files):
            if path.is_symlink():
                raise SystemExit(f'Unexpected symlink: {path}')
            out.write(path, 'fedora-kde-apple-front/' + path.relative_to(ROOT).as_posix())
    temporary.replace(archive)
    with zipfile.ZipFile(archive) as zipped:
        assert zipped.testzip() is None, 'ZIP integrity test failed'
        assert not any('/history/' in n or '/.font-trial-state' in n for n in zipped.namelist())
    (dist / 'SHA256SUMS').write_text(f'{digest(archive)}  {archive.name}\n')
    print(f'{archive}\n{archive.stat().st_size / 1024**2:.1f} MiB; {len(files)} files; ZIP CRC and source checksums verified.')


if __name__ == '__main__':
    main()
