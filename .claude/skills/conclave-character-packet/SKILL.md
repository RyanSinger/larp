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
  copy_shared.py        seed the shared game world from an existing packet DB
  dbhelpers.py          insert/insert_many/update helpers (author with these)
  check_db.py           structural report + curation/depth/content quality lint
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

### 2. Create the database and seed the shared world
```
python3 SKILL_DIR/scripts/init_db.py conclave.db
```
The game world is identical for every player. If a finished packet already exists
(for example another character's `conclave.db`), seed the shared tables from it
instead of re-extracting them from the PDFs:
```
python3 SKILL_DIR/scripts/copy_shared.py OTHER_CHARACTER/conclave.db conclave.db
```
This fills the world tables, the base character facts, the mercenary specs, and
the family roster, and leaves every PC-relative column blank for you to author.
Prefer the least-authored existing packet as the source, since `what_they_want`
and `notes` carry over as a baseline and may hold the source character's slant;
review and adjust them. Then relabel any relatives that carry the other
character's framing (a name like "Uncle Giovanni della Rovere" may be the new
PC's brother).

### 3. Populate the PC-relative content from the character sheet
Read the PCs sheet and INSERT or UPDATE rows. See `reference/sources.md` for
which file feeds which table.

**Reading the PDFs.** The built-in file reader cannot render these PDFs (it needs
poppler, which is not installed), and `pdfminer`/`pypdf` fail because the
environment's `cryptography` binding is broken. Use PyMuPDF, which is
self-contained:
```
python3 -m pip install --quiet pymupdf
python3 -c "import fitz,sys; print(''.join(p.get_text() for p in fitz.open(sys.argv[1])))" SHEET.pdf
```

In short, the character sheet supplies:

- **The PC's character sheet** is the spine. It fills `pc` (one row), `goals`,
  `possessions`, `courtiers`, `siblings`, `relationships`, `strategic_insights`,
  `families.our_connection`, and the PC-relative framing on every `characters`,
  `mercenaries`, and `marriage_candidates` row (`our_opinion`, `what_they_want`,
  `what_we_want`, `what_we_offer`, `what_to_avoid`, `is_ally`, `is_contact`,
  `priority`, `relation_to_pc`). Set `papabile=1` on every papal contender and
  `is_ally=1` on every ally.
- **Judge who matters and flag `is_key=1` on them.** As you read the character
  sheet, decide who this PC will actually deal with most over the game: their
  patron and inner circle, their closest allied cardinals, the papal contenders
  (allies *and* the chief rivals they must outmaneuver), and the great powers who
  shape their fate. Flag those `is_key=1`, aiming for a readable set of roughly
  ten to fourteen so Section 2 stays useful at the table during play. Importance
  is not alliance: include the rivals you must study, and leave family relatives
  (`role='NPC'`) to Section 8. This judgment is the skill's job, not the player's;
  if you flag nobody, the booklet falls back to all papabili and allies.
- **The `pc` row drives the cover and contents page.** Set `name`, `styled_name`
  (the honorific form, e.g. "His Eminence Cardinal ..." or "His Most Christian
  Majesty ..."), `cover_title` (the big cover line, may contain `<br>`), and
  `subtitle`. Set `role` to `'Cardinal'` (default) or `'Monarch'` to pick the
  packet profile. A non-cardinal may set `cover_kicker` to override the
  "Sede Vacante" line.
- **Author with `dbhelpers`.** Insert rows with
  `from dbhelpers import insert, insert_many, update` rather than hand-written
  positional SQL: the statement is built from the dict keys, so a stray or missing
  value cannot silently roll back the whole build (the recurring binding bug).
- **Monarchs** also fill `claims` (dynastic and territorial claims), `forces`
  (standing armies and commanders, distinct from hireable `mercenaries`), and
  `external_powers` (the figures a monarch's game turns on who are NOT seated at
  the conclave: the Prince-Electors, rival kings like a Vladislaus, creditors like
  the Fugger bank, the Sultan). These three tables stay empty for cardinals.
  Putting the off-roster game in `external_powers` gives it a real reference
  section instead of leaving it buried in prose. A monarch's `siblings` table
  holds the whole direct dynasty, not just siblings: spouse, children, the heir,
  and parents belong there too (the family tree renders them by relation).
- **The character list** fills the base facts of `characters` (name, age, rank,
  role, faction, location, papabile).
- **The rules PDF** fills `rules`, `vatican_offices`, `monastic_orders`,
  `forms_of_address`, `ports`, `territories`, `logistics`.
- **The world-facts PDF** fills `world_facts`; **the timeline PDF** fills `timeline`.
- **`marriage_candidates`** are the PC's OWN brides and grooms (their kin to marry
  off), listed on the sheet, not a shared roster. Rebuild them per character.
- **`mercenaries`** is a shared roster, but the Mercenary Reference section and
  Mercenary Deal Tracker only render if the PC has framed it (set any
  `priority` / `natural_buyers` / `notes`). The full commander roster is a
  broker's tool: author the framing for a mercenary-broker PC (Sanseverino), and
  leave it blank for a PC who only occasionally hires, so the section omits.

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
node SKILL_DIR/scripts/generate_pdf.cjs booklet/print-shop.html
```
The output filename is derived from the PC named on the cover, e.g.
`booklet/Cardinal della Rovere Reference Booklet.pdf`. Pass a second argument to
override it. The script fails loudly unless the PDF page count equals the live page count and is
a multiple of four. (This is the exact failure mode that once silently dropped the
worksheets: a stale or truncated browser "Save as PDF". Always use this script.)

If Chromium is not installed, install it once:
```
node "$(npm root -g)/playwright/cli.js" install chromium
```

### 7. Iterate, and keep the packet alive during play
To change the booklet, edit the **database**, then re-run steps 5 and 6. Do not
hand-edit `booklet-content.js`; it is generated. Edit `booklet-engine.js` /
`booklet.css` only for structural design changes that should apply to every
character (and read `reference/design-house-rules.md` first).

The first build is a foundation, not the finished product. The most useful packet
is the one that grows as the game unfolds: log exchanges in `messages` and add
`strategic_insights` (commitments made, intel gathered, phased strategy, shifting
alliances), then regenerate. Strategic insights are the single biggest driver of a
booklet's usefulness at the table, and they carry the parts of the game the
character roster cannot, above all a monarch's off-roster world (Electors, foreign
kings, debts). A thorough first pass is good; a packet maintained through play is
what becomes a true playbook.

## Notes

- **Packet profiles.** The generator picks the section and worksheet set from
  `pc.role`. The **Cardinal** profile is the 13 sections plus 6 worksheets above.
  The **Monarch** profile drops the conclave-only Starting State Checklist, adds
  Claims and Armies sections near the front, moves Forms of Address and
  Pronunciation to the back, and leads the worksheets with a Campaign Tracker.
  Section numbers and the table of contents are derived automatically, so any
  reordering or subset stays correctly numbered and paged. Add a new profile by
  editing `_profile()` in `build_content.py`.
- **Section 2 is the skill's importance judgment.** Full profile cards go to the
  characters flagged `is_key` during ingestion: the dozen-or-so figures this PC
  will deal with most, allies *and* chief rivals. The point of a tight set is
  usability in play, so keep it to roughly ten to fourteen and let everyone else
  fall to the **Section 3** roster tables (where they are still one scannable
  row). If a database has nothing flagged, Section 2 falls back to all papabili
  and allies (`(papabile or is_ally) and role not NPC`), a complete but busier
  default. Importance is not alliance: a papal rival you must beat belongs in
  Section 2; a friendly uncle belongs in Section 8.
- **Section 8 family tree.** A monospace family-tree diagram is generated from
  the `siblings` table: actual siblings are grouped by mother (multiple marriages
  read correctly) and split sister/brother, while other direct kin (spouse,
  children, heir, parents) are listed by relation, so a monarch's dynasty renders
  as cleanly as a cardinal's brood. A kin needs table and the family connections
  table follow. Set `pc.house` for the tree's header line.
- Worksheets prefill writable rows from the database (mercenary commanders, brides
  and grooms, the full cardinal roster for the vote tracker, possessions,
  courtiers) and leave the rest open for ink.
- The booklet is intentionally a faithful mirror of the schema. If you add a column
  the booklet should show, update `build_content.py` and `reference/booklet-structure.md`.
