from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v13 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# 1) Raw Vita input telemetry.
p = Path('src/input/input_vita.c')
s = p.read_text(encoding='utf-8')
anchor = 'static unsigned char s_keyState[KC_LIST_END];\n'
if anchor not in s:
    raise SystemExit('v13 patch: Vita key-state anchor missing')
extra = r'''
static uint32_t s_v13_prev_buttons = 0xffffffffu;
static int s_v13_prev_lx_bucket = 999;
static int s_v13_prev_ly_bucket = 999;
static int s_v13_prev_rx_bucket = 999;
static int s_v13_prev_ry_bucket = 999;
static int s_v13_prev_front_reports = -1;
static int s_v13_diag_ticks = 0;
'''
if 's_v13_prev_buttons' not in s:
    s = s.replace(anchor, anchor + extra, 1)
anchor = '    apply_click_pulses();\n'
if anchor not in s:
    raise SystemExit('v13 patch: apply_click_pulses call missing')
telemetry = r'''    apply_click_pulses();

    const int v13_lx = (int)s_padData.lx - 128;
    const int v13_ly = (int)s_padData.ly - 128;
    const int v13_rx = (int)s_padData.rx - 128;
    const int v13_ry = (int)s_padData.ry - 128;
    const int v13_lxb = v13_lx / 16;
    const int v13_lyb = v13_ly / 16;
    const int v13_rxb = v13_rx / 16;
    const int v13_ryb = v13_ry / 16;
    const int v13_active = (abs(v13_lx) > VITA_STICK_DEADZONE) ||
                           (abs(v13_ly) > VITA_STICK_DEADZONE) ||
                           (abs(v13_rx) > VITA_STICK_DEADZONE) ||
                           (abs(v13_ry) > VITA_STICK_DEADZONE) ||
                           (s_touchDataFront.reportNum > 0);
    s_v13_diag_ticks++;
    if ((s_padData.buttons != s_v13_prev_buttons) ||
        (v13_lxb != s_v13_prev_lx_bucket) || (v13_lyb != s_v13_prev_ly_bucket) ||
        (v13_rxb != s_v13_prev_rx_bucket) || (v13_ryb != s_v13_prev_ry_bucket) ||
        ((int)s_touchDataFront.reportNum != s_v13_prev_front_reports) ||
        (v13_active && ((s_v13_diag_ticks % 15) == 0)))
    {
        SYNCLOG("[V13 raw] btn=0x%08X L=(%d,%d) R=(%d,%d) front=%d back=%d mouse=(%d,%d) mb=0x%X",
                (unsigned int)s_padData.buttons, v13_lx, v13_ly, v13_rx, v13_ry,
                (int)s_touchDataFront.reportNum, (int)s_touchDataBack.reportNum,
                s_mouseX, s_mouseY, s_mouseButtons);
        s_v13_prev_buttons = s_padData.buttons;
        s_v13_prev_lx_bucket = v13_lxb; s_v13_prev_ly_bucket = v13_lyb;
        s_v13_prev_rx_bucket = v13_rxb; s_v13_prev_ry_bucket = v13_ryb;
        s_v13_prev_front_reports = (int)s_touchDataFront.reportNum;
    }
'''
s = replace_once(s, anchor, telemetry, 'raw Vita telemetry')
p.write_text(s, encoding='utf-8')

