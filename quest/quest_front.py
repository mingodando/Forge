import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup
from pages.quest_page import get_quest

class QuestFront:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.quest_page = get_quest()

        self.slots_used = 2
        self.max_slots = 5

        #--- Topbar ---#
        self.quest_topbar = None
        self.title_label = None
        self.subtitle_label = None
        self.slots_frame = None
        self.slots_count_label = None
        self.slots_text_label = None
        self.new_quest_button = None

    def main(self):
        pass

    def setup_topbar(self):
        self.setup.topbar.columnconfigure(0, weight=1)
        self.setup.topbar.rowconfigure(0, weight=1)

        self.quest_topbar = ctk.CTkFrame(self.setup.topbar, fg_color=self.config.bg)
        self.quest_topbar.grid(row=0, column=0, sticky="nsew")
        self.quest_topbar.columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.quest_topbar, text="Quests", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text)
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        self.subtitle_label = ctk.CTkLabel(self.quest_topbar, text="One-time tasks · complete for XP, coins & materials", font=self.config.body_font, text_color=self.config.muted)
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.slots_frame = ctk.CTkFrame(self.quest_topbar, fg_color=self.config.bg)
        self.slots_frame.grid(row=0, column=1, padx=(20, 10), pady=(15, 0), sticky="e")

        self.slots_count_label = ctk.CTkLabel(self.slots_frame, text=f"{self.slots_used} / {self.max_slots}", font=self.config.body_font, text_color=self.config.gold)
        self.slots_count_label.grid(row=0, column=0, sticky="e")

        self.slots_text_label = ctk.CTkLabel(self.slots_frame, text=" slots used", font=self.config.body_font, text_color=self.config.muted)
        self.slots_text_label.grid(row=0, column=1, sticky="e")

        self.new_quest_button = ctk.CTkButton(self.quest_topbar, text="+ New quest", font=self.config.button_font,
                                              fg_color=self.config.ember, hover_color=self.config.gold,
                                              text_color=self.config.nav, corner_radius=20)
        self.new_quest_button.grid(row=0, column=2, rowspan=2, padx=(10, 30), pady=15, sticky="e")