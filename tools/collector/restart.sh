#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : restart.sh
#
# Description
# -----------
# Restart the DNS Measurement Collector.
#
# Usage
# -----
# ./tools/collector/restart.sh
#
# Author
# ------
# Helen Liu
# ==========================================================

echo "======================================================"
echo "DNS Measurement Platform"
echo "Collector Restart"
echo "======================================================"

echo
echo "Stopping collector..."
echo

./tools/collector/stop.sh

STOP_RESULT=$?

echo
echo "Starting collector..."
echo

./tools/collector/start.sh

START_RESULT=$?

echo
echo "Verifying collector status..."
echo

./tools/collector/status.sh

STATUS_RESULT=$?

echo
echo "======================================================"

if [ $STOP_RESULT -eq 0 ] && \
   [ $START_RESULT -eq 0 ] && \
   [ $STATUS_RESULT -eq 0 ]; then

    echo "Restart completed successfully."

    echo "======================================================"

    exit 0

else

    echo "Restart failed."

    echo "======================================================"

    exit 1

fi