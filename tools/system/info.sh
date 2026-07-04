#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : info.sh
#
# Description
# ----------------------------------------------------------
# Display platform information.
#
# Usage
# ----------------------------------------------------------
# ./tools/system/info.sh
#
# Author
# ----------------------------------------------------------
# Helen Liu
# ==========================================================

echo "======================================================"
echo "DNS Measurement Platform"
echo "System Information"
echo "======================================================"

echo
echo "Platform"
echo "------------------------------------------------------"
echo "DNS Measurement Platform"

echo
echo "Python Version"
echo "------------------------------------------------------"
python3 --version

echo
echo "SQLite Version"
echo "------------------------------------------------------"
sqlite3 --version

echo
echo "Operating System"
echo "------------------------------------------------------"
uname -a

echo
echo "Disk Usage"
echo "------------------------------------------------------"
df -h .

echo
echo "Memory"
echo "------------------------------------------------------"
free -h

echo
echo "CPU"
echo "------------------------------------------------------"
lscpu | grep "Model name"

echo
echo "======================================================"