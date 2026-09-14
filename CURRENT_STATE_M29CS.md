# FEARVita current state — M29CS / 0.41 — 2026-09-14

## Hardware result from M29CR / 0.40

M29CR was a regression before gameplay. Both Base F.E.A.R. and Extraction Point successfully parsed the Jupiter EX v113 render metadata, but the metadata log ended with an empty source path and `shared-render-load-failed`. Consequently the server world load returned error 42 and EP never reached `retail-camera`.

Root cause: `CServerMgr::LoadWorld()` bound the World00p source path before calling `CWorldServerBSP::Load()`. `CWorldServerBSP::Load()` performs its own `Term()` first; FEARVita's shared-world Term clears the v113 render bridge, including the source path. The parser then had valid metadata but rejected it solely because the now-cleared lazy reopen path was empty.

## M29CS fix

- Do not bind the lazy World00p source before `CWorldServerBSP::Load()`.
- v113 metadata parsing succeeds based on parsed surfaces only; it no longer requires the lazy reopen path during the shared-world phase.
- After `CWorldServerBSP::Load()` succeeds, `CServerMgr::LoadWorld()` binds the World00p path.
- `FearVita_SetJupiterWorldRenderSource()` no longer clears the freshly parsed v113 metadata. It releases only an old reopen stream and replaces the source path.
- The rest of M29CR is unchanged: deferred visible-surface mesh cache, Mat00 `tDiffuseMap` parsing, DTX/DDS diffuse upload, repeat UV wrapping, 12 MiB mesh/texture LRUs, 2 texture uploads/frame, 3000 world triangles/frame, and triangle-selective near-plane safety.

## Expected hardware ladder

For both Base and EP the load should now show:
1. `world-v113-render metadata-ready ... persistent-mesh-bytes=0 source=` — empty is expected at this exact phase;
2. `world-v113-render shared-render-ready`;
3. after shared load returns: `world-v113-render source=<world>.World00p`.

Base should then continue through player Model00p creation without the old world-mesh memory pressure and reach the retail postload confirmation.

EP performance test should return to the M29CQ stability baseline (`GS_PLAYING`, repeated `retail-camera` / `retail-present`) and additionally exercise lazy `world-v113-cache`, `world-material`, and `world-texture` markers.

## Build verification

Release ELF/SELF/VPK built successfully with VitaSDK 2026.08.1. The VPK contains 22 entries including the private local boot/launcher artwork and all three menu-video caches. `param.sfo` reports `00.41` / `FEAR00001`. ELF RX/RW segments remain non-overlapping.

SHA-256:
- VPK: `1c110ad0ca9d19cfa76577d16c9789826c64f97126b462dfe49eb55b807e817c`
- eboot.bin: `8b55df611b670f51b64f076c8ae73e245545c91f55dd41e6ca9012cd480a0c5c`
- ELF: `ec3a7e05219447d5cf2e106432dbd817444745f22659e2dfd30dbbb8a54285e7`
