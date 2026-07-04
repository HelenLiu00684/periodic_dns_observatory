#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : health.sh
#
# Description
# -----------
# Run a one-time SQLite database health check.
#
# Usage
# -----
# ./tools/db/health.sh
#
# Author
# ------
# Helen Liu
# ==========================================================

DATABASE="data/dns_measurement.db"

echo "======================================================"
echo "DNS Measurement Platform"
echo "Database Health"
echo "======================================================"

if [ ! -f "$DATABASE" ]; then
    echo
    echo "Database"
    echo "------------------------------------------------------"
    echo "NOT FOUND"

    echo
    echo "Status"
    echo "------------------------------------------------------"
    echo "FAIL"

    echo "======================================================"
    exit 1
fi

INTEGRITY=$(sqlite3 "$DATABASE" "PRAGMA integrity_check;")

if [ "$INTEGRITY" != "ok" ]; then
    echo
    echo "SQLite Integrity"
    echo "------------------------------------------------------"
    echo "$INTEGRITY"

    echo
    echo "Status"
    echo "------------------------------------------------------"
    echo "FAIL"

    echo "======================================================"
    exit 1
fi

OBSERVATIONS=$(sqlite3 "$DATABASE" "SELECT COUNT(*) FROM observation;")

echo
echo "Database"
echo "------------------------------------------------------"
echo "$DATABASE"

echo
echo "SQLite Integrity"
echo "------------------------------------------------------"
echo "PASS"

echo
echo "Observation Records"
echo "------------------------------------------------------"
echo "$OBSERVATIONS"

echo
echo "Status"
echo "------------------------------------------------------"
echo "PASS"

echo "======================================================"

exit 0