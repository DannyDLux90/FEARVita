from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v8c patch: pattern not found: {name}')
    return text.replace(old, new, 1)

p = Path('src/platform/vita_bootstrap.hpp')
s = p.read_text(encoding='utf-8')

# Track whether the temporary pre-SDL framebuffer is actually registered with
# sceDisplay so shutdown can safely detach it before freeing CDRAM.
s = replace_once(
    s,
    'static bool g_loader_background_drawn = false;\n',
    'static bool g_loader_background_drawn = false;\nstatic bool g_loader_display_active = false;\n',
    'loader display-active state')

# Add a real shutdown path. The official VitaSDK debug-screen sample detaches
# the framebuffer with sceDisplaySetFrameBuf(NULL, IMMEDIATE) before freeing the
# display memory. Keep the loader strictly pre-SDL/pre-vitaGL and release all of
# its CDRAM before the renderer starts.
needle = 'static bool loader_init()\n{\n'
shutdown = '''static void loader_shutdown()\n{\n    const bool had_loader = (g_loader_pixels != NULL) || (g_loader_memblock >= 0) || g_loader_display_active;\n\n    if (g_loader_display_active) {\n        int rc = sceDisplaySetFrameBuf(NULL, SCE_DISPLAY_SETBUF_IMMEDIATE);\n        if (rc < 0)\n            log_printf("loader framebuffer detach failed: 0x%08X", (unsigned int)rc);\n        g_loader_display_active = false;\n    }\n\n    g_loader_pixels = NULL;\n    g_loader_background_drawn = false;\n\n    if (g_loader_memblock >= 0) {\n        int rc = sceKernelFreeMemBlock(g_loader_memblock);\n        if (rc < 0)\n            log_printf("loader framebuffer free failed: 0x%08X", (unsigned int)rc);\n        g_loader_memblock = -1;\n    }\n\n    if (had_loader)\n        log_line("loader framebuffer released before SDL/vitaGL");\n}\n\nstatic bool loader_init()\n{\n'''
s = replace_once(s, needle, shutdown, 'loader_shutdown insertion')

# The display-failure branch previously leaked the newly allocated CDRAM block.
old = '''    int display_rc = sceDisplaySetFrameBuf(&frame, SCE_DISPLAY_SETBUF_NEXTFRAME);\n    if (display_rc < 0) {\n        log_printf("loader sceDisplaySetFrameBuf failed: 0x%08X", (unsigned int)display_rc);\n        return false;\n    }\n\n    loader_draw_progress(0, 1'''
new = '''    int display_rc = sceDisplaySetFrameBuf(&frame, SCE_DISPLAY_SETBUF_NEXTFRAME);\n    if (display_rc < 0) {\n        log_printf("loader sceDisplaySetFrameBuf failed: 0x%08X", (unsigned int)display_rc);\n        loader_shutdown();\n        return false;\n    }\n    g_loader_display_active = true;\n\n    loader_draw_progress(0, 1'''
s = replace_once(s, old, new, 'display failure cleanup and active state')

# Ensure every exit from install_bundled_data releases the temporary loader.
start = s.find('static bool install_bundled_data()')
end = s.find('static int run_kfxmain', start)
if start < 0 or end < 0:
    raise SystemExit('v8c patch: install_bundled_data block not found')
block = s[start:end]
block = block.replace('return false;', 'loader_shutdown();\n        return false;')
block = block.replace('return true;', 'loader_shutdown();\n        return true;')
# Keep the marker contents consistent with its v8 filename for diagnostics.
block = block.replace('KeeperFX Vita data v3\\n', 'KeeperFX Vita data v8\\n')
s = s[:start] + block + s[end:]

p.write_text(s, encoding='utf-8')
print('v8c loader CDRAM/display cleanup patch applied')
