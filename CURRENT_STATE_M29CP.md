# FEARVita current state — M29CP / 0.38 — 2026-09-14

## Why M29CO / 0.37 still failed on hardware

M29CO proved that the local-client/gameplay state path is no longer the blocker: both campaigns can reach the stock gameplay transition and CharacterFX registration succeeds. The remaining failures were renderer/lifecycle specific.

### Base F.E.A.R. mission

After the postload confirmation the retail game state kept updating, but no gameplay `RenderCamera` call occurred. The Vita runtime never delivered the engine's normal `LTEVENT_RENDERINIT`, so FEAR left `m_bMainWindowFocus` false and rejected every gameplay camera render. `FlipScreen` also did not swap/vsync when no frame had been opened, allowing a hot loop that matched the frozen-loadscreen / unusable-HOME symptom.

### Extraction Point performance test

The benchmark also reached gameplay without a gameplay-camera draw before the GPU watchdog. The menu video path used the transient `sceAvPlayerGetVideoData().pData` pointer directly as a GXM texture source. Decoder buffer recycling could therefore race queued GPU work.

### World rendering gap

The FEAR World00p files are Jupiter EX version 113. The old Vita client-render path had no v113 render-section parser, so even after restoring camera focus it could not display the real world geometry.

## M29CP fixes

### Retail focus / lifecycle

- Dispatch the authentic `LTEVENT_RENDERINIT` to the retail client shell after successful Vita renderer/client-shell initialization.
- Preserve normal FEAR event handling rather than directly modifying private focus flags.
- On Vita resume, dispatch `LTEVENT_GAINEDFOCUS` through the retail shell.

### Present / HOME safety

`ILTClient::FlipScreen` now always performs a real frame completion. If retail skipped camera rendering, the bridge opens and clears a fallback frame before `EndFrame`, so swap/vblank pacing and the OS scheduler still progress. A skipped camera can no longer become an unthrottled no-present loop.

### AVPlayer / GXM lifetime

- Never expose decoder-owned `frame.pData` directly to GXM.
- Copy decoded YVU420P2 frames into five FEARVita-owned, physically contiguous, GPU-mapped staging buffers.
- Synchronize GPU rendering before reusing a staging slot after a full ring rotation.
- Drain GPU work before AVPlayer close and before freeing/unmapping staging memory.

### Real Jupiter EX v113 world render

The active shared-world loader now parses the real v113 render section at the World00p `render_data_pos` while the stream is alive.

Parsed data:
- 10-DWORD render-section header;
- global vertex data block;
- triangulation/index block;
- 8-byte vertex property descriptors;
- position, normal and UV properties;
- render surfaces with vertex start/count/stride, triangle start/count, material id and vertex-definition index;
- 16-bit-length-prefixed material names.

The format layout was cross-checked against the public `io_scene_jupex` FEAR/Jupiter-EX importer rather than guessed from bytes.

### Vita draw strategy

- Surfaces are split into small spatial mesh chunks and uploaded as persistent FEARVita meshes.
- The retail camera supplies its real position, rotation and FOV.
- +Z forward / Y-up view-projection is used.
- CPU frustum culling rejects chunks outside the camera volume.
- Chunks intersecting the near plane are conservatively skipped because the current CPU projector does not clip triangles.
- Depth read/write is enabled.
- Initial per-frame budget is 3000 world triangles to reduce first-frame GXM risk.
- Parser loading is transactional: any parse/mesh failure frees every partially created world mesh immediately.

M29CP intentionally uses diagnostic vertex/normal shading for the first hardware proof. Material ids, names and UVs are parsed, but `.Mat00 -> tDiffuseMap -> DTX` binding is not enabled yet. This isolates world-geometry/GPU stability from the known Vita texture-heap pressure.

## Build verification

Full Release compile and link succeeded with VitaSDK 2026.08.1. The remaining linker messages are the pre-existing mixed enum-size warnings seen in earlier working milestones; there are no undefined references or link errors.

Artifacts:
- `FEARVita_0.38_M29CP.vpk`
- `FEARVita_0.38_M29CP_eboot.bin`
- `FEARVita_M29CP_0.38.elf`
- `FEARVita_M29CP_0.38.velf`
- `FEARVita_M29CP_0.38_param.sfo`

SHA-256:
- VPK: `58b028f48043eb3af279c4acd54bd7f040338cd9db8e874fbdeeedc245e95f77`
- eboot.bin: `9539146b32dbaeccb0075522e9bca3833898823eafb9097e9e8d3f5561bc15f7`
- ELF: `4554241a5bc57f084c7f05b354b2291867514a0bac301e1a47027326bb0f315f`
- VELF: `73ba2427e1bb756c90757734f4215d492fb269ddb5793844228a8e87e21818bd`
- param.sfo: `38cfa5df809ac54970f8737079879eb928085fd78bba7cf53a4a5e4b2ef84af6`

ELF load layout:
- RX: `0x81000000`, FileSiz `0x00ea0848`
- RW: `0x81eb0000`, FileSiz `0x00134e5c`, MemSiz `0x001d8fb0`
- no RX/RW overlap.

The VPK contains the same 22 paths as the complete M29CO package, including all boot/launcher art and all three menu-video caches. `param.sfo` reports `00.38` / `FEAR00001`.

## Decisive hardware test

### Base F.E.A.R. mission

Expected ladder:
1. `FEARVita 0.38 / M29CP`
2. `retail-event renderinit-dispatched`
3. `bink-avplayer ... storage=owned-staging`
4. `world-v113-render parsed ... chunks=...`
5. `world-v113-render shared-render-ready`
6. CharacterFX `add-list-ok lookup=same`
7. stock `ChangeState(GS_PLAYING)`
8. `retail-camera ... world=1 chunks>0 tris>0`
9. `retail-present ... frame-open-before=1`
10. visible diagnostic-shaded 3D world and responsive controls
11. HOME should be able to suspend/leave the application normally.

### Extraction Point performance test

This remains the required direct-3D control path. It should show the authentic performance-test markers, parse the `worlds\\Release\\performance` v113 render section, enter gameplay, draw world chunks and continue without a GPU watchdog.

If a GPU crash remains, capture `fear_ep.log`, `vitaGL.log` and the new `.psp2dmp`. The new logs distinguish parser failure, zero visible chunks, draw failure and post-present GPU failure.
