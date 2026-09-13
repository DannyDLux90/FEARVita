from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v9 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# 1) Vita native input: one poll per frame, KeeperFX logical 640x480 space.
# ---------------------------------------------------------------------------
p = Path('src/input/input_vita.c')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    '#define VITA_SCREEN_WIDTH  960\n#define VITA_SCREEN_HEIGHT 544\n',
    '#define VITA_SCREEN_WIDTH  640\n#define VITA_SCREEN_HEIGHT 480\n',
    'Vita logical pointer dimensions')
# A released tap is a pulse. Two frames give the frontend one extra chance to
# consume it without making held physical buttons sticky.
s = s.replace('s_leftClickPulse = 1;', 's_leftClickPulse = 2;')
s = s.replace('s_rightClickPulse = 1;', 's_rightClickPulse = 2;')
p.write_text(s, encoding='utf-8')

p = Path('src/platform/WindowSystemVita.cpp')
s = p.read_text(encoding='utf-8')
old = '''void WindowSystemVita::PollInput()\n{\n    int new_x = 0;\n'''
new = '''void WindowSystemVita::PollInput()\n{\n    // Poll SCE controller/touch exactly once, before translating that state to\n    // KeeperFX mouse events. update_mouse() only consumes the resulting state.\n    if (g_input != NULL && g_input->poll_events != NULL)\n        g_input->poll_events();\n\n    int new_x = 0;\n'''
s = replace_once(s, old, new, 'single Vita input poll in WindowSystem')
# The Vita pointer is in KeeperFX's fixed logical 640x480 surface, so compare it
# to the logical display mouse coordinates rather than any SDL/window object.
s = s.replace('lbMouse.MMouseX', 'lbDisplay.MMouseX')
s = s.replace('lbMouse.MMouseY', 'lbDisplay.MMouseY')
p.write_text(s, encoding='utf-8')

p = Path('src/kjm_input.c')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    '    g_input->poll_events();   // read sceCtrl / touch (peek, safe alongside SDL)\n',
    '    // SCE state was already polled by WindowSystemVita::PollInput().\n',
    'remove duplicate late Vita poll')
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 2) Disable vitaGL's on-screen debugger and compile a tiny startup HUD helper.
# ---------------------------------------------------------------------------
p = Path('build/cmake/modules/PlatformVita.cmake')
s = p.read_text(encoding='utf-8')
if s.count('HAVE_DEBUGGER=1') < 2:
    raise SystemExit('v9 patch: expected vitaGL debugger flags not found')
s = s.replace('HAVE_DEBUGGER=1', 'HAVE_DEBUGGER=0')
old = '    target_sources(${_target} PRIVATE "${CMAKE_SOURCE_DIR}/src/platform/stack_monitor.c")\n'
new = '''    target_sources(${_target} PRIVATE\n        "${CMAKE_SOURCE_DIR}/src/platform/stack_monitor.c"\n        "${CMAKE_SOURCE_DIR}/src/platform/vita_startup_progress.cpp")\n'''
s = replace_once(s, old, new, 'Vita startup progress source registration')
p.write_text(s, encoding='utf-8')

