import customtkinter as ctk

from backend.config import Config
from currency.currency import Currency

TIER_LEVEL = {
    "easy": 10,
    "medium": 20,
    "hard": 30,
}

class QuestBack:
    def __init__(self):
        self.config = Config()
        self.currency = Currency()

    def main(self):
        pass
