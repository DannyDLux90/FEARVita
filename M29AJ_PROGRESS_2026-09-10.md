# M29AJ / 0.02 Progress — add-on frontend partial DB recovery

## Hardware evidence used
The M29AH logs show a clean divergence after PlayerMgr MoveMgr initialization:

- F.E.A.R.: `player-movemgr-ok` -> weapon records resolve -> `player-weaponmgr-ok` -> frontend continues.
- Extraction Point: `player-movemgr-ok` -> immediate `engine-init-failed result=1`.
- Perseus Mandate: `player-movemgr-ok` -> immediate `engine-init-failed result=1`.

Both expansion main GADB tables are found and substantially parsed, but full packed-table decoding stops late with `bad-record-name`:

- EP: 156 of 158 categories were reached.
- PM: 162 of 164 categories were reached.

The previous database adapter treated `tablesDecoded == false` as invalidating every packed `RecordLink`, even links that point into categories/records that had already been parsed successfully. ClientWeaponMgr depends on those links for the PlayerWeapons list.

## M29AJ changes

1. `ILTDatabase::GetRecordLink` now permits links into already-parsed categories when a later category caused the packed-table decoder to stop. Bounds and `cat->parsed` checks remain mandatory.
2. `bad-record-name` diagnostics now include category index/name, record index, string offset and packed-table byte position so any remaining expansion-only serialization construct can be identified from the next Vita log.
3. PlayerMgr logs `player-weaponmgr-failed` explicitly.
4. On the Vita frontend-first path only, a failed ClientWeaponMgr initialization no longer aborts the complete retail frontend. It logs `player-weaponmgr-skip-vita` and continues so EP/PM can reach their menus while full gameplay weapon initialization remains a later milestone.
5. M29AI's minimal campaign-art loading screen remains intact.
6. F.E.A.R.'s working fullscreen menu-video path remains intact.

## Expected next hardware result
For EP/PM, the next log should progress beyond `player-movemgr-ok`. Preferred path:

`player-movemgr-ok -> player-weaponmgr-ok -> player-pvattach-ok -> ... -> frontend-main-ok -> complete`

If the partial-record-link recovery is insufficient, the fallback path should show:

`player-weaponmgr-failed -> player-weaponmgr-skip-vita`

and then continue to the next PlayerMgr stages instead of returning `engine-init-failed` immediately.

If `gamedb-table-decode` still reports a late failure, its reason now contains enough structural context to implement the exact expansion format rather than guessing.
