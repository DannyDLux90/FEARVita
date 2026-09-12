# FEARVita M29BI progress — 2026-09-12

## Hardware frontier from M29BH

M29BH proved the new Jupiter EX v113 bootstrap is parsing real F.E.A.R. world content rather than returning `LT_INVALIDWORLDFILE` at the header. The base-game Intro load parsed all 347 collision/world BSPs, reached 60% visible loading progress, read 93 blind-data chunks, reported 1,988 server objects, and began constructing real ObjectDLL classes. The Vita then crashed during the object phase.

The M29BH PSP2 core dump resolves to the main FEAR thread at runtime PC `0x811e4f90`, relocated to linked address `0x811b4f90`. The linked symbol is `GenericPropList::GetNumProps() const`; register r0 is zero. The stack returns through `GenericPropList::GetProp`, `GenericPropList::GetString`, `CDestructibleModel::InitialUpdate(const GenericPropList*)`, and the legacy FEAR `EngineMessageFn` path.

## Root cause fixed in M29BI

LithTech's SDK exposes both the newer `OnObjectCreated(const GenericPropList*, float)` API and FEAR's legacy `EngineMessageFn` API. Message id 1 is shared by `MID_OBJECTCREATED` and FEAR's `MID_INITIALUPDATE`. The default two-argument SDK overload discarded `pProps` and delegated to the one-argument overload, which called legacy message id 1 with `pData == NULL`. FEAR classes such as `CDestructibleModel` interpret message id 1 as `MID_INITIALUPDATE` and immediately read properties, producing the null dereference seen in the hardware core.

M29BI adds a scoped Vita-only object-create property context. `sm_AddObjectToWorld` sets the current `GenericPropList` immediately around the virtual `OnObjectCreated` call and restores the previous value afterward, so nested object creation is safe. The legacy one-argument `ILTBaseClass::OnObjectCreated(float)` now forwards that real property list as `EngineMessageFn` pData. Classes that override the newer two-argument API still receive their normal virtual call.

## White loading-screen fix

M29BH's visible GT4 progress fallback changed DrawPrim state to `NOCOLOROP/NOBLEND/NOZ`. In the portable Vita `ILTDrawPrim` implementation, `SetRenderMode(...)` is only a compatibility no-op, so the state was not restored before the next synchronous loading-screen redraw. The mission background was then rendered under the wrong color operation and appeared white.

M29BI explicitly restores screen transform, `DRAWPRIM_MODULATE`, `DRAWPRIM_BLEND_MOD_SRCALPHA`, and `DRAWPRIM_NOZ` before drawing the mission background and after drawing the fallback progress bar. The loading bar remains tied to real world/object progress.

## Deliberately unchanged

Audio is unchanged from M29BH/M29BG for this milestone. The 48 kHz stereo hardware path and 160/147 polyphase resampler stay in place so this hardware test isolates the object-loader and loading-UI fixes.

## Build and package validation

- Public Vita version: `00.06`
- Internal checkpoint: `M29BI`
- Marker: `FEARVita 0.06 / M29BI; legacy object properties + stable loading UI`
- ARM executable SHA-256: `f9a0ca1bd7463d593398daed687af4ae35d4defda7ad630762401380a41090b5`
- EBOOT SHA-256: `f3f923edf80ecea52b0d69b341156622073dcda454e3787a9bb03d11265eec7e`
- Complete VPK SHA-256: `7f82be761aa9efa80da4c9c7f6c28f878dd2a39fa5df0d8d00bf61bf4887487b`
- VPK: 22 payload files / 35 ZIP entries, archive integrity OK, APP_VER 00.06, embedded EBOOT byte-identical to build output.

## Next hardware qualification

One base F.E.A.R. run: New Game -> Medium. Expected improvement is continuation beyond the first destructible-model object initialization while retaining the mission-screen background and real progress bar. If another crash occurs, preserve `fear_fear.log` and the newest PSP2 core dump; the new frontier should be resolvable from that single run.
