
function blockscore:control/stop
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run function blockscore:build/clear_bank
kill @e[type=minecraft:marker,tag=blockscore_anchor]
scoreboard players set #tick bs_tick 0
