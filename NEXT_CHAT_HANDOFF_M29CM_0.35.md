# FEARVita next-chat handoff — M29CM / 0.35 — 2026-09-14

## Canonical state

- Workspace: `/mnt/data/fear_work`
- Project: `/mnt/data/fear_work/m29ay_src/project`
- LithTech tree: `/mnt/data/fear_work/m29ay_lithtech/lithtech-master`
- Build: `/mnt/data/fear_work/m29ay_build`
- VitaSDK: `/mnt/data/vitasdk_m29bu`
- Milestone/version: **M29CM / 0.35**

## What M29CL hardware proved

M29CL / 0.34 crosses ClientInWorld and reaches the authentic stock `ChangeState(GS_PLAYING)` in both F.E.A.R. and Extraction Point.

The immediate post-transition blocker is a repeatable local-player CharacterFX creation storm. `CreateObject()` succeeds but insertion into `CSFXMgr` fails with `characterfx-stage add-list-failed`.

## M29CM root cause and fix

The Vita frontend in `CGameClientShell::OnEngineInitialized()` returns before the normal `m_sfxMgr.Init(g_pLTClient)` call. Dynamic SpecialFX lists are therefore never created on Vita. `SFX_CHARACTER_ID` (11) later reaches a list whose backing arrays are null and `CSpecialFXList::Add()` returns false.

M29CM initializes `m_sfxMgr` inside the Vita frontend path before the early return. Desktop logic is not reordered.

Changed files:
- `FEAR/ClientShellDLL/GameClientShell.cpp`
- `project/CMakeLists.txt` (00.34 -> 00.35)
- `project/src/main.cpp` (M29CM diagnostics)

Patch: `patches/M29CM.patch`

## Do not regress

Keep every M29CL and earlier compatibility fix, especially:
- local ClientInWorld raw-worldcrc fallback only when ILTGameUtil is unavailable;
- shared texture cache/OOM guard;
- player Model00p v33/v34 parsing and animation/physics fixes;
- separate client proxy/native ModelInstance;
- narrow CharacterFX local-player retargeting;
- sanitized `MID_CLIENT_PLAYER_UPDATE`;
- deferred gameplay manager init;
- client/server interface-scope isolation;
- stock server frame bracket;
- dynamic SharedFXStructs serializer context;
- PlayerBody null-model guard.

Never force `GS_PLAYING` and never replace CharacterFX with a fake path.

## Next hardware ladder

1. startup: `FEARVita 0.35 / M29CM`
2. init: `pre-sfx-mgr` then `sfx-mgr-ok`
3. local player init completes
4. CharacterFX: `add-list-ok lookup=same`
5. no repeated CharacterFX create-failed storm
6. stock `ChangeState(GS_PLAYING)`
7. establish visible gameplay frame and input
8. if GPU crash persists, use the new dump/vitaGL log after step 4 is confirmed
