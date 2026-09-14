# FEARVita next-chat handoff — M29CP / 0.38 — 2026-09-14

## Canonical workspace

- Workspace: `/mnt/data/fear_work`
- Project: `/mnt/data/fear_work/m29ay_src/project`
- LithTech tree: `/mnt/data/fear_work/m29ay_lithtech/lithtech-master`
- Build: `/mnt/data/fear_work/m29ay_build`
- VitaSDK: `/mnt/data/vitasdk_m29bu`
- Milestone/version: **M29CP / 0.38**

## M29CO hardware conclusion

Do not revisit ClientInWorld or CharacterFX unless new logs explicitly regress them. M29CO already proved the authentic stock gameplay transition is reached. The remaining 0.37 failures were after that point:

- Base F.E.A.R.: no gameplay `RenderCamera`; frozen previous loadscreen and bad HOME behavior.
- EP benchmark: GPU watchdog before any gameplay-camera draw.

## M29CP root causes fixed

1. Missing engine `LTEVENT_RENDERINIT` left FEAR's main-window focus false, so retail `RenderCamera` returned before drawing.
2. `FlipScreen` skipped swap/vsync when no camera frame was open, producing an unthrottled hot loop.
3. AVPlayer decoder-owned YUV pointers were used directly by GXM and could be recycled while queued GPU work still referenced them.
4. No real Jupiter EX v113 render-section parser existed in the active Vita world path.

## M29CP implementation

- Dispatch `LTEVENT_RENDERINIT` through `IClientShell::OnEvent` after successful Vita retail initialization.
- Dispatch `LTEVENT_GAINEDFOCUS` after Vita resume.
- `FlipScreen` always submits/presents a frame; fallback frame is used on retail render skip.
- AVPlayer uses five owned physically-contiguous/GXM-mapped YUV staging buffers and waits before ring-slot reuse/free.
- `CWorldSharedBSP::LoadJupiterEx113` calls the v113 render parser at the real `render_data_pos`.
- New files:
  - `project/integration/lithtech/fearvita_jupiterex_render_vita.cpp`
  - `project/integration/lithtech/fearvita_jupiterex_render_vita.h`
- FEAR v113 render format parsed from the public Jupiter-EX layout: render header, vertex/index blocks, vertex definitions, surfaces, material names.
- World surfaces become persistent Vita mesh chunks.
- Retail `ILTClient::RenderCamera` builds real FEAR camera MVP, frustum-culls chunks and submits up to 3000 triangles/frame with depth read/write.
- Near-plane intersecting chunks are skipped until triangle clipping is implemented.
- Initial world render is diagnostic vertex/normal shaded; materials and UVs are parsed but world material textures are not yet bound.

## Safety invariants retained

- authentic local-client flow only;
- real server-side player;
- stock StartGameRequest/postload/ClientInWorld;
- separate server/client objects and client ModelInstance proxy;
- real CharacterFX message/list insertion;
- stock OnEnterWorld and stock `ChangeState(GS_PLAYING)`;
- no forced game state;
- no fake/model-less player;
- no broad unsafe HOBJECT forwarding.

## Build/package status

Release compile/link: **success**.
VELF/SELF/VPK: **success**.
VPK contents: same 22 file paths as complete M29CO, including 3 boot images, 4 launcher images and 3 menu videos.
SFO: `00.38`, title id `FEAR00001`.

VPK SHA-256: `58b028f48043eb3af279c4acd54bd7f040338cd9db8e874fbdeeedc245e95f77`
ELF SHA-256: `4554241a5bc57f084c7f05b354b2291867514a0bac301e1a47027326bb0f315f`

Patch from M29CO: `/mnt/data/M29CO_to_M29CP.patch`

## Next action

Hardware test M29CP, always both:

1. Base F.E.A.R. normal mission path through intro/postload/X.
2. Extraction Point -> Performance Test as the direct-3D control path.

For Base, verify `renderinit-dispatched`, `world-v113-render ... shared-render-ready`, `retail-camera world=1`, visible shaded geometry, input and HOME behavior.

For EP benchmark, verify `perf-test ...`, `world-v113-render`, `retail-camera world=1`, continuing presents, and absence of GPU watchdog.

If there is a crash, collect the campaign log, `vitaGL.log`, and the new GPU/CPU dump. Do not infer renderer success from `GS_PLAYING` alone; require positive `retail-camera world=1 chunks>0 tris>0` hardware evidence.
