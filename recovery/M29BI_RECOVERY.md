# M29BI recovery

Base branch/checkpoint: `m29bh-jupiter113-worldloader` / M29BH.

Apply the M29BI delta by decoding and decompressing:

```sh
base64 -d recovery/M29BI_FROM_M29BH.patch.gz.b64 | gzip -dc > M29BI_FROM_M29BH.patch
patch -p1 < M29BI_FROM_M29BH.patch
```

Expected decoded patch SHA-256:
`92ca53c1fc8d3ee186e47d9af9b6f7896b88806fa501dfe854f9ce5b8b7e89f5`

Stored base64 file SHA-256:
`05593edc194797060a3a8768d33b85ff3c7c7ae9f2ee7126b71398b786506894`

M29BI is Vita app version `00.06`. It fixes the null GenericPropList legacy object-create bridge revealed by the M29BH hardware core dump and explicitly restores DrawPrim texture/blend state around the GT4 loading-progress fallback. Audio is intentionally unchanged from M29BH/M29BG.

Build/package hashes are recorded in `M29BI_PROGRESS_2026-09-12.md` and `CURRENT_STATE_M29BI.txt`. Retail game data and VPK binaries are intentionally not stored in this public recovery branch.
