# FEARVita M29CT / 0.42 — Current State

## Purpose
M29CT is the first hardware candidate combining the stable 0.41 deferred Jupiter-EX world path with native FEAR v33 Model00p rendering, corrected native-client LTObjRef lifetime, and Killzone: Mercenary-style Vita controls routed through FEAR's own CBindMgr.

## Proven before this build
- Base 0.41 reaches the authentic ScreenPostload / PressAnyKey transition, acknowledges it, sends stock ClientInWorld, and reaches GS_PLAYING.
- EP Performance Test 0.41 reaches real 3D and resolves/uploads real `.Mat00 -> tDiffuseMap -> DTX/DDS` textures.
- 0.41's follow-on CPU crash was a stale native-client ModelInstance LTObjRef used by Flashlight socket lookup, not a GPU watchdog.

## M29CT changes
- Native client ModelInstance LTObjRefs are linked into LTObject::m_RefList and are invalidated with NotifyObjRefList_Delete before destruction.
- FEAR v33 Model00p mesh/index/bone-weight data is retained and rendered through the Vita camera path using CPU skinning and LOD0.
- Client model texture resources / skins are tracked and stale texture slots are released on rebind.
- First-hardware Model00p proof is deliberately double-sided (`CullMode::None`) because the CPU projection flips Y into Vita screen space; this prevents valid weapon/prop/character meshes disappearing from a D3D/Vita winding mismatch. Backface culling can be restored after hardware orientation is proven.
- World renderer keeps deferred v113 geometry and real diffuse materials, with separate opaque/alpha-additive ordering, invisible-material suppression, UV repeat, conservative LRU caches, and texture warmup.
- World mesh cache: 8 MiB. World texture cache: 16 MiB. Max uploaded world texture dimension: 256 px.
- World triangle budget warms at 3000 and may rise to 7000; native Model00p budget is 3500 triangles.
- Projected geometry no longer burns the vita2d transient pool for an extra CPU/GPU intermediate copy.
- RX/RW split moved to 0x81F00000. Final ELF RX ends at 0x81EB3D3C; no segment overlap.

## Vita controls (Killzone: Mercenary-oriented)
- Left stick: move / strafe
- Right stick: look
- L: aim / iron sight
- R: fire
- X: jump
- Square: reload
- Triangle: use / interact
- Circle: crouch while stationary; start sprint while moving; sprint remains latched until left stick returns neutral
- D-pad left/right: previous / next weapon
- D-pad down: quick grenade
- D-pad up: flashlight
- Front touch left: SlowMo
- Front touch center: melee
- Front touch right: next grenade type
- Rear touch: alternate sprint (double-tap + hold)
- SELECT: mission/objectives
- START: pause/menu
- START+SELECT: emergency exit

The Vita input snapshot is polled once per retail frame. Held buttons and analog axes are injected into FEAR CBindMgr, so CMoveMgr and PlayerMgr consume native FEAR command state instead of a parallel event-only path.

## Diagnostics expected on hardware
- `controls-move` — analog axes and FEAR movement flags
- `controls-look` — raw right-stick plus applied yaw/pitch
- `model-render registered` and `model-render frame`
- `retail-camera ... model-tris=`
- `world-material`, `world-texture`, `world-v113-cache`

## Packaging verification
- APP_VER: 00.42
- TITLE_ID: FEAR00001
- VPK entries: 22, identical file list to 0.41
- Private boot/launcher/video assets are packaged only in the private VPK and are not included in the source snapshot/public repository.

## Hardware success criteria
1. Base normal mission: PressAnyKey remains present, GS_PLAYING follows, no Flashlight/socket Data Abort, HOME remains usable.
2. EP Performance Test: direct 3D runs beyond the previous short window without CPU/GPU crash, real world textures appear, and Model00p geometry begins drawing where visible.
3. Gameplay controls work in-level: movement, look, aim, fire, jump, reload, use, crouch and sprint.

## Known limits / not yet claimed
- M29CT Model00p rendering is hardware-unproven.
- World rendering is diffuse-first, not full FEAR normal/specular/emissive/lightmap parity.
- Model rendering currently uses LOD0 and a diffuse-first path rather than the complete original renderstyle stack.
- Do not call the renderer final until the hardware run confirms stability and correctness.
