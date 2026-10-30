# OPLC-Plus (Dual-Architecture macOS 27 Project)

OPLC-Plus is an experimental, developer-focused fork targeting **macOS 27 Golden Gate** compatibility. By combining binary instruction translation for x86_64 and low-level platform firmware emulation for Qualcomm ARM64, this project bypasses Apple Silicon hardware exclusivity.

---

## 🚀 Tier 1 Release Strategy (Launch Targets)

To ensure maximum impact and optimization, development is actively prioritized for two specific categories of hardware before scaling out to broader PC and late-model Mac architectures:

1. **All Qualcomm Snapdragon Laptops:** Universal architecture shims targeting Snapdragon X-Elite, X-Plus, and preceding compute platforms to establish a reliable ARM-to-ARM boot pipeline.
2. **2010 to 2015 Intel Macs:** Broad compatibility support mapping legacy Intel core architectures (such as Westmere, Sandy Bridge, Ivy Bridge, Haswell, and Broadwell) directly to the `arm2x86` translation layer.

---

## 📊 Development Status & Roadmap

Because our Phase 1 platforms use completely different hardware paradigms, progress is tracked across two distinct engineering branches:

### 💻 1. Intel Mac Support (2010–2015 Legacy Branch)
Utilizes low-level binary instruction translation to force the pure ARM64 macOS 27 kernel to run on legacy x86_64 Intel processors.
* **Status:** Proof of concept achieved on 2013 hardware (MacPro6,1). Legacy CPU instruction mapping underway.
* **Current Core Targets:**
  - [x] **Kernel Initialization:** Spawning a functional `Darwin 27.0.0 x86_64` environment.
  - [x] **Driver Injection:** Successfully mounting a 159-kext stack using macOS 26 Tahoe drivers.
  - [x] **DriverKit Runtime:** Restoring the missing x86_64 `io user server` runtime for stable HID interaction.
  - [x] **Basic WindowServer:** Renders the login window, wallpaper, and user icons.
  - [ ] **Password Handoff:** *Current Roadblock.* Fixing the crypto/Secure Enclave token handoff on x86 CPUs to allow full desktop login.

### 📱 2. Snapdragon Laptop Support (Universal ARM Branch)
Bridges the architectural gap between Qualcomm's Snapdragon laptop platforms and Apple Silicon's proprietary device tree/firmware environments using EL2 hypervisor layers and custom ACPI shims.
* **Status:** Experimental. Universal interface elements successfully drawing.
* **Current Core Targets:**
  - [x] **Basic I/O:** Functioning laptop keyboard and trackpad routing across multiple brands.
  - [x] **UI Draw:** Renders basic elements like the system green-room Dock and desktop framebuffers.
  - [ ] **Graphics Acceleration:** *Current Roadblock.* Mapping macOS's Metal graphics API to Qualcomm Adreno GPUs to enable fluid UI animations.
  - [ ] **Power Management:** Implementing stable ACPI tables for system sleep, wake, and laptop battery scaling.

---

## 📂 Repository Layout

```text
OPLC-Plus/
├── src/
│   ├── target_intel/           # --- 2010-2015 MAC MODULES ---
│   │   ├── arm2x86_core/       # Intercepts ARM64 kernel instructions for x86_64 execution
│   │   ├── tahoe_kext_bridge/  # Scripts to inject the 159-kext stack from macOS 26
│   │   └── driverkit_runtime/  # Reconstructs the deleted x86_64 DriverKit/HID runtime
│   │
│   ├── target_snapdragon/      # --- UNIVERSAL LAPTOP MODULES ---
│   │   ├── platform_emulation/ # Device trees and ACPI shims for Qualcomm X-Series firmware
│   │   ├── adreno_framebuffer/ # Initial UI rendering and early Metal-to-Adreno hooks
│   │   └── qualcomm_hid/       # Keyboard and trackpad I/O routing for laptop hardware
│   │
│   └── shared/                 # Common OpenCore configuration wrappers
├── templates/                  # Base config.plist layouts
│   ├── intel_mac_2010_2015/    # SMBIOS targeting vintage Intel hardware tables
│   └── snapdragon_arm/         # Experimental profiles spoofing Apple Silicon identities
└── README.md                   # Project documentation
```

---

## 🛠️ Getting Started for Contributors

### Prerequisites
* A copy of the macOS 26 (Tahoe) full installer (for legacy x86_64 kext asset extraction).
* A cross-compilation toolchain capable of targeting both `x86_64` and `aarch64`.

### Building the Project Templates
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd OPLC-Plus
   ```
2. Run the template configuration generator targeting your hardware architecture:
   ```bash
   # For 2010-2015 Intel Mac targets
   python3 src/shared/generate.py --target intel --generation legacy

   # For Snapdragon Laptop targets
   python3 src/shared/generate.py --target snapdragon
   ```

---

## ⚠️ Disclaimer
This is a highly experimental developer ecosystem. It does not provide plug-and-play, end-user EFI folders or installation images. Modifying operating system kernels can lead to permanent data loss or unbootable hardware states. Proceed with caution.
