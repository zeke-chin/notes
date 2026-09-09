#!/usr/bin/env python3
"""Rebuild the pinned font bundle without installing fonts or executing vendor scripts."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

PROJECT = Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def extract(path, target):
    subprocess.run(['7z', 'x', str(path), '-o' + str(target), '-y'],
                   check=True, stdout=subprocess.DEVNULL)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=PROJECT / '.cache/downloads')
    parser.add_argument('--output', type=Path, default=PROJECT / 'fonts')
    parser.add_argument('--emoji-rpm', type=Path, default=PROJECT / 'assets/fonts-apple-color-emoji.rpm')
    args = parser.parse_args()
    expected = json.loads((PROJECT / 'fonts-manifest.json').read_text())
    if args.output.exists():
        for item in expected:
            p = args.output / item['path']
            if not p.is_file() or sha(p) != item['sha256']:
                raise SystemExit(f'Existing bundle differs: {p}. Choose a new --output directory.')
        print('Pinned font bundle already complete; nothing changed.')
        return
    for tool in ['curl', '7z', 'rpm2cpio', 'cpio']:
        if not shutil.which(tool):
            raise SystemExit(f'Missing dependency: {tool}; see README.md')
    sources = json.loads((PROJECT / 'sources.json').read_text())
    rpm_source = next(s for s in sources if s['file'].endswith('.rpm'))
    if not args.emoji_rpm.is_file() or sha(args.emoji_rpm) != rpm_source['sha256']:
        raise SystemExit('Provide the archived, checksum-matching Emoji RPM using --emoji-rpm.')
    args.cache.mkdir(parents=True, exist_ok=True)
    for source in sources:
        if not source['url']:
            continue
        path = args.cache / source['file']
        if not path.exists():
            partial = path.with_suffix(path.suffix + '.part')
            subprocess.run(['curl', '-fL', '--retry', '2', '--connect-timeout', '20',
                            '--max-time', '600', source['url'], '-o', str(partial)], check=True)
            if sha(partial) != source['sha256']:
                raise SystemExit(f'Source changed: {source["file"]}. Do not silently accept new hashes; see README.')
            partial.replace(path)
        if sha(path) != source['sha256']:
            raise SystemExit(f'Cached source differs: {path}')
    with tempfile.TemporaryDirectory(prefix='apple-font-extract-') as temp:
        work = Path(temp)
        bundle = work / 'fonts'
        bundle.mkdir()
        for name, group, pattern in [('SF-Pro', 'SF-Pro-Text', 'SF-Pro-Text-*.otf'), ('SF-Mono', 'SF-Mono', '*.otf')]:
            dmg, pkg, payload, unpacked = [work / (name + '-' + suffix) for suffix in ['dmg', 'pkg', 'payload', 'unpacked']]
            extract(args.cache / (name + '.dmg'), dmg)
            packages = [p for p in dmg.rglob('*.pkg') if p.is_file()]
            if len(packages) != 1:
                raise SystemExit(f'Unexpected {name} DMG layout: {packages}')
            extract(packages[0], pkg)
            payloads = list(pkg.rglob('Payload'))
            if len(payloads) != 1:
                raise SystemExit(f'Unexpected {name} PKG payload layout')
            extract(payloads[0], payload)
            archives = [p for p in payload.iterdir() if p.is_file()]
            if len(archives) != 1:
                raise SystemExit(f'Unexpected {name} gzip payload layout')
            extract(archives[0], unpacked)
            target = bundle / group
            target.mkdir()
            for path in unpacked.rglob(pattern):
                shutil.copy2(path, target / path.name)
        (bundle / 'PingFang').mkdir()
        for source in sources:
            if source['file'].startswith('PingFang'):
                shutil.copy2(args.cache / source['file'], bundle / 'PingFang' / source['file'])
        archive = work / 'emoji.cpio'
        with archive.open('wb') as stream:
            subprocess.run(['rpm2cpio', str(args.emoji_rpm)], stdout=stream, check=True)
        (bundle / 'Emoji').mkdir()
        with archive.open('rb') as stream, (bundle / 'Emoji/AppleColorEmoji.ttf').open('wb') as font:
            subprocess.run(['cpio', '-i', '--to-stdout', './usr/share/fonts/truetype/apple-color-emoji/AppleColorEmoji.ttf'],
                           stdin=stream, stdout=font, check=True)
        for item in expected:
            path = bundle / item['path']
            if not path.is_file() or sha(path) != item['sha256']:
                raise SystemExit(f'Rebuilt font mismatch: {item["path"]}')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(bundle, args.output)
    print(f'Prepared and verified {len(expected)} fonts: {args.output}')


if __name__ == '__main__':
    main()
