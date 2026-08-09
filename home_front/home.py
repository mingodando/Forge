import customtkinter as ctk

from backend.config import Config
from backend.leveling import get_level_info
from currency.currency import Currency
from focus.focus_card import FocusCard
from pages.home_page import get_home
from backend.start_setup import get_setup
from quest.quest_back import QuestBack
from quest.quest_front import get_quest_front
from habit.habit_back import get_habitback
from forge.forge_back import get_forgeback, GEAR_CATALOG, GEAR_SLOTS
from home_back.clock import Time

MATERIAL_ICON = {"Wood": "\U0001FAB5", "Stone": "\U0001FAA8", "Clay": "\U0001F9F1", "Iron": "⛓"}
GEAR_SLOT_DISPLAY_COUNT = 6

class HomePage:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.currency = Currency()
        self.focus = FocusCard()
        self.time = Time()
        self.quest_back = QuestBack()
        self.quest_front = get_quest_front()
        self.habit_back = get_habitback()
        self.forge_back = get_forgeback()
        self.setup = get_setup()
        self.home = get_home()

        #--- Widgets ---#
        self.coin_label = None
        self.coin_display = None
        self.coin_change_display = None
        self.streak_label = None
        self.streak_value_label = None
        self.streak_sub_label = None
        self.gear_bonus_label = None
        self.gear_bonus_value_label = None
        self.gear_bonus_sub_label = None
        self.quests_completed_label = None
        self.quests_completed_value_label = None
        self.quests_completed_sub_label = None
        self.onboard_display1 = None
        self.onboard_display2 = None
        self.onboard_display3 = None

        #--- Level / XP bar ---#
        self.level_label = None
        self.title_label = None
        self.xp_progress_bar = None
        self.xp_text_label = None
        self.unlock_hint_label = None

        self.bottom_row_frame = None
        self.quest_section_frame = None
        self.section_title_label = None
        self.section_hint_label = None
        self.list_frame = None
        self.right_column_frame = None
        self.materials_frame = None
        self.materials_label = None
        self.material_value_labels = {}
        self.gear_frame = None
        self.gear_label = None
        self.gear_hint_label = None
        self.gear_slot_labels = []

        #--- Topbar ---#
        self.home_topbar = None

    def main(self):
        self.coin_frame()
        self.setup_xp_bar()
        self.focus_session()
        self.home_setup_quest_list()
        self.refresh_streak_and_gear()
        self.refresh_level()
        self.refresh_materials_and_gear()

        self.home.refresh_materials_and_gear = self.refresh_materials_and_gear
        self.home.refresh_level = self.refresh_level
        self.home.refresh_streak_and_gear = self.refresh_streak_and_gear

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
        self.streak_label.grid(row=0, column=0, padx=25, pady=(15, 0), sticky="w")
        self.streak_value_label = ctk.CTkLabel(self.home.streak_frame, text="0 days", font=self.config.heading_font, text_color=self.config.text)
        self.streak_value_label.grid(row=1, column=0, padx=25, sticky="w")
        self.streak_sub_label = ctk.CTkLabel(self.home.streak_frame, text="No habits yet", font=self.config.body_font, text_color=self.config.muted)
        self.streak_sub_label.grid(row=2, column=0, padx=25, pady=(0, 10), sticky="w")

        self.gear_bonus_label = ctk.CTkLabel(self.home.gear_bonus_frame, text="GEAR BONUS", font=self.config.label_font, text_color=self.config.muted)
        self.gear_bonus_label.grid(row=0, column=0, padx=25, pady=(15, 0), sticky="w")
        self.gear_bonus_value_label = ctk.CTkLabel(self.home.gear_bonus_frame, text="+0%", font=self.config.heading_font, text_color=self.config.text)
        self.gear_bonus_value_label.grid(row=1, column=0, padx=25, sticky="w")
        self.gear_bonus_sub_label = ctk.CTkLabel(self.home.gear_bonus_frame, text="XP · 0 pieces", font=self.config.body_font, text_color=self.config.muted)
        self.gear_bonus_sub_label.grid(row=2, column=0, padx=25, pady=(0, 10), sticky="w")

        self.quests_completed_label = ctk.CTkLabel(self.home.quests_completed_frame, text="QUESTS DONE", font=self.config.label_font, text_color=self.config.muted)
        self.quests_completed_label.grid(row=0, column=0, padx=25, pady=(15, 0), sticky="w")
        self.quests_completed_value_label = ctk.CTkLabel(self.home.quests_completed_frame, text="0", font=self.config.heading_font, text_color=self.config.text)
        self.quests_completed_value_label.grid(row=1, column=0, padx=25, sticky="w")
        self.quests_completed_sub_label = ctk.CTkLabel(self.home.quests_completed_frame, text="+0 today", font=self.config.body_font, text_color=self.config.muted)
        self.quests_completed_sub_label.grid(row=2, column=0, padx=25, pady=(0, 10), sticky="w")

    def refresh_streak_and_gear(self):
        name, streak = self.habit_back.get_best_streak()
        self.streak_value_label.configure(text=f"{streak} day" + ("s" if streak != 1 else ""))
        self.streak_sub_label.configure(text=f"\U0001F525 {name} · active" if name else "No habits yet")

        bonus_percent = self.forge_back.get_gear_bonus_percent()
        pieces = self.forge_back.get_equipped_count()
        self.gear_bonus_value_label.configure(text=f"+{bonus_percent}%")
        self.gear_bonus_sub_label.configure(text=f"XP · {pieces} piece" + ("s" if pieces != 1 else ""))

        total = self.quest_back.get_completed_total()
        today = self.quest_back.get_completed_today_count()
        self.quests_completed_value_label.configure(text=str(total))
        self.quests_completed_sub_label.configure(text=f"+{today} today")

    #--- Level / XP bar ---#
    def setup_xp_bar(self):
        self.home.xpbar_frame.grid_columnconfigure(0, weight=1)
        self.home.xpbar_frame.grid_columnconfigure(1, weight=0)

        self.level_label = ctk.CTkLabel(self.home.xpbar_frame, text="LEVEL 0", font=self.config.label_font, text_color=self.config.muted)
        self.level_label.grid(row=0, column=0, padx=25, pady=(10, 0), sticky="w")

        self.xp_text_label = ctk.CTkLabel(self.home.xpbar_frame, text="", font=self.config.body_font, text_color=self.config.muted)
        self.xp_text_label.grid(row=0, column=1, padx=25, pady=(10, 0), sticky="e")

        self.title_label = ctk.CTkLabel(self.home.xpbar_frame, text="Apprentice", font=self.config.body_font, text_color=self.config.gold)
        self.title_label.grid(row=1, column=0, padx=25, sticky="w")

        self.unlock_hint_label = ctk.CTkLabel(self.home.xpbar_frame, text="", font=self.config.body_font, text_color=self.config.muted)
        self.unlock_hint_label.grid(row=1, column=1, padx=25, sticky="e")

        self.xp_progress_bar = ctk.CTkProgressBar(self.home.xpbar_frame, progress_color=self.config.ember, fg_color=self.config.card_hi, corner_radius=8)
        self.xp_progress_bar.grid(row=2, column=0, columnspan=2, padx=25, pady=(6, 10), sticky="ew")
        self.xp_progress_bar.set(0)

    def refresh_level(self):
        data = self.forge_back.read_save()
        username = data.get("username") or "Smith"
        info = get_level_info(data.get("xp", 0))

        self.level_label.configure(text=f"LEVEL {info['level']}")
        self.title_label.configure(text=f"{info['title']} {username}")
        self.xp_progress_bar.set(info["progress"])
        self.xp_text_label.configure(text=f"{info['xp_to_next']:,} XP to Lv {info['level'] + 1}")

        next_level = info["level"] + 1
        unlock_item = next((item for item in GEAR_CATALOG.values() if item["unlock_level"] == next_level), None)
        self.unlock_hint_label.configure(text=f"unlocks {unlock_item['name']}" if unlock_item else "")

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

        self.onboard_display3 = ctk.CTkLabel(self.home_topbar, text=self.habit_back.habit_display(), font=ctk.CTkFont("Space Grotesk", 13 ), text_color=self.config.muted)
        self.onboard_display3.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")

        # Shared with HabitFront so it can refresh this line live when a habit is checked.
        self.home.topbar_habit_display = self.onboard_display3

        coin_badge = ctk.CTkFrame(self.home_topbar, fg_color=self.config.bg, corner_radius=20, height=40)
        coin_badge.grid(row=0, column=3, rowspan=2, padx=(20, 30), pady=10, sticky="e")
        coin_badge.grid_propagate(False)
        coin_badge.columnconfigure(0, weight=1)
        coin_badge.rowconfigure(0, weight=1)

        coin_icon = ctk.CTkLabel(coin_badge, text="●", font=ctk.CTkFont("Space Grotesk", 24), text_color=self.config.gold)
        coin_icon.grid(row=0, column=0, padx=(18, 8), pady=8, sticky="e")
        coin_display = ctk.CTkLabel(coin_badge, text=str(self.currency.get_currencies()), font=ctk.CTkFont("Space Grotesk", 24, "bold"), text_color=self.config.text)
        coin_display.grid(row=0, column=1, padx=(0, 18), pady=8, sticky="w")

        # Shared with FocusCard/QuestFront so they can refresh the topbar coin display live.
        self.home.topbar_coin_display = coin_display

    def home_setup_quest_list(self):
        self.bottom_row_frame = ctk.CTkFrame(self.home.frame, width=1050, height=325, fg_color=self.config.bg, corner_radius=0)
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

        #--- Right column: Materials + Equipped Gear (placeholders) ---#
        self.right_column_frame = ctk.CTkFrame(self.bottom_row_frame, width=materials_width, fg_color=self.config.bg, corner_radius=0)
        self.right_column_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        self.right_column_frame.grid_propagate(False)
        self.right_column_frame.grid_columnconfigure(0, weight=1)
        self.right_column_frame.grid_rowconfigure(0, weight=1)
        self.right_column_frame.grid_rowconfigure(1, weight=1)

        self.materials_frame = ctk.CTkFrame(self.right_column_frame, fg_color=self.config.card, corner_radius=30)
        self.materials_frame.grid(row=0, column=0, pady=(0, 10), sticky="nsew")
        self.materials_frame.grid_columnconfigure((0, 1), weight=1)

        self.materials_label = ctk.CTkLabel(self.materials_frame, text="MATERIALS", font=self.config.label_font, text_color=self.config.muted)
        self.materials_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(16, 10), sticky="w")

        material_types = [("Wood", self.config.ember), ("Stone", self.config.muted), ("Clay", self.config.gold), ("Iron", self.config.text)]
        self.material_value_labels = {}
        for i, (name, dot_color) in enumerate(material_types):
            row, col = 1 + i // 2, i % 2
            item_frame = ctk.CTkFrame(self.materials_frame, fg_color="transparent")
            item_frame.grid(row=row, column=col, padx=20, pady=(0, 14), sticky="w")

            icon = ctk.CTkFrame(item_frame, width=16, height=16, fg_color=dot_color, corner_radius=5)
            icon.grid(row=0, column=0, rowspan=2, padx=(0, 9), sticky="w")
            icon.grid_propagate(False)

            ctk.CTkLabel(item_frame, text=name, font=self.config.body_font, text_color=self.config.muted).grid(row=0, column=1, sticky="w")
            value_label = ctk.CTkLabel(item_frame, text="0", font=self.config.label_font, text_color=self.config.text)
            value_label.grid(row=1, column=1, sticky="w")
            self.material_value_labels[name] = value_label

        #--- Equipped Gear ---#
        self.gear_frame = ctk.CTkFrame(self.right_column_frame, fg_color=self.config.card, corner_radius=30)
        self.gear_frame.grid(row=1, column=0, sticky="nsew")
        self.gear_frame.grid_columnconfigure(tuple(range(GEAR_SLOT_DISPLAY_COUNT)), weight=1)

        self.gear_label = ctk.CTkLabel(self.gear_frame, text="EQUIPPED GEAR", font=self.config.label_font, text_color=self.config.muted)
        self.gear_label.grid(row=0, column=0, columnspan=GEAR_SLOT_DISPLAY_COUNT, padx=20, pady=(16, 12), sticky="w")

        self.gear_slot_labels = []
        for slot in range(GEAR_SLOT_DISPLAY_COUNT):
            gear_slot = ctk.CTkFrame(self.gear_frame, width=40, height=40, fg_color=self.config.card_hi, corner_radius=12)
            gear_slot.grid(row=1, column=slot, padx=(20 if slot == 0 else 6, 6), pady=(0, 12), sticky="w")
            gear_slot.grid_propagate(False)
            gear_slot.grid_columnconfigure(0, weight=1)
            gear_slot.grid_rowconfigure(0, weight=1)
            slot_label = ctk.CTkLabel(gear_slot, text="+", font=self.config.label_font, text_color=self.config.muted)
            slot_label.grid(row=0, column=0)
            self.gear_slot_labels.append(slot_label)

        self.gear_hint_label = ctk.CTkLabel(self.gear_frame, text="Empty slots · smelt gear in the Forge →", font=self.config.body_font, text_color=self.config.ember)
        self.gear_hint_label.grid(row=2, column=0, columnspan=GEAR_SLOT_DISPLAY_COUNT, padx=20, pady=(0, 14), sticky="w")

    def refresh_materials_and_gear(self):
        materials = self.forge_back.get_materials()
        for name, label in self.material_value_labels.items():
            label.configure(text=str(materials.get(name, 0)))

        _, equipped = self.forge_back.get_gear_state()
        for i, label in enumerate(self.gear_slot_labels):
            if i < len(GEAR_SLOTS):
                item_id = equipped.get(GEAR_SLOTS[i])
                item = GEAR_CATALOG.get(item_id)
            else:
                item = None
            label.configure(text=item["icon"] if item else "+", text_color=self.config.text if item else self.config.muted)

        empty_slots = GEAR_SLOT_DISPLAY_COUNT - len(equipped)
        if empty_slots > 0:
            self.gear_hint_label.configure(text="Empty slots · smelt gear in the Forge →")
        else:
            self.gear_hint_label.configure(text="All slots equipped ⚔")
