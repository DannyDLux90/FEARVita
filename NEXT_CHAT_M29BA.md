# M29BA next-chat handoff

M29AZ hardware retest confirms the strcasecmp-recursion fix: startup proceeds far beyond MissionDB.

New FEAR/EP core dumps both normalize to `FearVitaLegacyCheapLTLink::AddAfter` with the chain `CInterfaceMgr::Init -> CClientFXMgr::SetCamera -> LTObjRef -> CLTServer::LinkObjRef`. Root cause is an ARM ABI offset: complete polymorphic `LTObjRef*` and its `LTLink<HOBJECT>` base differ by 4 bytes. M29BA bridges the real base-subobject pointer into the legacy reference list and reverses that adjustment on deletion.

Generated code proves +4/-4 adjustment. PM's later malloc/audio crash may be downstream heap corruption; do not assume a separate audio root cause unless M29BA still reaches it.

Retest M29BA on Vita. If it crashes, collect per-campaign log + psp2core and normalize against the M29BA ELF from the current workspace.
