package dev.blockscore.instruments;

import dev.blockscore.instruments.registry.ModBlocks;
import dev.blockscore.instruments.registry.ModSounds;
import net.fabricmc.api.ModInitializer;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class BlockScoreInstruments implements ModInitializer {
    public static final String MOD_ID = "blockscore";
    public static final Logger LOGGER = LoggerFactory.getLogger("blockscore-instruments");

    @Override
    public void onInitialize() {
        ModSounds.initialize();
        ModBlocks.initialize();
        LOGGER.info("BlockScore Instruments initialized.");
    }

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }
}
