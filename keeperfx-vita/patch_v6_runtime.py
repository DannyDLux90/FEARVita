from pathlib import Path
import re


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v6 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# 1) RendererVita: implement deterministic FMV staging into the PAL8 framebuffer.
h = Path('src/renderer/RendererVita.h')
s = h.read_text(encoding='utf-8')
if 'SubmitVideoFrame(' not in s:
    marker = '    void UnlockFramebuffer() override;\n'
    addition = marker + '''\n    // Vita FMV path: stage decoded PAL8 frames directly into the renderer's\n    // CPU framebuffer. EndFrame() then performs the normal palette-shader upload.\n    bool SubmitVideoFrame(\n        const uint8_t* pal8_pixels, int src_w, int src_h, int src_pitch,\n        const uint8_t* bgra_palette_1024,\n        int dst_x, int dst_y, int dst_w, int dst_h) override;\n'''
    s = replace_once(s, marker, addition, 'RendererVita.h UnlockFramebuffer')
    h.write_text(s, encoding='utf-8')

cpp = Path('src/renderer/RendererVita.cpp')
s = cpp.read_text(encoding='utf-8')
if 'RendererVita::SubmitVideoFrame' not in s:
    marker = '\n#endif // PLATFORM_VITA\n'
    impl = r'''

bool RendererVita::SubmitVideoFrame(
    const uint8_t* pal8_pixels, int src_w, int src_h, int src_pitch,
    const uint8_t* bgra_palette_1024,
    int dst_x, int dst_y, int dst_w, int dst_h)
{
    if (!m_initialized || !pal8_pixels || !bgra_palette_1024 ||
        src_w <= 0 || src_h <= 0 || src_pitch < src_w || dst_w <= 0 || dst_h <= 0 ||
        !lbDrawSurface || !lbDrawSurface->pixels) {
        return false;
    }

    // The caller already holds RendererLockScreen(), so lbDrawSurface is locked.
    // Write exactly into that surface rather than relying on the generic FMV copy
    // helpers, which left the Vita renderer with a black movie despite decoded frames.
    const int fb_w = lbDrawSurface->w;
    const int fb_h = lbDrawSurface->h;
    const int fb_pitch = lbDrawSurface->pitch;
    uint8_t* fb = static_cast<uint8_t*>(lbDrawSurface->pixels);

    // Clear letterbox/pillarbox area every frame.
    memset(fb, 0, static_cast<size_t>(fb_pitch) * static_cast<size_t>(fb_h));

    int x0 = dst_x < 0 ? 0 : dst_x;
    int y0 = dst_y < 0 ? 0 : dst_y;
    int x1 = dst_x + dst_w;
    int y1 = dst_y + dst_h;
    if (x1 > fb_w) x1 = fb_w;
    if (y1 > fb_h) y1 = fb_h;

    if (x0 < x1 && y0 < y1) {
        for (int y = y0; y < y1; ++y) {
            const int rel_y = y - dst_y;
            int sy = (rel_y * src_h) / dst_h;
            if (sy < 0) sy = 0;
            if (sy >= src_h) sy = src_h - 1;
            const uint8_t* src_row = pal8_pixels + sy * src_pitch;
            uint8_t* dst_row = fb + y * fb_pitch;
            for (int x = x0; x < x1; ++x) {
                const int rel_x = x - dst_x;
                int sx = (rel_x * src_w) / dst_w;
                if (sx < 0) sx = 0;
                if (sx >= src_w) sx = src_w - 1;
                dst_row[x] = src_row[sx];
            }
        }
    }

    // FFmpeg supplies BGRA palette entries. RendererVita expects RGB in 6-bit
    // lbPalette[] form and expands them again in EndFrame().
    for (int i = 0; i < 256; ++i) {
        lbPalette[i * 3 + 0] = bgra_palette_1024[i * 4 + 2] >> 2;
        lbPalette[i * 3 + 1] = bgra_palette_1024[i * 4 + 1] >> 2;
        lbPalette[i * 3 + 2] = bgra_palette_1024[i * 4 + 0] >> 2;
    }
    return true;
}
'''
    s = replace_once(s, marker, impl + marker, 'RendererVita.cpp endif')
    cpp.write_text(s, encoding='utf-8')

