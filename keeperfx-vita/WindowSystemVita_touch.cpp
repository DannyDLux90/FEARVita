/******************************************************************************/
// Dungeon Keeper - Platform Abstraction Layer
/******************************************************************************/
/** @file WindowSystemVita.cpp
 *     PS Vita window-system implementation of IWindowSystem.
 * @par Purpose:
 *     Bridges the Vita virtual pointer/touch state to KeeperFX's mouse event
 *     handler.  This includes movement, button transitions and mouse wheel.
 */
/******************************************************************************/
#ifdef PLATFORM_VITA

#include "kfx_memory.h"
#include "pre_inc.h"
#include "platform/WindowSystemVita.h"
#include "bflib_planar.h"
#include "bflib_mouse.h"
#include "bflib_video.h"
#include "input/input_interface.h"
#include "post_inc.h"

extern "C" void vita_get_virtual_mouse(int* x, int* y, int* buttons);
extern "C" int vita_consume_virtual_wheel(void);
extern "C" void mouseControl(unsigned int action, struct TbPoint* pos);

static int s_prevMouseButtons = 0;

static void vita_emit_button_transition(int previous, int current, int mask,
                                        unsigned int down_action,
                                        unsigned int up_action)
{
    const bool was_down = (previous & mask) != 0;
    const bool is_down = (current & mask) != 0;
    if (was_down == is_down) return;

    // mouseControl expects a movement delta, not an absolute coordinate, for
    // button events.  Keep it zero because the cursor was already moved first.
    struct TbPoint zero_delta;
    zero_delta.x = 0;
    zero_delta.y = 0;
    mouseControl(is_down ? down_action : up_action, &zero_delta);
}

void WindowSystemVita::PollInput()
{
    int new_x = 0;
    int new_y = 0;
    int buttons = 0;
    vita_get_virtual_mouse(&new_x, &new_y, &buttons);

    struct TbPoint delta;
    delta.x = new_x - lbMouse.MMouseX;
    delta.y = new_y - lbMouse.MMouseY;

    if (delta.x != 0 || delta.y != 0) {
        mouseControl(MActn_MOUSEMOVE, &delta);
    }

    vita_emit_button_transition(s_prevMouseButtons, buttons,
                                INPUT_MOUSE_BUTTON_LEFT,
                                MActn_LBUTTONDOWN, MActn_LBUTTONUP);
    vita_emit_button_transition(s_prevMouseButtons, buttons,
                                INPUT_MOUSE_BUTTON_RIGHT,
                                MActn_RBUTTONDOWN, MActn_RBUTTONUP);
    vita_emit_button_transition(s_prevMouseButtons, buttons,
                                INPUT_MOUSE_BUTTON_MIDDLE,
                                MActn_MBUTTONDOWN, MActn_MBUTTONUP);
    s_prevMouseButtons = buttons;

    const int wheel = vita_consume_virtual_wheel();
    if (wheel != 0) {
        struct TbPoint zero_delta;
        zero_delta.x = 0;
        zero_delta.y = 0;
        mouseControl(wheel > 0 ? MActn_WHEELMOVEUP : MActn_WHEELMOVEDOWN,
                     &zero_delta);
    }
}

#endif // PLATFORM_VITA
