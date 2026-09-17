# M29DI graphics pool fix — draft, 2026-09-17

The M29DH hardware crash resolves to a null write in
`vita2d_draw_array_textured` at linked PC `0x81656bb6` (runtime
`0x816aabb6`, RX relocation `+0x54000`). The preceding log contains
153 transient-pool failures. libvita2d's textured draw allocates a 16-byte
RGBA uniform without checking for failure.

## Implemented in this draft

- Preflight the GPU output vertices, worst-case alignment and hidden color
  uniform as one allocation budget. Respect the allocator's strict `end <
  pool_size` rule and its unsigned-int size limit.
- Move CPU-only projected vertices into reusable, checked heap storage. Keep
  only the output vertices in the existing 8 MiB vita2d pool.
- Release the reusable scratch allocation on renderer shutdown.
- Supply boundary/alignment/overflow tests and a standalone integration patch.

This is a targeted crash and memory-pressure correction. It does not assert
that every world draw now fits, that the benchmark completes, or that models,
timers and cinematics are complete. The retained CPU scratch buffer grows to
the largest draw seen; its peak memory use needs measurement on Vita.

## Source and applying the patch

Base: `m29dh-workspace-snapshot-2026-09-17`,
commit `eb39e81caac2970b9c3fd8238e434c0d4ddd46c9`.

This repository is a checkpoint/patch repository, not the complete M29DH
build tree. The backend hunks were prepared from the exact M29DH source
inspected in the earlier analysis. The full source is in the separate
`FEARVita_M29DH_CURRENT_WORKSPACE_SOURCE_2026-09-17.zip`.

From the original extracted `workspace/fear_work/m29ay_src` directory,
apply the standalone patch from this branch:

```sh
git apply --check /path/to/M29DI_GRAPHICS_POOL.patch
git apply /path/to/M29DI_GRAPHICS_POOL.patch
g++ -std=c++17 -O2 -Wall -Wextra -Werror -Iproject/include \
  project/tests/vita2d_pool_budget_test.cpp -o /tmp/fearvita-pool-budget-test
/tmp/fearvita-pool-budget-test
```

The patch includes the new header and test. Do not copy those files into the
original workspace before applying it. Stop if the context check fails.
The separately tracked header/test in this checkpoint branch allow CI to
exercise the allocator contract without the unavailable full source tree.

## Validation limits

The workflow compiles and runs the budget helper tests and checks patch
syntax. It does not apply the backend hunks to the original source, compile
the renderer against the complete Vita headers, build an ELF/VPK, or execute
on Vita. Those remain required gates before a release.

Local execution is blocked by a full workspace, including attempts to remove
the temporary disassembly. Newly attached files failed to materialize and
were not used. A fresh usable workspace with the source archive and matching
package is needed for full integration. CMake was also absent in the earlier
local build attempt.

Hardware gate: Extraction Point -> Performance Test -> normal result dialog,
then a second run without restarting. Check for pool errors, missing world
draws, memory growth, menu/input regressions and any new core dump.

## Next: timers and MP4 cinematics

1. Add one frame/update boundary for engine timers. All elapsed-time getters
   must return the same cached interval during that update. Preserve timer
   hierarchy, pause, time scale and update-range behavior. The current getter
   calls Sync on every read; the fade log stays almost opaque. Locate the
   actual outer loop before wiring this change. Also replace or reconcile
   the fixed `FrameSeconds() == 1/60` compatibility path.
2. Inspect the user's actual package and converted intro MP4s. Confirm the
   campaign namespace, virtual Bink -> MP4 mapping, codec/profile/pixel
   format, audio streams and duration. Confirm PlayOnce/PlaySound flags,
   AvPlayer audio delivery, EOF, skip and return to the game. Do not infer
   cinematic support from menu-video playback.
3. Re-enable the authored camera/AI event flow after underlying compatibility
   fixes. The performance-only AI node-tracker skip is still present.
4. Complete/verify object rendering, material semantics and the normal
   New Game -> Intro.World00p -> player-control path.

No timer or MP4 runtime changes, new VPK, completed benchmark, or intro
playback are claimed by this draft.
