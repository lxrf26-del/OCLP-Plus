# ==========================================
# OPLC-Plus Kernel Extension Builder Makefile
# Targets: macOS 27 Golden Gate (x86_64 Core Runtime)
# ==========================================

# Toolchain definitions
CC       = clang++
STRIP    = strip
MKDIR    = mkdir -p
CP       = cp -R
RM       = rm -rf

# Compilation and Linker Flags optimized for Darwin kernel space
CFLAGS   = -Wall -Wextra -std=c++14 -nostdinc -nostdlibinc \
           -fno-builtin -fno-common -fno-exceptions -fno-rtti \
           -fno-asynchronous-unwind-tables -mkernel -m64 -O2 \
           -Xarch_x86_64 -mno-mmx -Xarch_x86_64 -mno-sse \
           -DKERNEL -DCONFIG_KPI_VERSION="27.0.0"

INC      = -I. \
           -I/System/Library/Frameworks/Kernel.framework/Headers \
           -I/System/Library/Frameworks/Kernel.framework/Headers/bsd

LDFLAGS  = -nostdlib -Xlinker -kext -mkernel -Xlinker -object_path_lto \
           -Xlinker /tmp/OPLC_Intel_Translation_Core.lto \
           -lkmod -lcc_kext

# Output naming frameworks
KEXT_NAME   = OPLC_Intel_Translation_Core
BUNDLE_DIR  = $(KEXT_NAME).kext
CONTENTS    = $(BUNDLE_DIR)/Contents
MACOS_DIR   = $(CONTENTS)/MacOS

# Source and Object targeting
SRCS        = OPLC_Intel_Translation_Core.cpp
OBJS        = $(SRCS:.cpp=.o)

.PHONY: all clean install

all: $(BUNDLE_DIR)

# Compiles source files down to flat raw objects
%.o: %.cpp
	@echo "[*] Compiling C++ Kernel Source: $<"
	$(CC) $(CFLAGS) $(INC) -c $< -o $@

# Links binary objects and assembles the official Apple directory bundle layout
$(BUNDLE_DIR): $(OBJS)
	@echo "[*] Linking final runtime Mach-O kext binary..."
	$(MKDIR) $(MACOS_DIR)
	$(CC) $(LDFLAGS) $(OBJS) -o $(MACOS_DIR)/$(KEXT_NAME)
	@echo "[*] Stripping symbols to optimize payload size..."
	$(STRIP) -x $(MACOS_DIR)/$(KEXT_NAME)
	@echo "[*] Injecting XML layout metadata properties..."
	$(CP) Info.plist $(CONTENTS)/Info.plist
	@echo "[++++] Kext Bundle Build Success: $(BUNDLE_DIR)"

clean:
	@echo "[*] Purging object workspaces..."
	$(RM) $(OBJS) $(BUNDLE_DIR)
	@echo "[+] Workspace sanitized completely."

install: all
	@echo "[*] Staging compiled driver payload for distribution templates..."
	$(MKDIR) ../../../../../payloads/kexts
	$(CP) $(BUNDLE_DIR) ../../../../../payloads/kexts/
	@echo "[+] Driver bundle safely staged in repository distribution paths."
