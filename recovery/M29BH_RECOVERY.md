# M29BH recovery

Checkpoint: FEARVita 0.05 / M29BH (2026-09-12)

The M29BH delta from the M29BG source state is stored as two base64 chunks:

- `M29BH_FROM_M29BG.patch.gz.b64.part00` — 6500 bytes
- `M29BH_FROM_M29BG.patch.gz.b64.part01` — 5844 bytes

Reconstruct with:

```sh
cat recovery/M29BH_FROM_M29BG.patch.gz.b64.part00 \
    recovery/M29BH_FROM_M29BG.patch.gz.b64.part01 > /tmp/M29BH.patch.gz.b64
base64 -d /tmp/M29BH.patch.gz.b64 > /tmp/M29BH.patch.gz
gzip -dc /tmp/M29BH.patch.gz > /tmp/FEARVita_M29BH_FROM_M29BG.patch
```

SHA-256:

- reconstructed base64: `907ad2e290b65a9957b7ba2ce41ec84eabd23af62bee36570a330d94be29d26d`
- gzip: `452d14127adcc8fba1959a8e51cdd510b3fa1da8ef74a5eb1ed043bbe2d17c44`
- patch: `030f4ac1f061883fc55b2d86f0d059120ed55c7f48b66df4ca9b5945ea06ca09`

The patch contains the v113 shared-world loader, v113 server object and blind-data paths, the deferred v113 client-render boundary, the loading-bar placement adjustment, and the M29BH/00.05 build markers.

Retail game data and VPK payloads are intentionally not stored in this public repository.