# 2) KeeperFX input gates + camera vector telemetry.
p = Path('src/front_input.c')
s = p.read_text(encoding='utf-8')
old = r'''static void vita_recover_stale_ingame_input_lock(struct PlayerInfo *player)
{
    if ((player == NULL) || (player->view_type != PVT_DungeonTop) ||
        (player->instance_num != PI_Unset))
        return;

    const unsigned long stale = player->allocflags &
        (PlaF_MouseInputDisabled | PlaF_KeyboardInputDisabled);
    if (stale != 0)
    {
        player->allocflags &= ~(PlaF_MouseInputDisabled | PlaF_KeyboardInputDisabled);
        JUSTLOG("[Vita input] recovered stale dungeon input lock flags=0x%lx turn=%lu",
                stale, (unsigned long)game.play_gameturn);
    }
}
'''
new = r'''static void vita_recover_stale_ingame_input_lock(struct PlayerInfo *player)
{
    static int last_view_type = -999;
    static int last_view_mode = -999;
    static int last_instance = -999;
    static unsigned long last_allocflags = ~0UL;
    static int last_work_state = -999;
    if (player == NULL)
    {
        JUSTLOG("[V13 state] player=NULL");
        return;
    }

    const unsigned long turn = (unsigned long)get_gameturn();
    const int changed = ((int)player->view_type != last_view_type) ||
                        ((int)player->view_mode != last_view_mode) ||
                        ((int)player->instance_num != last_instance) ||
                        ((unsigned long)player->allocflags != last_allocflags) ||
                        ((int)player->work_state != last_work_state);
    if (changed || ((turn % 30UL) == 0UL))
    {
        JUSTLOG("[V13 state] turn=%lu view_type=%d view_mode=%d inst=%d remain=%ld alloc=0x%lx work=%d op=0x%lx",
                turn, (int)player->view_type, (int)player->view_mode,
                (int)player->instance_num, (long)player->instance_remain_turns,
                (unsigned long)player->allocflags, (int)player->work_state,
                (unsigned long)game.operation_flags);
        last_view_type = (int)player->view_type;
        last_view_mode = (int)player->view_mode;
        last_instance = (int)player->instance_num;
        last_allocflags = (unsigned long)player->allocflags;
        last_work_state = (int)player->work_state;
    }

    if ((player->view_type != PVT_DungeonTop) || (player->instance_num != PI_Unset))
        return;

    const unsigned long stale = player->allocflags &
        (PlaF_MouseInputDisabled | PlaF_KeyboardInputDisabled);
    if (stale != 0)
    {
        player->allocflags &= ~(PlaF_MouseInputDisabled | PlaF_KeyboardInputDisabled);
        JUSTLOG("[V13 recovery] stale dungeon input lock flags=0x%lx turn=%lu",
                stale, turn);
    }
}
'''
s = replace_once(s, old, new, 'expand v12 state probe')
old = '    if ((player->allocflags & PlaF_MouseInputDisabled) != 0)\n    {\n'
new = r'''#ifdef PLATFORM_VITA
    if ((player->allocflags & PlaF_MouseInputDisabled) != 0)
    {
        JUSTLOG("[V13 gate] get_inputs MOUSE_DISABLED view_type=%d view_mode=%d inst=%d remain=%ld flags=0x%lx",
                (int)player->view_type, (int)player->view_mode, (int)player->instance_num,
                (long)player->instance_remain_turns, (unsigned long)player->allocflags);
    }
#endif
    if ((player->allocflags & PlaF_MouseInputDisabled) != 0)
    {
'''
s = replace_once(s, old, new, 'mouse-disabled input gate')
old = '''    if ((player->allocflags & PlaF_KeyboardInputDisabled) != 0)\n      return;\n'''
new = r'''    if ((player->allocflags & PlaF_KeyboardInputDisabled) != 0)
    {
#ifdef PLATFORM_VITA
        JUSTLOG("[V13 gate] iso KEYBOARD_DISABLED inst=%d remain=%ld flags=0x%lx",
                (int)player->instance_num, (long)player->instance_remain_turns,
                (unsigned long)player->allocflags);
#endif
        return;
    }
'''
s = replace_once(s, old, new, 'isometric keyboard gate')
old = '''    *out_movement_x = clamp(*out_movement_x, -1.0f, 1.0f);\n    *out_movement_y = clamp(*out_movement_y, -1.0f, 1.0f);\n}\n'''
new = r'''    *out_movement_x = clamp(*out_movement_x, -1.0f, 1.0f);
    *out_movement_y = clamp(*out_movement_y, -1.0f, 1.0f);
#ifdef PLATFORM_VITA
    if ((fabsf(vita_x) > 0.001f) || (fabsf(vita_y) > 0.001f) ||
        ((get_gameturn() % 60) == 0))
    {
        JUSTLOG("[V13 move] vita=(%.3f,%.3f) merged=(%.3f,%.3f) ignore_mods=%d",
                vita_x, vita_y, *out_movement_x, *out_movement_y, (int)ignore_mods);
    }
#endif
}
'''
s = replace_once(s, old, new, 'movement vector telemetry')
old = '''        get_dungeon_control_nonaction_inputs();\n        get_player_gui_clicks();\n        get_packet_control_mouse_clicks();\n        return inp_handled;\n'''
new = r'''        get_dungeon_control_nonaction_inputs();
#ifdef PLATFORM_VITA
        if (left_button_clicked || left_button_held || left_button_released ||
            right_button_clicked || right_button_held || right_button_released)
        {
            JUSTLOG("[V13 click-pre] L c=%d h=%d r=%d R c=%d h=%d r=%d mouse=(%ld,%ld)",
                    (int)left_button_clicked, (int)left_button_held, (int)left_button_released,
                    (int)right_button_clicked, (int)right_button_held, (int)right_button_released,
                    GetMouseX(), GetMouseY());
        }
#endif
        get_player_gui_clicks();
        get_packet_control_mouse_clicks();
#ifdef PLATFORM_VITA
        {
            struct Packet* v13p = get_packet(my_player_number);
            if ((v13p->control_flags & (PCtr_LBtnAnyAction | PCtr_RBtnAnyAction)) != 0)
                JUSTLOG("[V13 click-packet] flags=0x%08lx pos=(%ld,%ld) action=%d",
                        (unsigned long)v13p->control_flags, (long)v13p->pos_x,
                        (long)v13p->pos_y, (int)v13p->action);
        }
#endif
        return inp_handled;
'''
s = replace_once(s, old, new, 'dungeon click telemetry')
p.write_text(s, encoding='utf-8')

