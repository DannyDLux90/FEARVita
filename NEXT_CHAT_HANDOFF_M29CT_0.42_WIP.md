# NEXT CHAT — FEARVita M29CT / 0.42-WIP

Use this workspace/source ZIP as the starting point. Do not start from 0.40.

## First tasks
1. Reconfigure the Vita build tree; archived CMakeCache contains stale absolute paths.
2. Compile the re-applied input/BindMgr/ObjRef files first.
3. Verify LTObjRef helper + NotifyObjRefList_Delete closes the 0.41 flashlight/Model::GetSocket UAF.
4. Restore/finish native Model00p v33 rendering from M29CT_MODEL00P_V33_NOTES.md and public haekb/io_scene_lithtech PR #24 `reader_model00p_pc.py`.
5. Continue EP Performance Test rendering: correct material states/textures, alpha/transparent passes, worldmodels/props/models, stable cache lifetime.
6. Full link, verify RX/RW no overlap with 0x81f00000 base, package complete 22-file VPK only after build passes.

## Mandatory hardware matrix
Base FEAR: PressAnyKey must remain present; stock ClientInWorld and GS_PLAYING; no result=67; no socket UAF; controls work in real level.
EP Performance Test: direct 3D path; stable beyond prior limit; real textures/materials; LS movement + RS look + actions; visible Model00p weapon/objects after renderer restoration; no CPU Data Abort/GPU watchdog.

## User priorities
- Everything must be displayed correctly, not just diagnostic geometry.
- Performance Test must load textures and all other scene content correctly.
- Controls in-level are mandatory and should feel like Killzone: Mercenary on Vita.
