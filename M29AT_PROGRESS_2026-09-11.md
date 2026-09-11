# M29AT progress — per-campaign logs, weapon priority controls, first single-player start bridge

## Confirmed M29AS hardware state

- Vita system language is German and the language overlay is active again.
- FEAR/EP/PM frontend/video milestone remains accepted.
- WeaponDB and ClientWeaponMgr initialize successfully; base FEAR creates all 19 client weapon slots.
- The Weapons options screen already had working retail priority data, but Vita controller UX only made selection obvious; reordering was not practical.

## M29AT changes

### Separate hardware logs

The launcher and each campaign now have separate persistent logs:

- `ux0:data/FEARVita/fear_launcher.log`
- `ux0:data/FEARVita/fear_fear.log`
- `ux0:data/FEARVita/fear_ep.log`
- `ux0:data/FEARVita/fear_pm.log`

Selecting a campaign switches diagnostics to its own file and rewrites checkpoint/language/campaign context at the top.

### Weapon priority menu

The retail Weapons screen keeps its original X-to-select behavior. Once a weapon is selected:

- D-pad Left moves it one slot up in priority.
- D-pad Right moves it one slot down in priority.
- The original change sound is played.
- Leaving the screen keeps the existing retail SaveList/Profile save path, and M29AT logs the saved count.

This is an options/menu priority editor only; it does not claim weapon gameplay is complete.

### First single-player / ingame bring-up bridge

The menu-only Vita ILTClient previously made New Game impossible by design: `StartGame` returned `LT_UNSUPPORTED`, `IsConnected` was always false and `SendToServer` was unavailable.

M29AT adds a deliberately limited local single-player session shim for `STARTGAME_NORMAL` only. It allows the authentic client path to advance through New Game -> first mission/world -> preload -> StartClientServer while logging every seam. Multiplayer/host/client networking remains unsupported.

Because the full ObjectDLL/server transport is not online yet, M29AT deliberately does **not** construct the `MID_START_GAME` / `MID_START_LEVEL` CAutoMessages on Vita. Those require the real engine/server `ILTCommon` path. Instead, the client enters the normal loading state, accepts the selected world locally and records that it is waiting for the world/server-object runtime.

New trace categories include `ingame-start`, `ingame-connection`, and `ingame-client`.

## Full server/ObjectDLL frontier

A compile probe of the FEAR ObjectDLL target confirms that the next true gameplay milestone is not a one-switch enable. Initial blockers include server-object property macro ABI differences and missing server-side SDK/API pieces (for example property macro argument variants and ILTServer methods used by FEAR ObjectDLL). This work is now the main frontier after the M29AT hardware trace identifies how far the client loading path advances.

## Hardware test

Start with base F.E.A.R.: Main menu -> Single Player -> New Game -> choose a difficulty. Let it proceed until it loads, hangs, exits or crashes, then copy `ux0:data/FEARVita/fear_fear.log` and any new core dump.

For the weapon priority UI: Options -> Weapons -> X on a weapon, then Left/Right to reorder; leave the screen and re-enter to confirm persistence.

Do not treat M29AT as playable gameplay yet. Its purpose is to move from the completed frontend into the first real single-player loading/runtime seam and make the remaining blocker exact.
