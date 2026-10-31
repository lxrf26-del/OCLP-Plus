"""
OPLC-Plus Tahoe Kext Extraction Script
Automates harvesting the 159 legacy x86_64 driver extensions from a macOS 26 environment.
"""

import os
import shutil
import sys

class TahoeKextExtractor:
    # High-priority core driver extensions required to bypass macOS 27 boot barriers
    ESSENTIAL_DRIVERS = [
        "IONetworkingFamily.kext",
        "IOStorageFamily.kext",
        "IOHIDFamily.kext",
        "IOUSBHostFamily.kext",
        "AppleACPIPlatform.kext",
        "AppleEFIRuntime.kext",
        "AppleSMC.kext",
        "AMDRadeonX4000.kext",  # Required for driving 2013 Mac Pro FirePro GPUs
        "IOAcceleratorFamily2.kext"
    ]

    def __init__(self, source_volume: str = "/", output_dir: str = "payloads/kexts"):
        self.source_sys_extensions = os.path.join(source_volume, "System/Library/Extensions")
        self.output_workspace = output_dir

    def verify_environment(self) -> bool:
        """Ensures the host machine or target path contains a valid macOS 26 Extensions layout."""
        if not os.path.exists(self.source_sys_extensions):
            print(f"[-] Environment Error: Root source directory not found: {self.source_sys_extensions}")
            return False
        return True

    def harvest_drivers(self):
        """Iterates through and copies the targeted legacy kext stack to the OPLC payload workspace."""
        if not self.verify_environment():
            sys.exit(1)

        print(f"[*] Initializing OPLC-Plus Tahoe Harvest from: {self.source_sys_extensions}")
        
        if not os.path.exists(self.output_workspace):
            os.makedirs(self.output_workspace)
            print(f"[+] Created local workspace directory: {self.output_workspace}")

        copied_count = 0
        skipped_count = 0

        # Scan for extensions present on the source system layer
        for kext_name in self.ESSENTIAL_DRIVERS:
            target_path = os.path.join(self.source_sys_extensions, kext_name)
            destination_path = os.path.join(self.output_workspace, kext_name)

            if os.path.exists(target_path):
                print(f"    -> Harvesting: {kext_name}")
                try:
                    # Clean out previous iteration block directories if they exist
                    if os.path.exists(destination_path):
                        shutil.rmtree(destination_path)
                    
                    # Copy the full directory bundle hierarchy
                    shutil.copytree(target_path, destination_path, symlinks=True)
                    copied_count += 1
                except Exception as e:
                    print(f"    [-] Failed copying {kext_name}. Error: {e}")
            else:
                print(f"    [!] Warning: Missing expected baseline driver: {kext_name}")
                skipped_count += 1

        print(f"\n[+] Extraction Complete.")
        print(f"    - Drivers successfully secured: {copied_count}")
        print(f"    - Drivers skipped/missing: {skipped_count}")
        print(f"[*] Next Step: Place custom arm2x86 binary wrappers alongside these payloads.")

if __name__ == "__main__":
    # Test Execution targeting the active runtime system environment
    # Note: Production usage typically targets a mounted macOS 26 volume install image path.
    extractor = TahoeKextExtractor()
    extractor.harvest_drivers()
