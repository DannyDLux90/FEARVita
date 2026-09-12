# M29BK recovery

Base branch/checkpoint: `m29bj-soundset-single-loading-bar` / M29BJ.

Reconstruct the source delta:

```sh
base64 -d M29BK_FROM_M29BJ.patch.gz.b64 | gzip -dc > M29BK_FROM_M29BJ.patch
git apply M29BK_FROM_M29BJ.patch
```

Patch SHA-256: `3a3c9b05c33f75915beb3068518e807ef5eb71acd442c63d51a1238f76a15f0d`  
Compressed payload SHA-256: `bb494ba3838abc1111e942fd853cfdcfaeac3c467eb3f5ff686dc9aae4da5d4a`

M29BK is the NavMesh ABI milestone:
- build FEAR/LithTech Vita targets with `-fno-short-enums` to match Win32/MSVC serialized enum width;
- verify critical packed NavMesh structure sizes at compile time;
- pass the actual BlindObject buffer size into `CAINavMesh::RuntimeSetup` and preflight every packed section before pointer fix-up;
- fix the stale edge-list count reset;
- suppress repetitive `FindObjectsCB` overflow logging and raise the runtime log cap to 2 MiB;
- keep only the retail cyan loading bar and leave audio unchanged.

No VPK, EBOOT, retail game data or proprietary assets are stored in this recovery payload.
