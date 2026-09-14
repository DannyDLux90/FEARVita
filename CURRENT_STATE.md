# FEARVita current state — M29CR / 0.40 — 2026-09-14

**Last hardware-verified package:** M29CQ / 0.39  
**Current test package:** M29CR / 0.40

M29CQ is hardware-proven stable in Extraction Point -> Performance Test for at least 3000 retail-loop frames. Real v113 world camera rendering, presents, input and movement audio continue; the prior GPU watchdog and later Data Abort are gone.

Base F.E.A.R. M29CQ still fails before the real postload confirmation because the Intro renderer allocates ~17 MiB of persistent world mesh geometry before local player creation. `Playerbase.Model00p` then returns result 67 (`LT_OUTOFMEMORY`), `PLAYER.MODEL00P` fails and `ServerShell::OnClientEnterWorld` returns `LTNULL`.

M29CR fixes this at the renderer lifetime boundary: v113 server-world load retains only compact RenderSurface/material/bounds metadata and zero persistent world meshes. The World00p source is reopened lazily from the real gameplay camera, visible surfaces enter a 12 MiB mesh LRU, and real FEAR `.Mat00` `tDiffuseMap` textures are decoded from DTX/DDS into a bounded 12 MiB texture LRU (<=512x512, <=2 new uploads/frame). World textures use GXM repeat U/V for FEAR tiled UVs. Whole-surface near-plane rejection is replaced with per-triangle safety filtering.

M29CR Release compile/link and full VPK packaging succeeded. `APP_VER=00.40`, title ID `FEAR00001`, same 22 package paths as 0.39. VPK SHA-256: `be79faff1e90004e8cb3c2a48d6c123f2ac1a20556f2212b4124debb489133db`.

Required hardware proof: Base must stop reporting Playerbase result=67 and reach actual ScreenPostload/confirmation before lazy world meshes are created. EP Performance Test must retain >=3000-frame stability while progressively loading real diffuse world textures. See `CURRENT_STATE_M29CR.md` and `M29CR_NEXT_CHAT_HANDOFF_2026-09-14.md`.