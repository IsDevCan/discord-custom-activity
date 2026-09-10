#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIDFILE="$DIR/activity.pid"
LOGFILE="$DIR/activity.log"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    PID=$(cat "$PIDFILE")
    echo "=========================================="
    echo "🟢 STATUS: Active (PID: $PID)"
    echo "=========================================="
    if [ -f "$LOGFILE" ]; then
        tail -n 10 "$LOGFILE"
    fi
    echo ""
    echo "To stop: ./stop.sh"
else
    echo "=========================================="
    echo "🔴 STATUS: Inactive"
    echo "=========================================="
    echo "To start interactive builder: python3 activity.py"
    echo "To start in background: ./start.sh --name 'My Game'"
fi
