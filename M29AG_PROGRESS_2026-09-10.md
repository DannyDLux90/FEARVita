# M29AG progress — 2026-09-10

## Hardware evidence entering M29AG

The M29AF hardware run made two separate issues explicit.

1. `SCE_SYSMODULE_AVPLAYER` loads successfully, but FEARVita still labels the value returned by `sceAvPlayerInit` (`0x817432A0`, signed `-2123091296`) as a failure solely because `SceAvPlayerHandle` is typedef'd as a signed `int`. Therefore `sceAvPlayerAddSource` is never reached.
2. The private JPEG pack is present, but every attempted `vita2d_load_JPEG_file` returns null. The repeated failed file/decode attempts add frame-time overhead, explaining the new menu stutter without changing the image.

The JPEG path is therefore retired from the active M29AG test and no JPEGs are packaged.

## AvPlayer opaque-handle test

M29AG follows the call pattern used by working Vita AvPlayer homebrew: preserve the non-zero handle value and call `sceAvPlayerAddSource` instead of rejecting it only because bit 31 is set. Explicit values in the `0x806A00xx` AvPlayer error facility are still rejected. The hardware log records the signed value, raw hex value, whether it looks like a known AvPlayer error, the containing memblock probe, and whether it was accepted.

The video cache is now generic: a retail virtual path such as `videos\\Menu.bik` resolves to `video_cache/videos/menu.mp4`. This scales to later Bink cinematics without one-file-per-frame installs. `project/tools/prepare_video_cache.py` recursively converts user-owned exported `.bik` files into this mirrored MP4 layout.

The private M29AG test VPK contains exactly one user-derived video asset: `app0:video_cache/videos/menu.mp4` (H.264 Constrained Baseline, yuv420p, 512x512, 30 fps). Public source/release builds contain no retail-derived media.

## Audio reference correction

The Vita backend was applying FEARVita-only bus multipliers (`0.72` music, `0.90` non-music) plus a block-wide headroom limiter. Those alter the retail relative level and can duck the background track when UI sounds overlap it. M29AG removes the extra bus multipliers and block-wide limiter; retail PlaySound/master/class volume remains authoritative and only an individual output sample that actually exceeds full scale is clamped.

The original `Music\\IntroIntLp1v2.wav` is exported once to `ux0:data/FEARVita/debug/IntroIntLp1v2.wav`. That allows a lossless digital comparison after the hardware run instead of judging the source through the Vita speaker and a phone microphone.

## Hardware success criteria

Expected decisive lines:

- `bink-avplayer init-handle ... accepted=1`
- `bink-avplayer add-source result=0 ...`
- `bink-avplayer first-frame ...`
- `sound-export menu-wav ... complete=1`
- `sound-decode ... IntroIntLp1v2.wav ... volume=... pitch=... class=... flags=... loop=...`

If `add-source` succeeds but no first frame appears, the next problem is downstream decode/rendering rather than player construction. If the call rejects `0x817432A0`, the return value is a genuine lower-level error and the new log's memblock/error classification will narrow it further.
