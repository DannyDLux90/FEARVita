# M29BJ recovery

Base branch/checkpoint: `m29bi-object-props-loading-state` / M29BI.

Apply the compressed patch:

```sh
base64 -d M29BJ_FROM_M29BI.patch.gz.b64 | gzip -dc > M29BJ_FROM_M29BI.patch
git apply M29BJ_FROM_M29BI.patch
```

Patch SHA-256: `6c91af8c775c56d9feadb5c111f8fe6761d18a92aa93825df8fb71b3b6825801`  
Compressed payload SHA-256: `6740b5956b94fdb8dbb7f536eb66163e8684dcf9a983ec28db858e636b375b60`

M29BJ changes are intentionally small and hardware-frontier driven:
- enable the desktop SoundDB file-selection implementation for `PLATFORM_VITA` in both random-file functions;
- remove the duplicate white GT4 loading fallback while retaining the real retail loading bar;
- bump runtime/package marker to 0.07 / M29BJ.

No retail game data, VPK, EBOOT or proprietary assets are stored in this recovery payload.
