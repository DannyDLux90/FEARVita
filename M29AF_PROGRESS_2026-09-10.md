# M29AF progress — 2026-09-10

## Hardware evidence entering M29AF

M29AE boots and behaves like M29AD visually. Its log proves that `app0:cache/Menu.mp4` is selected, `SCE_SYSMODULE_AVPLAYER` loads successfully, and `sceAvPlayerInit` immediately returns `-2123091296` (`0x817432A0`). No `sceAvPlayerAddSource` call occurs.

The uploaded Menu.bik is unchanged and valid: BIKi, 6,301,124 bytes, 512x512, 420 frames, 30 fps, no embedded audio track. The uploaded session video confirms the uniform green background and working menu navigation.

## Implementation

M29AF adds a private JPEG sequence fallback in `project/integration/lithtech/fearvita_bink_vita.cpp`:

- probes `app0:menu_frames/000.jpg`;
- uses the original Bink frame count/rate for the timeline;
- decodes only when the target frame changes;
- renders the most recent decoded frame directly with vita2d;
- logs first-frame decode latency and average/max latency after 30 decoded frames;
- leaves AvPlayer first in the chain so it can be re-enabled automatically if the firmware-level failure is later solved.

`project/tools/prepare_menu_framepack.py` generates the 420-frame private pack from a user-owned/exported `Menu.bik`. Retail/derived media stays out of public source control.

## Hardware success criteria

The main menu visibly shows the real F.E.A.R. radar/logo animation. Log contains `bink-jpeg frame-pack-present` and `bink-jpeg first-frame`; `decode-perf` determines whether 30 fps is sustainable or whether M29AG should switch to a lower-overhead packed frame format.
