#!/bin/bash

# OPLC-Plus GUI/Launcher Handoff Entrypoint
# Spawns native macOS dialog interface boxes to pass parameters to the builder backend.

APP_DIR="$(dirname "$0")"
PYTHON_ENGINE="$APP_DIR/../Resources/src/shared/generate.py"

# Use native AppleScript GUI popups to query the target configuration selection
TARGET_CHOICE=$(osascript -e 'choose from list {"1. Intel Mac (2010-2015 Legacy)", "2. Qualcomm Snapdragon Laptop"} with title "OPLC-Plus Release Build Manager" with prompt "Select target device environment:" default items {"1. Intel Mac (2010-2015 Legacy)"}')

if [ "$TARGET_CHOICE" == "false" ]; then
    exit 0
fi

if [[ "$TARGET_CHOICE" == *"Intel"* ]]; then
    SMBIOS_ID=$(osascript -e 'display dialog "Enter target Mac SMBIOS Identifier (e.g., MacBookPro11,4):" default answer "MacBookPro11,4" with title "OPLC-Plus Intel Pipeline"' -e 'text returned of result')
    
    # Run the core python generator pipeline right inside the app tree context
    python3 "$PYTHON_ENGINE" --target intel_legacy --hardware_id "$SMBIOS_ID"
    
    osascript -e "display dialog \"OpenCore template bundle layout generated successfully in your local workspace path: dist/config.plist\" with title \"OPLC-Plus Success\" buttons {\"OK\"}"
else
    # Trigger Snapdragon layout variables
    python3 "$PYTHON_ENGINE" --target snapdragon --hardware_id "X1E-80-100"
    osascript -e "display dialog \"Universal Qualcomm Snapdragon firmware configurations generated inside: dist/\" with title \"OPLC-Plus Success\" buttons {\"OK\"}"
fi
