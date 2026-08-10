import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup
from pages.forge_page import get_forge
from pages.home_page import get_home
from forge.forge_back import get_forgeback, GEAR_CATALOG, GEAR_SLOTS

MATERIAL_ICON = {"Wood": "\U0001FAB5", "Stone": "\U0001FAA8", "Clay": "\U0001F9F1", "Iron": "⛓"}

_forgefront_instance = None


def get_forgefront():
    global _forgefront_instance
    if _forgefront_instance is None:
        _forgefront_instance = ForgeFront()
    return _forgefront_instance


class ForgeFront:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.forge_page = get_forge()
        self.home_page = get_home()
        self.forge_back = get_forgeback()

        self.active_tab = "smelt"
        self.smelt_tab_button = None
        self.equip_tab_button = None
        self.badge_labels = {}

        self.list_frame = None
        self.cards = []

    def main(self):
        pass

    #--- Topbar ---#
    def setup_topbar(self):
        title_label = ctk.CTkLabel(self.forge_page.topbar_frame, text="Forge", font=ctk.CTkFont("Space Grotesk", 28, "bold"), text_color=self.config.text)
        title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        subtitle_label = ctk.CTkLabel(self.forge_page.topbar_frame, text="Smelt materials into gear · equip for real bonuses", font=self.config.body_font, text_color=self.config.muted)
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        badge_frame = ctk.CTkFrame(self.forge_page.topbar_frame, fg_color=self.config.card, corner_radius=20)
        badge_frame.grid(row=0, column=1, rowspan=2, padx=(20, 30), pady=15, sticky="e")

        self.forge_page.topbar_frame.grid_columnconfigure(1, weight=1)

        coin_icon = ctk.CTkLabel(badge_frame, text="●", font=self.config.label_font, text_color=self.config.gold)
        coin_icon.grid(row=0, column=0, padx=(16, 4), pady=10)
        self.badge_labels["coins"] = ctk.CTkLabel(badge_frame, text=str(self.forge_back.currency.get_currencies()), font=self.config.label_font, text_color=self.config.text)
        self.badge_labels["coins"].grid(row=0, column=1, padx=(0, 14), pady=10)

        for i, material in enumerate(("Wood", "Stone", "Clay", "Iron")):
            col = 2 + i * 2
            icon = ctk.CTkLabel(badge_frame, text=MATERIAL_ICON[material], font=self.config.label_font, text_color=self.config.muted)
            icon.grid(row=0, column=col, padx=(4, 4), pady=10)
            label = ctk.CTkLabel(badge_frame, text="0", font=self.config.label_font, text_color=self.config.text)
            label.grid(row=0, column=col + 1, padx=(0, 14 if i < 3 else 16), pady=10)
            self.badge_labels[material] = label

        self.refresh_badges()

    def refresh_badges(self):
        self.badge_labels["coins"].configure(text=str(self.forge_back.currency.get_currencies()))
        materials = self.forge_back.get_materials()
        for material in ("Wood", "Stone", "Clay", "Iron"):
            self.badge_labels[material].configure(text=str(materials[material]))

    #--- Tabs ---#
    def setup_forge_body(self):
        self.forge_page.frame.grid_rowconfigure(1, weight=1)
        self.forge_page.frame.grid_columnconfigure(0, weight=1)

        tab_frame = ctk.CTkFrame(self.forge_page.frame, fg_color="transparent")
        tab_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.smelt_tab_button = ctk.CTkButton(tab_frame, text="Smelt", font=self.config.button_font, width=90,
                                              corner_radius=10, command=lambda: self.select_tab("smelt"))
        self.smelt_tab_button.grid(row=0, column=0, padx=(0, 6))

        self.equip_tab_button = ctk.CTkButton(tab_frame, text="Equip", font=self.config.button_font, width=90,
                                              corner_radius=10, command=lambda: self.select_tab("equip"))
        self.equip_tab_button.grid(row=0, column=1)

        self.list_frame = ctk.CTkScrollableFrame(self.forge_page.frame, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.list_frame.grid_columnconfigure((0, 1), weight=1)

        self.select_tab("smelt")

    def select_tab(self, tab):
        self.active_tab = tab
        self.smelt_tab_button.configure(
            fg_color=self.config.ember if tab == "smelt" else self.config.card_hi,
            text_color="white" if tab == "smelt" else self.config.muted,
            hover_color=self.config.gold if tab == "smelt" else self.config.card,
        )
        self.equip_tab_button.configure(
            fg_color=self.config.ember if tab == "equip" else self.config.card_hi,
            text_color="white" if tab == "equip" else self.config.muted,
            hover_color=self.config.gold if tab == "equip" else self.config.card,
        )
        self.render_body()

    def render_body(self):
        for card in self.cards:
            card.destroy()
        self.cards = []

        if self.active_tab == "smelt":
            self.render_smelt_cards()
        else:
            self.render_equip_cards()

    #--- Smelt tab ---#
    def render_smelt_cards(self):
        for i, item_id in enumerate(GEAR_CATALOG):
            row, col = i // 2, i % 2
            self.build_smelt_card(item_id, row, col)

    def build_smelt_card(self, item_id, row, col):
        item = GEAR_CATALOG[item_id]
        can, reason = self.forge_back.can_smelt(item_id)
        already_smelted = self.forge_back.is_smelted(item_id)
        is_locked = self.forge_back.is_locked(item_id)

        card = ctk.CTkFrame(self.list_frame, fg_color=self.config.card, corner_radius=16)
        card.grid(row=row, column=col, padx=(0, 10) if col == 0 else (10, 0), pady=(0, 12), sticky="new")
        card.grid_columnconfigure(1, weight=1)
        self.cards.append(card)

        icon_frame = ctk.CTkFrame(card, width=44, height=44, fg_color=self.config.card_hi, corner_radius=12)
        icon_frame.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=16, sticky="n")
        icon_frame.grid_propagate(False)
        icon_frame.grid_columnconfigure(0, weight=1)
        icon_frame.grid_rowconfigure(0, weight=1)
        ctk.CTkLabel(icon_frame, text=item["icon"], font=ctk.CTkFont("Space Grotesk", 18)).grid(row=0, column=0)

        ctk.CTkLabel(card, text=item["name"], font=self.config.label_font, text_color=self.config.text).grid(row=0, column=1, padx=(0, 16), pady=(16, 0), sticky="w")
        ctk.CTkLabel(card, text=f"{item['slot_label']} · Path {item['path']} — {item['tag']}", font=self.config.body_font, text_color=self.config.muted).grid(row=1, column=1, padx=(0, 16), sticky="w")
        bonus_pady = (2, 14) if is_locked else (2, 8)
        ctk.CTkLabel(card, text=item["bonus_label"], font=self.config.body_font, text_color=self.config.green).grid(row=2, column=1, padx=(0, 16), pady=bonus_pady, sticky="w")

        if is_locked:
            ctk.CTkLabel(card, text=reason, font=self.config.body_font, text_color=self.config.red).grid(row=3, column=1, padx=(0, 16), pady=(0, 16), sticky="w")
            return

        cost_frame = ctk.CTkFrame(card, fg_color="transparent")
        cost_frame.grid(row=3, column=1, padx=(0, 16), pady=(0, 8), sticky="w")
        materials = self.forge_back.get_materials()
        have = materials.get(item["material"], 0)
        cost_color = self.config.green if have >= item["material_cost"] else self.config.red
        ctk.CTkLabel(cost_frame, text=f"{MATERIAL_ICON[item['material']]} {have} / {item['material_cost']} {item['material']}", font=self.config.body_font, text_color=cost_color).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(cost_frame, text=f"● {item['coin_cost']}", font=self.config.body_font, text_color=self.config.gold).grid(row=0, column=1)

        smelt_button = ctk.CTkButton(
            card, text="⚒ Already smelted" if already_smelted else "⚒ Smelt",
            font=self.config.button_font, corner_radius=10,
            fg_color=self.config.ember if can else self.config.card_hi,
            text_color="white" if can else self.config.muted,
            hover_color=self.config.gold if can else self.config.card_hi,
            state="normal" if can else "disabled",
            command=lambda: self.on_smelt_click(item_id),
        )
        smelt_button.grid(row=4, column=1, padx=(0, 16), pady=(0, 12), sticky="ew")

        if not can and not already_smelted:
            ctk.CTkLabel(card, text=reason, font=self.config.body_font, text_color=self.config.red).grid(row=5, column=1, padx=(0, 16), pady=(0, 14), sticky="w")

    def on_smelt_click(self, item_id):
        if self.forge_back.smelt(item_id):
            self.refresh_badges()
            self.render_body()
            self.refresh_home()

    #--- Equip tab ---#
    def render_equip_cards(self):
        smelted, equipped = self.forge_back.get_gear_state()
        if not smelted:
            empty_label = ctk.CTkLabel(self.list_frame, text="You haven't smelted any gear yet — head to the Smelt tab.", font=self.config.body_font, text_color=self.config.muted)
            empty_label.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="w")
            self.cards.append(empty_label)
            return

        for i, item_id in enumerate(smelted):
            row, col = i // 2, i % 2
            self.build_equip_card(item_id, equipped, row, col)

    def build_equip_card(self, item_id, equipped, row, col):
        item = GEAR_CATALOG[item_id]
        is_equipped = equipped.get(item["slot"]) == item_id

        card = ctk.CTkFrame(self.list_frame, fg_color=self.config.card, corner_radius=16)
        card.grid(row=row, column=col, padx=(0, 10) if col == 0 else (10, 0), pady=(0, 12), sticky="new")
        card.grid_columnconfigure(1, weight=1)
        self.cards.append(card)

        icon_frame = ctk.CTkFrame(card, width=44, height=44, fg_color=self.config.card_hi, corner_radius=12)
        icon_frame.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=16, sticky="n")
        icon_frame.grid_propagate(False)
        icon_frame.grid_columnconfigure(0, weight=1)
        icon_frame.grid_rowconfigure(0, weight=1)
        ctk.CTkLabel(icon_frame, text=item["icon"], font=ctk.CTkFont("Space Grotesk", 18)).grid(row=0, column=0)

        ctk.CTkLabel(card, text=item["name"], font=self.config.label_font, text_color=self.config.text).grid(row=0, column=1, padx=(0, 16), pady=(16, 0), sticky="w")
        ctk.CTkLabel(card, text=f"{item['slot_label']} · Path {item['path']} — {item['tag']}", font=self.config.body_font, text_color=self.config.muted).grid(row=1, column=1, padx=(0, 16), sticky="w")
        ctk.CTkLabel(card, text=item["bonus_label"], font=self.config.body_font, text_color=self.config.green).grid(row=2, column=1, padx=(0, 16), pady=(2, 10), sticky="w")

        toggle_button = ctk.CTkButton(
            card, text="✓ Equipped" if is_equipped else "Equip",
            font=self.config.button_font, corner_radius=10,
            fg_color=self.config.green if is_equipped else self.config.ember,
            hover_color=self.config.card_hi if is_equipped else self.config.gold,
            text_color=self.config.nav if is_equipped else "white",
            command=lambda: self.on_equip_toggle_click(item_id, item["slot"], is_equipped),
        )
        toggle_button.grid(row=3, column=1, padx=(0, 16), pady=(0, 14), sticky="ew")

    def on_equip_toggle_click(self, item_id, slot, is_equipped):
        if is_equipped:
            self.forge_back.unequip(slot)
        else:
            self.forge_back.equip(item_id)
        self.render_body()
        self.refresh_home()

    #--- Home sync ---#
    def refresh_home(self):
        refresh = getattr(self.home_page, "refresh_materials_and_gear", None)
        if refresh is not None:
            refresh()
