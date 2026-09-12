# FEARVita current state

**Public version:** 0.06  
**Internal checkpoint:** M29BI  
**Date:** 2026-09-12

M29BH hardware testing proved the Jupiter EX v113 path is now reading real F.E.A.R. Intro data: all 347 BSPs completed, the real loading bar reached 60%, 93 blind-data chunks were read, and the server began the 1,988-object world list. This moves the project past the former `LT_INVALIDWORLDFILE` frontier.

The resulting PSP2 core identifies the next blocker precisely. The main thread crashed in `GenericPropList::GetNumProps()` with a null `this` pointer while `CDestructibleModel::InitialUpdate` was reading world properties. The cause is the SDK transition between the newer `OnObjectCreated(const GenericPropList*, float)` API and F.E.A.R.'s legacy message-id-1 `EngineMessageFn` path: the default newer overload discarded the property list before the legacy handler ran.

M29BI adds a Vita-only scoped property bridge around `sm_AddObjectToWorld`. The legacy `ILTBaseClass::OnObjectCreated(float)` now receives the active `GenericPropList` as message data, while classes overriding the newer two-argument method continue to dispatch normally. Nested object creation restores the previous property context.

M29BI also fixes the white mission screen seen during M29BH loading. The GT4 fallback bar intentionally changes DrawPrim state, but the portable `SetRenderMode` helper is a no-op. The loader now explicitly restores screen transform, modulation, alpha blending and no-Z state before each mission-background redraw and after the progress bar.

Audio is deliberately unchanged for this milestone so the next hardware run isolates the object/startup and loading-screen fixes.

**Build validation:** Vita ARM executable and FSELF generation succeeded. Complete VPK carries APP_VER `00.06`, contains 22 payload files, passes ZIP integrity testing, and embeds the freshly built M29BI EBOOT byte-for-byte. VPK SHA-256: `7f82be761aa9efa80da4c9c7f6c28f878dd2a39fa5df0d8d00bf61bf4887487b`. EBOOT SHA-256: `f3f923edf80ecea52b0d69b341156622073dcda454e3787a9bb03d11265eec7e`.
