import os
import sys


def resource_root():
    """Root for read-only bundled assets (images, fonts, ...). Works both
    running from source and packaged into a PyInstaller exe."""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _data_root():
    """Root for user data (save file, currency, quests, habits, focus...).
    Always %APPDATA%\\Forge, regardless of where the app is run from or
    whether it's a script or a packaged exe, so progress is stable across
    reinstalls/updates and never lands in a temp folder that gets wiped."""
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    root = os.path.join(base, "Forge")
    os.makedirs(root, exist_ok=True)
    return root


class Directory:
    def __init__(self):
        self._resource_root = resource_root()
        self._data_root = _data_root()

    def main(self):
        return self._data_root

    def images_directory(self):
        return os.path.join(self._resource_root, "images")

    def balance_file(self):
        return os.path.join(self._data_root, "balance.txt")

    def history_file(self):
        return os.path.join(self._data_root, "history.txt")

    def focus_file(self):
        return os.path.join(self._data_root, "focus.txt")

    def reward_state_file(self):
        return os.path.join(self._data_root, "reward_state.txt")

    def quest_file(self):
        path = os.path.join(self._data_root, "quests")
        os.makedirs(path, exist_ok=True)
        return path

    def habit_file(self):
        path = os.path.join(self._data_root, "habits")
        os.makedirs(path, exist_ok=True)
        return path