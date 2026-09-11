# Reconstruct the canonical M29AY patch

The canonical incremental M29AY patch is generated against the M29AX build-verified source baseline.

Patch metadata:
- uncompressed file: `M29AY.patch`
- uncompressed size: `1131451` bytes
- uncompressed SHA-256: `9a499ec2fcd6300b6c6f843beb3066d0f2f51847b5c0160ac5c5aaf852c2df22`
- XZ SHA-256: `b94abcd0c28e67ebdf0dbbcaeed0508a7568eb17a9db3b647fb1e4ecfb731751`
- storage: `patches/M29AY.patch.xz.b64.part00` through `part29`

Reconstruct on a Unix-like host:

```sh
cat patches/M29AY.patch.xz.b64.part{00..29} | base64 -d > /tmp/M29AY.patch.xz
sha256sum /tmp/M29AY.patch.xz
# expected: b94abcd0c28e67ebdf0dbbcaeed0508a7568eb17a9db3b647fb1e4ecfb731751

xz -dc /tmp/M29AY.patch.xz > /tmp/M29AY.patch
sha256sum /tmp/M29AY.patch
# expected: 9a499ec2fcd6300b6c6f843beb3066d0f2f51847b5c0160ac5c5aaf852c2df22

git apply --check /tmp/M29AY.patch
git apply /tmp/M29AY.patch
```

This canonical patch preserves the recovered M29AY state including the three-campaign localization work, 533/533 ARM ObjectDLL compatibility, Player unguaranteed-data transport, world/light/object-template compatibility, and the recovered full-executable ClientShell fixes.

Later continuation work from the same 2026-09-11 session is stored separately as `M29AY_CURRENT_DELTA_2026-09-11.patch.xz.b64.part00` and `part01`; that delta is relative to the recovered M29AY workspace, not to M29AX.
