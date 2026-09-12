# FEARVita M29BB artifacts — 2026-09-12

Build marker: `FEARVita 0.02 / M29BB; LTObjRef client/server ownership dispatch + ObjectDLL runtime`

## Executable artifacts
- ARM ELF SHA-256: `684e061f97e9c3ee9b563a4eb5cb1015943cbf3f21fa6068739d6b3f6e1eb544`
- VELF SHA-256: `93a591cacf5f3763d711eeb4128544ea0d1aeaa236625800333c3fd295c34942`
- SELF `eboot.bin` SHA-256: `1f855df87ee33dd948ba757c395bf79e8901403c326cf793f3bc117ef035753a`

## Standalone VPK
- File: `FEARVita_M29BB_0.02_LTOBJREF_OWNERSHIP_DISPATCH_2026-09-12.vpk`
- Size: `21,926,651` bytes
- SHA-256: `7d2deb9cbda06581540a027a28c96b098fce8a91c444db61680cddbe6013202e`
- ZIP integrity: PASS
- Entries: 22
- Embedded `eboot.bin`: byte-identical to M29BB SELF
- Ten private M29AX launcher/menu/video assets: 10/10 byte-identical; packaging-only

## Current backups
- Source: `FEARVita_M29BB_SOURCE_OBJREF_DISPATCH_FIX_2026-09-12.zip`
  - Size: `46,285,074` bytes
  - SHA-256: `65a4c8c69576dc916c8ef7c6fdb27f939d2c48ff9806efc29ea18050dd53225f`
- Workspace: `FEARVita_M29BB_WORKSPACE_OBJREF_DISPATCH_FIX_2026-09-12.zip`
  - Size: `116,991,219` bytes
  - SHA-256: `7af19ca959f134ee7edb57b53cc3d69fd9ac12882d6dc15167940cd284685d93`
- Both passed full `unzip -tq` integrity checks.
- Both contain zero `.vpk`, `boot_art/`, `launcher_art/`, `video_cache/`, or private asset-root payload entries.
- Workspace contains the latest M29BA hardware logs/core dumps, normalized-PC summary, final M29BB build logs, and `LTObjRef::Link` disassembly.

## Validation
M29BB is build/package validated only. Real Vita retest is required.
