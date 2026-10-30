# OPLC-Plus (Dual-Architecture macOS 27 Project)

OPLC-Plus is an experimental, developer-focused fork targeting **macOS 27 Golden Gate** compatibility across two highly unconventional platforms: Legacy Intel Macs and modern Qualcomm Snapdragon ARM laptops. 

By combining binary instruction translation for x86_64 and low-level platform firmware emulation for Qualcomm ARM64, this project bypasses Apple Silicon hardware exclusivity.

---

## 📊 Development Status & Roadmap

Because these platforms use completely different hardware paradigms, progress is tracked across two distinct engineering branches:

### 💻 1. Intel Mac Support (The Translation Branch)
Utilizes low-level binary instruction translation to force the pure ARM64 macOS 27 kernel to run on legacy x86_64 Intel processors.
* **Status:** Proof of concept achieved on genuine hardware (e.g., 2013 Mac Pro "Trash Can").
* **Current Core Targets:**
  - [x] **Kernel Initialization:** Spawning a functional `Darwin 27.0.0 x86_64` environment.
  - [x] **Driver Injection:** Successfully mounting a 159-kext stack using macOS 26 Tahoe drivers.
  - [x] **DriverKit Runtime:** Restoring the missing x86_64 `io user server` runtime for stable HID interaction.
  - [x] **Basic WindowServer:** Renders the login window, wallpaper, and user icons.
  - [ ] **Password Handoff:** *Current Roadblock.* Fixing the crypto/Secure Enclave token handoff on x86 CPUs to allow full desktop login.

### 📱 2. Snapdragon ARM Support (The Platform Emulation Branch)
Bridges the architectural gap between Qualcomm's Snapdragon X-Series platforms and Apple Silicon's proprietary device tree/firmware environments using EL2 hypervisor and custom ACPI shims.
* **Status:** Highly experimental. Interface elements successfully drawing.
* **Current Core Targets:**
  - [x] **Basic I/O:** Functioning laptop keyboard and trackpad routing.
  - [x] **UI Draw:** Renders basic elements like the system Dock and desktop framebuffers.
  - [ ] **Graphics Acceleration:** *Current Roadblock.* Mapping macOS's Metal graphics API to Qualcomm Adreno GPUs to enable fluid UI animations.
  - [ ] **Power Management:** Implementing stable ACPI tables for system sleep, wake, and battery scaling.

---

## 📂 Repository Layout

```text
OPLC-Plus/
├── src/
│   ├── target_intel/           # --- INTEL MAC MODULES ---
│   │   ├── arm2x86_core/       # Intercepts ARM64 kernel instructions for x86_64 execution
│   │   ├── tahoe_kext_bridge/  # Scripts to inject the 159-kext stack from macOS 26
│   │   └── driverkit_runtime/  # Reconstructs the deleted x86_64 DriverKit/HID runtime
│   │
│   ├── target_snapdragon/      # --- SNAPDRAGON MODULES ---
│   │   ├── platform_emulation/ # Device trees and ACPI shims for Qualcomm X-Series firmware
│   │   ├── adreno_framebuffer/ # Initial UI rendering and early Metal-to-Adreno hooks
│   │   └── qualcomm_hid/       # Keyboard and trackpad I/O routing for laptop hardware
│   │
│   └── shared/                 # Common OpenCore configuration wrappers
├── templates/                  # Base config.plist layouts
│   ├── intel_mac/              # Profiles targeting real hardware (e.g., MacPro7,1, MacPro6,1)
│   └── snapdragon_arm/         # Experimental profiles spoofing Apple Silicon identities
└── README.md                   # Project documentation
```

---

## 🛠️ Getting Started for Contributors

### Prerequisites
* A copy of the macOS 26 (Tahoe) full installer (for extracting the x86_64 legacy driver kext stack).
* A cross-compilation toolchain capable of targeting both `x86_64` and `aarch64`.

### Building the Project Templates
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd OPLC-Plus
   ```
2. Run the template configuration generator targeting your hardware architecture:
   ```bash
   # For Intel Mac targets
   python3 src/shared/generate.py --target intel --smbios MacPro7,1

   # For Snapdragon targets
   python3 src/shared/generate.py --target snapdragon
   ```

---

## ⚠️ Disclaimer
This is a highly experimental developer ecosystem. It does not provide plug-and-play, end-user EFI folders or installation images. Modifying operating system kernels can lead to permanent data loss or unbootable hardware states. Proceed with caution.
