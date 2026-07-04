#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : logs.sh
#
# Description
# ----------------------------------------------------------
# Display the collector log.
#
# Usage
# ----------------------------------------------------------
# ./tools/collector/logs.sh
# ./tools/collector/logs.sh -f
#
# Author
# ----------------------------------------------------------
# Helen Liu
# ==========================================================

LOG_FILE="logs/collector.log"

if [ ! -f "$LOG_FILE" ]; then

    echo "Collector log not found."

    exit 1

fi

if [ "$1" = "-f" ]; then

    tail -f "$LOG_FILE"

else

    tail -100 "$LOG_FILE"

fi