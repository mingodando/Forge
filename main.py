import customtkinter as ctk

from backend.config import Config
from backend.start_setup import get_setup
from pages.home_page import get_home
from pages.quest_page import get_quest
from pages.habit_page import get_habit
from pages.forge_page import get_forge
from pages.shop_page import get_shop
from pages.settings_page import get_settings
from home_back.clock import Time
from home_back.setup_navbar import SetupNavbar
from home_front.home import HomePage
from quest.quest_front import QuestFront

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
        self.quest_page = get_quest()
        self.habit_page = get_habit()
        self.forge_page = get_forge()
        self.shop_page = get_shop()
        self.settings_page = get_settings()
        self.time = Time()
        self.home_front = HomePage()
        self.quest_front = QuestFront()
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
        self.setup_app()
        self.home_front.setup_topbar()

        self.home_page.main()
        self.home_front.main()
        self.quest_page.main()
        self.habit_page.main()
        self.forge_page.main()
        self.shop_page.main()
        self.settings_page.main()

        self.quest_front.setup_topbar()
        self.quest_front.setup_quest_list()

        self.setupnavbar.register_topbar(self.home_page.frame, self.home_front.home_topbar)
        self.setupnavbar.register_topbar(self.quest_page.frame, self.quest_page.topbar_frame)
        self.setupnavbar.setup_navbar()

        self.root.mainloop()

    def setup_app(self):
        self.setup.setup_files()
        self.setup.check_user_name()

if __name__ == "__main__":
    app = App()
    app.main()