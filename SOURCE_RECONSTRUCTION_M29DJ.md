# M29DJ source reconstruction

M29DJ is a source/checkpoint milestone; an installable VPK is not required to preserve this state.

## Identifiers

- Repository: `DannyDLux90/FEARVita`
- M29DH base branch: `m29dh-workspace-snapshot-2026-09-17`
- M29DH base commit: `eb39e81caac2970b9c3fd8238e434c0d4ddd46c9`
- M29DJ integration branch: `m29di-graphics-pool-fix` (legacy name retained for PR #5)
- LithTech upstream: `https://github.com/jsj2008/lithtech`
- LithTech pin: `0eab18289bed72879eddb648d3311075b108cf46`
- Reference M29DH workspace ZIP SHA-256: `59dca232d2bdcf711c5b59c56d21066952242a0cacfff01fc18804caa00b10d0`
- M29DJ consolidated patch SHA-256: `90f06fc1c46ed9ebaeb97294e2bb20729570369729e7e338b1921dbae7e35092`

## Current delta

`patches/M29DJ_RUNTIME_INTEGRATION.patch` is the single current patch from the exact M29DH workspace source to M29DJ. It includes the graphics-pool integration, frame timer semantics, dynamic retail frame time, Bink/AvPlayer audio/EOF behavior and recursive MP4-cache packaging.

The separately tracked allocator helper/header and host test remain in the repository so GitHub Actions can validate the most failure-sensitive allocation contract without reconstructing the entire Vita build tree.

## Validation command

From an unmodified M29DH workspace source root:

```sh
git apply --check /path/to/M29DJ_RUNTIME_INTEGRATION.patch
git apply /path/to/M29DJ_RUNTIME_INTEGRATION.patch

g++ -std=c++17 -O2 -Wall -Wextra -Werror \
  -Iproject/include project/tests/vita2d_pool_budget_test.cpp \
  -o /tmp/fearvita-pool-budget-test
/tmp/fearvita-pool-budget-test
```

Expected allocator test result: `PASS: 403264 accepted draw layouts satisfy the libvita2d contract`.

## Repository cleanup policy

Only `CURRENT_STATE.md` describes the active milestone. Old per-milestone state/progress/handoff files are intentionally removed from the active branch once superseded. They remain recoverable from Git history and their historical branches. Older checkpoint patches are retained where they are needed to understand/reconstruct pre-M29DH lineage.
