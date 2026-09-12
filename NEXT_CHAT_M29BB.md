# FEARVita M29BB — continuation handoff — 2026-09-12

## Current build
M29BB fixes the monolithic LTObjRef client/server ownership-dispatch bug exposed by M29BA hardware testing.

Startup marker:
`FEARVita 0.02 / M29BB; LTObjRef client/server ownership dispatch + ObjectDLL runtime`

## Proven previous failures
- M29AY: recursive `strcasecmp()` wrapper -> stack overflow during database initialization.
- M29AZ: recursion fixed; hardware advanced far beyond MissionDB.
- M29BA: +4/-4 LTObjRef base-subobject bridge was ABI-correct but did not move the crash.
- M29BA F.E.A.R./EP/PM cores all normalize to `0x81590790`, `FearVitaLegacyCheapLTLink::AddAfter`.
- All three M29BA campaign logs end at `if-camera-created` / `if-interfacefx-before`.

## M29BB root fix
Frontend camera/FX handles are Vita `VitaLocalObject` instances created by ILTClient, not server `LTObject` instances. In the monolithic executable both client and server interface holders exist; original LTObjRef code preferred server whenever present and therefore sent client-local handles into `CLTServer::LinkObjRef`.

M29BB dispatches ownership client-first on Vita:
- client recognizes only its registered `VitaLocalObject` handles;
- unknown handles return `LT_NOTFOUND`;
- server is tried only after that, preserving genuine server `LTObject` reference tracking.

The first eight accepted client-local refs are logged as `[objref] client-local-link accepted ...`.

## Artifact hashes
- ELF: `684e061f97e9c3ee9b563a4eb5cb1015943cbf3f21fa6068739d6b3f6e1eb544`
- VELF: `93a591cacf5f3763d711eeb4128544ea0d1aeaa236625800333c3fd295c34942`
- SELF: `1f855df87ee33dd948ba757c395bf79e8901403c326cf793f3bc117ef035753a`
- VPK: `7d2deb9cbda06581540a027a28c96b098fce8a91c444db61680cddbe6013202e`
- Source backup: `65a4c8c69576dc916c8ef7c6fdb27f939d2c48ff9806efc29ea18050dd53225f`
- Workspace backup: `7af19ca959f134ee7edb57b53cc3d69fd9ac12882d6dc15167940cd284685d93`

## Next hardware action
Test M29BB on real Vita, preferably F.E.A.R. first. Confirm whether the log contains `[objref] client-local-link accepted` and whether execution advances past `if-interfacefx-before`. If there is another hard crash, symbolise the new psp2 core against the M29BB ELF before changing runtime code.

M29BB is not hardware validated yet. Do not claim gameplay/world success until real Vita logs prove it.
