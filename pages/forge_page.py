import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup

_forge_instance = None

def get_forge():
    global _forge_instance
    if _forge_instance is None:
        _forge_instance = Forge()
    return _forge_instance

class Forge:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()

        self.frame = None
        self.topbar_frame = None

    def main(self):
        self.frame = ctk.CTkFrame(self.setup.content_frame, width=1120, height=780, fg_color=self.config.bg, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_propagate(False)

        self.topbar_frame = ctk.CTkFrame(self.setup.topbar, width=1120, height=780, fg_color=self.config.bg)
        self.topbar_frame.grid(row=0, column=0, sticky="nsew")
