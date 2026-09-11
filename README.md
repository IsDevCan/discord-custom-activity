# ✨ Discord Custom Activity & Rich Presence Manager

A lightweight, zero-dependency tool that lets you display **any custom game or activity** on your Discord profile with live timers, custom descriptions, and clickable profile buttons.

Created with ❤️ by **[IsDevCan](https://github.com/IsDevCan)**.

---

## 🌟 Features

- 🖥️ **Zero Terminal Visual GUI:** Control your Discord status from an easy web dashboard—no terminal knowledge required!
- 🖱️ **Double-Click Launchers:** Built-in `.command` (Mac) and `.bat` (Windows) scripts for instant 1-click launch.
- 🎮 **100% Custom Activity Names:** Display *any* title on your Discord profile (e.g., `Grand Theft Auto VI`, `Silksong`, `Studying for Exams`, `Watching Anime`).
- 📝 **Two Customizable Status Lines:** Fully customize **Details** (Line 1) and **State** (Line 2).
- 🔗 **Clickable Profile Buttons:** Add up to 2 clickable links directly to your Discord profile card (e.g., `Join My Stream`, `GitHub Profile`, `Play With Me`).
- ⚡ **Popular Game Presets:** Built-in instant presets for *VALORANT, Fortnite, Rocket League, Overwatch 2, Minecraft, Roblox, CS2, GTA V*, and more.
- 🪶 **Zero Resource Consumption:** Runs at **0.0% CPU**, zero battery drain, and zero fan noise.
- 📦 **No Dependencies:** Pure Python standard library—no `pip install` needed.
- 💻 **Cross-Platform:** Works on macOS, Windows, and Linux.

---

## 🚀 How to Use

### Option 1: Visual GUI (Recommended - No Terminal Needed!)

#### On macOS:
1. Double-click **`Launch-GUI.command`**.
2. A beautiful visual control panel opens automatically in your browser.
3. Pick a preset or type any custom game, then click **▶ Start Activity on Discord**!

#### On Windows:
1. Double-click **`Launch-GUI.bat`**.
2. Customize your game and click Start!

*(Or run `python3 app.py` from inside the folder).*

---

### Option 2: Terminal / Command Line Usage

> [!TIP]
> Make sure to navigate into the folder first:
> ```bash
> cd discord-custom-activity
> ```

#### Interactive Mode
```bash
python3 activity.py
```
Follow the interactive prompts to choose a preset or type in your custom game name, details, state, and buttons!

#### Instant One-Line Commands

**Custom Game / Activity:**
```bash
python3 activity.py --name "Grand Theft Auto VI" --details "Heist Mission" --state "5 Stars"
```

**Custom Activity with Clickable Profile Button:**
```bash
python3 activity.py --name "Coding" --details "Working on Open Source" --state "Python Project" --btn-text "GitHub Profile" --btn-url "https://github.com/IsDevCan"
```

**Instant Game Presets:**
```bash
python3 activity.py --preset valorant
python3 activity.py --preset fortnite
python3 activity.py --preset rocket_league
python3 activity.py --preset gta5
python3 activity.py --preset minecraft
python3 activity.py --preset roblox
```

---

### Option 3: Background Daemon Mode (Run 24/7)

**Start in background:**
```bash
./start.sh --name "GTA 6" --details "Exploring Vice City" --state "Story Mode"
```

**Check status:**
```bash
./status.sh
```

**Stop:**
```bash
./stop.sh
```

---

## 📄 License

MIT License • Free for everyone • Created by **[IsDevCan](https://github.com/IsDevCan)**
