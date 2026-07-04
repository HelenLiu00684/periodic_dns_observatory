#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : status.sh
#
# Description
# -----------
# Display the current status of the DNS Measurement Collector.
#
# Usage
# -----
# ./tools/collector/status.sh
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
echo "Collector Status"
echo "======================================================"

# ==========================================================
# Validation
# ==========================================================

if [ ! -f "$PID_FILE" ]; then

    echo
    echo "Collector"
    echo "------------------------------------------------------"
    echo "STOPPED"

    echo
    echo "Status"
    echo "------------------------------------------------------"
    echo "FAIL : PID file not found."

    echo
    echo "======================================================"

    exit 1

fi

PID=$(cat "$PID_FILE")

# ==========================================================
# Process Status
# ==========================================================

if is_running "$PID"; then

    STATUS="RUNNING"
    RESULT="PASS"

    START_TIME=$(ps -p "$PID" -o lstart=)

else

    STATUS="STOPPED"
    RESULT="FAIL"

fi

# ==========================================================
# Report
# ==========================================================

echo
echo "Collector"
echo "------------------------------------------------------"
echo "$STATUS"

echo
echo "PID"
echo "------------------------------------------------------"
echo "$PID"

if [ "$RESULT" = "PASS" ]; then

    echo
    echo "Start Time"
    echo "------------------------------------------------------"
    echo "$START_TIME"

fi

echo
echo "Log File"
echo "------------------------------------------------------"
echo "$LOG_FILE"

echo
echo "Status"
echo "------------------------------------------------------"
echo "$RESULT"

echo
echo "======================================================"

if [ "$RESULT" = "PASS" ]; then

    exit 0

else

    exit 1

fi