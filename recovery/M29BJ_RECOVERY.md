# M29BJ recovery

Base branch/checkpoint: `m29bi-object-props-loading-state` / M29BI.

Apply the compressed patch:

```sh
base64 -d M29BJ_FROM_M29BI.patch.gz.b64 | gzip -dc > M29BJ_FROM_M29BI.patch
git apply M29BJ_FROM_M29BI.patch
```

Patch SHA-256: `6c77c7df5fc212a1c69d2ecf7f601e85841bbd654e95a470d3e2b86e070ab12e`  
Compressed payload SHA-256: `cde8efc3d9a33a687d533c6f46997bc5c932484176c2d1afb8569a4ec1234b6c`

M29BJ changes are hardware-frontier driven:
- enable the desktop SoundDB file-selection implementation for `PLATFORM_VITA` in both random-file functions;
- remove the duplicate white GT4 loading fallback while retaining the real retail loading bar;
- accept F.E.A.R. `.Model00p` filenames in the existing LTB model header/version loader path;
- bump runtime/package marker to 0.07 / M29BJ.

No retail game data, VPK, EBOOT or proprietary assets are stored in this recovery payload.
