package dev.blockscore.instruments.registry;

import dev.blockscore.instruments.BlockScoreInstruments;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvent;

public final class ModSounds {
    public static final SoundEvent GUITAR_NYLON =
            register("block.note_block.guitar_nylon");
    public static final SoundEvent GUITAR_NYLON_M40 = register("block.note_block.guitar_nylon.m40");
    public static final SoundEvent GUITAR_NYLON_M45 = register("block.note_block.guitar_nylon.m45");
    public static final SoundEvent GUITAR_NYLON_M50 = register("block.note_block.guitar_nylon.m50");
    public static final SoundEvent GUITAR_NYLON_M55 = register("block.note_block.guitar_nylon.m55");
    public static final SoundEvent GUITAR_NYLON_M59 = register("block.note_block.guitar_nylon.m59");
    public static final SoundEvent GUITAR_NYLON_M64 = register("block.note_block.guitar_nylon.m64");
    public static final SoundEvent GUITAR_NYLON_M69 = register("block.note_block.guitar_nylon.m69");
    public static final SoundEvent GUITAR_NYLON_M76 = register("block.note_block.guitar_nylon.m76");

    public static final SoundEvent GUITAR_NATURAL_HARMONIC =
            register("block.note_block.guitar_natural_harmonic");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N00 = register("block.note_block.guitar_natural_harmonic.n00");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N03 = register("block.note_block.guitar_natural_harmonic.n03");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N08 = register("block.note_block.guitar_natural_harmonic.n08");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N13 = register("block.note_block.guitar_natural_harmonic.n13");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N17 = register("block.note_block.guitar_natural_harmonic.n17");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N22 = register("block.note_block.guitar_natural_harmonic.n22");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N24 = register("block.note_block.guitar_natural_harmonic.n24");

    public static final SoundEvent GUITAR_TAPPED_HARMONIC =
            register("block.note_block.guitar_tapped_harmonic");
    public static final SoundEvent GUITAR_TAPPED_HARMONIC_N00 = register("block.note_block.guitar_tapped_harmonic.n00");
    public static final SoundEvent GUITAR_TAPPED_HARMONIC_N03 = register("block.note_block.guitar_tapped_harmonic.n03");
    public static final SoundEvent GUITAR_TAPPED_HARMONIC_N08 = register("block.note_block.guitar_tapped_harmonic.n08");
    public static final SoundEvent GUITAR_TAPPED_HARMONIC_N13 = register("block.note_block.guitar_tapped_harmonic.n13");
    public static final SoundEvent GUITAR_TAPPED_HARMONIC_N17 = register("block.note_block.guitar_tapped_harmonic.n17");
    public static final SoundEvent GUITAR_TAPPED_HARMONIC_N22 = register("block.note_block.guitar_tapped_harmonic.n22");
    public static final SoundEvent GUITAR_TAPPED_HARMONIC_N24 = register("block.note_block.guitar_tapped_harmonic.n24");

    public static final SoundEvent GUITAR_DEAD_NOTE =
            register("block.note_block.guitar_dead_note");
    public static final SoundEvent GUITAR_DEAD_NOTE_LOW =
            register("block.note_block.guitar_dead_note.low");
    public static final SoundEvent GUITAR_DEAD_NOTE_MID =
            register("block.note_block.guitar_dead_note.mid");
    public static final SoundEvent GUITAR_DEAD_NOTE_HIGH =
            register("block.note_block.guitar_dead_note.high");

    public static final SoundEvent GUITAR_STEEL_CLEAN = register("block.note_block.guitar_steel_clean");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M40 = register("block.note_block.guitar_steel_clean.m40");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M45 = register("block.note_block.guitar_steel_clean.m45");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M50 = register("block.note_block.guitar_steel_clean.m50");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M55 = register("block.note_block.guitar_steel_clean.m55");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M59 = register("block.note_block.guitar_steel_clean.m59");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M64 = register("block.note_block.guitar_steel_clean.m64");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M69 = register("block.note_block.guitar_steel_clean.m69");
    public static final SoundEvent GUITAR_STEEL_CLEAN_M76 = register("block.note_block.guitar_steel_clean.m76");

