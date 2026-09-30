package dev.blockscore.instruments.registry;

import dev.blockscore.instruments.BlockScoreInstruments;
import dev.blockscore.instruments.block.GuitarDeadNoteBlock;
import dev.blockscore.instruments.block.GuitarNaturalHarmonicNoteBlock;
import dev.blockscore.instruments.block.GuitarNylonNoteBlock;
import dev.blockscore.instruments.block.GuitarTappedHarmonicNoteBlock;
import dev.blockscore.instruments.block.GuitarSampledNoteBlock;
import dev.blockscore.instruments.block.GuitarBodyHitBlock;
import net.minecraft.sounds.SoundEvent;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;

public final class ModBlocks {

    public static final Block GUITAR_NYLON_LOW_NOTE_BLOCK = registerWithItem(
            "guitar_nylon_low_note_block",
            properties -> new GuitarNylonNoteBlock(properties, 40, 2.65f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_NYLON_HIGH_NOTE_BLOCK = registerWithItem(
            "guitar_nylon_high_note_block",
            properties -> new GuitarNylonNoteBlock(properties, 55, 2.65f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_NYLON_GHOST_LOW_NOTE_BLOCK = registerWithItem(
            "guitar_nylon_ghost_low_note_block",
            properties -> new GuitarNylonNoteBlock(properties, 40, 1.35f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_NYLON_GHOST_HIGH_NOTE_BLOCK = registerWithItem(
            "guitar_nylon_ghost_high_note_block",
            properties -> new GuitarNylonNoteBlock(properties, 55, 1.35f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    /**
     * Softer acoustic/fingerstyle dead-note endpoint.
     *
     * It deliberately reuses the accepted LOW/MID/HIGH dead-note samples and
     * register semantics, but at 0.85 volume instead of Crow's 2.25. This is
     * approximately -8.5 dB relative to the standard dead-note block.
     */
    public static final Block GUITAR_NYLON_DEAD_NOTE_BLOCK = registerWithItem(
            "guitar_nylon_dead_note_block",
            properties -> new GuitarDeadNoteBlock(properties, 0.85f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_NATURAL_HARMONIC_NOTE_BLOCK = registerWithItem(
            "guitar_natural_harmonic_note_block",
            GuitarNaturalHarmonicNoteBlock::new,
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_TAPPED_HARMONIC_NOTE_BLOCK = registerWithItem(
            "guitar_tapped_harmonic_note_block",
            GuitarTappedHarmonicNoteBlock::new,
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    // Accepted Crow mix remains unchanged.
    public static final Block GUITAR_DEAD_NOTE_BLOCK = registerWithItem(
            "guitar_dead_note_block",
            GuitarDeadNoteBlock::new,
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );


    // ---- v0.5 static guitar articulation family ----

    public static final Block GUITAR_STEEL_CLEAN_LOW_NOTE_BLOCK = registerWithItem(
            "guitar_steel_clean_low_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 40,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_STEEL_CLEAN_M40, ModSounds.GUITAR_STEEL_CLEAN_M45, ModSounds.GUITAR_STEEL_CLEAN_M50, ModSounds.GUITAR_STEEL_CLEAN_M55, ModSounds.GUITAR_STEEL_CLEAN_M59, ModSounds.GUITAR_STEEL_CLEAN_M64, ModSounds.GUITAR_STEEL_CLEAN_M69, ModSounds.GUITAR_STEEL_CLEAN_M76}, 2.45f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_STEEL_CLEAN_HIGH_NOTE_BLOCK = registerWithItem(
            "guitar_steel_clean_high_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 55,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_STEEL_CLEAN_M40, ModSounds.GUITAR_STEEL_CLEAN_M45, ModSounds.GUITAR_STEEL_CLEAN_M50, ModSounds.GUITAR_STEEL_CLEAN_M55, ModSounds.GUITAR_STEEL_CLEAN_M59, ModSounds.GUITAR_STEEL_CLEAN_M64, ModSounds.GUITAR_STEEL_CLEAN_M69, ModSounds.GUITAR_STEEL_CLEAN_M76}, 2.45f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_DISTORTED_LOW_NOTE_BLOCK = registerWithItem(
            "guitar_distorted_low_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 40,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_DISTORTED_M40, ModSounds.GUITAR_DISTORTED_M45, ModSounds.GUITAR_DISTORTED_M50, ModSounds.GUITAR_DISTORTED_M55, ModSounds.GUITAR_DISTORTED_M59, ModSounds.GUITAR_DISTORTED_M64, ModSounds.GUITAR_DISTORTED_M69, ModSounds.GUITAR_DISTORTED_M76}, 2.25f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_DISTORTED_HIGH_NOTE_BLOCK = registerWithItem(
            "guitar_distorted_high_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 55,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_DISTORTED_M40, ModSounds.GUITAR_DISTORTED_M45, ModSounds.GUITAR_DISTORTED_M50, ModSounds.GUITAR_DISTORTED_M55, ModSounds.GUITAR_DISTORTED_M59, ModSounds.GUITAR_DISTORTED_M64, ModSounds.GUITAR_DISTORTED_M69, ModSounds.GUITAR_DISTORTED_M76}, 2.25f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_PALM_MUTE_LOW_NOTE_BLOCK = registerWithItem(
            "guitar_palm_mute_low_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 40,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_PALM_MUTE_M40, ModSounds.GUITAR_PALM_MUTE_M45, ModSounds.GUITAR_PALM_MUTE_M50, ModSounds.GUITAR_PALM_MUTE_M55, ModSounds.GUITAR_PALM_MUTE_M59, ModSounds.GUITAR_PALM_MUTE_M64, ModSounds.GUITAR_PALM_MUTE_M69, ModSounds.GUITAR_PALM_MUTE_M76}, 2.15f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_PALM_MUTE_HIGH_NOTE_BLOCK = registerWithItem(
            "guitar_palm_mute_high_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 55,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_PALM_MUTE_M40, ModSounds.GUITAR_PALM_MUTE_M45, ModSounds.GUITAR_PALM_MUTE_M50, ModSounds.GUITAR_PALM_MUTE_M55, ModSounds.GUITAR_PALM_MUTE_M59, ModSounds.GUITAR_PALM_MUTE_M64, ModSounds.GUITAR_PALM_MUTE_M69, ModSounds.GUITAR_PALM_MUTE_M76}, 2.15f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_PALM_MUTE_GHOST_LOW_NOTE_BLOCK = registerWithItem(
            "guitar_palm_mute_ghost_low_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 40,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_PALM_MUTE_M40, ModSounds.GUITAR_PALM_MUTE_M45, ModSounds.GUITAR_PALM_MUTE_M50, ModSounds.GUITAR_PALM_MUTE_M55, ModSounds.GUITAR_PALM_MUTE_M59, ModSounds.GUITAR_PALM_MUTE_M64, ModSounds.GUITAR_PALM_MUTE_M69, ModSounds.GUITAR_PALM_MUTE_M76}, 1.10f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_PALM_MUTE_GHOST_HIGH_NOTE_BLOCK = registerWithItem(
            "guitar_palm_mute_ghost_high_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 55,
                    new int[]{40,45,50,55,59,64,69,76},
                    new SoundEvent[]{ModSounds.GUITAR_PALM_MUTE_M40, ModSounds.GUITAR_PALM_MUTE_M45, ModSounds.GUITAR_PALM_MUTE_M50, ModSounds.GUITAR_PALM_MUTE_M55, ModSounds.GUITAR_PALM_MUTE_M59, ModSounds.GUITAR_PALM_MUTE_M64, ModSounds.GUITAR_PALM_MUTE_M69, ModSounds.GUITAR_PALM_MUTE_M76}, 1.10f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_ARTIFICIAL_HARMONIC_NOTE_BLOCK = registerWithItem(
            "guitar_artificial_harmonic_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 54,
                    new int[]{54,57,62,67,71,76,78},
                    new SoundEvent[]{ModSounds.GUITAR_ARTIFICIAL_HARMONIC_M54, ModSounds.GUITAR_ARTIFICIAL_HARMONIC_M57, ModSounds.GUITAR_ARTIFICIAL_HARMONIC_M62, ModSounds.GUITAR_ARTIFICIAL_HARMONIC_M67, ModSounds.GUITAR_ARTIFICIAL_HARMONIC_M71, ModSounds.GUITAR_ARTIFICIAL_HARMONIC_M76, ModSounds.GUITAR_ARTIFICIAL_HARMONIC_M78}, 2.35f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_PINCH_HARMONIC_NOTE_BLOCK = registerWithItem(
            "guitar_pinch_harmonic_note_block",
            properties -> new GuitarSampledNoteBlock(properties, 66,
                    new int[]{66,69,74,79,83,88,90},
                    new SoundEvent[]{ModSounds.GUITAR_PINCH_HARMONIC_M66, ModSounds.GUITAR_PINCH_HARMONIC_M69, ModSounds.GUITAR_PINCH_HARMONIC_M74, ModSounds.GUITAR_PINCH_HARMONIC_M79, ModSounds.GUITAR_PINCH_HARMONIC_M83, ModSounds.GUITAR_PINCH_HARMONIC_M88, ModSounds.GUITAR_PINCH_HARMONIC_M90}, 2.15f),
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    public static final Block GUITAR_ACOUSTIC_BODY_HIT_BLOCK = registerWithItem(
            "guitar_acoustic_body_hit_block",
            GuitarBodyHitBlock::new,
            BlockBehaviour.Properties.ofFullCopy(Blocks.NOTE_BLOCK)
    );

    private ModBlocks() {}

    private static Block registerWithItem(
            String name,
            Function<BlockBehaviour.Properties, Block> blockFactory,
            BlockBehaviour.Properties properties
    ) {
        Identifier id = BlockScoreInstruments.id(name);
        ResourceKey<Block> blockKey = ResourceKey.create(Registries.BLOCK, id);
        ResourceKey<Item> itemKey = ResourceKey.create(Registries.ITEM, id);

        Block block = blockFactory.apply(properties.setId(blockKey));
        Registry.register(BuiltInRegistries.BLOCK, blockKey, block);

        BlockItem blockItem = new BlockItem(
                block,
                new Item.Properties().setId(itemKey).useBlockDescriptionPrefix()
        );
        Registry.register(BuiltInRegistries.ITEM, itemKey, blockItem);
        return block;
    }

    public static void initialize() {}
}
