# Reconstruct the canonical M29AY patch

The canonical incremental patch is generated against the M29AX build-verified source baseline.

Patch metadata:
- uncompressed file: `M29AY.patch`
- uncompressed size: `1133579` bytes
- uncompressed SHA-256: `347014192e81f6aa96c4555352bd8652387530e3f93325ceb3d33b7c44307bf4`
- gzip SHA-256: `100715abada3056d450b52d32e832d49d52d71087307d86e97d8b9ca70327b64`
- base64 text SHA-256: `a40528db106a81f6525aa4b59839d3fc651bffa69cdc5f3038fec0847948aa43`

The GitHub connector stores the compressed/base64 representation as four text files:

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
# expected: 347014192e81f6aa96c4555352bd8652387530e3f93325ceb3d33b7c44307bf4

git apply --check /tmp/M29AY.patch
git apply /tmp/M29AY.patch
```

The patch contains 61 changed/new files. It includes the M29AY three-campaign localization fallback, ObjectDLL target/build changes, FEAR SDK 1.08 compatibility overlays, Player object unguaranteed-data transport, world/light/object-template compatibility and the new-chat handoff documents.
