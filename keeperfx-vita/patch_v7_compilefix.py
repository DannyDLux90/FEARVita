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

# v7 uses the status lettering baked into the supplied reference image. Remove
# the legacy v6 status storage entirely so -Werror cannot flag it as unused.
s = s.replace('static const char *g_loader_status = "SPIELDATEN WERDEN VORBEREITET";\n\n', '', 1)
s = s.replace('static const char * __attribute__((unused)) g_loader_status = "SPIELDATEN WERDEN VORBEREITET";\n\n', '', 1)

# Force one v7 validation pass so the user can actually see the corrected loader.
# Existing files with matching sizes are skipped, so this is mainly verification.
for old_marker in ('.keeperfx_vita_data_v3', '.keeperfx_vita_data_v5', '.keeperfx_vita_data_v6'):
    s = s.replace(old_marker, '.keeperfx_vita_data_v7')

p.write_text(s, encoding='utf-8')
print('v7 compile compatibility fix applied')
