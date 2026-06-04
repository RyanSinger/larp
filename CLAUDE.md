# Conclave 1492: Cardinal Sanseverino

## What this project is

Player support materials for Ryan playing **Cardinal Federico Sanseverino**
(age 17, Noble, Ghibelline, Benedictine) in the Temptemus Papam papal
election LARP. The simulation runs June 8 through 11, 2026 at Lighthaven,
3:30 to 6:30 PM daily.

## The database

`conclave.db` is a SQLite database with all game knowledge. Read it before
answering questions about the game, characters, rules, or strategy. Key tables:

- `characters`: all 40 PCs with negotiation profiles
- `mercenaries`: 26 mercenary commanders with specs, restrictions, priorities
- `marriage_candidates`: brides and grooms with ranks
- `rules`: 38 condensed game mechanics entries
- `messages`: Discord exchanges with analysis (update after every conversation)
- `strategic_insights`: principles, commitments, intel gathered, phased strategy

## Active commitments

Query `SELECT * FROM strategic_insights WHERE category='commitment'` before
advising on any deal. Federico has made specific promises that must be honored.

## When helping with Discord messages

1. Read the `messages` table for conversation history and prior analysis
2. Check `strategic_insights` for relevant principles and intel
3. Check the character profile in `characters` table for the person being messaged
4. Draft in character as a 17 year old cardinal from a military family: respectful
   but not servile, genuine, strategically sharp
5. After the message is sent, INSERT the sent and received messages with analysis
   into the `messages` table and commit the database

## Writing rules

Follow the user's global CLAUDE.md: no dashes (em, en, or hyphens as separators).
Use colons, commas, periods, or rewrite. No emoji.

## Design system

When creating or editing HTML handouts, use the existing design system:
`conclave.css`, `colors_and_type.css`, embedded fonts. See `SKILL.md` for
the full design guide. Keep `-print.html` variants in sync (identical content
plus a `<script>` block before `</body>` that triggers `window.print()`).

## Files

- `reference-booklet.html`: 13-section printable reference booklet (the main product)
- `worksheets.html`: 6 writable tracking worksheets
- `conclave.db`: SQLite game knowledge database
- `uploads/`: source game documents (character sheet, rules, character list, etc.)
- `assets/europe-1492-map.jpg`: the game map
