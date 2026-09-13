# FEARVita next-chat handoff — M29CL / 0.34 — 2026-09-13

Canonical local workspace: `/mnt/data/fear_work` with project source in `m29ay_src`, LithTech runtime in `m29ay_lithtech/lithtech-master`, and build tree in `m29ay_build`. Current test artifact is `FEARVita_0.34_M29CL.vpk` (SHA-256 `5142634839655bc6bff276cf6360fec5b6ec8f29bcefb8ac01f3fbdb67cd0a62`). Current source snapshot SHA-256 is `b6a0ce45729597eff6f390d1589e11c69739e8268b7f89ace264a1721fb90209`.

Last hardware evidence is M29CK/0.33 from `fear_fear(9).log`, `fear_ep(9).log`, `vitaGL.log`, and the two associated psp2dmp files. 0.33 reaches real server player, native client proxy, stock OnEnterWorld, `player-local-model-ok`, complete PlayerBody reset and `player-local-init-complete`. Extraction Point reaches ScreenPostload and the real ClientInWorld send.

Active 0.33 crash A: `ClientConnectionMgr::SendClientInWorldMessage()` null-dereferences `g_pLTGameUtil` at `WriteServerKeyData` (DFAR 0). Active crash B: `std::bad_alloc` on a normal 4 MiB decoded texture allocation in `CVitaTextureMgr::CreateTextureFromFile` from `CScreenPostload::OnFocus`. vitaGL provides negative evidence: no shader/GPU/VitaGL error signature near the crash.

M29CL/0.34 adds a local-singleplayer-only paired raw-world-CRC fallback when ILTGameUtil is absent, shared normalized-filename texture caching/refcounts, decode OOM fallback to a transparent 1x1 texture, and more CharacterFX/postload diagnostics. It does not fake a player, force `GS_PLAYING`, bypass CharacterFX, or broadly forward unsafe HOBJECT-bearing messages.

Preserve all prior fixes: Model00p v33/v34 + LDOM BE, v34 child-count semantics, animation layout inference, strict physics/subshape parsing, separate native client proxy, narrow CharacterFX retarget, sanitized player update, deferred gameplay managers, monolithic client/server scope isolation, stock server PreUpdate/Update/PostUpdate frame bracket, dynamic SharedFXStructs client/server serializer context, and PlayerBody null-model guard.

Next hardware ladder: M29CL startup -> player-local-model-ok -> player-body-reset-complete -> player-local-init-complete -> new characterfx-stage markers -> postload/texture markers -> ClientInWorld fallback markers if needed -> Respawn -> Alive -> stock GS_PLAYING.

GitHub: branch `m29cl-0.34-handoff`, based on public M29BW commit `5cd48609d9a01e452e1212c0f93e8713fd933436`. GitHub stores source/docs only; the local handoff ZIP stores workspace + source snapshot + VPK + latest logs/dumps.