# 2) FMV: direct hardware START edge detection, independent of SDL/key translation.
fmv = Path('src/bflib_fmvids.cpp')
s = fmv.read_text(encoding='utf-8')
if '#include <psp2/ctrl.h>' not in s:
    marker = '#ifdef PLATFORM_VITA\n'
    s = replace_once(s, marker, '#ifdef PLATFORM_VITA\n#include <psp2/ctrl.h>\n', 'fmv PLATFORM_VITA include')

if 'vita_fmv_start_pressed' not in s:
    marker = 'static int vita_avio_read(void *opaque, uint8_t *buf, int buf_size)\n'
    helper = r'''static bool vita_fmv_start_pressed()
{
    static bool was_down = false;
    SceCtrlData pad;
    memset(&pad, 0, sizeof(pad));
    const int got = sceCtrlPeekBufferPositive(0, &pad, 1);
    const bool is_down = got > 0 && (pad.buttons & SCE_CTRL_START) != 0;
    const bool pressed = is_down && !was_down;
    was_down = is_down;
    return pressed;
}

'''
    s = replace_once(s, marker, helper + marker, 'fmv vita_avio_read')

if '[Vita FMV] START pressed' not in s:
    old = '''\t\t\twait_for_pts();\n\t\t\toutput_video_frame();\n\t\t\tif (!poll_inputs()) {'''
    new = '''\t\t\twait_for_pts();\n\t\t\toutput_video_frame();\n#ifdef PLATFORM_VITA\n\t\t\tif (vita_fmv_start_pressed()) {\n\t\t\t\tSYNCLOG("[Vita FMV] START pressed - skipping movie");\n\t\t\t\treturn false;\n\t\t\t}\n#endif\n\t\t\tif (!poll_inputs()) {'''
    s = replace_once(s, old, new, 'fmv output_video_frames')
fmv.write_text(s, encoding='utf-8')

# 3) Restore a normal frontend video mode after -2 startup movies on Vita.
front = Path('src/front_fmvids.c')
s = front.read_text(encoding='utf-8')
if '[Vita FMV] restoring frontend mode after startup movie' not in s:
    old = '''  } else\n  {\n    memset(frontend_palette, 0, PALETTE_SIZE);\n  }\n  RendererClearScreen(0);'''
    new = '''  } else\n  {\n#ifdef PLATFORM_VITA\n    // Startup movies use nstate=-2 on desktop to keep the movie mode alive.\n    // On Vita this leaves the palette renderer in a stale movie state and the\n    // next frontend frame can remain black. Restore the frontend mode explicitly.\n    SYNCLOG("[Vita FMV] restoring frontend mode after startup movie");\n    if (!setup_screen_mode_minimal(get_frontend_vidmode()))\n    {\n      ERRORLOG("[Vita FMV] failed to restore frontend video mode");\n      FatalError = 1;\n      exit_keeper = 1;\n      return 0;\n    }\n    RendererClearScreen(0);\n    RendererPresentFrame();\n#else\n    memset(frontend_palette, 0, PALETTE_SIZE);\n#endif\n  }\n  RendererClearScreen(0);'''
    s = replace_once(s, old, new, 'front_fmvids nstate -2 restore')
front.write_text(s, encoding='utf-8')

