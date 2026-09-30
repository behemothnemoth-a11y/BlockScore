package dev.blockscore.instruments.registry;

import dev.blockscore.instruments.BlockScoreInstruments;
import dev.blockscore.instruments.block.GuitarDeadNoteBlock;
import dev.blockscore.instruments.block.GuitarNaturalHarmonicNoteBlock;
import dev.blockscore.instruments.block.GuitarNylonNoteBlock;
import dev.blockscore.instruments.block.GuitarTappedHarmonicNoteBlock;
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
