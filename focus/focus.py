import datetime
import os

from backend.directory_setup import Directory

class Focus:
    def __init__(self):
        self.directory = Directory()

    def main(self):
        pass

    def log_session(self, minutes):
        path = self.directory.focus_file()
        timestamp = datetime.datetime.now().isoformat()
        with open(path, "a") as f:
            f.write(f"{timestamp},{minutes}\n")

    def get_today_focus(self):
        path = self.directory.focus_file()
        today = datetime.date.today()
        minutes = 0
        sessions = 0
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    timestamp_str, minutes_str = line.split(",")
                    entry_date = datetime.datetime.fromisoformat(timestamp_str).date()
                    if entry_date == today:
                        minutes += int(minutes_str)
                        sessions += 1
        return {"minutes": minutes, "sessions": sessions}


if __name__ == "__main__":
    f = Focus()
    print(f.get_today_focus())