import customtkinter as ctk

from config import Config
from start_setup import Setup

class Home:
    def __init__(self):
        self.config = Config()
        self.setup = Setup()

        #--- Widgets ---#
        self.level_label = None

    def main(self):
        self.create_widgets()
    def create_widgets(self):
        pass
    def setup_home_page(self):
        self.create_widgets()