progress_cpp = r'''/******************************************************************************/
// KeeperFX PS Vita startup progress overlay.
// Draws only a tiny percent/bar patch over the already-visible CD loading art.
/******************************************************************************/
#ifdef PLATFORM_VITA

#include "kfx_memory.h"
#include "pre_inc.h"
#include "renderer/RendererManager.h"
#include "post_inc.h"
#include <stdint.h>
#include <string.h>

static unsigned int s_last_progress = 101;

static uint8_t glyph3x5(char ch, int row)
{
    // 3-bit rows, top to bottom. Enough for "100%".
    static const uint8_t digits[10][5] = {
        {7,5,5,5,7}, {2,6,2,2,7}, {7,1,7,4,7}, {7,1,7,1,7}, {5,5,7,1,1},
        {7,4,7,1,7}, {7,4,7,5,7}, {7,1,1,1,1}, {7,5,7,5,7}, {7,5,7,1,7}
    };
    static const uint8_t percent[5] = {5,1,2,4,5};
    if (ch >= '0' && ch <= '9') return digits[ch - '0'][row];
    if (ch == '%') return percent[row];
    return 0;
}

static void draw_char(uint8_t *fb, int pitch, int x, int y, char ch, uint8_t colour)
{
    for (int row = 0; row < 5; ++row) {
        uint8_t bits = glyph3x5(ch, row);
        for (int col = 0; col < 3; ++col) {
            if (bits & (1u << (2-col)))
                fb[(y + row) * pitch + x + col] = colour;
        }
    }
}

extern "C" void vita_startup_progress(unsigned int pct)
{
    if (pct > 100) pct = 100;
    if (pct == s_last_progress) return;

    int pitch = 0;
    uint8_t *fb = RendererLockFramebuffer(&pitch);
    if (!fb || pitch <= 0) return;

    const int w = (int)RendererScreenWidth();
    const int h = (int)RendererScreenHeight();
    if (w < 80 || h < 40) {
        RendererUnlockFramebuffer();
        return;
    }

    // Resolve dark/bright palette indices dynamically so the indicator stays
    // legible on KeeperFX loading palettes without replacing the loading art.
    unsigned char pal[256 * 3];
    uint8_t dark = 0, bright = 255;
    if (RendererPaletteGet(pal) == Lb_SUCCESS) {
        int min_l = 100000, max_l = -1;
        for (int i = 0; i < 256; ++i) {
            const int l = (int)pal[i*3] + (int)pal[i*3+1] + (int)pal[i*3+2];
            if (l < min_l) { min_l = l; dark = (uint8_t)i; }
            if (l > max_l) { max_l = l; bright = (uint8_t)i; }
        }
    }

    const int box_w = 46;
    const int box_h = 13;
    const int x0 = w - box_w - 8;
    const int y0 = h - box_h - 7;
    for (int y = y0; y < y0 + box_h; ++y)
        memset(fb + y * pitch + x0, dark, (size_t)box_w);

    char text[5];
    if (pct >= 100) {
        text[0] = '1'; text[1] = '0'; text[2] = '0'; text[3] = '%'; text[4] = 0;
    } else if (pct >= 10) {
        text[0] = (char)('0' + pct / 10); text[1] = (char)('0' + pct % 10);
        text[2] = '%'; text[3] = 0;
    } else {
        text[0] = (char)('0' + pct); text[1] = '%'; text[2] = 0;
    }
    const int len = (int)strlen(text);
    const int text_w = len * 4 - 1;
    int tx = x0 + (box_w - text_w) / 2;
    const int ty = y0 + 2;
    for (int i = 0; i < len; ++i)
        draw_char(fb, pitch, tx + i * 4, ty, text[i], bright);

    const int bar_x = x0 + 5;
    const int bar_y = y0 + 9;
    const int bar_w = box_w - 10;
    const int fill = (int)((bar_w * pct) / 100u);
    memset(fb + bar_y * pitch + bar_x, dark, (size_t)bar_w);
    if (fill > 0)
        memset(fb + bar_y * pitch + bar_x, bright, (size_t)fill);

    RendererUnlockFramebuffer();
    s_last_progress = pct;
    RendererPresentFrame();
}

#endif // PLATFORM_VITA
'''
Path('src/platform/vita_startup_progress.cpp').write_text(progress_cpp, encoding='utf-8')

# ---------------------------------------------------------------------------
# 3) First-run loader: load reference artwork ONCE, then only repaint bar area.
#    v7's success path forgot to set g_loader_background_drawn, causing the
#    baked 37% sample in the artwork to be copied back before every update.
# ---------------------------------------------------------------------------
p = Path('src/platform/vita_bootstrap.hpp')
s = p.read_text(encoding='utf-8')
old = '''    if (!g_loader_background_drawn) {\n        if (!loader_load_background()) {\n            loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF050509u);\n            g_loader_background_drawn = true;\n        }\n    }\n'''
new = '''    if (!g_loader_background_drawn) {\n        if (!loader_load_background())\n            loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF050509u);\n        // loader_load_background() does not own this state flag. Mark the\n        // reference as consumed even on success so the baked 37% sample is\n        // never recopied between live progress repaints.\n        g_loader_background_drawn = true;\n    }\n'''
s = replace_once(s, old, new, 'loader reference loaded once')
s = s.replace('.keeperfx_vita_data_v8', '.keeperfx_vita_data_v9')
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 4) Small staged startup percentage on the existing CD loading screen.
# ---------------------------------------------------------------------------
p = Path('src/main.cpp')
s = p.read_text(encoding='utf-8')
anchor = '''#ifdef PLATFORM_VITA\nTbBool vita_deeper_direct = false;\n#endif\n'''
replacement = '''#ifdef PLATFORM_VITA\nTbBool vita_deeper_direct = false;\nextern "C" void vita_startup_progress(unsigned int pct);\n#endif\n'''
s = replace_once(s, anchor, replacement, 'startup progress declaration')

