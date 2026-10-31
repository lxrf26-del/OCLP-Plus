"""
OPLC-Plus Legacy Mac Hardware Dictionary (2010 - 2015)
Maps vintage Intel SMBIOS profiles to CPU microarchitectures for arm2x86 translation routing.
"""

class LegacyMacDictionary:
    # 2010-2015 Target Groups mapped by SMBIOS ID
    TARGETS = {
        # --- MAC PRO (The Flagship Desktops) ---
        "MacPro5,1": {
            "marketing_name": "Mac Pro (Mid 2010 - Mid 2012)",
            "cpu_generation": "Westmere",
            "required_translation_flags": ["SSE4.2", "NO_AVX"]
        },
        "MacPro6,1": {
            "marketing_name": "Mac Pro (Late 2013 'Trash Can')",
            "cpu_generation": "Ivy Bridge-E",
            "required_translation_flags": ["AVX1", "RDRAND"]
        },

        # --- IMAC (All Screen Sizes) ---
        "iMac11,2": {"marketing_name": "iMac 21.5-inch (Mid 2010)", "cpu_generation": "Clarkdale"},
        "iMac11,3": {"marketing_name": "iMac 27-inch (Mid 2010)", "cpu_generation": "Lynnfield"},
        "iMac12,1": {"marketing_name": "iMac 21.5-inch (Mid 2011)", "cpu_generation": "Sandy Bridge"},
        "iMac12,2": {"marketing_name": "iMac 27-inch (Mid 2011)", "cpu_generation": "Sandy Bridge"},
        "iMac13,1": {"marketing_name": "iMac 21.5-inch (Late 2012)", "cpu_generation": "Ivy Bridge"},
        "iMac13,2": {"marketing_name": "iMac 27-inch (Late 2012)", "cpu_generation": "Ivy Bridge"},
        "iMac14,1": {"marketing_name": "iMac 21.5-inch (Late 2013)", "cpu_generation": "Haswell"},
        "iMac14,2": {"marketing_name": "iMac 27-inch (Late 2013)", "cpu_generation": "Haswell"},
        "iMac14,4": {"marketing_name": "iMac 21.5-inch (Mid 2014)", "cpu_generation": "Haswell"},
        "iMac15,1": {"marketing_name": "iMac 27-inch Retina 5K (Late 2014 - Mid 2015)", "cpu_generation": "Haswell"},

        # --- MACBOOK PRO (Legendary Unibody & Early Retina) ---
        "MacBookPro6,1": {"marketing_name": "MacBook Pro 17-inch (Mid 2010)", "cpu_generation": "Arrandale"},
        "MacBookPro6,2": {"marketing_name": "MacBook Pro 15-inch (Mid 2010)", "cpu_generation": "Arrandale"},
        "MacBookPro7,1": {"marketing_name": "MacBook Pro 13-inch (Mid 2010)", "cpu_generation": "Penryn"},
        "MacBookPro8,1": {"marketing_name": "MacBook Pro 13-inch (Early/Late 2011)", "cpu_generation": "Sandy Bridge"},
        "MacBookPro8,2": {"marketing_name": "MacBook Pro 15-inch (Early/Late 2011)", "cpu_generation": "Sandy Bridge"},
        "MacBookPro8,3": {"marketing_name": "MacBook Pro 17-inch (Early/Late 2011)", "cpu_generation": "Sandy Bridge"},
        "MacBookPro9,1": {"marketing_name": "MacBook Pro 15-inch (Mid 2012 Unibody)", "cpu_generation": "Ivy Bridge"},
        "MacBookPro9,2": {"marketing_name": "MacBook Pro 13-inch (Mid 2012 Unibody)", "cpu_generation": "Ivy Bridge"},
        "MacBookPro10,1": {"marketing_name": "MacBook Pro 15-inch Retina (Mid 2012 - Early 2013)", "cpu_generation": "Ivy Bridge"},
        "MacBookPro10,2": {"marketing_name": "MacBook Pro 13-inch Retina (Late 2012 - Early 2013)", "cpu_generation": "Ivy Bridge"},
        "MacBookPro11,1": {"marketing_name": "MacBook Pro 13-inch Retina (Late 2013 - Mid 2014)", "cpu_generation": "Haswell"},
        "MacBookPro11,2": {"marketing_name": "MacBook Pro 15-inch Retina (Late 2013 - Mid 2014 IG)", "cpu_generation": "Haswell"},
        "MacBookPro11,3": {"marketing_name": "MacBook Pro 15-inch Retina (Late 2013 - Mid 2014 DG)", "cpu_generation": "Haswell"},
        "MacBookPro11,4": {"marketing_name": "MacBook Pro 15-inch Retina (Mid 2015 IG)", "cpu_generation": "Haswell"},
        "MacBookPro11,5": {"marketing_name": "MacBook Pro 15-inch Retina (Mid 2015 DG)", "cpu_generation": "Haswell"},
        "MacBookPro12,1": {"marketing_name": "MacBook Pro 13-inch Retina (Early 2015)", "cpu_generation": "Broadwell"},

        # --- MACBOOK AIR ---
        "MacBookAir3,1": {"marketing_name": "MacBook Air 11-inch (Late 2010)", "cpu_generation": "Penryn"},
        "MacBookAir3,2": {"marketing_name": "MacBook Air 13-inch (Late 2010)", "cpu_generation": "Penryn"},
        "MacBookAir4,1": {"marketing_name": "MacBook Air 11-inch (Mid 2011)", "cpu_generation": "Sandy Bridge"},
        "MacBookAir4,2": {"marketing_name": "MacBook Air 13-inch (Mid 2011)", "cpu_generation": "Sandy Bridge"},
        "MacBookAir5,1": {"marketing_name": "MacBook Air 11-inch (Mid 2012)", "cpu_generation": "Ivy Bridge"},
        "MacBookAir5,2": {"marketing_name": "MacBook Air 13-inch (Mid 2012)", "cpu_generation": "Ivy Bridge"},
        "MacBookAir6,1": {"marketing_name": "MacBook Air 11-inch (Mid 2013 - Early 2014)", "cpu_generation": "Haswell"},
        "MacBookAir6,2": {"marketing_name": "MacBook Air 13-inch (Mid 2013 - Early 2014)", "cpu_generation": "Haswell"},
        "MacBookAir7,1": {"marketing_name": "MacBook Air 11-inch (Early 2015)", "cpu_generation": "Broadwell"},
        "MacBookAir7,2": {"marketing_name": "MacBook Air 13-inch (Early 2015)", "cpu_generation": "Broadwell"},

        # --- MAC MINI ---
        "MacMini4,1": {"marketing_name": "Mac Mini (Mid 2010)", "cpu_generation": "Penryn"},
        "MacMini5,1": {"marketing_name": "Mac Mini (Mid 2011 i5)", "cpu_generation": "Sandy Bridge"},
        "MacMini5,2": {"marketing_name": "Mac Mini (Mid 2011 i7)", "cpu_generation": "Sandy Bridge"},
        "MacMini6,1": {"marketing_name": "Mac Mini (Late 2012 i5)", "cpu_generation": "Ivy Bridge"},
        "MacMini6,2": {"marketing_name": "Mac Mini (Late 2012 i7)", "cpu_generation": "Ivy Bridge"},
        "MacMini7,1": {"marketing_name": "Mac Mini (Late 2014)", "cpu_generation": "Haswell"},
    }

    @classmethod
    def is_supported_legacy_model(cls, smbios_id: str) -> bool:
        """Checks if a target SMBIOS falls under Tier 1 Intel support."""
        return smbios_id in cls.TARGETS

    @classmethod
    def get_model_spec(cls, smbios_id: str) -> dict:
        """Retrieves hardware data and CPU generation flags for the backend generator."""
        return cls.TARGETS.get(smbios_id, {})
