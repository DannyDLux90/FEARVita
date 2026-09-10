# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AM  
**Date:** 2026-09-10

The F.E.A.R. base-game main menu remains accepted on hardware: the Menu.bik-derived H.264 cache plays through SceAvPlayer and is stretched to the complete 960x544 Vita framebuffer. The retail menu music uses the source WAV at retail-requested gain through the Vita 48 kHz HQ resampler.

M29AM fixes the visual launcher/loading flow after M29AL hardware feedback. The pre-selector boot-progress overlay is now hidden, so startup enters the game selector directly. Boot-progress rendering is armed only after a campaign has actually been selected. The overlay reset now happens before the selected-campaign diagnostic; this prevents the selected EP/PM campaign id from being reset back to F.E.A.R. and fixes the wrong post-selection loading background. The loading phase text remains visible above the progress bar. Private/user-provided artwork is not committed to the public repository.

The previous M29AK database change is retained: the late expansion Surfaces/WeaponFX packed-table record-name anomaly is given a synthetic internal record name, which allows the main EP/PM GADB table to decode fully instead of failing at the last categories. Hardware logs show that this part now succeeds; the remaining EP/PM crash still occurs later around PlayerMgr/weapon initialization and remains the next code target.

Next hardware priority: verify the M29AM visual flow (direct selector, correct EP/PM loading art), then return fresh EP/PM boot logs/core dumps for the remaining menu bring-up.
