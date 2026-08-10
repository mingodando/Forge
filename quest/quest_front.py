import customtkinter as ctk
import ctypes
import platform
from tkinter import messagebox

from backend.config import Config
from backend.start_setup import get_setup
from pages.home_page import get_home
from pages.quest_page import get_quest
from quest.quest_back import QuestBack

DIFFICULTY_COLOR_KEY = {"easy": "green", "medium": "gold", "hard": "red"}

class QuestFront:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.quest_page = get_quest()
        self.home_page = get_home()
        self.quest_back = QuestBack()
        self.strike_font = ctk.CTkFont("Space Grotesk", 15, "bold", overstrike=True)

        self.slots_used = 0
        self.max_slots = self.quest_back.get_max_quests()

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
        self.difficulty_frame = None
        self.difficulty_buttons = []
        self.selected_difficulty = None
        self.actions_frame = None

        #--- Quest List ---#
        self.list_frame = None
        self.footer_label = None
        self.quest_cards = []

        #--- Home Quest Preview ---#
        self.home_list_frame = None
        self.home_quest_cards = []

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
                btn.configure(fg_color=self.config.ember, border_color=self.config.ember, text_color="white")
            else:
                btn.configure(fg_color=self.config.card_hi, border_color=self.config.card_hi, text_color=self.config.text)

    def select_difficulty(self, dog):
        self.selected_difficulty = dog
        for btn_dog, btn in self.difficulty_buttons:
            if btn_dog == dog:
                btn.configure(fg_color=self.config.ember, border_color=self.config.ember, text_color="white")
            else:
                btn.configure(fg_color=self.config.card_hi, border_color=self.config.card_hi, text_color=self.config.text)

    def create_quest_check(self):
        if not self.name_entry.get().strip():
            messagebox.showinfo("Missing info", "Please enter a name!")
            return False
        if self.selected_category is None:
            messagebox.showinfo("Missing info", "Please pick a category!")
            return False
        if self.selected_difficulty is None:
            messagebox.showinfo("Missing info", "Please pick a difficulty!")
            return False
        return True

    def create_quest(self):
        self.popup = ctk.CTkToplevel(self.quest_page.frame)
        self.popup.title("New Quest")
        self.popup.geometry("420x300")
        self.popup.configure(fg_color=self.config.card)
        self.popup.transient(self.quest_page.frame.winfo_toplevel())
        self.popup.grab_set()
        self.popup.grid_columnconfigure(0, weight=1)

        self.popup.update()
        if platform.system() == "Windows":
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

        ctk.CTkLabel(self.popup, text="DIFFICULTY", font=self.config.body_font, text_color=self.config.muted).grid(row=4, column=0, padx=20, pady=(0, 5), sticky="w")
        self.difficulty_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        self.difficulty_frame.grid(row=5, column=0, padx=20, pady=(0,15), sticky="ew")

        self.difficulty_buttons = []
        for i, dog in enumerate(["Easy", "Medium", "Hard"]):
            btn = ctk.CTkButton(self.difficulty_frame, text=dog, font=self.config.body_font,
                                fg_color=self.config.card_hi, text_color=self.config.text, hover_color=self.config.card,
                                border_width=2, border_color=self.config.card_hi, corner_radius=8, command=lambda d=dog: self.select_difficulty(d))
            btn.grid(row=0, column=i, padx=(0, 4) if i < 3 else 0, sticky="ew")
            self.difficulty_frame.grid_columnconfigure(i, weight=1)
            self.difficulty_buttons.append((dog, btn))

        self.actions_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        self.actions_frame.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.actions_frame.grid_columnconfigure(0, weight=1)
        self.actions_frame.grid_columnconfigure(1, weight=2)

        ctk.CTkButton(self.actions_frame, text="Cancel", font=self.config.button_font,
                      fg_color="transparent", hover_color=self.config.card_hi,
                      text_color=self.config.ember, border_width=2, border_color=self.config.ember,
                      corner_radius=20, command=lambda: self.popup.destroy()).grid(row=0, column=0, padx=(0, 8), sticky="ew")

        ctk.CTkButton(self.actions_frame, text="Create quest", font=self.config.button_font,
                      fg_color=self.config.ember, hover_color=self.config.gold,
                      text_color=self.config.nav, corner_radius=20,
                      command=self.on_create_quest_click).grid(row=0, column=1, sticky="ew")

    def on_create_quest_click(self):
        if not self.create_quest_check():
            return
        if self.slots_used >= self.max_slots:
            messagebox.showinfo("Quest slots full", "Finish or delete a quest to free up a slot.")
            return
        self.quest_back.create_quest_file(name=self.name_entry.get(), category=self.selected_category, difficulty=self.selected_difficulty)
        self.popup.destroy()
        self.render_quest_cards()

    #--- Quest List ---#
    def setup_quest_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self.quest_page.frame, fg_color="transparent")
        self.list_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.quest_page.frame.grid_rowconfigure(0, weight=1)
        self.quest_page.frame.grid_columnconfigure(0, weight=1)

        self.footer_label = ctk.CTkLabel(
            self.quest_page.frame,
            text="Quest slots are limited — buy more in the Shop when you hit the cap.",
            font=self.config.body_font, text_color=self.config.muted,
        )
        self.footer_label.grid(row=1, column=0, padx=20, pady=(10, 15), sticky="w")

        self.render_quest_cards()

    def setup_home_quest_list(self, home_list_frame):
        self.home_list_frame = home_list_frame
        self.render_home_quest_cards()

    def render_quest_cards(self):
        for card in self.quest_cards:
            card["frame"].destroy()
        self.quest_cards = []

        quests = self.quest_back.load_quests()
        quests.sort(key=lambda quest: quest.get("completed", False))

        for i, quest in enumerate(quests):
            self.build_quest_card(i, quest, self.list_frame, self.quest_cards)

        self.slots_used = len([quest for quest in quests if not quest.get("completed", False)])
        self.slots_count_label.configure(text=f"{self.slots_used} / {self.max_slots}")
        self.footer_label.grid() if self.slots_used >= self.max_slots else self.footer_label.grid_remove()
        self.new_quest_button.configure(state="disabled" if self.slots_used >= self.max_slots else "normal")

        self.render_home_quest_cards()

    def render_home_quest_cards(self):
        if self.home_list_frame is None:
            return

        for card in self.home_quest_cards:
            card["frame"].destroy()
        self.home_quest_cards = []

        quests = self.quest_back.load_quests()
        quests.sort(key=lambda quest: quest.get("completed", False))

        for i, quest in enumerate(quests):
            self.build_quest_card(i, quest, self.home_list_frame, self.home_quest_cards, scale=0.7)

    def build_quest_card(self, row, quest, list_frame, card_list, scale=1.0):
        coins, xp = self.quest_back.calculate_rewards(quest["difficulty"])
        difficulty_color = getattr(self.config, DIFFICULTY_COLOR_KEY.get(quest["difficulty"].lower(), "muted"))
        completed = quest.get("completed", False)

        pad = round(15 * scale)
        gap = round(10 * scale)

        card = ctk.CTkFrame(list_frame, fg_color=self.config.card, corner_radius=round(12 * scale))
        card.grid(row=row, column=0, sticky="ew", pady=(0, gap))
        card.grid_columnconfigure(1, weight=1)

        checkbox = ctk.CTkCheckBox(
            card, text="", width=round(24 * scale), checkbox_width=round(24 * scale), checkbox_height=round(24 * scale),
            fg_color=self.config.green if completed else self.config.ember,
            hover_color=self.config.gold,
            border_color=self.config.green if completed else self.config.muted,
            state="disabled" if completed else "normal",
            command=lambda: self.on_complete_click(quest["file_name"]),
        )
        checkbox.grid(row=0, column=0, rowspan=2, padx=(pad, gap), pady=pad)
        if completed:
            checkbox.select()

        name_label = ctk.CTkLabel(
            card, text=quest["name"],
            font=self.strike_font if completed else self.config.label_font,
            text_color=self.config.muted if completed else self.config.text,
        )
        name_label.grid(row=0, column=1, pady=(round(12 * scale), 0), sticky="w")

        tags_frame = ctk.CTkFrame(card, fg_color="transparent")
        tags_frame.grid(row=1, column=1, pady=(0, round(12 * scale)), sticky="w")

        category_pill = ctk.CTkLabel(
            tags_frame, text=f"  {quest['category'].upper()}  ", font=self.config.body_font,
            text_color=self.config.muted, fg_color=self.config.card_hi, corner_radius=6,
        )
        category_pill.grid(row=0, column=0, padx=(0, 6), pady=2)

        difficulty_pill = ctk.CTkLabel(
            tags_frame, text=f"  {quest['difficulty'].upper()}  ", font=self.config.body_font,
            text_color=self.config.nav, fg_color=difficulty_color, corner_radius=6,
        )
        difficulty_pill.grid(row=0, column=1, pady=2)

        reward_label = ctk.CTkLabel(
            card,
            text="earned ✓" if completed else f"{coins} \U0001F7E1  ·  +{xp} XP",
            font=self.config.body_font,
            text_color=self.config.green if completed else self.config.gold,
        )
        reward_label.grid(row=0, column=2, rowspan=2, padx=(gap, gap), pady=pad, sticky="e")

        delete_button = ctk.CTkButton(
            card, text="\U0001F5D1", width=round(28 * scale), height=round(28 * scale), font=self.config.body_font,
            fg_color="transparent", hover_color=self.config.card_hi, text_color=self.config.muted,
            command=lambda: self.on_delete_click(quest["file_name"]),
        )
        delete_button.grid(row=0, column=3, rowspan=2, padx=(0, pad), pady=pad)

        card_list.append({
            "frame": card, "file_name": quest["file_name"],
            "checkbox": checkbox, "name_label": name_label, "reward_label": reward_label,
        })

    def on_complete_click(self, file_name):
        for card_list in (self.quest_cards, self.home_quest_cards):
            card = next((c for c in card_list if c["file_name"] == file_name), None)
            if card is None:
                continue

            card["checkbox"].select()
            card["checkbox"].configure(state="disabled", fg_color=self.config.green, border_color=self.config.green)
            card["name_label"].configure(font=self.strike_font, text_color=self.config.muted)
            card["reward_label"].configure(text="earned ✓", text_color=self.config.green)

        self.list_frame.after(500, lambda: self.finish_complete(file_name))

    def finish_complete(self, file_name):
        self.quest_back.complete_quest(file_name)
        self.refresh_coins()
        self.render_quest_cards()
        self.refresh_home_stats()

    def refresh_home_stats(self):
        for method_name in ("refresh_streak_and_gear", "refresh_level", "refresh_materials_and_gear"):
            method = getattr(self.home_page, method_name, None)
            if method is not None:
                method()

    def refresh_coins(self):
        coin_display = self.home_page.coin_display
        coin_change_display = self.home_page.coin_change_display
        topbar_coin_display = self.home_page.topbar_coin_display
        if coin_display is None or coin_change_display is None:
            return

        balance = str(self.quest_back.currency.get_currencies())
        coin_display.configure(text=balance)
        if topbar_coin_display is not None:
            topbar_coin_display.configure(text=balance)

        net = self.quest_back.currency.get_today_flow()["net"]
        if net > 0:
            change_text, change_color = f"+{net} today", self.config.green
        elif net < 0:
            change_text, change_color = f"{net} today", self.config.red
        else:
            change_text, change_color = "0 today", self.config.muted
        coin_change_display.configure(text=change_text, text_color=change_color)

    def on_delete_click(self, file_name):
        self.quest_back.delete_quest(file_name)
        self.render_quest_cards()

    def refresh_max_slots(self):
        self.max_slots = self.quest_back.get_max_quests()
        self.render_quest_cards()

_quest_front_instance = None

def get_quest_front():
    global _quest_front_instance
    if _quest_front_instance is None:
        _quest_front_instance = QuestFront()
    return _quest_front_instance