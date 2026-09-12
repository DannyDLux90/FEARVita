# FEARVita current state

**Last hardware-verified package:** 0.08 / M29BK  
**Current source checkpoint:** M29BL WIP / package marker 0.09  
**Date:** 2026-09-12

M29BK is the first hardware-tested FEARVita build that completes the real F.E.A.R. Intro world load without crashing. Base F.E.A.R., Extraction Point, and Perseus Mandate all reach 100% loading progress, complete the Jupiter EX v113 world, pass the bounded NavMesh layout preflight, complete `DoRunWorld`, return `do-start-world ok`, and report `preload FinishStartGame result=1`. The retail loop then continues for many thousands of frames, but the loading screen does not transition into gameplay.

The current blocker is therefore no longer World00p parsing, object creation, or NavMesh. It is the authentic local client/server handoff after the server world has successfully started. The Vita monolith needs a genuine local LithTech server `Client`, real client-data propagation, client->server message dispatch, safe server->client control-message delivery, a real server-side player, and the stock client `OnEnterWorld()` transition. Do not fake `GS_PLAYING` or fabricate a successful intro state.

M29BL WIP begins this local-client/player handoff work. The source tree carries package marker 00.09 and modifies the Vita ILTClient bridge, menu/runtime frame gate, runtime-server bridge/platform glue, and LithTech server client/message paths. The WIP adds local server-client preparation with client data, direct local client->server message dispatch, filtered server->client control-message delivery, detection of the real in-world server client/player, creation of a client-local player proxy, and a stock `CGameClientShell::OnEnterWorld()` notification only after a genuine server player exists.

M29BL WIP has **not** yet been rebuilt or hardware-tested. The binaries present in the exported workspace remain the last verified M29BK / 0.08 build. A rebuild attempt stopped during CMake toolchain setup because the temporary VitaSDK path from the previous runtime was no longer present; this is not evidence of a source compile error.

The separate F.E.A.R. `Model00p` compatibility frontier remains. The runtime now reaches the genuine Jupiter EX `MODL!` container and reports that it is not a legacy LTB model. This did not prevent M29BK from completing the server world load, but a dedicated Model00p loader is still required for full rendering/gameplay.

Audio is also still not considered matched to PC. The current backend uses synchronous 48 kHz stereo output, separate SFX/music/voice gains, and 44.1->48 kHz polyphase resampling. Use the exported debug WAVs for future digital comparison rather than phone-recording-only tuning.

For continuation, use branch **`m29bl-wip-local-client-handoff`**. Read `M29BL_NEW_CHAT_HANDOFF_2026-09-12.md` and `recovery/M29BL_WIP_RECOVERY.md`. The two recovery patch files preserve the exact M29BK -> M29BL-WIP source delta without committing VPKs, retail data, proprietary assets, or local build artifacts.
