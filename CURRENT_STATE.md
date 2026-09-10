# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AH  
**Date:** 2026-09-10

M29AG is the real-hardware video breakthrough: SceAvPlayer accepts the generated H.264 cache and returns the first 512x512 YVU420P2 frame. The value `0x817432A0` is an opaque AvPlayer handle, not a failure merely because its signed form is negative.

M29AH stretches the PC menu movie across the complete 960x544 Vita framebuffer and namespaces converted movie caches per campaign (`fear`, `ep`, `pm`) so two campaigns cannot collide on the same virtual `videos\\Menu.bik` name. The old JPEG frame fallback is removed.

The correct retail menu audio source is `Music\\IntroIntLp1v2.wav`, 44.1 kHz stereo, looped. FEARVita exports it unchanged for validation and mixes it at the retail-requested gain through the Vita 48 kHz HQ sinc path.

Extraction Point and Perseus Mandate still require current hardware diagnosis. Their pre-M29X failures had separate causes before any menu video was needed. The VFS/network fixes remain present, but successful add-on menu entry has not been verified on current hardware. If an add-on reaches ScreenMovie, M29AH exports its menu Bink separately for conversion.

## Remaining PC-menu work
1. Hardware-verify M29AH fullscreen movie presentation and final loop/timing.
2. Finish exact audio A/B tuning only if the source-faithful current path still differs perceptually.
3. Finish packed StringDB values, original/PC-nearer font, and final visual polish.
