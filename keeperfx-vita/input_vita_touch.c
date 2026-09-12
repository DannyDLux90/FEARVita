/******************************************************************************/
// Free implementation of Bullfrog's Dungeon Keeper strategy game.
/******************************************************************************/
/** @file input_vita.c
 *     PlayStation Vita input implementation.
 * @par Purpose:
 *     Vita-first controls with front/rear touch support.
 *
 * Front touch:
 *   - one finger moves the pointer absolutely
 *   - short tap emits a left click
 *   - hold or move beyond the drag threshold holds left mouse for dragging
 *   - two fingers hold right mouse
 * Rear touch:
 *   - edge zones emulate the arrow keys for camera control
 *   - vertical swipes through the centre emit mouse-wheel pulses
 * Physical controls:
 *   - left stick moves the pointer
 *   - right stick emulates arrow keys for camera movement
 *   - Cross/Circle are left/right mouse buttons
 *   - Square/triangle are Space/Tab
 *   - L/R are Shift/Ctrl
 *   - Start is Escape; Select is M (map)
 */
/******************************************************************************/
#include "kfx_memory.h"
#include "../pre_inc.h"
#include "input_interface.h"

#ifdef PLATFORM_VITA

#include <psp2/ctrl.h>
#include <psp2/touch.h>
#include <stdlib.h>
#include <string.h>

#include "../bflib_keybrd.h"
#include "../post_inc.h"

