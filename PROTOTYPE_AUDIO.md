# Prototype Natural-Harmonic Audio

The seven OGG files in this module are **procedurally generated prototype audio**.

They contain no third-party samples.

Their purpose is to make the first Fabric implementation immediately testable:

- correct block registration
- correct `note=0..24` behavior
- correct redstone rising-edge behavior
- correct nearest-root multisample selection
- correct residual pitch shift
- correct Command Rail retrigger behavior

They are not intended to be the final Crow-quality guitar library.

After the mechanical test passes, replace:

```text
n00.ogg
n04.ogg
n08.ogg
n12.ogg
n16.ogg
n20.ogg
n24.ogg
```

with recorded/licensed natural-harmonic samples tuned to the same sounding roots.

No Java or registry changes are required when swapping the samples.
