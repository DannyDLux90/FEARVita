# M29AQ / 0.02 Progress — menu completeness and weapon linkage

## Milestone transition

The M29AP frontend/menu milestone is complete on hardware: F.E.A.R., Extraction Point and Perseus Mandate all enter their retail frontends and show their original animated menu backgrounds. The accepted campaign selector, loading artwork and menu-video presentation are intentionally unchanged in M29AQ.

The next milestone is to make the retail menus and their submenus complete and correctly linked, with the Performance/"Leistung" pages as a first target, while beginning a structured weapon-database/client-weapon audit.

## Packed StringDB decoding

The previous Vita StringEdit bridge indexed real symbolic IDs from `StringDatabase/FEAR.Strdb00p`, but did not decode the packed value table. That forced many strings through a small hand-written language safety net or raw symbolic-id fallback and is a likely source of incomplete/incorrect submenu presentation.

M29AQ adds a packed SKDB v2 reader to `fearvita_stringedit_vita.cpp`:

- validates the `SKDB` header/version,
- reads the padded symbolic-id table,
- decodes the packed UTF-16LE value table,
- reads the TOC at `24 + tocOffset`,
- maps every retail id to its real localized value,
- retains the old symbolic-id scanner as a safe fallback when a database does not validate.

The selected raw StringDB is also exported to `ux0:data/FEARVita/debug/StringDB_<campaign>.strdb00p` to make hardware-only format differences inspectable without guessing.

## Menu navigation audit

`CScreenMgr` now records requested/current screen transitions and first-build success. `CScreenPerformance` records its build and command routing. These diagnostics are intended to distinguish three separate failure classes cleanly: wrong text, missing screen construction, and wrong command/screen routing.

## Weapon audit

`CScreenWeapons` now logs the retail default weapon-priority list. For every usable weapon it records:

- priority position,
- database record name,
- short-name StringDB id,
- long-name StringDB id,
- silhouette icon path.

This gives a campaign-by-campaign baseline for F.E.A.R., Extraction Point and Perseus Mandate before deeper in-game weapon work. M29AQ does not claim the full server/gameplay weapon pipeline is complete yet.

## Hardware test

Visit `Options -> Leistung` and its advanced CPU/GPU pages, then `Options -> Waffen`. Repeat for all three campaigns where practical. The key log markers are `stringedit-packed`, `screen-nav`, `screen-build`, `menu-audit`, and `weapon-audit`.

A successful packed StringDB decode should report `resolved=<entryCount>` followed by `retail SKDB values decoded; retail menu strings authoritative`. If decoding falls back, copy the corresponding `StringDB_fear/ep/pm.strdb00p` export together with the log for the next parser correction.
