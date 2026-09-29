package dev.blockscore.instruments.block;

import dev.blockscore.instruments.registry.ModSounds;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.stats.Stats;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.level.redstone.Orientation;
import net.minecraft.world.phys.BlockHitResult;
import org.jspecify.annotations.Nullable;

/**
 * A physical dead/muted-string note block.
 *
 * Unlike a pitched note block, NOTE is a register selector:
 *
 *  0..7   -> low strings
 *  8..16  -> middle strings
 * 17..24  -> high strings
 *
 * No runtime pitch shifting is applied. Each register sound event has
 * two string-derived variants in sounds.json, giving automatic variation
 * during dense ghost/dead-string passages.
 */
public final class GuitarDeadNoteBlock extends Block {
    public static final BooleanProperty POWERED = BlockStateProperties.POWERED;
    public static final IntegerProperty NOTE = BlockStateProperties.NOTE;

    public GuitarDeadNoteBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(NOTE, 12).setValue(POWERED, false));
    }

    @Override
    protected void neighborChanged(
            BlockState state,
            Level level,
            BlockPos pos,
            Block neighborBlock,
            @Nullable Orientation orientation,
            boolean movedByPiston
    ) {
        boolean signal = level.hasNeighborSignal(pos);
        boolean powered = state.getValue(POWERED);
        if (signal != powered) {
            if (signal) playNote(null, state, level, pos);
            level.setBlock(pos, state.setValue(POWERED, signal), 3);
        }
    }

    private void playNote(@Nullable Entity source, BlockState state, Level level, BlockPos pos) {
        if (level.getBlockState(pos.above()).isAir()) {
            level.blockEvent(pos, this, 0, 0);
            level.gameEvent(source, GameEvent.NOTE_BLOCK_PLAY, pos);
        }
    }

    @Override
    protected InteractionResult useWithoutItem(
            BlockState state,
            Level level,
            BlockPos pos,
            Player player,
            BlockHitResult hitResult
    ) {
        if (!level.isClientSide()) {
            BlockState tuned = state.cycle(NOTE);
            level.setBlock(pos, tuned, 3);
            playNote(player, tuned, level, pos);
            player.awardStat(Stats.TUNE_NOTEBLOCK);
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    protected void attack(BlockState state, Level level, BlockPos pos, Player player) {
        if (!level.isClientSide()) {
            playNote(player, state, level, pos);
            player.awardStat(Stats.PLAY_NOTEBLOCK);
        }
    }

    @Override
    protected boolean triggerEvent(BlockState state, Level level, BlockPos pos, int eventId, int eventParam) {
        int note = state.getValue(NOTE);
        SoundEvent sound = soundForRegister(note);

        level.addParticle(
                ParticleTypes.NOTE,
                pos.getX() + 0.5,
                pos.getY() + 1.2,
                pos.getZ() + 0.5,
                (double) note / 24.0,
                0.0,
                0.0
        );

        level.playSeededSound(
                null,
                pos.getX() + 0.5,
                pos.getY() + 0.5,
                pos.getZ() + 0.5,
                sound,
                SoundSource.RECORDS,
                2.25f,
                1.0f,
                level.getRandom().nextLong()
        );
        return true;
    }

    private static SoundEvent soundForRegister(int note) {
        if (note <= 7) return ModSounds.GUITAR_DEAD_NOTE_LOW;
        if (note <= 16) return ModSounds.GUITAR_DEAD_NOTE_MID;
        return ModSounds.GUITAR_DEAD_NOTE_HIGH;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(NOTE, POWERED);
    }
}
