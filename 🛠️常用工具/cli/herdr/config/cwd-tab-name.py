"""Give generated Herdr tab labels the shell's directory name."""
import json
import fcntl
import hashlib
import os
from pathlib import Path
import subprocess
import sys


def herdr(*args):
    result = subprocess.run(
        ["herdr", *args], capture_output=True, text=True, timeout=2, check=True
    )
    return json.loads(result.stdout)["result"]


def update_label(tab_id, label, name, old_name, state):
    if state.get("manual"):
        return
    last = state.get("last_label")
    if last is not None and label != last:
        # Once overridden, even numeric or directory-like manual names stay put.
        state["manual"] = True
        return
    if last is None and not (label.isdecimal() or label in (old_name, name)):
        state["manual"] = True
        return
    if label != name:
        herdr("tab", "rename", tab_id, name)
    state["last_label"] = name


def main():
    if os.environ.get("HERDR_ENV") != "1":
        return
    cwd = sys.argv[1]
    previous = sys.argv[2]
    name = os.path.basename(cwd.rstrip("/")) or "/"
    old_name = os.path.basename(previous.rstrip("/")) or "/"
    pane = herdr("pane", "current", "--current")["pane"]
    tab_id = pane["tab_id"]
    # Share ownership across shells in split panes and persist manual overrides.
    # Socket identity keeps new server sessions from inheriting old tab IDs.
    socket = Path(os.environ.get("HERDR_SOCKET_PATH", str(Path.home() / ".config/herdr/herdr.sock")))
    identity = [str(socket), str(socket.stat().st_ino), str(socket.stat().st_mtime_ns),
                os.environ.get("HERDR_SESSION", ""), tab_id]
    key = hashlib.sha256("\0".join(identity).encode()).hexdigest()
    directory = Path.home() / ".cache/herdr/cwd-tab-names"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (directory / (key + ".lock")).open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state_path = directory / (key + ".json")
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        tab = herdr("tab", "get", tab_id)["tab"]
        update_label(tab_id, tab["label"], name, old_name, state)
        temporary = state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state))
        temporary.replace(state_path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        # A missing/stopped session must never break an interactive prompt.
        pass
