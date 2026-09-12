# FEARVita M29BO / 0.12 — Model00p crash + schema checkpoint

Date: 2026-09-12

## Hardware result from M29BN / 0.11

- Base F.E.A.R. and Extraction Point both entered the new Jupiter EX `MODL` path.
- EP performance world reached 100%, then `CHARS\\MODELS\\PLAYER.MODEL00P` parsed successfully through:
  - header
  - 61 nodes
  - 2 animation schemas
  - raw animation block
  - animation binding/keyframe info
  - 5 animation weight sets
  - 12 sockets
  - 21 child-model entries
- The loader then returned `LT_INVALIDFILE` (numeric 77) before the packed physics/LOD/mesh section completed.
- Important: in M29BN, result `77` is `LT_INVALIDFILE`; it is no longer the old LTB-file-type byte `'M'` problem.

## Core-dump root cause

Dump: `psp2core-1789241811-0x00039029dd-eboot.bin.psp2dmp.tmp`

- Exception: ARM Data Abort.
- Runtime PC translated into M29BN ELF: `ModelAnim::GetModel()`.
- Caller: `Model::TermAnims()`.
- `this`/animation pointer was NULL.
- Cause: a failed partial Model00p load expanded `m_Anims`, left unbuilt slots null/uninitialized, then normal error cleanup called `Model::Term() -> Model::TermAnims()` and unconditionally dereferenced every slot.

## M29BO fixes

### 1. Partial-load cleanup is null-safe

`Model::TermAnims()` now checks `pAnim` before `pAnim->GetModel()`.
The new v33 loader also initializes every newly allocated `m_Anims` slot to a deterministic null/default state before constructing individual animations.

The final M29BO ELF was disassembled and verified to contain a null comparison/branch before the call to `ModelAnim::GetModel()`.

### 2. F.E.A.R. v33 animation position compression is schema-specific

M29BN trusted the binding field `compressedPosition` to choose all position channels as either 6-byte `int16[3]` or 12-byte `float3` data.
Real F.E.A.R. Model00p files do not permit that assumption.

The public Jupiter EX reverse-engineering reference and the M29BN core dump show that compression is encoded by each animation schema's channel offsets.
M29BO infers position width per schema from those offsets and uses that value for:

- animation buffer sizing,
- position channel interpreter selection,
- raw animation channel addressing.

A real `Base_Intro_Alma.Model00p` image recovered from the core dump contains six schemas. M29BO's inference gives:

`6, 6, 6, 6, 6, 12` bytes per position sample.

This is the mixed layout that M29BN could not represent correctly.

### 3. Packed physics/LOD/mesh stage diagnostics

The Player model previously stopped after `children-ok` with only `LT_INVALIDFILE`.
M29BO now logs bounded stages for:

- `geometry-flag`
- physics header and shape records
- constraints
- physics weight sets
- LOD groups
- mesh-link block / optional external mesh name
- mesh header/data/index list
- after-mesh byte list
- MeshInfo records/influence lists

Every bounds failure emits `[model00p-fail] stage=... pos=... len=... file=...` and returns cleanly.
Header-vs-stream count differences are diagnostic notes, not automatic rejection.

## Expected next hardware flow

For Base F.E.A.R. -> New Game -> Medium, useful success markers are:

```
[model00p-player] header ...
[model00p-player] schema=... pos-bytes=...
[model00p-player] children-ok ...
[model00p-player] geometry-flag=...
[model00p-player] physics-header ...
[model00p-player] shapes-ok ...
[model00p-player] constraints-ok ...
[model00p-player] physics-weights-ok ...
[model00p-player] lod-groups-ok ...
[model00p-player] mesh-header ...
[model00p-player] mesh-info-ok ...
[model00p-player] packed-sections-ok ...
[model00p-player] skeleton-built ...
[model00p-player] animations-built ...
[model00p-player] runtime-model-ready ...
[model00p] loaded v33 file=CHARS\\MODELS\\PLAYER.MODEL00P ...
```

If a packed section is still not fully understood, M29BO should no longer crash in animation cleanup; the log should identify the exact first failing section.

## Build/package validation

- Version: FEARVita 0.12 / M29BO
- VPK: `FEARVita_M29BO_0.12_MODEL00P_SCHEMA_HARDENING_2026-09-12.vpk`
- Full package layout: 22 non-directory payload files (35 ZIP entries with directories), retained from the hardware-tested layout.
- Embedded `eboot.bin` SHA-256: `4b04ece422c6636141c7a1f4373e45ebc95f09f3e89b00bd0cb40490c7fd0af0`
- VPK SHA-256: `7d0da85301acf25a4c3e24a4ce5096100ca1e9644057b0d98fbc7a6c112a9ae1`
- SFO APP_VER: `00.12`
- TITLE_ID: `FEAR00001`

## Project rule preserved

No forced `GS_PLAYING`, no model-less Player object, and no fake successful Model00p load. The real local client/server state machine and the real Player model creation path remain in use.
