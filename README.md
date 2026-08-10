# Forge

Forge is a desktop app (built with CustomTkinter) that turns everyday productivity — schoolwork, chores,
workouts, focus sessions — into an RPG-style progression system. It's aimed at students and anyone else
who struggles to stay focused: instead of a plain to-do list, finishing real tasks earns you coins and XP,
levels you up, and lets you craft gear that makes future progress a little faster.

This is a personal project — a rebuild of an earlier app called Probo, redone from scratch as Forge with a
clearer gameplan.

## How to Download

Go to the **[Releases page](https://github.com/mingodando/Forge/releases)** (also linked on the right side
of the repo homepage under "Releases"), then pick your OS below.

### Windows
1. On the latest release, under **Assets**, click **`Forge.exe`** to download it.
2. Once downloaded, Windows Defender will show a warning ("Windows protected your PC"). Click **More info**, then **Run anyway**.
3. The app will ask for your username — enter it, and you're in.

### Mac
1. On the latest release, under **Assets**, click **`ForgeApp-mac.zip`** to download it.
2. Double-click the downloaded zip to unzip it — this creates a **`Forge.app`** file (it has the app icon).
3. **Right-click** (or Control-click) `Forge.app` and choose **Open**. macOS will warn that it's from an unidentified developer — click **Open** again to confirm. (This step is only needed the first time.)
4. The app will ask for your username — enter it, and you're in.

**If step 3 instead says "Forge is damaged and can't be opened"** (this can happen if the app was passed
through email/chat instead of downloaded straight from the Release page, which can corrupt its signature):
open **Terminal**, type `xattr -cr ` (with a trailing space), drag `Forge.app` into the Terminal window,
press Enter, then try step 3 again.

Your progress is saved locally (in `%APPDATA%\Forge` on Windows, or the equivalent user data folder on
Mac), so it persists across app updates and isn't tied to any account.

## How it works

Everything in Forge revolves around one loop: **complete something → earn coins, XP, and crafting
materials → spend them to grow stronger and unlock more.**

### Home
Your dashboard. Shows your current level and title, XP progress toward the next level, coin balance and
today's net coin flow, your best current habit streak, and a Focus timer widget.

### Quests
One-off tasks for things you need to do once — e.g. "Finish math homework." When creating a quest you
pick a **category** (Social, Work, Study, or Exercise) and a **difficulty** (Easy, Medium, or Hard).
Difficulty sets the reward:

| Difficulty | Coins | XP        |
|------------|-------|-----------|
| Easy       | 10    | 60        |
| Medium     | 20    | 120       |
| Hard       | 30    | 180       |

Completing a quest also drops crafting materials tied to its category (Social → Wood, Work → Stone,
Study → Clay, Exercise → Iron; more materials for harder quests). Quests reset daily and you have a
limited number of slots per day (5 by default — buyable in the Shop).

### Habits
Recurring daily tasks — things you want to build a routine around. Checking off a habit each day builds a
**streak**, and pays out the same coin/XP rewards as quests based on difficulty. Miss a day and your
streak normally resets to 0 — unless you're protected by a **streak shield** (see Forge below), which lets
you absorb a missed day without losing progress. You get a limited number of habit slots per day (3 by
default).

### Forge
Where you spend crafting materials and coins to smelt gear, then equip it across three slots — **Main
Hand**, **Off Hand**, and **Chest**. Gear gives passive bonuses: extra XP gain, extra streak-shield
charges, or extra missed-day protection for habits. Some gear unlocks only once you reach a certain
level.

### Shop
Spend coins on one-off upgrades and consumables:
- **Extra quest slot** — permanently raises your daily quest cap by 1.
- **Streak revival** — restores a broken habit streak to what it was before it reset.
- **Shield refresh** — refills the shield charges on your equipped Off-Hand gear.
- **Ember skin** — a cosmetic weapon finish (no stat effect).

### Focus
A focus-timer feature that rewards longer, uninterrupted focus sessions. The more total minutes you focus
in a day, the bigger the one-time coin bonus for that day (thresholds at 30/60/90/120+ minutes).

### Settings
Export your save file as a backup, or reset all progress back to a fresh start.

## Leveling

XP earned from quests, habits, and focus sessions feeds a single level track. Each level needs
progressively more XP than the last, and every level has its own title — starting at "Tinkerer" and
climbing through smith-and-forge-themed ranks (e.g. "Apprentice Smith," "Master Smith," "Forgefather")
up to "Legendary Forgemaster" and beyond.

## Building from source

The app is a standard CustomTkinter/Pillow Python app (see `requirements.txt`). To build a standalone
executable yourself:

```
pip install -r requirements.txt
pyinstaller main.spec --noconfirm
```

Always build from `main.spec`, not `main.py` directly — running PyInstaller straight against `main.py`
regenerates the spec file and drops the bundled images/fonts, which will crash the resulting app on
launch. `dist/Forge.exe` (Windows) or `dist/Forge.app` (Mac) is the result.

GitHub Actions (`.github/workflows/build.yml`) builds both platforms automatically on every push to `main`.