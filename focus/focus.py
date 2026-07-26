import datetime
import os
from tkinter import messagebox

from backend.directory_setup import Directory
from currency.currency import Currency

class Focus:
    def __init__(self):
        self.directory = Directory()
        self.currency = Currency()

    def main(self):
        pass

    def log_session(self, minutes):
        path = self.directory.focus_file()
        timestamp = datetime.datetime.now().isoformat()
        with open(path, "a") as file:
            file.write(f"At: {timestamp}, Focused For: {minutes}\n")

    def get_today_focus(self):
        path = self.directory.focus_file()
        today = datetime.date.today()
        minutes = 0
        sessions = 0
        if os.path.exists(path):
            with open(path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    timestamp_part, minutes_part = line.split(", ")
                    timestamp_str = timestamp_part.removeprefix("At: ")
                    minutes_str = minutes_part.removeprefix("Focused For: ")
                    entry_date = datetime.datetime.fromisoformat(timestamp_str).date()
                    if entry_date == today:
                        minutes += int(minutes_str)
                        sessions += 1
        return {"minutes": minutes, "sessions": sessions}

    # --- Rewards ---#
    def rewards(self):
        minutes = self.get_today_focus()["minutes"]

        if minutes > 120:
            reward_amount = 90
            messagebox.showinfo("Rewarded", "You got 90 coins")
        elif minutes > 90:
            reward_amount = 60
            messagebox.showinfo("Rewarded", "You got 60 coins")
        elif minutes > 60:
            reward_amount = 30
            messagebox.showinfo("Rewarded", "You got 30 coins")
        elif minutes > 30:
            reward_amount = 15
            messagebox.showinfo("Rewarded", "You got 15 coins")
        else:
            reward_amount = 0

        already_paid = self.get_reward_paid_today()
        if reward_amount > already_paid:
            self.currency.currency_change(reward_amount - already_paid)
            self.set_reward_paid_today(reward_amount)
            if reward_amount == 90:
                messagebox.showinfo("Rewarded", "You got 90 coins")

    def get_reward_paid_today(self):
        path = self.directory.reward_state_file()
        if not os.path.exists(path):
            return 0
        with open(path, "r") as file:
            content = file.read().strip()
        if not content:
            return 0
        date_str, amount_str = content.split(",")
        if date_str != datetime.date.today().isoformat():
            return 0
        return int(amount_str)

    def set_reward_paid_today(self, amount):
        path = self.directory.reward_state_file()
        with open(path, "w") as file:
            file.write(f"{datetime.date.today().isoformat()},{amount}")


if __name__ == "__main__":
    f = Focus()
    print(f.get_today_focus())