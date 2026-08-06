import os

class Directory:
    def __init__(self):
        self._backend_directory = os.path.dirname(os.path.abspath(__file__))
        self._main_directory = os.path.dirname(self._backend_directory)
        self._currency_directory = None
        self._images_directory = None
        self._home_directory = None
        self._pages_directory = None
        self._focus_directory = None
        self._balance_file = None
        self._history_file = None
        self._focus_file = None
        self._reward_state_file = None
        self._quest_directory = None
        self.quest_folder = None

    def main(self):
        return self._main_directory

    def backend_directory(self):
        return self._backend_directory

    def currency_directory(self):
        self._currency_directory = os.path.join(self._main_directory, "currency")
        return self._currency_directory

    def balance_file(self):
        self._balance_file = os.path.join(self.currency_directory(), "balance.txt")
        return self._balance_file

    def history_file(self):
        self._history_file = os.path.join(self.currency_directory(), "history.txt")
        return self._history_file

    def images_directory(self):
        self._images_directory = os.path.join(self._main_directory, "images")
        return self._images_directory

    def home_directory(self):
        self._home_directory = os.path.join(self._main_directory, "home_back")
        return self._home_directory

    def pages_directory(self):
        self._pages_directory = os.path.join(self._main_directory, "pages")
        return self._pages_directory

    def focus_directory(self):
        self._focus_directory = os.path.join(self._main_directory, "focus")
        return self._focus_directory

    def focus_file(self):
        self._focus_file = os.path.join(self.focus_directory(), "focus.txt")
        return self._focus_file

    def reward_state_file(self):
        self._reward_state_file = os.path.join(self.focus_directory(), "reward_state.txt")
        return self._reward_state_file
    def quest_directory(self):
        self._quest_directory = os.path.join(self._main_directory, "quest")
        return self._quest_directory
    def quest_file(self):
        self._quest_folder = os.path.join(self.quest_directory(), "quests")
        return self._quest_folder
    def habit_directory(self):
        self._habit_directory = os.path.join(self._main_directory, "habit")
        return self._habit_directory
    def habit_file(self):
        self._habit_file = os.path.join(self.habit_directory(), "habits")
        return self._habit_file