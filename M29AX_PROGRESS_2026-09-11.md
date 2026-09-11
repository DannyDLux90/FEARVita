# FEARVita M29AX — D-pad and touchscreen retail-menu navigation

Date: 2026-09-11

## Starting point

M29AW already provides the canonical Killzone-inspired Vita gameplay profile for F.E.A.R., Extraction Point and Perseus Mandate. The base F.E.A.R. first loading screen also has the FEARVita-authored German fallback when the Vita system language is German.

## M29AX changes

### Correct D-pad navigation in retail menus

The gameplay profile intentionally maps D-pad up/down/left/right to SlowMo, grenade, previous weapon and next weapon. The old frontend command bridge interpreted those command ids as unrelated keyboard directions, so the physical D-pad did not behave as an actual menu D-pad.

M29AX checks the physical Vita button state while `GS_SCREEN` or `GS_MENU` is active and translates the four D-pad directions to the matching retail UI arrow keys. Left-stick digital navigation remains available. X/Triangle confirm through the existing Enter path; Circle/START return through Escape.

### Absolute front-touch navigation

The Vita controller backend now exposes the first front-touch contact as normalized X/Y coordinates plus down/pressed/released state. The LithTech bridge makes that state available to the client shell.

While a retail screen or menu is active, normalized touch coordinates are mapped to the Vita framebuffer (960x544) and forwarded through the existing `CInterfaceMgr::OnMouseMove`, `OnLButtonDown` and `OnLButtonUp` paths. This preserves the retail screen, user-menu, system-menu and message-box hit testing instead of inventing a parallel UI.

The existing gameplay front-touch zones remain unchanged: left = flashlight, center = melee, right = next weapon. Their command edges are suppressed as keyboard navigation while the frontend touch-pointer path is active, preventing one tap from also moving the highlighted menu selection.

### Manual and diagnostics identity

The five-page Vita Bubble manual now documents D-pad and touchscreen retail-menu navigation. Startup diagnostics identify this checkpoint as M29AX.

## Validation

Host smoke tests pass:

- `fearvita_controller_input_smoke` — PASS, including absolute front-touch coordinates and press/release edges.
- `fearvita_lithtech_input_bridge_smoke` — PASS, including controller button and touch-state bridge access.
- `git apply --check M29AX.patch` against the M29AW public source export — PASS.

A full Vita ELF/VELF/SELF/VPK rebuild was not run in this environment because the uploaded public source export contains the FEARVita overlay but not the pinned full LithTech upstream checkout required by `FEARVITA_LITHTECH_ROOT`. The uploaded VitaSDK packages are sufficient for the toolchain side once that checkout is present.

## Loading screen status

The M29AW German base-game loading fallback is intentionally unchanged. Existing hardware logs already show `fallback=de-steam-base-intro applied=1` for `Worlds\\Release\\Intro`.

## Gameplay frontier

Unchanged: the real ObjectDLL/server/world runtime remains the blocker after the local single-player handshake. Menu input work does not alter that frontier.
