# OPLC-Plus: Boot Troubleshooting Manual

This guide helps developers identify and resolve critical halts, panics, and lockups when attempting to boot macOS 27 Golden Gate using the OPLC-Plus framework.

---

## 💻 1. Intel Mac Diagnostics (e.g., MacBookPro11,4)

### 🚨 Symptom: Immediate Kernel Panic (Early Handoff Halt)
* **The Screen Shows:** A localized cascade of text strings rapidly printing, culminating in a `panic(cpu 0 caller...): "Incompatible architecture"` or a sudden reboot.
* **The Cause:** The `arm2x86_core` engine generated instruction translation vectors matching a different CPU profile than the physical silicon present on the board.
* **The Fix:** Ensure your model string matches your exact hardware configuration. Re-verify using `sysctl hw.model` and run the generator script using the precise ID:
  ```bash
  ./build.sh --clean
  ./build.sh --intel MacBookPro11,4
  ```

### 🚨 Symptom: The "Black Screen" Lockup (No Display Output)
* **The Screen Shows:** The chime plays, the keyboard backlight activates, but the panel remains pitch black or the backlight dims completely after the initial Apple logo disappears.
* **The Cause:** `WindowServer` failed to load because macOS 27 natively lacks Intel Iris graphics drivers. 
* **The Fix:** Force unaccelerated VESA safe-mode parameters to prevent premature hardware display controller scaling. Open your compiled `dist/config.plist` and confirm that the following boot arguments are present:
  ```text
  -igfxvesa-no-egpu modern_framebuffer=1
  ```

### 🚨 Symptom: Immediate Freeze or Loop at the Login Screen
* **The Screen Shows:** The interface loads successfully (wallpaper, user icons, password entry field appear), but typing the password and pressing Enter freezes the mouse or loops back to the same screen.
* **The Cause:** The security session handover failed. The `OpenDirectory` or crypto subsystems are looking for an Apple Silicon Secure Enclave framework layout instead of your Intel CPU architecture.
* **The Fix:** Ensure your `OPLC_Intel_Translation_Core.kext` driver successfully compiled and placed into the OpenCore layout tree. This kext contains the necessary `restore_driverkit=1` handoff shims to bypass early token verification loops.

---

## 📱 2. Qualcomm Snapdragon Laptop Diagnostics

### 🚨 Symptom: The OpenCore Loader Fails to Boot (Instant Halt)
* **The Screen Shows:** A generic Windows on ARM firmware error or an immediate drop back into the laptop's UEFI/BIOS interface selection options.
* **The Cause:** The firmware interface does not recognize the standard Apple boot files, or your ACPI tables failed to report an ARM-compatible system topology.
* **The Fix:** Ensure that your unified platform emulation table successfully compiled using `iasl`. Verify that the output binary file is named exactly `SSDT-OPLC-SNAP.aml` and resides directly inside your boot drive path:
  ```text
  EFI/OC/ACPI/SSDT-OPLC-SNAP.aml
  ```

### 🚨 Symptom: Heavy Graphic Stuttering / Sluggish Input Tracking
* **The Screen Shows:** The desktop environment interface renders (e.g., the Dock draws successfully), but window dragging trails severely and animations run at less than 5 frames per second.
* **The Cause:** This is expected behavior for initial Phase 1 development blocks. True Metal-to-Adreno hardware acceleration hooks are still missing, bounding all UI tasks to a software-rendered frame buffer structure.
* **The Fix:** No current software settings can resolve this limitation locally. Await the public integration of upcoming v3 translation pipelines optimized for direct native GPU vector mapping loops.

---

## 🔍 3. Collecting Debug Logs for Bug Reports

If your machine encounters a freeze or a panic not covered in this documentation:
1. Boot the target drive using your testing medium.
2. Execute the unified log collection utility tool directly inside your project path:
   ```bash
   ./build.sh --report
   ```
3. Attach the output JSON report found inside your `dist/logs/` path to your repository issue tracker to assist development optimization workflows.
