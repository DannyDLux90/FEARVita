# FEARVita patch recovery audit — 2026-09-11

This audit compares the public `main` patch history with the canonical source snapshot rescued from `FEARVita_M29AY_SOURCE_WORKSPACE_2026-09-11`.

## Exact matches already present on public main

These canonical rescued patches are byte-identical to the existing GitHub blobs:

| Patch | Bytes | Git blob SHA |
|---|---:|---|
| M29AF.patch | 8,798 | `cbafacd21924d9a2ae83330e75b00bedc2be7138` |
| M29AO.patch | 2,067 | `8662c642ab82f43750aa3099fe698d5ec0ac5b88` |
| M29AS.patch | 5,475 | `eed8802cfbf7950e539a441cc2d0ef76a30a5503` |
| M29AU.patch | 2,414 | `73f75e3cb008d9358f8acbe899d57b9f11720c52` |
| M29AV.patch | 17,732 | `bba29865ceeb60e68567a53618fb2af9acdbab17` |

## Public patch files repaired on the recovery branch

The rescued canonical files differed from public `main`; the recovery branch now carries the full canonical text at the normal path:

| Patch | Canonical bytes | Canonical Git blob SHA |
|---|---:|---|
| M29AJ.patch | 4,931 | `b4b670a2ee521b18815293292bea2769fdd6a31d` |
| M29AN.patch | 2,415 | `6e19f972d391e4a42f83f57a9ce321e80394963d` |
| M29AR.patch | 12,607 | `53d23f03e914b5dd0cee2d2aedab886827409b95` |
| M29AT.patch | 15,897 | `5ad05b43dc90f71ce5c32cbfb9a4ca37e80db610` |

## Truncated or missing history preserved losslessly

For the larger historical corrections below, the exact rescued patch bytes are preserved in `patches/recovered/*.patch.gz.b64`. The public files are intentionally not silently replaced until the recovery set is reviewed.

| Patch | Public-main state | Canonical bytes | Canonical SHA-256 | gzip/base64 recovery file |
|---|---|---:|---|---|
| M29AG.patch | truncated (12,290 bytes) | 20,408 | `7bf45c18d0cd6e12dee8833ca4e52c99a17e85dae10f04ee2fd0da00c0b13eae` | `patches/recovered/M29AG.patch.gz.b64` |
| M29AH.patch | missing | 23,263 | `596ccc861be289cfe2efe168016033cd5c0788ad564bf8d9d76b6df9821b3436` | `patches/recovered/M29AH.patch.gz.b64` |
| M29AQ.patch | missing | 20,890 | `52604da4bc07d49ee8facf6e12408b74710bcff24e14b656fbdb752509055439` | `patches/recovered/M29AQ.patch.gz.b64` |
| M29AW.patch | truncated (7,690 bytes) | 17,658 | `592de7cba0793aeecd0bcf8f2df7ed515a2db370281d236fee4587faf1add042` | `patches/recovered/M29AW.patch.gz.b64` |

Reconstruct any preserved patch with:

```sh
base64 -d patches/recovered/M29AG.patch.gz.b64 | gzip -dc > /tmp/M29AG.patch
sha256sum /tmp/M29AG.patch
```

Substitute the desired checkpoint name and compare against the SHA-256 table above.

## M29AX recovered exactly

`patches/M29AX.patch` is now restored directly on the recovery branch:

- size: 21,745 bytes
- SHA-256: `84027a622839a442d22de640896ad494dc6001f48d3a77a03e3c3c53f04cea6a`
- Git blob SHA: `4f14ad7888d902e947ecf4956e41214599fbf1a3`

This is the exact rescued source delta corresponding to the hardware-tested M29AX private VPK.

## M29AY handoff

The canonical M29AY incremental patch is 1,131,451 bytes with SHA-256:

`9a499ec2fcd6300b6c6f843beb3066d0f2f51847b5c0160ac5c5aaf852c2df22`

The rescued canonical source snapshot includes the raw patch and its original four-part gzip/base64 handoff representation. `patches/M29AY_PATCH_RECONSTRUCT.md` records the reconstruction hashes and procedure.

M29AY is source/build progress only. The last hardware-proven binary remains M29AX; no M29AY hardware validation is claimed.
