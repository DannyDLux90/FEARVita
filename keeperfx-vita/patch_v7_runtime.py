from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v7 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# 1) Root black-screen fix: Vita cannot use the desktop modes as 0x0 logical
# draw surfaces. Mode 28 is DESKTOP and was creating a zero-sized PAL8 buffer,
# while vitaGL itself was alive at 960x544. Keep a 640x480 logical game surface
# and let RendererVita upscale it to the native Vita display.
p = Path('src/bflib_video.c')
s = p.read_text(encoding='utf-8')
old = '''static void LbRegisterModernVideoModes(void)\n{\n    LbRegisterVideoMode("DESKTOP",      0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_BORDERLESS|Lb_VF_DESKTOP); // borderless fullscreen window mode\n    LbRegisterVideoMode("DESKTOP_FULL", 0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_DESKTOP); // normal fullscreen mode (at desktop resolution)\n    //LbRegisterVideoMode("WINDOW",       0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_WINDOWED); // normal bordered window at any resolution, remebers previous set size (defaults to 640x480?)\n    LbRegisterVideoMode("BORDERLESS",   0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_BORDERLESS|Lb_VF_WINDOWED); // borderless window at desktop resolution\n    LbRegisterVideoMode("ALL",          0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_FILLALL); // span all displays with a borderless window\n}\n'''
new = '''static void LbRegisterModernVideoModes(void)\n{\n#ifdef PLATFORM_VITA\n    // Vita has no desktop/window geometry. A 0x0 modern mode produced a 0x0\n    // lbDrawSurface (mode 28 / DESKTOP), so the GPU displayed only its clear\n    // framebuffer. Keep KeeperFX's logical PAL8 surface at 640x480; RendererVita\n    // scales that surface to the native 960x544 display.\n    const TbScreenCoord vita_w = 640;\n    const TbScreenCoord vita_h = 480;\n    LbRegisterVideoMode("DESKTOP",      vita_w, vita_h, 32, Lb_VF_RGBCOLOR|Lb_VF_BORDERLESS|Lb_VF_DESKTOP);\n    LbRegisterVideoMode("DESKTOP_FULL", vita_w, vita_h, 32, Lb_VF_RGBCOLOR|Lb_VF_DESKTOP);\n    LbRegisterVideoMode("BORDERLESS",   vita_w, vita_h, 32, Lb_VF_RGBCOLOR|Lb_VF_BORDERLESS|Lb_VF_WINDOWED);\n    LbRegisterVideoMode("ALL",          vita_w, vita_h, 32, Lb_VF_RGBCOLOR|Lb_VF_FILLALL);\n#else\n    LbRegisterVideoMode("DESKTOP",      0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_BORDERLESS|Lb_VF_DESKTOP); // borderless fullscreen window mode\n    LbRegisterVideoMode("DESKTOP_FULL", 0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_DESKTOP); // normal fullscreen mode (at desktop resolution)\n    //LbRegisterVideoMode("WINDOW",       0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_WINDOWED);\n    LbRegisterVideoMode("BORDERLESS",   0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_BORDERLESS|Lb_VF_WINDOWED);\n    LbRegisterVideoMode("ALL",          0, 0, 32, Lb_VF_RGBCOLOR|Lb_VF_FILLALL);\n#endif\n}\n'''
s = replace_once(s, old, new, 'Vita modern video mode dimensions')
p.write_text(s, encoding='utf-8')

