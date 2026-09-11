# M29AS / 0.02 — Vita language priority restore + weapon runtime trace

## Regression fixed
M29AQ added the packed SKDB v2 decoder. That decoder was correct enough to resolve all 9294 base-game entries on hardware, but its return order accidentally made the packed retail value authoritative before the existing Vita system-language overlay. On an English retail StringDB this regressed a German Vita back to English even though the launcher still detected `de` correctly.

M29AS restores the intended precedence:
1. if an id has a FEARVita system-language localization, use the Vita-selected language;
2. otherwise use the fully decoded retail packed SKDB value;
3. only then use the symbolic-id fallback.

`IDS_GAME_LANGUAGE` therefore again resolves from the Vita language bridge, preserving the previous InterfaceResMgr language behavior while keeping the new complete packed decoder for all ids that are not in the portable overlay. New diagnostics report `stringedit-lang` with `override-priority=1` and the active Vita language.

## Weapon milestone continuation
The accepted menu presentation is unchanged. M29AS also starts tracing the actual runtime client-weapon layer rather than only the Options -> Weapons priority screen. The Vita build now logs:
- the number of player weapon objects created by `CClientWeaponMgr::Init`;
- each initialized WeaponDB record/index;
- weapon-change requests;
- the active/pending weapon after dispatch and whether the switch was immediate.

This does not claim weapon gameplay complete. It gives the next hardware/gameplay pass a clean trace from WeaponDB -> CClientWeapon -> weapon selection/change so viewmodel, animation, ammo and firing work can be corrected in order.

## Build
M29AS builds successfully through executable -> VELF -> SELF -> VPK. The private hardware VPK is based on the accepted M29AR package and retains all three user-generated menu-video caches plus launcher/loading art.
