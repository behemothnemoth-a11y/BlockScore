
# Run this function AS A PLAYER standing where endpoint x=0 support block should be.
# If a previous prototype exists, remove its bank first.
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run function blockscore:build/clear_bank
kill @e[type=minecraft:marker,tag=blockscore_anchor]

# Snap the anchor to the current player's block coordinates.
execute at @s align xyz run summon minecraft:marker ~ ~ ~
execute at @s align xyz run tag @e[type=minecraft:marker,sort=nearest,limit=1,distance=..0.1] add blockscore_anchor

execute at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run function blockscore:build/place_bank
scoreboard players set #state bs_state 0
scoreboard players set #tick bs_tick 0
