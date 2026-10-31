# OPLC-Plus: macOS 27 Golden Gate Recovery Installer Guide

This document details the step-by-step developer procedure to prepare a bootable installation drive for Tier 1 targets (Qualcomm Snapdragon laptops or 2010–2015 Intel Macs) using OPLC-Plus.

---

## 🛠️ Phase 1: Preparing the Base Medium (All Platforms)

1. Connect a USB flash drive (minimum 32GB capacity) to your workspace computer.
2. Format the target drive using your host operating system's disk configuration utility:
   * **Name:** `OPLC_Recovery`
   * **Format Architecture:** ExFAT or FAT32 (Must use a **GUID Partition Map / GPT** layout).

---

## 💻 Phase 2: Deploying to a 2010–2015 Intel Mac (e.g., MacBookPro11,4)

### Step 2.1: Extract System Drivers
Before compiling your configuration profile, you must secure the 159 legacy driver kext stack from an active macOS 26 Tahoe host environment. Open your terminal and execute:
```bash
python3 src/target_intel/extract_tahoe_kexts.py
```

### Step 2.2: Compile the Patcher Layout
Generate your customized deployment configuration. This dynamically bakes your on-the-fly `arm2x86` assembly shims and your Intel Iris Pro display properties (`-igfxvesa-no-egpu modern_framebuffer=1`) straight into the output:
```bash
python3 src/shared/generate.py --target intel_legacy --hardware_id MacBookPro11,4
```

### Step 2.3: Stage the EFI Runtime Workspace
1. Mount the hidden EFI system partition on your target USB installation drive.
2. Create an empty directory structure matching standard OpenCore paths: `EFI/OC/`.
3. Copy your compiled configuration profile straight from your repository build folder to your drive layout:
   ```bash
   cp dist/config.plist /Volumes/EFI/EFI/OC/
   ```
4. Move your generated assembly microcode patches (`dist/translation/vector_shims_haswell.asm`) into your binary compiler path to link your project's custom `OPLC_Intel_Translation_Core.kext` driver before testing.

---

## 📱 Phase 3: Deploying to a Universal Snapdragon Laptop

### Step 3.1: Compile Emulated ACPI Firmware
Build your dual-part platform emulation table (`SSDT-OPLC-SNAP.aml`) to map the authorized Apple Silicon M5 memory controller and basic I2C HID routing lines:
```bash
# Handled automatically via GitHub Actions CI, or run locally:
iasl -sa -p dist/acpi/SSDT-OPLC-SNAP src/target_snapdragon/SSDT-OPLC-SNAP.asl
```

### Step 3.2: Build the ARM64 Configuration Template
Execute the builder script targeting your specific Qualcomm SoC family (e.g., `X1E-84-100` for premium Snapdragon X Elite configurations):
```bash
python3 src/shared/generate.py --target snapdragon --hardware_id X1E-84-100
```

### Step 3.3: Flash the Emulation Workspace
1. Copy your compiled layout file (`dist/config.plist`) to your USB drive's boot layer directory (`EFI/OC/`).
2. Move your compiled binary firmware table (`dist/acpi/SSDT-OPLC-SNAP.aml`) directly into the OpenCore ACPI payload directory: `EFI/OC/ACPI/`.

---

## ⚠️ Booting the Target System

1. Insert the prepared recovery installer into your target computer.
2. Restart the machine and access your device's native boot option menu (Hold the `Option (Alt)` key on Intel Macs; use your specific brand's BIOS override key on Snapdragon laptops).
3. Select your OpenCore EFI loader option. The custom verbose strings (`-v`) will initialize your platform logging screens, routing past early hardware check barriers down toward the basic setup interface.
