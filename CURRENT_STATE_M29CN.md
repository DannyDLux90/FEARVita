# FEARVita current state — M29CN / 0.36 — 2026-09-14

## M29CM hardware result

M29CM fixed the dynamic SpecialFX manager initialization bug. Hardware logs now show `sfx-mgr-ok`, local-player CharacterFX registration succeeds with `characterfx-stage add-list-ok lookup=same`, and the stock retail path reaches `ChangeState(GS_PLAYING)` in both F.E.A.R. and Extraction Point.

Base F.E.A.R. continues running for thousands of retail-loop frames after the user confirms the postload screen. The apparent freeze is therefore visual, not the former client/server handoff or CharacterFX recreate storm.

## Current rendering frontier

The Vita ILTClient implementation still had `RenderCamera` as a no-op. At `GS_PLAYING`, the retail interface path also stops automatically clearing the loading screen. Therefore the last postload image can remain visible while the game simulation continues underneath it.

The original desktop engine sends the retail camera into the client scene renderer. That world-scene submit path is not yet wired to the Vita renderer. Existing Vita groundwork covers frame/present handling plus selected render-state and vertex-buffer compatibility, but does not yet submit the loaded Jupiter world scene.

## M29CN change

M29CN is a diagnostic gameplay-present milestone, not a fake world renderer.

- version/package marker: 0.36 / M29CN
- `RenderCamera` now opens/clears a fresh gameplay frame and logs `retail-camera`
- stock HUD/interface rendering remains after the camera call
- `FlipScreen` logs `retail-present`
- controller state logs `input-heartbeat` every 600 retail frames
- no forced `GS_PLAYING`
- no fabricated world geometry
- full private launcher/menu assets restored to the hardware-test VPK using the user-provided previous package as local packaging input only

Expected hardware proof after postload confirmation:

1. `ChangeState(GS_PLAYING)`
2. visible transition away from the frozen loadscreen to a fresh dark gameplay frame / stock HUD
3. `retail-camera` heartbeats
4. `retail-present` heartbeats
5. `input-heartbeat` continues and changes when controls are used

If this ladder succeeds, the next real blocker is the Retail camera -> Jupiter client world-scene submit bridge.

## EP benchmark GPU crash

The separately reproduced EP benchmark GPU crash remains a renderer issue. The supplied PSP2 core dump contains Vita GPU/GXM crash state, but the precise offending draw has not yet been established. It should be debugged independently from the Base F.E.A.R. gameplay-state transition, which is now proven alive.

## Packaging

The M29CN test VPK is complete. Compared with the user-provided full M29CL VPK it contains all non-directory asset files, including 3 boot graphics, 4 launcher graphics, and all 3 menu videos. Private binary/media assets are not included in the public source snapshot or GitHub branch.
