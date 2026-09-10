#!/usr/bin/env python3
"""Convert a user-owned FEAR/EP/PM Menu.bik to the Vita MP4 cache."""
from __future__ import annotations
import argparse, shutil, subprocess
from pathlib import Path

TAGS = ("fear", "ep", "pm")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path, nargs="?", default=Path("Menu.mp4"))
    ap.add_argument("--campaign", choices=TAGS, default="fear")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    args = ap.parse_args()
    if not args.input.is_file(): ap.error(f"input does not exist: {args.input}")
    exe = shutil.which(args.ffmpeg) if not Path(args.ffmpeg).is_file() else str(args.ffmpeg)
    if not exe: ap.error("ffmpeg not found")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [exe, "-hide_banner", "-loglevel", "warning", "-y", "-i", str(args.input),
           "-map", "0:v:0", "-an", "-c:v", "libx264", "-profile:v", "baseline",
           "-level", "3.1", "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", "18",
           "-movflags", "+faststart", str(args.output)]
    subprocess.run(cmd, check=True)
    print(f"Created: {args.output}")
    print(f"Copy to: ux0:data/FEARVita/video_cache/{args.campaign}/videos/menu.mp4")
    return 0

if __name__ == "__main__": raise SystemExit(main())
