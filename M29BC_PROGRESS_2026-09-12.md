# FEARVita M29BC progress — 2026-09-12

## Hardware evidence from M29BB
M29BB proves the client/server LTObjRef ownership-dispatch fix on real Vita hardware: the title reaches the retail main menus again. F.E.A.R. and Perseus Mandate can proceed into the new-game preload path; Extraction Point reaches the same path but its M29BB run generated a Vita core dump.

## Retail mission briefing restoration
The Vita loading-screen compatibility path previously overwrote the retail MissionDB/StringDB values for `Mission_01 / Level_Intro / Briefing_Intro / Help_Intro` with a handwritten German placeholder. M29BC disables that placeholder path. `CLoadingScreen::UpdateMissionInfo` now leaves the normal retail values from MissionDB/StringDB authoritative and logs `[loading-localize] source=retail-missiondb-stringdb placeholder=0`. No replacement mission text is invented by FEARVita.

## Main-menu music verification
The retail LayoutDB path remains authoritative. Current hardware logs select `Music\IntroIntLp1v2.wav` for the loaded menu. M29BC does not substitute another title; instead the Vita sound backend now logs the resolved VFS source/archive plus file size, RIFF data offset/length and FNV-1a content hash for this track. The next hardware log can therefore distinguish wrong database selection from wrong VFS bytes/playback behavior.

## Extraction Point M29BB crash
The uploaded EP core stops the `fearvita_pcm_mixer` thread with a data abort inside `MixerThread`; the faulting iteration holds an invalid candidate sound pointer (`0x000024d1`). The main game thread has already entered the preload/loading-screen path.

M29BC replaces the heap-node based `std::unordered_set<VitaSound*>` registry with a fixed 512-slot mutex-protected pointer table. Playback, validity checks, pause/resume, mixer iteration, auto-release and KillSound use the same storage. This directly removes the observed hash-node traversal failure mode but does not claim no other memory bug can exist.

## Real local server/world bootstrap
M29BB intentionally stopped after the accepted local StartGame handshake and waited for server/world runtime. M29BC removes that stop and wires the real upstream runtime into the Vita path:

1. `ILTClient::StartGame` calls `FearVita_RuntimePrepareLocalServer`.
2. A real `CServerMgr` is allocated and initialized.
3. The exact FEAR StartGame game-info bytes are copied into the server.
4. The mounted retail VFS is registered as the server resource tree.
5. `CServerMgr::LoadBinaries()` loads the statically linked real ObjectDLL.
6. The original `local` driver is selected with `Listen("local", ...)`.
7. Mission preload calls `CServerMgr::DoStartWorld("Worlds\Release\Intro", LOADWORLD_LOADWORLDOBJECTS | LOADWORLD_RUNWORLD, ...)`.
8. After a real world start, `CServerMgr::Update` is pumped from the normal retail frame loop.

No `GS_PLAYING`, MID_START_LEVEL, object, world or success state is fabricated. Failure remains visible through explicit `[server-world]` diagnostics.

## Build closure
M29BC adds the original upstream server/world interface implementations required by `CServerMgr::Init`, ObjectDLL startup and BSP world loading (server ILTCommon/Physics/Model/Sound, ConsoleState, Server/Shared BSP, BlindObjectData, shared ILTCommon/model implementation, world-info parsing and swept-sphere intersection support).

The complete ARM executable links with no undefined references. ELF, VELF, SELF and the 22-entry VPK all pass local validation. M29BC is not hardware validated.