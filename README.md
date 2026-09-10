# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AF**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `Menu.bik`, archives, music, generated menu frames, and other proprietary retail assets are intentionally excluded from this repository.

## Current status

The retail F.E.A.R. front-end boots on real PS Vita hardware, renders, accepts controller input, and follows Vita system language. The real `videos\\Menu.bik` has been exported and validated as Bink/BIKi: 6,301,124 bytes, 512x512, 420 frames, 30 fps, 14 seconds, no embedded audio track. The menu music remains the separate retail WAV path.

M29AE proved that `SceAvPlayer` still fails at `sceAvPlayerInit` with `0x817432A0` before the private MP4 cache can even be opened. M29AF therefore adds a deterministic software presentation fallback: a private 30-fps JPEG frame pack generated from the user's own `Menu.bik` and drawn through vita2d. The public source contains the loader and conversion tool only; it never contains the frames.

Start with `CURRENT_STATE.md` and `M29AF_PROGRESS_2026-09-10.md`.

## Source layout

- `project/` — FEARVita source, compatibility layer, tools, tests, and Vita build files.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `LITHTECH_OVERLAY_MANIFEST.txt` — overlay file manifest.

## Private menu frame pack

After FEARVita exports your own `Menu.bik`, generate the fallback frames on a PC:

```bash
python3 project/tools/prepare_menu_framepack.py Menu.bik menu_frames
```

A private test VPK can package that directory at `app0:menu_frames/`. Do not commit or redistribute the generated frames.
