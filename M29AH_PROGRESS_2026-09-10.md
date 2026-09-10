# M29AH / 0.02 Progress — fullscreen menu + campaign video namespaces

## M29AG hardware result
M29AG proves the SceAvPlayer path on a real PS Vita. `sceAvPlayerInit` returns `0x817432A0`; despite its signed representation, it is a usable opaque handle. `sceAvPlayerAddSource` returns 0 and the first YVU420P2 video frame is decoded at 512x512. The retail menu WAV is also exported byte-complete and runs at retail volume 100 through the 48 kHz HQ output path.

## M29AH changes
- Stretch the decoded menu movie non-uniformly to the full 960x544 framebuffer.
- Remove the abandoned per-frame JPEG fallback completely.
- Namespace MP4 caches by campaign: `fear/`, `ep/`, `pm/`.
- Export each campaign's requested menu Bink separately as `ux0:data/FEARVita/debug/Menu_fear.bik`, `Menu_ep.bik`, or `Menu_pm.bik`.
- Menu movies loop; non-menu movies are configured non-looping for future cinematics.
- `prepare_menu_video.py` accepts `--campaign fear|ep|pm`.
- `prepare_video_cache.py` batch-converts a campaign-organized Bink tree and preserves an optional first audio track as AAC stereo/48 kHz for future cinematics.

## Add-on state
Extraction Point and Perseus Mandate still need fresh M29AH hardware logs. Their known M29W blockers were the disconnected frontend pause-message crash (FEAR/EP) and missing canonical DB/StringDB paths in an XP2-only mount (PM). M29X added the network guard plus base-FEAR + expansion overlay VFS, but add-on menu completion was never hardware-proven afterward. Missing MP4 video cache does not itself block frontend initialization; it only prevents movie frames after a ScreenMovie is requested.

## Next hardware test
1. Verify F.E.A.R. menu movie fills the Vita screen.
2. Run Extraction Point, then copy `fear_menu_boot.log` before starting another campaign.
3. Run Perseus Mandate, then copy `fear_menu_boot.log` again.
4. If an add-on reaches ScreenMovie, also return `debug/Menu_ep.bik` or `debug/Menu_pm.bik`; those can then be converted to the matching campaign cache.
