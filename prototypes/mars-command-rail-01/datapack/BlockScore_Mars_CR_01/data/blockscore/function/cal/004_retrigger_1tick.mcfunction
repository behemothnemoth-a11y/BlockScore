
execute unless entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run tellraw @s {text:"CAL-004 1t: install the bank first.",color:"red"}
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run tellraw @s {text:"CAL-004 1t: listen for TWO Bass G1 attacks 50 ms apart.",color:"yellow"}
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~0 ~1 ~1 minecraft:redstone_block
schedule function blockscore:cal/004_1tick_phase2 1t replace
