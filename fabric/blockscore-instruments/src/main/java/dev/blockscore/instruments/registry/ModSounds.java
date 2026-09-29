package dev.blockscore.instruments.registry;

import dev.blockscore.instruments.BlockScoreInstruments;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvent;

public final class ModSounds {
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
