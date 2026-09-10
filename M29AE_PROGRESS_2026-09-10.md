# FEARVita M29AE / public 0.02 — 2026-09-10

The exact retail `Menu.bik` exported by M29AD was received and decoded successfully. Properties: BIKi, 512x512, 420 frames, 30 fps, 14 seconds, no embedded audio. This matches the runtime parser and confirms that F.E.A.R. supplies menu music separately.

The M29AD hardware log proves the HQ music path is active and that SceAvPlayer fails at initialization (`-2123091296`) before `sceAvPlayerAddSource`.

## M29AE implementation

- AvPlayer texture callback now uses physically contiguous user-main memory (`SCE_KERNEL_MEMBLOCK_TYPE_USER_MAIN_PHYCONT_NC_RW`).
- Decoded-frame allocations are rounded/aligned to at least 1 MiB and mapped with GXM RW access.
- Added allocation/base/map diagnostics.
- AvPlayer base priority is `0xA0`; output frame buffers are 5.
- Added private packaged-cache fallback `app0:cache/Menu.mp4` after the normal writable cache.
- Retained raw Bink direct probe only as a diagnostic fallback.
- Generated a private video-only H.264 constrained-baseline/yuv420p cache from the user's own Bink. That cache is not committed.

## Build status

The Vita build completed through ARM ELF -> VELF -> SAFE SELF -> VPK with the supplied VitaSDK/toolchain packages.

## Next hardware criterion

Success is `bink-avplayer add-source result=0` followed by `bink-avplayer first-frame`, with the animated F.E.A.R. menu background visibly rendered behind the retail controls.
