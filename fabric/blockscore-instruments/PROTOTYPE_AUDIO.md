# Audio Status — v0.3

The natural-harmonic and tapped-harmonic banks from v0.2 are **accepted** by the Crow in-game test and remain unchanged.

The dead/muted-string bank is redesigned in v0.3.

Instead of seven pitched dead-note samples, it now has three percussion registers:

```text
LOW   -> note_state 0
MID   -> note_state 12
HIGH  -> note_state 24
```

Each register has two string-derived variants. Minecraft's sound-event variation chooses between them automatically.

No runtime pitch shifting is applied to dead notes.

The source material remains the CC0 SpeedY `Nylon Guitar Single notes` pack. The audio is processed to emphasize real pick/fret/string transients while suppressing stable pitch.

Crow v3 routes GPX muted notes by their original string number:

```text
strings 6/5 -> LOW
strings 4/3 -> MID
strings 2/1 -> HIGH
```

(Internally GPX stores the strings low-to-high as indices 0..5.)

See `THIRD_PARTY_AUDIO.md`.
