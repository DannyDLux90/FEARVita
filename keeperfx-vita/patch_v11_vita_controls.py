from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v11 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# 1) Vita raw input: direct face-button mouse clicks + reliable camera vector.
#    Left stick / D-pad / active front-touch edge zones pan the map/camera.
#    Right stick remains the pointer. Touch away from edges remains pointer/click.
# ---------------------------------------------------------------------------
p = Path('src/input/input_vita.c')
s = p.read_text(encoding='utf-8')

# Slightly more responsive deadzone while still comfortably above the neutral
# jitter measured on hardware (roughly +/- 12 around centre in the user log).
s = s.replace('#define VITA_STICK_DEADZONE          30', '#define VITA_STICK_DEADZONE          24', 1)
s = s.replace('#define VITA_CAMERA_STICK_THRESHOLD  48', '#define VITA_CAMERA_STICK_THRESHOLD  32', 1)

# Add an explicit logical-screen touch edge zone used only while the finger is
# actually down. This avoids permanent edge scrolling after a touch is released.
anchor = '#define VITA_TOUCH_HOLD_FRAMES       14\n'
if anchor not in s:
    raise SystemExit('v11 patch: touch-hold define not found')
s = s.replace(anchor, anchor + '#define VITA_TOUCH_SCROLL_EDGE       56\n', 1)

# v10's rear-touch-only keyboard fallback is useful, but add physical Vita
# buttons back as keyboard fallbacks. v9's single-poll ordering now makes these
# dependable and they cover menu/game actions which are not mouse clicks.
old = '''static void update_key_states(void)\n{\n    unsigned char new_state[KC_LIST_END];\n    memset(new_state, 0, sizeof(new_state));\n    merge_vita_camera_keys(new_state);\n\n    for (int keycode = 0; keycode < KC_LIST_END; keycode++) {\n'''
new = '''static void update_key_states(void)\n{\n    unsigned char new_state[KC_LIST_END];\n    memset(new_state, 0, sizeof(new_state));\n\n    // D-pad is a universally reliable fallback for menu navigation and camera.\n    if (s_padData.buttons & SCE_CTRL_LEFT)  new_state[KC_LEFT] = 1;\n    if (s_padData.buttons & SCE_CTRL_RIGHT) new_state[KC_RIGHT] = 1;\n    if (s_padData.buttons & SCE_CTRL_UP)    new_state[KC_UP] = 1;\n    if (s_padData.buttons & SCE_CTRL_DOWN)  new_state[KC_DOWN] = 1;\n\n    if (s_padData.buttons & SCE_CTRL_SQUARE)   new_state[KC_SPACE] = 1;\n    if (s_padData.buttons & SCE_CTRL_TRIANGLE) new_state[KC_TAB] = 1;\n    if (s_padData.buttons & SCE_CTRL_L1)       new_state[KC_LSHIFT] = 1;\n    if (s_padData.buttons & SCE_CTRL_R1)       new_state[KC_LCONTROL] = 1;\n    if (s_padData.buttons & SCE_CTRL_START)    new_state[KC_ESCAPE] = 1;\n    if (s_padData.buttons & SCE_CTRL_SELECT)   new_state[KC_M] = 1;\n\n    merge_vita_camera_keys(new_state);\n\n    for (int keycode = 0; keycode < KC_LIST_END; keycode++) {\n'''
s = replace_once(s, old, new, 'physical keyboard fallbacks')

# Restore direct physical mouse buttons. This is intentionally the same path
# that already works for front touch; it bypasses controller bindings entirely.
anchor = '''static void apply_click_pulses(void)\n{\n'''
if anchor not in s:
    raise SystemExit('v11 patch: apply_click_pulses not found')
phys = '''static void update_physical_mouse_buttons(void)\n{\n    if (s_padData.buttons & SCE_CTRL_CROSS)\n        s_mouseButtons |= INPUT_MOUSE_BUTTON_LEFT;\n    if (s_padData.buttons & SCE_CTRL_CIRCLE)\n        s_mouseButtons |= INPUT_MOUSE_BUTTON_RIGHT;\n}\n\n'''
s = s.replace(anchor, phys + anchor, 1)

