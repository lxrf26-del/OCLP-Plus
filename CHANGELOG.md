# Changelog

All notable changes to the **OPLC-Plus** project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org).

---

## [0.2.0-Alpha.2] - 2026-11-01

### 🚀 Added
* **Bare-Metal Performance Alignment:** Optimized `arm2x86_core` routing modules following upstream verification of full-speed bare-metal execution matching Apple Silicon M4 performance metrics.
* **Log Gathering Framework:** Staged internal pipeline frameworks to accept and parse incoming community hardware boot logs to broaden initial deployment support.

### 🔄 Changed
* **Release Timeline Calibration:** Shifted the launch target window to align with the upcoming v3 deployment schedule (estimated 1–2 weeks).


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
