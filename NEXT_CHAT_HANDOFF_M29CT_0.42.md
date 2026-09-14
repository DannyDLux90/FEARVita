# NEXT CHAT HANDOFF — FEARVita M29CT / 0.42

Continue from M29CT/0.42. Do not regress the authentic local-client/server flow, stock postload ClientInWorld, real server player, separate client ModelInstance proxy, CharacterFX, or stock GS_PLAYING state machine.

## Mandatory first action after user hardware test
Inspect both `fear_fear.log` and `fear_ep.log`. EP Performance Test is the mandatory direct-3D control path.

## What M29CT adds
- Real LTObjRef lifecycle for native client ModelInstance objects, fixing the 0.41 Flashlight/GetSocket stale-reference Data Abort.
- Real v33 Model00p sidecar geometry retained by model_load and rendered using current node transforms / CPU skinning.
- First hardware proof renders Model00p double-sided (`CullMode::None`) to avoid D3D/Vita winding inversion hiding valid geometry after CPU projection; re-enable backface culling only after orientation is confirmed.
- Killzone: Mercenary-oriented controller mapping injected into FEAR CBindMgr, including real analog movement/look.
- Single controller poll per retail frame so press edges are not consumed twice.
- World render hardening: alpha/additive ordering, invisible-material skip, texture warmup, 8 MiB mesh + 16 MiB texture LRUs, 256px max world texture dimension, 3000->7000 world triangle budget.
- RW link split is 0x81F00000. Final RX ends at 0x81EB3D3C.

## Hardware checks
### Base F.E.A.R.
- PressAnyKey / ScreenPostload still appears.
- Acknowledge with X.
- Reach stock GS_PLAYING.
- No socket/Flashlight Data Abort.
- Test LS, RS, L, R, X, Square, Triangle, Circle crouch/sprint, weapon/grenade/flashlight controls.
- Test HOME / resume.

### Extraction Point -> Performance Test
- Must reach direct 3D.
- Must run beyond the 0.41 four-frame texture window and old crash boundary.
- Look for `world-v113-cache`, `world-texture`, `model-render frame`, `retail-camera`.
- Expect warm budget 3000 then steady budget up to 7000.
- Check `controls-move` and `controls-look` while actually moving the sticks.
- Check whether gun/other native Model00p objects are visible and `model-tris > 0`.
- Model00p is deliberately double-sided in this proof build; if geometry is visible/oriented correctly, restore selective backface culling later.

## If it crashes
Request the new `.psp2dmp`, both logs, and `vitaGL.log` if present. Symbolize CPU dumps against the M29CT unstripped ELF if still available under `/mnt/data/fear_work/m29ay_build/FEARVita`.

## Honest renderer status
Static world diffuse texturing is proven in 0.41; full FEAR lighting/material parity is not. M29CT's dynamic Model00p rendering is new and not hardware-proven yet. Preserve these distinctions in user-facing claims.
