# FEARVita M29BT / 0.17 checkpoint — Model00p variable-boundary solver

Date: 2026-09-13

## Hardware result that triggered M29BT

M29BS / 0.16 restored the hardware-proven Jupiter-EX v113 world loader. Base F.E.A.R. and Extraction Point again load their worlds to 100% and reach the real local client/player creation path.

The remaining player blocker is the retail `CHARS\\MODELS\\PLAYER.MODEL00P` v33 physics-shape block. The M29BQ/M29BS solver assumed every shape was a 57-byte common prefix plus either 0 or 24 trailing bytes. Hardware disproved that assumption:

- Player physics block starts at 8660, 11 shapes, 10 constraints, 9 physics weight sets.
- Shape 0 at 8660 has a node-valid 57-byte prefix and its next valid record is at 8741: 57 + 24 bytes.
- Shape 1 at 8741 has a node-valid 57-byte prefix, but neither 8798 (+0) nor 8822 (+24) is a node-valid next record.
- Therefore the public WIP 57/81-only layout is incomplete for retail FEAR v33.
- `shapeCount == 0` models (for example ALMA) also exposed a solver bug: the old solver tried to probe a non-existent first shape.

## M29BT change

M29BT keeps the complete hardware-proven M29BP/M29BS world/server/client baseline. The only LithTech runtime change remains `runtime/model/src/model_load.cpp`.

Physics-shape layout solving now:

1. Reads and validates the known 57-byte prefix at each shape boundary.
2. Searches a bounded 0..256-byte trailing extension in 4-byte increments instead of only {0,24}.
3. Recurses only into candidate next records whose decoded node index is `< nodeCount`.
4. Accepts a complete layout only when the byte after the final shape equals the aggregate constraint count from the v33 header.
5. Uses the existing constraint/physics-weight tail parser only as a tie-breaker if multiple exact-boundary layouts survive. If ambiguity remains, loading fails instead of guessing.
6. Handles `shapeCount == 0` as a valid empty shape block whose constraint block starts immediately.
7. Logs `physics-layout solved ... tail=... candidates=...` plus each chosen per-shape `extra=` length for PLAYER.MODEL00P.
8. If no solution exists, logs variable-boundary frontier edges as `[model00p-layout-edge]`.

No fake player, no model-less player, no forced client state and no `GS_PLAYING` bypass were added.

## Binary invariants checked

Fresh 0.17 ELF contains `CWorldSharedBSP::LoadJupiterEx113`, `FearVita_ServerDispatchClientMessage`, `CLTServer::GetClientAddr`, the M29BT startup marker and the variable-layout solver markers. `CLTServer::GetClientAddr` still checks `Client::m_ConnectionID` at offset 0x7c for NULL before the virtual `GetIPAddress` call.
