# FEARVita M29CT / 0.42-WIP
Date: 2026-09-14
Status: WIP handoff, not release-tested.

Last hardware-proven base is M29CS/0.41: Base reaches the real ScreenPostload/PressAnyKey and stock GS_PLAYING; EP Performance Test reaches real World00p rendering with Mat00 diffuse texture resolution. The latest core exposed a CPU Data Abort in Model::GetSocket from the flashlight path, diagnosed as stale native client ModelInstance LTObjRef lifetime.

Re-applied in this reconstructed WIP:
- Native client ModelInstance LTObjRefs are linked into the real LTObject ref list via a runtime helper.
- Native client model destruction calls NotifyObjRefList_Delete before UnbindModelDB/delete.
- Vita held command states are injected into stock FEAR CBindMgr.
- CBindMgr axis reads use Vita Forward/Strafe/Yaw/Pitch analog values.
- Killzone: Mercenary-oriented mapping: LS move, RS look, L aim, R fire, X jump, Square reload, Triangle use, Circle contextual crouch/sprint; D-pad Up flashlight, Left/Right weapon, Down grenade; front touch Left SlowMo, Center melee, Right next grenade; rear touch sprint fallback; SELECT mission, START menu.
- Circle sprint latch is set when Circle is pressed while moving and clears when LS returns to neutral.
- Retail main loop no longer polls the controller a second time before CGameClientShell; the stock shell owns the canonical per-frame poll, avoiding consumed edge events.
- Staged VITA_VERSION 00.42 and RW/init-array base 0x81f00000.

RECONSTRUCTION WARNING: the active previous workspace disappeared before this handoff. This tree was rebuilt from the complete M29CS/0.41 source artifact and the changes above were re-applied from the conversation/code audit. A further native Model00p renderer WIP that had been described in the previous runtime was not persisted and is NOT falsely claimed as present. See M29CT_MODEL00P_V33_NOTES.md.
