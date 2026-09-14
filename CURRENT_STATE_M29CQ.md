# FEARVita M29CQ / 0.39

Date: 2026-09-14

M29CP / 0.38 produced the first genuine Jupiter EX v113 world frames on Vita hardware. Extraction Point Performance Test reached authentic GS_PLAYING and rendered 8 camera frames, but then hit an ARM Data Abort. Base F.E.A.R. regressed before postload because the Intro world upload created 49,610 persistent render meshes and subsequent Model00p loads repeatedly returned LithTech result 67 (LT_OUTOFMEMORY), including Playerbase.Model00p.

M29CQ fixes the new render-memory regression at its source. Jupiter EX render surfaces are now the persistent batching unit and are split only at 2,048 triangles. Source vertices are deduplicated inside each persistent mesh. For the observed worlds this bounds handle count to roughly <=2,553 for Base Intro instead of 49,610 and <=549 for EP benchmark instead of 6,707. FrameRenderer reserves 4,096 mesh-map entries to reduce rehash/fragmentation.

New diagnostics log persistent world VB/IB bytes and Vita free USER/CDRAM/PHYCONT memory before/after render upload. World mesh create/draw errors are explicit. Diagnostic world rendering remains intentionally untextured; M29CQ uses flat grayscale per material so missing textures cannot be confused with noisy normal shading.

All M29CP focus/VSync/AVPlayer-lifetime fixes remain intact. Do not force GS_PLAYING, fake the player, bypass ClientInWorld, or mask the EP crash with a ClassifyHighX guard; the uploaded 0.38 core indicates memory/control-flow corruption rather than a normal collision classification failure.

Build/package succeeded. VPK contains the same 22 paths as M29CP including private local test art/video caches; those assets are not committed here. APP_VER 00.39, TITLE_ID FEAR00001.

SHA-256: VPK 387a0a56c6b07a9850d06a4d6124fbe837183c4420cde8b6a712fa22777c3267; eboot ce2d50066e1165c00483f67c20cfc633d1390cd9a72ed003220228bc64358623; ELF 0a150af40604b670f969016656ebed7a73c7f35344622e26e9d17f5f080e6f4b; patch 7bd241853507e264560475e833907efa8be68d5b56451a072d905da8706ccafd.
