#!/usr/bin/env python3
"""Build campaign-aware Vita MP4 caches from user-owned exported F.E.A.R. Binks.

Prepare an input tree grouped by campaign, then run:
    python3 prepare_video_cache.py binks video_cache

The output mirrors the campaign and virtual paths:
    binks/fear/videos/Menu.bik -> video_cache/fear/videos/menu.mp4
    binks/ep/videos/Menu.bik   -> video_cache/ep/videos/menu.mp4
    binks/pm/videos/Menu.bik   -> video_cache/pm/videos/menu.mp4

M29AH itself exports the menu Bink as ``debug/Menu_<campaign>.bik`` for
hardware validation. A later extraction/batch step will populate the complete
cinematic input tree without shipping any retail data.

Copy ``video_cache`` back to ``ux0:data/FEARVita/video_cache``. The campaign
namespace is important because the expansions can reuse a virtual Bink name
while containing different media.

The first embedded audio track, when present, is converted to AAC stereo/48 kHz
inside the MP4 so the cache is suitable for later cinematics as well as silent
menu backgrounds. FEARVita's current menu path does not request AvPlayer audio
for Menu.bik because the menu uses a separate ScreenMusic WAV.

No retail data is included with FEARVita; this tool converts only files supplied
by the user.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

CAMPAIGNS = ("fear", "ep", "pm")


def lower_rel(path: Path) -> Path:
    return Path(*(part.lower() for part in path.parts))


def convert(exe: str, src: Path, dst: Path, crf: int, audio_bitrate: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        exe, "-hide_banner", "-loglevel", "warning", "-y", "-i", str(src),
        "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.1",
        "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", str(crf),
        "-c:a", "aac", "-b:a", audio_bitrate, "-ac", "2", "-ar", "48000",
        "-movflags", "+faststart", str(dst),
    ]
    print(f"[video-cache] {src} -> {dst}")
    subprocess.run(cmd, check=True)


def discover(input_dir: Path, default_campaign: str) -> list[tuple[str, Path, Path]]:
    found: list[tuple[str, Path, Path]] = []
    campaign_dirs = {tag: input_dir / tag for tag in CAMPAIGNS if (input_dir / tag).is_dir()}
    if campaign_dirs:
        for tag, root in campaign_dirs.items():
            for movie in sorted(root.rglob("*")):
                if movie.is_file() and movie.suffix.lower() == ".bik":
                    found.append((tag, movie, movie.relative_to(root)))
        return found

    for movie in sorted(input_dir.rglob("*")):
        if movie.is_file() and movie.suffix.lower() == ".bik":
            found.append((default_campaign, movie, movie.relative_to(input_dir)))
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", type=Path,
                    help="exported binks root (campaign subdirs fear/ep/pm are auto-detected)")
    ap.add_argument("output_dir", type=Path,
                    help="directory that will receive campaign-aware .mp4 files")
    ap.add_argument("--campaign", choices=CAMPAIGNS, default="fear",
                    help="campaign tag for a legacy flat input directory (default: fear)")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--crf", type=int, default=18, help="x264 CRF (default: 18)")
    ap.add_argument("--audio-bitrate", default="160k", help="AAC bitrate (default: 160k)")
    ap.add_argument("--force", action="store_true",
                    help="rebuild MP4 files even when newer than input")
    args = ap.parse_args()

    if not args.input_dir.is_dir():
        ap.error(f"input directory does not exist: {args.input_dir}")
    exe = shutil.which(args.ffmpeg) if not Path(args.ffmpeg).is_file() else str(Path(args.ffmpeg))
    if not exe:
        ap.error("ffmpeg not found in PATH (or pass --ffmpeg /path/to/ffmpeg)")

    movies = discover(args.input_dir, args.campaign)
    if not movies:
        ap.error(f"no .bik files found under {args.input_dir}")

    converted = skipped = 0
    by_campaign = {tag: 0 for tag in CAMPAIGNS}
    for campaign, movie, rel in movies:
        by_campaign[campaign] += 1
        dst = args.output_dir / campaign / lower_rel(rel.with_suffix(".mp4"))
        if (not args.force and dst.is_file()
                and dst.stat().st_mtime >= movie.stat().st_mtime):
            print(f"[video-cache] up-to-date: {dst}")
            skipped += 1
            continue
        convert(exe, movie, dst, args.crf, args.audio_bitrate)
        converted += 1

    counts = " ".join(f"{k}={v}" for k, v in by_campaign.items())
    print(f"[video-cache] done converted={converted} skipped={skipped} "
          f"total={len(movies)} {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
