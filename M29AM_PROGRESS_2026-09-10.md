# M29AM / 0.02 Progress — visual-flow correction

## Hardware feedback after M29AL
The launcher/loading flow looked unchanged on hardware. Re-checking the actual source and packaged VPK found two independent logic problems:

1. The separate startup splash call had been removed, but the boot-progress overlay was still rendered by the early `startup: renderer and controller ready` diagnostic. That made a pre-selector loading screen remain visible even though `RunStartupSplash` was no longer called.
2. After selecting a campaign, the code emitted `selected campaign=...` and correctly set the overlay campaign, but then immediately called `ResetBootProgressOverlay()`. That reset `campaign` back to F.E.A.R., so EP and PM always displayed the F.E.A.R. loading background.

## M29AM fixes
- Boot-progress overlay defaults to hidden.
- It is armed only when the `selected campaign=...` diagnostic is received.
- `ResetBootProgressOverlay()` is now called before the campaign-selection diagnostic, not after it.
- Therefore EP and PM retain their selected campaign id while the post-selection loading overlay runs.
- The unused startup splash art is no longer packaged.
- The campaign selector background and the three campaign icons remain.
- Loading phase text remains visible above the progress bar.
- Private hardware-test VPK retains the known-good F.E.A.R. menu MP4 cache.

## Verification before hardware test
- Fresh VitaSDK rebuild completed through ELF -> VELF -> SELF -> VPK.
- The built ELF contains the M29AM banner.
- The VPK contains distinct `boot_art/fear.png`, `boot_art/ep.png`, and `boot_art/pm.png` files.
- `boot_art/ep.png` and `boot_art/pm.png` match the user re-supplied images byte-for-byte by MD5.
- `launcher_art/startup.png` is absent from the new package.

## Expansion status
The earlier M29AK GADB change remains active. EP hardware logging now shows the main expansion database reaching `decoded=1` after synthesizing the anomalous late `Surfaces/WeaponFX` record name. The remaining expansion crash is later, around PlayerMgr/weapon initialization, and is still under investigation.
