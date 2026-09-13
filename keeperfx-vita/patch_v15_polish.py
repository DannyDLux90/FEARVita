from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v15 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# 1) Restore local quit semantics which networking-off stubbed out.
p = Path('src/bflib_network_stub.c')
s = p.read_text(encoding='utf-8')
if '#include "keeperfx.hpp"\n' not in s:
    s = s.replace('#include "player_data.h"\n', '#include "player_data.h"\n#include "keeperfx.hpp"\n', 1)
old = 'void  process_quit_packet(struct PlayerInfo *player, short complete_quit) { (void)player; (void)complete_quit; }'
if old not in s:
    old = 'void process_quit_packet(struct PlayerInfo *player, short complete_quit) { (void)player; (void)complete_quit; }'
new = '''void process_quit_packet(struct PlayerInfo *player, short complete_quit)\n{\n    if (player == NULL)\n        return;\n    struct PlayerInfo *myplyr = get_my_player();\n    player->allocflags &= ~PlaF_Allocated;\n    if (player == myplyr)\n    {\n        quit_game = 1;\n        if (complete_quit)\n            exit_keeper = 1;\n    }\n    SYNCMSG("[V15 quit] local quit player=%d complete=%d quit=%d exit=%d",\n            (int)player->id_number, (int)complete_quit, (int)quit_game, (int)exit_keeper);\n}'''
s = replace_once(s, old, new, 'networking-off process_quit_packet')
p.write_text(s, encoding='utf-8')

# 2) Follow Vita system language before async speech loading starts.
p = Path('src/main.cpp')
s = p.read_text(encoding='utf-8')
s = replace_once(s,
'''#ifdef PLATFORM_VITA\n#include <psp2/kernel/processmgr.h>\n#include <psp2/kernel/clib.h>\n#endif\n''',
'''#ifdef PLATFORM_VITA\n#include <psp2/kernel/processmgr.h>\n#include <psp2/kernel/clib.h>\n#include <psp2/apputil.h>\n#include <psp2/system_param.h>\n#endif\n''', 'Vita language includes')
anchor = 'unsigned char exit_keeper;\nunsigned char quit_game;\n'
helper = r'''
#ifdef PLATFORM_VITA
static enum TbLanguage vita_keeperfx_language_from_system(int lang)
{
    switch (lang)
    {
    case SCE_SYSTEM_PARAM_LANG_JAPANESE:      return Lang_Japanese;
    case SCE_SYSTEM_PARAM_LANG_FRENCH:        return Lang_French;
    case SCE_SYSTEM_PARAM_LANG_SPANISH:       return Lang_Spanish;
    case SCE_SYSTEM_PARAM_LANG_GERMAN:        return Lang_German;
    case SCE_SYSTEM_PARAM_LANG_ITALIAN:       return Lang_Italian;
    case SCE_SYSTEM_PARAM_LANG_DUTCH:         return Lang_Dutch;
    case SCE_SYSTEM_PARAM_LANG_PORTUGUESE_PT:
    case SCE_SYSTEM_PARAM_LANG_PORTUGUESE_BR: return Lang_Portuguese;
    case SCE_SYSTEM_PARAM_LANG_RUSSIAN:       return Lang_Russian;
    case SCE_SYSTEM_PARAM_LANG_KOREAN:        return Lang_Korean;
    case SCE_SYSTEM_PARAM_LANG_CHINESE_T:     return Lang_ChineseTra;
    case SCE_SYSTEM_PARAM_LANG_CHINESE_S:     return Lang_ChineseInt;
    case SCE_SYSTEM_PARAM_LANG_SWEDISH:       return Lang_Swedish;
    case SCE_SYSTEM_PARAM_LANG_DANISH:        return Lang_Danish;
    case SCE_SYSTEM_PARAM_LANG_NORWEGIAN:     return Lang_Norwegian;
    case SCE_SYSTEM_PARAM_LANG_POLISH:        return Lang_Polish;
    case SCE_SYSTEM_PARAM_LANG_ENGLISH_US:
    case SCE_SYSTEM_PARAM_LANG_ENGLISH_GB:
    case SCE_SYSTEM_PARAM_LANG_FINNISH:
    case SCE_SYSTEM_PARAM_LANG_TURKISH:
    default:                                  return Lang_English;
    }
}

static void vita_apply_system_language(void)
{
    int vita_lang = SCE_SYSTEM_PARAM_LANG_ENGLISH_US;
    int rc = sceAppUtilSystemParamGetInt(SCE_SYSTEM_PARAM_ID_LANG, &vita_lang);
    if (rc < 0)
    {
        WARNLOG("[V15 language] sceAppUtilSystemParamGetInt failed: 0x%08X; using English", rc);
        vita_lang = SCE_SYSTEM_PARAM_LANG_ENGLISH_US;
    }
    install_info.lang_id = vita_keeperfx_language_from_system(vita_lang);
    SYNCMSG("[V15 language] Vita=%d KeeperFX=%d (%s)", vita_lang,
            (int)install_info.lang_id, get_language_lwrstr(install_info.lang_id));
}
#endif
'''
if anchor not in s:
    raise SystemExit('v15 patch: quit globals anchor missing')
