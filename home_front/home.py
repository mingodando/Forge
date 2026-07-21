import customtkinter as ctk

from backend.config import Config
from currency.currency import Currency
from focus.focus_card import FocusCard
from pages.home_page import get_home

class HomePage:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.currency = Currency()
        self.focus = FocusCard()
        self.home = get_home()

        #--- Widgets ---#
        self.coin_label = None
        self.coin_display = None
        self.coin_change_display = None
        self.streak_label = None
        self.gear_bonus_label = None
        self.quests_completed_label = None

    def main(self):
        self.coin_frame()
        self.focus_session()

    def coin_frame(self):
        self.coin_label = ctk.CTkLabel(self.home.coins_frame, text="COINS", font=self.config.label_font, text_color=self.config.muted)
        self.coin_label.grid(row=0, column=0, padx=25, pady=(15,0), sticky="w")

        self.coin_display = ctk.CTkLabel(self.home.coins_frame, text=str(self.currency.get_currencies()), font=self.config.heading_font, text_color=self.config.text)
        self.coin_display.grid(row=1, column=0, padx=25, sticky="w")

        net = self.currency.get_today_flow()["net"]
        if net > 0:
            change_text, change_color = f"+{net} today", self.config.green
        elif net < 0:
            change_text, change_color = f"{net} today", self.config.red
        else:
            change_text, change_color = "0 today", self.config.muted

        self.coin_change_display = ctk.CTkLabel(self.home.coins_frame, text=change_text, font=self.config.label_font, text_color=change_color)
        self.coin_change_display.grid(row=2, column=0, padx=25, pady=(0, 10), sticky="w")

        self.streak_label = ctk.CTkLabel(self.home.streak_frame, text="BEST STREAK", font=self.config.label_font, text_color=self.config.muted)
        self.streak_label.grid(row=0, column=0, padx=25, pady=10, sticky="es")

        self.gear_bonus_label = ctk.CTkLabel(self.home.gear_bonus_frame, text="GEAR BONUS", font=self.config.label_font, text_color=self.config.muted)
        self.gear_bonus_label.grid(row=0, column=0, padx=25, pady=10, sticky="es")

        self.quests_completed_label = ctk.CTkLabel(self.home.quests_completed_frame, text="QUESTS DONE", font=self.config.label_font, text_color=self.config.muted)
        self.quests_completed_label.grid(row=0, column=0, padx=25, pady=10, sticky="es")

    def focus_session(self):
        self.focus.create_ring()
        self.focus.create_onboard()