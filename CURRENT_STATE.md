# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AN  
**Date:** 2026-09-10

The F.E.A.R. base-game main menu is accepted on hardware and remains unchanged. The M29AM visual flow is also accepted: launch enters the campaign selector directly, and F.E.A.R. / Extraction Point / Perseus Mandate use their correct per-campaign loading presentation with loading phase text and progress.

Both EP and PM now fully decode their main expansion GADB after the late `Surfaces/WeaponFX` compatibility fix. M29AM hardware logs then reach `player-movemgr-ok`, resolve expansion weapon records `NailGun`, `Cannon` and `Plasma`, and data-abort before `player-weaponmgr-ok`.

The paired Vita core dumps point to the same frontend failure site: `AnimPropUtils::Enum()` constructs a `CAutoMessage` for a newly discovered expansion animation property, while the Vita ILTClient compatibility layer currently has no `ILTCommon` implementation and returns `NULL` from `Common()`. This makes `g_pCommonLT` unavailable during the dynamic animation-property synchronization message.

M29AN keeps newly discovered dynamic animation-property mappings local when `g_pCommonLT` is unavailable on Vita and skips only that client/server synchronization message in the current frontend-only runtime. PC/upstream behavior is unchanged. `PlayerMgr` now logs `player-commonlt-ok` or `player-commonlt-null-local-anim-sync` before ClientWeaponMgr initialization so the next hardware result is explicit.

Next hardware priority: boot EP and PM and confirm progress beyond `NailGun/Cannon/Plasma` toward `player-weaponmgr-ok`, `frontend-main-ok` and `complete`. Any later crash becomes the next isolated compatibility seam.