s = replace_once(
    s,
    '''      display_loading_screen();\n#ifdef PLATFORM_VITA\n      SYNCLOG("[Vita startup] display_loading_screen end");\n#endif\n''',
    '''      display_loading_screen();\n#ifdef PLATFORM_VITA\n      vita_startup_progress(5);\n      SYNCLOG("[Vita startup] display_loading_screen end");\n#endif\n''',
    'startup progress after loading screen')

s = replace_once(
    s,
    '''      SYNCLOG("[Vita startup] initial_setup end result=%d", (int)result);\n#endif\n''',
    '''      vita_startup_progress(14);\n      SYNCLOG("[Vita startup] initial_setup end result=%d", (int)result);\n#endif\n''',
    'startup progress after initial setup')

s = replace_once(
    s,
    '''    SYNCLOG("[Vita v8] settings/gui strings end result=%d", (int)result);\n#endif\n''',
    '''    vita_startup_progress(20);\n    SYNCLOG("[Vita v8] settings/gui strings end result=%d", (int)result);\n#endif\n''',
    'startup progress after settings')

s = replace_once(
    s,
    '''void init_keeper(void)\n{\n    SYNCDBG(8,"Starting");\n''',
    '''void init_keeper(void)\n{\n    SYNCDBG(8,"Starting");\n#ifdef PLATFORM_VITA\n    vita_startup_progress(24);\n#endif\n''',
    'startup progress init_keeper start')

s = replace_once(
    s,
    '''    init_custom_sprites(SPRITE_LAST_LEVEL);\n    RendererNotifyCustomSpritesReloaded();\n''',
    '''    init_custom_sprites(SPRITE_LAST_LEVEL);\n#ifdef PLATFORM_VITA\n    vita_startup_progress(88);\n#endif\n    RendererNotifyCustomSpritesReloaded();\n''',
    'startup progress after custom sprites')

s = replace_once(
    s,
    '''      SYNCLOG("[Vita v8] init_keeper/setup end");\n#endif\n''',
    '''      vita_startup_progress(100);\n      SYNCLOG("[Vita v8] init_keeper/setup end");\n#endif\n''',
    'startup progress complete')
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 5) Make the dominant sprite-cache read/write phase update that percentage.
# ---------------------------------------------------------------------------
p = Path('src/custom_sprites_cache.c')
s = p.read_text(encoding='utf-8')
inc_anchor = '#include "post_inc.h"\n'
s = replace_once(
    s, inc_anchor,
    inc_anchor + '\nextern void vita_startup_progress(unsigned int pct);\n',
    'sprite cache progress declaration')

old = '''    /* keepersprite_add pixel blobs */\n    for (int i = base_kspr; i < end_kspr; i++) {\n        int w  = ctx->creature_table_add[i].SWidth;\n'''
new = '''    /* keepersprite_add pixel blobs */\n    for (int i = base_kspr; i < end_kspr; i++) {\n        if (cnt_kspr >= 64 && (((i - base_kspr) & 63) == 0)) {\n            const unsigned int local = (unsigned int)(i - base_kspr);\n            vita_startup_progress(32u + (local * 52u) / (unsigned int)cnt_kspr);\n        }\n        int w  = ctx->creature_table_add[i].SWidth;\n'''
s = replace_once(s, old, new, 'sprite cache write progress')

old = '''    /* keepersprite_add pixel blobs */\n    for (uint32_t i = h_base_kspr; i < h_base_kspr + h_cnt_kspr; i++) {\n        int w  = ctx->creature_table_add[i].SWidth;\n'''
new = '''    /* keepersprite_add pixel blobs */\n    for (uint32_t i = h_base_kspr; i < h_base_kspr + h_cnt_kspr; i++) {\n        if (h_cnt_kspr >= 64 && (((i - h_base_kspr) & 63u) == 0)) {\n            const uint32_t local = i - h_base_kspr;\n            vita_startup_progress(32u + (local * 52u) / h_cnt_kspr);\n        }\n        int w  = ctx->creature_table_add[i].SWidth;\n'''
s = replace_once(s, old, new, 'sprite cache read progress')
p.write_text(s, encoding='utf-8')

print('v9 UX/input/progress patch applied')
