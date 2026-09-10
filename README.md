# ✨ Discord Custom Activity & Rich Presence Manager

A lightweight, zero-dependency tool that lets you display **any custom game or activity** on your Discord profile with live timers, custom descriptions, and clickable profile buttons.

Created by **[IsDevCan](https://github.com/IsDevCan)**.

---

## 🌟 Features

- **100% Custom Activity Names:** Display *any* title on your Discord profile (e.g., `GTA 6`, `Silksong`, `Studying for Exams`, `Watching Anime`).
- **Two Customizable Status Lines:** Fully customize **Details** (Line 1) and **State** (Line 2).
- **Clickable Profile Buttons:** Add up to 2 clickable links directly to your Discord profile card (e.g., `Join My Stream`, `GitHub Profile`, `Play With Me`).
- **Popular Game Presets:** Built-in instant presets for *VALORANT, Fortnite, Rocket League, Overwatch, Rainbow Six Siege, GTA V*, and more.
- **Zero Resource Consumption:** Runs at **0.0% CPU**, zero battery drain, and zero fan noise.
- **No Dependencies:** Pure Python standard library—no `pip install` required.
- **Cross-Platform:** Works on macOS, Windows, and Linux.

---

## 🚀 Quick Start

### 1. Interactive Mode (Recommended)
Simply run the script to launch the interactive terminal wizard:
```bash
python3 activity.py
```
Follow the on-screen prompts to choose a preset or type in your custom game name, details, state, and buttons!

---

### 2. Quick Command Line Usage

**Custom Game / Activity:**
```bash
python3 activity.py --name "Grand Theft Auto VI" --details "Heist Mission" --state "5 Stars"
```

**Custom Activity with Clickable Profile Button:**
```bash
python3 activity.py --name "Coding" --details "Working on Open Source" --state "Python Project" --btn-text "GitHub Profile" --btn-url "https://github.com/IsDevCan"
```

**Instant Game Preset:**
```bash
python3 activity.py --preset valorant
python3 activity.py --preset fortnite
python3 activity.py --preset rocket_league
python3 activity.py --preset gta5
```

---

### 3. Background Daemon Mode (Run 24/7)

**Start in background:**
```bash
./start.sh --name "GTA 6" --details "Exploring Vice City" --state "Story Mode"
```

**Check status anytime:**
```bash
./status.sh
```

**Stop background activity:**
```bash
./stop.sh
```

---

## ⚙️ Requirements & Settings
- Python 3.7+ (Pre-installed on macOS and Linux)
- Official Discord Desktop App open and running.
- In Discord: **User Settings (⚙️) > Activity Privacy**:
  - Ensure **"Display current activity as a status message"** is toggled **ON**.

---

## 🔒 Safety & TOS Compliance
- **No Self-Botting:** Never asks for or uses your Discord account token or password.
- **Official IPC:** Uses Discord's built-in local IPC socket (`discord-ipc-0`), exactly like Spotify and official games.
- **Clean & Safe:** Does not inject or modify Discord client files.

---

## 👤 Author
- **IsDevCan** - [GitHub Profile](https://github.com/IsDevCan)