# 2) Startup FMV mode restoration: v6 tried to rebuild mode 28 after the movie.
# Once mode 28 is a real 640x480 logical mode that would work, but it is not
# necessary for nstate=-2 and caused extra renderer churn. Keep the active mode,
# restore the frontend palette, then let the common clear/present code run.
p = Path('src/front_fmvids.c')
s = p.read_text(encoding='utf-8')
old = '''#ifdef PLATFORM_VITA\n    // Startup movies use nstate=-2 on desktop to keep the movie mode alive.\n    // On Vita this leaves the palette renderer in a stale movie state and the\n    // next frontend frame can remain black. Restore the frontend mode explicitly.\n    SYNCLOG("[Vita FMV] restoring frontend mode after startup movie");\n    if (!setup_screen_mode_minimal(get_frontend_vidmode()))\n    {\n      ERRORLOG("[Vita FMV] failed to restore frontend video mode");\n      FatalError = 1;\n      exit_keeper = 1;\n      return 0;\n    }\n    RendererClearScreen(0);\n    RendererPresentFrame();\n#else\n    memset(frontend_palette, 0, PALETTE_SIZE);\n#endif\n'''
new = '''#ifdef PLATFORM_VITA\n    SYNCLOG("[Vita FMV] startup movie ended; keeping active logical mode %d", (int)RendererActiveMode());\n    memset(frontend_palette, 0, PALETTE_SIZE);\n#else\n    memset(frontend_palette, 0, PALETTE_SIZE);\n#endif\n'''
s = replace_once(s, old, new, 'remove failing post-FMV mode reset')
p.write_text(s, encoding='utf-8')

# 3) Give KeeperFX access to Vita's extended memory mode and use a larger but
# deliberately non-maximal newlib heap so vitaGL/CDRAM still have headroom.
p = Path('build/cmake/modules/PlatformVita.cmake')
s = p.read_text(encoding='utf-8')
s = s.replace('ScePower_stub SceAudio_stub SceShaccCg_stub SceKernelDmacMgr_stub SceAppUtil_stub)',
              'ScePower_stub SceAudio_stub SceShaccCg_stub SceKernelDmacMgr_stub SceAppUtil_stub SceAppMgr_stub)', 1)
old = 'vita_create_self(keeperfx.self keeperfx UNSAFE)\nvita_create_vpk(keeperfx.vpk KFXV00001 keeperfx.self\n'
new = '''# ATTRIBUTE2=12 enables the Vita extended-memory application mode used by\n# memory-heavy homebrew. The heap itself is capped in PlatformVita.cpp so GPU\n# and physically-contiguous allocations retain headroom.\nset(VITA_MKSFOEX_FLAGS "${VITA_MKSFOEX_FLAGS} -d ATTRIBUTE2=12")\nvita_create_self(keeperfx.self keeperfx UNSAFE)\nvita_create_vpk(keeperfx.vpk KFXV00001 keeperfx.self\n'''
s = replace_once(s, old, new, 'ATTRIBUTE2=12')
p.write_text(s, encoding='utf-8')

p = Path('src/platform/PlatformVita.cpp')
s = p.read_text(encoding='utf-8')
if '#include <psp2/appmgr.h>' not in s:
    s = s.replace('#include <psp2/audioout.h>', '#include <psp2/audioout.h>') if '#include <psp2/audioout.h>' in s else s
    s = s.replace('#include <psp2/power.h>\n', '#include <psp2/power.h>\n#include <psp2/appmgr.h>\n', 1)
s = s.replace('int _newlib_heap_size_user  = 192 * 1024 * 1024; // 192 MB heap — ~245 MB total, within 256 MB',
              'int _newlib_heap_size_user  = 256 * 1024 * 1024; // v7: extended-memory mode, retain headroom for vitaGL/CDRAM', 1)
