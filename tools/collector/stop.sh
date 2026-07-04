#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : stop.sh
#
# Description
# -----------
# Stop the DNS Measurement Collector.
#
# Usage
# -----
# ./tools/collector/stop.sh
#
# Author
# ------
# Helen Liu
# ==========================================================

# ==========================================================
# Configuration
# ==========================================================

PID_FILE="run/collector.pid"

# ==========================================================
# Helper Function
# is_running() {

#     # Save the process ID passed to this function.
#     local pid="$1"

#     # Verify whether the process is currently running.
#     # Only the command exit status is used.
#     ps -p "$pid" > /dev/null 2>&1

# }
# ==========================================================

is_running() {

    ps -p "$1" > /dev/null 2>&1

}

# ==========================================================
# Header
# ==========================================================

echo "======================================================"
echo "DNS Measurement Platform"
echo "Collector Stop"
echo "======================================================"

# ==========================================================
# Validation
# ==========================================================

if [ ! -f "$PID_FILE" ]; then

    echo
    echo "Status"
    echo "------------------------------------------------------"
    echo "FAIL : PID file not found."

    echo
    echo "Collector is probably not running."

    echo
    echo "======================================================"

    exit 1

fi

PID=$(cat "$PID_FILE")

# ==========================================================
# Check Process
# ==========================================================

if ! is_running "$PID"; then

    rm -f "$PID_FILE"

    echo
    echo "Status"
    echo "------------------------------------------------------"
    echo "Collector is already stopped."

    echo
    echo "======================================================"

    exit 0

fi

# ==========================================================
# Stop Collector
# ==========================================================

echo
echo "Stopping Collector..."
echo

kill "$PID"

sleep 2

# ==========================================================
# Verification
# ==========================================================

if is_running "$PID"; then

    STATUS="FAIL"

else

    STATUS="PASS"

    rm -f "$PID_FILE"

fi

# ==========================================================
# Report
# ==========================================================

echo "PID"
echo "------------------------------------------------------"
echo "$PID"

echo
echo "Status"
echo "------------------------------------------------------"
echo "$STATUS"

echo

if [ "$STATUS" = "PASS" ]; then

    echo "Collector stopped successfully."

    echo
    echo "======================================================"

    exit 0

else

    echo "Collector is still running."

    echo
    echo "======================================================"

    exit 1

fi