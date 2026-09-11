#!/usr/bin/env python3
"""
Discord Custom Activity & Rich Presence Manager - Visual Dashboard
Created by IsDevCan
Zero-dependency visual UI with Meme/Unreleased game presets, Drag & Drop custom image support, and built-in logos.
"""

import os
import sys
import time
import socket
import struct
import json
import base64
import webbrowser
import threading
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

from activity import DiscordIPC, PRESETS, get_discord_socket

DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(DIR, "assets")
CUSTOM_IMG_PATH = os.path.join(ASSETS_DIR, "custom_icon.png")
os.makedirs(ASSETS_DIR, exist_ok=True)

CURRENT_IPC = None
CURRENT_CONFIG = {
    "status": "idle",
    "name": "",
    "details": "",
    "state": "",
    "timer": True,
    "start_time": None,
    "custom_image": None,
    "preset": "",
    "buttons": []
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Discord Custom Activity Manager - by IsDevCan</title>
  <style>
    :root {
      --bg: #0b0e14;
      --card-bg: #151921;
      --input-bg: #1f2430;
      --border: #2a3142;
      --primary: #5865F2;
      --primary-hover: #4752c4;
      --accent-green: #23a55a;
      --accent-red: #f23f43;
      --accent-gold: #f1c40f;
      --accent-purple: #9b59b6;
      --text: #f2f3f5;
      --text-muted: #949ba4;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body {
      background-color: var(--bg);
      color: var(--text);
      display: flex;
      justify-content: center;
      padding: 30px 15px;
      min-height: 100vh;
    }
    .container {
      width: 100%;
      max-width: 700px;
    }
    .header {
      text-align: center;
      margin-bottom: 25px;
    }
    .header h1 {
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }
    .badge {
      background: var(--primary);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 3px 8px;
      border-radius: 20px;
      font-weight: 700;
      color: white;
    }
    .badge-meme {
      background: linear-gradient(135deg, #ff007f, #7928ca);
      box-shadow: 0 0 10px rgba(255, 0, 127, 0.4);
    }
    .subtitle {
      color: var(--text-muted);
      font-size: 14px;
      margin-top: 6px;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .card-title {
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 20px;
      background: rgba(255,255,255,0.05);
    }
    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #747f8d;
    }
    .status-active .status-dot { background: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }
    .status-active { color: var(--accent-green); font-weight: 600; }
    .form-group {
      margin-bottom: 15px;
    }
    label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 6px;
    }
    input[type="text"], select {
      width: 100%;
      padding: 10px 14px;
      background: var(--input-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }
    input[type="text"]:focus, select:focus {
      border-color: var(--primary);
    }
    optgroup {
      font-weight: 800;
      background: #141720;
      color: #7289da;
    }
    option {
      font-weight: 400;
      background: var(--input-bg);
      color: var(--text);
    }
    .preset-row {
      display: flex;
      gap: 10px;
    }
    .preset-row select {
      flex: 1;
    }
    .btn-dice {
      background: var(--input-bg);
      border: 1px solid var(--border);
      color: var(--accent-gold);
      padding: 0 16px;
      border-radius: 8px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .btn-dice:hover {
      background: rgba(241, 196, 15, 0.15);
      border-color: var(--accent-gold);
    }
    .row {
      display: flex;
      gap: 12px;
    }
    .row .form-group {
      flex: 1;
    }
    /* Drag and Drop Zone */
    .drop-zone {
      border: 2px dashed var(--border);
      background: var(--input-bg);
      border-radius: 10px;
      padding: 18px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-bottom: 15px;
      position: relative;
    }
    .drop-zone.dragover {
      border-color: var(--primary);
      background: rgba(88, 101, 242, 0.12);
    }
    .drop-zone-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }
    .drop-icon {
      font-size: 26px;
    }
    .drop-text {
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
    }
    .drop-subtext {
      font-size: 11px;
      color: var(--text-muted);
    }
    .image-preview-bar {
      display: none;
      align-items: center;
      gap: 12px;
      background: rgba(0,0,0,0.3);
      padding: 8px 12px;
      border-radius: 8px;
      margin-top: 10px;
    }
    .image-preview-thumb {
      width: 42px;
      height: 42px;
      border-radius: 6px;
      object-fit: cover;
      border: 1px solid var(--border);
    }
    .btn-remove-img {
      background: none;
      border: none;
      color: var(--accent-red);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      margin-left: auto;
      padding: 4px 8px;
    }
    .btn-remove-img:hover { text-decoration: underline; }
    .checkbox-group {
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 15px 0;
      cursor: pointer;
      font-size: 13px;
    }
    .checkbox-group input {
      accent-color: var(--primary);
      width: 16px;
      height: 16px;
    }
    .btn-container {
      display: flex;
      gap: 10px;
      margin-top: 10px;
    }
    button.action-btn {
      flex: 1;
      padding: 12px;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: opacity 0.2s, transform 0.1s;
    }
    button.action-btn:active { transform: scale(0.98); }
    .btn-start { background: var(--accent-green); color: white; }
    .btn-stop { background: var(--accent-red); color: white; }
    button.action-btn:hover { opacity: 0.9; }

    /* Live Discord Card Preview */
    .discord-profile-card {
      background: #111214;
      border: 1px solid #232428;
      border-radius: 10px;
      padding: 18px;
      display: flex;
      gap: 16px;
      align-items: flex-start;
      margin-top: 10px;
    }
    .discord-logo-container {
      position: relative;
      width: 72px;
      height: 72px;
      flex-shrink: 0;
    }
    .discord-game-logo {
      width: 100%;
      height: 100%;
      border-radius: 12px;
      object-fit: cover;
      background: #1e1f22;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid #2b2d31;
      overflow: hidden;
    }
    .discord-badge-icon {
      position: absolute;
      bottom: -4px;
      right: -4px;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #2b2d31;
      border: 2px solid #111214;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
    }
    .discord-info h4 {
      font-size: 12px;
      font-weight: 800;
      color: #b5bac1;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .discord-title {
      font-size: 16px;
      font-weight: 700;
      color: #f2f3f5;
      margin-bottom: 3px;
    }
    .discord-details {
      font-size: 13px;
      color: #dbdee1;
      margin-bottom: 3px;
    }
    .discord-state {
      font-size: 13px;
      color: #949ba4;
      margin-bottom: 5px;
    }
    .discord-time {
      font-size: 12px;
      color: #949ba4;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .footer {
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 25px;
    }
    .footer a { color: var(--primary); text-decoration: none; font-weight: 600; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎮 Discord Custom Activity <span class="badge badge-meme">Meme Edition</span></h1>
      <p class="subtitle">Flex unreleased games like GTA 6, Silksong, Half-Life 3, or drop any custom meme image on your Discord!</p>
    </div>

    <div class="card">
      <div class="card-title">
        <span>Activity Controls</span>
        <div id="statusBadge" class="status-badge">
          <span class="status-dot"></span>
          <span id="statusText">Not Running</span>
        </div>
      </div>

      <!-- Presets & Random Meme Dice -->
      <div class="form-group">
        <label>⚡ Game Preset / Troll Games</label>
        <div class="preset-row">
          <select id="presetSelect" onchange="applyPreset()">
            <option value="">-- Pick a Game or Custom --</option>
            <optgroup label="🔥 TROLL & UNRELEASED GAMES (MEME VAULT)">
              <option value="gta6">Grand Theft Auto VI (Early Dev Build)</option>
              <option value="silksong">Hollow Knight: Silksong</option>
              <option value="halflife3">Half-Life 3 (Valve Beta)</option>
              <option value="bloodborne_pc">Bloodborne PC Remaster</option>
              <option value="portal3">Portal 3</option>
              <option value="tes6">The Elder Scrolls VI: Hammerfell</option>
              <option value="titanfall3">Titanfall 3</option>
              <option value="minecraft2">Minecraft 2 (Unreal Engine 5)</option>
              <option value="chess2">Chess 2: Battle Royale</option>
              <option value="touching_grass">Touching Grass Simulator 2026</option>
              <option value="nitro_generator">Free Discord Nitro Generator 3D</option>
              <option value="skate4">Skate 4</option>
            </optgroup>
            <optgroup label="🎮 POPULAR ESPORTS & GAMES">
              <option value="valorant">VALORANT</option>
              <option value="fortnite">Fortnite</option>
              <option value="minecraft">Minecraft</option>
              <option value="roblox">Roblox</option>
              <option value="gta5">Grand Theft Auto V</option>
              <option value="cs2">Counter-Strike 2</option>
              <option value="rocket_league">Rocket League</option>
              <option value="apex">Apex Legends</option>
              <option value="overwatch">Overwatch 2</option>
              <option value="r6">Rainbow Six Siege</option>
              <option value="elden_ring">Elden Ring</option>
              <option value="lol">League of Legends</option>
            </optgroup>
          </select>
          <button class="btn-dice" onclick="pickRandomMeme()" title="Pick a random troll game!">🎲 Random Troll</button>
        </div>
      </div>

      <!-- Drag and Drop Image Box -->
      <div class="form-group">
        <label>🖼️ Custom Game Logo / Icon (Drop any PNG, Meme or Picture!)</label>
        <div class="drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
          <input type="file" id="fileInput" accept="image/png, image/jpeg, image/webp, image/gif, image/svg+xml" style="display: none;" onchange="handleFileSelect(event)">
          <div class="drop-zone-content">
            <span class="drop-icon">📁</span>
            <span class="drop-text">Drag & Drop any PNG, JPG, or Meme image here</span>
            <span class="drop-subtext">or click to browse from your computer</span>
          </div>
        </div>
        <div class="image-preview-bar" id="previewBar">
          <img id="customThumb" class="image-preview-thumb" src="" alt="Custom Image">
          <span style="font-size: 13px;" id="customFileName">Custom image loaded</span>
          <button class="btn-remove-img" onclick="removeCustomImage()">Remove</button>
        </div>
        <div id="localImageNotice" style="display: none; margin-top: 8px; padding: 10px 14px; background: rgba(88, 101, 242, 0.12); border: 1px solid rgba(88, 101, 242, 0.35); border-radius: 8px; font-size: 13px; line-height: 1.4; color: #dbdee1;">
          <strong>💡 Loaded in local preview!</strong> To display on your Discord profile, Discord requires a web link.<br>
          <span style="color: #949ba4;">👉 <strong>Fastest trick (5 sec):</strong> Drop this image into any Discord chat/DM ➔ Right-click ➔ <strong>Copy Link</strong> ➔ click <strong>📋 Paste Link</strong> below!</span>
        </div>
        <div style="display: flex; gap: 8px; margin-top: 8px;">
          <input type="text" id="imageUrl" placeholder="🔗 Paste Image URL (e.g. from Discord, Imgur, Tenor, Web: https://...)" oninput="handleImageUrlInput()" style="flex: 1;">
          <button type="button" class="btn-dice" style="padding: 0 14px; white-space: nowrap;" onclick="pasteClipboardUrl()" title="Paste image link from clipboard">📋 Paste Link</button>
        </div>
      </div>

      <div class="form-group">
        <label>Game / Activity Title</label>
        <input type="text" id="gameName" placeholder="e.g. Grand Theft Auto VI, Silksong, Studying...">
      </div>

      <div class="row">
        <div class="form-group">
          <label>Details (Line 1)</label>
          <input type="text" id="gameDetails" placeholder="e.g. Playing Early Access Dev Build">
        </div>
        <div class="form-group">
          <label>State (Line 2)</label>
          <input type="text" id="gameState" placeholder="e.g. Vice City Heist (Mission 42)">
        </div>
      </div>

      <label class="checkbox-group">
        <input type="checkbox" id="showTimer" checked>
        <span>Show live elapsed timer on Discord profile</span>
      </label>

      <div class="row">
        <div class="form-group">
          <label>Clickable Button Label (Optional)</label>
          <input type="text" id="btn1Text" placeholder="e.g. Download Leak, My Twitch">
        </div>
        <div class="form-group">
          <label>Button Link URL</label>
          <input type="text" id="btn1Url" placeholder="https://...">
        </div>
      </div>

      <div class="btn-container">
        <button class="action-btn btn-start" onclick="startActivity()">▶ Start Activity on Discord</button>
        <button class="action-btn btn-stop" onclick="stopActivity()">⏹ Stop Activity</button>
      </div>
    </div>

    <!-- Live Discord Card Preview -->
    <div class="card">
      <div class="card-title">Live Discord Profile Preview</div>
      <div class="discord-profile-card">
        <div class="discord-logo-container">
          <div id="logoSlot" class="discord-game-logo">
            <span id="fallbackEmoji" style="font-size: 36px;">🎮</span>
          </div>
          <div class="discord-badge-icon">⚡</div>
        </div>
        <div class="discord-info">
          <h4>PLAYING A GAME</h4>
          <div class="discord-title" id="previewTitle">Grand Theft Auto VI</div>
          <div class="discord-details" id="previewDetails">Playing Early Access Dev Build</div>
          <div class="discord-state" id="previewState">Vice City Heist (Mission 42)</div>
          <div class="discord-time" id="previewTime">⏳ 01:42:15 elapsed</div>
        </div>
      </div>
    </div>

    <div class="footer">
      Created by <a href="https://github.com/IsDevCan" target="_blank">IsDevCan</a> • Zero CPU Usage • 100% Free & Open Source
    </div>
  </div>

  <script>
    // Crisp SVG logos including custom Meme & Unreleased Games
    const GAME_SVGS = {
      // --- TROLL & UNRELEASED ---
      gta6: `<svg viewBox="0 0 100 100" width="100%" height="100%"><defs><linearGradient id="gta6grad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ff2a8d"/><stop offset="50%" stop-color="#9a00ff"/><stop offset="100%" stop-color="#00f0ff"/></linearGradient></defs><rect width="100" height="100" rx="12" fill="#090514"/><path d="M15 75 C 20 60, 30 50, 45 45 C 35 48, 25 55, 18 68 Z" fill="#ff2a8d" opacity="0.6"/><path d="M85 75 C 80 60, 70 50, 55 45 C 65 48, 75 55, 82 68 Z" fill="#00f0ff" opacity="0.6"/><text x="50" y="66" font-size="44" font-weight="900" fill="url(#gta6grad)" text-anchor="middle" font-family="Arial Black, Impact" letter-spacing="-2">VI</text><text x="50" y="85" font-size="8" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black" letter-spacing="1">VICE CITY</text></svg>`,
      silksong: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#140204"/><polygon points="50,10 56,50 50,90 44,50" fill="#ffffff"/><circle cx="50" cy="50" r="14" fill="#a71920"/><circle cx="47" cy="48" r="3" fill="#ffffff"/><circle cx="53" cy="48" r="3" fill="#ffffff"/><polygon points="50,2 53,20 47,20" fill="#d9d9d9"/><text x="50" y="94" font-size="7" font-weight="800" fill="#e54b4b" text-anchor="middle" font-family="Georgia">SILKSONG</text></svg>`,
      halflife3: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#1b1c20"/><circle cx="50" cy="50" r="40" stroke="#f68b1f" stroke-width="7" fill="none"/><text x="44" y="68" font-size="48" font-weight="900" fill="#f68b1f" text-anchor="middle" font-family="Georgia, serif">λ</text><text x="70" y="44" font-size="28" font-weight="900" fill="#f68b1f" text-anchor="middle" font-family="Impact">3</text></svg>`,
      bloodborne_pc: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#08080a"/><line x1="50" y1="15" x2="50" y2="85" stroke="#c0232b" stroke-width="6"/><line x1="30" y1="35" x2="70" y2="35" stroke="#c0232b" stroke-width="5"/><line x1="35" y1="65" x2="65" y2="65" stroke="#c0232b" stroke-width="5"/><path d="M30 35 Q 50 65 70 35" stroke="#c0232b" stroke-width="5" fill="none"/><text x="50" y="94" font-size="7" font-weight="800" fill="#ffffff" text-anchor="middle" font-family="Georgia">PC EDITION</text></svg>`,
      portal3: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#181818"/><ellipse cx="38" cy="50" rx="16" ry="32" fill="none" stroke="#00a2ff" stroke-width="6"/><ellipse cx="62" cy="50" rx="16" ry="32" fill="none" stroke="#ff7700" stroke-width="6"/><text x="50" y="60" font-size="30" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Impact">3</text></svg>`,
      tes6: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#101014"/><polygon points="50,15 65,40 50,55 35,40" fill="none" stroke="#d4af37" stroke-width="4"/><polygon points="50,55 60,80 50,72 40,80" fill="none" stroke="#d4af37" stroke-width="4"/><text x="50" y="70" font-size="34" font-weight="900" fill="#d4af37" text-anchor="middle" font-family="Cinzel, Georgia">VI</text></svg>`,
      titanfall3: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#1c2024"/><polygon points="25,25 75,25 85,75 50,90 15,75" fill="#2d333b"/><polygon points="30,42 70,42 65,58 35,58" fill="#00d0ff"/><text x="50" y="80" font-size="20" font-weight="900" fill="#ff6b00" text-anchor="middle" font-family="Impact">/// 3</text></svg>`,
      minecraft2: `<svg viewBox="0 0 100 100" width="100%" height="100%"><defs><linearGradient id="mc2g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#00ffff"/><stop offset="100%" stop-color="#0066ff"/></linearGradient></defs><rect width="100" height="100" rx="12" fill="#0b1329"/><circle cx="50" cy="50" r="38" fill="url(#mc2g)"/><text x="50" y="60" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Impact">MC 2</text><text x="50" y="76" font-size="7" font-weight="900" fill="#ffe600" text-anchor="middle">UNREAL ENGINE 5</text></svg>`,
      chess2: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#1c1917"/><polygon points="20,75 80,75 75,40 60,55 50,25 40,55 25,40" fill="#eab308"/><circle cx="35" cy="48" r="3" fill="#ff0000"/><circle cx="65" cy="48" r="3" fill="#ff0000"/><text x="50" y="90" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black">CHESS II</text></svg>`,
      touching_grass: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#052e16"/><circle cx="80" cy="25" r="16" fill="#facc15"/><path d="M20 90 Q 25 35 45 40 Q 35 60 30 90" fill="#22c55e"/><path d="M40 90 Q 50 20 70 30 Q 55 55 50 90" fill="#4ade80"/><path d="M60 90 Q 70 35 85 45 Q 75 65 70 90" fill="#16a34a"/><text x="50" y="93" font-size="8" font-weight="800" fill="#ffffff" text-anchor="middle">TOUCH GRASS</text></svg>`,
      nitro_generator: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#5865F2"/><text x="50" y="52" font-size="38" font-weight="900" fill="#ffffff" text-anchor="middle">$</text><text x="50" y="78" font-size="14" font-weight="900" fill="#f1c40f" text-anchor="middle">FREE NITRO</text></svg>`,
      skate4: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="12" fill="#e5e5e5"/><rect x="15" y="42" width="70" height="16" rx="8" fill="#111111"/><circle cx="28" cy="62" r="7" fill="#ea580c"/><circle cx="72" cy="62" r="7" fill="#ea580c"/><text x="50" y="34" font-size="18" font-weight="900" fill="#111111" text-anchor="middle" font-family="Arial Black">skate.</text></svg>`,

      // --- POPULAR ESPORTS ---
      valorant: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#0f1923"/><polygon points="20,25 45,25 35,75 10,75" fill="#ff4655"/><polygon points="55,25 90,25 80,45 65,45" fill="#ff4655"/><polygon points="62,55 77,55 69,75 54,75" fill="#ff4655"/></svg>`,
      minecraft: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#583822"/><rect width="100" height="40" fill="#528e35" rx="10"/><rect y="25" width="100" height="20" fill="#528e35"/><rect x="15" y="40" width="15" height="15" fill="#528e35"/><rect x="45" y="40" width="15" height="20" fill="#528e35"/><rect x="75" y="40" width="15" height="15" fill="#528e35"/></svg>`,
      fortnite: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#1b1c28"/><path d="M35 15 L75 15 L70 32 L52 32 L49 45 L68 45 L64 62 L45 62 L39 88 L20 88 Z" fill="#ffffff"/></svg>`,
      roblox: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#000000"/><g transform="rotate(-15 50 50)"><rect x="25" y="25" width="50" height="50" fill="#ffffff"/><rect x="40" y="40" width="20" height="20" fill="#000000"/></g></svg>`,
      gta5: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#0a0a0a"/><polygon points="20,20 40,20 50,70 60,20 80,20 62,85 38,85" fill="#439b4b"/><text x="50" y="94" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Arial Black">GTA V</text></svg>`,
      cs2: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#1b2838"/><text x="50" y="65" font-size="34" font-weight="900" fill="#de9b35" text-anchor="middle" font-family="Impact">CS2</text></svg>`,
      rocket_league: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#0077dd"/><polygon points="50,15 85,30 75,80 50,92 25,80 15,30" fill="#ffffff"/><text x="50" y="62" font-size="22" font-weight="900" fill="#0077dd" text-anchor="middle" font-family="Arial Black">RL</text></svg>`,
      apex: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#da292a"/><polygon points="50,15 85,85 70,85 50,45 30,85 15,85" fill="#ffffff"/><line x1="32" y1="65" x2="68" y2="65" stroke="#da292a" stroke-width="8"/></svg>`,
      overwatch: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#212529"/><circle cx="50" cy="50" r="38" stroke="#f06414" stroke-width="8" fill="none"/><path d="M30 35 L42 58 L50 42 L58 58 L70 35" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round"/></svg>`,
      r6: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#1e2328"/><text x="50" y="70" font-size="55" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="Impact">6</text></svg>`,
      elden_ring: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#111111"/><circle cx="50" cy="40" r="22" stroke="#d4af37" stroke-width="4" fill="none"/><circle cx="40" cy="55" r="22" stroke="#d4af37" stroke-width="4" fill="none"/><circle cx="60" cy="55" r="22" stroke="#d4af37" stroke-width="4" fill="none"/><line x1="50" y1="12" x2="50" y2="88" stroke="#d4af37" stroke-width="4"/></svg>`,
      lol: `<svg viewBox="0 0 100 100" width="100%" height="100%"><rect width="100" height="100" rx="10" fill="#091428"/><text x="50" y="65" font-size="34" font-weight="900" fill="#c89b3c" text-anchor="middle" font-family="Cinzel, Georgia">LoL</text></svg>`
    };

    const presets = {
      // Meme / Unreleased
      gta6: { name: "Grand Theft Auto VI", details: "Playing Early Access Dev Build", state: "Vice City Heist (Mission 42)" },
      silksong: { name: "Hollow Knight: Silksong", details: "Pharloom Citadel (100% Run)", state: "Waiting Since 2019" },
      halflife3: { name: "Half-Life 3", details: "Valve Internal Beta v0.9", state: "Chapter 7: Return to Borealis" },
      bloodborne_pc: { name: "Bloodborne PC Remaster", details: "4K 120FPS (Finally on PC)", state: "Father Gascoigne (Attempt 1)" },
      portal3: { name: "Portal 3", details: "Aperture Science Testing", state: "Chamber 47 - Still No Cake" },
      tes6: { name: "The Elder Scrolls VI: Hammerfell", details: "Bethesda Early Playtest", state: "Exploring High Rock" },
      titanfall3: { name: "Titanfall 3", details: "Multiplayer Pilot Match", state: "Taking Normal Pills (Delusion Level 100)" },
      minecraft2: { name: "Minecraft 2 (Unreal Engine 5)", details: "Spherical World Mode", state: "Herobrine Encounter" },
      chess2: { name: "Chess 2: Battle Royale", details: "Ranked 100-Player Gulag", state: "Pawns Got Nerfed" },
      touching_grass: { name: "Touching Grass Simulator 2026", details: "Tutorial: Leaving My Room", state: "Sunlight Burning My Eyes" },
      nitro_generator: { name: "Free Discord Nitro Generator 3D", details: "Mining Free Nitro Coins", state: "100% Legit No Virus" },
      skate4: { name: "Skate 4", details: "Closed Developer Playtest", state: "Doing 900 Kickflips at San Van" },

      // Popular
      valorant: { name: "VALORANT", details: "Competitive", state: "In Match (13 - 11)" },
      fortnite: { name: "Fortnite", details: "Battle Royale", state: "Victory Royale! #1/100" },
      minecraft: { name: "Minecraft", details: "Survival Mode", state: "Exploring Nether" },
      roblox: { name: "Roblox", details: "Blox Fruits", state: "Grinding Bosses" },
      gta5: { name: "Grand Theft Auto V", details: "GTA Online", state: "Cayo Perico Heist" },
      cs2: { name: "Counter-Strike 2", details: "Premier Match", state: "Score: 11 - 9" },
      rocket_league: { name: "Rocket League", details: "Competitive 3v3", state: "In Overtime (3 - 3)" },
      apex: { name: "Apex Legends", details: "Ranked Leagues", state: "Top 3 Squads" },
      overwatch: { name: "Overwatch 2", details: "Competitive", state: "Push - Final Point" },
      r6: { name: "Rainbow Six Siege", details: "Ranked Bomb", state: "Match Point (4 - 4)" },
      elden_ring: { name: "Elden Ring", details: "The Lands Between", state: "Altus Plateau" },
      lol: { name: "League of Legends", details: "Ranked Solo", state: "Mid Lane (5/0/2)" }
    };

    const MEME_KEYS = ["gta6", "silksong", "halflife3", "bloodborne_pc", "portal3", "tes6", "titanfall3", "minecraft2", "chess2", "touching_grass", "nitro_generator", "skate4"];

    let currentCustomImage = null;

    function applyPreset() {
      const key = document.getElementById("presetSelect").value;
      if (presets[key]) {
        document.getElementById("gameName").value = presets[key].name;
        document.getElementById("gameDetails").value = presets[key].details;
        document.getElementById("gameState").value = presets[key].state;
        if (!currentCustomImage) {
          setLogoSvg(key);
        }
        updatePreview();
      }
    }

    function pickRandomMeme() {
      const randKey = MEME_KEYS[Math.floor(Math.random() * MEME_KEYS.length)];
      document.getElementById("presetSelect").value = randKey;
      applyPreset();
    }

    function setLogoSvg(key) {
      const slot = document.getElementById("logoSlot");
      if (GAME_SVGS[key]) {
        slot.innerHTML = GAME_SVGS[key];
      } else {
        slot.innerHTML = `<span style="font-size: 36px;">🎮</span>`;
      }
    }

    function setLogoImage(src) {
      const slot = document.getElementById("logoSlot");
      slot.innerHTML = `<img src="${src}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 12px;" alt="Logo">`;
    }

    // Prevent browser from opening files dragged onto window
    window.addEventListener("dragover", (e) => e.preventDefault(), false);
    window.addEventListener("drop", (e) => e.preventDefault(), false);

    // Drag & Drop Handling
    const dropZone = document.getElementById("dropZone");

    ["dragenter", "dragover"].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
      });
    });

    ["dragleave", "drop"].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
      });
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");

      // Check if an image URL was dragged (e.g. directly from Discord or browser)
      const droppedUrl = e.dataTransfer.getData("text/uri-list") || e.dataTransfer.getData("URL") || e.dataTransfer.getData("text/plain");
      if (droppedUrl && (droppedUrl.startsWith("http://") || droppedUrl.startsWith("https://"))) {
        document.getElementById("imageUrl").value = droppedUrl.trim();
        handleImageUrlInput();
        return;
      }

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        processImageFile(files[0]);
      }
    });

    function handleFileSelect(e) {
      if (e.target.files.length > 0) {
        processImageFile(e.target.files[0]);
      }
    }

    function handleImageUrlInput() {
      const url = document.getElementById("imageUrl").value.trim();
      if (url && (url.startsWith("http://") || url.startsWith("https://"))) {
        currentCustomImage = url;
        setLogoImage(url);
        document.getElementById("previewBar").style.display = "flex";
        document.getElementById("customThumb").src = url;
        document.getElementById("customFileName").innerText = "Image URL Linked";
        const notice = document.getElementById("localImageNotice");
        if (notice) notice.style.display = "none";
      }
    }

    async function pasteClipboardUrl() {
      try {
        const text = await navigator.clipboard.readText();
        if (text && (text.startsWith("http://") || text.startsWith("https://"))) {
          document.getElementById("imageUrl").value = text.trim();
          handleImageUrlInput();
        } else {
          alert("Please copy a valid image link first (starting with https://)!");
        }
      } catch (err) {
        const manual = prompt("Paste your Image URL (https://...):");
        if (manual && (manual.startsWith("http://") || manual.startsWith("https://"))) {
          document.getElementById("imageUrl").value = manual.trim();
          handleImageUrlInput();
        }
      }
    }

    function processImageFile(file) {
      if (!file.type.startsWith("image/")) {
        alert("Please drop a valid image file (PNG, JPG, SVG, WebP)!");
        return;
      }
      const reader = new FileReader();
      reader.onload = function(evt) {
        const base64Data = evt.target.result;
        currentCustomImage = base64Data;
        setLogoImage(base64Data);

        // Show thumbnail bar
        document.getElementById("previewBar").style.display = "flex";
        document.getElementById("customThumb").src = base64Data;
        document.getElementById("customFileName").innerText = "⏳ Uploading " + file.name + "...";

        // Upload to server and get instant Discord-ready public URL
        fetch("/api/upload_image", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: base64Data, filename: file.name })
        })
        .then(res => res.json())
        .then(data => {
          if (data.success && data.url) {
            currentCustomImage = data.url;
            document.getElementById("imageUrl").value = data.url;
            document.getElementById("customFileName").innerText = "✅ " + file.name + " (Ready for Discord!)";
            const notice = document.getElementById("localImageNotice");
            if (notice) notice.style.display = "none";
          } else {
            document.getElementById("customFileName").innerText = "✅ " + file.name + " (" + Math.round(file.size / 1024) + " KB)";
          }
        })
        .catch(() => {
          document.getElementById("customFileName").innerText = "✅ " + file.name + " (" + Math.round(file.size / 1024) + " KB)";
        });
      };
      reader.readAsDataURL(file);
    }

    function removeCustomImage() {
      currentCustomImage = null;
      document.getElementById("previewBar").style.display = "none";
      document.getElementById("fileInput").value = "";
      document.getElementById("imageUrl").value = "";
      const notice = document.getElementById("localImageNotice");
      if (notice) notice.style.display = "none";
      const presetKey = document.getElementById("presetSelect").value;
      if (presetKey && GAME_SVGS[presetKey]) {
        setLogoSvg(presetKey);
      } else {
        document.getElementById("logoSlot").innerHTML = `<span style="font-size: 36px;">🎮</span>`;
      }
    }

    function updatePreview() {
      const name = document.getElementById("gameName").value || "Grand Theft Auto VI";
      const details = document.getElementById("gameDetails").value || "Playing Early Access Dev Build";
      const state = document.getElementById("gameState").value || "Vice City Heist (Mission 42)";
      document.getElementById("previewTitle").innerText = name;
      document.getElementById("previewDetails").innerText = details;
      document.getElementById("previewState").innerText = state;
    }

    document.getElementById("gameName").addEventListener("input", updatePreview);
    document.getElementById("gameDetails").addEventListener("input", updatePreview);
    document.getElementById("gameState").addEventListener("input", updatePreview);

    async function startActivity() {
      const name = document.getElementById("gameName").value.trim();
      const details = document.getElementById("gameDetails").value.trim();
      const state = document.getElementById("gameState").value.trim();
      const timer = document.getElementById("showTimer").checked;
      const btn1Text = document.getElementById("btn1Text").value.trim();
      const btn1Url = document.getElementById("btn1Url").value.trim();

      if (!name) {
        alert("Please enter a Game or Activity title!");
        return;
      }

      const buttons = [];
      if (btn1Text && btn1Url) {
        buttons.push({ label: btn1Text, url: btn1Url });
      }

      try {
        const res = await fetch("/api/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name, details, state, timer, buttons,
            custom_image: currentCustomImage
          })
        });
        const data = await res.json();
        if (data.success) {
          document.getElementById("statusBadge").className = "status-badge status-active";
          document.getElementById("statusText").innerText = "Active on Discord (" + name + ")";
        } else {
          alert("Could not connect to Discord: " + (data.error || "Make sure Discord desktop app is running!"));
        }
      } catch (err) {
        alert("Error connecting to local server: " + err);
      }
    }

    async function stopActivity() {
      try {
        await fetch("/api/stop", { method: "POST" });
        document.getElementById("statusBadge").className = "status-badge";
        document.getElementById("statusText").innerText = "Stopped";
      } catch (err) {
        console.error(err);
      }
    }

    // Default to GTA 6 on first load!
    document.getElementById("presetSelect").value = "gta6";
    applyPreset();
  </script>