old = '''    update_front_touch();\n    if (!s_frontTouchActive) {\n        update_cursor_from_right_stick();\n    }\n    apply_click_pulses();\n'''
new = '''    update_front_touch();\n    if (!s_frontTouchActive) {\n        update_cursor_from_right_stick();\n    }\n    update_physical_mouse_buttons();\n    apply_click_pulses();\n'''
s = replace_once(s, old, new, 'direct Cross/Circle mouse path')

# Cross/Circle must not also synthesize controller trigger clicks; duplicate
# down/up transitions were one of the sources of inconsistent v10 behaviour.
s = s.replace('    if (s_padData.buttons & SCE_CTRL_CROSS)    out |= CBtn_R2;\n', '', 1)
s = s.replace('    if (s_padData.buttons & SCE_CTRL_CIRCLE)   out |= CBtn_L2;\n', '', 1)

# Add a direct camera vector. Left stick is proportional, D-pad is digital, and
# touch scroll only exists while a finger is down in an edge zone.
anchor = '''float vita_get_controller_axis_value(TbControllerButtons btn)\n{\n'''
idx = s.find(anchor)
if idx < 0:
    raise SystemExit('v11 patch: controller axis function not found')
# Insert the helper before the axis function so both can reuse the deadzone.
helper = r'''static float vita_camera_axis(int raw)
{
    const int mag = abs(raw);
    if (mag <= VITA_STICK_DEADZONE)
        return 0.0f;
    float value = (float)(mag - VITA_STICK_DEADZONE) /
                  (float)(127 - VITA_STICK_DEADZONE);
    if (value > 1.0f) value = 1.0f;
    // Gentle curve: accurate near centre, fast enough at the rim.
    value = value * value;
    return raw < 0 ? -value : value;
}

void vita_get_camera_scroll(float *out_x, float *out_y)
{
    float x = vita_camera_axis((int)s_padData.lx - 128);
    float y = vita_camera_axis((int)s_padData.ly - 128);

    if (s_padData.buttons & SCE_CTRL_LEFT)  x = -1.0f;
    if (s_padData.buttons & SCE_CTRL_RIGHT) x =  1.0f;
    if (s_padData.buttons & SCE_CTRL_UP)    y = -1.0f;
    if (s_padData.buttons & SCE_CTRL_DOWN)  y =  1.0f;

    // Touch scrolling is edge-driven and active only while touching. The
    // pointer may remain at an edge after release without moving the camera.
    if (s_touchDataFront.reportNum > 0) {
        const int tx = touch_x_to_screen((int)s_touchDataFront.report[0].x);
        const int ty = touch_y_to_screen((int)s_touchDataFront.report[0].y);
        float touch_x = 0.0f;
        float touch_y = 0.0f;
        if (tx < VITA_TOUCH_SCROLL_EDGE)
            touch_x = -(float)(VITA_TOUCH_SCROLL_EDGE - tx) / (float)VITA_TOUCH_SCROLL_EDGE;
        else if (tx >= VITA_SCREEN_WIDTH - VITA_TOUCH_SCROLL_EDGE)
            touch_x = (float)(tx - (VITA_SCREEN_WIDTH - VITA_TOUCH_SCROLL_EDGE - 1)) /
                      (float)VITA_TOUCH_SCROLL_EDGE;
        if (ty < VITA_TOUCH_SCROLL_EDGE)
            touch_y = -(float)(VITA_TOUCH_SCROLL_EDGE - ty) / (float)VITA_TOUCH_SCROLL_EDGE;
        else if (ty >= VITA_SCREEN_HEIGHT - VITA_TOUCH_SCROLL_EDGE)
            touch_y = (float)(ty - (VITA_SCREEN_HEIGHT - VITA_TOUCH_SCROLL_EDGE - 1)) /
                      (float)VITA_TOUCH_SCROLL_EDGE;
        if (touch_x < -1.0f) touch_x = -1.0f;
        if (touch_x >  1.0f) touch_x =  1.0f;
        if (touch_y < -1.0f) touch_y = -1.0f;
        if (touch_y >  1.0f) touch_y =  1.0f;
        if (fabsf(touch_x) > fabsf(x)) x = touch_x;
        if (fabsf(touch_y) > fabsf(y)) y = touch_y;
    }

    if (out_x != NULL) *out_x = x;
    if (out_y != NULL) *out_y = y;
}

'''
# input_vita.c currently has stdlib but not math; fabsf is used above.
include_anchor = '#include <stdlib.h>\n'
if include_anchor in s and '#include <math.h>\n' not in s:
    s = s.replace(include_anchor, '#include <math.h>\n' + include_anchor, 1)
