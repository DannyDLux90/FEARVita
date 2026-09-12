from pathlib import Path

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
    // Ensure the runtime root exists before PlatformVita::SystemInit() chdirs into it.
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
    // Install VPK-bundled data once, before KeeperFX opens any runtime assets.
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

p = Path('build/cmake/modules/PlatformVita.cmake')
s = p.read_text(encoding='utf-8')
old = 'ScePower_stub SceAudio_stub SceShaccCg_stub SceKernelDmacMgr_stub)'
new = 'ScePower_stub SceAudio_stub SceShaccCg_stub SceKernelDmacMgr_stub SceAppUtil_stub)'
if old not in s:
    raise SystemExit('PlatformVita.cmake stub anchor not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
