#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : backup.sh
#
# Description
# -----------
# Create a timestamped backup of the SQLite database.
#
# Usage
# -----
# ./tools/db/backup.sh
#
# Author
# ------
# Helen Liu
# ==========================================================


# ==========================================================
# Configuration
# ==========================================================

DB="data/dns_measurement.db"

BACKUP_DIR="backup"


# ==========================================================
# Validation
# ==========================================================

if [ ! -f "$DB" ]; then

    echo "[ERROR] Database not found."

    echo "$DB"

    exit 1

fi


# ==========================================================
# Prepare Backup Directory
# ==========================================================

mkdir -p "$BACKUP_DIR"


# ==========================================================
# Generate Backup Filename
# ==========================================================

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

BACKUP_FILE="$BACKUP_DIR/periodic_dns_${TIMESTAMP}.db"


# ==========================================================
# Backup
# ==========================================================

cp "$DB" "$BACKUP_FILE"

if [ $? -ne 0 ]; then

    echo "[ERROR] Backup failed."

    exit 1

fi


# ==========================================================
# Report
# ==========================================================

echo "======================================================"
echo "DNS Measurement Platform"
echo "Database Backup"
echo "======================================================"

echo
echo "Source Database"
echo "------------------------------------------------------"
echo "$DB"

echo
echo "Backup File"
echo "------------------------------------------------------"
echo "$BACKUP_FILE"

echo
echo "Backup Size"
echo "------------------------------------------------------"
du -h "$BACKUP_FILE" | cut -f1

echo
echo "Backup Time"
echo "------------------------------------------------------"
date

echo
echo "Observation Records"
echo "------------------------------------------------------"

sqlite3 "$BACKUP_FILE" \
"SELECT COUNT(*) FROM observation;"

echo
echo "Verifying Backup..."

ORIGINAL=$(sqlite3 "$DB" \
"SELECT COUNT(*) FROM observation;")

BACKUP=$(sqlite3 "$BACKUP_FILE" \
"SELECT COUNT(*) FROM observation;")

if [ "$ORIGINAL" = "$BACKUP" ]; then
    echo "Verification : PASS"
else
    echo "Verification : FAIL"
fi

echo
echo "Status"
echo "------------------------------------------------------"
echo "PASS"

echo "======================================================"

exit 0