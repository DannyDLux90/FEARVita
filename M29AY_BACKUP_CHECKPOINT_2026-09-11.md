# FEARVita M29AY backup checkpoint — 2026-09-11

Backup was prioritized before further linker work. No VPK was generated.

## Verified local archives

- `FEARVita_M29AY_SOURCE_CURRENT_2026-09-11.zip`
  - SHA-256: `b1b0f5c03f9c8a778ef3ba51f0a21a974d13f27b7ab8e4d0c1cb15681204710e`
  - ZIP integrity test: PASS
- `FEARVita_M29AY_WORKSPACE_CURRENT_2026-09-11.zip`
  - SHA-256: `16116d19080235f7fcdab8c5913b4d69e5a9e9efea67498be8d0beb57415b7ea`
  - ZIP integrity test: PASS

The workspace archive contains the patched source trees, Ninja build tree/dependency metadata, current build logs, source SHA-256 manifest, and the unified delta against the originally recovered M29AY workspace.

## Current delta versus recovered M29AY workspace

- Added files: 1
- Modified files: 12
- Deleted files: 0
- Current delta XZ SHA-256: `ae779a99646fc1fd685760e6844a7f359daf140c4536ce9f5e0f066059b6f4a9`
- GitHub reconstruction: `patches/M29AY_CURRENT_DELTA_RECONSTRUCT.md`

## Preserved current work

- F.E.A.R. retail `SplashScreenSound` is resolved from the installed FEAR game database and played once immediately before the game selector; no retail audio asset is bundled.
- M29AY continuation compatibility changes are preserved.
- FEAR Shared client/server compilation has been advanced through TeamMgr, WeaponDB, SurfaceDB, EngineTimer, ForceVolume, ActivateTypeHandler and related shared code.
- LithTech SDK/server-base integration has advanced toward the executable linker frontier.
- Last hardware-proven package remains M29AX.
- M29AY is not hardware-validated.
- VPK generation remains intentionally deferred until explicitly requested.

## Redundant canonical recovery

The original canonical M29AY patch is now fully stored as `patches/M29AY.patch.xz.b64.part00` through `part29`; reconstruction instructions and hashes are in `patches/M29AY_PATCH_RECONSTRUCT.md`.