    public static final SoundEvent GUITAR_DISTORTED = register("block.note_block.guitar_distorted");
    public static final SoundEvent GUITAR_DISTORTED_M40 = register("block.note_block.guitar_distorted.m40");
    public static final SoundEvent GUITAR_DISTORTED_M45 = register("block.note_block.guitar_distorted.m45");
    public static final SoundEvent GUITAR_DISTORTED_M50 = register("block.note_block.guitar_distorted.m50");
    public static final SoundEvent GUITAR_DISTORTED_M55 = register("block.note_block.guitar_distorted.m55");
    public static final SoundEvent GUITAR_DISTORTED_M59 = register("block.note_block.guitar_distorted.m59");
    public static final SoundEvent GUITAR_DISTORTED_M64 = register("block.note_block.guitar_distorted.m64");
    public static final SoundEvent GUITAR_DISTORTED_M69 = register("block.note_block.guitar_distorted.m69");
    public static final SoundEvent GUITAR_DISTORTED_M76 = register("block.note_block.guitar_distorted.m76");

    public static final SoundEvent GUITAR_PALM_MUTE = register("block.note_block.guitar_palm_mute");
    public static final SoundEvent GUITAR_PALM_MUTE_M40 = register("block.note_block.guitar_palm_mute.m40");
    public static final SoundEvent GUITAR_PALM_MUTE_M45 = register("block.note_block.guitar_palm_mute.m45");
    public static final SoundEvent GUITAR_PALM_MUTE_M50 = register("block.note_block.guitar_palm_mute.m50");
    public static final SoundEvent GUITAR_PALM_MUTE_M55 = register("block.note_block.guitar_palm_mute.m55");
    public static final SoundEvent GUITAR_PALM_MUTE_M59 = register("block.note_block.guitar_palm_mute.m59");
    public static final SoundEvent GUITAR_PALM_MUTE_M64 = register("block.note_block.guitar_palm_mute.m64");
    public static final SoundEvent GUITAR_PALM_MUTE_M69 = register("block.note_block.guitar_palm_mute.m69");
    public static final SoundEvent GUITAR_PALM_MUTE_M76 = register("block.note_block.guitar_palm_mute.m76");

    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC = register("block.note_block.guitar_artificial_harmonic");
    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC_M54 = register("block.note_block.guitar_artificial_harmonic.m54");
    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC_M57 = register("block.note_block.guitar_artificial_harmonic.m57");
    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC_M62 = register("block.note_block.guitar_artificial_harmonic.m62");
    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC_M67 = register("block.note_block.guitar_artificial_harmonic.m67");
    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC_M71 = register("block.note_block.guitar_artificial_harmonic.m71");
    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC_M76 = register("block.note_block.guitar_artificial_harmonic.m76");
    public static final SoundEvent GUITAR_ARTIFICIAL_HARMONIC_M78 = register("block.note_block.guitar_artificial_harmonic.m78");

    public static final SoundEvent GUITAR_PINCH_HARMONIC = register("block.note_block.guitar_pinch_harmonic");
    public static final SoundEvent GUITAR_PINCH_HARMONIC_M66 = register("block.note_block.guitar_pinch_harmonic.m66");
    public static final SoundEvent GUITAR_PINCH_HARMONIC_M69 = register("block.note_block.guitar_pinch_harmonic.m69");
    public static final SoundEvent GUITAR_PINCH_HARMONIC_M74 = register("block.note_block.guitar_pinch_harmonic.m74");
    public static final SoundEvent GUITAR_PINCH_HARMONIC_M79 = register("block.note_block.guitar_pinch_harmonic.m79");
    public static final SoundEvent GUITAR_PINCH_HARMONIC_M83 = register("block.note_block.guitar_pinch_harmonic.m83");
    public static final SoundEvent GUITAR_PINCH_HARMONIC_M88 = register("block.note_block.guitar_pinch_harmonic.m88");
    public static final SoundEvent GUITAR_PINCH_HARMONIC_M90 = register("block.note_block.guitar_pinch_harmonic.m90");

    public static final SoundEvent GUITAR_ACOUSTIC_BODY_HIT = register("block.note_block.guitar_acoustic_body_hit");
    public static final SoundEvent GUITAR_ACOUSTIC_BODY_HIT_LOW = register("block.note_block.guitar_acoustic_body_hit.low");
    public static final SoundEvent GUITAR_ACOUSTIC_BODY_HIT_MID = register("block.note_block.guitar_acoustic_body_hit.mid");
    public static final SoundEvent GUITAR_ACOUSTIC_BODY_HIT_HIGH = register("block.note_block.guitar_acoustic_body_hit.high");

    private ModSounds() {
    }

    private static SoundEvent register(String path) {
        Identifier id = BlockScoreInstruments.id(path);
        return Registry.register(
                BuiltInRegistries.SOUND_EVENT,
                id,
                SoundEvent.createVariableRangeEvent(id)
        );
    }

    public static void initialize() {
    }
}
