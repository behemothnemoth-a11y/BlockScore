package dev.blockscore.instruments.registry;

import dev.blockscore.instruments.BlockScoreInstruments;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvent;

public final class ModSounds {
    public static final SoundEvent GUITAR_NATURAL_HARMONIC =
            register("block.note_block.guitar_natural_harmonic");

    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N00 =
            register("block.note_block.guitar_natural_harmonic.n00");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N04 =
            register("block.note_block.guitar_natural_harmonic.n04");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N08 =
            register("block.note_block.guitar_natural_harmonic.n08");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N12 =
            register("block.note_block.guitar_natural_harmonic.n12");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N16 =
            register("block.note_block.guitar_natural_harmonic.n16");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N20 =
            register("block.note_block.guitar_natural_harmonic.n20");
    public static final SoundEvent GUITAR_NATURAL_HARMONIC_N24 =
            register("block.note_block.guitar_natural_harmonic.n24");

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
