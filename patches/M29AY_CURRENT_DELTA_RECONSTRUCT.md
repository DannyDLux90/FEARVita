# Reconstruct the 2026-09-11 current M29AY continuation delta

This is the continuation delta from the originally recovered M29AY workspace to the current backup checkpoint. It is **not** a patch against M29AX or `main`.

Metadata:
- uncompressed patch: `M29AY_CURRENT_DELTA_FROM_RECOVERED_WORKSPACE_2026-09-11.patch`
- uncompressed size: `26982` bytes
- XZ SHA-256: `ae779a99646fc1fd685760e6844a7f359daf140c4536ce9f5e0f066059b6f4a9`
- storage: `M29AY_CURRENT_DELTA_2026-09-11.patch.xz.b64.part00` + `part01`
- delta inventory: 1 added file, 12 modified files, 0 deleted files

Reconstruct:

```sh
cat patches/M29AY_CURRENT_DELTA_2026-09-11.patch.xz.b64.part00 \
    patches/M29AY_CURRENT_DELTA_2026-09-11.patch.xz.b64.part01 \
  | base64 -d > /tmp/M29AY_CURRENT_DELTA.patch.xz
sha256sum /tmp/M29AY_CURRENT_DELTA.patch.xz
# expected: ae779a99646fc1fd685760e6844a7f359daf140c4536ce9f5e0f066059b6f4a9

xz -dc /tmp/M29AY_CURRENT_DELTA.patch.xz > /tmp/M29AY_CURRENT_DELTA.patch
```

The delta includes the retail `SplashScreenSound` launcher entry behavior, the current FEAR Shared client/server compatibility work, timer/matrix compatibility, the legacy-runtime LTLink seam, and the current executable-link integration changes.
