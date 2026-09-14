# FEARVita M29CQ / 0.39 handoff

Hardware M29CP result: Base Intro v113 render upload produced 49,610 persistent chunks and then real Model00p loads failed with result 67 = LT_OUTOFMEMORY, preventing player creation/postload. EP Performance Test parsed 503 surfaces / 94,135 triangles / 6,707 chunks, reached authentic GS_PLAYING and rendered 8 real camera frames (77 chunks / 2,845 triangles each), then crashed with an ARM Data Abort. Core symbolization lands in ClassifyHighX but the saved call context is corrupted; do not paper over it with a collision guard.

M29CQ changes: per-surface v113 batching, split only at 2,048 triangles; per-mesh source-vertex deduplication; FrameRenderer mesh-table reserve 4,096; persistent VB/IB byte logging; Vita USER/CDRAM/PHYCONT free-memory logging before/after render upload; explicit mesh create/draw errors; flat grayscale untextured diagnostic surfaces. M29CP focus/VSync/AVPlayer safety stays intact.

Test Base first for disappearance of repeated result=67 and return of ScreenPostload/press-any-key, then EP Performance Test for survival beyond old frame 8. If either crashes, collect fear_fear.log/fear_ep.log, vitaGL.log and the new psp2dmp.

VPK SHA-256: 387a0a56c6b07a9850d06a4d6124fbe837183c4420cde8b6a712fa22777c3267.
