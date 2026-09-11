# FEARVita M29AY continuation — full executable/runtime bridge

Date: 2026-09-11

This continuation starts from the rescued canonical M29AY workspace. M29AX remains the last hardware-proven VPK. No new hardware validation is claimed here.

## Progress in this continuation

- Rebuilt the VitaSDK/toolchain from the preserved packages and resumed the rescued Ninja workspace.
- Confirmed the previously completed ObjectDLL milestone remains the baseline: 533/533 retail server translation units compiled for ARM/Vita.
- Fixed the full-build Jupiter runtime compatibility translation unit without globally replacing FEAR's newer templated `LTLink<T>` ABI:
  - added a translation-unit-local legacy LithTech link/list compatibility header derived from the pinned public upstream `sdk/inc/ltlink.h`;
  - supplied the old-runtime compatibility aliases needed by that bridge (`FLAG2_ADDITIVE`, `DDMatrix`, atomic Interlocked helpers);
  - included the public `ILTCommon` contract explicitly.
- `fearvita_jupiter_runtime_compat.cpp` now compiles cleanly for Vita/ARM.
- Added the missing `ILTRenderer::MakeCubicEnvMap` compatibility method as an explicit `LT_UNSUPPORTED` PC/debug operation; `GameClientShell.cpp` proceeds beyond that compile frontier.
- Aligned the full Vita client source list with the already-existing unsupported/no-op adapters:
  - exclude PC/private-Jupiter model decal, orbital screenshot and performance-log implementations;
  - exclude the Windows/GameSpy multiplayer browser screen (`ScreenMulti`, `ServerBrowserCtrl`) on Vita. `ScreenMgr` already does not register `SCREEN_ID_MULTI` under `PLATFORM_VITA`, so this does not remove a Vita single-player path.

## Current build state

The full `FEARVita` target now rebuilds past all errors listed above. The most recent Ninja run was interrupted only by the execution time limit while compiling later ClientShell/ObjectDLL objects; it did not report a new compiler/linker error before interruption.

Continue with:

```sh
export VITASDK=/mnt/data/vitasdk_m29ay
ninja -C /mnt/data/m29ay_build -j10 FEARVita
```

Do not produce or claim a new VPK until the full executable link and Vita packaging steps actually succeed.
