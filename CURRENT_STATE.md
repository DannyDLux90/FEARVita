# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AJ  
**Date:** 2026-09-10

The F.E.A.R. base-game main menu is now accepted on hardware: the Menu.bik-derived H.264 cache plays through SceAvPlayer and is stretched to the complete 960x544 Vita framebuffer. The retail menu music uses the source WAV at retail-requested gain through the Vita 48 kHz HQ resampler.

M29AI replaced the temporary text-heavy boot overlay with a minimal campaign-specific loading presentation: background art plus progress bar and percentage only. Proprietary art is not included in public source; private/user builds can place it under `project/boot_art/`.

M29AJ targets the remaining Extraction Point / Perseus Mandate menu boot failure. Both supplied M29AH logs reach PlayerMgr MoveMgr and fail before WeaponMgr completion. Both expansion main GADB tables are substantially decoded but stop late on a currently unsupported record-name construct. M29AJ preserves valid RecordLinks into already-decoded categories and adds a Vita frontend-only WeaponMgr failure fallback so gameplay weapon initialization cannot abort an otherwise usable menu frontend.

Next hardware priority: test EP and PM and return their M29AJ logs. A successful run should continue beyond `player-movemgr-ok` toward `frontend-main-ok` / `complete`.
