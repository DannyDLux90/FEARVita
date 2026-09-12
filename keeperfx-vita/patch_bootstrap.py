from pathlib import Path

# Patch the Vita homebrew entry point: first-run data install + LiveArea argument.
p = Path('src/platform/PlatformHomebrewMain.cpp')
s = p.read_text(encoding='utf-8')
old = '#include "platform/PlatformVita.h"\n'
new = old + '#include "platform/vita_bootstrap.hpp"\n'
if old not in s:
    raise SystemExit('PlatformHomebrewMain include anchor not found')
s = s.replace(old, new, 1)

old = '''int main(int argc, char* argv[]) {
#if defined(PLATFORM_VITA)
    // Create log file before SystemInit so the boot-log writes inside have a file to append to.
    { FILE* _f = fopen("ux0:data/keeperfx/kfx_boot.log", "w"); if (_f) { fprintf(_f, "main-enter\\n"); fclose(_f); } }
#endif
'''
new = '''int main(int argc, char* argv[]) {
#if defined(PLATFORM_VITA)
    kfx_vita_bootstrap::ensure_data_root();
    // Create log file before SystemInit so the boot-log writes inside have a file to append to.
    { FILE* _f = fopen("ux0:data/keeperfx/kfx_boot.log", "w"); if (_f) { fprintf(_f, "main-enter\\n"); fclose(_f); } }
#endif
'''
if old not in s:
    raise SystemExit('PlatformHomebrewMain main anchor not found')
s = s.replace(old, new, 1)

old = '''    PlatformManager::Get()->SystemInit();
    KfxMemInit();

    // Route SDL log output to a file before SDL_Init is called in VideoInit.
'''
new = '''    PlatformManager::Get()->SystemInit();
    KfxMemInit();
#if defined(PLATFORM_VITA)
    if (!kfx_vita_bootstrap::install_bundled_data()) {
        kfx_vita_bootstrap::shutdown_apputil();
        return 24;
    }
    const bool vita_deeper_launch = kfx_vita_bootstrap::deeper_requested();
#endif

    // Route SDL log output to a file before SDL_Init is called in VideoInit.
'''
if old not in s:
    raise SystemExit('PlatformHomebrewMain bootstrap anchor not found')
s = s.replace(old, new, 1)

old = '    return kfxmain(argc, argv);\n'
new = '''#if defined(PLATFORM_VITA)
    int result = kfx_vita_bootstrap::run_kfxmain(argc, argv, vita_deeper_launch);
    kfx_vita_bootstrap::shutdown_apputil();
    return result;
#else
    return kfxmain(argc, argv);
#endif
'''
if old not in s:
    raise SystemExit('PlatformHomebrewMain kfxmain anchor not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

# Patch the main KeeperFX command-line/front-end flow with a Vita-only internal flag.
p = Path('src/main.cpp')
s = p.read_text(encoding='utf-8')
old = 'struct StartupParameters start_params;\n'
new = old + '''#ifdef PLATFORM_VITA
TbBool vita_deeper_direct = false;
#endif
'''
if old not in s:
    raise SystemExit('main.cpp startup-parameters anchor not found')
s = s.replace(old, new, 1)

old = '''      if (strcasecmp(parstr, "nointro") == 0)
      {
        start_params.no_intro = true;
      } else
      if (strcasecmp(parstr, "nocd") == 0)'''
new = '''      if (strcasecmp(parstr, "nointro") == 0)
      {
        start_params.no_intro = true;
      } else
#ifdef PLATFORM_VITA
      if (strcasecmp(parstr, "vitadeeper") == 0)
      {
        vita_deeper_direct = true;
        start_params.no_intro = true;
      } else
#endif
      if (strcasecmp(parstr, "nocd") == 0)'''
if old not in s:
    raise SystemExit('main.cpp command-line anchor not found')
s = s.replace(old, new, 1)

old = '''    if (!load_campaigns_list(&mp_mappacks_list,FGrp_MpLevels,"multiplayer mappacks","mp_mappck_order.txt"))
    {
      WARNMSG("No valid multiplayer mappack files found");
    }
    //Set level number and campaign (for single level mode: GOF_SingleLevel)
'''
new = '''    if (!load_campaigns_list(&mp_mappacks_list,FGrp_MpLevels,"multiplayer mappacks","mp_mappck_order.txt"))
    {
      WARNMSG("No valid multiplayer mappack files found");
    }
#ifdef PLATFORM_VITA
    // A LiveArea Deeper-Dungeons launch selects the real map-pack instead of
    // abusing the campaign command-line option. Keep normal KeeperFX flow once
    // the level selector has been entered.
    if (vita_deeper_direct)
    {
      if (!change_campaign(CampgnT_Mappack, "levels/deepdngn"))
      {
        WARNMSG("Vita direct start could not load Deeper Dungeons map-pack");
        vita_deeper_direct = false;
      }
    }
#endif
    //Set level number and campaign (for single level mode: GOF_SingleLevel)
'''
if old not in s:
    raise SystemExit('main.cpp mappack-list anchor not found')
s = s.replace(old, new, 1)

old = '''    else
    {
        set_selected_level_number(first_singleplayer_level());
    }
    // Init load/save catalogue
'''
new = '''    else
    {
#ifdef PLATFORM_VITA
        if (vita_deeper_direct && campaign.freeplay_levels_count > 0)
            set_selected_level_number(campaign.freeplay_levels[0]);
        else
#endif
            set_selected_level_number(first_singleplayer_level());
    }
    // Init load/save catalogue
'''
if old not in s:
    raise SystemExit('main.cpp initial-level anchor not found')
s = s.replace(old, new, 1)

old = '''    frontend_set_state(get_startup_menu_state());
    try_restore_frontend_error_box();
'''
new = '''#ifdef PLATFORM_VITA
    if (vita_deeper_direct)
    {
        frontend_set_state(FeSt_LEVEL_SELECT);
        vita_deeper_direct = false;
    }
    else
#endif
    {
        frontend_set_state(get_startup_menu_state());
    }
    try_restore_frontend_error_box();
'''
if old not in s:
    raise SystemExit('main.cpp frontend-state anchor not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

# AppUtil is needed for LiveArea launch event parsing.
p = Path('build/cmake/modules/PlatformVita.cmake')
s = p.read_text(encoding='utf-8')
old = 'ScePower_stub SceAudio_stub SceShaccCg_stub SceKernelDmacMgr_stub)'
new = 'ScePower_stub SceAudio_stub SceShaccCg_stub SceKernelDmacMgr_stub SceAppUtil_stub)'
if old not in s:
    raise SystemExit('PlatformVita.cmake stub anchor not found')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
