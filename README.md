# ✨ Discord Custom Activity & Rich Presence Manager

[![Release](https://img.shields.io/badge/release-v1.0.0--beta-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://github.com/IsDevCan/discord-custom-activity/releases)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-brightgreen?style=for-the-badge)](https://github.com/IsDevCan/discord-custom-activity)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Standard%20Lib)-success?style=for-the-badge)](https://github.com/IsDevCan/discord-custom-activity)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

A powerful, zero-dependency tool that lets you display **any custom game, meme, or custom image** on your Discord profile card with live timers, custom descriptions, and clickable profile buttons!

Flex unreleased games like **Grand Theft Auto VI**, **Hollow Knight: Silksong**, **Half-Life 3**, or drop your own custom meme pictures with automatic cloud hosting!

Created with ❤️ by **[IsDevCan](https://github.com/IsDevCan)**.

---

## 🌟 Highlights & Features

- 🖥️ **Zero-Terminal Web Dashboard:** Control your Discord status from a sleek visual dashboard with live preview.
- 🖼️ **Instant Drag & Drop Custom Images:** Drop any PNG, JPG, or meme picture from your computer. The app automatically publishes it so it displays directly on your Discord profile!
- 🎲 **Meme & Unreleased Games Vault:** Built-in instant presets with official high-res logos:
  - 🚗 *Grand Theft Auto VI (Early Access Dev Build)*
  - 🪡 *Hollow Knight: Silksong (Waiting Since 2019)*
  - λ³ *Half-Life 3 (Valve Internal Beta v0.9)*
  - 🩸 *Bloodborne PC Remaster (4K 120FPS)*
  - 🎂 *Portal 3 (Aperture Science Testing)*
  - ⚔️ *The Elder Scrolls VI: Hammerfell*
  - 🤖 *Titanfall 3 (Pilot Match)*
  - ⛏️ *Minecraft 2 (Unreal Engine 5 Edition)*
  - ♟️ *Chess 2: Battle Royale*
  - 🌿 *Touching Grass Simulator 2026*
  - 💎 *Free Discord Nitro Generator 3D*
  - 🛹 *Skate 4 (Closed Developer Playtest)*
- 🖱️ **1-Click Launchers:** Built-in `.command` (Mac) and `.bat` (Windows) scripts—just double-click to launch!
- 🔗 **Clickable Profile Buttons:** Add up to 2 clickable links directly to your Discord profile card (e.g. YouTube, Twitch, GitHub).
- ⚡ **Popular Esports Presets:** Instant presets for *VALORANT, Fortnite, Rocket League, Overwatch 2, Minecraft, Roblox, CS2, GTA V*, and more.
- 🪶 **Zero Resource Consumption:** Runs at **0.0% CPU**, zero battery drain, and zero fan noise.
- 📦 **100% Zero Dependencies:** Uses only pure Python standard library—no `pip install`, no node modules, no external bloat.

---

## 🚀 Quick Start Guide

### Step 1: Requirements
- **Discord Desktop App** must be running on your computer.
- **Python 3.8+** installed ([python.org](https://python.org)).

---

### Step 2: How to Launch (No Coding Needed!)

#### 🍏 On macOS:
1. Double-click **`Launch-GUI.command`** inside the folder (or the shortcut on your Desktop).
2. The control panel will automatically open in your web browser (`http://localhost:5255`).
3. Pick a game preset or drop any custom picture, then click **▶ Update Discord Activity**!

#### 🪟 On Windows:
1. Double-click **`Launch-GUI.bat`**.
2. The control panel will automatically open in your web browser.
3. Pick your game or drop a picture and click **▶ Update Discord Activity**!

---

## 🖼️ How Custom Images Work

You can put **any picture or meme** as your game icon:

1. **Drag & Drop any image** (`.png`, `.jpg`, `.webp`) into the image box on the dashboard (or click it to browse).
2. The app will automatically optimize and link it.
3. Click **▶ Update Discord Activity** — your custom picture will appear on your Discord profile immediately!
4. *Or paste an online link:* You can also paste any image URL directly or click **📋 Paste Link**.

---

## 💻 Terminal / Command Line Mode (Optional)

If you prefer using the terminal:

```bash
# Clone the repository
git clone https://github.com/IsDevCan/discord-custom-activity.git
cd discord-custom-activity

# Launch the visual web dashboard
python3 app.py
```

### Quick Preset One-Liners:

```bash
# Grand Theft Auto VI
python3 activity.py --preset gta6

# Hollow Knight: Silksong
python3 activity.py --preset silksong

# Half-Life 3
python3 activity.py --preset halflife3

# Bloodborne PC Remaster
python3 activity.py --preset bloodborne

# Minecraft 2
python3 activity.py --preset minecraft2

# Touching Grass Simulator
python3 activity.py --preset grass

# Free Discord Nitro Generator
python3 activity.py --preset nitro
```

### Custom Activity:
```bash
python3 activity.py --name "Custom Game" --details "Playing Solo" --state "Level 100"
```

---

## 🛠️ Troubleshooting

- **Activity not showing on Discord?**
  - Make sure the official **Discord Desktop App** is running (not just Discord in a browser tab).
  - Go to Discord **User Settings ⚙️ ➔ Activity Privacy** and ensure **"Display current activity as a status message"** is turned **ON**.
- **Images taking a moment to show?**
  - Discord's servers proxy images globally. When you drop a brand-new image, allow 2-3 seconds for Discord's media proxy to load the image.

---

## 📄 License

MIT License • 100% Free & Open Source • Created with ❤️ by **[IsDevCan](https://github.com/IsDevCan)**
