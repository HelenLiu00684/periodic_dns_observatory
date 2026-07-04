#!/bin/bash

# ==========================================================
# Project : DNS Measurement Platform
# Script  : diagnose.sh
#
# Description
# ----------------------------------------------------------
# Launch the platform diagnosis engine.
#
# Usage
# ----------------------------------------------------------
# ./tools/system/diagnose.sh
# ./tools/system/diagnose.sh --json
#
# Author
# ----------------------------------------------------------
# Helen Liu
# ==========================================================

python3 -m app.system.diagnose "$@"