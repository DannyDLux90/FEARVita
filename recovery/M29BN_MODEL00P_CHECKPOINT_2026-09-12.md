# FEARVita M29BN / 0.11 — Jupiter EX Model00p v33 checkpoint

Date: 2026-09-12

## Why M29BN exists

M29BM fixed the connectionless local-client crash and restored the real world load. Hardware logs for both Base F.E.A.R. Intro and Extraction Point Performance Test reached 100% and completed world loading, but `ServerShell::OnClientEnterWorld` could not create the player because the old LithTech model loader treated `*.Model00p` as an LTB file.

The failure was deterministic:

- legacy loader read the first byte of `MODL` as the LTB file type (`77`, ASCII `M`),
- `CHARS\\MODELS\\PLAYER.MODEL00P` failed,
- `OnClientEnterWorld` returned `LTNULL`,
- local client remained `state=2 player=0` and repeatedly retried player entry.

The same old-loader error affected many weapon/character Model00p assets during world construction.

## M29BN implementation

M29BN adds a separate content-detected Jupiter EX packed-model path in `runtime/model/src/model_load.cpp`.

- `MODL` magic is detected before the legacy LTB header is read.
- F.E.A.R. Model00p version 33 is accepted explicitly.
- Legacy `.ltb` files continue through the original LTB loader unchanged.
- Model00p is no longer accepted by the LTB extension branch.

The v33 parser covers the packed sections used by F.E.A.R.:

- header and string table,
- depth-first skeleton nodes and global bind transforms,
- animation schemas / two-track channel flags,
- packed animation data and animation bindings/keyframes,
- 1/64 compressed position channels and int16 quaternion channels,
- animation weight sets,
- sockets,
- child-model names,
- physics shapes / constraints / physics weight sets,
- LOD groups / piece metadata,
- packed mesh/index payload bounds validation,
- post-mesh influence metadata.

On the Vita/server runtime, geometry is represented with the existing `CDIModelDrawable` dummy render objects, but the packed geometry section is still structurally parsed and bounds-checked. Engine-visible skeletons, animations, weight sets, sockets and piece/LOD metadata are populated as normal `Model` structures rather than bypassing the player model.

A pre-existing `ModelPiece::Term` typo was also fixed: the render-object pointer array is now freed based on `m_pRenderObjects`, not the already-cleared `m_pLODDists` pointer.

## Diagnostic markers

To make the first hardware validation actionable, `PLAYER.MODEL00P` emits staged markers without spamming every model:

- `[model00p-player] header ...`
- `[model00p-player] nodes-ok ...`
- `[model00p-player] schemas-ok ...`
- `[model00p-player] anim-raw-ok ...`
- `[model00p-player] anim-info-ok ...`
- `[model00p-player] weights-ok ...`
- `[model00p-player] sockets-ok ...`
- `[model00p-player] children-ok ...`
- `[model00p-player] packed-sections-ok ...`
- `[model00p-player] skeleton-built ...`
- `[model00p-player] pieces-built ...`
- `[model00p-player] children-built ...`
- `[model00p-player] animations-built ...`
- `[model00p-player] runtime-model-ready ...`
- `[model00p] loaded v33 file=CHARS\\MODELS\\PLAYER.MODEL00P ...`

If an undocumented packed-layout variant is encountered, the final emitted stage identifies the section immediately before the failure.

## Build result

Full Vita build completed:

- executable link: PASS
- VELF: PASS
- SELF / `eboot.bin`: PASS
- SFO: PASS
- VPK generation: PASS

Public app metadata for this private test candidate:

- APP_VER: `00.11`
- internal checkpoint: `M29BN`
- title ID: `FEAR00001`

The full hardware-test package was rebuilt from the same 22-file payload layout used by M29BM; only `eboot.bin` and `sce_sys/param.sfo` were replaced.

## Artifacts

- `FEARVita_M29BN_0.11_JUPITEREX_MODEL00P_2026-09-12.vpk`
  - SHA-256: `cb94702150301f58dd04a08ce4f0be799857b6ecf9f9e7e2b55c12a461d448c7`
- `FEARVita_M29BN_0.11_BUILDABLE_SOURCE_2026-09-12.zip`
  - SHA-256: `f1ed66aba73894468c176f3dbad1dfb37474740e2370725e5e34562b21ab1153`
- `M29BN_JUPITEREX_MODEL00P_V33_FIX_2026-09-12.patch`
  - SHA-256: `fc72893b63ae68ff222218720da57f00542896a0379ce085f3ea5e424ffd62a9`

## Hardware test

First test:

1. Base F.E.A.R.
2. New Game
3. Medium
4. Let the Intro load without leaving the app.

Then optionally repeat Extraction Point -> Performance Test.

Success frontier:

1. no `Incorrect LTB file type (77)` for Model00p,
2. `[model00p] loaded v33 ... PLAYER.MODEL00P`,
3. `OnClientEnterWorld` returns a real player instead of `LTNULL`,
4. `engine-client ... player=1`,
5. client `OnEnterWorld` / normal Loading -> Loaded -> InWorld progression,
6. loading screen gives way to the Intro / in-game camera.

If M29BN still stops before entering the game, preserve `fear_fear.log` (and PSP2 core dump only if there is a crash). The last `[model00p-player]` marker is the primary discriminator for the next fix.
