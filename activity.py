#!/usr/bin/env python3
"""
Discord Custom Activity & Rich Presence Manager
Created by IsDevCan
Allows anyone to display any custom game, activity, details, state, and buttons on Discord with 0% CPU.
"""

import os
import sys
import time
import socket
import struct
import json
import uuid
import signal
import argparse

PRESETS = {
    "1": {
        "id": "811469787657928704",
        "name": "VALORANT",
        "details": "Competitive",
        "state": "In Match (13 - 11)",
        "assets": {"large_image": "bind", "large_text": "Ascent", "small_image": "reyna", "small_text": "Reyna"}
    },
    "2": {
        "id": "432980957394370572",
        "name": "Fortnite",
        "details": "Battle Royale",
        "state": "Victory Royale! #1/100",
        "assets": {}
    },
    "3": {
        "id": "356877880938070016",
        "name": "Rocket League",
        "details": "Competitive 3v3",
        "state": "In Overtime (3 - 3)",
        "assets": {}
    },
    "4": {
        "id": "356875221078245376",
        "name": "Overwatch",
        "details": "Competitive",
        "state": "Push - Final Point",
        "assets": {}
    },
    "5": {
        "id": "356876590342340608",
        "name": "Rainbow Six Siege",
        "details": "Ranked Bomb",
        "state": "Match Point (4 - 4)",
        "assets": {}
    },
    "6": {
        "id": "356869127241072640",
        "name": "Grand Theft Auto V",
        "details": "GTA Online",
        "state": "Cayo Perico Heist",
        "assets": {}
    },
    "gta6": {
        "id": "811469787657928704",
        "name": "Grand Theft Auto VI",
        "details": "Playing Early Access Dev Build",
        "state": "Vice City Heist (Mission 42)",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/gta6.png?v=2",
            "large_text": "Grand Theft Auto VI"
        }
    },
    "silksong": {
        "id": "811469787657928704",
        "name": "Hollow Knight: Silksong",
        "details": "Pharloom Citadel (100% Run)",
        "state": "Waiting Since 2019",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/silksong.png?v=2",
            "large_text": "Hollow Knight: Silksong"
        }
    },
    "halflife3": {
        "id": "811469787657928704",
        "name": "Half-Life 3",
        "details": "Valve Internal Beta v0.9",
        "state": "Chapter 7: Return to Borealis",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/halflife3.png?v=2",
            "large_text": "Half-Life 3"
        }
    },
    "bloodborne": {
        "id": "811469787657928704",
        "name": "Bloodborne PC Remaster",
        "details": "4K 120FPS (Finally on PC)",
        "state": "Father Gascoigne (Attempt 1)",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/bloodborne_pc.png?v=2",
            "large_text": "Bloodborne PC Remaster"
        }
    },
    "portal3": {
        "id": "811469787657928704",
        "name": "Portal 3",
        "details": "Aperture Science Testing",
        "state": "Chamber 47 - Still No Cake",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/portal3.png?v=2",
            "large_text": "Portal 3"
        }
    },
    "minecraft2": {
        "id": "432980957394370572",
        "name": "Minecraft 2 (Unreal Engine 5)",
        "details": "Spherical World Mode",
        "state": "Herobrine Encounter",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/minecraft2.png?v=2",
            "large_text": "Minecraft 2 (UE5)"
        }
    },
    "chess2": {
        "id": "811469787657928704",
        "name": "Chess 2: Battle Royale",
        "details": "Ranked 100-Player Gulag",
        "state": "Pawns Got Nerfed",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/chess2.png?v=2",
            "large_text": "Chess 2"
        }
    },
    "grass": {
        "id": "811469787657928704",
        "name": "Touching Grass Simulator 2026",
        "details": "Tutorial: Leaving My Room",
        "state": "Sunlight Burning My Eyes",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/touching_grass.png?v=2",
            "large_text": "Touching Grass"
        }
    },
    "nitro": {
        "id": "811469787657928704",
        "name": "Free Discord Nitro Generator 3D",
        "details": "Mining Free Nitro Coins",
        "state": "100% Legit No Virus",
        "assets": {
            "large_image": "https://raw.githubusercontent.com/IsDevCan/discord-custom-activity/main/assets/icons/nitro_generator.png?v=2",
            "large_text": "Free Nitro Generator"
        }
    }
}

running = True

