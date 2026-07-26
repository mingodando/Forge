import customtkinter as ctk

from backend.config import Config
from pages.quest_page import get_quest

class QuestFront:
    def __init__(self, data_file_name):
        self.config = Config()
        self.quest_page = get_quest()
        self.data_file_name = data_file_name

    def main(self):
        pass

    def quest_topbar(self):
        self.quest_label = ctk.CTkLabel(self.quest_page.frame, text="Quests", font=self.config.body_font, text_color=self.config.muted)
        self.quest_label.grid(row=0, column=0, )