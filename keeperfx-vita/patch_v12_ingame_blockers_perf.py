from pathlib import Path


def replace_once(text, old, new, name):
    if old not in text:
        raise SystemExit(f'v12 patch: pattern not found: {name}')
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# 1) Fix Vita gpGame static-init crash in Computer Assist / Autopilot.
# ---------------------------------------------------------------------------
p = Path('src/gui_frontbtns.h')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    'void reset_tend_buttons(struct GuiMenu *gmnu);\n',
    'void reset_tend_buttons(struct GuiMenu *gmnu);\nvoid reset_autopilot_buttons(struct GuiMenu *gmnu);\n',
    'autopilot reset declaration')
p.write_text(s, encoding='utf-8')

p = Path('src/gui_frontbtns.c')
s = p.read_text(encoding='utf-8')
anchor = 'void gui_set_menu_mode(struct GuiButton *gbtn)\n'
if anchor not in s:
    raise SystemExit('v12 patch: gui_set_menu_mode anchor missing')
helper = r'''void reset_autopilot_buttons(struct GuiMenu *gmnu)
{
    // Vita allocates gpGame after C/C++ static initialisation. The four
    // &game.comp_player_* pointers in autopilot_menu_buttons therefore contain
    // field offsets, not valid runtime addresses, until we repair them here.
    // GuiMenu::create_cb runs immediately before create_button(), which is the
    // first place these pointers are dereferenced.
    for (int i = 0; gmnu->buttons[i].gbtype != -1; i++)
    {
        struct GuiButtonInit *btn = &gmnu->buttons[i];
        if ((btn->gbtype != LbBtnT_RadioBtn) || (btn->click_event != gui_set_autopilot))
            continue;
        switch (btn->btype_value)
        {
        case 0: btn->content.ptr = &game.comp_player_aggressive;  break;
        case 1: btn->content.ptr = &game.comp_player_defensive;   break;
        case 2: btn->content.ptr = &game.comp_player_construct;   break;
        case 3: btn->content.ptr = &game.comp_player_creatrsonly; break;
        default: break;
        }
    }
}

'''
s = s.replace(anchor, helper + anchor, 1)
p.write_text(s, encoding='utf-8')

p = Path('src/frontmenu_ingame_opts_data.cpp')
s = p.read_text(encoding='utf-8')
old = '{ GMnu_AUTOPILOT,    0, 4, autopilot_menu_buttons,     POS_GAMECTR,POS_GAMECTR,224, 120, gui_pretty_background,       0, NULL,    NULL,                    0, 1, 0,};'
new = '{ GMnu_AUTOPILOT,    0, 4, autopilot_menu_buttons,     POS_GAMECTR,POS_GAMECTR,224, 120, gui_pretty_background,       0, NULL,    reset_autopilot_buttons, 0, 1, 0,};'
s = replace_once(s, old, new, 'autopilot runtime create callback')
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 2) Recover stale level-start input locks on Vita only.
#    The lock bits are legitimate while an instance/fade is active. They are
#    impossible/contradictory once we are back in DungeonTop with PI_Unset.
# ---------------------------------------------------------------------------
p = Path('src/front_input.c')
s = p.read_text(encoding='utf-8')
anchor = '''/** Fill packet struct with game action information.\n */\nstatic short get_inputs(void)\n{\n'''
if anchor not in s:
    raise SystemExit('v12 patch: get_inputs anchor missing')
helper = r'''#ifdef PLATFORM_VITA
static void vita_recover_stale_ingame_input_lock(struct PlayerInfo *player)
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
#endif

'''
s = s.replace(anchor, helper + anchor, 1)
old = '''    struct PlayerInfo* player = get_my_player();\n    if ((player->allocflags & PlaF_MouseInputDisabled) != 0)\n'''
new = '''    struct PlayerInfo* player = get_my_player();\n#ifdef PLATFORM_VITA\n    vita_recover_stale_ingame_input_lock(player);\n#endif\n    if ((player->allocflags & PlaF_MouseInputDisabled) != 0)\n'''
s = replace_once(s, old, new, 'stale lock recovery call')
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 3) Vita CPU topology: isolate the main loop from audio/stream workers.
#    Vita exposes three user cores; the fourth Cortex-A9 core is system-only.
# ---------------------------------------------------------------------------
p = Path('src/platform/PlatformVita.cpp')
s = p.read_text(encoding='utf-8')
inc = '#include <psp2/kernel/threadmgr.h>\n'
if inc not in s:
    raise SystemExit('v12 patch: PlatformVita threadmgr include missing')
