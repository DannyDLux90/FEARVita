# FEARVita M29AY — installable VPK checkpoint — 2026-09-12

## Build artifacts

- ARM ELF `FEARVita`: SHA-256 `7fa7a2ab6957bb46c7c98574f6e02ea79b2f8601c7ee26fb584eb6cde21a0b05`
- VELF `FEARVita.velf`: SHA-256 `7614746c596072065680140138d586a6d8a2fa5141d297753b3004aa78438a37`
- SELF `eboot.bin`: SHA-256 `681aab35c2e7b801864f1dcfc67df0c523e33890d9a615927e8c4d17e7c72e95`
- standalone VPK `FEARVita_M29AY_0.02_OBJECTDLL_RUNTIME_SPLASH_2026-09-12.vpk`: SHA-256 `6fa6302c96c9f6ba0c977f441269ed861d5835b9b49831dc88339c818ce22672`

## Verification

- Full FEARVita executable link: PASS, no undefined references.
- VELF conversion: PASS.
- SELF generation: PASS.
- VPK integrity: PASS.
- VPK contents: 12 files.
- `TITLE_ID=FEAR00001`.
- `APP_VER=00.02`.
- Embedded `eboot.bin` is byte-identical to the verified build SELF.
- The selector uses the installed retail FEAR database `SplashScreenSound`; no retail audio/game asset is bundled in the VPK.

## Recovery delta

The Runtime54 -> Runtime64/final/VPK source continuation is stored as:

`patches/recovered/M29AY_RUNTIME64_FINAL_VPK_DELTA_2026-09-12.patch.xz.b64.part00`

Metadata:
- raw patch size: 10624 bytes
- raw SHA-256: `3b2d68bd960c1b37c07f51749ff89389818e79cdc80e1d23f697e9f2a0de4bcc`
- xz size: 3912 bytes
- xz SHA-256: `ff031cf740e7a86dab6625c2cf3f3d85240de33ee3040b873f1f71bf4040435c`
- base64 size: 5216 chars
- base64 SHA-256: `d5c6141e66bd2394714e40dcdb56b2fb2ff634b1f89212f0e54bc96927a605a4`

## Validation status

This is an installable **test VPK**, not a hardware-proven release. M29AX remains the last hardware-validated build until this M29AY VPK is installed and tested on a real Vita with fresh FEAR / Extraction Point / Perseus Mandate logs.
