
scoreboard players set #state bs_state 0
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run function blockscore:build/reset_drivers