def signal_handler(signum, frame):
    global running
    print("\n[!] Stopping Custom Activity...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_discord_socket():
    candidates = [
        os.environ.get("TMPDIR", ""),
        "/tmp",
        os.environ.get("XDG_RUNTIME_DIR", "")
    ]
    for base in candidates:
        if not base:
            continue
        for i in range(10):
            p = os.path.join(base, f"discord-ipc-{i}")
            if os.path.exists(p):
                return p
    return None

class DiscordIPC:
    def __init__(self, client_id):
        self.client_id = str(client_id)
        self.sock = None

    def connect(self):
        sock_path = get_discord_socket()
        if not sock_path:
            return False, "Discord is not running. Please launch the Discord desktop app."

        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect(sock_path)

            # Handshake
            payload = json.dumps({"v": 1, "client_id": self.client_id}).encode("utf-8")
            self.sock.sendall(struct.pack("<ii", 0, len(payload)) + payload)

            resp_hdr = self.sock.recv(8)
            if len(resp_hdr) < 8:
                self.close()
                return False, "Invalid handshake response from Discord."
            op, length = struct.unpack("<ii", resp_hdr)
            resp = json.loads(self.sock.recv(length).decode("utf-8"))
            if resp.get("evt") == "ERROR":
                self.close()
                return False, resp.get("data", {}).get("message")
            return True, "Connected"
        except Exception as e:
            self.close()
            return False, str(e)

    def set_activity(self, name, details, state, start_timestamp, assets=None, buttons=None):
        if not self.sock:
            return False
        try:
            activity = {}
            if name:
                activity["name"] = name
            if details:
                activity["details"] = details
            if state:
                activity["state"] = state
            if start_timestamp:
                activity["timestamps"] = {"start": start_timestamp}
            if assets:
                activity["assets"] = assets
            if buttons:
                activity["buttons"] = buttons

            payload = json.dumps({
                "cmd": "SET_ACTIVITY",
                "args": {
                    "pid": os.getpid(),
                    "activity": activity
                },
                "nonce": str(uuid.uuid4())
            }).encode("utf-8")

            self.sock.sendall(struct.pack("<ii", 1, len(payload)) + payload)
            resp_hdr = self.sock.recv(8)
            if len(resp_hdr) < 8:
                return False
            op, length = struct.unpack("<ii", resp_hdr)
            self.sock.recv(length)
            return True
        except Exception:
            return False

    def close(self):
        if self.sock:
            try:
                clear = json.dumps({
                    "cmd": "SET_ACTIVITY",
                    "args": {"pid": os.getpid(), "activity": None},
                    "nonce": str(uuid.uuid4())
                }).encode("utf-8")
                self.sock.sendall(struct.pack("<ii", 1, len(clear)) + clear)
                resp_hdr = self.sock.recv(8)
                if len(resp_hdr) == 8:
                    self.sock.recv(struct.unpack("<ii", resp_hdr)[1])
            except Exception:
                pass
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None

def interactive_menu():
    print("=" * 60)
    print("✨ DISCORD CUSTOM ACTIVITY BUILDER")
    print("Author: IsDevCan (https://github.com/IsDevCan)")
    print("=" * 60)
    print("Choose an option:")
    print("  [1] Pick a Verified Game Preset (Valorant, Fortnite, GTA V, etc.)")
    print("  [2] Create a 100% Custom Activity (Any game name, details & state)")
    print("  [3] Custom Activity with Clickable Profile Buttons")
    print("=" * 60)

    choice = input("Enter choice (1-3) [default: 1]: ").strip() or "1"

    if choice == "1":
        print("\nAvailable Presets:")
        for k, v in PRESETS.items():
            print(f"  [{k}] {v['name']} ({v['details']} - {v['state']})")
        preset_choice = input(f"Select preset (1-{len(PRESETS)}) [default: 1]: ").strip() or "1"
        preset = PRESETS.get(preset_choice, PRESETS["1"])
        return {
            "client_id": preset["id"],
            "name": preset["name"],
            "details": preset["details"],
            "state": preset["state"],
            "timer": True,
            "assets": preset.get("assets", {}),
            "buttons": None
        }

    elif choice in ["2", "3"]:
        print("\n--- Customize Your Activity ---")
        name = input("Activity / Game Name (e.g. GTA 6, Silksong, Studying): ").strip() or "Custom Game"
        details = input("Details (Line 1, e.g. Playing Solo, Episode 5): ").strip() or "In Game"
        state = input("State (Line 2, e.g. Rank: Immortal, Chapter 3): ").strip() or "Online"
        timer_in = input("Show elapsed timer? (y/n) [default: y]: ").strip().lower()
        timer = timer_in != "n"

        buttons = None
        if choice == "3":
            print("\n--- Clickable Profile Buttons ---")
            btn1_label = input("Button 1 Text (e.g. Join Party / View Stream): ").strip()
            btn1_url = input("Button 1 Link (https://...): ").strip()
            if btn1_label and btn1_url:
                buttons = [{"label": btn1_label, "url": btn1_url}]
                btn2_label = input("Button 2 Text (optional): ").strip()
                if btn2_label:
                    btn2_url = input("Button 2 Link (https://...): ").strip()
                    if btn2_url:
                        buttons.append({"label": btn2_label, "url": btn2_url})

        return {
            "client_id": "811469787657928704",
            "name": name,
            "details": details,
            "state": state,
            "timer": timer,
            "assets": {},
            "buttons": buttons
        }

    return None

def main():
    parser = argparse.ArgumentParser(description="Discord Custom Activity Manager")
    parser.add_argument("--name", help="Custom game or activity name")
    parser.add_argument("--details", help="Line 1 status details")
    parser.add_argument("--state", help="Line 2 status state")
    parser.add_argument("--preset", choices=["valorant", "fortnite", "rocket_league", "overwatch", "siege", "gta5"],
                        help="Quick launch a game preset")
    parser.add_argument("--no-timer", action="store_true", help="Disable elapsed live timer")
    parser.add_argument("--btn-text", help="Clickable button label")
    parser.add_argument("--btn-url", help="Clickable button URL")
    args = parser.parse_args()

    # If no flags passed, launch interactive builder
    if not (args.name or args.preset):
        config = interactive_menu()
        if not config:
            print("[!] Exiting.")
            sys.exit(0)
    else:
        preset_map = {
            "valorant": "1",
            "fortnite": "2",
            "rocket_league": "3",
            "overwatch": "4",
            "siege": "5",
            "gta5": "6",
            "gta6": "gta6",
            "silksong": "silksong",
            "halflife3": "halflife3",
            "bloodborne": "bloodborne",
            "portal3": "portal3",
            "minecraft2": "minecraft2",
            "chess2": "chess2",
            "grass": "grass",
            "nitro": "nitro"
        }
        if args.preset:
            p = PRESETS[preset_map[args.preset]]
            config = {
                "client_id": p["id"],
                "name": p["name"],
                "details": args.details or p["details"],
                "state": args.state or p["state"],
                "timer": not args.no_timer,
                "assets": p.get("assets", {}),
                "buttons": None
            }
        else:
            btns = None
            if args.btn_text and args.btn_url:
                btns = [{"label": args.btn_text, "url": args.btn_url}]
            config = {
                "client_id": "811469787657928704",
                "name": args.name,
                "details": args.details or "Playing",
                "state": args.state or "Online",
                "timer": not args.no_timer,
                "assets": {},
                "buttons": btns
            }

    print("\n" + "=" * 60)
    print("🚀 LAUNCHING CUSTOM DISCORD ACTIVITY")
    print(f"Activity Name : {config['name']}")
    print(f"Details       : {config['details']}")
    print(f"State         : {config['state']}")
    print(f"Elapsed Timer : {'Enabled' if config['timer'] else 'Disabled'}")
    if config.get("buttons"):
        print(f"Buttons       : {len(config['buttons'])} custom clickable link(s)")
    print("=" * 60)

    ipc = DiscordIPC(config["client_id"])
    start_time = int(time.time()) if config["timer"] else None

    while running:
        if not ipc.sock:
            ok, msg = ipc.connect()
            if not ok:
                sys.stdout.write(f"\r[!] {msg} Retrying in 5s...   ")
                sys.stdout.flush()
                time.sleep(5)
                continue
            print("\n[✓] Connected to Discord! Activity is now live on your profile.")

        ok = ipc.set_activity(
            name=config["name"],
            details=config["details"],
            state=config["state"],
            start_timestamp=start_time,
            assets=config.get("assets"),
            buttons=config.get("buttons")
        )
        if not ok:
            print("\n[!] Connection dropped. Reconnecting...")
            ipc.close()
            time.sleep(3)
            continue

        elapsed = time.time() - (start_time or time.time())
        sys.stdout.write(f"\r🟢 Active: {config['name']} | Status: {config['details']} - {config['state']} {' ' * 10}")
        sys.stdout.flush()
        time.sleep(10)

    ipc.close()
    print("\n[✓] Custom activity stopped cleanly.")

if __name__ == "__main__":
    main()
