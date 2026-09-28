
execute unless entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run tellraw @s {text:"BlockScore: no anchor. Run /function blockscore:install first.",color:"red"}
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run function blockscore:build/reset_drivers
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run scoreboard players set #tick bs_tick 0
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run scoreboard players set #state bs_state 1
