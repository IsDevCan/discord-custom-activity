#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="$DIR/activity.pid"
LOGFILE="$DIR/activity.log"

if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "[!] Activity is already running (PID $PID)."
        echo "[*] Run ./status.sh to check, or ./stop.sh to stop."
        exit 0
    fi
fi

echo "[*] Launching Discord Custom Activity in background..."
nohup python3 -u "$DIR/activity.py" "$@" > "$LOGFILE" 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PIDFILE"

sleep 1
if kill -0 "$NEW_PID" 2>/dev/null; then
    echo "[✓] Custom Activity started! (PID: $NEW_PID)"
    echo "[*] Check status: ./status.sh"
    echo "[*] Stop anytime: ./stop.sh"
else
    echo "[X] Failed to launch. Check $LOGFILE."
    rm -f "$PIDFILE"
fi
