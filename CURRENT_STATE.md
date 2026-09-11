# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AR  
**Date:** 2026-09-11

The M29AP three-game frontend/video milestone is complete on hardware: F.E.A.R., Extraction Point and Perseus Mandate boot to their retail menus and play their original animated menu backgrounds with retail menu music/UI sounds. That accepted presentation remains unchanged.

M29AR continues the menu-completeness/weapon milestone. The full reachable single-player and Options screen graph has been statically audited. Main/Single/Profile, Load/Save, Display, Audio, Game/Crosshair, Performance/Advanced CPU/Advanced GPU, Controls/Configure/Mouse/Joystick and Weapons all have registered screen targets. A runtime registry audit now catches future missing targets explicitly.

The campaign selector now behaves like an actual selection UI with touch: the first tap selects and shows the frame, while a second tap starts the selected game. Left/right and touch selection use the original retail `interface\Snd\selectchange.wav`; activation uses `interface\Snd\select.wav`. The base user-owned FEAR VFS is mounted before the selector so these are the real game UI sounds rather than bundled replacements.

For the Performance/Leistung tree, `CPerformanceMgr::GetOptionRecord` now validates type, group and option indices before following the DB RecordLink. M29AQ's packed SKDB v2 decoder is retained so original localized StringDB values can populate labels/help text instead of the older fallback set. The dormant Keyboard screen id aliases to the existing Configure-controls screen instead of dead-ending if a data variant exposes it.

M29AQ's weapon-menu audit is retained as the foundation for the weapon work: campaign weapon records, name ids and silhouette icons are traced through the real WeaponDB. Full gameplay weapon behavior is not yet claimed complete.

The PC Multiplayer menu belongs to a separate FEARMP executable/network browser architecture; that networking path is deliberately tracked as a separate milestone and is not counted as a completed gameplay feature in this SP/options menu pass.
