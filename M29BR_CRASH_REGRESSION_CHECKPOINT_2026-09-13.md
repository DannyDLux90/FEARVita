# FEARVita M29BR / 0.15 — restored connectionless local-client null-safety

Date: 2026-09-13

## Hardware failure in M29BQ / 0.14

Both Base F.E.A.R. and Extraction Point crashed immediately after the local server began listening, before world loading and before any Model00p diagnostic marker.

Observed log frontier:

- ObjectDLL loaded.
- `Listening on driver: local`.
- `[server-world] listen-local-ok`.
- Immediate Data Abort; no `model00p-player` / `model00p-layout` marker.

Two uploaded PSP2 core dumps were independently parsed. Both resolve to the same FEARVita text-segment offset `+0x5e040c` in the M29BQ ELF:

- dump 1789287290 runtime PC `0x815ea40c`, FEARVita segment base `0x8100a000`;
- dump 1789287363 runtime PC `0x8162640c`, FEARVita segment base `0x81046000`.

Both map to `CLTServer::GetClientAddr(HCLIENT_t*, unsigned char*, unsigned short*)` at the instruction that dereferences the `Client::m_ConnectionID` vtable. Register `R3` is `0x00000000` at the fault.

The first dump's stack resolves the call path through:

- `BanIPMgr_Impl::IsClientBanned(HCLIENT_t*)`
- `BanIPMgr_Impl::OnAddClient(HCLIENT_t*)`
- `ServerConnectionMgr::OnAddClient(HCLIENT_t*)`

This is the same connectionless-local-client crash previously fixed in M29BM. The M29BQ reconstructed compiled LithTech tree had lost the M29BM/M29BP null-safety even though the local FEAR client is intentionally created without a packet-level `CBaseConn`.

## M29BR fix

M29BR keeps the M29BQ Model00p v33 global physics-shape layout solver unchanged and restores the hardware-proven connectionless-local server behavior from M29BM/M29BP:

1. `CLTServer::GetClientAddr` returns LithTech's localhost sentinel `0.0.0.0:0` when `m_ConnectionID == NULL`.
2. `CLTServer::SendTo` skips connectionless clients while scanning packet endpoints.
3. The headless-local `Client` skips file-transfer-server creation and marks the engine hello as satisfied.
4. `Client::~Client` and `sm_UpdateClientFileTransfer` tolerate a NULL file-transfer server.
5. `sm_UpdateClientInWorld` skips packet/bandwidth replication for the connectionless local client.
6. `IServerFileMgr::AddUsedFile` does not add files to a NULL file-transfer server.
7. A kicked connectionless client is removed locally instead of passing NULL to `NetMgr::Disconnect`.

The M29BQ in-process Retail ClientShell dispatch (`FearVita_ClientReceiveServerMessage` / `FearVita_ServerDispatchClientMessage`) was explicitly retained while restoring these guards.

## Binary verification

Final M29BR ELF disassembly confirms that `CLTServer::GetClientAddr` now loads `Client::m_ConnectionID` from offset `0x7c`, compares it against zero, and branches around the virtual `GetIPAddress` call when NULL.

The final ELF also exports `FearVita_ServerDispatchClientMessage` and contains the M29BQ `physics-layout solved` / `model00p-layout` diagnostic strings.

Runtime marker:

`FEARVita 0.15 / M29BR; M29BQ Model00p solver + restored connectionless null-safety`

## Package

- APP_VER: `00.15`
- TITLE_ID: `FEAR00001`
- Full package layout: 35 ZIP entries / 22 payload files
- eboot.bin SHA-256: `e933ce67d679ae11d5a2f7e59660d2a0a63a65ebc07c1d610304ff5e63f3e215`
- VPK SHA-256: `5ae8cbbe63eb5583ee4eb83f3070f2ad590647a33e1d71bd8f6c0a6409c1a411`

## Next hardware test

Test Base F.E.A.R. -> New Game -> Medium first. Expected minimum frontier is now beyond `[server-world] listen-local-ok`, into normal world loading. The important next Model00p evidence is either `[model00p-player] physics-layout solved ...` followed by `shapes-ok`, or `[model00p-fail] stage=physics-shape-layout ...` plus `[model00p-layout] ...` diagnostics.
