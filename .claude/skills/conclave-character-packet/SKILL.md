---
name: conclave-character-packet
description: Build a complete player support packet for any Temptemus Papam (1492 papal-election LARP) character from the game's source files. Ingests the provided PDFs (character sheet, character list, rules, world facts, timeline) and the map, builds a per-character SQLite knowledge database, and generates a print-ready reference booklet (13 sections + 6 worksheets) in the canonical rubricated-chancery design. Use when setting up a new character, regenerating a booklet after database edits, or porting the system from Sanseverino to another player.
user-invocable: true
---

# Conclave Character Packet

Turn the game's source documents into two deliverables for one player character (PC):

1. **`conclave.db`** — a SQLite knowledge base (23 tables) holding the shared
   game world plus everything framed from this PC's point of view.
2. **A print-ready reference booklet** — 13 reference sections and 6 worksheets,
   rendered from the database in the Temptemus Papam house design and exported as
   a saddle-stitch PDF.

The database is the single source of truth. The booklet is generated from it, so
re-running the build after any DB edit reproduces a correct, complete booklet.

## When to use

- A new player picks a character and hands you their packet of game PDFs.
- You edited the database (new intel, changed framing) and want a fresh booklet.
- You are moving the whole system from Sanseverino to a different character.

## What's in this skill

```
schema.sql              generalized 23-table schema (pc + 20 game tables + claims/forces)
scripts/
  init_db.py            create an empty DB from schema.sql
  check_db.py           row-count + missing/empty-table report
  build_content.py      DB  ->  booklet/booklet-content.js  (the generator)
  generate_pdf.cjs      print-shop HTML  ->  verified PDF (headless Chromium)
booklet/                shared rendering assets (copy into the working booklet dir)
  booklet-engine.js     pagination + imposition engine (do not edit per-character)
  booklet.css           the chancery component stylesheet
  fonts-embedded.css    the four embedded webfonts (base64)
  europe-1492-map.jpg   the game map (Section 13 + cover)
  print-shop.html       linear master to send to a print shop
  diy-imposed.html      2-up fold-and-staple master for home printing
reference/
  sources.md            what each source file provides; shared vs PC-specific
  booklet-structure.md   the 13 sections + 6 worksheets and their tables
  design-house-rules.md  the visual brand rules (read before touching HTML/CSS)
```

## Procedure

Work in a per-character directory (e.g. the repo root). `SKILL_DIR` below is this
skill's folder.

### 1. Identify the character
Find the character sheet PDF in `uploads/` (named for the character). Confirm with
the user which character this packet is for. Everything framed as "you / we / our"
means this PC.

### 2. Create the database
```
python3 SKILL_DIR/scripts/init_db.py conclave.db
```

### 3. Populate it from the source files
Read the PDFs in `uploads/` and INSERT rows. See `reference/sources.md` for which
file feeds which table. In short:

- **The PC's character sheet** is the spine. It fills `pc` (one row), `goals`,
  `possessions`, `courtiers`, `siblings`, `relationships`, `strategic_insights`,
  `families.our_connection`, and the PC-relative framing on every `characters`,
  `mercenaries`, and `marriage_candidates` row (`our_opinion`, `what_they_want`,
  `what_we_want`, `what_we_offer`, `what_to_avoid`, `is_ally`, `is_contact`,
  `priority`, `relation_to_pc`). Flag the figures who deserve a full Section 2
  profile card with `is_key=1`.
- **The `pc` row drives the cover and contents page.** Set `name`, `styled_name`
  (the honorific form, e.g. "His Eminence Cardinal ..." or "His Most Christian
  Majesty ..."), `cover_title` (the big cover line, may contain `<br>`), and
  `subtitle`. Set `role` to `'Cardinal'` (default) or `'Monarch'` to pick the
  packet profile. A non-cardinal may set `cover_kicker` to override the
  "Sede Vacante" line.
- **Monarchs** also fill `claims` (dynastic and territorial claims) and `forces`
  (standing armies and commanders, distinct from hireable `mercenaries`). These
  tables stay empty for cardinals.
- **The character list** fills the base facts of `characters` (name, age, rank,
  role, faction, location, papabile).
- **The rules PDF** fills `rules`, `vatican_offices`, `monastic_orders`,
  `forms_of_address`, `ports`, `territories`, `logistics`.
- **The world-facts PDF** fills `world_facts`; **the timeline PDF** fills `timeline`.
- **`mercenaries` and `marriage_candidates`** rosters come from the rules /
  character materials; their priority/buyer/relation framing comes from the sheet.

Use the PC's voice throughout (second person "you"), exact period honorifics,
explanations in plain English, **no dashes as separators, no emoji** (use colons,
commas, periods). Flag every ally with `is_ally=1`; flag papal candidates
`papabile=1`. Commit the database.

### 4. Sanity-check
```
python3 SKILL_DIR/scripts/check_db.py conclave.db
```
Fix any empty critical tables (`pc`, `characters`, `goals`) or missing allies.

### 5. Assemble the booklet directory and generate content
```
mkdir -p booklet
cp SKILL_DIR/booklet/{booklet-engine.js,booklet.css,fonts-embedded.css,europe-1492-map.jpg,print-shop.html,diy-imposed.html} booklet/
python3 SKILL_DIR/scripts/build_content.py conclave.db booklet/booklet-content.js
```

### 6. Render and verify the PDF
```
node SKILL_DIR/scripts/generate_pdf.cjs booklet/print-shop.html "booklet/Reference-Booklet.pdf"
```
The script fails loudly unless the PDF page count equals the live page count and is
a multiple of four. (This is the exact failure mode that once silently dropped the
worksheets: a stale or truncated browser "Save as PDF". Always use this script.)

If Chromium is not installed, install it once:
```
node "$(npm root -g)/playwright/cli.js" install chromium
```

### 7. Iterate
To change the booklet, edit the **database**, then re-run steps 5 and 6. Do not
hand-edit `booklet-content.js`; it is generated. Edit `booklet-engine.js` /
`booklet.css` only for structural design changes that should apply to every
character (and read `reference/design-house-rules.md` first).

## Notes

- **Packet profiles.** The generator picks the section and worksheet set from
  `pc.role`. The **Cardinal** profile is the 13 sections plus 6 worksheets above.
  The **Monarch** profile drops the conclave-only Starting State Checklist, adds
  Claims and Armies sections near the front, moves Forms of Address and
  Pronunciation to the back, and leads the worksheets with a Campaign Tracker.
  Section numbers and the table of contents are derived automatically, so any
  reordering or subset stays correctly numbered and paged. Add a new profile by
  editing `_profile()` in `build_content.py`.
- **Section 2 curation.** Full profile cards go to characters flagged
  `is_key=1`; everyone else falls to the **Section 3** roster tables. If no
  character is flagged `is_key` (an un-curated DB), Section 2 falls back to all
  `is_ally=1` or `papabile=1` characters. Curate by setting `is_key` on the
  dozen or so figures who deserve a full card; leave it unset for a complete but
  busier booklet.
- **Section 8 family tree.** A monospace family-tree diagram is generated from
  the `siblings` table, grouped by mother (multiple marriages read correctly) and
  split sister/brother, followed by a sibling needs table and the family
  connections table. Set `pc.house` for the tree's header line.
- Worksheets prefill writable rows from the database (mercenary commanders, brides
  and grooms, the full cardinal roster for the vote tracker, possessions,
  courtiers) and leave the rest open for ink.
- The booklet is intentionally a faithful mirror of the schema. If you add a column
  the booklet should show, update `build_content.py` and `reference/booklet-structure.md`.
