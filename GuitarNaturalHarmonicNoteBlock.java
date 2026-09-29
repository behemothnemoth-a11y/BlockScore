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

public final class GuitarNaturalHarmonicNoteBlock extends Block {
    public static final BooleanProperty POWERED = BlockStateProperties.POWERED;
    public static final IntegerProperty NOTE = BlockStateProperties.NOTE;

    private static final int[] ROOT_STATES = {0, 4, 8, 12, 16, 20, 24};

    public GuitarNaturalHarmonicNoteBlock(Properties properties) {
        super(properties);
        registerDefaultState(
                stateDefinition.any()
                        .setValue(NOTE, 0)
                        .setValue(POWERED, false)
        );
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
            if (signal) {
                playNote(null, state, level, pos);
            }

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
        int root = nearestRoot(note);
        SoundEvent sound = soundForRoot(root);
        float pitch = pitchFromOffset(note - root);

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
                3.0f,
                pitch,
                level.getRandom().nextLong()
        );

        return true;
    }

    static int nearestRoot(int noteState) {
        int candidate = ((noteState + 2) / 4) * 4;
        return Math.max(ROOT_STATES[0], Math.min(ROOT_STATES[ROOT_STATES.length - 1], candidate));
    }

    static float pitchFromOffset(int semitones) {
        return (float) Math.pow(2.0, semitones / 12.0);
    }

    private static SoundEvent soundForRoot(int root) {
        return switch (root) {
            case 0 -> ModSounds.GUITAR_NATURAL_HARMONIC_N00;
            case 4 -> ModSounds.GUITAR_NATURAL_HARMONIC_N04;
            case 8 -> ModSounds.GUITAR_NATURAL_HARMONIC_N08;
            case 12 -> ModSounds.GUITAR_NATURAL_HARMONIC_N12;
            case 16 -> ModSounds.GUITAR_NATURAL_HARMONIC_N16;
            case 20 -> ModSounds.GUITAR_NATURAL_HARMONIC_N20;
            case 24 -> ModSounds.GUITAR_NATURAL_HARMONIC_N24;
            default -> throw new IllegalArgumentException("Unsupported multisample root: " + root);
        };
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(NOTE, POWERED);
    }
}
