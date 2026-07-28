import customtkinter as ctk
from PIL import Image

from backend.start_setup import get_setup
from backend.config import Config
from backend.directory_setup import Directory


from pages.home_page import get_home
from pages.quest_page import get_quest
from pages.habit_page import get_habit
from pages.forge_page import get_forge
from pages.settings_page import get_settings
from pages.shop_page import get_shop

class SetupNavbar:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()
        self.home = get_home()
        self.quest = get_quest()
        self.habit = get_habit()
        self.forge = get_forge()
        self.shop = get_shop()
        self.settings = get_settings()
        self.directory = Directory()

        self.current_directory = None

        self.logo_raw_image = None
        self.home_raw_image = None
        self.quest_raw_image = None
        self.habit_raw_image = None
        self.forge_raw_image = None
        self.shop_raw_image = None
        self.settings_raw_image = None

        self.logo_button_image = None
        self.quest_button_image = None
        self.habit_button_image = None
        self.home_button_image = None
        self.forge_button_image = None
        self.shop_button_image = None
        self.settings_button_image = None

        self.home_button = None
        self.quest_button = None
        self.habit_button = None
        self.forge_button = None
        self.title_home_button = None
        self.shop_button = None
        self.settings_button = None

        self.nav_buttons = []
        self.active_button = None

        self.topbar_by_frame = {}
        self.active_topbar = None

    def setup_navbar_images(self):
        self.current_directory = self.directory.images_directory()
        self.logo_raw_image = Image.open(rf"{self.current_directory}\logo.jpg")
        self.home_raw_image = Image.open(rf"{self.current_directory}\home_logo.jpg")
        self.quest_raw_image = Image.open(rf"{self.current_directory}\quest_logo.jpg")
        self.habit_raw_image = Image.open(rf"{self.current_directory}\habit_logo.jpg")
        self.forge_raw_image = Image.open(rf"{self.current_directory}\forge_logo.jpg")
        self.shop_raw_image = Image.open(rf"{self.current_directory}\shop_logo.jpg")
        self.settings_raw_image = Image.open(rf"{self.current_directory}\settings_logo.jpg")

    def setup_navbar(self):
        self.setup_navbar_images()

        self.logo_button_image = ctk.CTkImage(light_image=self.logo_raw_image,
                                               dark_image=self.logo_raw_image,
                                              size=(80, 80))

        self.home_button_image = ctk.CTkImage(light_image=self.home_raw_image,
                                              dark_image=self.home_raw_image)

        self.quest_button_image = ctk.CTkImage(light_image=self.quest_raw_image,
                                               dark_image=self.quest_raw_image)

        self.habit_button_image = ctk.CTkImage(light_image=self.habit_raw_image,
                                               dark_image=self.habit_raw_image)

        self.forge_button_image = ctk.CTkImage(light_image=self.forge_raw_image,
                                               dark_image=self.forge_raw_image
                                               )
        self.shop_button_image = ctk.CTkImage(light_image=self.shop_raw_image,
                                              dark_image=self.shop_raw_image)

        self.settings_button_image = ctk.CTkImage(light_image=self.settings_raw_image,
                                                dark_image=self.settings_raw_image)

        self.title_home_button = ctk.CTkLabel(self.setup.navbar, height=60, width=120, text="Forge",
                                              font=self.config.heading_font, text_color=self.config.text,
                                              image=self.logo_button_image, compound="left")
        self.title_home_button.grid(row=0, column=0)

        self.home_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Home", font=self.config.body_font,
                                         text_color=self.config.text, image=self.home_button_image,
                                         fg_color=self.config.nav, hover_color=self.config.card_hi,
                                         compound="top", command=lambda: self.on_nav_click(self.home_button, self.home.frame))
        self.home_button.grid(row=1, column=0, padx=10)

        self.quest_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Quests",
                                          font=self.config.body_font,
                                          text_color=self.config.text, image=self.quest_button_image,
                                          fg_color=self.config.nav, hover_color=self.config.card_hi,
                                          compound="top", command=lambda: self.on_nav_click(self.quest_button, self.quest.frame))
        self.quest_button.grid(row=2, column=0, padx=10)

        self.habit_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Habits",
                                          font=self.config.body_font,
                                          text_color=self.config.text, image=self.habit_button_image,
                                          fg_color=self.config.nav, hover_color=self.config.card_hi,
                                          compound="top", command=lambda: self.on_nav_click(self.habit_button, self.habit.frame))
        self.habit_button.grid(row=3, column=0, padx=10)

        self.forge_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Forge",
                                          font=self.config.body_font,
                                          text_color=self.config.text, image=self.forge_button_image,
                                          fg_color=self.config.nav, hover_color=self.config.card_hi,
                                          compound="top", command=lambda: self.on_nav_click(self.forge_button, self.forge.frame))
        self.forge_button.grid(row=4, column=0, padx=10)

        self.shop_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Shop",
                                          font=self.config.body_font,
                                          text_color=self.config.text, image=self.shop_button_image,
                                          fg_color=self.config.nav, hover_color=self.config.card_hi,
                                          compound="top", command=lambda: self.on_nav_click(self.shop_button, self.shop.frame))
        self.shop_button.grid(row=5, column=0, padx=10)

        self.settings_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Settings",
                                             font=self.config.body_font,
                                             text_color=self.config.text, image=self.settings_button_image,
                                             fg_color=self.config.nav, hover_color=self.config.card_hi,
                                             compound="top", command=lambda: self.on_nav_click(self.settings_button, self.settings.frame))
        self.settings_button.grid(row=6, column=0, padx=10)

        self.nav_buttons = [self.home_button, self.quest_button, self.habit_button,
                             self.forge_button, self.shop_button, self.settings_button]
        self.on_nav_click(self.home_button, self.home.frame)

    def register_topbar(self, frame, topbar_frame):
        self.topbar_by_frame[frame] = topbar_frame

    def on_nav_click(self, button, frame):
        self.select_nav_button(button)
        frame.tkraise()

        topbar_frame = self.topbar_by_frame.get(frame)
        if topbar_frame is not self.active_topbar:
            if self.active_topbar is not None:
                self.active_topbar.grid_remove()
            if topbar_frame is not None:
                topbar_frame.grid()
            self.active_topbar = topbar_frame

    def select_nav_button(self, button):
        for nav_button in self.nav_buttons:
            nav_button.configure(fg_color=self.config.nav, text_color=self.config.text)

        button.configure(fg_color=self.config.card, text_color=self.config.gold)
        self.active_button = button

