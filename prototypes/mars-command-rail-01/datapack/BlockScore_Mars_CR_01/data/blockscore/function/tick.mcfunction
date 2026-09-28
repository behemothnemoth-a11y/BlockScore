
# Stop cleanly if the anchor was removed.
execute if score #state bs_state matches 1 unless entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run scoreboard players set #state bs_state 0

# Dispatch this song tick at the physical bank anchor.
execute if score #state bs_state matches 1 at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run function blockscore:song/dispatch

# Advance only while playing.
execute if score #state bs_state matches 1 run scoreboard players add #tick bs_tick 1

# Tick 356 contains the final driver resets. Stop after it has run.
execute if score #state bs_state matches 1 if score #tick bs_tick matches 357.. run scoreboard players set #state bs_state 0
