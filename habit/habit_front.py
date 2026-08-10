import customtkinter as ctk
import ctypes
import platform
from datetime import datetime, timedelta
from tkinter import messagebox

from backend.config import Config
from backend.start_setup import get_setup
from pages.habit_page import get_habit
from pages.home_page import get_home
from habit.habit_back import get_habitback

_habitfront_instance = None

def get_habitfront():
    global _habitfront_instance
    if _habitfront_instance is None:
        _habitfront_instance = HabitFront()
    return _habitfront_instance

DIFFICULTY_COLOR_KEY = {"easy": "green", "medium": "gold", "hard": "red"}

class HabitFront:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.habit_page = get_habit()
        self.home_page = get_home()
        self.habit_back = get_habitback()
        self.strike_font = ctk.CTkFont("Space Grotesk", 15, "bold", overstrike=True)

        self.slots_used = 0
        self.max_slots = self.habit_back.get_max_habits()
        self.unchecked_count = 0
        self.shields_equipped = 0

        #--- Topbar ---#
        self.title_label = None
        self.subtitle_label = None
        self.slots_frame = None
        self.slots_count_label = None
        self.slots_text_label = None
        self.new_habit_button = None

        #--- New Habit Widgets ---#
        self.name_entry = None
        self.category_frame = None
        self.popup = None
        self.category_buttons = []
        self.selected_category = None
        self.difficulty_frame = None
        self.difficulty_buttons = []
        self.selected_difficulty = None
        self.actions_frame = None

        #--- Reset Banner ---#
        self.reset_banner = None
        self.reset_label = None
        self.reset_job = None

        #--- Habit List ---#
        self.list_frame = None
        self.footer_label = None
        self.habit_cards = []

    def main(self):
        pass

    def setup_topbar(self):
        self.title_label = ctk.CTkLabel(self.habit_page.topbar_frame, text="Habits", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text)
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        self.subtitle_label = ctk.CTkLabel(self.habit_page.topbar_frame,
                                text="Daily repeatables · streaks reset at midnight", font=self.config.body_font, text_color=self.config.muted)
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.slots_frame = ctk.CTkFrame(self.habit_page.topbar_frame, fg_color=self.config.bg)
        self.slots_frame.grid(row=0, column=1, rowspan=2, padx=(20, 2), pady=15, sticky="e")

        self.slots_count_label = ctk.CTkLabel(self.slots_frame, text=f"{self.slots_used} / {self.max_slots}", font=self.config.body_font, text_color=self.config.gold)
        self.slots_count_label.grid(row=0, column=0, sticky="e")

        self.slots_text_label = ctk.CTkLabel(self.slots_frame, text=" slots used", font=self.config.body_font, text_color=self.config.muted)
        self.slots_text_label.grid(row=0, column=1, padx=(0, 4), sticky="e")

        self.new_habit_button = ctk.CTkButton(self.habit_page.topbar_frame, text="+ New habit", font=self.config.button_font,
                                              fg_color=self.config.ember, hover_color=self.config.gold,
                                              text_color=self.config.nav, corner_radius=20, command=lambda: self.create_habit())
        self.new_habit_button.grid(row=0, column=2, rowspan=2, padx=(0, 30), pady=15, sticky="e")

        self.habit_page.topbar_frame.grid_columnconfigure(1, weight=1)

    #--- New Habit Popup ---#
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

    def create_habit_check(self):
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

    def create_habit(self):
        self.selected_category = None
        self.selected_difficulty = None

        self.popup = ctk.CTkToplevel(self.habit_page.frame)
        self.popup.title("New Habit")
        self.popup.geometry("420x300")
        self.popup.configure(fg_color=self.config.card)
        self.popup.transient(self.habit_page.frame.winfo_toplevel())
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
        self.difficulty_frame.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="ew")

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

        ctk.CTkButton(self.actions_frame, text="Create habit", font=self.config.button_font,
                      fg_color=self.config.ember, hover_color=self.config.gold,
                      text_color=self.config.nav, corner_radius=20,
                      command=self.on_create_habit_click).grid(row=0, column=1, sticky="ew")

    def on_create_habit_click(self):
        if not self.create_habit_check():
            return
        if self.slots_used >= self.max_slots:
            messagebox.showinfo("Habit slots full", "Delete a habit to free up a slot.")
            return
        self.habit_back.create_habit_file(name=self.name_entry.get(), category=self.selected_category, difficulty=self.selected_difficulty)
        self.popup.destroy()
        self.refresh_habit_topbar()
        self.render_habit_cards()

    #--- Habit List ---#
    def setup_habit_list(self):
        self.habit_page.frame.grid_rowconfigure(1, weight=1)
        self.habit_page.frame.grid_columnconfigure(0, weight=1)

        self.reset_banner = ctk.CTkFrame(self.habit_page.frame, fg_color=self.config.card, corner_radius=14)
        self.reset_banner.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.reset_label = ctk.CTkLabel(self.reset_banner, text="", font=self.config.body_font, text_color=self.config.text)
        self.reset_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.list_frame = ctk.CTkScrollableFrame(self.habit_page.frame, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.footer_label = ctk.CTkLabel(
            self.habit_page.frame,
            text="Habit slots are limited — buy more in the Shop when you hit the cap.",
            font=self.config.body_font, text_color=self.config.muted,
        )
        self.footer_label.grid(row=2, column=0, padx=20, pady=(10, 15), sticky="w")

        self.render_habit_cards()

    def render_habit_cards(self):
        for card in self.habit_cards:
            card["frame"].destroy()
        self.habit_cards = []

        habits = self.habit_back.load_habits()
        habits.sort(key=lambda habit: habit.get("checked", False))

        for i, habit in enumerate(habits):
            self.build_habit_card(i, habit)

        self.slots_used = len(habits)
        self.unchecked_count = len([habit for habit in habits if not habit.get("checked")])
        self.shields_equipped = len([habit for habit in habits if habit.get("shielded")])

        self.slots_count_label.configure(text=f"{self.slots_used} / {self.max_slots}")
        self.footer_label.grid() if self.slots_used >= self.max_slots else self.footer_label.grid_remove()
        self.new_habit_button.configure(state="disabled" if self.slots_used >= self.max_slots else "normal")

        self.update_reset_banner()

    def update_reset_banner(self):
        if self.reset_job is not None:
            self.reset_banner.after_cancel(self.reset_job)
            self.reset_job = None

        now = datetime.now()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delta = tomorrow - now
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60

        habit_word = "habit" if self.unchecked_count == 1 else "habits"
        if self.shields_equipped == 0:
            shield_text = "no shield charges equipped"
        else:
            shield_text = f"{self.shields_equipped} shield charge" + ("s" if self.shields_equipped != 1 else "") + " equipped"

        self.reset_label.configure(
            text=f"\U0001F319  Resets in  {hours}h {minutes}m  —  {self.unchecked_count} {habit_word} unchecked  ·  {shield_text}"
        )

        self.reset_job = self.reset_banner.after(30000, self.update_reset_banner)

    def build_habit_card(self, row, habit):
        coins, xp = self.habit_back.calculate_rewards(habit["difficulty"])
        difficulty_color = getattr(self.config, DIFFICULTY_COLOR_KEY.get(habit["difficulty"].lower(), "muted"))
        checked = habit.get("checked", False)
        shielded = habit.get("shielded", False)
        streak = habit.get("streak", 0)

        card = ctk.CTkFrame(self.list_frame, fg_color=self.config.card, corner_radius=12)
        card.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        card.grid_columnconfigure(1, weight=1)

        checkbox = ctk.CTkCheckBox(
            card, text="", width=24, checkbox_width=24, checkbox_height=24,
            fg_color=self.config.green if checked else self.config.ember,
            hover_color=self.config.gold,
            border_color=self.config.green if checked else self.config.muted,
            state="disabled" if checked else "normal",
            command=lambda: self.on_complete_click(habit["file_name"]),
        )
        checkbox.grid(row=0, column=0, rowspan=2, padx=(15, 10), pady=15)
        if checked:
            checkbox.select()

        name_label = ctk.CTkLabel(
            card, text=habit["name"],
            font=self.strike_font if checked else self.config.label_font,
            text_color=self.config.muted if checked else self.config.text,
        )
        name_label.grid(row=0, column=1, pady=(12, 0), sticky="w")

        tags_frame = ctk.CTkFrame(card, fg_color="transparent")
        tags_frame.grid(row=1, column=1, pady=(0, 12), sticky="w")

        category_pill = ctk.CTkLabel(
            tags_frame, text=f"  {habit['category'].upper()}  ", font=self.config.body_font,
            text_color=self.config.muted, fg_color=self.config.card_hi, corner_radius=6,
        )
        category_pill.grid(row=0, column=0, padx=(0, 6), pady=2)

        difficulty_pill = ctk.CTkLabel(
            tags_frame, text=f"  {habit['difficulty'].upper()}  ", font=self.config.body_font,
            text_color=self.config.nav, fg_color=difficulty_color, corner_radius=6,
        )
        difficulty_pill.grid(row=0, column=1, padx=(0, 6), pady=2)

        shield_pill = ctk.CTkButton(
            tags_frame, text=f"  \U0001F6E1 {'shielded' if shielded else 'unprotected'}  ",
            font=self.config.body_font, corner_radius=6, width=1, height=1,
            fg_color=self.config.gold if shielded else self.config.card_hi,
            text_color=self.config.nav if shielded else self.config.muted,
            hover_color=self.config.card,
            command=lambda: self.on_shield_click(habit["file_name"]),
        )
        shield_pill.grid(row=0, column=2, pady=2)

        reward_frame = ctk.CTkFrame(card, fg_color="transparent")
        reward_frame.grid(row=0, column=2, rowspan=2, padx=(10, 10), pady=15, sticky="e")

        streak_label = ctk.CTkLabel(
            reward_frame, text=f"\U0001F525 {streak} day" + ("s" if streak != 1 else ""),
            font=self.config.body_font, text_color=self.config.ember,
        )
        streak_label.grid(row=0, column=0, sticky="e")

        reward_label = ctk.CTkLabel(
            reward_frame,
            text="earned ✓" if checked else f"{coins} \U0001F7E1  ·  +{xp} XP",
            font=self.config.body_font,
            text_color=self.config.green if checked else self.config.gold,
        )
        reward_label.grid(row=1, column=0, sticky="e")

        delete_button = ctk.CTkButton(
            card, text="\U0001F5D1", width=28, height=28, font=self.config.body_font,
            fg_color="transparent", hover_color=self.config.card_hi, text_color=self.config.muted,
            command=lambda: self.on_delete_click(habit["file_name"]),
        )
        delete_button.grid(row=0, column=3, rowspan=2, padx=(0, 15), pady=15)

        self.habit_cards.append({
            "frame": card, "file_name": habit["file_name"],
            "checkbox": checkbox, "name_label": name_label, "reward_label": reward_label,
        })

    def on_complete_click(self, file_name):
        card = next((c for c in self.habit_cards if c["file_name"] == file_name), None)
        if card is None:
            return

        card["checkbox"].select()
        card["checkbox"].configure(state="disabled", fg_color=self.config.green, border_color=self.config.green)
        card["name_label"].configure(font=self.strike_font, text_color=self.config.muted)
        card["reward_label"].configure(text="earned ✓", text_color=self.config.green)

        self.list_frame.after(500, lambda: self.finish_complete(file_name))

    def finish_complete(self, file_name):
        self.habit_back.complete_habit(file_name)
        self.refresh_coins()
        self.refresh_habit_topbar()
        self.render_habit_cards()
        self.refresh_home_stats()

    def refresh_home_stats(self):
        for method_name in ("refresh_streak_and_gear", "refresh_level", "refresh_materials_and_gear"):
            method = getattr(self.home_page, method_name, None)
            if method is not None:
                method()

    def refresh_habit_topbar(self):
        topbar_habit_display = self.home_page.topbar_habit_display
        if topbar_habit_display is not None:
            topbar_habit_display.configure(text=self.habit_back.habit_display())

    def refresh_coins(self):
        coin_display = self.home_page.coin_display
        coin_change_display = self.home_page.coin_change_display
        topbar_coin_display = self.home_page.topbar_coin_display
        if coin_display is None or coin_change_display is None:
            return

        balance = str(self.habit_back.currency.get_currencies())
        coin_display.configure(text=balance)
        if topbar_coin_display is not None:
            topbar_coin_display.configure(text=balance)

        net = self.habit_back.currency.get_today_flow()["net"]
        if net > 0:
            change_text, change_color = f"+{net} today", self.config.green
        elif net < 0:
            change_text, change_color = f"{net} today", self.config.red
        else:
            change_text, change_color = "0 today", self.config.muted
        coin_change_display.configure(text=change_text, text_color=change_color)

    def on_delete_click(self, file_name):
        self.habit_back.delete_habit(file_name)
        self.refresh_habit_topbar()
        self.render_habit_cards()

    def on_shield_click(self, file_name):
        if not self.habit_back.toggle_shield(file_name):
            messagebox.showinfo("No shield charges", "You don't have any shield charges available.")
            return
        self.render_habit_cards()

    def refresh_max_slots(self):
        self.max_slots = self.habit_back.get_max_habits()
        self.render_habit_cards()
