#pragma once
#ifdef PLATFORM_VITA

#include <psp2/apputil.h>
#include <psp2/display.h>
#include <psp2/io/fcntl.h>
#include <psp2/io/stat.h>
#include <psp2/kernel/processmgr.h>
#include <psp2/kernel/sysmem.h>
#include <minizip/unzip.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <vector>
#include <new>

namespace kfx_vita_bootstrap {

static bool g_apputil_initialized = false;
static const char *kDataRoot = "ux0:data/keeperfx";
static const char *kBundlePath = "app0:/game_data/keeperfx_data_bundle.zip";
static const char *kMarkerPath = "ux0:data/keeperfx/.keeperfx_vita_data_v3";
static const char *kLogPath = "ux0:data/keeperfx/vita_install.log";

// A tiny direct-framebuffer loader is used before SDL/vitaGL are initialized.
// This makes the one-time ~500 MB data extraction visible instead of leaving
// the user on a black screen for the duration of the install.
static const int kLoaderWidth = 960;
static const int kLoaderHeight = 544;
static const int kLoaderPitch = 1024;
static SceUID g_loader_memblock = -1;
static uint32_t *g_loader_pixels = NULL;

static void log_line(const char *msg)
{
    FILE *f = fopen(kLogPath, "a");
    if (f) {
        fprintf(f, "%s\n", msg);
        fclose(f);
    }
}

static void log_printf(const char *fmt, ...)
{
    char buffer[768];
    va_list args;
    va_start(args, fmt);
    vsnprintf(buffer, sizeof(buffer), fmt, args);
    va_end(args);
    buffer[sizeof(buffer) - 1] = '\0';
    log_line(buffer);
}

static void ensure_data_root()
{
    sceIoMkdir("ux0:data", 0777);
    sceIoMkdir(kDataRoot, 0777);
}

static void loader_fill_rect(int x, int y, int w, int h, uint32_t color)
{
    if (!g_loader_pixels || w <= 0 || h <= 0)
        return;

    if (x < 0) { w += x; x = 0; }
    if (y < 0) { h += y; y = 0; }
    if (x + w > kLoaderWidth) w = kLoaderWidth - x;
    if (y + h > kLoaderHeight) h = kLoaderHeight - y;
    if (w <= 0 || h <= 0)
        return;

    for (int py = y; py < y + h; ++py) {
        uint32_t *row = g_loader_pixels + py * kLoaderPitch + x;
        for (int px = 0; px < w; ++px)
            row[px] = color;
    }
}

static void loader_draw_progress(unsigned long done, unsigned long total)
{
    if (!g_loader_pixels)
        return;

    if (total == 0)
        total = 1;
    if (done > total)
        done = total;

    const int bar_x = 110;
    const int bar_y = 260;
    const int bar_w = 740;
    const int bar_h = 42;
    const int inner_x = bar_x + 4;
    const int inner_y = bar_y + 4;
    const int inner_w = bar_w - 8;
    const int inner_h = bar_h - 8;
    const int filled = (int)(((unsigned long long)inner_w * done) / total);

    // Dark dungeon-like background with a simple gold frame and light progress.
    loader_fill_rect(0, 0, kLoaderWidth, kLoaderHeight, 0xFF090909u);
    loader_fill_rect(86, 192, 788, 164, 0xFF171717u);
    loader_fill_rect(bar_x, bar_y, bar_w, bar_h, 0xFFB0A060u);
    loader_fill_rect(inner_x, inner_y, inner_w, inner_h, 0xFF282828u);
    if (filled > 0)
        loader_fill_rect(inner_x, inner_y, filled, inner_h, 0xFFE0D0A0u);

    // Small status ornaments so a 0% screen is visibly intentional, not black.
    loader_fill_rect(110, 226, 250, 6, 0xFFB0A060u);
    loader_fill_rect(600, 226, 250, 6, 0xFFB0A060u);
    loader_fill_rect(448, 218, 64, 22, 0xFFE0D0A0u);

    sceKernelPowerTick(SCE_KERNEL_POWER_TICK_DEFAULT);
}

static bool loader_init()
{
    if (g_loader_pixels)
        return true;

    const unsigned int bytes = (unsigned int)(kLoaderPitch * kLoaderHeight * 4);
    g_loader_memblock = sceKernelAllocMemBlock(
        "KeeperFX data loader",
        SCE_KERNEL_MEMBLOCK_TYPE_USER_CDRAM_RW,
        bytes,
        NULL);
    if (g_loader_memblock < 0) {
        log_printf("loader framebuffer allocation failed: 0x%08X", (unsigned int)g_loader_memblock);
        g_loader_memblock = -1;
        return false;
    }

    void *base = NULL;
    int base_rc = sceKernelGetMemBlockBase(g_loader_memblock, &base);
    if (base_rc < 0 || !base) {
        log_printf("loader framebuffer base failed: 0x%08X", (unsigned int)base_rc);
        sceKernelFreeMemBlock(g_loader_memblock);
        g_loader_memblock = -1;
        return false;
    }
    g_loader_pixels = (uint32_t *)base;
    memset(g_loader_pixels, 0, bytes);

    SceDisplayFrameBuf frame;
    memset(&frame, 0, sizeof(frame));
    frame.size = sizeof(frame);
    frame.base = g_loader_pixels;
    frame.pitch = kLoaderPitch;
    frame.pixelformat = SCE_DISPLAY_PIXELFORMAT_A8B8G8R8;
    frame.width = kLoaderWidth;
    frame.height = kLoaderHeight;

    int display_rc = sceDisplaySetFrameBuf(&frame, SCE_DISPLAY_SETBUF_NEXTFRAME);
    if (display_rc < 0) {
        log_printf("loader sceDisplaySetFrameBuf failed: 0x%08X", (unsigned int)display_rc);
        // Keep the allocation alive; the installer can still continue and log.
        return false;
    }

    loader_draw_progress(0, 1);
    sceDisplayWaitVblankStart();
    log_line("loader framebuffer active");
    return true;
}

static bool exists(const char *path)
{
    SceIoStat st;
    memset(&st, 0, sizeof(st));
    return sceIoGetstat(path, &st) >= 0;
}

static long long file_size(const char *path)
{
    SceIoStat st;
    memset(&st, 0, sizeof(st));
    if (sceIoGetstat(path, &st) < 0)
        return -1;
    return (long long)st.st_size;
}

static bool safe_relative_name(const char *name)
{
    if (!name || !*name || name[0] == '/' || name[0] == '\\' || strchr(name, ':') || strchr(name, '\\'))
        return false;

    const char *p = name;
    while (*p) {
        while (*p == '/')
            ++p;
        const char *segment = p;
        while (*p && *p != '/')
            ++p;
        size_t len = (size_t)(p - segment);
        if (len == 2 && segment[0] == '.' && segment[1] == '.')
            return false;
    }
    return true;
}

static void mkdirs_for(const char *full_path, bool final_is_dir)
{
    char tmp[768];
    snprintf(tmp, sizeof(tmp), "%s", full_path);
    size_t len = strlen(tmp);
    for (size_t i = 1; i < len; ++i) {
        if (tmp[i] == '/') {
            tmp[i] = '\0';
            const char *colon = strchr(tmp, ':');
            if (!colon || colon != tmp + strlen(tmp) - 1)
                sceIoMkdir(tmp, 0777);
            tmp[i] = '/';
        }
    }
    if (final_is_dir)
        sceIoMkdir(tmp, 0777);
}

static bool init_apputil()
{
    if (g_apputil_initialized)
        return true;

    SceAppUtilInitParam init_param;
    SceAppUtilBootParam boot_param;
    memset(&init_param, 0, sizeof(init_param));
    memset(&boot_param, 0, sizeof(boot_param));
    if (sceAppUtilInit(&init_param, &boot_param) < 0) {
        log_line("sceAppUtilInit failed");
        return false;
    }
    g_apputil_initialized = true;
    return true;
}

static void shutdown_apputil()
{
    if (g_apputil_initialized) {
        sceAppUtilShutdown();
        g_apputil_initialized = false;
    }
}

static bool deeper_requested()
{
    if (!init_apputil())
        return false;

    SceAppUtilAppEventParam event_param;
    memset(&event_param, 0, sizeof(event_param));
    if (sceAppUtilReceiveAppEvent(&event_param) < 0)
        return false;

    // VitaSDK does not publish a symbolic LIVEAREA event type in apputil.h.
    // Parse the received event directly; non-LiveArea events simply fail here.
    char buffer[2048];
    memset(buffer, 0, sizeof(buffer));
    if (sceAppUtilAppEventParseLiveArea(&event_param, buffer) < 0)
        return false;
    buffer[sizeof(buffer) - 1] = '\0';

    return strcmp(buffer, "-deeper") == 0 || strstr(buffer, "-deeper") != NULL;
}

static bool install_bundled_data()
{
    ensure_data_root();

    if (exists(kMarkerPath)) {
        log_line("data marker present; skipping install");
        return true;
    }
    if (!exists(kBundlePath)) {
        log_line("bundled data archive missing");
        return false;
    }

    FILE *log = fopen(kLogPath, "w");
    if (log) {
        fprintf(log, "KeeperFX Vita first-run data install begin\n");
        fclose(log);
    }

    // Present a visible loader before touching the large archive. Failure to
    // create the loader is non-fatal; the detailed file log remains available.
    loader_init();
    loader_draw_progress(0, 100);
    log_line("opening bundled data archive");

    unzFile zf = unzOpen(kBundlePath);
    if (!zf) {
        log_line("unzOpen failed");
        return false;
    }
    log_line("bundled data archive open");

    unz_global_info global_info;
    memset(&global_info, 0, sizeof(global_info));
    unsigned long total_entries = 0;
    int global_rc = unzGetGlobalInfo(zf, &global_info);
    if (global_rc == UNZ_OK) {
        total_entries = global_info.number_entry;
        log_printf("archive entries: %lu", total_entries);
    } else {
        log_printf("unzGetGlobalInfo failed: %d", global_rc);
    }
    if (total_entries == 0)
        total_entries = 1;

    loader_draw_progress(1, total_entries);

    unsigned char *buffer = new(std::nothrow) unsigned char[256 * 1024];
    if (!buffer) {
        unzClose(zf);
        log_line("buffer alloc failed");
        return false;
    }
    log_line("copy buffer allocated");

    bool ok = true;
    unsigned long entries_done = 0;
    unsigned long files_done = 0;
    int rc = unzGoToFirstFile(zf);
    if (rc != UNZ_OK)
        log_printf("unzGoToFirstFile failed: %d", rc);

    while (rc == UNZ_OK) {
        unz_file_info info;
        char name[512];
        memset(&info, 0, sizeof(info));
        memset(name, 0, sizeof(name));

        int info_rc = unzGetCurrentFileInfo(zf, &info, name, sizeof(name) - 1, NULL, 0, NULL, 0);
        if (info_rc != UNZ_OK) {
            log_printf("unzGetCurrentFileInfo failed at entry %lu: %d", entries_done, info_rc);
            ok = false;
            break;
        }
        if (!safe_relative_name(name)) {
            log_printf("unsafe path in data archive: %s", name);
            ok = false;
            break;
        }

        size_t name_len = strlen(name);
        bool is_dir = name_len > 0 && name[name_len - 1] == '/';
        char dest[768];
        snprintf(dest, sizeof(dest), "%s/%s", kDataRoot, name);
        mkdirs_for(dest, is_dir);

        if (!is_dir) {
            long long existing = file_size(dest);
            if (existing != (long long)info.uncompressed_size) {
                int open_rc = unzOpenCurrentFile(zf);
                if (open_rc != UNZ_OK) {
                    log_printf("unzOpenCurrentFile failed: %s rc=%d", name, open_rc);
                    ok = false;
                    break;
                }

                char tmp[800];
                snprintf(tmp, sizeof(tmp), "%s.kfxvita.tmp", dest);
                FILE *out = fopen(tmp, "wb");
                if (!out) {
                    log_printf("could not create output: %s", tmp);
                    unzCloseCurrentFile(zf);
                    ok = false;
                    break;
                }

                unsigned long long file_written = 0;
                for (;;) {
                    int got = unzReadCurrentFile(zf, buffer, 256 * 1024);
                    if (got < 0) {
                        log_printf("read failed: %s rc=%d after %llu bytes", name, got, file_written);
                        ok = false;
                        break;
                    }
                    if (got == 0)
                        break;
                    if (fwrite(buffer, 1, (size_t)got, out) != (size_t)got) {
                        log_printf("write failed: %s after %llu bytes", tmp, file_written);
                        ok = false;
                        break;
                    }
                    file_written += (unsigned long long)got;
                    sceKernelPowerTick(SCE_KERNEL_POWER_TICK_DEFAULT);
                }
                fclose(out);

                int close_rc = unzCloseCurrentFile(zf);
                if (!ok || close_rc != UNZ_OK) {
                    if (close_rc != UNZ_OK)
                        log_printf("unzCloseCurrentFile failed: %s rc=%d", name, close_rc);
                    sceIoRemove(tmp);
                    ok = false;
                    break;
                }

                sceIoRemove(dest);
                int rename_rc = sceIoRename(tmp, dest);
                if (rename_rc < 0) {
                    log_printf("rename failed: %s -> %s rc=0x%08X", tmp, dest, (unsigned int)rename_rc);
                    sceIoRemove(tmp);
                    ok = false;
                    break;
                }
            }

            ++files_done;
        }

        ++entries_done;
        if ((entries_done & 0x0F) == 0 || entries_done == total_entries) {
            loader_draw_progress(entries_done, total_entries);
            if ((entries_done & 0x7F) == 0 || entries_done == total_entries)
                log_printf("progress: entries=%lu/%lu files=%lu current=%s", entries_done, total_entries, files_done, name);
        }

        rc = unzGoToNextFile(zf);
    }

    delete[] buffer;
    unzClose(zf);

    if (ok && rc == UNZ_END_OF_LIST_OF_FILE) {
        loader_draw_progress(total_entries, total_entries);
        FILE *marker = fopen(kMarkerPath, "wb");
        if (!marker) {
            log_line("could not write data marker");
            return false;
        }
        fprintf(marker, "KeeperFX Vita data v3\n");
        fclose(marker);
        log_printf("first-run data install complete: entries=%lu files=%lu", entries_done, files_done);
        return true;
    }

    log_printf("first-run data install failed; rc=%d entries=%lu files=%lu; next start will resume", rc, entries_done, files_done);
    return false;
}

static int run_kfxmain(int argc, char **argv, bool deeper)
{
    if (!deeper)
        return kfxmain(argc, argv);

    std::vector<char *> args;
    for (int i = 0; i < argc; ++i)
        args.push_back(argv[i]);

    static char fallback_argv0[] = "keeperfx";
    static char flag[] = "-vitadeeper";
    if (args.empty())
        args.push_back(fallback_argv0);
    args.push_back(flag);
    args.push_back(NULL);

    log_line("LiveArea direct start: Deeper Dungeons map-pack selector");
    return kfxmain((int)args.size() - 1, args.data());
}

} // namespace kfx_vita_bootstrap
#endif
