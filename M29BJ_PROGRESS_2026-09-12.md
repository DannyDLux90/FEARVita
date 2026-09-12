# FEARVita M29BJ progress — 2026-09-12

## Hardware evidence from M29BI

The M29BI Vita run proves the Jupiter EX v113 bootstrap is now substantially inside the genuine F.E.A.R. Intro load. All 347 collision/world BSPs finish, BlindData reports 93 chunks, the object section declares 1,988 objects, and the retail progress callback reaches 70%. The run proceeds through at least object index 1151 before faulting.

The loading-screen screenshot also proves that the retail cyan progress bar works. The second upper white bar was the temporary Vita GT4 fallback introduced during earlier loading-screen bring-up, so M29BJ removes that fallback entirely rather than maintaining two progress displays.

## Crash resolution

The M29BI core dump maps the main-thread fault to `CSoundSet::GetRandomFile()`. Disassembly showed a compiler-generated `UDF #255` at the platform fall-through. In `FEAR/Shared/SoundDB.cpp`, the real database-backed implementation was guarded by `PLATFORM_WIN32 || PLATFORM_LINUX`, excluding Vita. `CSoundSet::GetRandomNotDirtyFile()` had the same defect and was fixed at the same time.

M29BJ adds `PLATFORM_VITA` to both guards. This uses the same F.E.A.R. GameDB sound-file/weight selection path used by the desktop runtime instead of adding a Vita-specific approximation.

## Loading UI

`CLoadingScreen::Update()` still calls the retail `m_LoadProgress.Render()` path. The explicit white GT4 outline/track/fill fallback has been removed. The concrete DrawPrim state restoration added in M29BI remains in place so the mission background stays textured during synchronous loading updates.

## Known next frontier

The same hardware log contains many `MODEL00P ... Invalid Header` messages. They did not cause the M29BI crash and the loader continued through hundreds of objects, so M29BJ deliberately does not mix a speculative model-format rewrite into this crash fix. If the SoundSet trap is cleared and object creation advances to completion, the Jupiter EX model loader is the likely next major compatibility block to address.

## Artifact verification

- Version: `0.07 / M29BJ`
- Complete VPK payload files: 22
- ZIP entries including directories: 35
- EBOOT SHA-256: `d35ca4ef30211ec5c40f064febf1b1a34ba08a387586afa4c1636d82c2c57ff9`
- VPK SHA-256: `c24cb6c166434f3b46fb0889b09a8f9c23a62b25a6c897078a4299c03e00f55e`
- Patch SHA-256: `6c91af8c775c56d9feadb5c111f8fe6761d18a92aa93825df8fb71b3b6825801`
