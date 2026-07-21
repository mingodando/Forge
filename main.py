import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup
from pages.home_page import get_home
from pages.quest_page import Quest
from pages.habit_page import Habit
from pages.forge_page import Forge
from pages.shop_page import Shop
from pages.settings_page import Settings
from home_back.clock import Time
from home_back.setup_navbar import SetupNavbar
from home_front.home import HomePage

class App:
    def __init__(self):
        #--- Main Window Activation ---#
        self.root = ctk.CTk()

        #--- OS Directory ---#
        self.current_directory = None

        #--- Other File Activation ---#
        self.setup = get_setup()
        self.config = Config()
        self.setupnavbar = SetupNavbar()
        self.home_page = get_home()
        self.quest_page = Quest()
        self.habit_page = Habit()
        self.forge_page = Forge()
        self.shop_page = Shop()
        self.settings_page = Settings()
        self.time = Time()
        self.home_front = HomePage()
        self.config.main()

        #--- Topbar Widgets ---#
        self.topbar_currency_display = None
        self.topbar_level_display = None
        self.xp_level_display = None
        self.onboard_display1 = None
        self.onboard_display2 = None

        #--- Navbar Widgets ---#
        self.title_home_button = None
        self.home_button = None
        self.quest_button = None
        self.habit_button = None

        #--- Images ---#
        self.forge_raw_image = None
        self.forge_button_image = None
        self.home_raw_image = None
        self.home_button_image = None
        self.quest_raw_image = None
        self.quest_button_image = None
        self.habit_raw_image = None
        self.habit_button_image = None

#----- Starting Functions -----#
    def main(self):
        self.root.title("Forge")
        self.root.geometry("1280x800")

        self.setup.create_home_page(self.root)
        self.setup.navbar.columnconfigure(0, weight=1)
        self.setupnavbar.setup_navbar()
        self.setup_topbar()
        self.setup_app()
        self.home_page.main()
        self.home_front.main()

        self.root.mainloop()

    def setup_app(self):
        self.setup.setup_files()

    def setup_topbar_images(self):
        pass

    def setup_topbar(self):
        self.setup.topbar.columnconfigure(0, weight=1)
        self.setup.topbar.rowconfigure(1, weight=1)

        self.onboard_display1 = ctk.CTkLabel(self.setup.topbar, text=self.time.print_date(), font=self.config.body_font, text_color=self.config.muted)
        self.onboard_display1.grid(row=0, column=0, padx=20, pady=(10,0), sticky="w")

        self.onboard_display2 = ctk.CTkLabel(self.setup.topbar, text=self.time.print_time(), font=self.config.heading_font, text_color=self.config.text)
        self.onboard_display2.grid(row=1, column=0, padx=20, sticky="wn")


if __name__ == "__main__":
    app = App()
    app.main()