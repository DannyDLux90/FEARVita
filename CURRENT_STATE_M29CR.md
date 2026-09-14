# FEARVita current state — M29CR / 0.40 — 2026-09-14

## Hardware-proven baseline

M29CQ / 0.39 is stable on real Vita hardware in Extraction Point -> Performance Test for at least 3000 retail-loop frames. World camera rendering, present, input and movement audio continue; the former GPU watchdog and M29CP Data Abort are gone.

Base F.E.A.R. still does not reach the real postload confirmation in M29CQ. The Intro world creates 2415 persistent world meshes (~13.6 MiB vertex data + ~3.5 MiB indices) before the player is created. `Playerbase.Model00p` then returns result 67 (`LT_OUTOFMEMORY`), `PLAYER.MODEL00P` fails and `ServerShell::OnClientEnterWorld` returns `LTNULL`.

## M29CR / 0.40

M29CR moves v113 world rendering to a deferred/lazy lifetime:

- server-world load retains only vertex definitions, RenderSurface descriptors, material names, offsets and streamed surface bounds;
- persistent world mesh bytes are zero during Playerbase / OnClientEnterWorld;
- the current World00p VFS path is recorded in `CServerMgr::LoadWorld` and reopened only from the real gameplay camera;
- visible surfaces are decoded lazily into a 12 MiB LRU mesh cache;
- `.Mat00` files are parsed from the real `LTMI` format and `tDiffuseMap` is resolved;
- DTX/DDS diffuse textures use the existing FEARVita decoder and a 12 MiB texture LRU, <=512x512 RGBA8, at most two new uploads/frame;
- world texture U/V addressing explicitly uses GXM repeat so tiled FEAR UVs do not clamp-smear;
- M29CQ whole-surface near-plane rejection is replaced with per-triangle near-plane safety filtering;
- the 3000 world-triangle/frame budget is retained to preserve the proven EP workload.

Full Vita Release compile/link and VPK packaging succeeded. `APP_VER=00.40`, title ID `FEAR00001`, and the VPK retains the same 22 package paths as 0.39 including all launcher/boot art and menu videos.

VPK SHA-256: `be79faff1e90004e8cb3c2a48d6c123f2ac1a20556f2212b4124debb489133db`

## Required hardware proof

Base must show `metadata-ready ... persistent-mesh-bytes=0`, stop producing `Playerbase.Model00p result=67`, create the real player and reach actual ScreenPostload/confirmation. Lazy `mesh-load` entries should begin only after gameplay camera rendering.

EP Performance Test must retain >=3000-frame stability while progressively reporting `world-material diffuse` and `world-texture loaded` and displaying real tiled diffuse world textures.

Do not call M29CR fully hardware-verified until both paths pass.