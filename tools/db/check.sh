#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : check.sh
#
# Description
# ----------------------------------------------------------
# Monitor the SQLite archive database.
#
# Validation:
#
#   • Database exists
#   • SQLite is readable
#   • Latest observation timestamp increases
#
# Author
# ----------------------------------------------------------
# Helen Liu
# ==========================================================


# ==========================================================
# Configuration
# ==========================================================

CHECK_INTERVAL=120


# ==========================================================
# Project Paths
# ==========================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

DB="$PROJECT_ROOT/data/dns_measurement.db"


# ==========================================================
# Validation
# ==========================================================

if [ ! -f "$DB" ]; then

    echo ""
    echo "==============================================="
    echo "Database Health Check"
    echo "==============================================="
    echo "[ERROR] Database not found."
    echo "$DB"
    echo "==============================================="
    exit 1

fi


# ==========================================================
# Initial Snapshot
# ==========================================================

previous_count=$(sqlite3 "$DB" \
"SELECT COUNT(*) FROM observation;")

previous_timestamp=$(sqlite3 "$DB" \
"SELECT COALESCE(MAX(timestamp),0) FROM observation;")


# ==========================================================
# Main Loop
# ==========================================================

while true
do

    current_count=$(sqlite3 "$DB" \
    "SELECT COUNT(*) FROM observation;")

    current_timestamp=$(sqlite3 "$DB" \
    "SELECT COALESCE(MAX(timestamp),0) FROM observation;")

    delta=$((current_timestamp-previous_timestamp))

    clear

    echo "======================================================"
    echo "West Africa DNS Observatory"
    echo "SQLite Archive Health Monitor"
    echo "======================================================"

    echo ""
    echo "Check Time"
    echo "------------------------------------------------------"
    date

    echo ""
    echo "Database"
    echo "------------------------------------------------------"
    echo "$DB"

    echo ""
    echo "Observation Count"
    echo "------------------------------------------------------"
    echo "$current_count"

    echo ""
    echo "Latest Timestamp"
    echo "------------------------------------------------------"
    echo "$current_timestamp"

    echo ""
    echo "Timestamp Delta"
    echo "------------------------------------------------------"
    echo "$delta"

    echo ""

    if [ "$delta" -gt 0 ]; then

        echo "Status"
        echo "------------------------------------------------------"
        echo "PASS : Archive is updating normally."

    elif [ "$delta" -eq 0 ]; then

        echo "Status"
        echo "------------------------------------------------------"
        echo "WARNING : No new observations."

    else

        echo "Status"
        echo "------------------------------------------------------"
        echo "ERROR : Timestamp moved backwards."

    fi

    echo ""
    echo "Next Check"
    echo "------------------------------------------------------"
    date -d "+$CHECK_INTERVAL seconds"

    previous_count="$current_count"
    previous_timestamp="$current_timestamp"

    sleep "$CHECK_INTERVAL"

done