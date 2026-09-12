# FEARVita current state

**Public package version:** 0.07  
**Internal checkpoint:** M29BJ  
**Date:** 2026-09-12

M29BJ advances the real F.E.A.R. Intro local-world path. Hardware-tested M29BI parsed all 347 Jupiter EX v113 BSPs, detected 93 BlindData chunks, entered the 1,988-object server section, reached at least object 1151, and drove the genuine retail loading bar to 70% before the next deterministic crash.

The M29BI core dump resolved that crash to `CSoundSet::GetRandomFile()`: Vita was excluded from the Win32/Linux database-backed sound-file selection implementation, leaving a non-void platform fall-through that compiled to `UDF #255`. M29BJ enables the same implementation for `PLATFORM_VITA` in both `GetRandomFile()` and `GetRandomNotDirtyFile()`.

The temporary white GT4 loading-bar fallback has been removed. The working retail cyan `m_LoadProgress` bar is now the only loading bar. The M29BI textured-background DrawPrim-state fix remains.

M29BJ also addresses the repeated `MODEL00P ... Invalid Header` messages without bypassing validation: the old model loader accepted only `.ltb` filenames and rejected F.E.A.R.'s `.Model00p` extension before reading its LTB header. `.Model00p` now enters the same existing header/version path as `.ltb`, so the next hardware run either loads those models or reveals the next genuine model-format incompatibility.

For continuation, use GitHub branch **`m29bj-soundset-single-loading-bar`** and read `CURRENT_STATE_M29BJ.txt`, `M29BJ_PROGRESS_2026-09-12.md`, and `recovery/M29BJ_RECOVERY.md`.
