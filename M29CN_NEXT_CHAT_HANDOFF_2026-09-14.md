# FEARVita next-chat handoff — M29CN / 0.36 — 2026-09-14

## Canonical workspace

- project: `/mnt/data/fear_work/m29ay_src/project`
- LithTech overlay: `/mnt/data/fear_work/m29ay_lithtech/lithtech-master`
- build: `/mnt/data/fear_work/m29ay_build`
- VitaSDK: `/mnt/data/vitasdk_m29bu`
- local private packaging assets: `/mnt/data/fear_work/private_assets_m29cn`

## Hardware-verified M29CM facts

- Vita SFX manager initializes: `sfx-mgr-ok`
- local CharacterFX now registers: `add-list-ok lookup=same`
- F.E.A.R. reaches stock `ChangeState(GS_PLAYING)`
- after X, Base F.E.A.R. retail loop keeps advancing past frame 3600
- Extraction Point reaches the same stock gameplay state
- EP benchmark still separately reproduces a GPU crash

## Root cause of apparent Base F.E.A.R. freeze

The Vita `ILTClient::RenderCamera` implementation was a no-op. Once state becomes `GS_PLAYING`, retail code no longer clears the postload screen automatically. The last loading image can therefore remain on screen while the CPU/game loop continues normally.

## M29CN / 0.36

Changed source files:
- `project/CMakeLists.txt`
- `project/src/main.cpp`
- `project/integration/lithtech/fearvita_iltclient_vita.cpp`

Patch: `patches/M29CN.patch`

M29CN intentionally does not fabricate world geometry. It clears/presents a fresh gameplay frame from the authentic retail camera call, leaves stock HUD/interface drawing in place, and logs:
- `retail-camera`
- `retail-present`
- `input-heartbeat`

## Next hardware test

Test Base F.E.A.R. first. After loading completes, press X and observe whether the loadscreen visibly disappears. Move/look and press controls for several seconds.

Capture `fear_fear.log`. Key ladder:
1. `0.36 / M29CN`
2. `sfx-mgr-ok`
3. `add-list-ok lookup=same`
4. stock `ChangeState(GS_PLAYING)`
5. `retail-camera`
6. `retail-present`
7. `input-heartbeat`

If this succeeds, implement the real Retail camera -> Jupiter world scene submission path next.

EP benchmark is a separate test. If reproduced, collect the new `.psp2dmp` and any `vitaGL.log`/runtime log available.

## Packaging rule

The complete test VPK uses user-provided private launcher/menu media extracted locally from the old complete VPK. Do not commit those assets publicly.
