"""
OPLC-Plus & BridgePatcher-GoldenGate Unified Log Collection Utility
Gathers native system hardware metrics, active boot configurations, and driver topologies 
to assist in scaling out macOS 27 Golden Gate compatibility profiles.
"""

import os
import platform
import subprocess
import json
from datetime import datetime

class OPLCLogCollector:
    def __init__(self, output_dir: str = "dist/logs"):
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_data = {
            "collection_time": datetime.now().isoformat(),
            "patcher_framework": "OPLC-Plus / BridgePatcher-GoldenGate Branch",
            "host_os": {},
            "hardware_specs": {},
            "boot_configuration": {}
        }

    def _run_cmd(self, args: list) -> str:
        """Helper to cleanly execute shell calls and trap exceptions."""
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            return "UNAVAILABLE"

    def gather_os_metrics(self):
        """Extracts running kernel properties and Darwin version strings."""
        print("[*] Harvesting operating system properties...")
        self.log_data["host_os"] = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine()
        }

    def gather_hardware_specs(self):
        """Queries local hardware parameters and processor architectures."""
        print("[*] Querying local hardware silicon layouts...")
        
        if platform.system() == "Darwin":
            # Native Mac Hardware Parsing Pipeline
            self.log_data["hardware_specs"] = {
                "smbios_id": self._run_cmd(["sysctl", "-n", "hw.model"]),
                "cpu_brand": self._run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"]),
                "cpu_cores": self._run_cmd(["sysctl", "-n", "hw.ncpu"]),
                "physical_memory": self._run_cmd(["sysctl", "-n", "hw.memsize"]),
                "secure_chip": self._check_apple_secure_chip()
            }
        else:
            # Generic/Cross-Platform Baseline Parsing Pipeline (e.g. Snapdragon Linux environments)
            self.log_data["hardware_specs"] = {
                "smbios_id": "NON_APPLE_ARM_OR_X86",
                "cpu_brand": platform.processor() or "Qualcomm / Intel Target",
                "cpu_cores": os.cpu_count(),
                "secure_chip": "NONE"
            }

    def _check_apple_secure_chip(self) -> str:
        """Determines if the Mac board contains a T1 or T2 security engine."""
        ioreg_data = self._run_cmd(["ioreg", "-p", "IODeviceTree", "-r", "-n", "apple-chip-id"])
        if "apple-chip-id" in ioreg_data:
            if "0x8012" in ioreg_data:
                return "T2 (Secure Enclave)"
            elif "0x8002" in ioreg_data:
                return "T1 (Touch Bar)"
        return "NONE_INTEL_LEGACY"

    def gather_boot_configuration(self):
        """Secures NVRAM variable entries and custom active boot arguments."""
        print("[*] Sampling NVRAM active environment flags...")
        if platform.system() == "Darwin":
            self.log_data["boot_configuration"] = {
                "active_boot_args": self._run_cmd(["sysctl", "-n", "kern.bootargs"]),
                "sip_status": self._run_cmd(["csrutil", "status"])
            }
        else:
            self.log_data["boot_configuration"] = {
                "active_boot_args": "RUNNING_OUTSIDE_DARWIN_KERNEL"
            }

    def export_report(self):
        """Compiles the report payload into a highly readable JSON tracking layout."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        model_slug = self.log_data["hardware_specs"].get("smbios_id", "generic").replace(",", "_")
        filename = f"OPLC_Log_{model_slug}_{self.timestamp}.json"
        target_dest = os.path.join(self.output_dir, filename)

        with open(target_dest, "w") as fp:
            json.dump(self.log_data, fp, indent=4)

        print(f"\n[+] System Profile Log Compiled Successfully!")
        print(f"    -> Destination Tracked At: '{target_dest}'")
        print(f"[!] Share this json dump inside the patcher issue tracker to assist our v3 scaling matrix.")

if __name__ == "__main__":
    collector = OPLCLogCollector()
    collector.gather_os_metrics()
    collector.gather_hardware_specs()
    collector.gather_boot_configuration()
    collector.export_report()
