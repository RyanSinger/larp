# Temptemus Papam: Character Packet Toolkit

Build player support materials for **Temptemus Papam**, a papal election LARP set
in 1492, for any character. From a player's packet (their character sheet plus the
shared game documents) this toolkit produces a SQLite knowledge database and a
print-ready reference booklet in a Renaissance chancery design.

This repository is character-agnostic. Federico Sanseverino's filled-in packet
lives on the `sanseverino` branch; `main` is a clean starting point for a new
player.

## What's here

- **`.claude/skills/conclave-character-packet/`** — the skill that ingests a
  character's packet and produces the database and a print-ready booklet
  (13 reference sections plus 6 worksheets). It bundles its own rendering engine,
  stylesheet, embedded fonts, and the game map, so it is self-contained.
- **`uploads/`** — the shared game documents, identical for every player: rules,
  facts about the world, timeline, character list, quickstart, and the map. Add
  your own character sheet PDF here.
- **Design system** — `conclave.css`, `colors_and_type.css`, `fonts/`, the
  `SKILL.md` design guide, `preview/` specimen cards, and `ui_kits/` components,
  for building additional handouts in the same brand.

## Quick start

1. Drop your character sheet PDF into `uploads/`.
2. Invoke the `conclave-character-packet` skill (type `/conclave-character-packet`)
   and follow its steps. It builds `conclave.db`, populates it from the source
   documents, and generates a `booklet/` directory with a verified PDF.
3. Print the booklet (the skill's `generate_pdf.cjs` exports and verifies it).

The database is the single source of truth. Re-run the build whenever the game
state changes and you get a correct, complete booklet.

## The game

About 40 players take real historical figures (cardinals, functionaries,
monarchs), each with private goals, resources, and secrets. 25 cardinals vote for
a new pope over up to 9 rounds across 3 days. If no pope is elected by the ninth
vote, a war phase begins. There is no single winner; each player pursues their own
goals.
