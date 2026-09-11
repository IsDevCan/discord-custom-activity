# ✨ Discord Custom Activity & Rich Presence Manager

A lightweight, zero-dependency tool that lets you display **any custom game or activity** on your Discord profile with live timers, custom descriptions, and clickable profile buttons.

Flex unreleased games like **Grand Theft Auto VI**, **Hollow Knight: Silksong**, **Half-Life 3**, or drop your own custom meme images!

Created with ❤️ by **[IsDevCan](https://github.com/IsDevCan)**.

---

## 🌟 Features

- 🖥️ **Zero Terminal Visual GUI:** Control your Discord status from a sleek web dashboard—no terminal knowledge required!
- 🎲 **Meme & Unreleased Games Vault:** Built-in instant presets for *GTA 6, Silksong, Half-Life 3, Bloodborne PC, Portal 3, Elder Scrolls VI, Titanfall 3, Minecraft 2, Chess 2, Touching Grass Simulator, Free Nitro Generator*, and more!
- 🖼️ **Drag & Drop Custom Images:** Drop any PNG, JPG, or meme picture directly into the app to use it as your custom Discord game logo!
- 🖱️ **Double-Click Launchers:** Built-in `.command` (Mac) and `.bat` (Windows) scripts for instant 1-click launch.
- 🎮 **100% Custom Activity Names:** Display *any* title on your Discord profile.
- 📝 **Two Customizable Status Lines:** Fully customize **Details** (Line 1) and **State** (Line 2).
- 🔗 **Clickable Profile Buttons:** Add up to 2 clickable links directly to your Discord profile card.
- ⚡ **Popular Esports Presets:** Instant presets for *VALORANT, Fortnite, Rocket League, Overwatch 2, Minecraft, Roblox, CS2, GTA V*, and more.
- 🪶 **Zero Resource Consumption:** Runs at **0.0% CPU**, zero battery drain, and zero fan noise.
- 📦 **No Dependencies:** Pure Python standard library—no `pip install` needed.
- 💻 **Cross-Platform:** Works on macOS, Windows, and Linux.

---

## 🚀 How to Use

### Option 1: Visual GUI (Recommended - No Terminal Needed!)

#### On macOS:
1. Double-click **`Launch-GUI.command`** (or the shortcut on your Desktop).
2. A visual control panel opens automatically in your browser.
3. Pick a meme preset, drop a picture, or type any custom game, then click **▶ Start Activity on Discord**!

#### On Windows:
1. Double-click **`Launch-GUI.bat`**.
2. Pick your game and click Start!

*(Or run `python3 app.py` from inside the folder).*

---

### Option 2: Terminal / Command Line Usage

> [!TIP]
> Navigate into the folder first:
> ```bash
> cd discord-custom-activity
> ```

#### 🔥 Meme & Troll One-Liners

```bash
# Grand Theft Auto VI (Early Dev Build)
python3 activity.py --preset gta6

# Hollow Knight: Silksong (Waiting Since 2019)
python3 activity.py --preset silksong

# Half-Life 3 (Valve Internal Beta)
python3 activity.py --preset halflife3

# Bloodborne PC Remaster (4K 120FPS)
python3 activity.py --preset bloodborne

# Minecraft 2 (Unreal Engine 5 Edition)
python3 activity.py --preset minecraft2

# Touching Grass Simulator 2026
python3 activity.py --preset grass

# Free Discord Nitro Generator 3D
python3 activity.py --preset nitro
```

#### 🎮 Esports & Popular Game Presets

```bash
python3 activity.py --preset valorant
python3 activity.py --preset fortnite
python3 activity.py --preset rocket_league
python3 activity.py --preset gta5
```

#### Custom Game / Activity:
```bash
python3 activity.py --name "Custom Game" --details "Playing Solo" --state "Level 100"
```

---

## 📄 License

MIT License • Free for everyone • Created by **[IsDevCan](https://github.com/IsDevCan)**
