# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AE  
**Date:** 2026-09-10  
**Current milestone:** make the F.E.A.R. retail menu look and sound like the PC version.

The original boot-menu milestone remains complete on real PS Vita hardware: the retail front-end boots, renders, navigates/selects, and Vita system language is bridged to the menu (German verified).

## Latest hardware evidence (M29AD)

- `videos\\Menu.bik` is found and parsed as BIKi.
- Exact retail movie: 6,301,124 bytes, 512x512, 420 frames, 30 fps, 0 audio tracks.
- The movie exports successfully to `ux0:data/FEARVita/debug/Menu.bik`.
- Separate menu music `Music\\IntroIntLp1v2.wav` decodes as 44.1 kHz stereo PCM.
- HQ Vita output is active: 48 kHz stereo, 12-tap sinc resampler + float headroom limiter.
- M29AD fails at `sceAvPlayerInit` before the source is opened (`-2123091296`).

## M29AE change

M29AE changes the decoded-video allocator from CDRAM to `SCE_KERNEL_MEMBLOCK_TYPE_USER_MAIN_PHYCONT_NC_RW`, with 1 MiB physical-contiguous alignment and GXM mapping. It also uses five output frame buffers and base priority `0xA0`.

The exported Bink was converted to a video-only H.264 constrained-baseline/yuv420p MP4 cache. M29AE checks `ux0:data/FEARVita/cache/Menu.mp4`, then private `app0:cache/Menu.mp4`, then the raw exported Bink diagnostic probe. No retail movie/audio is committed.

## Known steps to PC-like menu: 3

1. Hardware-verify visible `Menu.bik`-derived playback and finish movie presentation/loop behavior.
2. Hardware-verify/tune the HQ background-music path.
3. Finish packed StringDB values, original/PC-nearer font, and final visual polish.
