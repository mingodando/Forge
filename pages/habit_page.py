from backend.config import Config
from backend.start_setup import Setup

class Habit:
    def __init__(self, setup):
        self.config = Config()
        self.config.main()
        self.setup = setup

    def main(self):
        pass