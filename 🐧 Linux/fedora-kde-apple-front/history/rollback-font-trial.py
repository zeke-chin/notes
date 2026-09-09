#!/usr/bin/env python3
"""Undo this trial's font settings while preserving unrelated KDE settings."""
import configparser
import json
import shutil
import subprocess
from pathlib import Path


def main():
    project = Path(__file__).resolve().parent
    state = project / 'original-state'
    manifest_path = state / 'installed.json'
    if not manifest_path.exists():
        raise SystemExit('No installed trial recorded; nothing to roll back.')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('rolled_back'):
        print('This trial has already been rolled back.')
        return
    current = configparser.RawConfigParser(strict=False)
    current.optionxform = str
    current.read(Path.home() / '.config/kdeglobals')
    for item in manifest['kde_keys']:
        group, key = item['group'], item['key']
        if current.get(group, key, fallback=None) != item['applied']:
            print(f'Preserved subsequently changed KDE setting: {group}/{key}')
            continue
        args = ['kwriteconfig6', '--file', 'kdeglobals', '--group', group, '--key', key]
        args += ['--delete'] if item['previous'] is None else [item['previous']]
        subprocess.run(args, check=True)
    # Move only this trial's dedicated paths out of the active font locations.
    for label in ['fontconfig', 'fontdir']:
        path = Path(manifest[label])
        if path.exists():
            shutil.move(str(path), str(state / ('disabled-' + path.name)))
    subprocess.run(['fc-cache', '-f'], check=True)
    try:
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtDBus import QDBusConnection, QDBusMessage
        app = QCoreApplication([])
        bus = QDBusConnection.sessionBus()
        bus.send(QDBusMessage.createSignal('/KDEPlatformTheme', 'org.kde.KDEPlatformTheme', 'refreshFonts'))
        app.processEvents()
    except ImportError:
        pass
    subprocess.run(['qdbus-qt6', 'org.kde.KWin', '/KWin', 'reconfigure'], check=False)
    manifest['rolled_back'] = True
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print('Original font settings restored. Restart applications to refresh their font caches.')
    print(f'Backups and disabled trial fonts: {state}')


if __name__ == '__main__':
    main()
