 #!/bin/bash

# OPLC-Plus Automated Generation Tool
# Orchestrates firmware compilation, legacy driver harvesting, and config boilerplate assembly.

set -e # Terminate script immediately if any individual build command encounters an error

# Text color definitions for crisp terminal formatting
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

show_usage() {
    echo -e "${YELLOW}OPLC-Plus Unified Builder Pipeline Utilities${NC}"
    echo -e "Usage: $0 [options]"
    echo ""
    echo -e "Options:"
    echo -e "  --intel <smbios>       Compile an Intel profile layout (e.g., MacBookPro11,4, MacPro6,1)"
    echo -e "  --snapdragon <soc>     Compile a Snapdragon platform layout (e.g., X1E-84-100, X1P-64-100)"
    echo -e "  --clean                Wipe previous compilation assets inside the /dist and /payloads workspaces"
    echo -e "  --help                 Display this layout roadmap menu"
    echo ""
}

clean_workspace() {
    echo -e "${CYAN}[*] Flushing previous build work trees...${NC}"
    rm -rf dist/
    rm -rf payloads/
    echo -e "${GREEN}[+] Workspaces successfully normalized.${NC}"
}

compile_acpi_firmware() {
    echo -e "${CYAN}[*] Locating ACPI Compiler Suite (iasl)...${NC}"
    if ! command -v iasl &> /dev/null; then
        echo -e "${RED}[- ] Configuration Error: 'iasl' binary could not be found.${NC}"
        echo -e "${YELLOW}Please install the Intel ACPI tools (e.g., 'brew install iasl' or 'sudo apt install iasl')${NC}"
        exit 1
    fi
    echo -e "${GREEN}[+] Compiler verified. Building Qualcomm Hardware Table...${NC}"
    mkdir -p dist/acpi
    iasl -sa -p dist/acpi/SSDT-OPLC-SNAP src/target_snapdragon/SSDT-OPLC-SNAP.asl
    echo -e "${GREEN}[+] Firmware successfully compiled to: dist/acpi/SSDT-OPLC-SNAP.aml${NC}"
}

# Ensure at least one argument was passed down to the shell hook
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

# Multi-flag command router loop parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            clean_workspace
            shift
            exit 0
            ;;
                --intel)
            if [ -z "$2" ]; then
                echo -e "${RED}[- ] Error: --intel flag requires an active SMBIOS identifier target.${NC}"
                exit 1
            fi
            TARGET_ID="$2"
            
            echo -e "${CYAN}[*] Starting OPLC-Plus Intel Pipeline compilation matrix...${NC}"
            
            # Step 1: Run driver harvest routine
            python3 src/target_intel/extract_tahoe_kexts.py
            
            # --- NEW: Step 2: Compile the low-level C++ driver engine via Makefile ---
            echo -e "${CYAN}[*] Compiling custom translation core kernel driver...${NC}"
            make -C src/target_intel/arm2x86_core/kext clean all install
            
            # Step 3: Compile the OpenCore layout template and microcode tables
            python3 src/shared/generate.py --target intel_legacy --hardware_id "$TARGET_ID"
            
            # Step 4: Run audit check
            python3 src/shared/verify_config.py
            
            echo -e "${GREEN}[+++] Phase 1 deployment build finalized successfully inside /dist workspace.${NC}"
            shift 2
            exit 0
            ;;

        --snapdragon)
            TARGET_SOC="${2:-X1E-80-100}" # Fallback to mid-tier standard model identifier if empty
            
            echo -e "${CYAN}[*] Starting OPLC-Plus Qualcomm ARM Pipeline compilation matrix...${NC}"
            
            # Step 1: Execute firmware assembly blocks
            compile_acpi_firmware
            
            # Step 2: Generate config maps
            python3 src/shared/generate.py --target snapdragon --hardware_id "$TARGET_SOC"
            
            echo -e "${GREEN}[+++] Phase 1 deployment build finalized successfully inside /dist workspace.${NC}"
            shift 2
            exit 0
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}[-] Unknown execution parameter option flag: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
# Add this code selection flag directly inside the main case routing blocks in /build.sh
        --app)
            echo -e "${CYAN}[*] Starting OPLC-Plus Native macOS Application Bundle Build...${NC}"
            
            APP_NAME="OPLC-Plus.app"
            BUILD_DIR="dist/$APP_NAME"
            CONTENTS_DIR="$BUILD_DIR/Contents"
            
            # Step 1: Wipe clean any old workspace files
            rm -rf "$BUILD_DIR"
            mkdir -p "$CONTENTS_DIR/MacOS"
            mkdir -p "$CONTENTS_DIR/Resources/src"
            
            # Step 2: Ensure your core driver extensions compile cleanly into your payloads tracking paths
            if [ -f "src/target_intel/arm2x86_core/kext/Makefile" ]; then
                echo -e "${CYAN}[*] Bundling binary kernel extension modules...${NC}"
                make -C src/target_intel/arm2x86_core/kext clean all install
            fi
            
            # Step 3: Copy over your complete Python script logic framework to act as internal App resources
            cp -R src/ "$CONTENTS_DIR/Resources/src/"
            if [ -d "payloads" ]; then
                cp -R payloads/ "$CONTENTS_DIR/Resources/payloads/"
            fi
            
            # Step 4: Inject metadata assets and the launching code
            cp src/shared/app_assets/Info.plist "$CONTENTS_DIR/"
            cp src/shared/app_assets/launcher.sh "$CONTENTS_DIR/MacOS/OPLC-Plus"
            chmod +x "$CONTENTS_DIR/MacOS/OPLC-Plus"
            
            # Step 5: Pull down the official BridgePatcher logo icon payload straight into the app resource path
            echo -e "${CYAN}[*] Pulling down canonical AppIcon asset dependencies...${NC}"
            curl -s -o "$CONTENTS_DIR/Resources/AppIcon.icns" "https://githubusercontent.com" || true
            
            # Step 6: Compress the application into a distribution-ready zip file for your GitHub Release page
            echo -e "${CYAN}[*] Packaging application archive for GitHub Release page deployment...${NC}"
            cd dist
            zip -r "../OPLC-Plus-v0.1.0-Beta-Release.zip" "$APP_NAME" > /dev/null
            cd ..
            
            echo -e "${GREEN}[+++++] APP BUILD COMPLETE! Release archive generated at: ./OPLC-Plus-v0.1.0-Beta-Release.zip${NC}"
            exit 0
            ;;
