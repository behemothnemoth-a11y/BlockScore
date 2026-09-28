
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~0 ~1 ~1 minecraft:air
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~0 ~1 ~1 minecraft:redstone_block
schedule function blockscore:cal/003_reset 1t replace
