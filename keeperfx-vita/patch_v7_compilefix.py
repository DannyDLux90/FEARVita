from pathlib import Path

p = Path('src/platform/vita_bootstrap.hpp')
s = p.read_text(encoding='utf-8')

# v7 intentionally uses the user's exact reference artwork as the loader base.
# Make sure it is actually loaded instead of falling back to a solid colour.
old = '''    if (!g_loader_background_drawn) {\n        // Fallback only. Normally loader_load_background() has already copied the\n        // user's exact reference artwork into the framebuffer.\n        loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF050509u);\n        g_loader_background_drawn = true;\n    }\n'''
new = '''    if (!g_loader_background_drawn) {\n        if (!loader_load_background()) {\n            loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF050509u);\n            g_loader_background_drawn = true;\n        }\n    }\n'''
if old not in s:
    raise SystemExit('v7 compilefix: reference-background block not found')
s = s.replace(old, new, 1)

# The v6 compatibility layer leaves a status pointer in the generated header.
# v7 uses the exact status lettering baked into the reference artwork, so retain
# the ABI but explicitly mark the legacy status storage as intentionally unused.
s = s.replace('static const char *g_loader_status =',
              'static const char * __attribute__((unused)) g_loader_status =', 1)

p.write_text(s, encoding='utf-8')
print('v7 compile compatibility fix applied')
