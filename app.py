#!/usr/bin/env python3
"""
Discord Custom Activity & Rich Presence Manager - Visual Dashboard
Created by IsDevCan
Zero-dependency visual UI with Drag & Drop custom image support and built-in official game logos.
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
      max-width: 680px;
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
      padding: 20px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-bottom: 15px;
      position: relative;
    }
    .drop-zone.dragover {
      border-color: var(--primary);
      background: rgba(88, 101, 242, 0.1);
    }
    .drop-zone-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }
    .drop-icon {
      font-size: 28px;
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
      padding: 16px;
      display: flex;
      gap: 16px;
      align-items: flex-start;
      margin-top: 10px;
    }
    .discord-logo-container {
      position: relative;
      width: 68px;
      height: 68px;
      flex-shrink: 0;
    }
    .discord-game-logo {
      width: 100%;
      height: 100%;
      border-radius: 10px;
      object-fit: cover;
      background: #1e1f22;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid #2b2d31;
    }
    .discord-badge-icon {
      position: absolute;
      bottom: -4px;
      right: -4px;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #2b2d31;
      border: 2px solid #111214;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
    }
    .discord-info h4 {
      font-size: 12px;
      font-weight: 800;
      color: #b5bac1;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 3px;
    }
    .discord-title {
      font-size: 15px;
      font-weight: 700;
      color: #f2f3f5;
      margin-bottom: 2px;
    }
    .discord-details {
      font-size: 13px;
      color: #dbdee1;
      margin-bottom: 2px;
    }
    .discord-state {
      font-size: 13px;
      color: #949ba4;
      margin-bottom: 4px;
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
      <h1>🎮 Discord Custom Activity <span class="badge">Visual UI</span></h1>
      <p class="subtitle">Set custom games, logos, live timers & status on your Discord with zero terminal commands!</p>
    </div>

    <div class="card">
      <div class="card-title">
        <span>Activity Settings</span>
        <div id="statusBadge" class="status-badge">
          <span class="status-dot"></span>
          <span id="statusText">Not Running</span>
        </div>
      </div>

      <!-- Preset Selector -->
      <div class="form-group">
        <label>⚡ Quick Game Preset with Official Logo</label>
        <select id="presetSelect" onchange="applyPreset()">
          <option value="">-- Choose a Game Preset or Custom --</option>
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
        </select>
      </div>

      <!-- Drag and Drop Image Box -->
      <div class="form-group">
        <label>🖼️ Custom Game Logo / Icon (Drop any PNG or Image!)</label>
        <div class="drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
          <input type="file" id="fileInput" accept="image/png, image/jpeg, image/webp, image/gif, image/svg+xml" style="display: none;" onchange="handleFileSelect(event)">
          <div class="drop-zone-content">
            <span class="drop-icon">📁</span>
            <span class="drop-text">Drag & Drop any PNG, JPG, or icon image here</span>
            <span class="drop-subtext">or click to browse from your computer</span>
          </div>
        </div>
        <div class="image-preview-bar" id="previewBar">
          <img id="customThumb" class="image-preview-thumb" src="" alt="Custom Image">
          <span style="font-size: 13px;" id="customFileName">Custom image loaded</span>
          <button class="btn-remove-img" onclick="removeCustomImage()">Remove</button>
        </div>
      </div>

      <div class="form-group">
        <label>Game / Activity Title</label>
        <input type="text" id="gameName" placeholder="e.g. Grand Theft Auto VI, Silksong, Studying...">
      </div>

      <div class="row">
        <div class="form-group">
          <label>Details (Line 1)</label>
          <input type="text" id="gameDetails" placeholder="e.g. Competitive, Heist Mission">
        </div>
        <div class="form-group">
          <label>State (Line 2)</label>
          <input type="text" id="gameState" placeholder="e.g. In Match (13 - 11), Solo Queue">
        </div>
      </div>

      <label class="checkbox-group">
        <input type="checkbox" id="showTimer" checked>
        <span>Show live elapsed timer on Discord</span>
      </label>

      <div class="row">
        <div class="form-group">
          <label>Profile Button Label (Optional)</label>
          <input type="text" id="btn1Text" placeholder="e.g. My Twitch Stream, GitHub">
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
            <span id="fallbackEmoji" style="font-size: 32px;">🎮</span>
          </div>
          <div class="discord-badge-icon">⚡</div>
        </div>
        <div class="discord-info">
          <h4>PLAYING A GAME</h4>
          <div class="discord-title" id="previewTitle">Grand Theft Auto VI</div>
          <div class="discord-details" id="previewDetails">Heist Mission</div>
          <div class="discord-state" id="previewState">5 Stars</div>
          <div class="discord-time" id="previewTime">⏳ 00:24:10 elapsed</div>
        </div>
      </div>
    </div>

    <div class="footer">
      Created by <a href="https://github.com/IsDevCan" target="_blank">IsDevCan</a> • Zero CPU Usage • 100% Free & Open Source
    </div>
  </div>

  <script>
    // Built-in crisp SVG logos for popular games
    const GAME_SVGS = {
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

    function setLogoSvg(key) {
      const slot = document.getElementById("logoSlot");
      if (GAME_SVGS[key]) {
        slot.innerHTML = GAME_SVGS[key];
      } else {
        slot.innerHTML = `<span style="font-size: 32px;">🎮</span>`;
      }
    }

    function setLogoImage(src) {
      const slot = document.getElementById("logoSlot");
      slot.innerHTML = `<img src="${src}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;" alt="Logo">`;
    }

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
        document.getElementById("customFileName").innerText = file.name + " (" + Math.round(file.size / 1024) + " KB)";

        // Upload to server
        fetch("/api/upload_image", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: base64Data, filename: file.name })
        });
      };
      reader.readAsDataURL(file);
    }

    function removeCustomImage() {
      currentCustomImage = null;
      document.getElementById("previewBar").style.display = "none";
      document.getElementById("fileInput").value = "";
      const presetKey = document.getElementById("presetSelect").value;
      if (presetKey && GAME_SVGS[presetKey]) {
        setLogoSvg(presetKey);
      } else {
        document.getElementById("logoSlot").innerHTML = `<span style="font-size: 32px;">🎮</span>`;
      }
    }

    function updatePreview() {
      const name = document.getElementById("gameName").value || "Grand Theft Auto VI";
      const details = document.getElementById("gameDetails").value || "Heist Mission";
      const state = document.getElementById("gameState").value || "5 Stars";
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

    // Initialize default view
    setLogoSvg("gta5");
    updatePreview();
  </script>
</body>
</html>
"""

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
            if "," in img_b64:
                img_b64 = img_b64.split(",", 1)[1]
            try:
                data = base64.b64decode(img_b64)
                with open(CUSTOM_IMG_PATH, "wb") as f:
                    f.write(data)
                self.send_json({"success": True, "url": "/assets/custom_icon.png"})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)})
            return

        elif self.path == "/api/start":
            name = body.get("name", "")
            details = body.get("details", "")
            state = body.get("state", "")
            timer = body.get("timer", True)
            buttons = body.get("buttons", [])
            custom_image = body.get("custom_image")

            # Match client ID or fallback to standard presence
            client_id = "811469787657928704"
            assets = {}
            for k, p in PRESETS.items():
                if p["name"].lower() == name.lower():
                    client_id = p["id"]
                    if p.get("assets"):
                        assets = p["assets"]
                    break

            if CURRENT_IPC:
                try:
                    CURRENT_IPC.close()
                except Exception:
                    pass

            ipc = DiscordIPC(client_id)
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
                self.send_json({"success": False, "error": "Failed to set Discord activity."})

        elif self.path == "/api/stop":
            if CURRENT_IPC:
                try:
                    CURRENT_IPC.clear_activity()
                    CURRENT_IPC.close()
                except Exception:
                    pass
                CURRENT_IPC = None
            CURRENT_CONFIG["status"] = "idle"
            self.send_json({"success": True})

def start_heartbeat():
    global CURRENT_IPC, CURRENT_CONFIG
    while True:
        time.sleep(15)
        if CURRENT_IPC and CURRENT_CONFIG.get("status") == "active":
            try:
                CURRENT_IPC.set_activity(
                    name=CURRENT_CONFIG.get("name"),
                    details=CURRENT_CONFIG.get("details"),
                    state=CURRENT_CONFIG.get("state"),
                    start_timestamp=CURRENT_CONFIG.get("start_time"),
                    buttons=CURRENT_CONFIG.get("buttons")
                )
            except Exception:
                pass

def main():
    port = 5255
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, WebHandler)
    url = f"http://localhost:{port}"

    threading.Thread(target=start_heartbeat, daemon=True).start()

    print("=" * 60)
    print("🎮 DISCORD CUSTOM ACTIVITY MANAGER - VISUAL GUI")
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
