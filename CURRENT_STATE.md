# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AF  
**Date:** 2026-09-10  
**Current milestone:** make the F.E.A.R. retail menu look and sound like the PC version.

The original boot-menu milestone remains complete on real PS Vita hardware: the retail front-end boots, renders, navigates/selects, and Vita system language is bridged to the menu (German verified).

## M29AE hardware result

The 2026-09-10 M29AE hardware run confirms that the private MP4 cache is present at `app0:cache/Menu.mp4`, but `sceAvPlayerInit` still fails with signed result `-2123091296` (`0x817432A0`) before `sceAvPlayerAddSource` is reached. Changing the decoded-frame allocator to physically contiguous main memory did not change that failure.

The same run still confirms the retail Bink and audio paths: `Menu.bik` is 512x512 / 420 frames / 30 fps and the separate `Music\\IntroIntLp1v2.wav` is decoded as 44.1 kHz stereo PCM. The HQ Vita audio output remains 48 kHz stereo with the 12-tap sinc resampler and float headroom limiter.

## M29AF change

M29AF keeps the AvPlayer path as a diagnostic/optional fast path but no longer lets it block visible menu-video progress. If AvPlayer cannot initialize and a private frame pack exists at `app0:menu_frames/000.jpg` through `419.jpg`, FEARVita decodes the user's Menu.bik-derived JPEG frames with libjpeg/vita2d and renders them at the original 30-fps timeline. Frame selection is process-time based, so slow decodes naturally skip ahead instead of slowing the menu clock. The log reports frame-pack detection, first-frame decode time, and a 30-frame decode performance sample.

The repository contains `project/tools/prepare_menu_framepack.py`, but never the generated frames or any retail asset.

## Next hardware test

Install the private M29AF VPK and enter the main menu. The decisive new log lines are:

- `bink-jpeg frame-pack-present`
- `bink-jpeg first-frame`
- `bink-jpeg decode-perf`

The visible result should be the real F.E.A.R. animated menu background (logo/radar imagery) instead of the uniform green fallback. Return the new `fear_menu_boot.log` and a photo/video. Also report whether menu music sounds better, equal, or worse than M29AE.

## Known steps to PC-like menu: 3

1. Hardware-verify visible `Menu.bik`-derived playback and finish movie sizing/loop behavior.
2. Hardware-verify/tune the HQ background-music path.
3. Finish packed StringDB values, original/PC-nearer font, and final visual polish.
