# FEARVita M29AY pre-VPK continuation — 2026-09-11

This checkpoint continues the recovered M29AY workspace on branch `m29ay-objectdll-world-runtime`.

## Selector startup sound

The FEAR PC frontend does not hard-code the logo/startup effect as a launcher WAV. `CInterfaceMgr::PreSplashScreenState()` reads `Client/Shared -> Shared -> SplashScreenSound` from the retail ClientDB and plays it as an interface sound.

FEARVita now resolves that same `SplashScreenSound` value from the user's own `Database/FEAR.Gamdb00p` through the existing Vita VFS/GADB reader and plays it exactly once immediately before entering the game-selection menu. No retail audio asset is copied into source, GitHub, or a package. Failure to resolve/play the value is non-fatal and is recorded under the `launcher-splash-sound` diagnostic tag.

The changed `main.cpp` and `fearvita_menu_boot.cpp` translation units compile successfully for ARM/Vita.

## Packaging boundary

Continue the full M29AY build through the executable, VELF and `eboot.bin` SELF stages. Do **not** invoke the `FEARVita.vpk` / `vita_create_vpk` target yet. The next private VPK must remain a separate artifact and is intentionally not created at this checkpoint.

## Hardware status

M29AX remains the last hardware-proven build. M29AY and this selector-sound continuation have not yet been hardware-tested.
