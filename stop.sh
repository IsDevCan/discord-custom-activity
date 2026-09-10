#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="$DIR/activity.pid"

if [ ! -f "$PIDFILE" ]; then
    echo "[!] No running activity found."
    exit 0
fi

PID=$(cat "$PIDFILE")
if kill -0 "$PID" 2>/dev/null; then
    echo "[*] Stopping Custom Activity (PID $PID)..."
    kill -TERM "$PID" 2>/dev/null
    sleep 1
    if kill -0 "$PID" 2>/dev/null; then
        kill -9 "$PID" 2>/dev/null
    fi
    echo "[✓] Custom Activity stopped."
else
    echo "[*] Process was not active."
fi
rm -f "$PIDFILE"
