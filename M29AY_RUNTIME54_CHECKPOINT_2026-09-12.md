# FEARVita M29AY — Runtime54 checkpoint — 2026-09-12

Backup-first checkpoint after expanding the real public LithTech server/runtime closure.

## Verified local archives
- `FEARVita_M29AY_SOURCE_RUNTIME54_2026-09-12.zip` — SHA-256 `59d07abf29e6a0fd89eaff97c1e77546683b121db9fc2e67881470945317a186`
- `FEARVita_M29AY_WORKSPACE_RUNTIME54_2026-09-12.zip` — SHA-256 `f00e8e2897050cf32026bcf60751aa826bc2c872032050f7c1cf2460aeb4e3f1`
- Both passed full `unzip -t` integrity checks.

## Runtime state
The expanded `fearvita_runtime_server_objects` target now compiles cleanly for ARM/Vita with the linker-proven world/model/collision/network/server pieces included. Newly closed portability seams include:
- Win32-free `TransformMaker` and server world source guards.
- Conservative `FLAG2_USEMODELOBBS=0` compatibility because that Jupiter-EX opt-in flag is absent from the public LithTech/FEAR source snapshot and no source here can set a reliable non-conflicting bit.
- Portable WinMM waveform structs for `wave.cpp` on Vita.
- Real `CLTServer::Timer()` backed by FEARVita's existing `ILTTimer` implementation.
- Server-side SFX message reads use `CLTMessage_Read_Server` rather than instantiating the abstract shared message base.
- FEAR templated `LTObjRef` is linked into the old runtime reference list through the already-established binary-layout adapter.
- Static ObjectDLL loading is performed inside `classmgr.cpp` via the real ClassBind path, avoiding a host DLL loader.
- Old `df_*` file-tree operations continue to map onto the mounted FEARVita retail VFS.

No VPK has been created. M29AX remains the last hardware-proven build; M29AY is not hardware validated.

## Recovery payload
Delta against the prior verified 2026-09-12 source backup:
- raw patch: 16,344 bytes
- raw SHA-256: `8e3258fb15050cac6b3aae7b420efb5e0c8bfa3fcb2705993ef318390cf9d436`
- XZ SHA-256: `b8a45922dff7543a141f0f057197fafdf6b4367f5cfa272076ace92325302449`
- base64 SHA-256: `75827f5cffe530ada422cbe4b1917b7766f97c4192269ac9cf4b64d9720f83d6`
- payload: `patches/recovered/M29AY_RUNTIME54_DELTA_2026-09-12.patch.xz.b64.part00`

Next step: run the full `FEARVita` link and add only linker-proven real runtime/world translation units or platform seams. Continue through ELF -> VELF -> SELF/`eboot.bin`, then stop before VPK packaging.
