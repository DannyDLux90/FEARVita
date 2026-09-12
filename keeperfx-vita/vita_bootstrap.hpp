#pragma once
#ifdef PLATFORM_VITA

#include <psp2/apputil.h>
#include <psp2/io/fcntl.h>
#include <psp2/io/stat.h>
#include <psp2/kernel/processmgr.h>
#include <minizip/unzip.h>
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

static void log_line(const char *msg)
{
    FILE *f = fopen(kLogPath, "a");
    if (f) {
        fprintf(f, "%s\n", msg);
        fclose(f);
    }
}

static void ensure_data_root()
{
    sceIoMkdir("ux0:data", 0777);
    sceIoMkdir(kDataRoot, 0777);
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

    unzFile zf = unzOpen(kBundlePath);
    if (!zf) {
        log_line("unzOpen failed");
        return false;
    }

    unsigned char *buffer = new(std::nothrow) unsigned char[256 * 1024];
    if (!buffer) {
        unzClose(zf);
        log_line("buffer alloc failed");
        return false;
    }

    bool ok = true;
    unsigned int files_done = 0;
    int rc = unzGoToFirstFile(zf);

    while (rc == UNZ_OK) {
        unz_file_info info;
        char name[512];
        memset(&info, 0, sizeof(info));
        memset(name, 0, sizeof(name));

        if (unzGetCurrentFileInfo(zf, &info, name, sizeof(name) - 1, NULL, 0, NULL, 0) != UNZ_OK) {
            ok = false;
            break;
        }
        if (!safe_relative_name(name)) {
            log_line("unsafe path in data archive");
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
                if (unzOpenCurrentFile(zf) != UNZ_OK) {
                    ok = false;
                    break;
                }

                char tmp[800];
                snprintf(tmp, sizeof(tmp), "%s.kfxvita.tmp", dest);
                FILE *out = fopen(tmp, "wb");
                if (!out) {
                    unzCloseCurrentFile(zf);
                    ok = false;
                    break;
                }

                for (;;) {
                    int got = unzReadCurrentFile(zf, buffer, 256 * 1024);
                    if (got < 0) {
                        ok = false;
                        break;
                    }
                    if (got == 0)
                        break;
                    if (fwrite(buffer, 1, (size_t)got, out) != (size_t)got) {
                        ok = false;
                        break;
                    }
                    sceKernelPowerTick(SCE_KERNEL_POWER_TICK_DEFAULT);
                }
                fclose(out);

                int close_rc = unzCloseCurrentFile(zf);
                if (!ok || close_rc != UNZ_OK) {
                    sceIoRemove(tmp);
                    ok = false;
                    break;
                }

                sceIoRemove(dest);
                if (sceIoRename(tmp, dest) < 0) {
                    sceIoRemove(tmp);
                    ok = false;
                    break;
                }
            }

            ++files_done;
            if ((files_done & 0x7F) == 0)
                sceKernelPowerTick(SCE_KERNEL_POWER_TICK_DEFAULT);
        }

        rc = unzGoToNextFile(zf);
    }

    delete[] buffer;
    unzClose(zf);

    if (ok && rc == UNZ_END_OF_LIST_OF_FILE) {
        FILE *marker = fopen(kMarkerPath, "wb");
        if (!marker) {
            log_line("could not write data marker");
            return false;
        }
        fprintf(marker, "KeeperFX Vita data v3\n");
        fclose(marker);
        log_line("first-run data install complete");
        return true;
    }

    log_line("first-run data install failed; next start will resume");
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
