# FEARVita M29AW — Vita defaults, Bubble manual, German Steam-loading fallback

Date: 2026-09-11

## Hardware evidence from M29AV

The base F.E.A.R. preload state machine is now working. `Worlds\\Release\\Intro` reaches `FinishStartGame`, the Vita `STARTGAME_NORMAL` local-session bridge returns success, and the client reaches the explicit `waiting-for-world/server-object-runtime` frontier. The next gameplay blocker remains the real ObjectDLL/server/world runtime, not the loading-screen state machine.

The M29AV loading trace identified the first screen's retail ids as `Level_Intro`, `Briefing_Intro` and `Help_Intro`. The Vita system language is German, while the packed retail StringDB supplied by the current Steam data remains English.

## M29AW changes

### Canonical PS Vita control preset

A single hard-coded Vita profile is now authoritative for F.E.A.R., Extraction Point and Perseus Mandate. It is loaded whenever Vita controls are initialized and is also the exact preset restored by **Restore Defaults**. `SetBindings()` does not erase it when the PC-oriented Configure screen closes, because Vita input is delivered through FEARVita's command-edge bridge rather than through PC ILTInput devices.

Default layout: left stick movement; right stick look; R fire; L aim; X jump; Circle crouch; Square reload; Triangle use/activate; D-pad up SlowMo; D-pad down grenade; D-pad left/right previous/next weapon; SELECT mission objectives; START menu; front-touch left flashlight; front-touch center melee; front-touch right next weapon; rear touch double-tap and hold the second contact to sprint.

### Vita Bubble manual

The old M16 four-page manual was replaced with a current five-page FEARVita manual. Page 5 documents the complete control preset including front and rear touch. The manual also documents the per-campaign logs and the current Steam-language limitation. `project/tools/generate_vita_manual.py` reproduces the PNG pages.

### Loading screen language

Steam's current F.E.A.R. store metadata lists German game-interface support as unavailable. M29AW therefore does not pretend the English Steam StringDB is official German retail data. Instead, for the base-game first mission only, when Vita system language is German and the campaign tag is `fear`, FEARVita applies an original German fallback for mission/level/briefing/help framework text. Expansion campaigns are explicitly excluded from this fallback so base-game wording cannot leak into EP or PM.

The loading diagnostics now also log the mission StringDB id in addition to world, level, briefing and help ids. This lets later campaign-specific localization work be grounded in the actual retail database ids.

## Build

VitaSDK build completed successfully. The private test VPK retains the accepted FEAR/EP/PM menu video caches and campaign artwork from the prior private package. Public source/export artifacts contain no user-provided retail movies or campaign artwork.

## Next gameplay frontier

ObjectDLL/server/world runtime. The client-side loading flow has already reached the handoff and will remain on the loading screen until the real local server can load the world and server objects.
