# FEARVita current state — M29CT / 0.42-WIP — 2026-09-14

**Last hardware-proven package:** M29CS / 0.41  
**Current branch:** `m29ct-0.42-wip-handoff`  
**Status:** reconstruction/WIP handoff only; no 0.42 VPK is release-ready.

M29CS/0.41 proved that Base F.E.A.R. again reaches the real ScreenPostload/PressAnyKey, acknowledges it, sends stock ClientInWorld and reaches stock GS_PLAYING. EP -> Performance Test reaches real v113 World00p rendering and real `.Mat00 -> tDiffuseMap -> DDS/DTX` diffuse texture loads.

The latest hardware core then exposed the next CPU-side frontier: a Data Abort in `Model::GetSocket` through the flashlight transform path. Analysis points to native client `ModelInstance` references being accepted by the Vita ILTClient without participating in the real `LTObject::m_RefList`, while destruction also skipped `NotifyObjRefList_Delete()`.

M29CT WIP re-applies the ObjRef lifetime fix, routes Vita held commands and analog Forward/Strafe/Yaw/Pitch through stock `CBindMgr`, adopts Killzone: Mercenary-style Vita controls, removes the duplicate retail-loop controller poll that could consume press edges, and stages the Vita RW/init-array base at `0x81f00000` for the larger image.

Important reconstruction warning: the live workspace from the prior runtime session disappeared before this handoff. The complete M29CS/0.41 source artifact was preserved and used as the verified reconstruction base. A further native Model00p renderer WIP described in that session was not persisted; it is documented in `M29CT_MODEL00P_V33_NOTES.md` rather than being falsely claimed as present.

See `CURRENT_STATE_M29CT_WIP.md`, `NEXT_CHAT_HANDOFF_M29CT_0.42_WIP.md`, and `patches/M29CS_to_M29CT_WIP.patch`.
