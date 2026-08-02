import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup
from backend.directory_setup import Directory

_quest_instance = None

TIER_LEVEL = {
    "easy": 10,
    "medium": 20,
    "hard": 30,
}

def get_quest():
    global _quest_instance
    if _quest_instance is None:
        _quest_instance = Quest()
    return _quest_instance

class Quest:
    def __init__(self):
        self.config = Config()
        self.directory = Directory()
        self.config.main()
        self.setup = get_setup()

        self.frame = None
        self.topbar_frame = None

    def main(self):
        self.frame = ctk.CTkFrame(self.setup.content_frame, width=1120, height=680, fg_color=self.config.bg, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_propagate(False)

        self.topbar_frame = ctk.CTkFrame(self.setup.topbar, width=1120, height=680, fg_color=self.config.bg)
        self.topbar_frame.grid(row=0, column=0, sticky="nsew")