# 4) Add narrow startup breadcrumbs around the post-intro section.
main = Path('src/main.cpp')
s = main.read_text(encoding='utf-8')
if '[Vita startup] display_loading_screen begin' not in s:
    old = '''  if (result == 1)\n  {\n      display_loading_screen();\n  }\n  LbDataFreeAll(legal_load_files);\n\n  if (result == 1)\n  {\n      if ( !initial_setup() )\n        result = 0;\n  }'''
    new = '''  if (result == 1)\n  {\n#ifdef PLATFORM_VITA\n      SYNCLOG("[Vita startup] display_loading_screen begin");\n#endif\n      display_loading_screen();\n#ifdef PLATFORM_VITA\n      SYNCLOG("[Vita startup] display_loading_screen end");\n#endif\n  }\n  LbDataFreeAll(legal_load_files);\n#ifdef PLATFORM_VITA\n  SYNCLOG("[Vita startup] legal resources freed");\n#endif\n\n  if (result == 1)\n  {\n#ifdef PLATFORM_VITA\n      SYNCLOG("[Vita startup] initial_setup begin");\n#endif\n      if ( !initial_setup() )\n        result = 0;\n#ifdef PLATFORM_VITA\n      SYNCLOG("[Vita startup] initial_setup end result=%d", (int)result);\n#endif\n  }'''
    s = replace_once(s, old, new, 'main post intro markers')
main.write_text(s, encoding='utf-8')

# 5) Loader v6: blood-style compact bar at bottom with status + percent text.
boot = Path('src/platform/vita_bootstrap.hpp')
s = boot.read_text(encoding='utf-8')
start = s.find('static void loader_draw_progress(')
end = s.find('static bool loader_init()', start)
if start < 0 or end < 0:
    raise SystemExit('v6 patch: loader_draw_progress block not found')
