# FEARVita M29AZ — MissionDB crash analysis and fix — 2026-09-12

## Hardware observation
The full-assets M29AY VPK installs and launches on Vita, but F.E.A.R., Extraction Point, and Perseus Mandate all crash while entering the retail game after selection.

All three per-campaign logs reach the same boundary:
- retail global initialization succeeds through WeaponDB (`weapon-db-ok`)
- the final line is `before-mission-db`
- no campaign reaches completed MissionDB initialization or the later real world/object load path

The launcher path, including the retail `SplashScreenSound`, succeeds before this point.

## Core-dump correlation
Three Vita core dumps from the three campaign attempts were normalized against the exact unstripped M29AY ELF. Vita ASLR differs per process, but all three normalize to the same ELF program counter:

- dump 1789203157: normalized PC `0x815f5372`
- dump 1789203192: normalized PC `0x815f5372`
- dump 1789203227: normalized PC `0x815f5372`

That address is inside the M29AY `strcasecmp()` implementation. Disassembly of the crashing M29AY ELF showed:

```
815f536c <strcasecmp>:
...
815f537a: bl 815f536c <strcasecmp>
```

The function calls itself unconditionally. The main-thread SP in the cores is also effectively at its stack boundary, consistent with recursion until stack overflow.

## Root cause
`runtime/kernel/src/sys/win/stringmgr.cpp` is compiled for the portable runtime with `__LINUX=1`.

The FEARVita MSVC compatibility force-include historically defines:

```
#define stricmp strcasecmp
#define strnicmp strncasecmp
```

The runtime-server compatibility prelude is force-included before the source file and includes `ltbasedefs.h`. Under `__LINUX`, `ltbasedefs.h` defines an inline `stricmp` helper that calls `strcasecmp`.

Because the MSVC alias was already active, preprocessing turned that helper into a local weak definition equivalent to:

```
inline int strcasecmp(const char* a, const char* b)
{
    return strcasecmp(a, b);
}
```

That weak local symbol overrode the intended libc implementation and recursed during MissionDB case-insensitive string lookups.

## M29AZ fix
The MSVC compatibility shim now supports a per-translation-unit opt-out:

`FEARVITA_NO_MSVC_STRICMP_ALIASES=1`

CMake applies that define only to `runtime/kernel/src/sys/win/stringmgr.cpp`, before either forced compatibility header is processed. Other translation units retain the existing portability aliases.

The source also keeps a local defensive `#undef stricmp/strnicmp` before `bdefs.h` for clarity and future non-force-included builds.

### Object-level verification
After the fix:

```
stringmgr.cpp.obj: U strcasecmp
```

It no longer defines a weak `strcasecmp` implementation.

### Final ELF verification
M29AZ marker:

`FEARVita 0.02 / M29AZ; MissionDB strcasecmp recursion fix + ObjectDLL runtime`

Final ELF `strcasecmp` is a strong libc symbol (`T strcasecmp`) at `0x816bdfac`. Its disassembly performs a real case-insensitive comparison and contains no branch/call back to its own entry point.

## Build artifacts
- ARM ELF SHA-256: `50496c07cd84ff09cf6f9b7006bb2dd4fd094831a07ccb35c91398c834555d6d`
- VELF SHA-256: `f60d5de9b45bc52f7d1eee5b2634e20a782e0bf9c0e80f5042ee324386bdfb23`
- `eboot.bin` SHA-256: `151a25c5ec1d13cd5c563d811aa1e0cc6d1076f154ca801578b229229920b85c`
- full 22-file test VPK SHA-256: `63d346f36fc3f24f2c5fff7e8156a59ee66b3d3e1f4865aa0ec6fee9a3aec6cd`

The VPK contains the same ten private menu/launcher/video assets as M29AX; all ten were verified byte-identical. Private assets remain packaging-only and are not stored in source/workspace backups or GitHub.

## Validation status
The crash root cause is proven from hardware logs + three core dumps and is removed from the M29AZ binary. M29AZ itself is **not yet hardware validated** until the new VPK is retested on Vita. No game-state transition is faked, and this fix does not claim that the subsequent world-load path is already runtime-correct.
