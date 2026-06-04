# Conclave 1492: Cardinal Sanseverino

Player materials for **Cardinal Federico (da Montefeltro) Sanseverino** in
*Temptemus Papam*, a papal election LARP set in 1492. The simulation runs
June 8 through 11, 2026 at Lighthaven.

## What's here

### Printed materials (the main product)

**`reference-booklet.html`** is a printable reference booklet with 13 sections:
personal quick reference, negotiation profiles for all 40 characters, mercenary
specs, marriage candidates, possessions and courtiers, forms of address, family
relationships, rules mechanics quick reference, pronunciation guide, game
logistics, starting state checklist, and a map of Europe in 1492.

**`worksheets.html`** contains six writable tracking sheets: mercenary deals,
marriage deals, vote tracker (9 votes across 3 days), a favors and promises
ledger with money tracking, a combined canonization and war tracker, and an
asset status and letters log.

Both have **`-print.html`** variants that trigger the print dialog on open
for quick PDF export.

### Game knowledge database

**`conclave.db`** is a SQLite database with everything needed to support play:

| Table | Rows | Contents |
|---|---|---|
| characters | 40 | All PCs with goals, opinions, negotiation notes |
| mercenaries | 26 | 15 experienced + 11 fledgling with specs and priorities |
| marriage_candidates | 27 | 14 brides, 12 grooms, 1 nunnery with ranks |
| possessions | 12 | Items with values and negotiation uses |
| courtiers | 6 | Specialists with deployment ideas |
| goals | 9 | Ranked priorities with sub-goals |
| rules | 38 | Condensed game mechanics |
| vatican_offices | 13 | Offices, salaries, current holders, powers |
| territories | 23 | Italian war map with defense and sack/tax values |
| ports | 28 | Sea ports with defense, quality, tax |
| monastic_orders | 4 | Orders with status gain methods |
| forms_of_address | 23 | Proper and rude forms for every rank |
| families | 15 | Major families with connection to Federico |
| world_facts | 25 | Geopolitical situation in 1492 |
| timeline | 23 | Key events from 1095 to 1492 |
| logistics | 15 | Schedule, locations, signals, starting state |
| messages | 11+ | Discord exchanges with analysis and strategic notes |
| strategic_insights | 30 | Principles, commitments, intel, phased strategy |

### Design system

The `conclave.css`, `colors_and_type.css`, and `fonts/` directory provide
Renaissance chancery styling. The `preview/` folder has specimen cards and
`ui_kits/` has reusable components for building additional handouts.

### Source materials

The `uploads/` directory holds the original game documents: character sheet
(40 pages), rules (42 pages), quickstart slides, character list, timeline,
world facts, and the map of Europe in 1492.

## The game

~40 players take real historical figures (cardinals, functionaries, monarchs)
each with private goals, resources, and secrets. 25 cardinals vote for a new
pope (13 votes for majority) over up to 9 rounds across 3 days. If no pope
is elected by vote 9, the Ottomans invade Europe and a war phase begins.
Day 4 is post-war negotiation. There is no single winner; each player pursues
their own goals.