s = s[:idx] + helper + s[idx:]
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 2) Game camera: use the direct Vita scroll vector and disable cursor-at-edge
#    panning on Vita. This removes the permanent top-left drift completely.
# ---------------------------------------------------------------------------
p = Path('src/front_input.c')
s = p.read_text(encoding='utf-8')

# Declaration near the top-level extern section.
inc_anchor = '#include "post_inc.h"\n'
if inc_anchor not in s:
    raise SystemExit('v11 patch: front_input post_inc include not found')
if 'vita_get_camera_scroll' not in s:
    s = s.replace(inc_anchor, inc_anchor + '#ifdef PLATFORM_VITA\nextern void vita_get_camera_scroll(float *out_x, float *out_y);\n#endif\n', 1)

old = '''    float movement_x = get_game_key_axis_value(Gkey_MoveRight,ignore_mods) - get_game_key_axis_value(Gkey_MoveLeft,ignore_mods);\n    float movement_y = get_game_key_axis_value(Gkey_MoveDown, ignore_mods) - get_game_key_axis_value(Gkey_MoveUp, ignore_mods);\n\n    // Handle horizontal movement - just accumulate for local camera\n'''
new = '''    float movement_x = get_game_key_axis_value(Gkey_MoveRight,ignore_mods) - get_game_key_axis_value(Gkey_MoveLeft,ignore_mods);\n    float movement_y = get_game_key_axis_value(Gkey_MoveDown, ignore_mods) - get_game_key_axis_value(Gkey_MoveUp, ignore_mods);\n#ifdef PLATFORM_VITA\n    // Bypass SDL/controller-binding translation for primary camera movement.\n    float vita_x = 0.0f, vita_y = 0.0f;\n    vita_get_camera_scroll(&vita_x, &vita_y);\n    if (fabsf(vita_x) > fabsf(movement_x)) movement_x = vita_x;\n    if (fabsf(vita_y) > fabsf(movement_y)) movement_y = vita_y;\n#endif\n\n    // Handle horizontal movement - just accumulate for local camera\n'''
s = replace_once(s, old, new, 'direct Vita in-game movement')

# Mouse-edge camera panning is useful on desktop, but wrong for an absolute
# touchscreen because a released pointer can remain at the edge forever.
old = '    if (is_feature_on(Ft_DisableCursorCameraPanning) == false)\n'
new = '''#ifdef PLATFORM_VITA\n    if (0) // Vita pans only from active touch edge zones / stick / D-pad.\n#else\n    if (is_feature_on(Ft_DisableCursorCameraPanning) == false)\n#endif\n'''
s = replace_once(s, old, new, 'disable passive Vita pointer-edge panning')
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 3) Campaign land view/map: same direct vector; no passive pointer-edge drift.
# ---------------------------------------------------------------------------
p = Path('src/front_landview.c')
s = p.read_text(encoding='utf-8')

inc_anchor = '#include "post_inc.h"\n'
if inc_anchor not in s:
    raise SystemExit('v11 patch: front_landview post_inc include not found')
if 'vita_get_camera_scroll' not in s:
    s = s.replace(inc_anchor, inc_anchor + '#ifdef PLATFORM_VITA\nextern void vita_get_camera_scroll(float *out_x, float *out_y);\n#endif\n', 1)

