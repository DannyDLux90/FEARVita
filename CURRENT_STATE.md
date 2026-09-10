# FEARVita current state

**Public version:** 0.02  
**Internal checkpoint:** M29AG  
**Date:** 2026-09-10  
**Current milestone:** make the F.E.A.R. retail menu look and sound like the PC version.

The original boot-menu milestone remains complete on real PS Vita hardware: the retail front-end boots, renders, navigates/selects, and Vita system language is bridged to the menu (German verified).

## Latest hardware evidence (M29AF)

The real retail media paths remain correct: `videos\\Menu.bik` is BIKi, 6,301,124 bytes, 512x512, 420 frames at 30 fps, and `Music\\IntroIntLp1v2.wav` decodes as 44.1 kHz stereo PCM. The menu movie contains no audio track; music is separate.

M29AF did not change the visible menu. Its log shows `SCE_SYSMODULE_AVPLAYER` loading successfully, followed by `sceAvPlayerInit` returning raw `0x817432A0` (signed `-2123091296`). FEARVita treated that value as an error before ever calling `sceAvPlayerAddSource`.

The private 420-JPEG fallback also failed: the pack was detected, but every attempted JPEG load returned null. Repeated failed decode attempts explain the observed menu stutter. This fallback is removed from the active M29AG test and no JPEGs are packaged.

## M29AG

M29AG tests the AvPlayer handle semantics directly. Working Vita AvPlayer programs preserve the return value and pass it to `sceAvPlayerAddSource`; M29AG therefore rejects explicit `0x806A00xx` AvPlayer error values but no longer rejects an otherwise non-zero handle merely because its sign bit is set. The hardware log includes the raw/signed value, an address-to-memblock probe, acceptance decision, and the subsequent AddSource result.

Video caches now mirror the game's virtual Bink paths (`videos\\foo.bik` -> `video_cache/videos/foo.mp4`). This is the intended scalable bridge for the menu and later in-game cinematics. Public source never ships converted game movies.

Audio is also moved closer to the PC reference: FEARVita's extra `0.72` music and `0.90` UI bus gains are removed, as is the block-wide limiter that could duck music when UI sounds overlap. The game/master/class volume is authoritative; only samples that actually exceed full scale are clamped. The exact retail menu WAV is exported once for lossless comparison after the next hardware run.

## Known steps to PC-like menu: 3

1. Hardware-verify the real Menu.bik-derived MP4 through AvPlayer and finish movie sizing/loop behavior.
2. Hardware-verify/tune source-faithful background music against the PC reference.
3. Finish packed StringDB values, original/PC-nearer font, and final visual/layout polish.
