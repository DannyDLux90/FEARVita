# FEARVita M29BM / 0.10 — local-client null-safety crash fix

Date: 2026-09-12

## Hardware regression observed in M29BL / 0.09

All three campaigns crashed immediately after starting a new game. The three runtime logs stop at exactly the same point:

- ObjectDLL loaded successfully.
- Local network driver started successfully.
- Last line is `[server-world] listen-local-ok`.
- No M29BL `[local-handoff]` marker is reached.

The three uploaded PSP2 core dumps all resolve to the same fault:

- Data Abort in `CLTServer::GetClientAddr(HCLIENT, uint8[4], uint16*)`.
- Caller: `BanIPMgr_Impl::IsClientBanned(HCLIENT)` during `ServerConnectionMgr::OnAddClient`.
- M29BL creates the authentic local server-side `Client` with `sm_OnNewConnection(NULL, true)`.
- That client intentionally has no packet-level `CBaseConn`, so `Client::m_ConnectionID == NULL`.
- Upstream `GetClientAddr` dereferenced `m_ConnectionID` unconditionally.

This explains the regression before world loading begins; it is unrelated to NavMesh or Intro world data.

## M29BM fix

M29BM keeps the authentic FEAR local-client/player state machine and makes only the connectionless-local runtime path null-safe:

1. `CLTServer::GetClientAddr`: a connectionless client reports LithTech's localhost sentinel `0.0.0.0:0` instead of dereferencing NULL. This matches BanIPMgr's existing localhost semantics.
2. `CLTServer::SendTo`: skips connectionless clients when scanning packet endpoints.
3. `Client::~Client`: does not terminate a NULL file-transfer server.
4. `sm_UpdateClientFileTransfer`: skips when no file-transfer server exists.
5. `sm_UpdateClientInWorld`: skips packet/bandwidth replication for the connectionless local client; FEARVita's local control/state bridge remains responsible for in-process handoff.
6. `IServerFileMgr::AddUsedFile`: does not add files to a NULL file-transfer server.
7. Kicked connectionless clients are removed locally rather than passed to `NetMgr::Disconnect` with a NULL connection.

Singleplayer `ServerConnectionMgr::OnAddClient` does not consume NetClientData during this early path; it sets the real FEAR connection state to `LoggedIn`. The existing StartGameRequest client-data preservation remains intact.

## Build

- Runtime marker: `FEARVita 0.10 / M29BM; connectionless local client null-safe handoff`
- APP_VER: `00.10`
- Full 22-payload-file VPK layout retained.
- VPK SHA-256: `6bf6cda4209f9beeb0a75e9b57fb032bd4dd9ee3b4ea9326c6f58ae066952b49`
- eboot.bin SHA-256: `e75192cfe199c93ac1ec6696be16152ac9be73ede9bec0c1431567c24d86417b`
- Embedded VPK eboot verified byte-for-byte against the fresh build.

## Hardware test

Test Base F.E.A.R. first: New Game -> Medium.

Expected new frontier at minimum:

- `[server-world] listen-local-ok`
- `[local-handoff] server-client-ready ...`

Then watch for world-load progress and, after the server world starts, the genuine FEAR local handoff markers. If a new crash occurs, preserve the new campaign log and PSP2 core dump; it should now symbolize beyond the former `GetClientAddr` fault.