start = s.find('void check_mouse_scroll(void)\n{')
end = s.find('\nvoid update_velocity(void)', start)
if start < 0 or end < 0:
    raise SystemExit('v11 patch: check_mouse_scroll function not found')
new_func = r'''void check_mouse_scroll(void)
{
#ifdef PLATFORM_VITA
    float sx = 0.0f, sy = 0.0f;
    vita_get_camera_scroll(&sx, &sy);
    const float ax = fabsf(sx);
    const float ay = fabsf(sy);
    if (ax > 0.01f) {
        map_info.velocity_x += (sx < 0.0f ? -1.0f : 1.0f) *
                               LANDVIEW_PAN_ACCEL * game.delta_time * ax;
        if (map_info.velocity_x < -LANDVIEW_PAN_MAX_SPEED) map_info.velocity_x = -LANDVIEW_PAN_MAX_SPEED;
        if (map_info.velocity_x >  LANDVIEW_PAN_MAX_SPEED) map_info.velocity_x =  LANDVIEW_PAN_MAX_SPEED;
    }
    if (ay > 0.01f) {
        map_info.velocity_y += (sy < 0.0f ? -1.0f : 1.0f) *
                               LANDVIEW_PAN_ACCEL * game.delta_time * ay;
        if (map_info.velocity_y < -LANDVIEW_PAN_MAX_SPEED) map_info.velocity_y = -LANDVIEW_PAN_MAX_SPEED;
        if (map_info.velocity_y >  LANDVIEW_PAN_MAX_SPEED) map_info.velocity_y =  LANDVIEW_PAN_MAX_SPEED;
    }
#else
    long mx = GetMouseX();
    if ( (mx < 8) || ( (is_game_key_pressed(Gkey_MoveLeft, false, false)) || (is_key_pressed(KC_LEFT,KMod_DONTCARE)) ) )
    {
        map_info.velocity_x -= LANDVIEW_PAN_ACCEL * game.delta_time;
        if (map_info.velocity_x < -LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_x = -LANDVIEW_PAN_MAX_SPEED;
        if (map_info.velocity_x > LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_x = LANDVIEW_PAN_MAX_SPEED;
    } else
    if ( (mx >= RendererPhysicalWidth()-8) || ( (is_game_key_pressed(Gkey_MoveRight, false, false)) || (is_key_pressed(KC_RIGHT,KMod_DONTCARE)) ) )
    {
        map_info.velocity_x += LANDVIEW_PAN_ACCEL * game.delta_time;
        if (map_info.velocity_x < -LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_x = -LANDVIEW_PAN_MAX_SPEED;
        if (map_info.velocity_x > LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_x = LANDVIEW_PAN_MAX_SPEED;
    }
    long my = GetMouseY();
    if ( (my < 8) || ( (is_game_key_pressed(Gkey_MoveUp, false, false)) || (is_key_pressed(KC_UP,KMod_DONTCARE)) ) )
    {
        map_info.velocity_y -= LANDVIEW_PAN_ACCEL * game.delta_time;
        if (map_info.velocity_y < -LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_y = -LANDVIEW_PAN_MAX_SPEED;
        if (map_info.velocity_y > LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_y = LANDVIEW_PAN_MAX_SPEED;
    } else
    if ( (my >= RendererPhysicalHeight()-8) || ( (is_game_key_pressed(Gkey_MoveDown, false, false)) || (is_key_pressed(KC_DOWN,KMod_DONTCARE)) ) )
    {
        map_info.velocity_y += LANDVIEW_PAN_ACCEL * game.delta_time;
        if (map_info.velocity_y < -LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_y = -LANDVIEW_PAN_MAX_SPEED;
        if (map_info.velocity_y > LANDVIEW_PAN_MAX_SPEED)
            map_info.velocity_y = LANDVIEW_PAN_MAX_SPEED;
    }
#endif
}
'''
s = s[:start] + new_func + s[end:]
p.write_text(s, encoding='utf-8')

print('v11 Vita controls patch applied')