s = s.replace(anchor, anchor + helper, 1)
s = replace_once(s,
'''  VITA_TICK("load_configuration");\n\n  // Kick off sound bank I/O on a background thread so it overlaps with\n''',
'''  VITA_TICK("load_configuration");\n#ifdef PLATFORM_VITA\n  vita_apply_system_language();\n#endif\n\n  // Kick off sound bank I/O on a background thread so it overlaps with\n''', 'apply Vita language before audio')
p.write_text(s, encoding='utf-8')

# 3) Persist a Vita-only rear-touch setting, default OFF.
p = Path('src/config_settings.h')
s = p.read_text(encoding='utf-8')
s = replace_once(s,
'''    int isometric_tilt;\n    TbBool highlight_mode;\n    };\n''',
'''    int isometric_tilt;\n    TbBool highlight_mode;\n#ifdef PLATFORM_VITA\n    TbBool vita_rear_touch_enabled;\n#endif\n    };\n''', 'GameSettings rear touch')
p.write_text(s, encoding='utf-8')

p = Path('src/config_settings.c')
s = p.read_text(encoding='utf-8')
s = replace_once(s, '    settings.highlight_mode                = false;\n',
'''    settings.highlight_mode                = false;\n#ifdef PLATFORM_VITA\n    settings.vita_rear_touch_enabled        = false;\n#endif\n''', 'rear default')
s = replace_once(s,
'''        val = value_dict_get(vsec, "first_person_move_sensitivity");\n        if (val && value_type(val) == VALUE_INT32) settings.first_person_move_sensitivity = (unsigned char)value_int32(val);\n    }\n''',
'''        val = value_dict_get(vsec, "first_person_move_sensitivity");\n        if (val && value_type(val) == VALUE_INT32) settings.first_person_move_sensitivity = (unsigned char)value_int32(val);\n#ifdef PLATFORM_VITA\n        val = value_dict_get(vsec, "vita_rear_touch_enabled");\n        if (val) settings.vita_rear_touch_enabled = (TbBool)value_coerce_bool(val);\n#endif\n    }\n''', 'rear load')
s = replace_once(s, '    settings.highlight_mode = clamp(settings.highlight_mode, false, true);\n',
'''    settings.highlight_mode = clamp(settings.highlight_mode, false, true);\n#ifdef PLATFORM_VITA\n    settings.vita_rear_touch_enabled = clamp(settings.vita_rear_touch_enabled, false, true);\n#endif\n''', 'rear clamp')
s = replace_once(s,
'''    TOSAVE("first_person_move_invert = %d\\n", (int)settings.first_person_move_invert);\n    TOSAVE("first_person_move_sensitivity = %d\\n", (int)settings.first_person_move_sensitivity);\n''',
'''    TOSAVE("first_person_move_invert = %d\\n", (int)settings.first_person_move_invert);\n    TOSAVE("first_person_move_sensitivity = %d\\n", (int)settings.first_person_move_sensitivity);\n#ifdef PLATFORM_VITA\n    TOSAVE("vita_rear_touch_enabled = %s\\n", settings.vita_rear_touch_enabled ? "true" : "false");\n#endif\n''', 'rear save')
p.write_text(s, encoding='utf-8')

# 4) Rear touch obeys setting; front touch and Cross/Circle mouse path stay intact.
p = Path('src/input/input_vita.c')
s = p.read_text(encoding='utf-8')
inc = '#include "../bflib_keybrd.h"\n'
if '#include "../config_settings.h"\n' not in s:
    s = replace_once(s, inc, inc + '#include "../config_settings.h"\n', 'input settings include')
needle = '    if (s_touchDataBack.reportNum > 0) {\n'
if needle not in s:
    raise SystemExit('v15 patch: rear touch camera block missing')
s = s.replace(needle, '    if (settings.vita_rear_touch_enabled && s_touchDataBack.reportNum > 0) {\n', 1)
s = replace_once(s,
'''static void update_rear_touch_wheel(void)\n{\n    if (s_touchDataBack.reportNum <= 0) {\n''',
'''static void update_rear_touch_wheel(void)\n{\n    if (!settings.vita_rear_touch_enabled) {\n        s_rearTouchActive = false;\n        s_rearWheelAccum = 0;\n        s_wheelPulses = 0;\n        return;\n    }\n    if (s_touchDataBack.reportNum <= 0) {\n''', 'rear wheel gate')
p.write_text(s, encoding='utf-8')

# 5) Add Rear Touchpad toggle to frontend Options.
p = Path('src/frontmenu_options.h')
s = p.read_text(encoding='utf-8')
s = replace_once(s, 'void frontend_draw_invert_mouse(struct GuiButton *gbtn);\n',
'''void frontend_draw_invert_mouse(struct GuiButton *gbtn);\n#ifdef PLATFORM_VITA\nvoid frontend_vita_rear_touch(struct GuiButton *gbtn);\nvoid frontend_draw_vita_rear_touch(struct GuiButton *gbtn);\n#endif\n''', 'rear option declarations')
p.write_text(s, encoding='utf-8')

