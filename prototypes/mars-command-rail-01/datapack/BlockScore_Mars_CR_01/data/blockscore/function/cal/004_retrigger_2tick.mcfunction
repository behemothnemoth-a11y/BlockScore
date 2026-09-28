
execute unless entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run tellraw @s {text:"CAL-004 2t: install the bank first.",color:"red"}
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run tellraw @s {text:"CAL-004 2t: listen for TWO Bass G1 attacks 100 ms apart.",color:"yellow"}
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~0 ~1 ~1 minecraft:redstone_block
schedule function blockscore:cal/004_2tick_reset1 1t replace
schedule function blockscore:cal/004_2tick_fire2 2t replace
