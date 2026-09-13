from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v8 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

p = Path('src/renderer/RendererVita.h')
s = p.read_text(encoding='utf-8')
old = '''    BackendCapabilities GetCapabilities() const override {\n        BackendCapabilities c = {};\n        c.hasGPURenderPath        = 1;\n        c.wantsFullscreenViewport = 1;\n        c.hasGPUSprites           = 1;\n        c.supportsGPUPasses       = 1;\n        return c;\n    }\n'''
new = '''    BackendCapabilities GetCapabilities() const override {\n        BackendCapabilities c = {};\n        // v8: Vita is a CPU 8-bit KeeperFX rasteriser with GPU palette/upscale presentation.\n        // It is not the full OpenGL world/UI path. Reporting a full GPU render path keeps\n        // lbDisplay.WScreen NULL and makes the software world/UI renderers draw nothing.\n        c.hasGPURenderPath        = 0;\n        c.wantsFullscreenViewport = 0;\n        c.hasGPUSprites           = 0;\n        c.supportsGPUPasses       = 1;\n        return c;\n    }\n'''
s = replace_once(s, old, new, 'RendererVita capabilities')
old = '''    bool BeginFrame() override;\n    void EndFrame() override;\n\n    uint8_t* LockFramebuffer(int* out_pitch) override;\n'''
new = '''    bool BeginFrame() override;\n    void EndFrame() override;\n    void ClearScreen(uint8_t colour_index) override;\n\n    uint8_t* LockFramebuffer(int* out_pitch) override;\n'''
s = replace_once(s, old, new, 'RendererVita ClearScreen declaration')
p.write_text(s, encoding='utf-8')

p = Path('src/renderer/RendererVita.cpp')
s = p.read_text(encoding='utf-8')
old = '''uint8_t* RendererVita::LockFramebuffer(int* out_pitch)\n{\n    if (SDL_LockSurface(lbDrawSurface) < 0) return nullptr;\n    if (out_pitch) *out_pitch = lbDrawSurface->pitch;\n    return static_cast<uint8_t*>(lbDrawSurface->pixels);\n}\n\nvoid RendererVita::UnlockFramebuffer()\n{\n    SDL_UnlockSurface(lbDrawSurface);\n}\n'''
new = '''void RendererVita::ClearScreen(uint8_t colour_index)\n{\n    if (lbDrawSurface)\n        SDL_FillRect(lbDrawSurface, nullptr, colour_index);\n}\n\nuint8_t* RendererVita::LockFramebuffer(int* out_pitch)\n{\n    if (!lbDrawSurface || !lbDrawSurface->pixels)\n        return nullptr;\n    if (SDL_LockSurface(lbDrawSurface) < 0)\n        return nullptr;\n    if (out_pitch) *out_pitch = lbDrawSurface->pitch;\n    return static_cast<uint8_t*>(lbDrawSurface->pixels);\n}\n\nvoid RendererVita::UnlockFramebuffer()\n{\n    if (lbDrawSurface)\n        SDL_UnlockSurface(lbDrawSurface);\n}\n'''
s = replace_once(s, old, new, 'RendererVita framebuffer hardening')
old = '''void RendererVita::EndFrame()\n{\n    if (!m_initialized) return;\n\n    {\n        const int w = lbDrawSurface->w;\n        const int h = lbDrawSurface->h;\n\n        SDL_LockSurface(lbDrawSurface);\n'''
new = '''void RendererVita::EndFrame()\n{\n    if (!m_initialized || !lbDrawSurface || !lbDrawSurface->pixels) return;\n\n    {\n        const int w = lbDrawSurface->w;\n        const int h = lbDrawSurface->h;\n\n        if (SDL_LockSurface(lbDrawSurface) < 0) {\n            ERRORLOG("RendererVita::EndFrame: SDL_LockSurface failed: %s", SDL_GetError());\n            return;\n        }\n'''
s = replace_once(s, old, new, 'RendererVita EndFrame guard')
p.write_text(s, encoding='utf-8')

p = Path('src/renderer/RendererManager.cpp')
s = p.read_text(encoding='utf-8')
old = '''#if defined(PLATFORM_VITA)\n    if (type == RENDERER_VITA)\n        RenderPass_Initialize(1); // BACKEND_GPU_VITA\n#elif defined(RENDERER_OPENGL_ENABLED)\n'''
new = '''#if defined(PLATFORM_VITA)\n    if (type == RENDERER_VITA) {\n        g_render_pass_active = 0;\n        SYNCLOG("Vita v8: GPU sprite intercept disabled; CPU WScreen rasteriser + vitaGL present");\n    }\n#elif defined(RENDERER_OPENGL_ENABLED)\n'''
s = replace_once(s, old, new, 'disable Vita RenderPass sprite intercept')
p.write_text(s, encoding='utf-8')

