
execute unless entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run tellraw @s {text:"CAL-005: install the bank first.",color:"red"}
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run tellraw @s {text:"CAL-005: five physical ostinato layers should attack together.",color:"yellow"}
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~0 ~1 ~1 minecraft:redstone_block
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~10 ~1 ~1 minecraft:redstone_block
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~1 ~1 ~1 minecraft:redstone_block
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~17 ~1 ~1 minecraft:redstone_block
execute if entity @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] at @e[type=minecraft:marker,tag=blockscore_anchor,limit=1] run setblock ~6 ~1 ~1 minecraft:redstone_block
schedule function blockscore:cal/005_reset 1t replace
