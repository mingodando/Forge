import customtkinter as ctk
import ctypes

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
        self.title_label = None
        self.subtitle_label = None
        self.slots_frame = None
        self.slots_count_label = None
        self.slots_text_label = None
        self.new_quest_button = None

        #--- New Quest Widgets ---#
        self.name_entry = None
        self.category_frame = None
        self.popup = None
        self.category_buttons = []
        self.selected_category = None

    def main(self):
        pass

    def setup_topbar(self):
        self.title_label = ctk.CTkLabel(self.quest_page.topbar_frame, text="Quests", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text)
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        self.subtitle_label = ctk.CTkLabel(self.quest_page.topbar_frame, text="One-time tasks · complete for XP, coins & materials", font=self.config.body_font, text_color=self.config.muted)
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.slots_frame = ctk.CTkFrame(self.quest_page.topbar_frame, fg_color=self.config.bg)
        self.slots_frame.grid(row=0, column=1, rowspan=2, padx=(20, 2), pady=15, sticky="e")

        self.slots_count_label = ctk.CTkLabel(self.slots_frame, text=f"{self.slots_used} / {self.max_slots}", font=self.config.body_font, text_color=self.config.gold)
        self.slots_count_label.grid(row=0, column=0, sticky="e")

        self.slots_text_label = ctk.CTkLabel(self.slots_frame, text=" slots used", font=self.config.body_font, text_color=self.config.muted)
        self.slots_text_label.grid(row=0, column=1, padx=(0,4), sticky="e")

        self.new_quest_button = ctk.CTkButton(self.quest_page.topbar_frame, text="+ New quest", font=self.config.button_font,
                                              fg_color=self.config.ember, hover_color=self.config.gold,
                                              text_color=self.config.nav, corner_radius=20, command=lambda: self.create_quest())
        self.new_quest_button.grid(row=0, column=2, rowspan=2, padx=(0, 30), pady=15, sticky="e")

        self.quest_page.topbar_frame.grid_columnconfigure(1, weight=1)

    def select_category(self, cat):
        self.selected_category = cat
        for btn_cat, btn in self.category_buttons:
            if btn_cat == cat:
                btn.configure(fg_color=self.config.ember, border_color=self.config.ember, text_color=self.config.nav)
            else:
                btn.configure(fg_color=self.config.card_hi, border_color=self.config.card_hi, text_color=self.config.text)

    def create_quest(self):
        self.popup = ctk.CTkToplevel(self.quest_page.frame)
        self.popup.title("New Quest")
        self.popup.geometry("420x460")
        self.popup.configure(fg_color=self.config.card)
        self.popup.transient(self.quest_page.frame.winfo_toplevel())
        self.popup.grab_set()
        self.popup.grid_columnconfigure(0, weight=1)

        self.popup.update()
        # noinspection PyUnresolvedReferences
        hwnd = ctypes.windll.user32.GetParent(self.popup.winfo_id())
        dark_mode = ctypes.c_int(1)
        # noinspection PyUnresolvedReferences
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode))

        ctk.CTkLabel(self.popup, text="NAME", font=self.config.body_font, text_color=self.config.muted).grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.name_entry = ctk.CTkEntry(self.popup, font=self.config.body_font, text_color=self.config.text, fg_color=self.config.bg, corner_radius=8)
        self.name_entry.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="ew")

        ctk.CTkLabel(self.popup, text="CATEGORY", font=self.config.body_font, text_color=self.config.muted).grid(row=2, column=0, padx=20, pady=(0, 5), sticky="w")

        self.category_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        self.category_frame.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.category_buttons = []
        for i, cat in enumerate(["Social", "Work", "Study", "Exercise"]):
            btn = ctk.CTkButton(self.category_frame, text=cat, font=self.config.body_font,
                         fg_color=self.config.card_hi, text_color=self.config.text, hover_color=self.config.card,
                         border_width=2, border_color=self.config.card_hi, corner_radius=8, command=lambda c=cat: self.select_category(c))
            btn.grid(row=0, column=i, padx=(0, 4) if i < 3 else 0, sticky="ew")
            self.category_frame.grid_columnconfigure(i, weight=1)
            self.category_buttons.append((cat, btn))


_quest_front_instance = None

def get_quest_front():
    global _quest_front_instance
    if _quest_front_instance is None:
        _quest_front_instance = QuestFront()
    return _quest_front_instance