p = Path('src/frontmenu_options.c')
s = p.read_text(encoding='utf-8')
idx = s.find('void frontend_draw_invert_mouse(struct GuiButton *gbtn)\n{\n')
insert_at = s.find('/**\n * Initializes start state of GUI menu settings.', idx)
if idx < 0 or insert_at < 0:
    raise SystemExit('v15 patch: frontend options insertion point missing')
funcs = r'''
#ifdef PLATFORM_VITA
void frontend_vita_rear_touch(struct GuiButton *gbtn)
{
    (void)gbtn;
    settings.vita_rear_touch_enabled = !settings.vita_rear_touch_enabled;
    save_settings();
    SYNCMSG("[V15 rear] rear touch %s", settings.vita_rear_touch_enabled ? "enabled" : "disabled");
}

void frontend_draw_vita_rear_touch(struct GuiButton *gbtn)
{
    int font_idx = frontend_button_caption_font(gbtn, frontend_mouse_over_button);
    LbTextSetFont(frontend_font[font_idx]);
    LbTextSetWindow(gbtn->scr_pos_x, gbtn->scr_pos_y, gbtn->width, gbtn->height);
    int tx_units_per_px = gbtn->height * 16 / LbTextLineHeight();
    const char *state = get_string(settings.vita_rear_touch_enabled ? GUIStr_On : GUIStr_Off);
    char text[96];
    snprintf(text, sizeof(text), "Rear Touchpad: %s", state);
    LbTextDrawResized(0, 0, tx_units_per_px, text);
}
#endif

'''
s = s[:insert_at] + funcs + s[insert_at:]
p.write_text(s, encoding='utf-8')

p = Path('src/frontmenu_options_data.cpp')
s = p.read_text(encoding='utf-8')
row = '  {LbBtnT_NormalBtn,  BID_DEFAULT, 0, 0, NULL,               NULL,        NULL,               0, 320, 303,   0,   0,100, 26, frontend_draw_invert_mouse,        0, GUIStr_Empty,  0,     {102},            0, NULL },\n'
added = row + '''#ifdef PLATFORM_VITA\n  {LbBtnT_NormalBtn,  BID_DEFAULT, 0, 0, frontend_vita_rear_touch,NULL, frontend_over_button,0, 102, 331, 102, 331,380, 26, frontend_draw_vita_rear_touch,      0, GUIStr_Empty,  0,       {0},            0, NULL },\n#endif\n'''
s = replace_once(s, row, added, 'rear option row')
p.write_text(s, encoding='utf-8')

# 6) Victory FinishLevel (Square/Space) must survive the transient Vita input lock.
p = Path('src/front_input.c')
s = p.read_text(encoding='utf-8')
# V13 diagnostics inserted a PLATFORM_VITA gate immediately after this declaration,
# so insert before that diagnostic block rather than expecting the old direct if().
anchor = '''    struct PlayerInfo* player = get_my_player();\n#ifdef PLATFORM_VITA\n    if ((player->allocflags & PlaF_MouseInputDisabled) != 0)\n'''
finish = '''    struct PlayerInfo* player = get_my_player();\n#ifdef PLATFORM_VITA\n    if ((player->allocflags & PlaF_MouseInputDisabled) != 0 &&\n        player->victory_state != VicS_Undecided &&\n        is_game_key_pressed(Gkey_FinishLevel, true, false))\n    {\n        SYNCMSG("[V15 finish] accepting FinishLevel through Vita input lock; victory=%d instance=%d",\n                (int)player->victory_state, (int)player->instance_num);\n        set_players_packet_action(player, PckA_FinishGame, player->victory_state, 0, 0, 0);\n        return true;\n    }\n    if ((player->allocflags & PlaF_MouseInputDisabled) != 0)\n'''
s = replace_once(s, anchor, finish, 'Vita FinishLevel after V13 diagnostics')
p.write_text(s, encoding='utf-8')

checks = {
    'src/bflib_network_stub.c': ['[V15 quit]', 'quit_game = 1;', 'exit_keeper = 1;', 'LOCAL_PACKET_HISTORY_SIZE 40'],
    'src/main.cpp': ['SCE_SYSTEM_PARAM_ID_LANG', '[V15 language]', 'vita_apply_system_language();'],
    'src/config_settings.h': ['vita_rear_touch_enabled'],
    'src/config_settings.c': ['vita_rear_touch_enabled        = false', 'vita_rear_touch_enabled = %s'],
    'src/input/input_vita.c': ['settings.vita_rear_touch_enabled', 'SCE_CTRL_CROSS', 'INPUT_MOUSE_BUTTON_LEFT', 'SCE_CTRL_CIRCLE', 'INPUT_MOUSE_BUTTON_RIGHT'],
    'src/frontmenu_options_data.cpp': ['frontend_vita_rear_touch', 'frontend_draw_vita_rear_touch'],
    'src/front_input.c': ['[V15 finish]'],
}
for name, needles in checks.items():
    text = Path(name).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'v15 patch: gate failed {name}: {needle}')

print('v15 Vita polish patch applied')
