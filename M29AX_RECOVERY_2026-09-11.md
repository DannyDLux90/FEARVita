# FEARVita M29AX recovery checkpoint

Date: 2026-09-11
Recovery source: private test VPK and locally preserved VitaSDK/LithTech inputs supplied after chat-state loss.

## Why this checkpoint exists

The public repository currently ends at M29AW, while the preserved private test package is a later M29AX build. The repository README describes `project/` compatibility/build sources and a `lithtech-overlay/`, but the current tree does not contain those source trees (apart from `project/tools/`). This document preserves the independently recoverable M29AX evidence without pretending that the missing source delta has already been reconstructed.

## Confirmed M29AX binary identity

Private VPK filename:

`FEARVita_M29AX_0.02_DPAD_TOUCH_DE_LOADING_PRIVATE_2026-09-11(1).vpk`

- size: 17,698,777 bytes
- SHA-256: `2831de6f48dddba77416b27bbaee54dfcdb0b8a8582734978166ab292c9434a2`
- `sce_sys/param.sfo`: title `F.E.A.R. Vita`, title id `FEAR00001`, app version `00.02`
- `eboot.bin`: 3,050,929 bytes
- VPK entries: 22

The `eboot.bin` is an unencrypted compressed Vita FSELF. Its three program segments were decompressed to a 14,581,036-byte VELF for string/evidence inspection. No retail asset was needed to inspect the executable.

The executable contains this exact startup marker:

`FEARVita 0.02 / M29AX; D-pad + touchscreen retail-menu navigation + German loading fallback`

It also contains the controller/backend marker:

`vita-scectrl-touch-m29ax`

and links against/contains the Vita touch module name:

`SceTouch`

## Confirmed launcher/navigation behavior in the executable

The M29AX executable contains localized selector instructions that establish the intended launcher interaction:

- English: `Left/Right: select   X: start   Touch: select / tap again to start   Circle: exit`
- German: `Links/Rechts: waehlen   X: starten   Touch: waehlen / erneut tippen: starten   Kreis: beenden`
- diagnostic channel: `launcher-touch`
- diagnostic fields include `selected=` and `activate=`

The executable also retains the retail-frontend state diagnostics and explicit marker that M29AX adds D-pad/touchscreen retail-menu navigation.

## Confirmed retained M29AW functionality

M29AX still contains the canonical Vita control-profile diagnostic:

`vita-profile=killzone-style-v1 L=aim R=fire X=jump O=crouch Square=reload Triangle=use dpad=slowmo/grenade/weapons front-touch=flashlight/melee/next rear=doubletap-hold-sprint`

It also retains:

- `restore-defaults applied canonical Vita profile`
- `loading-localize`
- `fallback=de-steam-base-intro applied=1`
- `client-handshake ok; waiting-for-world/server-object-runtime`

Therefore the known M29AW control/default-profile, first base-game German loading fallback, and local-session/loading frontier are present in the M29AX binary.

## Private assets deliberately not committed

The private VPK includes campaign artwork and user-owned converted retail menu videos under paths such as:

- `boot_art/`
- `launcher_art/`
- `video_cache/fear/videos/menu.mp4`
- `video_cache/ep/videosxp/menu.mp4`
- `video_cache/pm/videosxp2/menuxp2.mp4`

These are evidence that the private package is complete, but they remain outside the public repository in line with the repository policy.

## Recovered upstream/toolchain anchors

The supplied `lithtech-master(7).zip` identifies upstream commit:

`0eab18289bed72879eddb648d3311075b108cf46`

This exactly matches `UPSTREAM_PIN.txt`, so the public LithTech base is preserved. The archive SHA-256 is:

`9c6cab7d104301024b67d7d63d166c595a6b64012bc325232f1dbd52f05c7e4b`

The preserved build environment includes VitaSDK core `2026.08.1-1`, VDPM, libvita2d, FreeType, libjpeg-turbo, libpng and zlib. Exact package hashes are recorded in `RECOVERY_INPUTS_2026-09-11.txt`.

## What is still missing

This recovery proves what the M29AX executable is and what behavior was compiled into it, but it does **not** reconstruct an exact source patch from M29AW to M29AX. The binary should therefore be treated as the behavioral oracle while recreating the missing source delta.

The first reconstruction target should be the Vita controller/touch path plus launcher/retail-menu navigation, preserving the exact M29AX startup/backend markers until a rebuilt VPK matches the known behavior on hardware.
