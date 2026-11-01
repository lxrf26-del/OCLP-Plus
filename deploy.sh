#!/bin/bash

# OPLC-Plus Automated EFI Installation Deployment Tool
# Safe script utility to mount volume targets and stage compiled OpenCore workspaces.

set -e # Terminate script immediately if any step encounters an error

# Text color definitions for terminal reporting
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

show_usage() {
    echo -e "${YELLOW}OPLC-Plus Automated Flash Deployment Utility${NC}"
    echo -e "Usage: $0 --volume </Volumes/TargetDriveName>"
    echo ""
    echo -e "Options:"
    echo -e "  --volume <path>   Provide the direct mount path to your GPT-formatted target drive"
    echo -e "  --help            Display this automated deployment instruction menu"
    echo ""
}

# Ensure script is provided with an active volume argument path
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --volume)
            if [ -z "$2" ]; then
                echo -e "${RED}[- ] Error: --volume requires a valid mounted directory path target.${NC}"
                exit 1
            fi
            TARGET_VOLUME="$2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}[- ] Unknown parameter flag: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# --- SECURITY PROTECTION AUDITS ---
echo -e "${CYAN}[*] Running target drive security layout checks...${NC}"

# Absolute block preventing users from providing the primary operating system root partition
if [ "$TARGET_VOLUME" == "/" ] || [ "$TARGET_VOLUME" == "/System/Volumes/Data" ]; then
    echo -e "${RED}[!!] CRITICAL SAFETY CANCELLATION: Targeted directory path is locked by host OS partition system.${NC}"
    echo -e "${RED}Deployment aborted to protect your main workspace installation data from permanent loss.${NC}"
    exit 1
fi

# Ensure the targeted mount location actually exists on the computer file system
if [ ! -d "$TARGET_VOLUME" ]; then
    echo -e "${RED}[- ] Volume Target Error: Directory location path does not exist: $TARGET_VOLUME${NC}"
    echo -e "${YELLOW}Please confirm your USB media is attached and correctly mounted via Disk Utility.${NC}"
    exit 1
fi

# Confirm that compilation assets exist inside the /dist production folder path
if [ ! -f "dist/config.plist" ]; then
    echo -e "${RED}[- ] Deployment Error: Compiled configuration file 'dist/config.plist' was not found.${NC}"
    echo -e "${YELLOW}Please run your primary generation pipeline first (e.g., './build.sh --intel MacBookPro11,4')${NC}"
    exit 1
fi

# --- COMMENCE DISK STAGING PIPELINE ---
echo -e "${GREEN}[+] Target disk verified: $TARGET_VOLUME${NC}"

EFI_OC_DIR="$TARGET_VOLUME/EFI/OC"

echo -e "${CYAN}[*] Staging OpenCore structural directory paths...${NC}"
mkdir -p "$EFI_OC_DIR/ACPI"
mkdir -p "$EFI_OC_DIR/Kexts"

# Flush previous iteration test files safely within our designated EFI scope folder
echo -e "${CYAN}[*] Purging expired testing config templates from the media target...${NC}"
rm -f "$EFI_OC_DIR/config.plist"

# Copy newly compiled config boilerplate out to the flash volume destination path
echo -e "${CYAN}[*] Flashing newly compiled configuration template file...${NC}"
cp "dist/config.plist" "$EFI_OC_DIR/"

# Move compiled ACPI table assets over to the driver payloads layout if they were generated (Snapdragon targets)
if [ -f "dist/acpi/SSDT-OPLC-SNAP.aml" ]; then
    echo -e "${CYAN}[*] Deploying universal Snapdragon device trees to hardware tables...${NC}"
    cp "dist/acpi/SSDT-OPLC-SNAP.aml" "$EFI_OC_DIR/ACPI/"
fi

# Move custom compiled translation core kext driver files over if they exist
if [ -d "payloads/kexts/OPLC_Intel_Translation_Core.kext" ]; then
    echo -e "${CYAN}[*] Injecting compiled arm2x86 instruction kernel extension payloads...${NC}"
    cp -R "payloads/kexts/OPLC_Intel_Translation_Core.kext" "$EFI_OC_DIR/Kexts/"
fi

echo -e "\n${GREEN}[+++++] FLASH DEPLOYMENT SUCCESSFUL!${NC}"
echo -e "${GREEN}    -> OpenCore EFI workspace is fully staged at: $EFI_OC_DIR/${NC}"
echo -e "${YELLOW}[!] Safe to unmount flash drive. Safely plug into your target machine and open boot loader picker menu.${NC}"