if '#include <psp2/kernel/cpu.h>\n' not in s:
    s = s.replace(inc, inc + '#include <psp2/kernel/cpu.h>\n', 1)

clock_anchor = '''    scePowerSetGpuXbarClockFrequency(166);\n    _SYSI_LOG("clks-done");\n'''
clock_new = '''    scePowerSetGpuXbarClockFrequency(166);\n    _SYSI_LOG("clks-done");\n\n    // Keep the CPU-heavy game simulation + software rasterizer on USER_0.\n    // Audio workers are pinned to USER_1/USER_2 in audio_vita.c, preventing\n    // their decoder/mixer bursts from stealing time from frame production.\n    if (sceKernelChangeThreadCpuAffinityMask(sceKernelGetThreadId(),\n                                              SCE_KERNEL_CPU_MASK_USER_0) < 0)\n        _SYSI_LOG("main-affinity-failed");\n    else\n        _SYSI_LOG("main-affinity-user0");\n'''
s = replace_once(s, clock_anchor, clock_new, 'main thread user-core affinity')
p.write_text(s, encoding='utf-8')

p = Path('src/audio/audio_vita.c')
s = p.read_text(encoding='utf-8')
inc = '#include <psp2/kernel/threadmgr.h>\n'
if inc not in s:
    raise SystemExit('v12 patch: audio threadmgr include missing')
if '#include <psp2/kernel/cpu.h>\n' not in s:
    s = s.replace(inc, inc + '#include <psp2/kernel/cpu.h>\n', 1)

# One helper avoids changing the control-flow of existing if(thread>=0) sites.
insert_anchor = '/* ── Constants '
idx = s.find(insert_anchor)
if idx < 0:
    raise SystemExit('v12 patch: audio constants anchor missing')
thread_helper = r'''static void vita_start_thread_on_core(SceUID thread, int affinity_mask, const char *name)
{
    int ret = sceKernelChangeThreadCpuAffinityMask(thread, affinity_mask);
    if (ret < 0)
        WARNLOG("vita audio: affinity %s failed (0x%08X)", name, (unsigned int)ret);
    sceKernelStartThread(thread, 0, NULL);
}

'''
if 'vita_start_thread_on_core' not in s:
    s = s[:idx] + thread_helper + s[idx:]

replacements = {
    'sceKernelStartThread(s_dma_thread, 0, NULL);':
        'vita_start_thread_on_core(s_dma_thread, SCE_KERNEL_CPU_MASK_USER_1, "dma");',
    'sceKernelStartThread(s_music_thread, 0, NULL);':
        'vita_start_thread_on_core(s_music_thread, SCE_KERNEL_CPU_MASK_USER_2, "music");',
    'sceKernelStartThread(s_fmv_thread, 0, NULL);':
        'vita_start_thread_on_core(s_fmv_thread, SCE_KERNEL_CPU_MASK_USER_1, "fmv");',
}
for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f'v12 patch: audio thread start missing: {old}')
    s = s.replace(old, new)
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 4) Present on vblank for stable pacing. The old GL_FALSE path presented as
#    soon as possible, which maximises throughput but produces uneven cadence
#    and tearing when the CPU software renderer fluctuates around a refresh.
# ---------------------------------------------------------------------------
p = Path('src/renderer/RendererVita.cpp')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    '        vglSwapBuffers(GL_FALSE);\n',
    '''        // Synchronise presentation to the Vita display. Game logic remains\n        // time based; this only removes uneven/tearing presentation cadence.\n        vglSwapBuffers(GL_TRUE);\n''',
    'Vita vblank paced swap')
p.write_text(s, encoding='utf-8')

# ---------------------------------------------------------------------------
# 5) Static correctness gates for the game-side input bridge inherited from v8/v9.
# ---------------------------------------------------------------------------
p = Path('src/kjm_input.c')
s = p.read_text(encoding='utf-8')
for required in (
    'lbDisplay.MLeftButton  = btn_left;',
    'lbDisplay.MRightButton = btn_right;',
    'g_input->get_mouse(&ix, &iy, &ibuttons);',
):
    if required not in s:
        raise SystemExit(f'v12 patch: Vita in-game mouse bridge missing: {required}')

print('v12 Vita blockers/performance patch applied')
