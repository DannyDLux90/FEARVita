# FEARVita M29BA artifacts — 2026-09-12

## Standalone VPK
- `FEARVita_M29BA_0.02_LTOBJREF_ABI_FIX_2026-09-12.vpk`
- size: `21923532` bytes
- SHA-256: `47fa72f0f5166f3ccf9298607b9c1fee02cec3d24ec7997b63675e59e6a217e0`
- ZIP/VPK integrity: PASS
- entries: 22
- embedded eboot.bin SHA-256: `8f8cd8c62b92711913e678bd71df64357e81987bfc1f4a16f706a6f7c5f82316`
- 10 private menu/launcher/video assets verified byte-identical to M29AX.

## Build chain
- ELF: `27ff2a108c04e1e01d92c100768ef1d66f4501ac94266816a4b40100045c8b59`
- VELF: `7b41b6cb478b8a9d667e32bde1057a9b131c66b62257969a172e056ee8398499`
- eboot.bin: `8f8cd8c62b92711913e678bd71df64357e81987bfc1f4a16f706a6f7c5f82316`

## Current backups
- Source ZIP: `FEARVita_M29BA_SOURCE_LTOBJREF_FIX_2026-09-12.zip`
  - size: `46278949` bytes
  - SHA-256: `37c70db14d6fd2d8abba882a39559007e1d8e243998e86b9bbc4259ff5ae801a`
  - integrity: PASS
- Workspace ZIP: `FEARVita_M29BA_WORKSPACE_LTOBJREF_FIX_2026-09-12.zip`
  - size: `116999981` bytes
  - SHA-256: `083748364213c1ec04b05d5fe442f2efbf1778c89f4f98167d7e942b77d03cf5`
  - integrity: PASS

Both backup ZIPs exclude VPK files and private packaging assets. The workspace includes the M29AZ hardware-retest logs, all three uploaded core dumps, core normalization notes, and M29BA build logs.

## Recovery delta
Exact M29AZ -> M29BA code delta (4 code files):
- raw patch SHA-256: `aab4e2ac6416f75d4a0c3823cbf8225adb03b920ed087feede4432bfa4a09bca`
- xz SHA-256: `30a706f7574d9e6fbb7fbc7b29faa1579e51f2e9c2d7d00c40acd1d4ff439841`
- base64 SHA-256: `dbe5ceacb1cec75e8953507c847d56d2673b1e355b8caa97bee42c242e11a75b`
