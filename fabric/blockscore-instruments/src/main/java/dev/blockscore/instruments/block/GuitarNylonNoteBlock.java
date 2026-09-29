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
 * Physical sampled nylon-guitar note block.
 *
 * The low instance maps note 0..24 to MIDI 40..64 (E2..E4).
 * The high instance maps note 0..24 to MIDI 55..79 (G3..G5).
 * Ghost instances use the same samples and tuning with reduced volume.
 */
public final class GuitarNylonNoteBlock extends Block {
    public static final BooleanProperty POWERED = BlockStateProperties.POWERED;
    public static final IntegerProperty NOTE = BlockStateProperties.NOTE;
    private static final int[] ROOT_MIDI = {40, 45, 50, 55, 59, 64, 69, 76};

    private final int baseMidi;
    private final float volume;

    public GuitarNylonNoteBlock(Properties properties, int baseMidi, float volume) {
        super(properties);
        this.baseMidi = baseMidi;
        this.volume = volume;
        registerDefaultState(stateDefinition.any().setValue(NOTE, 0).setValue(POWERED, false));
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
        int midi = baseMidi + note;
        int root = nearestRoot(midi);
        SoundEvent sound = soundForRoot(root);
        float pitch = (float) Math.pow(2.0, (midi - root) / 12.0);

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
                volume,
                pitch,
                level.getRandom().nextLong()
        );
        return true;
    }

    private static int nearestRoot(int midi) {
        int best = ROOT_MIDI[0];
        int bestDistance = Math.abs(midi - best);
        for (int root : ROOT_MIDI) {
            int distance = Math.abs(midi - root);
            if (distance < bestDistance) {
                best = root;
                bestDistance = distance;
            }
        }
        return best;
    }

    private static SoundEvent soundForRoot(int root) {
        return switch (root) {
            case 40 -> ModSounds.GUITAR_NYLON_M40;
            case 45 -> ModSounds.GUITAR_NYLON_M45;
            case 50 -> ModSounds.GUITAR_NYLON_M50;
            case 55 -> ModSounds.GUITAR_NYLON_M55;
            case 59 -> ModSounds.GUITAR_NYLON_M59;
            case 64 -> ModSounds.GUITAR_NYLON_M64;
            case 69 -> ModSounds.GUITAR_NYLON_M69;
            case 76 -> ModSounds.GUITAR_NYLON_M76;
            default -> throw new IllegalArgumentException("Unsupported nylon root MIDI: " + root);
        };
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(NOTE, POWERED);
    }
}
