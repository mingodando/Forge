import customtkinter as ctk

from backend.config import Config
from currency.currency import Currency
from focus.focus_card import FocusCard
from pages.home_page import get_home
from backend.start_setup import get_setup
from quest.quest_back import QuestBack
from quest.quest_front import get_quest_front
from home_back.clock import Time

class HomePage:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.currency = Currency()
        self.focus = FocusCard()
        self.time = Time()
        self.quest_back = QuestBack()
        self.quest_front = get_quest_front()
        self.setup = get_setup()
        self.home = get_home()

        #--- Widgets ---#
        self.coin_label = None
        self.coin_display = None
        self.coin_change_display = None
        self.streak_label = None
        self.gear_bonus_label = None
        self.quests_completed_label = None
        self.onboard_display1 = None
        self.onboard_display2 = None
        self.onboard_display3 = None

        self.bottom_row_frame = None
        self.quest_section_frame = None
        self.section_title_label = None
        self.section_hint_label = None
        self.list_frame = None
        self.materials_frame = None
        self.materials_label = None

        #--- Topbar ---#
        self.home_topbar = None

    def main(self):
        self.coin_frame()
        self.focus_session()
        self.home_setup_quest_list()

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

        # Shared with FocusCard (holds the same Home singleton) so it can refresh the coin display live.
        self.home.coin_display = self.coin_display
        self.home.coin_change_display = self.coin_change_display

        self.streak_label = ctk.CTkLabel(self.home.streak_frame, text="BEST STREAK", font=self.config.label_font, text_color=self.config.muted)
        self.streak_label.grid(row=0, column=0, padx=25, pady=10, sticky="es")

        self.gear_bonus_label = ctk.CTkLabel(self.home.gear_bonus_frame, text="GEAR BONUS", font=self.config.label_font, text_color=self.config.muted)
        self.gear_bonus_label.grid(row=0, column=0, padx=25, pady=10, sticky="es")

        self.quests_completed_label = ctk.CTkLabel(self.home.quests_completed_frame, text="QUESTS DONE", font=self.config.label_font, text_color=self.config.muted)
        self.quests_completed_label.grid(row=0, column=0, padx=25, pady=10, sticky="es")

    def focus_session(self):
        self.focus.create_ring()
        self.focus.create_onboard()
        self.focus.focus_today()

    def setup_topbar(self):
        self.setup.topbar.columnconfigure(0, weight=1)
        self.setup.topbar.rowconfigure(0, weight=1)

        self.home_topbar = ctk.CTkFrame(self.setup.topbar, fg_color=self.config.bg)
        self.home_topbar.grid(row=0, column=0, sticky="nsew")
        self.home_topbar.columnconfigure(0, weight=1)

        self.onboard_display1 = ctk.CTkLabel(self.home_topbar, text=self.time.print_date(), font=self.config.body_font, text_color=self.config.muted)
        self.onboard_display1.grid(row=0, column=0, padx=20, pady=(10,0), sticky="w")

        self.onboard_display2 = ctk.CTkLabel(self.home_topbar, text=self.time.print_time(), font=self.config.heading_font, text_color=self.config.text)
        self.onboard_display2.grid(row=1, column=0, padx=20, sticky="wn")

        self.onboard_display3 = ctk.CTkLabel(self.home_topbar, text=self.quest_back.quest_display(), font=ctk.CTkFont("Space Grotesk", 13 ), text_color=self.config.muted)
        self.onboard_display3.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")

        coin_badge = ctk.CTkFrame(self.home_topbar, fg_color=self.config.bg, corner_radius=20, height=40)
        coin_badge.grid(row=0, column=3, rowspan=2, padx=(20, 30), pady=10, sticky="e")
        coin_badge.grid_propagate(False)
        coin_badge.columnconfigure(0, weight=1)
        coin_badge.rowconfigure(0, weight=1)

        coin_icon = ctk.CTkLabel(coin_badge, text="●", font=ctk.CTkFont("Space Grotesk", 24), text_color=self.config.gold)
        coin_icon.grid(row=0, column=0, padx=(18, 8), pady=8, sticky="e")
        coin_display = ctk.CTkLabel(coin_badge, text=str(self.currency.get_currencies()), font=ctk.CTkFont("Space Grotesk", 24, "bold"), text_color=self.config.text)
        coin_display.grid(row=0, column=1, padx=(0, 18), pady=8, sticky="w")

    def home_setup_quest_list(self):
        self.bottom_row_frame = ctk.CTkFrame(self.home.frame, width=1050, height=230, fg_color=self.config.bg, corner_radius=0)
        self.bottom_row_frame.grid(row=3, column=0, padx=35, pady=(20, 0), sticky="nsew")
        self.bottom_row_frame.grid_propagate(False)
        self.bottom_row_frame.grid_columnconfigure(0, weight=0)
        self.bottom_row_frame.grid_columnconfigure(1, weight=0)
        self.bottom_row_frame.grid_rowconfigure(0, weight=1)

        quest_width = 630
        materials_width = 400

        self.quest_section_frame = ctk.CTkFrame(self.bottom_row_frame, width=quest_width, fg_color=self.config.card, corner_radius=30)
        self.quest_section_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.quest_section_frame.grid_propagate(False)
        self.quest_section_frame.grid_columnconfigure(0, weight=1)
        self.quest_section_frame.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.quest_section_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        self.section_title_label = ctk.CTkLabel(header_frame, text="STILL OPEN TODAY", font=self.config.label_font, text_color=self.config.muted)
        self.section_title_label.grid(row=0, column=0, sticky="w")

        self.section_hint_label = ctk.CTkLabel(header_frame, text="Tap the circle to complete", font=self.config.body_font, text_color=self.config.gold)
        self.section_hint_label.grid(row=0, column=1, sticky="e")

        self.list_frame = ctk.CTkScrollableFrame(self.quest_section_frame, width=quest_width - 20, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.quest_front.setup_home_quest_list(self.list_frame)

        #--- Materials (placeholder) ---#
        self.materials_frame = ctk.CTkFrame(self.bottom_row_frame, width=materials_width, fg_color=self.config.card, corner_radius=30)
        self.materials_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        self.materials_frame.grid_propagate(False)
        self.materials_frame.grid_columnconfigure(0, weight=1)

        self.materials_label = ctk.CTkLabel(self.materials_frame, text="MATERIALS", font=self.config.label_font, text_color=self.config.muted)
        self.materials_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
