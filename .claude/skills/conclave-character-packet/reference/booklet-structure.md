# Booklet structure

`build_content.py` emits one flow of content that the engine paginates into a
saddle-stitch booklet: cover, table of contents, the reference sections, the
worksheets, ruled notes pages (auto-padded to a multiple of four), and a colophon.
Reference sections flow continuously; **each worksheet starts on a fresh page**
(class `pb`).

## Part I — Reference sections (each an `<h2>`)

| # | Section | Source table(s) | Form |
|---|---|---|---|
| 1 | Personal Quick Reference | `pc`, `goals`, allied `characters` | namebar + qr-meta + ranked goals + two-column ally list + reminders |
| 2 | Key Character Profiles | `characters` where `is_key` (skill-judged from the sheet; fallback `(papabile or is_ally) and role not NPC`) | `.profile` cards: They want / You want / You offer / Avoid / Your opinion |
| (after 2) | The character's priority tables | `agenda` (one table per distinct `section`) then `strategy_insights` as "Strategy and Intelligence" | character-tailored content: e.g. "Path to the Papacy", "Targets in Italy", "Alliance Options". For a monarch the `claims`/`forces`/`external_powers` sections precede these. |
| 3 | All Other Characters | `characters` not in Section 2, by role | `.t-tight` tables (Cardinals, Functionaries, Monarchs, Other) |
| 4 | Mercenary Reference | `mercenaries` | Experienced + Fledgling tables. Shown only if the PC has framed the mercenaries (any priority/natural_buyers/notes set): the full commander roster is a broker's tool. The Mercenary Deal Tracker worksheet is gated the same way. |
| 5 | Marriage Candidates | `marriage_candidates` | Brides + Grooms (+ Nunnery) tables |
| 6 | Possessions & Courtiers | `possessions`, `courtiers` | two tables |
| 7 | Forms of Address | `forms_of_address` | one table (proper + rude) |
| 8 | Key Family Relationships | `pc.house`, `siblings`, `families` | family-tree diagram + kin needs table + family connections. The `siblings` table is the PC's direct/generational family: actual siblings group by mother, while a monarch's dynasty (spouse, children, heir, parents) lists by relation. |
| 9 | Rules Mechanics | `rules` grouped by category | one table per category |
| 10 | Pronunciation Guide | `characters.pronunciation` | grouped by role |
| 11 | Game Logistics | `logistics` | one table |
| 12 | Starting State Checklist | `pc` + fixed checklist | qr-box with ballot boxes |
| 13 | Map of Europe in 1492 | image + `territories` | full-bleed map + territory table |

## Part II — Worksheets (each starts on its own page)

| Worksheet | Prefilled from | Writable columns |
|---|---|---|
| Mercenary Deal Tracker | `mercenaries` (name, faction) | Buyer, Price, Other Terms, Status |
| Marriage Deal Tracker | `marriage_candidates` (name, family) | Matched To, Dowry, Faction Gain, Notes, Status |
| Vote Tracker | `characters` role=Cardinal | nine vote columns V1..V9 |
| Favors & Promises | blank | owed-to-me, owed-by-me, vote commitments, money |
| Canonization & War | blank | saints, war declarations, family-safety checklist |
| Asset Status & Letters | `possessions` | given/traded status; letters-received log |

## Packet profiles (per role)

`build_content.py` chooses an ordered set of section and worksheet builders from
`pc.role`. Section numbers (I, II, ...) and the table of contents are derived from
the rendered content, so a profile may reorder or omit sections freely and stay
correctly numbered and paged.

- **Cardinal** (default): the 13 sections and 6 worksheets in the tables above.
- **Monarch**: drops the conclave-only Starting State Checklist; inserts **Claims
  to Thrones and Lands** (from `claims`), **Armies and Commanders** (from
  `forces`), and **Powers Beyond the Conclave** (from `external_powers`, the
  Electors, rival kings, and creditors who have no roster card) right after Key
  Profiles; moves Forms of Address and Pronunciation to the back; leads the
  worksheets with a **Campaign Tracker** in place of the Mercenary Deal Tracker.
  The Vote Tracker stays (a monarch tracks the cardinals as intel).

Add or adjust a profile in `_profile()` in `build_content.py`. Monarch-only
sections (`sec_claims`, `sec_forces`) and worksheets (`ws_campaign`) return empty
and are skipped when their tables are empty, so they are harmless in any profile.

## Changing the booklet

- Content change for one character: edit the **database**, re-run `build_content.py`.
- Add a column to a section, change a table layout, add a worksheet: edit the
  matching function in `build_content.py` (`sec_*` and `ws_*`), then re-render.
  Keep this table in sync.
- Pure visual change (spacing, rules, type) that applies to all characters: edit
  `booklet/booklet.css`. Pagination/imposition logic lives in `booklet-engine.js`.
- Only emit class names that exist in `booklet.css` (e.g. `profile`, `t-tight`,
  `write-row`, `prefilled`, `note`, `reminder-box`, `qr-meta`, `goals`,
  `sheet-head`, `halftitle`). `pb` is a behavioral marker the engine reads to force
  a page break; it has no styling.
