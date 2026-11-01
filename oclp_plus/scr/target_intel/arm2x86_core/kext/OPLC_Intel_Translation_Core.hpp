/**
 * OPLC_Intel_Translation_Core.hpp
 * OPLC-Plus Project Kernel-Extension Framework
 * 
 * Target Architecture: Legacy Intel x86_64 (Haswell/Broadwell Vector Environments)
 * Purpose: Low-level I/O Kit runtime driver mapping the arm2x86 instruction conversion matrices.
 */

#ifndef OPLC_INTEL_TRANSLATION_CORE_HPP
#define OPLC_INTEL_TRANSLATION_CORE_HPP

#include <IOKit/IOService.h>

class OPLC_Intel_Translation_Core : public IOService {
    OSDeclareDefaultStructors(OPLC_Intel_Translation_Core)

public:
    /**
     * Standard I/O Kit lifecycle overrides to handle core initialization.
     */
    virtual bool init(OSDictionary *dictionary = nullptr) override;
    virtual void free() override;
    virtual IOService *probe(IOService *provider, SInt32 *score) override;
    virtual bool start(IOService *provider) override;
    virtual void stop(IOService *provider) override;

protected:
    /**
     * Internal runtime properties managing instruction translation parameters.
     */
    uint32_t activeTranslationFlags;
    bool     hasNativeAVX2Acceleration;

    /**
     * Initializes hardware-specific vector shims based on detected host CPU features.
     */
    virtual bool initializeInstructionTranslationPipeline();
    
    /**
     * Bypasses the missing macOS 27 legacy x86_64 DriverKit dependencies 
     * to keep local Human Interface Devices (HID UserServer instances) operational.
     */
    virtual void forceDriverKitRuntimeHandoff();
};

#endif // OPLC_INTEL_TRANSLATION_CORE_HPP