#ifdef __cplusplus
extern "C" {
#endif
/******************************************************************************/

#define VITA_SCREEN_WIDTH  960
#define VITA_SCREEN_HEIGHT 544
#define VITA_TOUCH_WIDTH   1920
#define VITA_TOUCH_HEIGHT  1088

#define VITA_STICK_DEADZONE          30
#define VITA_CAMERA_STICK_THRESHOLD  48
#define VITA_TOUCH_DRAG_THRESHOLD    14
#define VITA_TOUCH_HOLD_FRAMES       14
#define VITA_REAR_EDGE_X             390
#define VITA_REAR_EDGE_Y             250
#define VITA_REAR_WHEEL_THRESHOLD    120

static const struct {
    uint32_t btn_vita;
    int keycode;
} s_buttonMap[] = {
    { SCE_CTRL_SQUARE,   KC_SPACE },
    { SCE_CTRL_TRIANGLE, KC_TAB },
    { SCE_CTRL_L1,       KC_LSHIFT },
    { SCE_CTRL_R1,       KC_LCONTROL },
    { SCE_CTRL_START,    KC_ESCAPE },
    { SCE_CTRL_SELECT,   KC_M },
    { SCE_CTRL_UP,       KC_UP },
    { SCE_CTRL_DOWN,     KC_DOWN },
    { SCE_CTRL_LEFT,     KC_LEFT },
    { SCE_CTRL_RIGHT,    KC_RIGHT },
};

#define BUTTON_MAP_SIZE (sizeof(s_buttonMap) / sizeof(s_buttonMap[0]))

static SceCtrlData s_padData;
static SceTouchData s_touchDataFront;
static SceTouchData s_touchDataBack;

static int s_mouseX = VITA_SCREEN_WIDTH / 2;
static int s_mouseY = VITA_SCREEN_HEIGHT / 2;
static int s_mouseButtons = 0;
static int s_wheelPulses = 0;

static bool s_frontTouchActive = false;
static bool s_frontDragging = false;
static bool s_frontTwoFinger = false;
static int s_frontTouchFrames = 0;
static int s_frontStartX = 0;
static int s_frontStartY = 0;
static int s_leftClickPulse = 0;
static int s_rightClickPulse = 0;

static bool s_rearTouchActive = false;
static int s_rearLastY = 0;
static int s_rearWheelAccum = 0;

static unsigned char s_keyState[KC_LIST_END];

/******************************************************************************/

static int clamp_int(int value, int min_value, int max_value)
{
    if (value < min_value) return min_value;
    if (value > max_value) return max_value;
    return value;
}

static int touch_x_to_screen(int x)
{
    return clamp_int((x * VITA_SCREEN_WIDTH) / VITA_TOUCH_WIDTH,
                     0, VITA_SCREEN_WIDTH - 1);
}

static int touch_y_to_screen(int y)
{
    return clamp_int((y * VITA_SCREEN_HEIGHT) / VITA_TOUCH_HEIGHT,
                     0, VITA_SCREEN_HEIGHT - 1);
}

static void merge_vita_camera_keys(unsigned char *new_state)
{
    int rx = (int)s_padData.rx - 128;
    int ry = (int)s_padData.ry - 128;

    if (rx <= -VITA_CAMERA_STICK_THRESHOLD) new_state[KC_LEFT] = 1;
    if (rx >=  VITA_CAMERA_STICK_THRESHOLD) new_state[KC_RIGHT] = 1;
    if (ry <= -VITA_CAMERA_STICK_THRESHOLD) new_state[KC_UP] = 1;
    if (ry >=  VITA_CAMERA_STICK_THRESHOLD) new_state[KC_DOWN] = 1;

    if (s_touchDataBack.reportNum > 0) {
        int x = (int)s_touchDataBack.report[0].x;
        int y = (int)s_touchDataBack.report[0].y;
        int dx = x - (VITA_TOUCH_WIDTH / 2);
        int dy = y - (VITA_TOUCH_HEIGHT / 2);

        if (dx <= -VITA_REAR_EDGE_X) new_state[KC_LEFT] = 1;
        if (dx >=  VITA_REAR_EDGE_X) new_state[KC_RIGHT] = 1;
        if (dy <= -VITA_REAR_EDGE_Y) new_state[KC_UP] = 1;
        if (dy >=  VITA_REAR_EDGE_Y) new_state[KC_DOWN] = 1;
    }
}

static void update_key_states(void)
{
    unsigned char new_state[KC_LIST_END];
    memset(new_state, 0, sizeof(new_state));

    for (int i = 0; i < (int)BUTTON_MAP_SIZE; i++) {
        if (s_padData.buttons & s_buttonMap[i].btn_vita) {
            new_state[s_buttonMap[i].keycode] = 1;
        }
    }

    merge_vita_camera_keys(new_state);

    for (int keycode = 0; keycode < KC_LIST_END; keycode++) {
        if (new_state[keycode] != s_keyState[keycode]) {
            keyboardControl(new_state[keycode] ? KActn_KEYDOWN : KActn_KEYUP,
                            (TbKeyCode)keycode, KMod_NONE, 0);
            s_keyState[keycode] = new_state[keycode];
        }
    }
}

static void update_front_touch(void)
{
    const bool touching = (s_touchDataFront.reportNum > 0);

    if (touching) {
        const int x = touch_x_to_screen((int)s_touchDataFront.report[0].x);
        const int y = touch_y_to_screen((int)s_touchDataFront.report[0].y);
        const bool two_fingers = (s_touchDataFront.reportNum >= 2);

        s_mouseX = x;
        s_mouseY = y;

        if (!s_frontTouchActive) {
            s_frontTouchActive = true;
            s_frontDragging = false;
            s_frontTwoFinger = two_fingers;
            s_frontTouchFrames = 0;
            s_frontStartX = x;
            s_frontStartY = y;
        }

        s_frontTouchFrames++;

        if (two_fingers) {
            s_frontTwoFinger = true;
            s_frontDragging = false;
            s_mouseButtons |= INPUT_MOUSE_BUTTON_RIGHT;
            return;
        }

        if (!s_frontTwoFinger) {
            const int dx = abs(x - s_frontStartX);
            const int dy = abs(y - s_frontStartY);
            if (!s_frontDragging &&
                (dx >= VITA_TOUCH_DRAG_THRESHOLD ||
                 dy >= VITA_TOUCH_DRAG_THRESHOLD ||
                 s_frontTouchFrames >= VITA_TOUCH_HOLD_FRAMES)) {
                s_frontDragging = true;
            }

            if (s_frontDragging) {
                s_mouseButtons |= INPUT_MOUSE_BUTTON_LEFT;
            }
        }
        return;
    }

    if (s_frontTouchActive) {
        if (s_frontTwoFinger) {
            // Very short two-finger contacts may otherwise miss a frame of
            // right-button state; guarantee a one-frame click on release.
            s_rightClickPulse = 1;
        } else if (!s_frontDragging) {
            s_leftClickPulse = 1;
        }
    }

    s_frontTouchActive = false;
    s_frontDragging = false;
    s_frontTwoFinger = false;
    s_frontTouchFrames = 0;
}

static void update_rear_touch_wheel(void)
{
    if (s_touchDataBack.reportNum <= 0) {
        s_rearTouchActive = false;
        s_rearWheelAccum = 0;
        return;
    }

    const int x = (int)s_touchDataBack.report[0].x;
    const int y = (int)s_touchDataBack.report[0].y;
    const int center_x = VITA_TOUCH_WIDTH / 2;

    if (!s_rearTouchActive) {
        s_rearTouchActive = true;
        s_rearLastY = y;
        s_rearWheelAccum = 0;
        return;
    }

    // Keep wheel gestures in the middle band so the outer rear-pad zones can
    // remain dedicated to camera movement.
    if (abs(x - center_x) < VITA_REAR_EDGE_X) {
        s_rearWheelAccum += y - s_rearLastY;
        while (s_rearWheelAccum >= VITA_REAR_WHEEL_THRESHOLD) {
            s_wheelPulses--;
            s_rearWheelAccum -= VITA_REAR_WHEEL_THRESHOLD;
        }
        while (s_rearWheelAccum <= -VITA_REAR_WHEEL_THRESHOLD) {
            s_wheelPulses++;
            s_rearWheelAccum += VITA_REAR_WHEEL_THRESHOLD;
        }
    } else {
        s_rearWheelAccum = 0;
    }

    s_rearLastY = y;
}

static void update_cursor_from_left_stick(void)
{
    int lx = (int)s_padData.lx - 128;
    int ly = (int)s_padData.ly - 128;

    if (abs(lx) < VITA_STICK_DEADZONE) lx = 0;
    if (abs(ly) < VITA_STICK_DEADZONE) ly = 0;

    if (lx == 0 && ly == 0) return;

    // Non-linear-ish speed without floats: fine movement around centre,
    // noticeably faster movement near the rim.
    int step_x = lx / 24;
    int step_y = ly / 24;
    if (abs(lx) > 90) step_x += lx / 32;
    if (abs(ly) > 90) step_y += ly / 32;

    s_mouseX = clamp_int(s_mouseX + step_x, 0, VITA_SCREEN_WIDTH - 1);
    s_mouseY = clamp_int(s_mouseY + step_y, 0, VITA_SCREEN_HEIGHT - 1);
}

static void update_physical_mouse_buttons(void)
{
    if (s_padData.buttons & SCE_CTRL_CROSS) {
        s_mouseButtons |= INPUT_MOUSE_BUTTON_LEFT;
    }
    if (s_padData.buttons & SCE_CTRL_CIRCLE) {
        s_mouseButtons |= INPUT_MOUSE_BUTTON_RIGHT;
    }
}

static void apply_click_pulses(void)
{
    if (s_leftClickPulse > 0) {
        s_mouseButtons |= INPUT_MOUSE_BUTTON_LEFT;
        s_leftClickPulse--;
    }
    if (s_rightClickPulse > 0) {
        s_mouseButtons |= INPUT_MOUSE_BUTTON_RIGHT;
        s_rightClickPulse--;
    }
}

/******************************************************************************/

static void input_vita_poll_events(void)
{
    sceCtrlPeekBufferPositive(0, &s_padData, 1);
    sceTouchPeek(SCE_TOUCH_PORT_FRONT, &s_touchDataFront, 1);
    sceTouchPeek(SCE_TOUCH_PORT_BACK, &s_touchDataBack, 1);

    update_rear_touch_wheel();
    update_key_states();

    s_mouseButtons = 0;
    update_front_touch();
    if (!s_frontTouchActive) {
        update_cursor_from_left_stick();
    }
    update_physical_mouse_buttons();
    apply_click_pulses();
}

static TbBool input_vita_is_key_down(int keycode)
{
    if (keycode < 0 || keycode >= KC_LIST_END) return false;
    return s_keyState[keycode];
}

static void input_vita_get_mouse(int* x, int* y, int* buttons)
{
    if (x != NULL) *x = s_mouseX;
    if (y != NULL) *y = s_mouseY;
    if (buttons != NULL) *buttons = s_mouseButtons;
}

void vita_get_virtual_cursor(int* x, int* y)
{
    if (x != NULL) *x = s_mouseX;
    if (y != NULL) *y = s_mouseY;
}

void vita_get_virtual_mouse(int* x, int* y, int* buttons)
{
    if (x != NULL) *x = s_mouseX;
    if (y != NULL) *y = s_mouseY;
    if (buttons != NULL) *buttons = s_mouseButtons;
}

int vita_consume_virtual_wheel(void)
{
    int pulse = 0;
    if (s_wheelPulses > 0) {
        pulse = 1;
        s_wheelPulses--;
    } else if (s_wheelPulses < 0) {
        pulse = -1;
        s_wheelPulses++;
    }
    return pulse;
}

static TbBool input_vita_get_gamepad_axis(int axis, int* value)
{
    if (value == NULL) return false;

    int raw_value = 0;
    switch (axis) {
        case 0: raw_value = (int)s_padData.lx - 128; break;
        case 1: raw_value = -((int)s_padData.ly - 128); break;
        case 2: raw_value = (int)s_padData.rx - 128; break;
        case 3: raw_value = -((int)s_padData.ry - 128); break;
        default:
            *value = 0;
            return false;
    }

    if (abs(raw_value) < VITA_STICK_DEADZONE) raw_value = 0;
    *value = raw_value * 256;
    return true;
}

static InputInterface input_vita_impl = {
    input_vita_poll_events,
    input_vita_is_key_down,
    input_vita_get_mouse,
    input_vita_get_gamepad_axis,
};

void input_vita_initialize(void)
{
    sceCtrlSetSamplingMode(SCE_CTRL_MODE_ANALOG);
    sceTouchSetSamplingState(SCE_TOUCH_PORT_FRONT, SCE_TOUCH_SAMPLING_STATE_START);
    sceTouchSetSamplingState(SCE_TOUCH_PORT_BACK, SCE_TOUCH_SAMPLING_STATE_START);

    memset(&s_padData, 0, sizeof(s_padData));
    memset(&s_touchDataFront, 0, sizeof(s_touchDataFront));
    memset(&s_touchDataBack, 0, sizeof(s_touchDataBack));
    memset(s_keyState, 0, sizeof(s_keyState));

    s_mouseX = VITA_SCREEN_WIDTH / 2;
    s_mouseY = VITA_SCREEN_HEIGHT / 2;
    s_mouseButtons = 0;
    s_wheelPulses = 0;
    s_frontTouchActive = false;
    s_frontDragging = false;
    s_frontTwoFinger = false;
    s_leftClickPulse = 0;
    s_rightClickPulse = 0;
    s_rearTouchActive = false;

    g_input = &input_vita_impl;
}

/******************************************************************************/
#ifdef __cplusplus
}
#endif

#endif // PLATFORM_VITA
