#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : health.sh
#
# Description
# -----------
# Perform a basic health check for the platform.
#
# Usage
# -----
# ./tools/system/health.sh
#
# Author
# ------
# Helen Liu
# ==========================================================

echo "======================================================"
echo "DNS Measurement Platform"
echo "System Health Check"
echo "======================================================"

echo
echo "Collector"
echo "------------------------------------------------------"

./tools/collector/status.sh > /dev/null

COLLECTOR_RESULT=$?

if [ $COLLECTOR_RESULT -eq 0 ]; then
    echo "PASS"
else
    echo "FAIL"
fi

echo
echo "Database"
echo "------------------------------------------------------"

./tools/db/status.sh > /dev/null

DATABASE_RESULT=$?

if [ $DATABASE_RESULT -eq 0 ]; then
    echo "PASS"
else
    echo "FAIL"
fi

echo
echo "SQLite Integrity"
echo "------------------------------------------------------"

./tools/db/health.sh > /dev/null

CHECK_RESULT=$?

if [ $CHECK_RESULT -eq 0 ]; then
    echo "PASS"
else
    echo "FAIL"
fi

echo
echo "Overall Health"
echo "------------------------------------------------------"

if [ $COLLECTOR_RESULT -eq 0 ] && \
   [ $DATABASE_RESULT -eq 0 ] && \
   [ $CHECK_RESULT -eq 0 ]; then

    echo "HEALTHY"

    RESULT=0

else

    echo "UNHEALTHY"

    RESULT=1

fi

echo
echo "======================================================"

exit $RESULT