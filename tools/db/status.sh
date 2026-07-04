#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : status.sh
#
# Description
# -----------
# Display the current status of the SQLite database.
#
# Usage
# -----
# ./tools/db/status.sh
#
# Author
# ------
# Helen Liu
# ==========================================================

# ==========================================================
# Configuration
# ==========================================================

DATABASE="data/dns_measurement.db"

# ==========================================================
# Header
# ==========================================================

echo "======================================================"
echo "DNS Measurement Platform"
echo "Database Status"
echo "======================================================"

# ==========================================================
# Validation
# ==========================================================

if [ ! -f "$DATABASE" ]; then

    echo
    echo "Database"
    echo "------------------------------------------------------"
    echo "NOT FOUND"

    echo
    echo "Status"
    echo "------------------------------------------------------"
    echo "FAIL"

    echo
    echo "======================================================"

    exit 1

fi

# ==========================================================
# Database Information
# ==========================================================

SIZE=$(du -h "$DATABASE" | cut -f1)

MEASUREMENTS=$(sqlite3 "$DATABASE" \
"SELECT COUNT(*) FROM measurement;")

PROBES=$(sqlite3 "$DATABASE" \
"SELECT COUNT(*) FROM probe;")

OBSERVATIONS=$(sqlite3 "$DATABASE" \
"SELECT COUNT(*) FROM observation;")

LATEST=$(sqlite3 "$DATABASE" \
"SELECT MAX(timestamp) FROM observation;")

# ==========================================================
# Report
# ==========================================================

echo
echo "Database"
echo "------------------------------------------------------"
echo "$DATABASE"

echo
echo "Database Size"
echo "------------------------------------------------------"
echo "$SIZE"

echo
echo "Measurement Records"
echo "------------------------------------------------------"
echo "$MEASUREMENTS"

echo
echo "Probe Records"
echo "------------------------------------------------------"
echo "$PROBES"

echo
echo "Observation Records"
echo "------------------------------------------------------"
echo "$OBSERVATIONS"

echo
echo "Latest Timestamp"
echo "------------------------------------------------------"
echo "$LATEST"

echo
echo "Status"
echo "------------------------------------------------------"
echo "PASS"

echo
echo "======================================================"

exit 0