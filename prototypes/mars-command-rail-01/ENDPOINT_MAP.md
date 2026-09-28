# Endpoint Map

The prototype anchor is the support-block coordinate of endpoint X=0.

| Endpoint | X | Instrument | Pitch | State | Support |
|---|---:|---|---|---:|---|
| `bass_g1_01` | 0 | `bass` | G1 | 1 | `minecraft:oak_planks` |
| `bass_g2_01` | 1 | `bass` | G2 | 13 | `minecraft:oak_planks` |
| `bass_g2_02` | 2 | `bass` | G2 | 13 | `minecraft:oak_planks` |
| `bass_db3_01` | 3 | `bass` | Db3 | 19 | `minecraft:oak_planks` |
| `bass_d3_01` | 4 | `bass` | D3 | 20 | `minecraft:oak_planks` |
| `basedrum_state00_01` | 6 | `basedrum` | percussion | 0 | `minecraft:stone` |
| `snare_state00_01` | 8 | `snare` | percussion | 0 | `minecraft:sand` |
| `guitar_g2_01` | 10 | `guitar` | G2 | 1 | `minecraft:white_wool` |
| `didgeridoo_g1_01` | 12 | `didgeridoo` | G1 | 1 | `minecraft:pumpkin` |
| `didgeridoo_db2_01` | 13 | `didgeridoo` | Db2 | 7 | `minecraft:pumpkin` |
| `didgeridoo_d2_01` | 14 | `didgeridoo` | D2 | 8 | `minecraft:pumpkin` |
| `didgeridoo_db3_01` | 15 | `didgeridoo` | Db3 | 19 | `minecraft:pumpkin` |
| `banjo_g3_01` | 17 | `banjo` | G3 | 1 | `minecraft:hay_block` |
| `trumpet_weathered_g2_01` | 19 | `trumpet_weathered` | G2 | 1 | `minecraft:weathered_copper` |
| `trumpet_weathered_db3_01` | 20 | `trumpet_weathered` | Db3 | 7 | `minecraft:weathered_copper` |
| `trumpet_weathered_d3_01` | 21 | `trumpet_weathered` | D3 | 8 | `minecraft:weathered_copper` |

Geometry for each endpoint:

```text
Y+2  air
Y+1  note block      driver at Z+1
Y+0  support block
```

The current bank spans X=0 through X=21. Empty X positions are deliberate one-block gaps between instrument families.
