# FEARVita M29BJ progress — 2026-09-12

## Hardware evidence from M29BI

The M29BI Vita run proves the Jupiter EX v113 bootstrap is now substantially inside the genuine F.E.A.R. Intro load. All 347 collision/world BSPs finish, BlindData reports 93 chunks, the object section declares 1,988 objects, and the retail progress callback reaches 70%. The run proceeds through at least object index 1151 before faulting.

The loading-screen screenshot also proves that the retail cyan progress bar works. The second upper white bar was the temporary Vita GT4 fallback introduced during earlier loading-screen bring-up, so M29BJ removes that fallback entirely rather than maintaining two progress displays.

## Crash resolution

The M29BI core dump maps the main-thread fault to `CSoundSet::GetRandomFile()`. Disassembly showed a compiler-generated `UDF #255` at the platform fall-through. In `FEAR/Shared/SoundDB.cpp`, the real database-backed implementation was guarded by `PLATFORM_WIN32 || PLATFORM_LINUX`, excluding Vita. `CSoundSet::GetRandomNotDirtyFile()` had the same defect and was fixed at the same time.

M29BJ adds `PLATFORM_VITA` to both guards. This uses the same F.E.A.R. GameDB sound-file/weight selection path used by the desktop runtime instead of adding a Vita-specific approximation.

## Loading UI

`CLoadingScreen::Update()` still calls the retail `m_LoadProgress.Render()` path. The explicit white GT4 outline/track/fill fallback has been removed. The concrete DrawPrim state restoration added in M29BI remains in place so the mission background stays textured during synchronous loading updates.

## Proactive MODEL00P compatibility

The M29BI log also showed many `MODEL00P ... Invalid Header` messages. Inspection of the old runtime loader showed those messages were generated before header parsing: `Model::Load` hard-rejected every extension except `.ltb`, while F.E.A.R. references its compiled packed models as `.Model00p`. M29BJ accepts `.model00p` in the same existing LTB header/version path. This is intentionally narrow: it does not bypass header or version validation. If F.E.A.R.'s model payload differs beyond the extension, the next run will now expose the real header/version/section error instead of the misleading extension rejection.

## Artifact verification

- Version: `0.07 / M29BJ`
- Complete VPK payload files: 22
- ZIP entries including directories: 35
- EBOOT SHA-256: `fcbec301a0712f6d5d54121c0950623c943d3c39fc71a8c02655986a7f67e772`
- VPK SHA-256: `a07ecdfa7549ab255a1fc27f36a42cfa6e5ae2c153222e361de2c7cf0296cbd3`
- Patch SHA-256: `6c77c7df5fc212a1c69d2ecf7f601e85841bbd654e95a470d3e2b86e070ab12e`
