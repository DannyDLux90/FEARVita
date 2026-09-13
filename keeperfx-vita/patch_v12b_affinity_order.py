from pathlib import Path

p = Path('src/platform/PlatformVita.cpp')
s = p.read_text(encoding='utf-8')

old = '''    // Keep the CPU-heavy game simulation + software rasterizer on USER_0.\n    // Audio workers are pinned to USER_1/USER_2 in audio_vita.c, preventing\n    // their decoder/mixer bursts from stealing time from frame production.\n    if (sceKernelChangeThreadCpuAffinityMask(sceKernelGetThreadId(),\n                                              SCE_KERNEL_CPU_MASK_USER_0) < 0)\n        _SYSI_LOG("main-affinity-failed");\n    else\n        _SYSI_LOG("main-affinity-user0");\n'''
if old not in s:
    raise SystemExit('v12b: early SystemInit affinity block missing')
s = s.replace(old, '', 1)

anchor = '''    SDL_Init(SDL_INIT_JOYSTICK | SDL_INIT_GAMECONTROLLER);\n    atexit(SDL_Quit);\n    _VGL_LOG("VideoInit:sdl")\n'''
new = '''    SDL_Init(SDL_INIT_JOYSTICK | SDL_INIT_GAMECONTROLLER);\n    atexit(SDL_Quit);\n    _VGL_LOG("VideoInit:sdl")\n\n    // Pin KeeperFX itself only after vitaGL/SDL have created any helper threads.\n    // Otherwise those threads could inherit USER_0 and compete with the\n    // software renderer. Audio workers are explicitly placed on USER_1/USER_2.\n    if (sceKernelChangeThreadCpuAffinityMask(sceKernelGetThreadId(),\n                                              SCE_KERNEL_CPU_MASK_USER_0) < 0)\n        _VGL_LOG("VideoInit:main-affinity-failed")\n    else\n        _VGL_LOG("VideoInit:main-affinity-user0")\n'''
if anchor not in s:
    raise SystemExit('v12b: SDL VideoInit anchor missing')
s = s.replace(anchor, new, 1)

p.write_text(s, encoding='utf-8')
print('v12b affinity order fix applied')
