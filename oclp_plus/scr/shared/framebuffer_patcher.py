"""
OPLC-Plus Graphics Framebuffer Patching Logic
Injects device properties and stolen memory shims to ensure stable display outputs 
on unaccelerated Intel Iris Pro and Qualcomm Snapdragon architectures under macOS 27.
"""

import sys

class FramebufferPatcher:
    
    @staticmethod
    def patch_intel_iris_pro(config: dict) -> dict:
        """
        Injects VESA fallback properties and sets stolen memory sizes for Haswell Iris Pro (Crystalwell).
        This forces the macOS 27 WindowServer into a stable, unaccelerated display loop.
        """
        # Target path for the primary integrated Intel GPU device tree node
        gpu_path = "PPCI0@0/AppleACPIPCI/IGPU@2"
        
        if gpu_path not in config["DeviceProperties"]["Add"]:
            config["DeviceProperties"]["Add"][gpu_path] = {}
            
        config["DeviceProperties"]["Add"][gpu_path].update({
            # Force basic VESA compliance to stop early screen blanking
            "AAPL,slot-name": "Built-In",
            "device_type": "Display Controller",
            "model": "Intel Iris Pro 5200 (VESA Fallback)",
            
            # Injection flags to alter frame buffer sizing layouts
            "framebuffer-patch-enable": [0x01, 0x00, 0x00, 0x00],
            "framebuffer-stolenmem": [0x00, 0x00, 0x30, 0x01],   # Adjusts the DVMT Pre-Allocated limit
            "framebuffer-fbmem": [0x00, 0x00, 0x90, 0x00],       # Modifies framebuffer memory size arrays
            "disable-metal-accel": [0x01, 0x00, 0x00, 0x00]      # Prevents hardware compiler panics before v3 drops
        })
        
        return config

    @staticmethod
    def patch_snapdragon_display(config: dict, gpu_arch: str) -> dict:
        """
        Injects Qualcomm platform display bus layout overrides to allow macOS 27 
        to talk directly to standard laptop screens using raw framebuffers.
        """
        snap_gpu_path = "PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)"
        
        if snap_gpu_path not in config["DeviceProperties"]["Add"]:
            config["DeviceProperties"]["Add"][snap_gpu_path] = {}
            
        config["DeviceProperties"]["Add"][snap_gpu_path].update({
            "model": gpu_arch,
            "vendor-id": [0xAC, 0x10, 0x00, 0x00],       # Identifies as a virtualized visual interface
            "opc-gfx-shim": "AdrenoToMetalBackend",
            "framebuffer-width": [0x80, 0x07, 0x00, 0x00],   # Configures native 1920 hardware width boundaries
            "framebuffer-height": [0x38, 0x04, 0x00, 0x00],  # Configures native 1080 hardware height boundaries
            "override-no-acceleration": [0x01, 0x00, 0x00, 0x00]
        })
        
        return config
