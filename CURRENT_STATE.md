# FEARVita current state — M29CT / 0.42 — 2026-09-14

**Last hardware-verified package:** M29CS / 0.41  
**Current test package:** M29CT / 0.42

M29CS hardware proved that Base F.E.A.R. reaches the authentic ScreenPostload / PressAnyKey transition, acknowledges it, sends stock ClientInWorld and reaches stock GS_PLAYING. EP -> Performance Test reaches real 3D and resolves/uploads real FEAR `.Mat00 -> tDiffuseMap -> DTX/DDS` world textures.

The 0.41 follow-on crash was symbolized as a CPU Data Abort in Flashlight -> ILTModel::GetSocket caused by stale native-client ModelInstance LTObjRef lifetime. M29CT links native client model refs into the real LTObject ref list and invalidates them with NotifyObjRefList_Delete before destruction.

M29CT also adds an initial real FEAR v33 Model00p renderer: retained mesh/index/bone-weight data, CPU skinning from current node transforms, LOD0 drawing and client model skin/material tracking. The v113 world path remains deferred and bounded, now with 8 MiB mesh + 16 MiB texture LRUs, 256px max world textures, invisible-material suppression, opaque/alpha-additive ordering and a 3000->7000 world triangle budget.

Vita controls are now Killzone: Mercenary-oriented and routed through FEAR's own CBindMgr: left stick move, right stick look, L aim, R fire, X jump, Square reload, Triangle use, Circle crouch/sprint context, D-pad weapon/grenade/flashlight controls, touch SlowMo/melee/grenade selection. The controller is polled once per retail frame so held state and press edges are consistent.

Release compile/link and full VPK packaging succeeded. `APP_VER=00.42`, title ID `FEAR00001`, same 22 package paths as 0.41. RX ends at `0x81EB3D1C` and RW begins at `0x81F00000`, with no overlap.

Required hardware proof: Base must retain its real PressAnyKey transition and avoid the prior Flashlight/socket Data Abort. EP Performance Test must run beyond the 0.41 short textured window, load/render real world materials, show Model00p geometry where visible, and allow full in-level movement/look/actions. See `CURRENT_STATE_M29CT.md` and `NEXT_CHAT_HANDOFF_M29CT_0.42.md`.
