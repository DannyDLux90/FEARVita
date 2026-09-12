from pathlib import Path

path = Path("src/audio/audio_vita.c")
s = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global s
    if old not in s:
        raise SystemExit(f"patch failed: {label}: expected text not found")
    s = s.replace(old, new, 1)


replace_once(
    "    SoundSmplTblID  smpl_id;\n    SoundBankID     bank_id;\n    SoundMilesID    miles_id;",
    "    SoundSmplTblID  smpl_id;       /* unified KeeperFX sample id */\n"
    "    SoundSmplTblID  bank_smpl_id;  /* local index in Vita bank */\n"
    "    uint8_t         bank_id;       /* 0=sfx, 1=speech; internal only */\n"
    "    SoundMilesID    miles_id;",
    "SwChannel bank fields",
)

old_play_head = '''SoundMilesID play_sample(SoundEmitterID emit_id, SoundSmplTblID smpl_id,
                          SoundVolume vol, SoundPan pan, SoundPitch pitch,
                          char repeats, unsigned char ctype, SoundBankID bank_id)
{
    (void)ctype;
    if (!s_initialized || emit_id <= 0 || smpl_id == 0) return 0;
    if (bank_id >= VITA_NUM_BANKS) return 0;
    if (smpl_id < 0 || smpl_id >= s_sample_counts[bank_id]) return 0;
    VitaSample *smp = &s_samples[bank_id][smpl_id];
    vita_ensure_sample_decoded(bank_id, smpl_id);
    if (!smp->data) return 0;
'''

new_play_head = '''/* Resolve the unified sample-ID space used by current KeeperFX to the two
   physical Vita .dat banks. Runtime custom sounds are not backed by the Vita
   streaming bank yet, so IDs at/after custom_offset fail cleanly. */
static TbBool vita_resolve_sample_id(SoundSmplTblID unified_id,
                                     int *bank_idx,
                                     SoundSmplTblID *bank_smpl_id)
{
    const SoundSmplTblID speech_offset = (SoundSmplTblID)s_sample_counts[0];
    const SoundSmplTblID custom_offset =
        speech_offset + (SoundSmplTblID)s_sample_counts[1];

    if (unified_id <= 0 || unified_id >= custom_offset)
        return false;

    if (unified_id >= speech_offset) {
        *bank_idx = 1;
        *bank_smpl_id = unified_id - speech_offset;
    } else {
        *bank_idx = 0;
        *bank_smpl_id = unified_id;
    }

    return (*bank_smpl_id > 0 &&
            *bank_smpl_id < (SoundSmplTblID)s_sample_counts[*bank_idx]);
}

SoundMilesID play_sample(SoundEmitterID emit_id, SoundSmplTblID smpl_id,
                          SoundVolume vol, SoundPan pan, SoundPitch pitch,
                          char repeats, unsigned char ctype)
{
    (void)ctype;
    if (!s_initialized || emit_id <= 0) return 0;

    int bank_idx = 0;
    SoundSmplTblID bank_smpl_id = 0;
    if (!vita_resolve_sample_id(smpl_id, &bank_idx, &bank_smpl_id)) return 0;

    VitaSample *smp = &s_samples[bank_idx][bank_smpl_id];
    vita_ensure_sample_decoded(bank_idx, bank_smpl_id);
    if (!smp->data) return 0;
'''
replace_once(old_play_head, new_play_head, "play_sample signature/dispatch")

replace_once(
    "    ch->smpl_id    = smpl_id;\n    ch->bank_id    = bank_id;",
    "    ch->smpl_id      = smpl_id;\n"
    "    ch->bank_smpl_id = bank_smpl_id;\n"
    "    ch->bank_id      = (uint8_t)bank_idx;",
    "channel resolved sample",
)

old_stop = '''void stop_sample(SoundEmitterID emit_id, SoundSmplTblID smpl_id, SoundBankID bank_id)
{
    for (int i = 0; i < VITA_MAX_CHANNELS; i++) {
        SwChannel *ch = &s_sw[i];
        if (ch->active && ch->emitter_id == emit_id &&
            ch->smpl_id == smpl_id && ch->bank_id == bank_id)
            ch->active = false;
    }
}
'''
new_stop = '''void stop_sample(SoundEmitterID emit_id, SoundSmplTblID smpl_id)
{
    for (int i = 0; i < VITA_MAX_CHANNELS; i++) {
        SwChannel *ch = &s_sw[i];
        if (ch->active && ch->emitter_id == emit_id && ch->smpl_id == smpl_id)
            ch->active = false;
    }
}
'''
replace_once(old_stop, new_stop, "stop_sample signature")

replace_once(
    "        VitaSample *smp = &s_samples[ch->bank_id][ch->smpl_id];",
    "        VitaSample *smp = &s_samples[ch->bank_id][ch->bank_smpl_id];",
    "SetSamplePitch local index",
)

old_sfx = '''SoundSFXID get_sample_sfxid(SoundSmplTblID smpl_id, SoundBankID bank_id)
{
    if (bank_id >= VITA_NUM_BANKS) return 0;
    if (smpl_id < 0 || smpl_id >= s_sample_counts[bank_id]) return 0;
    return s_samples[bank_id][smpl_id].sfxid;
}
'''
new_sfx = '''SoundSFXID get_sample_sfxid(SoundSmplTblID smpl_id)
{
    int bank_idx = 0;
    SoundSmplTblID bank_smpl_id = 0;
    if (!vita_resolve_sample_id(smpl_id, &bank_idx, &bank_smpl_id)) return 0;
    return s_samples[bank_idx][bank_smpl_id].sfxid;
}

SoundSmplTblID get_speech_offset(void)
{
    return (SoundSmplTblID)s_sample_counts[0];
}

SoundSmplTblID get_custom_offset(void)
{
    return (SoundSmplTblID)(s_sample_counts[0] + s_sample_counts[1]);
}
'''
replace_once(old_sfx, new_sfx, "get_sample_sfxid/offset helpers")

replace_once(
    "    play_sample(1, (SoundSmplTblID)id, (SoundVolume)vol, 64, 100, 0, 2, 0);",
    "    play_sample(1, (SoundSmplTblID)id, (SoundVolume)vol, 64, 100, 0, 2);",
    "AudioInterface play_sample call",
)

path.write_text(s, encoding="utf-8")
print("Patched", path)
