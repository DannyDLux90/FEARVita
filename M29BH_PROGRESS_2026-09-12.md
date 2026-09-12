# FEARVita M29BH progress — 2026-09-12

Public app version: 0.05  
Internal checkpoint: M29BH

## Hardware frontier inherited from M29BG

M29BG proves the real local-session path reaches `Worlds\\Release\\Intro.World00p` without crashing, but the legacy open LithTech world loader immediately rejects the packed world with `LT_INVALIDWORLDFILE (42)`. The Vita GT4 loading-bar track is visible at 0%, which confirms rendering works; there is no parser progress because the file is rejected before the first legacy world milestone.

The key format mismatch is now explicit: the open runtime's legacy loader expects world version 85, while F.E.A.R. Jupiter EX `World00p` uses version 113 with a different 56-byte header and independently addressed render, sector, object and blind-data sections.

## M29BH changes

- Adds a Vita/Jupiter-EX version-113 branch to `CWorldSharedBSP` while keeping the legacy version-85 path unchanged for non-Vita builds.
- Reads the v113 header (`version`, render/sector/object/blind offsets, world bounds and source offset).
- Parses F.E.A.R.'s packed WorldModels collision section: XOR-obfuscated section counts (FEAR magic 399), BSP name table, plane normals, polygon records, BSP nodes and vertices.
- Builds legacy `WorldBsp`/`WorldData` objects from the Jupiter EX collision data so the existing server collision and WorldModel-instance runtime can continue to operate.
- Infers each BSP root from the node reference graph and validates child indices instead of assuming node 0.
- Adds detailed `world-v113` diagnostics for section counts, BSP headers, invalid plane/vertex/node references and inferred roots.
- Adds a v113 server object loader for the offset-addressed object section and maps Jupiter EX property records to LithTech `GenericProp` values before normal ObjectDLL `OnPrecreate` / `sm_AddObjectToWorld` processing.
- Adds v113 blind-data loading using the packed data blob plus `{size,type,start}` index table.
- Defers the old client render-data reader for v113. M29BH's immediate goal is authentic server-world/bootstrap progression; render-surface integration remains a later stage if the server load succeeds.
- Moves the proven GT4 loading bar upward and makes it thinner so it no longer overlaps the help text. Progress remains tied to real parsing/object phases.
- Retains M29BG's 48 kHz polyphase audio backend and debug 48-kHz WAV export; no further speculative audio changes are made without the exported PCM comparison.

## Build verification

- ARM/Vita executable links successfully.
- `vita-elf-create` and `vita-make-fself` succeed.
- Build marker: `FEARVita 0.05 / M29BH; Jupiter EX v113 world bootstrap`.
- VPK app version: `00.05`.
- Complete VPK is rebuilt from the known-good 22-file package layout; embedded EBOOT is byte-identical to the built EBOOT.

## Next hardware test

Run only base F.E.A.R. -> New Game -> Medium. The expected next log sequence starts with `world-v113 header-ok` and decoded section counts. If v113 collision parsing succeeds, loading percentage should move above 0%, followed by v113 object/blind-data diagnostics and then the next authentic server/gameplay frontier.
