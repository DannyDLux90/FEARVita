# FEARVita M29AV — Loading UI, Vita controls, server bring-up

Date: 2026-09-11

## Hardware result that motivated this checkpoint

M29AU reaches the actual first-mission loading screen for `Worlds\Release\Intro`. The preload state machine now completes `FinishStartGame`, the local `STARTGAME_NORMAL` shim succeeds, and the client then waits for the missing world/ObjectDLL runtime. The loading loop is therefore no longer blocked by ScreenPreload itself; it is blocked at the real server/world boundary.

## M29AV changes

- Keeps the accepted F.E.A.R./EP/PM frontend, menu videos, system-language behavior and per-campaign logs.
- Adds Vita-native front and rear touch input to the controller backend.
- Reworks the fixed gameplay preset to a Killzone-inspired handheld layout:
  - left stick move, right stick look
  - R fire, L manual aim
  - X jump, Circle crouch, Square reload, Triangle activate/use
  - D-pad up SlowMo, down grenade, left/right previous/next weapon
  - SELECT mission/status entry, START menu
  - front touch left flashlight, center melee, right next weapon
  - rear touch double-tap + hold sprint
- Removes automatic sprint based only on left-stick magnitude so walking remains controllable.
- When the PC profile binding layer has no keyboard/device binding, Vita now exposes the real fixed Vita control label instead of `key unassigned`. The Configure Controls screen uses the same fallback labels.
- Adds localized Vita-overlay strings for the loading-screen framework (`Briefing`, server message, aborted load, unassigned control, connecting message).
- Adds a compact `loading-localize` diagnostic with the exact level/briefing/help StringDB ids. This lets remaining mission-specific English text be localized without guessing.
- Advances the ObjectDLL compile probe: the old public SDK property macros now accept FEAR's optional editor-description tail in ObjectDLL builds. The next compile frontier is no longer the first property macro; it exposes missing private-server contracts such as ICommandDef/ICommandMessageDef, GetClientObject, shadow LOD API and LTOBB.

## Important limitation

M29AV does not claim that the first world is loaded yet. `StartGame` currently reaches the local client-session bridge, but the real FEAR ObjectDLL/server world runtime is still being ported. Loading progress must not be faked; the next milestone is to bring that server/world path online.

## Hardware test focus

1. Start base F.E.A.R. -> Single Player -> New Game -> choose a difficulty.
2. Verify the loading-screen framework is German when the Vita system language is German.
3. Verify the help text shows Vita control names rather than `key unassigned` for mapped commands.
4. If the screen still contains mission-specific English text, save `fear_fear.log`; M29AV logs the exact StringDB ids under `loading-localize`.
5. The load itself is expected to wait until the ObjectDLL/server runtime milestone advances; the log is still useful for confirming the handoff remains stable.
