# Temptemus Papam: Character Packet Toolkit

## What this repo is

A character-agnostic toolkit for building player support materials for **Temptemus
Papam**, a papal election LARP set in 1492. From a player's packet it builds a
SQLite knowledge database and a print-ready reference booklet in a Renaissance
chancery design.

`main` is a clean starting point for any new player. A specific player's filled-in
materials (database, built booklet, Discord log, strategy) belong on their own
branch, not on `main`. Federico Sanseverino's is the `sanseverino` branch.

## Building a packet

Use the **`conclave-character-packet`** skill. In short:

1. Put the character sheet PDF in `uploads/` (the shared game documents are
   already there: rules, world facts, timeline, character list, quickstart, map).
2. Run the skill and follow `.claude/skills/conclave-character-packet/SKILL.md`:
   it creates `conclave.db`, populates it from the sources (this is also where the
   skill judges who the player will deal with most and flags them for the booklet's
   key-profiles section), then generates and verifies the booklet PDF.
3. The database is the single source of truth; regenerate the booklet whenever the
   game state changes.

When helping a specific player during play (drafting messages, tracking deals,
recording intel), do that work on that player's branch and keep their `conclave.db`
and notes there.

## Writing rules

No dashes (em, en, or hyphen as separators). Use colons, commas, periods, or
rewrite. No emoji.

## Design system

When creating or editing HTML handouts, use the existing design system:
`conclave.css`, `colors_and_type.css`, embedded fonts. See `SKILL.md` for the full
design guide, `preview/` for specimen cards, and `ui_kits/` for components. The
booklet's own engine and assets are bundled inside the skill. Keep any
`-print.html` variants in sync with their editable masters.