# 3) Mouse bridge telemetry.
p = Path('src/kjm_input.c')
s = p.read_text(encoding='utf-8')
old = '    s_prev_input_buttons = ibuttons;\n'
new = r'''    if ((ibuttons != s_prev_input_buttons) || btn_left || btn_right)
    {
      JUSTLOG("[V13 mouse-bridge] ib=0x%X prev=0x%X L=%d R=%d lbL=%d lbR=%d mL=%d mR=%d xy=(%d,%d)",
              ibuttons, s_prev_input_buttons, btn_left, btn_right,
              (int)lbDisplay.LeftButton, (int)lbDisplay.RightButton,
              (int)lbDisplay.MLeftButton, (int)lbDisplay.MRightButton, ix, iy);
    }
    s_prev_input_buttons = ibuttons;
'''
s = replace_once(s, old, new, 'native mouse bridge telemetry')
old = '''  update_wheel_scrolled();\n  lbDisplay.LeftButton = 0;\n'''
new = r'''  update_wheel_scrolled();
#ifdef PLATFORM_VITA
  if (left_button_clicked || left_button_held || left_button_released ||
      right_button_clicked || right_button_held || right_button_released)
  {
    JUSTLOG("[V13 mouse-sem] L c=%d h=%d r=%d R c=%d h=%d r=%d display L=%d/%d R=%d/%d",
            (int)left_button_clicked, (int)left_button_held, (int)left_button_released,
            (int)right_button_clicked, (int)right_button_held, (int)right_button_released,
            (int)lbDisplay.LeftButton, (int)lbDisplay.MLeftButton,
            (int)lbDisplay.RightButton, (int)lbDisplay.MRightButton);
  }
#endif
  lbDisplay.LeftButton = 0;
'''
s = replace_once(s, old, new, 'semantic mouse telemetry')
p.write_text(s, encoding='utf-8')

