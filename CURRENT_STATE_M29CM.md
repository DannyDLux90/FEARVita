# FEARVita current state — M29CM / 0.35 — 2026-09-14

## Hardware evidence from M29CL / 0.34

Both retail campaigns now cross the former ClientInWorld blocker and reach the stock gameplay state transition.

Observed in F.E.A.R. and Extraction Point:
- paired local `client-inworld-gameutil-fallback raw-worldcrc` / `server-inworld-gameutil-fallback raw-worldcrc` succeeds;
- player state reaches Alive;
- stock postload path executes `ChangeState(GS_PLAYING)`;
- no gameplay state is forged.

The first deterministic failure after that transition is local-player CharacterFX registration:

```
client-player-sfx-create id=11
characterfx-stage allocated
characterfx-stage init-ok
characterfx-stage create-object-ok
characterfx-stage add-list-failed
client-player-characterfx-create-failed
```

F.E.A.R. repeats this sequence heavily; Extraction Point also repeats it after entering gameplay.

## Root cause

`SFX_CHARACTER_ID` is dynamic SFX id 11 and its configured list capacity is 200. `CSpecialFXList::Add()` returns false when the list backing arrays have never been created.

On Vita, `CGameClientShell::OnEngineInitialized()` takes an early frontend return before the normal desktop-side `m_sfxMgr.Init(g_pLTClient)` block. Consequently the dynamic `CSFXMgr` lists remain at constructor defaults. The first real local-player CharacterFX reaches allocation, `Init`, and `CreateObject`, then fails exactly at insertion into that uninitialized list.

## M29CM change

Vita only: initialize `m_sfxMgr` before the frontend early return. The normal non-Vita initialization order is unchanged.

Expected new startup/stage markers:
- `FEARVita 0.35 / M29CM`
- `pre-sfx-mgr`
- `sfx-mgr-ok`

Expected CharacterFX result:
- `characterfx-stage add-list-ok lookup=same`
- no continuing `client-player-characterfx-create-failed` storm

## Architecture invariants retained

- authentic local-client flow only;
- real server-side player;
- stock StartGameRequest, postload and ClientInWorld flow;
- separate server/client objects and native client ModelInstance proxy;
- real CharacterFX SFX create message;
- stock OnEnterWorld;
- stock state machine reaches `GS_PLAYING`; never force it;
- no fake/model-less player;
- no broad unsafe HOBJECT forwarding.

## Next Vita test

Run both F.E.A.R. and Extraction Point. Capture `fear_fear.log`, `fear_ep.log`, `vitaGL.log`, and any new PSP2 core dump.

The decisive ladder is:
1. `0.35 / M29CM`
2. `sfx-mgr-ok`
3. local-player body init completes
4. `characterfx-stage add-list-ok lookup=same`
5. stock `ChangeState(GS_PLAYING)`
6. first stable gameplay frames / input
7. if a GPU crash remains, analyze it only after confirming the CharacterFX storm is gone
