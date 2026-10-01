# BlockScore Compiler Core

BlockScore now contains the first repository-owned production compiler foundation.

## Boundary

BlockScore generates and validates artifacts. It does not launch Minecraft,
install datapacks into a world, change the user's game tick rate, or claim that
offline validation is an in-game test.

The user remains responsible for Minecraft-side installation and game testing.

## Current compiler boundary

The compiler consumes the existing BlockScore Minecraft Master event format.
Source import/transcription (GP5, MIDI, notation, manual transcription) happens
upstream and must produce that Master representation.

Source material -> Source Score -> Minecraft Master events -> backend compiler -> artifacts

## Command Rail compile

Example:

    python -m blockscore compile-command-rail fixtures/mars/master-events-m001-m008.yaml --repo-root . --qpm 132 --tps 20 --pulse-ticks 1 --busy-window-ticks 2 --namespace blockscore_mars --title "Mars" --output build/mars --zip

The compiler performs deterministic absolute-time quantization, instrument/state
validation, endpoint pool allocation, sparse physical layout, schedule generation,
balanced dispatch generation, and build-plan reporting.

The allocator grows physical endpoint pools rather than merging musical events
to save blocks.

## Tick-rate ownership

Generated functions never execute /tick. A generated pack records and reports
its required TPS, but tick-rate selection remains user-side. The pack linter
enforces this boundary.

## Repository validation

    python -m blockscore validate-repo .

Current checks include JSON/YAML parsing, schema validation, custom block/resource
cross-checks, declared sample existence, function-reference resolution, the
user-side /tick boundary, and executable YAML contracts.

Tests that parse but do not yet have semantic handlers are reported as
STRUCTURAL_ONLY; they are not silently counted as passing.

## Generated pack validation

    python -m blockscore validate-pack path/to/pack-or-directory

This checks ZIP/JSON integrity, required function tags, function references,
physical-pack /playsound leakage, and the /tick boundary.

## CI

.github/workflows/blockscore-core.yml runs the compiler/contract suite and
recompiles Mars on every relevant push or pull request.

Minecraft itself is intentionally not invoked by CI.