marker = '    _SYSI_LOG("log-setup");\n'
addition = '''    _SYSI_LOG("log-setup");\n    {\n        SceAppMgrBudgetInfo mem;\n        memset(&mem, 0, sizeof(mem));\n        mem.size = sizeof(mem);\n        const int mem_rc = sceAppMgrGetBudgetInfo(&mem);\n        if (mem_rc >= 0) {\n            SYNCLOG("[Vita RAM] mode=%d extra_allowed=%d USER_RW=%u/%u MiB free EXTRA=%u/%u MiB free PHYCONT=%u/%u MiB free CDRAM=%u/%u MiB free",\n                    mem.app_mode, (int)mem.extra_mem_allowed,\n                    mem.free_user_rw / (1024u*1024u), mem.total_user_rw_mem / (1024u*1024u),\n                    mem.free_extra_mem / (1024u*1024u), mem.total_extra_mem / (1024u*1024u),\n                    mem.free_phycont_mem / (1024u*1024u), mem.total_phycont_mem / (1024u*1024u),\n                    mem.free_cdram_mem / (1024u*1024u), mem.total_cdram_mem / (1024u*1024u));\n        } else {\n            WARNLOG("[Vita RAM] sceAppMgrGetBudgetInfo failed: 0x%08X", (unsigned int)mem_rc);\n        }\n    }\n'''
s = replace_once(s, marker, addition, 'Vita RAM budget log')
p.write_text(s, encoding='utf-8')

# 4) Loader: use the exact reference artwork as the base image in the final VPK.
# Only repaint the interior of its ornate blood bar, so the outer frame/drips and
# static gold status line remain exactly those from the supplied reference. Fix
# A8B8G8R8 byte order (v6 red constants appeared blue on hardware).
p = Path('src/platform/vita_bootstrap.hpp')
s = p.read_text(encoding='utf-8')
start = s.find('static void loader_draw_progress(unsigned long done, unsigned long total)')
end = s.find('static bool loader_init()', start)
if start < 0 or end < 0:
    raise SystemExit('v7 patch: loader_draw_progress block not found')
block = r'''static void loader_draw_progress(unsigned long done, unsigned long total)
{
    if (!g_loader_pixels) return;
    if (total == 0) total = 1;
    if (done > total) done = total;

    const unsigned int pct = (unsigned int)(((unsigned long long)100 * done) / total);
    // Coordinates match the ornate bar in the supplied 1640x920 reference after
    // resizing to the Vita's 960x544 framebuffer. The reference image provides
    // the complete outer blood frame and drips; we only repaint its interior.
    const int inner_x = 253;
    const int inner_y = 465;
    const int inner_w = 451;
    const int inner_h = 25;
    const int filled = (int)(((unsigned long long)inner_w * done) / total);

    if (!g_loader_background_drawn) {
        // Fallback only. Normally loader_load_background() has already copied the
        // user's exact reference artwork into the framebuffer.
        loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF050509u);
        g_loader_background_drawn = true;
    }

    // SCE_DISPLAY_PIXELFORMAT_A8B8G8R8 on little-endian ARM is 0xAABBGGRR.
    // These constants are therefore intentionally ABGR (v6's RGB constants
    // rendered as black/blue on real hardware).
    const uint32_t bar_dark   = 0xFF050812u; // near-black brown/red
    const uint32_t blood_deep = 0xFF0808A8u;
    const uint32_t blood_mid  = 0xFF0A10D8u;
    const uint32_t blood_hot  = 0xFF2248FFu;
    const uint32_t gold       = 0xFF86CCF0u;

    // Erase the baked 37% sample fill and percentage inside the reference bar.
    loader_fill_rect(inner_x, inner_y, inner_w, inner_h, bar_dark);
    if (filled > 0) {
        loader_fill_rect(inner_x, inner_y, filled, inner_h, blood_deep);
        if (inner_h > 6)
            loader_fill_rect(inner_x, inner_y + 3, filled, inner_h - 7, blood_mid);
        if (filled > 3)
            loader_fill_rect(inner_x + 2, inner_y + 3, filled - 2, 3, blood_hot);
    }

    char pct_text[16];
    snprintf(pct_text, sizeof(pct_text), "%u %%", pct);
    const int pct_scale = 2;
    int pct_x = (kLoaderWidth - v6_text_width(pct_text, pct_scale)) / 2;
    v6_draw_text(pct_x, inner_y + 6, pct_text, gold, pct_scale);

    sceKernelPowerTick(SCE_KERNEL_POWER_TICK_DEFAULT);
}

'''
s = s[:start] + block + s[end:]
p.write_text(s, encoding='utf-8')

print('v7 runtime patch applied')
