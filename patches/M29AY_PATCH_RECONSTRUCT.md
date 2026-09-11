# Reconstruct the canonical M29AY patch

The canonical incremental patch is generated against the M29AX build-verified source baseline.

Patch metadata:
- uncompressed file: `M29AY.patch`
- uncompressed size: `1131451` bytes
- uncompressed SHA-256: `9a499ec2fcd6300b6c6f843beb3066d0f2f51847b5c0160ac5c5aaf852c2df22`
- gzip SHA-256: `a339d475d6d0c2cdd4146226cefdb97ac0d1aa83a0bb0eadbd94e7d4bd0b6b66`
- base64 text SHA-256: `f4f923b6e10a1e4d6705a3de2525b099c8a744696e745babad8f9dfb56219ccf`

The rescued workspace stores the compressed/base64 representation as four text files:

- `patches/M29AY.patch.gz.b64.part00`
- `patches/M29AY.patch.gz.b64.part01`
- `patches/M29AY.patch.gz.b64.part02`
- `patches/M29AY.patch.gz.b64.part03`

Reconstruct on a Unix-like host:

```sh
cat patches/M29AY.patch.gz.b64.part00 \
    patches/M29AY.patch.gz.b64.part01 \
    patches/M29AY.patch.gz.b64.part02 \
    patches/M29AY.patch.gz.b64.part03 \
  | base64 -d > /tmp/M29AY.patch.gz

gzip -dc /tmp/M29AY.patch.gz > /tmp/M29AY.patch
sha256sum /tmp/M29AY.patch
# expected: 9a499ec2fcd6300b6c6f843beb3066d0f2f51847b5c0160ac5c5aaf852c2df22

git apply --check /tmp/M29AY.patch
git apply /tmp/M29AY.patch
```

The patch contains the three-campaign localization fallback, the complete 533/533 ARM ObjectDLL compatibility work, Player object unguaranteed-data transport, world/light/object-template compatibility, and the current full-executable ClientShell fixes including explicit `ltobb.h` inclusion for `LTOBB` geometry helpers.
