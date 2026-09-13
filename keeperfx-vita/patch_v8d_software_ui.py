from pathlib import Path

p = Path('src/renderer/RendererManager.cpp')
s = p.read_text(encoding='utf-8')


def insert_before_function_close(text, function_name, code):
    """Insert code immediately before the matching closing brace of a C++ function."""
    marker = f'void {function_name}()'
    start = text.find(marker)
    if start < 0:
        raise SystemExit(f'v8d patch: function not found: {function_name}')
    brace = text.find('{', start)
    if brace < 0:
        raise SystemExit(f'v8d patch: opening brace not found: {function_name}')
    depth = 0
    close = -1
    for i in range(brace, len(text)):
        ch = text[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                close = i
                break
    if close < 0:
        raise SystemExit(f'v8d patch: closing brace not found: {function_name}')
    if code.strip() in text[brace:close]:
        return text
    return text[:close] + code + text[close:]


# Vita v8 deliberately uses the CPU WScreen/UI path. Runtime-loaded sprite sheets
# therefore need entries in SoftwareUIRenderer's handle table, not only the GL
# atlas. Make the helper visible before the first notification callback.
fwd = 'static void register_sheet_software(const struct TbSpriteSheet* sheet); // fwd\n\n'
first_notify = 'void RendererNotifySpritesReloaded()\n'
if fwd not in s[:s.find(first_notify)]:
    pos = s.find(first_notify)
    if pos < 0:
        raise SystemExit('v8d patch: RendererNotifySpritesReloaded not found')
    s = s[:pos] + fwd + s[pos:]

# Remove the old later declaration (the early one stays).
old_late = '\nstatic void register_sheet_software(const struct TbSpriteSheet* sheet); // fwd\n\n/** Append map_flag'
if old_late in s:
    s = s.replace(old_late, '\n/** Append map_flag', 1)

# Main GUI sheets are rebuilt on video/resource reloads.
s = insert_before_function_close(
    s, 'RendererNotifySpritesReloaded',
    '    register_sheet_software(gui_panel_sprites);\n'
    '    register_sheet_software(button_sprites);\n')

# These sheets are loaded later during normal startup/campaign changes.
s = insert_before_function_close(
    s, 'RendererNotifyPointerSpritesLoaded',
    '    register_sheet_software(pointer_sprites);\n')
s = insert_before_function_close(
    s, 'RendererNotifyFrontendSpritesLoaded',
    '    register_sheet_software(frontend_sprite);\n')
s = insert_before_function_close(
    s, 'RendererNotifyCustomSpritesReloaded',
    '    register_sheet_software(custom_sprites);\n')

p.write_text(s, encoding='utf-8')
print('v8d software UI sprite registration patch applied')
