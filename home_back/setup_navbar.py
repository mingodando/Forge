import customtkinter as ctk
from PIL import Image

from backend.start_setup import Setup
from backend.config import Config

from pages.home_page import Home
from pages.quest_page import Quest
from pages.habit_page import Habit
from pages.forge_page import Forge
from pages.settings_page import Settings
from pages.shop_page import Shop
from backend.directory_setup import Directory

class SetupNavbar:
    def __init__(self, setup):
        self.config = Config()
        self.config.main()
        self.setup = setup
        self.home = Home(setup)
        self.quest = Quest(setup)
        self.habit = Habit(setup)
        self.forge = Forge(setup)
        self.shop = Shop(setup)
        self.settings = Settings(setup)
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
                                              font=self.config.levelup_font, text_color=self.config.primary_text,
                                              image=self.logo_button_image, compound="left")
        self.title_home_button.grid(row=0, column=0)

        self.home_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Home", font=self.config.page_font,
                                         text_color=self.config.primary_text, image=self.home_button_image,
                                         fg_color=self.config.sidebar_color, hover_color=self.config.navhover_color,
                                         compound="top", command=lambda: self.on_nav_click(self.home_button, self.home.main))
        self.home_button.grid(row=1, column=0, padx=10)

        self.quest_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Quests",
                                          font=self.config.page_font,
                                          text_color=self.config.primary_text, image=self.quest_button_image,
                                          fg_color=self.config.sidebar_color, hover_color=self.config.navhover_color,
                                          compound="top", command=lambda: self.on_nav_click(self.quest_button, self.quest.main))
        self.quest_button.grid(row=2, column=0, padx=10)

        self.habit_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Habits",
                                          font=self.config.page_font,
                                          text_color=self.config.primary_text, image=self.habit_button_image,
                                          fg_color=self.config.sidebar_color, hover_color=self.config.navhover_color,
                                          compound="top", command=lambda: self.on_nav_click(self.habit_button, self.habit.main))
        self.habit_button.grid(row=3, column=0, padx=10)

        self.forge_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Forge",
                                          font=self.config.page_font,
                                          text_color=self.config.primary_text, image=self.forge_button_image,
                                          fg_color=self.config.sidebar_color, hover_color=self.config.navhover_color,
                                          compound="top", command=lambda: self.on_nav_click(self.forge_button, self.forge.main))
        self.forge_button.grid(row=4, column=0, padx=10)

        self.shop_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Shop",
                                          font=self.config.page_font,
                                          text_color=self.config.primary_text, image=self.shop_button_image,
                                          fg_color=self.config.sidebar_color, hover_color=self.config.navhover_color,
                                          compound="top", command=lambda: self.on_nav_click(self.shop_button, self.shop.main))
        self.shop_button.grid(row=5, column=0, padx=10)

        self.settings_button = ctk.CTkButton(self.setup.navbar, height=60, width=80, text="Settings",
                                             font=self.config.page_font,
                                             text_color=self.config.primary_text, image=self.settings_button_image,
                                             fg_color=self.config.sidebar_color, hover_color=self.config.navhover_color,
                                             compound="top", command=lambda: self.on_nav_click(self.settings_button, self.settings.main))
        self.settings_button.grid(row=6, column=0, padx=10)

        self.nav_buttons = [self.home_button, self.quest_button, self.habit_button,
                             self.forge_button, self.shop_button, self.settings_button]
        self.select_nav_button(self.home_button)

    def on_nav_click(self, button, page_main):
        self.select_nav_button(button)
        page_main()

    def select_nav_button(self, button):
        for nav_button in self.nav_buttons:
            nav_button.configure(fg_color=self.config.sidebar_color, text_color=self.config.primary_text)

        button.configure(fg_color=self.config.nav_tab_color, text_color=self.config.amber)
        self.active_button = button

