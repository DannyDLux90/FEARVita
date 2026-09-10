#!/usr/bin/env python3
"""Generate FEARVita's private JPEG menu-frame fallback from the user's Menu.bik.

No F.E.A.R. retail asset is distributed by FEARVita. This tool must be run on a
Menu.bik extracted/exported from a copy owned by the user. The resulting
`menu_frames/` directory is for local/private packaging only and is ignored by
git.
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, help="Menu.bik exported from your own F.E.A.R. data")
    ap.add_argument("output_dir", type=Path, nargs="?", default=Path("menu_frames"))
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--quality", type=int, default=6, help="ffmpeg MJPEG qscale (2=high, 31=low; default 6)")
    args = ap.parse_args()
    if not args.input.is_file():
        ap.error(f"input does not exist: {args.input}")
    exe = shutil.which(args.ffmpeg) if not Path(args.ffmpeg).is_file() else args.ffmpeg
    if not exe:
        ap.error("ffmpeg not found in PATH (or pass --ffmpeg /path/to/ffmpeg)")
    if not 2 <= args.quality <= 31:
        ap.error("--quality must be between 2 and 31")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for old in args.output_dir.glob("*.jpg"):
        old.unlink()
    pattern = args.output_dir / "%03d.jpg"
    cmd = [
        str(exe), "-hide_banner", "-y", "-i", str(args.input), "-an",
        "-vf", "fps=30,scale=512:512:flags=lanczos",
        "-q:v", str(args.quality), "-start_number", "0", str(pattern),
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    frames = sorted(args.output_dir.glob("*.jpg"))
    if len(frames) != 420:
        raise SystemExit(f"expected 420 Menu.bik frames, got {len(frames)}")
    print(f"Created {len(frames)} frames in {args.output_dir}")
    print("Private VPK layout: app0:menu_frames/000.jpg ... 419.jpg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
