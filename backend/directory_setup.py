import os

class Directory:
    def __init__(self):
        self._backend_directory = os.path.dirname(os.path.abspath(__file__))
        self._main_directory = os.path.dirname(self._backend_directory)
        self._currency_directory = None
        self._images_directory = None
        self._home_directory = None
        self._pages_directory = None
        self._balance_file = None
        self._history_file = None

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
