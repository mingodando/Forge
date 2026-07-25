import datetime
import os

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
            self.currency.currency_change(90)
        elif minutes > 90:
            self.currency.currency_change(60)
        elif minutes > 60:
            self.currency.currency_change(30)
        elif minutes > 30:
            self.currency.currency_change(15)


if __name__ == "__main__":
    f = Focus()
    print(f.get_today_focus())