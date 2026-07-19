import os

class Directory:
    def __init__(self):
        self._main_directory = None
        self._backend_directory = None
        self._currency_directory = None
        self._images_directory = None
        self._home_directory = None
        self._pages_directory = None

    def main(self):
        self._main_directory = os.getcwd().strip(r'\backend')
        return self._main_directory

    def backend_directory(self):
        self._backend_directory = os.getcwd()
        return self._backend_directory

    def currency_directory(self):
        self._currency_directory = os.getcwd().strip(r'\backend')+r"\currency"
        return self._currency_directory

    def images_directory(self):
        self._images_directory = os.getcwd().strip(r'\backend')+r"\images"
        return self._images_directory

    def home_directory(self):
        self._home_directory = os.getcwd().strip(r'\backend')+r"\home_back"
        return self._home_directory

    def pages_directory(self):
        self._pages_directory = os.getcwd().strip(r'\backend')+r"\pages"
        return self._pages_directory
