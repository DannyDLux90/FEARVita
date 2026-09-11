# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AS  
**Date:** 2026-09-11

The M29AP three-game frontend/video milestone is complete on hardware: F.E.A.R., Extraction Point and Perseus Mandate boot to their retail menus and play their original animated menu backgrounds with retail menu music/UI sounds. That accepted presentation remains unchanged.

M29AR's menu-completeness work remains active: the reachable single-player/options screen graph is registered, selector touch/highlight behavior is fixed, selector movement/activation use the original retail UI sounds, Performance RecordLinks are bounds-checked, and Advanced CPU/GPU layout state is separated correctly.

M29AS fixes the language regression introduced by M29AQ's packed SKDB decoder. Hardware still detected the Vita system language as German, but decoded packed retail strings were returned before the existing Vita-language overlay. System-language localizations are now authoritative where FEARVita defines them; decoded packed retail StringDB values remain the complete fallback for all other ids. `IDS_GAME_LANGUAGE` therefore again follows the Vita system language.

The weapon milestone is now moving from the menu/database audit into the actual client runtime. M29AS logs CClientWeaponMgr player-weapon creation and weapon-change requests/dispatch so the next gameplay pass can follow WeaponDB -> CClientWeapon -> viewmodel/animation/ammo/fire in order. Full gameplay weapon behavior is not yet claimed complete.

The PC Multiplayer menu belongs to a separate FEARMP executable/network browser architecture; that networking path remains a later standalone milestone.
