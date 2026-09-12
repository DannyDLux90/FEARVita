# FEARVita M29AY — Runtime Server Recovery Checkpoint — 2026-09-12

This checkpoint preserves the reconstructed real LithTech server-runtime expansion after a container reset. It is based on the verified 2026-09-11 workspace backup and restores the runtime-server target to a clean ARM/Vita build.

## Verified local backups

- `FEARVita_M29AY_SOURCE_CURRENT_2026-09-12.zip`
  - SHA-256: `eb60618ca26536739109903bd9c4d25333fb90a52eebfe37f8234b5c1fb6f42a`
- `FEARVita_M29AY_WORKSPACE_CURRENT_2026-09-12.zip`
  - SHA-256: `7666a5cc93c4a528e64c1710c0cac6a95da5f789cfbef5c43fe34d29b77330d1`
- Both archives passed full `unzip -t` integrity testing.

## Runtime-server state

`fearvita_runtime_server_objects` is restored and clean under Ninja (`ninja: no work to do` after a successful ARM/Vita compile). The target contains the real public LithTech server/runtime pieces currently needed by the local single-player path, including client/server state, class/object management, packet/net manager local path, world tree, model/animation support, sound data, file tree primitives and Vita platform glue.

The source list contains 38 C++ translation units; Ninja's previous `[39/39]` display included its target/build bookkeeping step.

Important compatibility choices retained:

- FEAR's templated `LTLink<T>` / `LTObjRef` ABI remains intact for FEAR code.
- Old LithTech runtime list operations use isolated legacy list types in the Vita runtime compatibility prelude.
- UDP/internet driver creation is disabled on Vita; local networking remains available for the local server path.
- Server extra-data/object-bank handling is mapped to FEAR/Jupiter-EX's seven object types rather than inventing old LithTech object-type numbers.
- No fake `GS_PLAYING` transition or server-state stub is used.

## Exact recovery delta

The delta from the verified 2026-09-11 source backup to this checkpoint is preserved as six text chunks:

`patches/recovered/M29AY_RUNTIME_SERVER_RECOVERY_2026-09-12.patch.xz.b64.part00` through `part05`.

Metadata:

- raw patch size: `167322` bytes
- raw patch SHA-256: `9b5470218fed8f5fafca9e2bc253f38a2e7bc18ba2c3af0a35464ab28db93da0`
- xz size: `34784` bytes
- xz SHA-256: `b0716d0215fdf26712ec8ecc6a3c6d326047a414b1f1970b5ecf8ae61e75bfa2`
- base64 size: `46380` characters
- base64 SHA-256: `50a787b98e071005a38a83154b517038d3dbe4fd96ff351347b1f70d1f07c031`
- parts 00–04: 8000 chars each
- part05: 6380 chars

Reconstruct:

```sh
cat patches/recovered/M29AY_RUNTIME_SERVER_RECOVERY_2026-09-12.patch.xz.b64.part{00..05} \
  > /tmp/m29ay-runtime.patch.xz.b64
base64 -d /tmp/m29ay-runtime.patch.xz.b64 > /tmp/m29ay-runtime.patch.xz
xz -dc /tmp/m29ay-runtime.patch.xz > /tmp/m29ay-runtime.patch
sha256sum /tmp/m29ay-runtime.patch
# expected: 9b5470218fed8f5fafca9e2bc253f38a2e7bc18ba2c3af0a35464ab28db93da0
```

The patch paths are rooted at the restored workspace layout (`m29ay_src/...` and `m29ay_lithtech/...`).

## Next frontier

Run a fresh full `FEARVita` target and use the resulting undefined-symbol list as the sole guide for additional real upstream runtime TUs. Continue through ELF -> VELF -> `eboot.bin`, but do **not** invoke VPK packaging yet.

M29AX remains the last hardware-proven build; this M29AY checkpoint is not hardware validated.
