import platform
import sys
import customtkinter as ctk
from tkinter import messagebox, filedialog

from backend.config import Config
from backend.start_setup import get_setup
from pages.settings_page import get_settings
from pages.home_page import get_home
from settings.settings_back import get_settingsback
from quest.quest_front import get_quest_front
from habit.habit_front import get_habitfront
from forge.forge_front import get_forgefront
from shop.shop_front import get_shopfront

_settingsfront_instance = None


def get_settingsfront():
    global _settingsfront_instance
    if _settingsfront_instance is None:
        _settingsfront_instance = SettingsFront()
    return _settingsfront_instance


class SettingsFront:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.settings_page = get_settings()
        self.home_page = get_home()
        self.settings_back = get_settingsback()

    def main(self):
        pass

    def setup_settings_body(self):
        frame = self.settings_page.frame
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Settings", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text).grid(row=0, column=0, padx=35, pady=(30, 0), sticky="w")
        ctk.CTkLabel(frame, text="Preferences & data", font=self.config.body_font, text_color=self.config.muted).grid(row=1, column=0, padx=35, pady=(0, 20), sticky="w")

        rows_card = ctk.CTkFrame(frame, fg_color=self.config.card, corner_radius=16)
        rows_card.grid(row=2, column=0, padx=35, sticky="ew")
        rows_card.grid_columnconfigure(0, weight=1)

        self.build_row(rows_card, 0, "Theme", "Ember Dark (default). Accent and card colors follow the app palette.", "Change", self.on_theme_click, divider=True)
        self.build_row(rows_card, 2, "Back up save", "Copy save.json to a folder of your choice. Do this before reinstalling.", "Export", self.on_export_click, divider=True)
        self.build_row(rows_card, 4, "About", "Forge v1.0 · built with Python + CustomTkinter", "Details", self.on_about_click, divider=False)

        danger_card = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=16, border_width=2, border_color="#4a2320")
        danger_card.grid(row=3, column=0, padx=35, pady=(16, 20), sticky="ew")
        danger_card.grid_columnconfigure(0, weight=1)

        self.build_row(danger_card, 0, "Reset all progress", "Wipes level, coins, materials, gear and streaks. This cannot be undone.", "Reset...", self.on_reset_click, divider=False, title_color=self.config.red, button_color=self.config.red)

    def build_row(self, parent, row, title, description, button_text, command, divider, title_color=None, button_color=None):
        ctk.CTkLabel(parent, text=title, font=self.config.label_font, text_color=title_color or self.config.text).grid(row=row, column=0, padx=20, pady=(16, 0), sticky="w")
        ctk.CTkLabel(parent, text=description, font=self.config.body_font, text_color=self.config.muted).grid(row=row + 1, column=0, padx=20, pady=(0, 16), sticky="w")

        button = ctk.CTkButton(
            parent, text=button_text, font=self.config.button_font, width=100, corner_radius=10,
            fg_color="transparent", hover_color=self.config.card_hi,
            text_color=button_color or self.config.gold,
            border_width=2, border_color=button_color or self.config.gold,
            command=command,
        )
        button.grid(row=row, column=1, rowspan=2, padx=20, pady=16, sticky="e")

        if divider:
            ctk.CTkFrame(parent, height=1, fg_color=self.config.card_hi).grid(row=row + 2, column=0, columnspan=2, padx=20, sticky="ew")

    #--- Actions ---#
    def on_theme_click(self):
        messagebox.showinfo("Theme", "Ember Dark is the only theme available right now — more palettes are on the way.")

    def on_export_click(self):
        dest_folder = filedialog.askdirectory(title="Choose a backup folder")
        if not dest_folder:
            return
        self.settings_back.export_save(dest_folder)
        messagebox.showinfo("Backup complete", f"save.json was copied to:\n{dest_folder}")

    def on_about_click(self):
        messagebox.showinfo(
            "About Forge",
            f"Forge v1.0\nBuilt with Python {platform.python_version()} + CustomTkinter\nRunning on {sys.platform}",
        )

    def on_reset_click(self):
        confirmed = messagebox.askyesno(
            "Reset all progress",
            "This wipes your level, coins, materials, gear and streaks. This cannot be undone. Continue?",
            icon="warning",
        )
        if not confirmed:
            return

        self.settings_back.reset_all_progress()
        self.refresh_everything()
        messagebox.showinfo("Reset complete", "Your progress has been wiped.")

    def refresh_everything(self):
        get_quest_front().refresh_max_slots()
        get_habitfront().refresh_max_slots()
        get_habitfront().refresh_habit_topbar()
        forge_front = get_forgefront()
        forge_front.refresh_badges()
        render_body = getattr(forge_front, "render_body", None)
        if render_body is not None and forge_front.list_frame is not None:
            render_body()

        get_shopfront().render_cards()

        refresh_materials_and_gear = getattr(self.home_page, "refresh_materials_and_gear", None)
        if refresh_materials_and_gear is not None:
            refresh_materials_and_gear()

        refresh_level = getattr(self.home_page, "refresh_level", None)
        if refresh_level is not None:
            refresh_level()

        coin_display = self.home_page.coin_display
        coin_change_display = self.home_page.coin_change_display
        topbar_coin_display = self.home_page.topbar_coin_display
        if coin_display is not None:
            coin_display.configure(text="0")
        if topbar_coin_display is not None:
            topbar_coin_display.configure(text="0")
        if coin_change_display is not None:
            coin_change_display.configure(text="0 today", text_color=self.config.muted)
