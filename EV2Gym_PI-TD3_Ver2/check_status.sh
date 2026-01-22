#!/bin/bash
echo "=== Checking Training Status ==="
echo ""

echo "1. Checking active processes..."
if pgrep -f "python train.py" > /dev/null; then
    echo "   [RUNNING] A training process is currently active."
    pgrep -af "python train.py"
else
    echo "   [STOPPED] No training process found."
fi
echo ""

echo "2. Checking most recent saved models (saved_models/)..."
# List directories sorted by time, newest first, max 3
ls -ltd saved_models/*/ 2>/dev/null | head -n 3
echo ""

echo "3. Checking last log entries (output.log)..."
if [ -f "output.log" ]; then
    tail -n 5 output.log
else
    echo "   [MISSING] output.log not found."
fi
