package dev.blockscore.instruments.block;

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
 * Generic physical multisample note-block endpoint for BlockScore.
 *
 * NOTE remains 0..24 and POWERED remains a rising-edge trigger, preserving
 * the proven Command Rail physical contract. baseMidi selects the 25-semitone
 * register represented by this block instance.
 */
public final class GuitarSampledNoteBlock extends Block {
    public static final BooleanProperty POWERED = BlockStateProperties.POWERED;
    public static final IntegerProperty NOTE = BlockStateProperties.NOTE;

    private final int baseMidi;
    private final int[] rootMidi;
    private final SoundEvent[] rootSounds;
    private final float volume;

    public GuitarSampledNoteBlock(
            Properties properties,
            int baseMidi,
            int[] rootMidi,
            SoundEvent[] rootSounds,
            float volume
    ) {
        super(properties);
        if (rootMidi.length == 0 || rootMidi.length != rootSounds.length) {
            throw new IllegalArgumentException("rootMidi/rootSounds must be non-empty and the same length");
        }
        this.baseMidi = baseMidi;
        this.rootMidi = rootMidi.clone();
        this.rootSounds = rootSounds.clone();
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
        int rootIndex = nearestRootIndex(midi);
        int root = rootMidi[rootIndex];
        SoundEvent sound = rootSounds[rootIndex];
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

    private int nearestRootIndex(int midi) {
        int best = 0;
        int bestDistance = Math.abs(midi - rootMidi[0]);
        for (int i = 1; i < rootMidi.length; i++) {
            int distance = Math.abs(midi - rootMidi[i]);
            if (distance < bestDistance) {
                best = i;
                bestDistance = distance;
            }
        }
        return best;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(NOTE, POWERED);
    }
}
