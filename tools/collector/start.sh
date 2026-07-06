#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : start.sh
#
# Description
# -----------
# Start the DNS Measurement Collector.
#
# Usage
# -----
# ./tools/collector/start.sh
#
# Author
# ------
# Helen Liu
# ==========================================================

# ==========================================================
# Configuration
# ==========================================================


PID_FILE="run/collector.pid"

LOG_FILE="logs/collector.log"

# ==========================================================
# Helper Functions
# ==========================================================

is_running() {

    # Save the process ID passed to this function.
    local pid="$1"

    # Return success if the specified process is running.
    ps -p "$pid" > /dev/null 2>&1

}

# ==========================================================
# Header
# ==========================================================

echo "======================================================"
echo "DNS Measurement Platform"
echo "Collector Start"
echo "======================================================"

# ==========================================================
# Prepare Directories
# ==========================================================

mkdir -p run

mkdir -p logs

# ==========================================================
# Validation
# ==========================================================

if [ -f "$PID_FILE" ]; then

    PID=$(cat "$PID_FILE")

    if is_running "$PID"; then

        echo
        echo "Status"
        echo "------------------------------------------------------"
        echo "Collector is already running."

        echo
        echo "PID"
        echo "------------------------------------------------------"
        echo "$PID"

        echo
        echo "======================================================"

        exit 0

    fi

fi

# ==========================================================
# Start Collector
# ==========================================================

echo
echo "Starting Collector..."
echo

nohup python -m app.collector.atlas_live_collector \
> "$LOG_FILE" 2>&1 &

PID=$!

echo "$PID" > "$PID_FILE"

sleep 2

# ==========================================================
# Verification
# ==========================================================

if is_running "$PID"; then

    STATUS="PASS"

else

    STATUS="FAIL"

    rm -f "$PID_FILE"

fi

# ==========================================================
# Report
# ==========================================================

echo "PID"
echo "------------------------------------------------------"
echo "$PID"

echo
echo "Log File"
echo "------------------------------------------------------"
echo "$LOG_FILE"

echo
echo "Status"
echo "------------------------------------------------------"
echo "$STATUS"

echo

if [ "$STATUS" = "PASS" ]; then

    echo "Collector started successfully."

    echo
    echo "======================================================"

    exit 0

else

    echo "Collector failed to start."

    echo
    echo "======================================================"

    exit 1

fi