#!/usr/bin/env python3
"""User-level, offline Fedora KDE font installation and rollback."""
import argparse
import configparser
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PROJECT = Path(__file__).resolve().parent
CONFIG = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
DATA = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local/share'))
STATE = Path(os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state')) / 'fedora-kde-apple-front'
FONTDIR = DATA / 'fonts/apple-font-trial'
CONF = CONFIG / 'fontconfig/conf.d/60-apple-font-trial.conf'
KDE = CONFIG / 'kdeglobals'
ACTIVE = STATE / 'active.json'
KEYS = [('General', k) for k in ['font', 'menuFont', 'toolBarFont', 'smallestReadableFont', 'fixed']] + [('WM', 'activeFont')]


def run(args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, text=True, **kwargs)


def output(args):
    return run(args, stdout=subprocess.PIPE).stdout.strip()


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


def read_kde():
    data = configparser.RawConfigParser(strict=False, interpolation=None)
    data.optionxform = str
    data.read(KDE)
    return data


def need_tools():
    for tool in ['fc-cache', 'fc-match', 'fc-scan', 'kwriteconfig6', 'kreadconfig6']:
        if not shutil.which(tool):
            raise RuntimeError(f'Missing dependency: {tool}; see README.md')


def check_bundle():
    files = json.loads((PROJECT / 'fonts-manifest.json').read_text())
    for item in files:
        path = PROJECT / 'fonts' / item['path']
        if not path.is_file() or digest(path) != item['sha256']:
            raise RuntimeError(f'Missing or changed font: {path}; see prepare-fonts.py')
    print(f'Font checksums OK: {len(files)} files')
    return files


def notify(disabled=False):
    if disabled:
        return
    try:
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtDBus import QDBusConnection, QDBusMessage
        app = QCoreApplication.instance() or QCoreApplication([])
        QDBusConnection.sessionBus().send(QDBusMessage.createSignal(
            '/KDEPlatformTheme', 'org.kde.KDEPlatformTheme', 'refreshFonts'))
        app.processEvents()
        if shutil.which('qdbus-qt6'):
            subprocess.run(['qdbus-qt6', 'org.kde.KWin', '/KWin', 'reconfigure'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as error:
        print(f'Desktop refresh unavailable ({error}); log out and back in to apply.')


def verify():
    expectations = [
        ('sans-serif:lang=en', 'SF Pro Text'),
        ('SF Pro Text:charset=4e2d', 'PingFang SC'),
        ('SF Pro Text:charset=4e2d:weight=bold', 'PingFang SC'),
        ('monospace:lang=en', 'SF Mono'),
        ('SF Mono:charset=4e2d', 'Noto Sans Mono CJK SC'),
        ('emoji:charset=1f600', 'Apple Color Emoji'),
        ('Noto Color Emoji', 'Noto Color Emoji'),
    ]
    failures = []
    for pattern, expected in expectations:
        result = output(['fc-match', '-f', '%{family}|%{style}|%{file}', pattern])
        ok = expected in result.split('|')[0].split(',')
        print(f'{"PASS" if ok else "FAIL"} {pattern}: {result}')
        if not ok:
            failures.append(pattern)
    if failures:
        raise RuntimeError('Font matching failed: ' + ', '.join(failures))


def restore(manifest, no_notify):
    # Refuse a copied state file targeting another account/configuration.
    if manifest['fontdir'] != str(FONTDIR) or manifest['fontconfig'] != str(CONF):
        raise RuntimeError('State belongs to different XDG directories; use the original environment.')
    current = read_kde()
    for item in manifest['kde_keys']:
        group, key = item['group'], item['key']
        if current.get(group, key, fallback=None) != item['applied']:
            print(f'Preserved later change: {group}/{key}')
            continue
        args = ['kwriteconfig6', '--file', KDE, '--group', group, '--key', key]
        args += ['--delete'] if item['previous'] is None else [item['previous']]
        run(args)
    backup = Path(manifest['backup'])
    for path in [CONF, FONTDIR]:
        if path.exists():
            destination = backup / ('disabled-' + path.name)
            if destination.exists():
                raise RuntimeError(f'Rollback destination already exists: {destination}')
            shutil.move(str(path), destination)
    run(['fc-cache', '-f'])
    notify(no_notify)
    manifest['status'] = 'rolled_back'
    save(ACTIVE, manifest)
    save(backup / 'manifest.json', manifest)
    print(f'Rolled back. Files retained in {backup}')


def install(args):
    files = check_bundle()
    need_tools()
    from PySide6.QtGui import QFont
    print(f'Fonts: {FONTDIR}\nFontconfig: {CONF}\nKDE: {KDE}\nBackups: {STATE}')
    if ACTIVE.exists():
        active = json.loads(ACTIVE.read_text())
        if active['status'] == 'installed':
            print('Already installed. Run verify or rollback; no files changed.')
            return
        if active['status'] == 'installing':
            raise RuntimeError('An interrupted installation exists. Run rollback first.')
    if FONTDIR.exists() or CONF.exists():
        if args.dry_run:
            print('Existing trial detected; installation would stop without overwriting it.')
            return
        raise RuntimeError('Existing trial paths are not owned by this installer. See README: current-machine rollback.')
    current = read_kde()
    edits = []
    for group, key in KEYS:
        default = 'Noto Sans,8,-1,5,50,0,0,0,0,0' if key == 'smallestReadableFont' else 'Noto Sans,10,-1,5,50,0,0,0,0,0'
        effective = output(['kreadconfig6', '--file', 'kdeglobals', '--group', group, '--key', key]) or default
        font = QFont()
        if not font.fromString(effective):
            raise RuntimeError(f'Cannot parse existing font {group}/{key}: {effective}')
        font.setFamily('SF Mono' if key == 'fixed' else 'SF Pro Text')
        font.setStyleName('Regular')
        edits.append({'group': group, 'key': key, 'previous': current.get(group, key, fallback=None),
                      'effective_before': effective, 'applied': font.toString()})
    if args.dry_run:
        print(json.dumps(edits, ensure_ascii=False, indent=2))
        print('Dry run complete; no files changed.')
        return
    backup = STATE / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True)
    if KDE.exists():
        shutil.copy2(KDE, backup / 'kdeglobals.before')
    manifest = {'status': 'installing', 'fontdir': str(FONTDIR), 'fontconfig': str(CONF),
                'backup': str(backup), 'kde_keys': edits, 'files': files}
    save(ACTIVE, manifest)
    save(backup / 'manifest.json', manifest)
    try:
        FONTDIR.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(PROJECT / 'fonts', FONTDIR)
        CONF.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PROJECT / 'config' / CONF.name, CONF)
        run(['fc-cache', '-f', FONTDIR])
        verify()
        for item in edits:
            run(['kwriteconfig6', '--file', KDE, '--group', item['group'], '--key', item['key'], item['applied']])
        manifest['status'] = 'installed'
        save(ACTIVE, manifest)
        save(backup / 'manifest.json', manifest)
    except Exception:
        print('Installation failed; restoring this attempt.', file=sys.stderr)
        restore(manifest, args.no_notify)
        raise
    notify(args.no_notify)
    print('Installed. Restart applications, or log out and back in; a reboot is unnecessary.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['install', 'verify', 'status', 'rollback'])
    parser.add_argument('--dry-run', action='store_true', help='install: inspect without writing')
    parser.add_argument('--no-notify', action='store_true', help='skip desktop D-Bus notifications (isolated testing)')
    args = parser.parse_args()
    if args.dry_run and args.command != 'install':
        parser.error('--dry-run is only valid with install')
    if args.command == 'install':
        install(args)
    elif args.command == 'verify':
        verify()
    elif args.command == 'status':
        print(f'Fonts: {FONTDIR} ({"present" if FONTDIR.exists() else "absent"})')
        print(f'Config: {CONF} ({"present" if CONF.exists() else "absent"})')
        print(ACTIVE.read_text() if ACTIVE.exists() else 'No new installer state. The original trial uses history/rollback-font-trial.py.')
    elif ACTIVE.exists():
        manifest = json.loads(ACTIVE.read_text())
        if manifest['status'] == 'rolled_back':
            print('Already rolled back.')
        else:
            restore(manifest, args.no_notify)
    else:
        raise RuntimeError('No installer state; see README for current-machine original-trial rollback.')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
