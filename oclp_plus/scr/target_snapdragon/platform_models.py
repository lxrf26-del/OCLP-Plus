"""
OPLC-Plus Snapdragon Laptop Platform Dictionary
Maps Qualcomm SoCs and laptop layouts to emulation targets for macOS 27 Golden Gate.
"""

class SnapdragonPlatformDictionary:
    # Universal Snapdragon Tier 1 SoC Families
    SOC_FAMILIES = {
        # --- SNAPDRAGON X ELITE SERIES (Premium Tier) ---
        "X1E-84-100": {
            "marketing_family": "Snapdragon X Elite (12-Core Top Tier)",
            "gpu_architecture": "Adreno X1-85 (4.6 TFLOPS)",
            "required_shims": ["EL2_HYPERVISOR", "MFI_EMULATION", "SMMU_BYPASS"]
        },
        "X1E-80-100": {
            "marketing_family": "Snapdragon X Elite (12-Core Mid Tier)",
            "gpu_architecture": "Adreno X1-85 (3.8 TFLOPS)",
            "required_shims": ["EL2_HYPERVISOR", "MFI_EMULATION", "SMMU_BYPASS"]
        },
        "X1E-78-100": {
            "marketing_family": "Snapdragon X Elite (12-Core Base Tier)",
            "gpu_architecture": "Adreno X1-85 (3.8 TFLOPS)",
            "required_shims": ["EL2_HYPERVISOR", "MFI_EMULATION", "SMMU_BYPASS"]
        },

        # --- SNAPDRAGON X PLUS SERIES (Mainstream Tier) ---
        "X1P-64-100": {
            "marketing_family": "Snapdragon X Plus (10-Core)",
            "gpu_architecture": "Adreno X1-45 (3.8 TFLOPS)",
            "required_shims": ["EL2_HYPERVISOR", "MFI_EMULATION", "SMMU_PASS_THROUGH"]
        },
        "X1P-42-100": {
            "marketing_family": "Snapdragon X Plus (8-Core Entry)",
            "gpu_architecture": "Adreno X1-45 (1.7 TFLOPS)",
            "required_shims": ["EL2_HYPERVISOR", "MFI_EMULATION", "CORE_REDUCTION_SHIM"]
        },

        # --- LEGACY COMPUTE PLATFORMS (Vintage Tier) ---
        "8cx-Gen3": {
            "marketing_family": "Snapdragon 8cx Gen 3",
            "gpu_architecture": "Adreno 690",
            "required_shims": ["LEGACY_AARCH64_SHIM", "ACPI_REWRITE", "BASIC_FRAMEBUFFER"]
        },
        "8cx-Gen2": {
            "marketing_family": "Snapdragon 8cx Gen 2",
            "gpu_architecture": "Adreno 680",
            "required_shims": ["LEGACY_AARCH64_SHIM", "ARM_V8_0_FALLBACK", "BASIC_FRAMEBUFFER"]
        }
    }

    @classmethod
    def get_supported_socs(cls) -> list:
        """Returns list of all Tier 1 Snapdragon SoCs."""
        return list(cls.SOC_FAMILIES.keys())

    @classmethod
    def identify_soc_profile(cls, soc_id: str) -> dict:
        """Retrieves specific hardware profiles and required boot shims for the patcher matrix."""
        if soc_id in cls.SOC_FAMILIES:
            return cls.SOC_FAMILIES[soc_id]
        
        # Universal fallback configuration if an unlisted or custom engineering sample SoC is found
        return {
            "marketing_family": f"Generic Qualcomm Snapdragon Silicon ({soc_id})",
            "gpu_architecture": "Generic Adreno Pipeline",
            "required_shims": ["EL2_HYPERVISOR", "UNIVERSAL_DEVICE_TREE_SHIM"]
        }
