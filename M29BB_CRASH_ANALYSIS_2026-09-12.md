# FEARVita M29BB — LTObjRef client/server ownership dispatch — 2026-09-12

## M29BA hardware retest
The M29BA +4/-4 LTObjRef base-subobject bridge did not move the hardware crash site. The new F.E.A.R., Extraction Point and Perseus Mandate logs all reach interface-manager setup and end at `if-camera-created` / `if-interfacefx-before`.

All three new Vita core dumps normalize to the same executable PC:
- normalized PC: `0x81590790`
- function: `FearVitaLegacyCheapLTLink::AddAfter(FearVitaLegacyCheapLTLink*)`

So the previous pointer-offset correction was ABI-correct but incomplete.

## Deeper root cause
The original LithTech code assumes client and server live in separate modules. FEARVita links the FEAR client shell and local server into one monolithic executable, so both `ILTClient` and `ILTServer` interface holders can be populated simultaneously.

Original `LTObjRef::Link()` selected the server interface whenever an `ILTServer` holder existed. During frontend initialization this is wrong: the interface camera and related local FX objects are created by the Vita `ILTClient` compatibility layer and are represented by opaque `VitaLocalObject` handles. They are not runtime `LTObject` instances.

Bad M29BA path:
`CInterfaceMgr::Init -> CClientFXMgr::SetCamera -> LTObjRef::Link -> CLTServer::LinkObjRef`

`CLTServer::LinkObjRef` then interpreted a `VitaLocalObject*` as an `LTObject*`, read a bogus `m_RefList`, and crashed in the legacy list code. This is why changing the LTObjRef base-subobject offset alone could not fix the crash: the linked object did not belong to the server object system at all.

## M29BB fix
On Vita/portable FEARVita builds, `LTObjRef::Link()` now performs ownership dispatch:
1. Ask `ILTClient::LinkObjRef` first.
2. Vita client accepts only handles in its `VitaLocalObject` registry and returns `LT_OK` for them.
3. If client returns `LT_NOTFOUND`, fall through to `ILTServer::LinkObjRef`, preserving genuine server `LTObject` reference-list tracking.
4. If neither side owns the handle, clear the reference.

No fake object, game-state transition, or world transition is introduced.

The first eight accepted client-local references are logged as:
`[objref] client-local-link accepted type=<type> count=<n>`

## Binary verification
Final M29BB ARM ELF disassembly verifies that `LTObjRef::Link()` calls through the `ILTClient` holder first and only accesses the `ILTServer` holder after client ownership fails.

## Build artifacts
- ELF SHA-256: `684e061f97e9c3ee9b563a4eb5cb1015943cbf3f21fa6068739d6b3f6e1eb544`
- VELF SHA-256: `93a591cacf5f3763d711eeb4128544ea0d1aeaa236625800333c3fd295c34942`
- eboot.bin SHA-256: `1f855df87ee33dd948ba757c395bf79e8901403c326cf793f3bc117ef035753a`
- Full 22-file VPK SHA-256: `7d2deb9cbda06581540a027a28c96b098fce8a91c444db61680cddbe6013202e`
- VPK size: `21,926,651` bytes
- Embedded eboot.bin is byte-identical to the verified SELF.
- Ten private M29AX launcher/menu/video assets are 10/10 byte-identical and remain packaging-only.

## Validation status
M29BB is build/package validated but NOT hardware validated. M29BA hardware testing provided the evidence for this ownership-dispatch fix. Retest F.E.A.R. first and preserve the new log/core if another real runtime frontier appears.
