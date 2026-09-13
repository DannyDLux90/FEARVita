# FEARVita M29BQ / 0.14 checkpoint — Model00p global physics-shape layout solver

Date: 2026-09-13
Branch target: `m29bq-model00p-global-shape-layout`
Baseline: M29BP / 0.13

## Hardware evidence from M29BP

Both Base F.E.A.R. Intro and Extraction Point Performance load the world to 100%, but the local player is not created. `CHARS\\MODELS\\PLAYER.MODEL00P` reaches the v33 physics block and then fails during shape-layout decoding. The first Player shape is parsed with tag `2`, node `7`, quaternion w about `0.485057`, and a 24-byte extension; the next record cannot be validated by either greedy 57-byte or 81-byte stepping. `ServerShell::OnClientEnterWorld` therefore returns `LTNULL`, and the engine client remains `state=2 player=0`.

The same failure family occurs on multiple retail character models (ATC, Soldier, Paxton, Rowdy), showing this is a systematic packed-v33 layout issue, not a corrupt Player asset.

## Root issue in M29BP

M29BP chose each shape stride greedily. This is insufficient because a local candidate can look plausible while placing the parser at an impossible later shape. The old public reverse-engineering reader also names the first byte `ShapeIndex`, but retail Player shape 0 contains value `2`; M29BQ therefore treats this byte as an opaque shape tag rather than requiring a sequential record index.

The public v33 template documents a 57-byte base PhysicsShape and an optional 24-byte capsule extension. M29BQ keeps those documented record sizes, but removes the per-record quaternion/greedy decision.

## M29BQ / 0.14 fix

`JexFindPhysicsShapeLayouts` solves the entire PhysicsShape sequence globally:

- explores both legal record sizes (57 and 81 bytes) for every shape;
- validates each candidate's `nodeIndex` against the model node count;
- does not require the first byte to equal the loop index;
- accepts a final shape position only if the following constraint block parses structurally and lands on a plausible PhysicsWeightSet count;
- rejects zero-solution and multi-solution layouts rather than guessing;
- logs a bounded shape frontier on Player when no complete layout exists.

M29BQ also includes `unk13` in the aggregate packed constraint count. The public v33 binary template has seven constraint-class count fields after `unk12`; M29BP had summed only six.

Expected Player diagnostics on success:

- `[model00p-player] physics-layout solved ...`
- one `[model00p-player] physics-shape=... extra=0|24 ...` line per shape
- `[model00p-player] shapes-ok ...`
- then constraint / physics-weight / LOD / mesh stages
- ultimately `[model00p-player] runtime-model-ready ...` if the whole model completes.

If no valid layout is found, M29BQ emits `[model00p-layout] depth=...` frontier diagnostics plus `stage=physics-shape-layout solutions=0`, which should identify the first structural disagreement without a crash.

## Buildability repair retained

The M29BP source snapshot omitted the already hardware-used local server-message export even though the client handoff code referenced it. M29BQ restores `FearVita_ServerDispatchClientMessage` and direct local-client delivery in `runtime/server/src/serverde_impl.cpp` to keep the source archive self-contained/buildable. This is a source-snapshot repair, not a new gameplay bypass.

## Build validation

Full Vita build succeeded with GCC 15.2.0 / VitaSDK 2026.08.1:

- C++ compile: PASS
- link: PASS
- VELF: PASS
- SELF / `eboot.bin`: PASS
- SFO: PASS (`APP_VER 00.14`, `TITLE_ID FEAR00001`)
- VPK: PASS

The final test VPK was repacked from the hardware-proven M29BP 35-entry / 22-file application payload, replacing only `eboot.bin` and `sce_sys/param.sfo`.

## SHA-256

- final VPK: `e3279e113f7539f41e5417cc34f714e2b3af23b78a34ca776278d474d65e3da5`
- buildable source ZIP: `3b8920d8fa823e6b4a35e12cc2ce47e72539e965a1faed92db407693f34221c1`
- focused patch: `5e9c3f786b6f2d355a7b16419fa54c3e7c9e269a95a1c70c61b3bf9bf9fb24b3`
- fresh `eboot.bin`: `05810baf2e96612375736bc69cd423874cab8a7f0cd47e77f4210dd3760b7394`

## Hardware status

M29BQ is build-validated but **not yet hardware-validated**. Do not claim Player creation or Intro entry until a Vita log shows the full model reaching runtime readiness and `player=1` / normal in-world transition.
