from pathlib import Path

p = Path('src/platform/vita_bootstrap.hpp')
s = p.read_text(encoding='utf-8')

old_sig = 'static void loader_draw_progress(unsigned long done, unsigned long total)\n{\n'
new_sig = '''static void loader_draw_progress(unsigned long done, unsigned long total, const char *status)\n{\n    if (status && *status)\n        g_loader_status = status;\n'''
if old_sig not in s:
    raise SystemExit('v6 compilefix: loader_draw_progress signature not found')
s = s.replace(old_sig, new_sig, 1)

# Keep the exact supplied artwork as the loader background. The v6 progress
# renderer draws only its bottom panel/bar on top of it.
old_bg = '''    if (!g_loader_background_drawn) {\n        loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF090505u);\n        g_loader_background_drawn = true;\n    }\n'''
new_bg = '''    if (!g_loader_background_drawn) {\n        if (!loader_load_background()) {\n            loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF090505u);\n            g_loader_background_drawn = true;\n        }\n    }\n'''
if old_bg not in s:
    raise SystemExit('v6 compilefix: loader background block not found')
s = s.replace(old_bg, new_bg, 1)

# The older v5 helper implementations remain in the generated bootstrap for
# compatibility/documentation. v6 has its own compact bottom bar renderer.
# Mark the two superseded draw helpers as intentionally unused under -Werror.
s = s.replace('static void loader_draw_text_centered(',
              'static void __attribute__((unused)) loader_draw_text_centered(', 1)
s = s.replace('static void loader_draw_blood_bar(',
              'static void __attribute__((unused)) loader_draw_blood_bar(', 1)

# Remove v6's temporary status setter calls; the existing v5 call sites already
# pass the correct per-phase status text as the third argument.
s = s.replace('v6_set_loader_status("ARCHIV WIRD GEOEFFNET");\n    loader_draw_progress(0, 100);\n    ', '')
s = s.replace('v6_set_loader_status("SPIELDATEN WERDEN INSTALLIERT");\n    ', '')

# This helper is no longer needed once status comes from the call site.
status_setter = '''static void v6_set_loader_status(const char *status)\n{\n    if (status && *status) g_loader_status = status;\n}\n\n'''
s = s.replace(status_setter, '')

p.write_text(s, encoding='utf-8')
print('v6 loader compile compatibility fix applied')
