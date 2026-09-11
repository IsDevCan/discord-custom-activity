#!/usr/bin/env python3
"""
Discord Custom Activity - Visual Web Dashboard
Created by IsDevCan
Provides a 100% zero-dependency visual interface to control Discord Rich Presence with zero terminal knowledge.
"""

import os
import sys
import time
import socket
import struct
import json
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import IPC and Presets from activity.py
from activity import DiscordIPC, PRESETS, get_discord_socket

CURRENT_IPC = None
CURRENT_CONFIG = {
    "status": "idle",
    "name": "",
    "details": "",
    "state": "",
    "timer": True,
    "start_time": None,
    "preset": "",
    "buttons": []
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Discord Custom Activity Manager</title>
  <style>
    :root {
      --bg: #0f1117;
      --card-bg: #181b24;
      --input-bg: #222634;
      --border: #2d3345;
      --primary: #5865F2;
      --primary-hover: #4752c4;
      --accent-green: #23a55a;
      --accent-red: #f23f43;
      --text: #f2f3f5;
      --text-muted: #949ba4;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
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
      max-width: 650px;
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
      box-shadow: 0 8px 24px rgba(0,0,0,0.25);
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
    button {
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
    button:active { transform: scale(0.98); }
    .btn-start {
      background: var(--accent-green);
      color: white;
    }
    .btn-stop {
      background: var(--accent-red);
      color: white;
    }
    .btn-discord {
      background: var(--primary);
      color: white;
    }
    button:hover { opacity: 0.9; }
    .preview-card {
      background: #111214;
      border: 1px solid #232428;
      border-radius: 8px;
      padding: 16px;
      display: flex;
      gap: 14px;
      align-items: center;
      margin-top: 15px;
    }
    .preview-icon {
      width: 50px;
      height: 50px;
      background: var(--input-bg);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }
    .preview-details h4 {
      font-size: 14px;
      font-weight: 700;
      color: var(--text);
    }
    .preview-details p {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 2px;
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
      <h1>🎮 Discord Activity Manager <span class="badge">Visual UI</span></h1>
      <p class="subtitle">Set custom games, details, state & buttons on your Discord profile with zero terminal commands!</p>
    </div>

    <div class="card">
      <div class="card-title">
        <span>Activity Controls</span>
        <div id="statusBadge" class="status-badge">
          <span class="status-dot"></span>
          <span id="statusText">Not Running</span>
        </div>
      </div>

      <div class="form-group">
        <label>⚡ Quick Game Preset</label>
        <select id="presetSelect" onchange="applyPreset()">
          <option value="">-- Or Choose a Preset --</option>
          <option value="1">VALORANT</option>
          <option value="2">Fortnite</option>
          <option value="3">Rocket League</option>
          <option value="4">Overwatch 2</option>
          <option value="5">Rainbow Six Siege</option>
          <option value="6">Grand Theft Auto V</option>
          <option value="7">Minecraft</option>
          <option value="8">Roblox</option>
          <option value="9">Counter-Strike 2</option>
          <option value="10">League of Legends</option>
          <option value="11">Apex Legends</option>
          <option value="12">Genshin Impact</option>
        </select>
      </div>

      <div class="form-group">
        <label>Game / Activity Title</label>
        <input type="text" id="gameName" placeholder="e.g. Grand Theft Auto VI, Studying for Exams, Coding...">
      </div>

      <div class="row">
        <div class="form-group">
          <label>Details (Line 1)</label>
          <input type="text" id="gameDetails" placeholder="e.g. In Match, Exploring Vice City">
        </div>
        <div class="form-group">
          <label>State (Line 2)</label>
          <input type="text" id="gameState" placeholder="e.g. Solo Queue, 5 Stars">
        </div>
      </div>

      <label class="checkbox-group">
        <input type="checkbox" id="showTimer" checked>
        <span>Show elapsed time counter on profile</span>
      </label>

      <div class="row">
        <div class="form-group">
          <label>Clickable Button 1 (Optional)</label>
          <input type="text" id="btn1Text" placeholder="Button Label (e.g. My Twitch)">
        </div>
        <div class="form-group">
          <label>Button 1 Link URL</label>
          <input type="text" id="btn1Url" placeholder="https://twitch.tv/...">
        </div>
      </div>

      <div class="btn-container">
        <button class="btn-start" onclick="startActivity()">▶ Start Activity on Discord</button>
        <button class="btn-stop" onclick="stopActivity()">⏹ Stop Activity</button>
      </div>
    </div>

    <!-- Live Preview -->
    <div class="card">
      <div class="card-title">Live Profile Preview</div>
      <div class="preview-card">
        <div class="preview-icon" id="previewIcon">🎮</div>
        <div class="preview-details">
          <h4 id="previewTitle">PLAYING A GAME</h4>
          <p id="previewDetails">Grand Theft Auto VI</p>
          <p id="previewState">Heist Mission</p>
          <p id="previewTime" style="color: #747f8d; font-size: 11px;">00:15:20 elapsed</p>
        </div>
      </div>
    </div>

    <div class="footer">
      Created with ❤️ by <a href="https://github.com/IsDevCan" target="_blank">IsDevCan</a> • Zero CPU Usage • 100% Free & Open Source
    </div>
  </div>

  <script>
    const presets = {
      "1": { name: "VALORANT", details: "Competitive", state: "In Match (13 - 11)" },
      "2": { name: "Fortnite", details: "Battle Royale", state: "Victory Royale! #1/100" },
      "3": { name: "Rocket League", details: "Competitive 3v3", state: "In Overtime (3 - 3)" },
      "4": { name: "Overwatch 2", details: "Competitive", state: "Push - Final Point" },
      "5": { name: "Rainbow Six Siege", details: "Ranked Bomb", state: "Match Point (4 - 4)" },
      "6": { name: "Grand Theft Auto V", details: "GTA Online", state: "Cayo Perico Heist" },
      "7": { name: "Minecraft", details: "Survival Mode", state: "Exploring Nether" },
      "8": { name: "Roblox", details: "Blox Fruits", state: "Grinding Bosses" },
      "9": { name: "Counter-Strike 2", details: "Premier Match", state: "Score: 11 - 9" },
      "10": { name: "League of Legends", details: "Ranked Solo", state: "Mid Lane (5/0/2)" },
      "11": { name: "Apex Legends", details: "Ranked Leagues", state: "Top 3 Squads" },
      "12": { name: "Genshin Impact", details: "Spiral Abyss", state: "Floor 12 Chamber 3" }
    };

    function applyPreset() {
      const val = document.getElementById("presetSelect").value;
      if (presets[val]) {
        document.getElementById("gameName").value = presets[val].name;
        document.getElementById("gameDetails").value = presets[val].details;
        document.getElementById("gameState").value = presets[val].state;
        updatePreview();
      }
    }

    function updatePreview() {
      const name = document.getElementById("gameName").value || "Grand Theft Auto VI";
      const details = document.getElementById("gameDetails").value || "Heist Mission";
      const state = document.getElementById("gameState").value || "5 Stars";
      document.getElementById("previewTitle").innerText = "PLAYING " + name.toUpperCase();
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
        alert("Please enter a Game or Activity name!");
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
          body: JSON.stringify({ name, details, state, timer, buttons })
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

    // Check status on load
    async function checkStatus() {
      try {
        const res = await fetch("/api/status");
        const data = await res.json();
        if (data.status === "active") {
          document.getElementById("statusBadge").className = "status-badge status-active";
          document.getElementById("statusText").innerText = "Active on Discord (" + data.name + ")";
          document.getElementById("gameName").value = data.name;
          document.getElementById("gameDetails").value = data.details;
          document.getElementById("gameState").value = data.state;
          updatePreview();
        }
      } catch (e) {}
    }
    checkStatus();
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

        if self.path == "/api/start":
            name = body.get("name", "")
            details = body.get("details", "")
            state = body.get("state", "")
            timer = body.get("timer", True)
            buttons = body.get("buttons", [])

            client_id = "811469787657928704" # Generic fallback client ID
            for k, p in PRESETS.items():
                if p["name"].lower() == name.lower():
                    client_id = p["id"]
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
                    "buttons": buttons
                }
                self.send_json({"success": True})
            else:
                self.send_json({"success": False, "error": "Failed to update Discord activity."})

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
