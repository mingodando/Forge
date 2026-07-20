from backend.config import Config
from backend.start_setup import get_setup

class Habit:
    def __init__(self):
        self.config = Config()
        self.config.main()
        self.setup = get_setup()

    def main(self):
        pass