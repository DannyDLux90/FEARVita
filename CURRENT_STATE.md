# FEARVita current state

**Public package version:** 0.08  
**Internal checkpoint:** M29BK  
**Date:** 2026-09-12

M29BJ hardware testing advanced the real F.E.A.R. Intro load to the genuine retail loading bar at 80%. The Jupiter EX v113 path completes all 347 BSPs, sees 93 BlindData chunks, begins the 1,988-object server list and logs object milestones through at least index 1663 before the old diagnostic cap is exhausted.

The M29BJ PSP2 core maps the new deterministic crash to `CAINavMesh::RuntimeSetup()` during `CGameServerShell::PostStartWorld`. The packed NavMesh is Win32/MSVC data with 4-byte unscoped enums; Vita GCC had compiled the same enum-bearing structures with short enums. In particular, `CAINavMeshEdge` was 64 bytes on Vita instead of the 72-byte retail layout, shifting the raw packed parser by thousands of bytes.

M29BK rebuilds the F.E.A.R./LithTech Vita game-runtime boundary with `-fno-short-enums` and compile-time layout assertions for the critical NavMesh structures. `RuntimeSetup` now also receives the real BlindObject buffer length and preflights each packed section with explicit overflow/bounds checks before the legacy pointer fix-up path runs. A future mismatch reports `[navmesh-layout] preflight-fail ...` instead of data-aborting; a matching layout reports `[navmesh-layout] preflight-ok ... enum=4 edge=72`.

The stale NavMesh edge-list count reset is corrected. Repetitive `FindObjectsCB` overflow logging is suppressed after the first few messages and the Vita diagnostic ceiling is raised from 512 KiB to 2 MiB. Only the cyan retail loading bar remains. Audio is unchanged for test isolation.

The separate F.E.A.R. `Model00p` compatibility frontier remains: M29BJ proved these files use the `MODL!` container and are not legacy LTB model files, so a dedicated Jupiter EX model-loader path is still required after the world-start path is stable.

For continuation, use GitHub branch **`m29bk-navmesh-abi`** and read `CURRENT_STATE_M29BK.txt`, `M29BK_PROGRESS_2026-09-12.md`, and `recovery/M29BK_RECOVERY.md`.
