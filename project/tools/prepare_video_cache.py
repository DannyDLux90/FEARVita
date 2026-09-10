#!/usr/bin/env python3
"""Build a Vita H.264 cache from user-owned F.E.A.R. Bink movies.

The input is a directory containing exported .bik files, preferably preserving
F.E.A.R.'s virtual layout (for example videos/Menu.bik). Output paths mirror
that layout with .mp4 extensions, normalized to lower-case to match FEARVita's
case-insensitive virtual filesystem names, under:

    ux0:data/FEARVita/video_cache/<virtual-path>.mp4

No retail data is included with FEARVita; this tool only converts files supplied
by the user.
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path


def convert(exe: str, src: Path, dst: Path, crf: int) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        exe, "-hide_banner", "-loglevel", "warning", "-y", "-i", str(src),
        "-map", "0:v:0", "-an",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.1",
        "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", str(crf),
        "-movflags", "+faststart", str(dst),
    ]
    print(f"[video-cache] {src} -> {dst}")
    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", type=Path, help="directory containing exported .bik files")
    ap.add_argument("output_dir", type=Path, help="directory that will receive mirrored .mp4 files")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--crf", type=int, default=18, help="x264 CRF (default: 18)")
    ap.add_argument("--force", action="store_true", help="rebuild MP4 files even when newer than input")
    args = ap.parse_args()

    if not args.input_dir.is_dir():
        ap.error(f"input directory does not exist: {args.input_dir}")
    exe = shutil.which(args.ffmpeg) if not Path(args.ffmpeg).is_file() else str(Path(args.ffmpeg))
    if not exe:
        ap.error("ffmpeg not found in PATH (or pass --ffmpeg /path/to/ffmpeg)")

    movies = sorted(p for p in args.input_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".bik")
    if not movies:
        ap.error(f"no .bik files found under {args.input_dir}")

    converted = skipped = 0
    for movie in movies:
        rel = movie.relative_to(args.input_dir).with_suffix(".mp4")
        # FEARVita normalizes retail VFS names to lower-case. Vita's ux0/app0
        # filesystems are case-sensitive, so mirror that normalization here.
        rel = Path(*[part.lower() for part in rel.parts])
        dst = args.output_dir / rel
        if not args.force and dst.is_file() and dst.stat().st_mtime >= movie.stat().st_mtime:
            print(f"[video-cache] up-to-date: {dst}")
            skipped += 1
            continue
        convert(exe, movie, dst, args.crf)
        converted += 1

    print(f"[video-cache] done converted={converted} skipped={skipped} total={len(movies)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