if 'v6_draw_text' not in s:
    block = r'''static const char *g_loader_status = "SPIELDATEN WERDEN VORBEREITET";

static uint8_t v6_glyph_row(char ch, int row)
{
    static const char chars[] = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%.-/:";
    static const uint8_t rows[][7] = {
      {0,0,0,0,0,0,0},
      {14,17,17,31,17,17,17},{30,17,17,30,17,17,30},{14,17,16,16,16,17,14},
      {30,17,17,17,17,17,30},{31,16,16,30,16,16,31},{31,16,16,30,16,16,16},
      {14,17,16,23,17,17,15},{17,17,17,31,17,17,17},{14,4,4,4,4,4,14},
      {7,2,2,2,18,18,12},{17,18,20,24,20,18,17},{16,16,16,16,16,16,31},
      {17,27,21,21,17,17,17},{17,25,21,19,17,17,17},{14,17,17,17,17,17,14},
      {30,17,17,30,16,16,16},{14,17,17,17,21,18,13},{30,17,17,30,20,18,17},
      {15,16,16,14,1,1,30},{31,4,4,4,4,4,4},{17,17,17,17,17,17,14},
      {17,17,17,17,17,10,4},{17,17,17,21,21,21,10},{17,17,10,4,10,17,17},
      {17,17,10,4,4,4,4},{31,1,2,4,8,16,31},
      {14,17,19,21,25,17,14},{4,12,4,4,4,4,14},{14,17,1,2,4,8,31},
      {30,1,1,14,1,1,30},{2,6,10,18,31,2,2},{31,16,30,1,1,17,14},
      {6,8,16,30,17,17,14},{31,1,2,4,8,8,8},{14,17,17,14,17,17,14},
      {14,17,17,15,1,2,12},
      {17,18,4,8,19,17,0},{0,0,0,0,0,12,12},{0,0,0,31,0,0,0},{0,0,0,0,0,0,4},
      {1,2,4,8,16,0,0},{0,4,0,0,4,0,0}
    };
    for (unsigned int i = 0; i < sizeof(chars)-1; ++i)
        if (chars[i] == ch) return rows[i][row];
    return 0;
}

static void v6_draw_text(int x, int y, const char *text, uint32_t color, int scale)
{
    if (!text || scale < 1) return;
    for (const char *p = text; *p; ++p) {
        char ch = *p;
        if (ch >= 'a' && ch <= 'z') ch = (char)(ch - 'a' + 'A');
        for (int row = 0; row < 7; ++row) {
            uint8_t bits = v6_glyph_row(ch, row);
            for (int col = 0; col < 5; ++col) {
                if (bits & (1u << (4-col)))
                    loader_fill_rect(x + col*scale, y + row*scale, scale, scale, color);
            }
        }
        x += 6 * scale;
    }
}

static int v6_text_width(const char *text, int scale)
{
    return text ? (int)strlen(text) * 6 * scale : 0;
}

static void v6_set_loader_status(const char *status)
{
    if (status && *status) g_loader_status = status;
}

static void loader_draw_progress(unsigned long done, unsigned long total)
{
    if (!g_loader_pixels) return;
    if (total == 0) total = 1;
    if (done > total) done = total;

    const int bar_x = 205;
    const int bar_y = 462;
    const int bar_w = 550;
    const int bar_h = 30;
    const int frame = 3;
    const int inner_x = bar_x + frame;
    const int inner_y = bar_y + frame;
    const int inner_w = bar_w - frame*2;
    const int inner_h = bar_h - frame*2;
    const int filled = (int)(((unsigned long long)inner_w * done) / total);
    const unsigned int pct = (unsigned int)(((unsigned long long)100 * done) / total);

    if (!g_loader_background_drawn) {
        loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF090505u);
        g_loader_background_drawn = true;
    }

    loader_fill_rect(150, 420, 660, 88, 0xD0100707u);
    const uint32_t gold = 0xFFE4C685u;
    const int status_scale = 2;
    int status_x = (kLoaderWidth - v6_text_width(g_loader_status, status_scale)) / 2;
    if (status_x < 10) status_x = 10;
    v6_draw_text(status_x, 431, g_loader_status, gold, status_scale);

    loader_fill_rect(bar_x-3, bar_y-3, bar_w+6, bar_h+6, 0xFF250000u);
    loader_fill_rect(bar_x, bar_y, bar_w, bar_h, 0xFF8A0808u);
    loader_fill_rect(inner_x, inner_y, inner_w, inner_h, 0xFF160606u);

    if (filled > 0) {
        loader_fill_rect(inner_x, inner_y, filled, inner_h, 0xFF8E0000u);
        if (inner_h > 8) loader_fill_rect(inner_x, inner_y+3, filled, inner_h/3, 0xFFD51414u);
        if (inner_h > 14) loader_fill_rect(inner_x, inner_y+inner_h-5, filled, 3, 0xFF510000u);
        const int drip_base = inner_x + filled;
        for (int d = 0; d < 5; ++d) {
            int dx = drip_base - 18 - d*41;
            if (dx > inner_x && dx < inner_x + filled)
                loader_fill_rect(dx, bar_y + bar_h, 3, 4 + (d%3)*3, 0xFF6D0000u);
        }
    }

    char pct_text[16];
    snprintf(pct_text, sizeof(pct_text), "%u%%", pct);
    const int pct_scale = 2;
    const int pct_x = bar_x + (bar_w - v6_text_width(pct_text, pct_scale)) / 2;
    v6_draw_text(pct_x, bar_y + 8, pct_text, 0xFFFFE2A6u, pct_scale);

    sceKernelPowerTick(SCE_KERNEL_POWER_TICK_DEFAULT);
}

'''
    s = s[:start] + block + s[end:]

s = s.replace('log_line("opening bundled data archive");', 'v6_set_loader_status("ARCHIV WIRD GEOEFFNET");\n    loader_draw_progress(0, 100);\n    log_line("opening bundled data archive");')
s = s.replace('log_line("copy buffer allocated");', 'v6_set_loader_status("SPIELDATEN WERDEN INSTALLIERT");\n    log_line("copy buffer allocated");')
s = s.replace('.keeperfx_vita_data_v3', '.keeperfx_vita_data_v6')
s = s.replace('.keeperfx_vita_data_v5', '.keeperfx_vita_data_v6')
boot.write_text(s, encoding='utf-8')

print('v6 runtime patch applied')
