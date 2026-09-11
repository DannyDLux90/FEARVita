# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AV  
**Date:** 2026-09-11

The three-game frontend/menu-video milestone remains complete on real PS Vita hardware: **F.E.A.R.**, **Extraction Point** and **Perseus Mandate** reach their retail menus with their original animated menu backgrounds, retail menu audio and Vita-system-language localization.

M29AU hardware testing proved the preload state machine is now running correctly. Base F.E.A.R. selects `Worlds\\Release\\Intro`, enters the real loading screen, executes `FinishStartGame`, accepts the local `STARTGAME_NORMAL` bridge and completes the client-side loading handshake. It then waits indefinitely at the expected missing **ObjectDLL/server/world runtime** boundary. The current loading stall is therefore no longer a menu/preload bug and is not a missing world file.

M29AV adds a Killzone-inspired Vita gameplay control preset and native touch input: left/right sticks move/look, R fires, L aims, X jumps, Circle crouches, Square reloads, Triangle activates, D-pad up/down/left/right provides SlowMo/grenade/previous weapon/next weapon, front touch provides flashlight/melee/next weapon zones, and rear touch double-tap + hold enables sprint. Automatic sprint based only on analog-stick magnitude has been removed.

The PC binding layer has no physical Vita device records yet, so M29AV supplies the actual fixed Vita command labels wherever FEAR would otherwise display `key unassigned`. The Configure Controls screen uses the same labels. Generic loading-screen framework strings are now covered by the Vita system-language overlay, and `loading-localize` diagnostics record the exact dynamic mission name/briefing/help StringDB ids for any remaining campaign-specific English text.

ObjectDLL bring-up also advanced: FEAR's later property macros with optional editor-description strings are now accepted by the public SDK compile path. The next server compile frontier exposes the real missing private contracts (`ICommandDef`/`ICommandMessageDef`, `ILTServer::GetClientObject`, shadow-LOD APIs, `LTOBB`, and related server compatibility work). Playable gameplay is not yet claimed.
