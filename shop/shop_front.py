import customtkinter as ctk
import ctypes
import platform
from tkinter import messagebox

from backend.config import Config
from backend.start_setup import get_setup
from pages.shop_page import get_shop
from pages.home_page import get_home
from shop.shop_back import get_shopback, SHOP_CATALOG
from quest.quest_front import get_quest_front
from habit.habit_front import get_habitfront

_shopfront_instance = None


def get_shopfront():
    global _shopfront_instance
    if _shopfront_instance is None:
        _shopfront_instance = ShopFront()
    return _shopfront_instance


class ShopFront:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.shop_page = get_shop()
        self.home_page = get_home()
        self.shop_back = get_shopback()
        self.quest_front = get_quest_front()
        self.habit_front = get_habitfront()

        self.coin_display = None
        self.list_frame = None
        self.cards = []
        self.popup = None

    def main(self):
        pass

    #--- Topbar ---#
    def setup_topbar(self):
        title_label = ctk.CTkLabel(self.shop_page.topbar_frame, text="Shop", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text)
        title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        subtitle_label = ctk.CTkLabel(self.shop_page.topbar_frame, text="Spend coins on capacity, insurance & style", font=self.config.body_font, text_color=self.config.muted)
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        self.shop_page.topbar_frame.grid_columnconfigure(1, weight=1)

        coin_badge = ctk.CTkFrame(self.shop_page.topbar_frame, fg_color=self.config.card, corner_radius=20)
        coin_badge.grid(row=0, column=1, rowspan=2, padx=(20, 30), pady=15, sticky="e")

        coin_icon = ctk.CTkLabel(coin_badge, text="●", font=self.config.label_font, text_color=self.config.gold)
        coin_icon.grid(row=0, column=0, padx=(16, 6), pady=10)
        self.coin_display = ctk.CTkLabel(coin_badge, text=str(self.shop_back.currency.get_currencies()), font=self.config.label_font, text_color=self.config.text)
        self.coin_display.grid(row=0, column=1, padx=(0, 16), pady=10)

    def refresh_coin_badge(self):
        balance = str(self.shop_back.currency.get_currencies())
        if self.coin_display is not None:
            self.coin_display.configure(text=balance)

        coin_display = self.home_page.coin_display
        coin_change_display = self.home_page.coin_change_display
        topbar_coin_display = self.home_page.topbar_coin_display
        if coin_display is not None:
            coin_display.configure(text=balance)
        if topbar_coin_display is not None:
            topbar_coin_display.configure(text=balance)

        net = self.shop_back.currency.get_today_flow()["net"]
        if coin_change_display is not None:
            if net > 0:
                change_text, change_color = f"+{net} today", self.config.green
            elif net < 0:
                change_text, change_color = f"{net} today", self.config.red
            else:
                change_text, change_color = "0 today", self.config.muted
            coin_change_display.configure(text=change_text, text_color=change_color)

    #--- Body ---#
    def setup_shop_body(self):
        self.shop_page.frame.grid_rowconfigure(0, weight=1)
        self.shop_page.frame.grid_columnconfigure(0, weight=1)

        self.list_frame = ctk.CTkScrollableFrame(self.shop_page.frame, fg_color="transparent")
        self.list_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.list_frame.grid_columnconfigure((0, 1), weight=1)

        self.render_cards()

    def render_cards(self):
        for card in self.cards:
            card.destroy()
        self.cards = []

        for i, item_id in enumerate(SHOP_CATALOG):
            row, col = i // 2, i % 2
            self.build_card(item_id, row, col)

    def build_card(self, item_id, row, col):
        item = SHOP_CATALOG[item_id]
        can, reason = self.shop_back.can_buy(item_id)

        description = item["description"]
        if item_id == "extra_quest_slot":
            current = self.quest_front.quest_back.get_max_quests()
            description = description.format(current=current, next=current + 1)

        card = ctk.CTkFrame(self.list_frame, fg_color=self.config.card, corner_radius=16)
        card.grid(row=row, column=col, padx=(0, 10) if col == 0 else (10, 0), pady=(0, 12), sticky="new")
        card.grid_columnconfigure(1, weight=1)
        self.cards.append(card)

        icon_frame = ctk.CTkFrame(card, width=44, height=44, fg_color=self.config.card_hi, corner_radius=12)
        icon_frame.grid(row=0, column=0, rowspan=3, padx=(16, 12), pady=16, sticky="n")
        icon_frame.grid_propagate(False)
        icon_frame.grid_columnconfigure(0, weight=1)
        icon_frame.grid_rowconfigure(0, weight=1)
        ctk.CTkLabel(icon_frame, text=item["icon"], font=ctk.CTkFont("Space Grotesk", 18)).grid(row=0, column=0)

        ctk.CTkLabel(card, text=item["name"], font=self.config.label_font, text_color=self.config.text).grid(row=0, column=1, padx=(0, 16), pady=(16, 0), sticky="w")
        ctk.CTkLabel(card, text=description, font=self.config.body_font, text_color=self.config.muted, wraplength=280, justify="left").grid(row=1, column=1, padx=(0, 16), sticky="w")

        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.grid(row=2, column=1, padx=(0, 16), pady=(10, 10), sticky="ew")

        ctk.CTkLabel(action_frame, text=f"● {item['cost']}", font=self.config.label_font, text_color=self.config.gold).grid(row=0, column=0, padx=(0, 10), sticky="w")

        buy_button = ctk.CTkButton(
            action_frame, text="Buy" if can else ("Owned" if reason == "Owned" else "Buy"),
            font=self.config.button_font, corner_radius=10, width=90,
            fg_color=self.config.ember if can else self.config.card_hi,
            text_color="white" if can else self.config.muted,
            hover_color=self.config.gold if can else self.config.card_hi,
            state="normal" if can else "disabled",
            command=lambda: self.on_buy_click(item_id),
        )
        buy_button.grid(row=0, column=1, sticky="e")

        if not can:
            ctk.CTkLabel(card, text=reason, font=self.config.body_font, text_color=self.config.red).grid(row=3, column=1, padx=(0, 16), pady=(0, 14), sticky="w")

    #--- Purchases ---#
    def on_buy_click(self, item_id):
        if item_id == "extra_quest_slot":
            self.shop_back.buy_extra_quest_slot()
            self.quest_front.refresh_max_slots()
        elif item_id == "shield_refresh":
            self.shop_back.buy_shield_refresh()
        elif item_id == "ember_skin":
            self.shop_back.buy_ember_skin()
        elif item_id == "streak_revival":
            self.open_streak_revival_picker()
            return

        self.refresh_coin_badge()
        self.render_cards()

    def open_streak_revival_picker(self):
        eligible = self.shop_back.get_revivable_habits()
        if not eligible:
            messagebox.showinfo("No broken streaks", "None of your habits have a broken streak to revive right now.")
            return

        self.popup = ctk.CTkToplevel(self.shop_page.frame)
        self.popup.title("Streak revival")
        self.popup.geometry("360x" + str(120 + 50 * len(eligible)))
        self.popup.configure(fg_color=self.config.card)
        self.popup.transient(self.shop_page.frame.winfo_toplevel())
        self.popup.grab_set()
        self.popup.grid_columnconfigure(0, weight=1)

        self.popup.update()
        if platform.system() == "Windows":
            # noinspection PyUnresolvedReferences
            hwnd = ctypes.windll.user32.GetParent(self.popup.winfo_id())
            dark_mode = ctypes.c_int(1)
            # noinspection PyUnresolvedReferences
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode))

        ctk.CTkLabel(self.popup, text="Choose a habit to revive", font=self.config.body_font, text_color=self.config.muted).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        for i, habit in enumerate(eligible):
            btn = ctk.CTkButton(
                self.popup, text=f"{habit['name']}  ·  restore to {habit['previous_streak']} days",
                font=self.config.body_font, fg_color=self.config.card_hi, hover_color=self.config.card,
                text_color=self.config.text, corner_radius=8,
                command=lambda fn=habit["file_name"]: self.on_revive_pick(fn),
            )
            btn.grid(row=i + 1, column=0, padx=20, pady=(0, 8), sticky="ew")

    def on_revive_pick(self, file_name):
        self.shop_back.buy_streak_revival(file_name)
        self.popup.destroy()
        self.refresh_coin_badge()
        self.render_cards()
        self.habit_front.render_habit_cards()
