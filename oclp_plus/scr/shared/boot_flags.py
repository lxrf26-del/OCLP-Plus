"""
OPLC-Plus Custom Boot Arguments & Flags Calculator
Programmatically generates environment runtime configurations for macOS 27 Golden Gate.
"""

from os_data import MacOSVersions

class BootFlagsCalculator:
    # Standard base troubleshooting strings
    BASE_DEBUG_FLAGS = "-v amfi=0x80 ipc_control_port_options=0"

    @classmethod
    def calculate_intel_flags(cls, cpu_generation: str) -> dict:
        """
        Computes boot arguments and SIP variables for 2010-2015 Intel architectures.
        Locks in arm2x86 core initialization variables.
        """
        args = [cls.BASE_DEBUG_FLAGS]
        
        # Append microarchitecture translation hints
        if cpu_generation in ["Westmere", "Penryn", "Arrandale", "Clarkdale"]:
            # Early Intel silicon lacking advanced modern instruction sets
            args.append("oplc_flags=0x01 translation_mode=heavy fallback=true")
        elif cpu_generation in ["Sandy Bridge", "Ivy Bridge", "Ivy Bridge-E"]:
            args.append("oplc_flags=0x03 translation_mode=standard")
        elif cpu_generation in ["Haswell", "Broadwell"]:
            # Native AVX2 vector paths accelerate the translation layer
            args.append("oplc_flags=0x07 translation_mode=fast avx2=true")
            
        # Add the legacy DriverKit runtime flag to keep HID components alive
        args.append("restore_driverkit=1")

        return {
            "boot-args": " ".join(args),
            # Completely disable System Integrity Protection (SIP) to execute custom kernel shims
            "csr-active-config": [0xEF, 0x0F, 0x00, 0x00], 
            "amfi-allow-arguments": [0x01, 0x00, 0x00, 0x00]
        }

    @classmethod
    def calculate_snapdragon_flags(cls, required_shims: list) -> dict:
        """
        Computes boot configurations targeting Qualcomm platform parameters.
        Passes memory maps and hardware overrides down to the EL2 hypervisor layers.
        """
        args = [cls.BASE_DEBUG_FLAGS, "snap_arm=1"]

        if "EL2_HYPERVISOR" in required_shims:
            args.append("el2_bypass=0 target_el2=true")
        if "SMMU_BYPASS" in required_shims:
            args.append("iommu_bypass=1")
        if "CORE_REDUCTION_SHIM" in required_shims:
            args.append("maxcpus=8 arm_thread_mask=0xFF")

        return {
            "boot-args": " ".join(args),
            # Standard developer SIP setting allowing custom hardware device trees
            "csr-active-config": [0x7F, 0x0A, 0x00, 0x00],
            "boot-screen-color": [0x00, 0x00, 0x00, 0x00] # Pure black background
        }