p = Path('src/main.cpp')
s = p.read_text(encoding='utf-8')
old = '''  if (result == 1)\n  {\n    load_settings();\n    if ( !setup_gui_strings_data() )\n      result = 0;\n    VITA_TICK("setup_gui_strings_data");\n  }\n'''
new = '''  if (result == 1)\n  {\n#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita v8] settings/gui strings begin");\n#endif\n    load_settings();\n    if ( !setup_gui_strings_data() )\n      result = 0;\n#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita v8] settings/gui strings end result=%d", (int)result);\n#endif\n    VITA_TICK("setup_gui_strings_data");\n  }\n'''
s = replace_once(s, old, new, 'settings/gui breadcrumb')
old = '''  if (result == 1)\n  {\n      init_keeper();\n      set_gamma(settings.gamma_correction, 0);\n'''
new = '''  if (result == 1)\n  {\n#ifdef PLATFORM_VITA\n      SYNCLOG("[Vita v8] init_keeper/setup begin");\n#endif\n      init_keeper();\n      set_gamma(settings.gamma_correction, 0);\n'''
s = replace_once(s, old, new, 'init_keeper begin breadcrumb')
old = '''      RendererNotifyGameTablesReady();\n      init_lookups();\n      VITA_TICK("init_keeper + setup");\n  }\n\n  return result;\n'''
new = '''      RendererNotifyGameTablesReady();\n      init_lookups();\n#ifdef PLATFORM_VITA\n      SYNCLOG("[Vita v8] init_keeper/setup end");\n#endif\n      VITA_TICK("init_keeper + setup");\n  }\n\n#ifdef PLATFORM_VITA\n  SYNCLOG("[Vita v8] setup_game returning result=%d", (int)result);\n#endif\n  return result;\n'''
s = replace_once(s, old, new, 'setup_game return breadcrumb')
old = '''    if ( !setup_screen_mode_minimal(get_frontend_vidmode()) )\n    {\n      FatalError = 1;\n      exit_keeper = 1;\n      return true;\n    }\n    RendererClearScreen(0);\n    RendererPresentFrame();\n    if (frontend_load_data() != Lb_SUCCESS)\n'''
new = '''#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita v8] entering frontend; requested mode=%d", (int)get_frontend_vidmode());\n#endif\n    if ( !setup_screen_mode_minimal(get_frontend_vidmode()) )\n    {\n      FatalError = 1;\n      exit_keeper = 1;\n      return true;\n    }\n#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita v8] frontend mode active=%d size=%dx%d", (int)RendererActiveMode(), (int)RendererScreenWidth(), (int)RendererScreenHeight());\n#endif\n    RendererClearScreen(0);\n    RendererPresentFrame();\n#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita v8] frontend_load_data begin");\n#endif\n    if (frontend_load_data() != Lb_SUCCESS)\n'''
s = replace_once(s, old, new, 'frontend mode/load breadcrumbs')
old = '''    memset(scratch, 0, PALETTE_SIZE);\n    RendererPaletteSet(scratch);\n#ifdef PLATFORM_VITA\n    if (vita_deeper_direct)\n'''
new = '''#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita v8] frontend_load_data end");\n#endif\n    memset(scratch, 0, PALETTE_SIZE);\n    RendererPaletteSet(scratch);\n#ifdef PLATFORM_VITA\n    if (vita_deeper_direct)\n'''
s = replace_once(s, old, new, 'frontend load end breadcrumb')
old = '''    try_restore_frontend_error_box();\n\n    poll_inputs();\n'''
new = '''#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita v8] frontend state selected; entering menu loop");\n#endif\n    try_restore_frontend_error_box();\n\n    poll_inputs();\n'''
s = replace_once(s, old, new, 'frontend state breadcrumb')
p.write_text(s, encoding='utf-8')

p = Path('src/platform/vita_bootstrap.hpp')
s = p.read_text(encoding='utf-8')
s = s.replace('.keeperfx_vita_data_v7', '.keeperfx_vita_data_v8')
p.write_text(s, encoding='utf-8')

print('v8 preflight/correctness patch applied')
