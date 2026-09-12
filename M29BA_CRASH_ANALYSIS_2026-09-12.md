# FEARVita M29BA — LTObjRef legacy-link ABI crash fix — 2026-09-12

## Hardware retest result
M29AZ removes the earlier recursive `strcasecmp()` stack overflow. The new hardware logs proceed far beyond MissionDB initialization and through substantial interface/player/frontend initialization.

Two retest core dumps corresponding to the F.E.A.R./Extraction Point attempts normalize to the same ARM PC:

- normalized PC: `0x81590790`
- function: `FearVitaLegacyCheapLTLink::AddAfter(FearVitaLegacyCheapLTLink*)`

The normalized return chain is:

`CInterfaceMgr::Init -> CClientFXMgr::SetCamera -> LTObjRef::operator= -> LTObjRef::Link -> CLTServer::LinkObjRef -> legacy AddAfter`

The Perseus Mandate attempt gets farther and crashes in `_malloc_r` from `operator new` / `CVitaSoundMgr::PlaySound`. That is consistent with prior heap corruption, but audio is not claimed as the root cause from this dump alone.

## Root cause
FEAR/Jupiter's `LTObjRef` is polymorphic and derives from `LTLink<HOBJECT>`. On ARM/Vita the complete `LTObjRef*` points at the vptr, while its `LTLink<HOBJECT>` base subobject starts four bytes later.

M29AZ's server bridge incorrectly did:

`reinterpret_cast<CheapLTLink*>(pRef)`

and passed the complete object address to the old untyped LithTech list code. The legacy `AddAfter` therefore treated the vptr/adjacent fields as the historical prev/next pointers, corrupting memory and crashing when it dereferenced the bogus list pointer.

## M29BA fix
The runtime compatibility layer now provides explicit two-way bridge helpers:

- `fearvita_ObjRefToLegacyLink(LTObjRef*)` first `static_cast`s to the real `LTLink<HOBJECT>*` base subobject, then exposes that exact two-pointer node to the old list code.
- `fearvita_LegacyLinkToObjRef(...)` converts the stored base-subobject node back to the complete `LTObjRef*` before object-reference deletion callbacks.

`CLTServer::LinkObjRef` uses the first helper. `LTObject::NotifyObjRefList_Delete` uses the reverse helper.

Generated ARM object code proves the ABI adjustment:

- forward bridge: `+4` bytes
- reverse bridge: `-4` bytes

No fake game-state transition is introduced.

## Build artifacts
- ELF SHA-256: `27ff2a108c04e1e01d92c100768ef1d66f4501ac94266816a4b40100045c8b59`
- VELF SHA-256: `7b41b6cb478b8a9d667e32bde1057a9b131c66b62257969a172e056ee8398499`
- eboot.bin SHA-256: `8f8cd8c62b92711913e678bd71df64357e81987bfc1f4a16f706a6f7c5f82316`
- Full 22-file VPK SHA-256: `47fa72f0f5166f3ccf9298607b9c1fee02cec3d24ec7997b63675e59e6a217e0`

The ten private launcher/menu/video assets are byte-identical to M29AX and remain packaging-only.

## Validation status
M29BA is build/package validated but not yet hardware validated. M29AZ hardware testing proves the previous `strcasecmp` fix worked and exposes this next ABI failure. A new Vita retest is required to determine the next real runtime frontier.
