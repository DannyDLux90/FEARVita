#!/usr/bin/env python3
"""Convert F.E.A.R.'s own Menu.bik to a Vita SceAvPlayer-compatible MP4 cache.

No game asset is shipped by FEARVita. Run this on the Menu.bik exported by the
Vita build, then copy the generated Menu.mp4 back to:
  ux0:data/FEARVita/video_cache/videos/menu.mp4
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, help="Menu.bik exported by FEARVita")
    ap.add_argument("output", type=Path, nargs="?", default=Path("Menu.mp4"))
    ap.add_argument("--ffmpeg", default="ffmpeg")
    args = ap.parse_args()
    if not args.input.is_file():
        ap.error(f"input does not exist: {args.input}")
    exe = shutil.which(args.ffmpeg) if not Path(args.ffmpeg).is_file() else args.ffmpeg
    if not exe:
        ap.error("ffmpeg not found in PATH (or pass --ffmpeg /path/to/ffmpeg)")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(exe), "-hide_banner", "-y", "-i", str(args.input),
        "-map", "0:v:0", "-an",
        # Keep the exact 512x512 source geometry. The Vita renderer scales once
        # at presentation time, avoiding an unnecessary pre-scale/re-filter.
        "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.1",
        "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", "18",
        "-movflags", "+faststart", str(args.output),
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Created: {args.output}")
    print("Copy it to: ux0:data/FEARVita/video_cache/videos/menu.mp4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
