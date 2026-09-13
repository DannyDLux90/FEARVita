from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v8d patch: pattern not found: {name}')
    return text.replace(old, new, 1)

p = Path('src/renderer/RendererManager.cpp')
s = p.read_text(encoding='utf-8')

# The Vita v8 renderer deliberately uses the CPU WScreen/UI path. Runtime-loaded
# sprite sheets therefore need registrations in SoftwareUIRenderer too, not only
# in the OpenGL atlas. Move the helper declaration before the first notification.
anchor = '''void RendererNotifySpritesReloaded()\n{\n'''
s = replace_once(s, anchor,
    '''static void register_sheet_software(const struct TbSpriteSheet* sheet); // fwd\n\nvoid RendererNotifySpritesReloaded()\n{\n''',
    'early register_sheet_software declaration')
# Remove the old later forward declaration to keep the file tidy.
s = s.replace('\nstatic void register_sheet_software(const struct TbSpriteSheet* sheet); // fwd\n\n/** Append map_flag',
              '\n/** Append map_flag', 1)

# Main in-game GUI sheets are loaded/reloaded by LoadVRes256Data/LoadMcgaData.
old = '''#endif\n}\n\nvoid RendererDrainDeferredAtlasRebuild()\n'''
new = '''#endif\n    register_sheet_software(gui_panel_sprites);\n    register_sheet_software(button_sprites);\n}\n\nvoid RendererDrainDeferredAtlasRebuild()\n'''
s = replace_once(s, old, new, 'register main GUI sheets for software UI')

# Pointer sprites are loaded after renderer initialisation on Vita.
old = '''#endif\n}\n\n/** Append frontend_sprite into the live atlas after frontend_load_data(). */\nvoid RendererNotifyFrontendSpritesLoaded()\n'''
new = '''#endif\n    register_sheet_software(pointer_sprites);\n}\n\n/** Append frontend_sprite into the live atlas after frontend_load_data(). */\nvoid RendererNotifyFrontendSpritesLoaded()\n'''
s = replace_once(s, old, new, 'register pointer sprites for software UI')

# Frontend sprites contain the actual main-menu widgets; without this registration
# SoftwareUIRenderer resolves every raw frontend sprite to kInvalidSpriteHandle.
old = '''#endif\n}\n\n/** Append map_flag into the live atlas after load_spritesheet() in front_landview.c.\n'''
new = '''#endif\n    register_sheet_software(frontend_sprite);\n}\n\n/** Append map_flag into the live atlas after load_spritesheet() in front_landview.c.\n'''
s = replace_once(s, old, new, 'register frontend sprites for software UI')

# Custom sprites are reloaded per campaign/level and are used by the in-game UI.
old = '''#endif\n}\n\n/*******************************************************************************/\n\n/** Resolve a TbSprite pointer'''
new = '''#endif\n    register_sheet_software(custom_sprites);\n}\n\n/*******************************************************************************/\n\n/** Resolve a TbSprite pointer'''
s = replace_once(s, old, new, 'register custom sprites for software UI')

p.write_text(s, encoding='utf-8')
print('v8d software UI sprite registration patch applied')
