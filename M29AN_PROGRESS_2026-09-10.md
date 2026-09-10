# M29AN / 0.02 — EP/PM dynamic animation-property frontend crash fix

Hardware M29AM logs show both Extraction Point and Perseus Mandate reach `player-movemgr-ok` and then create expansion weapon records (`NailGun`, `Cannon`, `Plasma`) before the process data-aborts.

The paired Vita core dumps point to the same failure site in `CAutoMessage::Init()`: the expansion weapon path enters `AnimPropUtils::Enum()` for a previously unseen dynamic animation property, but the Vita ILTClient compatibility layer still returns `NULL` from `ILTClient::Common()`. Therefore `g_pCommonLT` is unavailable and the original dynamic client/server synchronization message cannot be created.

M29AN keeps the dynamic animation-property mapping locally on Vita and skips only that network synchronization message while `g_pCommonLT` is unavailable. This is appropriate for the current frontend-only boot path and does not change PC/upstream behavior. `PlayerMgr` also emits `player-commonlt-null-local-anim-sync` so hardware logs confirm the path explicitly.

The user-verified M29AM visual flow is preserved unchanged: direct campaign selector, correct per-campaign loading artwork, loading phase text and progress bar. Proprietary/user-supplied artwork and converted retail videos are excluded from this public checkpoint.

Next hardware target: EP and PM should continue beyond `NailGun/Cannon/Plasma` and ideally reach `player-weaponmgr-ok`, `frontend-main-ok` and `complete`. Any later crash becomes the next isolated compatibility seam.
