# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AQ  
**Date:** 2026-09-11

The M29AP frontend/menu-video milestone is complete on hardware: F.E.A.R., Extraction Point and Perseus Mandate all reach their retail menus and play their original animated menu backgrounds. The accepted launcher/loading presentation remains unchanged.

M29AQ starts the next milestone: make every retail menu/submenu entry complete and correctly linked, with `Options -> Leistung` / Performance and the weapon options screen as the first audit targets.

The Vita StringEdit bridge now attempts a full packed SKDB v2 decode: id table, UTF-16LE value table and TOC mapping. When this succeeds, the actual retail/localized `.Strdb00p` values become authoritative instead of the earlier small hand-written language safety net. A symbolic-id fallback remains in place for unknown/invalid variants.

For hardware diagnosis M29AQ also adds screen-transition/build logs, Performance command logs, and a weapon-menu audit that records each default-priority weapon record plus its short-name id, long-name id and silhouette icon. The selected retail StringDB can be exported on hardware to `ux0:data/FEARVita/debug/StringDB_<campaign>.strdb00p` if format work is still needed.

Full weapon gameplay is not claimed complete at this checkpoint; M29AQ establishes the correct retail menu/database/client-weapon linkage first.
