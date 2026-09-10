# FEARVita

Work-in-progress PS Vita port/integration project for the open LithTech/Jupiter Ex source base used by **F.E.A.R.**.

Current public app version: **0.02**  
Current internal checkpoint: **M29AE**

The original retail game data is **not** included. You must provide your own legally obtained F.E.A.R. data files. `Menu.bik`, `Menu.mp4`, archives, music, and other proprietary retail assets are intentionally excluded from this repository.

## Current status

The retail F.E.A.R. front-end boots on real PS Vita hardware, renders, accepts controller input, and follows Vita system language. M29AE is focused on matching the PC menu presentation. The real `videos\\Menu.bik` has now been exported and validated; the Vita movie bridge uses an H.264 MP4 cache through `SceAvPlayer` while keeping the original F.E.A.R. menu music path separate.

M29AE corrects the AvPlayer decoded-frame allocator to use physically contiguous main memory. Private hardware-test VPKs may contain a user-derived `app0:cache/Menu.mp4`; release/source builds do not ship it.

Start with `CURRENT_STATE.md` and `M29AE_PROGRESS_2026-09-10.md`.

## Source layout

- `project/` — FEARVita source, compatibility layer, tools, tests, and Vita build files.
- `lithtech-overlay/` — FEARVita-modified files applied over the pinned public LithTech upstream.
- `UPSTREAM_PIN.txt` — upstream repository/commit used as the base.
- `LITHTECH_OVERLAY_MANIFEST.txt` — overlay file manifest.
