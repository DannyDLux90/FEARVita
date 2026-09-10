# M29AI / 0.02 Progress — minimal boot screen with campaign art

## User-facing goal
Keep the now-correct F.E.A.R. main menu as-is, but replace the temporary debug-heavy
boot/loading overlay with a much cleaner presentation and campaign-specific art.

## M29AI changes
- Replaced the previous text-heavy diagnostic boot overlay with a minimal layout.
- Added campaign-specific fullscreen boot art for:
  - F.E.A.R.
  - Extraction Point
  - Perseus Mandate
- Reduced visible overlay content to the essentials only:
  - background artwork
  - progress bar
  - percentage readout
- Removed the large debug title, phase, detail and helper text from the loading screen.
- Kept the internal diagnostic/logging pipeline unchanged so EP/PM boot failures remain traceable.
- Private test builds may package user-provided campaign art under `app0:boot_art/`; public source does not ship proprietary art.

## Add-on state
Extraction Point and Perseus Mandate still fail before reaching their finished frontend.
Current supplied logs end after `player-movemgr-ok` with:
- `engine-init-failed result=1`
- immediate fail-safe exit

This means the add-ons still have a pre-menu boot blocker independent of later per-campaign
video cache work.

## Next hardware test
1. Verify that the loading screen now shows the correct art per campaign with only the minimal bar/percent UI.
2. Confirm that the F.E.A.R. main menu remains unchanged and acceptable.
3. Continue collecting EP/PM boot logs after campaign selection so the remaining add-on boot failure can be isolated.
