import customtkinter as ctk

from backend.config import Config
from backend.start_setup import Setup

class Home:
    def __init__(self, setup):
        self.config = Config()
        self.config.main()
        self.setup = setup

        #--- Widgets ---#
        self.level_label = None

        #--- Frames ---#
        self.focus_frame = None
        self.xpbar_frame = None
        self.coins_frame = None
        self.streak_frame = None
        self.gear_bonus_frame = None
        self.quests_completed_frame = None
        self.four_frames = None

    def main(self):
        self.focus_frame = ctk.CTkFrame(self.setup.content_frame, width=1050, height=200, fg_color=self.config.home_color, corner_radius=30)
        self.focus_frame.grid(row=0, column=0, padx=35, sticky="nsew")

        self.xpbar_frame = ctk.CTkFrame(self.setup.content_frame, width=1050, height=50, fg_color=self.config.home_color, corner_radius=30)
        self.xpbar_frame.grid(row=1, column=0, padx=35, pady=20, sticky="nsew")

        self.four_frames = ctk.CTkFrame(self.setup.content_frame, width=1050, height=150, fg_color="red", corner_radius=30)
        self.four_frames.grid(row=2, column=0, padx=35, sticky="nsew")

        self.four_frames.grid_propagate(False)

        self.coins_frame = ctk.CTkFrame(self.four_frames, width=240, height=130, fg_color=self.config.home_color, corner_radius=30)
        self.coins_frame.grid(row=0, column=0, pady=10, padx=(15, 10), sticky="nsew")

        self.streak_frame = ctk.CTkFrame(self.four_frames, width=240, height=130, fg_color=self.config.home_color, corner_radius=30)
        self.streak_frame.grid(row=0, column=1, pady=10, padx=(10, 10), sticky="nsew")

        self.gear_bonus_frame = ctk.CTkFrame(self.four_frames, width=240, height=130, fg_color=self.config.home_color, corner_radius=30)
        self.gear_bonus_frame.grid(row=0, column=2, pady=10, padx=(10, 10), sticky="nsew")

        self.quests_completed_frame = ctk.CTkFrame(self.four_frames, width=240, height=130, fg_color=self.config.home_color, corner_radius=30)
        self.quests_completed_frame.grid(row=0, column=3, pady=10, padx=(10, 15), sticky="nsew")

        self.focus_frame.tkraise()