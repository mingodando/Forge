import json
import os
import shutil

from backend.config import Config
from backend.directory_setup import Directory
from currency.currency import Currency

_settingsback_instance = None


def get_settingsback():
    global _settingsback_instance
    if _settingsback_instance is None:
        _settingsback_instance = SettingsBack()
    return _settingsback_instance


class SettingsBack:
    def __init__(self):
        self.config = Config()
        self.directory = Directory()
        self.currency = Currency()

    def main(self):
        pass

    def save_path(self):
        return os.path.join(self.directory.main(), "save.json")

    def export_save(self, dest_folder):
        shutil.copy(self.save_path(), os.path.join(dest_folder, "save.json"))

    def reset_all_progress(self):
        default_data = {
            "username": "",
            "level": 0,
            "xp": 0,
            "max_quests": 5,
            "max_habits": 3,
            "materials": {"Wood": 0, "Stone": 0, "Clay": 0, "Iron": 0},
            "gear": {"smelted": [], "equipped": {}},
            "shield_charges": 1,
            "streaks": 0,
            "history": [],
        }
        with open(self.save_path(), "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)

        self.currency.write_balance(0)
        history_path = self.directory.history_file()
        with open(history_path, "w") as f:
            f.write("")

        for directory_getter in (self.directory.quest_file, self.directory.habit_file):
            folder = directory_getter()
            if os.path.isdir(folder):
                for fname in os.listdir(folder):
                    os.remove(os.path.join(folder, fname))
