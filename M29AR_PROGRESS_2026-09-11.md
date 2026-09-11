# M29AR / 0.02 — menu completeness pass + selector touch/audio

M29AP's three-game animated frontend milestone remains frozen: F.E.A.R., Extraction Point and Perseus Mandate all boot to their retail menus with their original menu movies/music. M29AQ's packed StringDB and weapon/menu diagnostics are retained.

M29AR performs a static audit of the complete single-player/options screen graph and fixes several concrete gaps without changing the accepted menu presentation.

## Campaign selector

- A touch no longer launches a different campaign immediately.
- First tap changes the selected campaign and leaves its highlight frame visible.
- Second tap on the already-selected campaign launches it; Cross continues to launch it.
- D-pad/touch selection plays the real retail `interface\Snd\selectchange.wav`.
- Launch plays the real retail `interface\Snd\select.wav`.
- The base retail VFS is mounted before the selector so these sounds come from the user's own game data rather than bundled replacements.

## Full single-player/options menu audit

The reachable screen targets for Main, Single Player, Profile, Load/Save, Display, Audio, Game, Crosshair, Performance, Advanced CPU, Advanced GPU, Controls, Configure, Mouse, Joystick and Weapons all have registered Vita screen objects. M29AR adds a runtime registry self-check so a future missing target is explicitly logged.

The dormant `SCREEN_ID_KEYBOARD` target has no ScreenKeyboard implementation in the released F.E.A.R. source and its menu item is normally commented out. M29AR aliases this target to ScreenConfigure on Vita so a retail-data variant cannot navigate into a missing screen.

`CPerformanceMgr::GetOptionRecord` also had an incorrect bounds condition in the retail source. M29AR validates performance type, group and option before following the DB RecordLink, preventing invalid Performance/Leistung links from becoming bogus records on the Vita bridge.

## Separate networking scope

The PC Multiplayer entry switches to a separate multiplayer executable and server-browser stack. That network path is intentionally not claimed complete by this SP/options menu pass; it remains a separate future networking milestone rather than being hidden as a menu-link fix.

## Build

M29AR builds successfully through executable -> VELF -> SELF -> VPK. The private test VPK retains the already accepted campaign selector art/loading art and all three menu-video caches.
