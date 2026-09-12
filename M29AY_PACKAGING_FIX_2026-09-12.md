# M29AY Packaging Fix — 2026-09-12

The first M29AY VPK after the Runtime64 link contained only 12 files and was about 8.1 MiB. This was a packaging regression, not an executable-size reduction.

M29AX contained ten private test assets which were absent from the restored public/source workspace: three boot-art PNGs, four selector/launcher PNGs and three converted campaign menu MP4 files.

CMake now supports `FEARVITA_PRIVATE_ASSET_ROOT`, an optional private packaging root mirroring the app0 layout (`boot_art/`, `launcher_art/`, `video_cache/`). Public/source builds remain asset-free. Private hardware-test builds can supply those files without committing them to Git.

The ten assets used for the corrected M29AY VPK were recovered from the user-provided, hardware-proven M29AX VPK and verified byte-for-byte identical.

Corrected test VPK:
- `FEARVita_M29AY_0.02_OBJECTDLL_RUNTIME_SPLASH_FULL_2026-09-12.vpk`
- size: 21,925,480 bytes
- SHA-256: `cb7c57bac4a33fb01b48d33d6f23d243cf321126c7fcbc2b34d5d7773c1a23d4`
- entries: 22
- embedded eboot.bin: 7,567,945 bytes
- embedded eboot.bin SHA-256: `681aab35c2e7b801864f1dcfc67df0c523e33890d9a615927e8c4d17e7c72e95`

For comparison M29AX:
- VPK size: 17,698,777 bytes
- eboot.bin size: 3,050,929 bytes
- eboot.bin SHA-256: `0c0583db1bac1b4710f990d8bb255e39ff1b98a52f455ecc97d00b99c7ef15bd`

The corrected M29AY VPK is larger because its Runtime64 SELF is about 4.52 MB larger while retaining all ten M29AX private menu/launcher assets.

M29AY remains not hardware validated until tested on a real Vita.