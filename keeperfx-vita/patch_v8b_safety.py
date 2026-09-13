from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v8b patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# Vita has one fixed presentation target. Do not let desktop/window config modes
# leak into legal screen, FMV or frontend transitions. Keep every CPU-rendered
# KeeperFX stage on the known 640x480x8 logical surface and let RendererVita
# perform the 960x544 presentation scaling.
p = Path('src/vidmode.c')
s = p.read_text(encoding='utf-8')
old = '''TbScreenMode try_failsafe_vidmode(void)\n{\n  // Check the failsafe mode\n  if (!LbScreenIsModeAvailable(failsafe_vidmode, display_id))\n  {\n      ERRORLOG("Failsafe video mode (mode %d) is invalid.",(int)failsafe_vidmode);\n      return Lb_SCREEN_MODE_INVALID;\n  }\n  return failsafe_vidmode;\n}\n'''
new = '''TbScreenMode try_failsafe_vidmode(void)\n{\n#ifdef PLATFORM_VITA\n  return Lb_SCREEN_MODE_640_480_8;\n#else\n  // Check the failsafe mode\n  if (!LbScreenIsModeAvailable(failsafe_vidmode, display_id))\n  {\n      ERRORLOG("Failsafe video mode (mode %d) is invalid.",(int)failsafe_vidmode);\n      return Lb_SCREEN_MODE_INVALID;\n  }\n  return failsafe_vidmode;\n#endif\n}\n'''
s = replace_once(s, old, new, 'try_failsafe fixed Vita mode')
old = '''TbScreenMode get_failsafe_vidmode(void)\n{\n  return failsafe_vidmode;\n}\n'''
new = '''TbScreenMode get_failsafe_vidmode(void)\n{\n#ifdef PLATFORM_VITA\n  return Lb_SCREEN_MODE_640_480_8;\n#else\n  return failsafe_vidmode;\n#endif\n}\n'''
s = replace_once(s, old, new, 'get_failsafe fixed Vita mode')
old = '''TbScreenMode get_movies_vidmode(void)\n{\n  return movies_vidmode;\n}\n'''
new = '''TbScreenMode get_movies_vidmode(void)\n{\n#ifdef PLATFORM_VITA\n  return Lb_SCREEN_MODE_640_480_8;\n#else\n  return movies_vidmode;\n#endif\n}\n'''
s = replace_once(s, old, new, 'get_movies fixed Vita mode')
old = '''TbScreenMode get_frontend_vidmode(void)\n{\n  return frontend_vidmode;\n}\n'''
new = '''TbScreenMode get_frontend_vidmode(void)\n{\n#ifdef PLATFORM_VITA\n  return Lb_SCREEN_MODE_640_480_8;\n#else\n  return frontend_vidmode;\n#endif\n}\n'''
s = replace_once(s, old, new, 'get_frontend fixed Vita mode')
p.write_text(s, encoding='utf-8')

# The first-run loader writes directly to the displayed CDRAM framebuffer.
# Synchronise each coarse (every 16 ZIP entries) progress repaint to VBlank to
# prevent the visible partial updates/blinking seen on hardware. This adds only
# a few seconds worst-case to the one-time verification pass, not one VBlank per file.
p = Path('src/platform/vita_bootstrap.hpp')
s = p.read_text(encoding='utf-8')
needle = '''static void loader_draw_progress(unsigned long done, unsigned long total, const char *status)\n{\n    if (!g_loader_pixels) return;\n'''
replacement = '''static void loader_draw_progress(unsigned long done, unsigned long total, const char *status)\n{\n    if (!g_loader_pixels) return;\n    sceDisplayWaitVblankStart();\n'''
s = replace_once(s, needle, replacement, 'loader VBlank synchronisation')
p.write_text(s, encoding='utf-8')

print('v8b fixed-mode/loader-synchronisation patch applied')