</body>
</html>
"""

SOCKET_LOCK = threading.Lock()

class WebHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            body = HTML_TEMPLATE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/status":
            self.send_json(CURRENT_CONFIG)
        elif self.path == "/assets/custom_icon.png":
            if os.path.exists(CUSTOM_IMG_PATH):
                with open(CUSTOM_IMG_PATH, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global CURRENT_IPC, CURRENT_CONFIG
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len)
        try:
            body = json.loads(post_data.decode("utf-8"))
        except Exception:
            body = {}

        if self.path == "/api/upload_image":
            img_b64 = body.get("image", "")
            filename = body.get("filename", "custom.png")
            ext = os.path.splitext(filename)[1].lower()
            if ext not in [".png", ".jpg", ".jpeg", ".webp", ".gif"]:
                ext = ".png"
            if "," in img_b64:
                img_b64 = img_b64.split(",", 1)[1]
            try:
                data = base64.b64decode(img_b64)
                unique_name = f"user_img_{int(time.time())}{ext}"
                target_path = os.path.join(ASSETS_DIR, unique_name)
                with open(target_path, "wb") as f:
                    f.write(data)
                
                # Auto push to repo to get public Discord-accessible link
                subprocess.run(["git", "add", target_path], cwd=DIR, check=True)
                subprocess.run([
                    "git", "commit", "-m", f"Auto-publish custom image {unique_name}",
                    "--author=IsDevCan <191389591+IsDevCan@users.noreply.github.com>"
                ], cwd=DIR, check=True)
                subprocess.run(["git", "push", "origin", "main"], cwd=DIR, timeout=8, check=True)
                
                public_url = f"https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/{unique_name}"
                self.send_json({"success": True, "url": public_url})
            except Exception as e:
                # Fallback to user_custom.png
                public_url = "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/user_custom.png"
                self.send_json({"success": True, "url": public_url})
            return

        elif self.path == "/api/start":
            name = body.get("name", "")
            details = body.get("details", "")
            state = body.get("state", "")
            timer = body.get("timer", True)
            buttons = body.get("buttons", [])
            custom_image = body.get("custom_image")

            # Auto-handle base64 or local custom images
            if custom_image and isinstance(custom_image, str) and custom_image.startswith("data:image"):
                try:
                    img_b64 = custom_image.split(",", 1)[1] if "," in custom_image else custom_image
                    data = base64.b64decode(img_b64)
                    unique_name = f"user_img_{int(time.time())}.png"
                    target_path = os.path.join(ASSETS_DIR, unique_name)
                    with open(target_path, "wb") as f:
                        f.write(data)
                    subprocess.run(["git", "add", target_path], cwd=DIR, check=True)
                    subprocess.run([
                        "git", "commit", "-m", f"Auto-publish custom image {unique_name}",
                        "--author=IsDevCan <191389591+IsDevCan@users.noreply.github.com>"
                    ], cwd=DIR, check=True)
                    subprocess.run(["git", "push", "origin", "main"], cwd=DIR, timeout=8, check=True)
                    custom_image = f"https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/{unique_name}"
                except Exception:
                    custom_image = "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/user_custom.png"
            elif custom_image and isinstance(custom_image, str) and (custom_image.startswith("/assets/") or custom_image == "custom"):
                custom_image = "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/user_custom.png"

            client_id = "811469787657928704"
            # Match registered preset ID if available
            for k, p in PRESETS.items():
                if p.get("name", "").lower() == name.lower():
                    client_id = p["id"]
                    break

            # Build assets dictionary
            assets = {}
            if custom_image and isinstance(custom_image, str) and (custom_image.startswith("http://") or custom_image.startswith("https://")):
                assets = {"large_image": custom_image, "large_text": name}
            else:
                for k, p in PRESETS.items():
                    if p.get("name", "").lower() == name.lower():
                        if p.get("assets"):
                            assets = p["assets"]
                        break

            with SOCKET_LOCK:
                # 1. Reuse existing open socket if alive
                if CURRENT_IPC and CURRENT_IPC.sock:
                    start_time = int(time.time()) if timer else None
                    ok = CURRENT_IPC.set_activity(
                        name=name,
                        details=details,
                        state=state,
                        start_timestamp=start_time,
                        assets=assets if assets else None,
                        buttons=buttons if buttons else None
                    )
                    if ok:
                        CURRENT_CONFIG = {
                            "status": "active",
                            "name": name,
                            "details": details,
                            "state": state,
                            "timer": timer,
                            "start_time": start_time,
                            "custom_image": custom_image,
                            "buttons": buttons
                        }
                        self.send_json({"success": True})
                        return

                # 2. If no open socket or update failed, clean and reconnect
                if CURRENT_IPC:
                    try:
                        CURRENT_IPC.close()
                    except Exception:
                        pass
                    CURRENT_IPC = None
                    time.sleep(1.2)

                ipc = DiscordIPC(client_id)
                ok, msg = ipc.connect()
                if not ok:
                    time.sleep(1.2)
                    ok, msg = ipc.connect()
                    if not ok:
                        self.send_json({"success": False, "error": msg})
                        return

                start_time = int(time.time()) if timer else None
                ok = ipc.set_activity(
                    name=name,
                    details=details,
                    state=state,
                    start_timestamp=start_time,
                    assets=assets if assets else None,
                    buttons=buttons if buttons else None
                )

                if ok:
                    CURRENT_IPC = ipc
                    CURRENT_CONFIG = {
                        "status": "active",
                        "name": name,
                        "details": details,
                        "state": state,
                        "timer": timer,
                        "start_time": start_time,
                        "custom_image": custom_image,
                        "buttons": buttons
                    }
                    self.send_json({"success": True})
                else:
                    self.send_json({"success": False, "error": "Discord rejected activity payload."})

        elif self.path == "/api/stop":
            with SOCKET_LOCK:
                if CURRENT_IPC:
                    try:
                        CURRENT_IPC.clear_activity()
                    except Exception:
                        pass
                CURRENT_CONFIG["status"] = "idle"
                self.send_json({"success": True})

def main():
    port = 5255
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, WebHandler)
    url = f"http://localhost:{port}"

    print("=" * 60)
    print("🎮 DISCORD CUSTOM ACTIVITY MANAGER - MEME & TROLL EDITION")
    print(f"🚀 Opening dashboard in your browser: {url}")
    print("✨ Leave this open while using the app. Press Ctrl+C to exit.")
    print("=" * 60)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    main()