# 4) Local camera telemetry.
p = Path('src/local_camera.c')
s = p.read_text(encoding='utf-8')
old = '''    local_camera_ready = true;\n}\n\nvoid process_local_minimap_click'''
new = r'''    local_camera_ready = true;
#ifdef PLATFORM_VITA
    JUSTLOG("[V13 localcam] init player=%d ready=1 iso=(%ld,%ld) mode=%d",
            (int)player->id_number,
            (long)destination_local_cameras[CamIV_Isometric].mappos.x.val,
            (long)destination_local_cameras[CamIV_Isometric].mappos.y.val,
            (int)destination_local_cameras[CamIV_Isometric].view_mode);
#endif
}

void process_local_minimap_click'''
s = replace_once(s, old, new, 'local camera init telemetry')
old = '''    if (!local_camera_ready) {\n        return;\n    }\n'''
new = r'''    if (!local_camera_ready) {
#ifdef PLATFORM_VITA
        if ((get_gameturn() % 30) == 0)
            JUSTLOG("[V13 localcam] NOT_READY turn=%lu", (unsigned long)get_gameturn());
#endif
        return;
    }
'''
s = replace_once(s, old, new, 'local camera not-ready gate')
old = '''        struct Packet* local_packet = get_packet_for_local_camera_update();\n        if (local_packet == NULL) {\n            return;\n        }\n        process_local_minimap_click(local_packet);\n        // Only process camera controls for the currently active camera view\n        int active_cam_idx = (my_player->view_mode == PVM_FrontView) ? CamIV_FrontView : CamIV_Isometric;\n        process_camera_controls(&destination_local_cameras[active_cam_idx], local_packet, my_player, true);\n        view_process_camera_inertia(&destination_local_cameras[active_cam_idx]);\n'''
new = r'''        struct Packet* local_packet = get_packet_for_local_camera_update();
        if (local_packet == NULL) {
#ifdef PLATFORM_VITA
            JUSTLOG("[V13 localcam] NO_HISTORY_PACKET turn=%lu packet_num=%d",
                    (unsigned long)get_gameturn(), (int)my_player->packet_num);
#endif
            return;
        }
        process_local_minimap_click(local_packet);
        // Only process camera controls for the currently active camera view
        int active_cam_idx = (my_player->view_mode == PVM_FrontView) ? CamIV_FrontView : CamIV_Isometric;
#ifdef PLATFORM_VITA
        const float v13_mx = camera_movement_x;
        const float v13_my = camera_movement_y;
        const long v13_before_x = destination_local_cameras[active_cam_idx].mappos.x.val;
        const long v13_before_y = destination_local_cameras[active_cam_idx].mappos.y.val;
#endif
        process_camera_controls(&destination_local_cameras[active_cam_idx], local_packet, my_player, true);
        view_process_camera_inertia(&destination_local_cameras[active_cam_idx]);
#ifdef PLATFORM_VITA
        if ((fabsf(v13_mx) > 0.001f) || (fabsf(v13_my) > 0.001f) ||
            ((get_gameturn() % 60) == 0))
        {
            JUSTLOG("[V13 localcam] turn=%lu mode=%d move=(%.3f,%.3f) pkt=0x%08lx pos=(%ld,%ld)->(%ld,%ld)",
                    (unsigned long)get_gameturn(), (int)my_player->view_mode,
                    v13_mx, v13_my, (unsigned long)local_packet->control_flags,
                    v13_before_x, v13_before_y,
                    (long)destination_local_cameras[active_cam_idx].mappos.x.val,
                    (long)destination_local_cameras[active_cam_idx].mappos.y.val);
        }
#endif
'''
s = replace_once(s, old, new, 'local camera movement telemetry')
if '#include <math.h>\n' not in s:
    s = s.replace('#include "post_inc.h"\n', '#include <math.h>\n#include "post_inc.h"\n', 1)
p.write_text(s, encoding='utf-8')

# 5) Player instance transitions.
p = Path('src/player_instances.c')
s = p.read_text(encoding='utf-8')
anchor = '''void set_player_instance(struct PlayerInfo *player, long ninum, TbBool force)\n{\n'''
if anchor not in s:
    raise SystemExit('v13 patch: set_player_instance anchor missing')
new = r'''void set_player_instance(struct PlayerInfo *player, long ninum, TbBool force)
{
#ifdef PLATFORM_VITA
    JUSTLOG("[V13 instance] old=%d new=%ld force=%d remain=%ld view_type=%d view_mode=%d flags=0x%lx",
            (int)player->instance_num, ninum, (int)force,
            (long)player->instance_remain_turns, (int)player->view_type,
            (int)player->view_mode, (unsigned long)player->allocflags);
#endif
'''
s = replace_once(s, anchor, new, 'instance transition telemetry')
p.write_text(s, encoding='utf-8')

print('v13 Vita diagnostics patch applied')
