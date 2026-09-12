# FEARVita M29BK progress — 2026-09-12

## Hardware evidence from M29BJ

M29BJ removes the duplicate white fallback bar and clears the SoundSet UDF crash. The real retail loading bar now reaches 80%. The Jupiter EX v113 world path still completes all 347 BSPs, finds 93 blind-data chunks, and enters the 1,988-object server list. The hardware log records object milestones through at least index 1663 before diagnostic flood reaches the old 512 KiB log cap.

The M29BJ `.Model00p` extension acceptance also exposed the real model frontier: F.E.A.R. Model00p files are not old LTB model files, and the legacy loader reports LTB type 77 / `MODL!`. This is not the M29BJ crash and is left as a later dedicated compatibility task.

## M29BJ crash root cause

The PSP2 core maps the main-thread crash to `CAINavMesh::RuntimeSetup`, called from `CAIMgr::SetupNavMesh` during `CGameServerShell::PostStartWorld`, after the real world-object phase. The packed NavMesh BlindObject chunk is 67,492 bytes after its four-byte outer processed-data flag and reports NavMesh version 6 with 557 edges.

The decisive ABI mismatch is enum width. Retail F.E.A.R. NavMesh data was packed by Win32/MSVC, where the unscoped enum fields in the serialized NavMesh structures occupy four bytes. Vita GCC defaults to short enums for this ABI: the M29BJ ARM binary compiled `CAINavMeshEdge` to 64 bytes and advanced the raw pointer by `edgeCount * 64`. The Win32 layout is 72 bytes. With 557 edges the parser is already 4,456 bytes off before it reaches the next packed count, eventually interpreting float payload as a count and faulting on an invalid pointer.

## M29BK fix

M29BK rebuilds the F.E.A.R./LithTech game-module boundary with `-fno-short-enums` so serialized enum-bearing structures match the original 32-bit Win32 ABI. Compile-time Vita assertions verify the critical packed structures, including 4-byte NavMesh enums, 72-byte `CAINavMeshEdge`, 72-byte `CAINavMeshPoly`, 16-byte component data, region/link/node-cluster records, and the 52-byte quad-tree node layout.

`CAINavMesh::RuntimeSetup` now receives the actual BlindObject buffer size. Before the legacy pointer-cast loader runs, a Vita preflight walks every packed section with overflow/bounds checks in the exact runtime order. A future format/layout mismatch therefore returns with a `[navmesh-layout] preflight-fail ...` diagnostic instead of causing another data abort. A successful layout produces `[navmesh-layout] preflight-ok ... enum=4 edge=72`.

The stale edge-list count reset in `TermNavMesh` is corrected as part of the same NavMesh hardening.

## Diagnostic quality

The hundreds of `FindObjectsCB: Overflowed` messages were consuming the log and hid the actual end-of-world sequence. Vita now records the first few and then suppresses duplicates. The default runtime-log ceiling is increased from 512 KiB to 2 MiB so a single hardware run is much more likely to capture the next genuine frontier.

## Loading UI / audio

Only the cyan retail `m_LoadProgress` bar remains; no white FEARVita fallback is reintroduced. Audio mixer/resampler behavior is unchanged in M29BK to keep the world-start test isolated.

## Build/package verification

- Version: `0.08 / M29BK`
- Complete VPK payload files: 22
- ZIP entries including directories: 35
- ARM ELF, VELF and FSELF generation: succeeded
- Embedded EBOOT: byte-identical to built EBOOT
- EBOOT SHA-256: `71bf928453df714588df92009671e7fd906897bbd4f4000f0ee2129b5157571a`
- VPK SHA-256: `65252da31112eed20325721eae21a2f9b279a2a0e161e611f1b92e817197e569`
- M29BJ->M29BK patch SHA-256: `3a3c9b05c33f75915beb3068518e807ef5eb71acd442c63d51a1238f76a15f0d`
