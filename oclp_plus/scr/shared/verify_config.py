"""
OPLC-Plus Configuration Verification Engine
Validates the structural and type integrity of generated OpenCore plists 
before deployment to Tier 1 target machines.
"""

import os
import plistlib
import sys

class ConfigVerifier:
    def __init__(self, file_path: str = "dist/config.plist"):
        self.file_path = file_path
        self.config_data = None

    def load_config(self) -> bool:
        """Loads and parses the compiled plist configuration file."""
        if not os.path.exists(self.file_path):
            print(f"[-] Verification Error: Target file '{self.file_path}' does not exist.")
            return False
        
        try:
            with open(self.file_path, "rb") as fp:
                self.config_data = plistlib.load(fp)
            return True
        except Exception as e:
            print(f"[-] Syntax Error: Failed parsing binary/XML formatting in plist. Error: {e}")
            return False

    def verify_rules(self) -> bool:
        """Validates critical boot structures required for macOS 27 Golden Gate stability."""
        if not self.config_data:
            return False

        passed = True
        print(f"[*] Commencing structural audit on: '{self.file_path}'")

        # 1. Audit NVRAM Target Flag Profiles
        try:
            nvram_add = self.config_data["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]
            boot_args = nvram_add.get("boot-args", "")
            csr_config = nvram_add.get("csr-active-config", [])

            print("[*] Auditing active NVRAM security and runtime parameters...")
            
            # Check for core verbose configuration loops
            if "-v" not in boot_args:
                print("    [!] Warning: Missing verbose boot flag (-v). Troubleshooting will be blind.")
            
            # Check for necessary unaccelerated fallback variables if targeting Intel Iris Pro hardware
            if "MacBookPro11,4" in str(self.config_data) and "-igfxvesa-no-egpu" not in boot_args:
                print("    [-] Error: Intel Iris Pro target lacks necessary VESA override strings.")
                passed = False
            else:
                print("    [+] Core boot-args format verified.")

            # Validate structural data formatting types for SIP configuration values
            if not isinstance(csr_config, (bytes, list)):
                print(f"    [-] Type Error: csr-active-config must be formatted as Data bytes. Found: {type(csr_config)}")
                passed = False
            else:
                print("    [+] System Integrity Protection (SIP) override formatting is valid.")

        except KeyError as e:
            print(f"    [-] Structural Error: Missing critical core NVRAM node layout. Key not found: {e}")
            passed = False

        # 2. Audit Kernel Translation and Driver Payload Nodes
        try:
            kernel_emulate = self.config_data["Kernel"]["Emulate"]
            print("[*] Auditing legacy Kernel Emulation subtrees...")
            
            if kernel_emulate.get("MinKernel", "") != "27.0.0":
                print("    [!] Warning: MinKernel version parameter is not locked explicitly to 27.0.0.")
            else:
                print("    [+] Kernel target layer correctly locked to macOS 27 Golden Gate environment.")

        except KeyError as e:
            print(f"    [-] Structural Error: Missing critical Kernel configuration node layouts. Key not found: {e}")
            passed = False

        return passed

    def execute_audit(self):
        """Runs the validation engine and triggers distinct exit parameters for CI scripts."""
        if not self.load_config():
            sys.exit(1)
            
        if self.verify_rules():
            print(f"\n${'='*40}")
            print("[++++] PASS: Configuration file integrity matches structural rules perfectly.")
            print(f"${'='*40}\n")
            sys.exit(0)
        else:
            print(f"\n${'='*40}")
            print("[-] FAIL: Core template anomalies detected. Inspect your generator scripts.")
            print(f"${'='*40}\n")
            sys.exit(1)

if __name__ == "__main__":
    verifier = ConfigVerifier()
    verifier.execute_audit()
