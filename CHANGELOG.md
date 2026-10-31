# Changelog

All notable changes to the **OPLC-Plus** project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org).

---

## [0.1.0-Beta.1] - 2026-10-31

### 🚀 Added
* **macOS 27 Registration:** Introduced core OS identifiers, hex strings (`0x001B0000`), and Darwin 27.x.x matching rules to register the *Golden Gate* ecosystem inside the patcher architecture.
* **Tier 1 Intel Mac Target Matrix:** Added dictionary mapping structures tracking vintage hardware profiles from 2010 to 2015 (Westmere through Broadwell architectures, including the classic `MacPro6,1` "Trash Can").
* **Universal Snapdragon SoC Platform Maps:** Integrated a universal hardware decoder identifying Qualcomm X-Elite, X-Plus, and legacy compute platforms (8cx Gen 2/3) to coordinate the ARM-to-ARM boot pipelines.
* **Dynamic Boilerplate Config Generator:** Built Python script automation executing structural OpenCore layout pipelines, producing baseline `config.plist` skeletons dynamically customized by architecture.
* **Programmatic Boot-Args Calculator:** Implemented localized boot configuration calculations targeting structural flags (`translation_mode`, `restore_driverkit`, `el2_bypass`, `iommu_bypass`) matching hardware specific profiles.
* **Unified Snapdragon Emulation Firmware:** Drafted and integrated `SSDT-OPLC-SNAP.asl`, introducing a dual-part spoof mapping an authorized Apple Silicon M5 memory controller and basic I2C HID routing blocks.
* **Tahoe Patch Harvester:** Added an automated extraction module tracking down and harvesting the baseline 159 legacy driver kext stack straight from mounted macOS 26 environments.
* **Automated CI/CD Pipeline:** Configured a global GitHub Actions workflow validating core Python code and auto-compiling ASL blocks using the Intel ACPI compiler suite (`iasl`) with every commit.

### 🔄 Changed
* **Patcher Execution Guard:** Overrode mainline OpenCore Legacy Patcher protection routines to intentionally permit configuration generation blocks for unsupported non-Apple ARM and legacy Intel x86 silicon.

### 🛑 Fixed
* Fixed a syntax collision inside the unified `SSDT-OPLC-SNAP.asl` script block by containing the system bus scope inside a singular consolidated `DefinitionBlock`.

### ⚠️ Current Known Roadblocks (Work in Progress)
* **Intel Mac:** The security session handover is currently failing; crypto token mappings expecting Apple Silicon Secure Enclave architecture drop connection cycles on raw x86 CPUs before full desktop environment registration.
* **Snapdragon Laptop:** Native Metal graphics engine acceleration maps are completely unaccelerated; fluid user interface rendering layers are currently constrained to a basic software frame buffer framework.

---

## [0.0.1-Alpha] - 2026-10-30

### 📝 Initial Conceptual Release
* Initial repository branch layout established.
* Project scope declared targeting macOS 27 compatibility loops for legacy Intel hardware platforms and Windows on ARM devices.
