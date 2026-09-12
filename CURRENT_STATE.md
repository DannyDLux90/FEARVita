# FEARVita current state

**Public package version:** 0.07  
**Internal checkpoint:** M29BJ  
**Date:** 2026-09-12

M29BJ advances the real F.E.A.R. Intro local-world path. Hardware-tested M29BI parsed all 347 Jupiter EX v113 BSPs, detected 93 BlindData chunks, entered the 1,988-object server section, reached at least object 1151, and drove the genuine retail loading bar to 70% before the next deterministic crash.

The M29BI core dump resolved that crash to `CSoundSet::GetRandomFile()`: Vita was excluded from the Win32/Linux database-backed sound-file selection implementation, leaving a non-void platform fall-through that compiled to `UDF #255`. M29BJ enables the same implementation for `PLATFORM_VITA` in both `GetRandomFile()` and `GetRandomNotDirtyFile()`.

The temporary white GT4 loading-bar fallback has been removed. The working retail cyan `m_LoadProgress` bar is now the only loading bar. The M29BI textured-background DrawPrim-state fix remains.

Known upcoming issue: the current hardware log reports many Jupiter EX `MODEL00P ... Invalid Header` model loads. They are not the M29BI crash source and are intentionally left for the next verified frontier rather than combined speculatively with the SoundSet fix.

For continuation, use GitHub branch **`m29bj-soundset-single-loading-bar`** and read `CURRENT_STATE_M29BJ.txt`, `M29BJ_PROGRESS_2026-09-12.md`, and `recovery/M29BJ_RECOVERY.md`.
