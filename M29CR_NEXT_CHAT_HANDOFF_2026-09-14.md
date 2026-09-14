# M29CR / 0.40 handoff — 2026-09-14

Hardware baseline: M29CQ / 0.39 is stable in Extraction Point Performance Test for >=3000 retail-loop frames. Base still fails before postload because `Playerbase.Model00p` returns result 67 (`LT_OUTOFMEMORY`) after the Intro v113 renderer allocated ~17 MiB of persistent world mesh data.

M29CR changes the world renderer lifetime rather than patching Playerbase:

- `CServerMgr::LoadWorld` records the current World00p VFS source after old-world termination.
- v113 load parses only compact surface metadata/material names/bounds; no persistent world meshes exist during local player creation.
- visible RenderSurfaces are lazily reopened/decoded from World00p after the real gameplay camera starts.
- world mesh cache: 12 MiB LRU; current-frame surfaces protected.
- real FEAR `.Mat00` (`LTMI`) parsing resolves `tDiffuseMap`.
- DTX/DDS top mip -> RGBA8, max 512x512, 12 MiB texture LRU, <=2 new texture uploads/frame.
- GXM U/V repeat enabled for tiled world UVs.
- whole-surface near-plane rejection replaced with per-triangle safety filtering.
- keep the 3000 world-triangle/frame cap until hardware proves the textured path stable.

Hardware test:

1. Base: require `metadata-ready ... persistent-mesh-bytes=0`, no Playerbase result=67, real ScreenPostload/OK returns, then lazy mesh/texture loads start after camera.
2. EP Performance Test: retain >=3000-frame stability; confirm `world-material diffuse`, `world-texture loaded`, correct tiled textures and no near-camera surface holes.

If static world rendering is correct but props/weapons/characters/FX remain missing or visually wrong, treat those as the next isolated renderer frontier. Preserve the now-proven stock local-client, GS_PLAYING, CharacterFX and performance-test flows.

Local build artifacts: `FEARVita_0.40_M29CR.vpk`, eboot, ELF/VELF/SFO, `FEARVita_0.40_M29CR_Source.zip`, and `M29CQ_to_M29CR.patch`. VPK SHA-256: `be79faff1e90004e8cb3c2a48d6c123f2ac1a20556f2212b4124debb489133db`.