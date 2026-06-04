# Booklet Additions: Design Spec

Five new sections appended to the existing reference booklet (`reference-booklet.html`),
following section 8 (Key Family Relationships). All use the existing design system
(`conclave.css`, `colors_and_type.css`, embedded fonts). Data pulled from `conclave.db`.

## Sections to Add

### Section 9: Rules Mechanics Quick Reference (2 pages)

Two pages of condensed game mechanics organized by use case ("I'm in the middle of a
negotiation and need to check something"), not by rules document order.

**Page 1: Deals and Negotiations.** Covers:
- Contracts: how to finalize (signatures then Notary), binding only after notarized,
  cannot create new ones, public record. Breaking contracts: extremely severe
  consequences (14 listed penalties). Three exceptions for dissolving without penalty.
- Public Declarations: alternative to contracts for non-contractable promises. Announced
  to everyone, cannot be secret, breakable but with faction consequences.
- Marriage rules recap: bride + groom + dowry to orchestrators, rank matching within one
  grade, natural children one rank below, dissolve only before pope elected, cardinal
  mistress rules.
- Mercenary pricing tiers: 50K normal, 40K good, 30K very low (kinsmen only), 20K bare
  minimum (will loot). Fledglings cannot go below 40K.
- Courtier trading rules.

**Page 2: Election, Church, and Consequences.** Covers:
- Papal Petitions: must be signed and turned in to Maffei, Vice-Chancellor controls
  order, pope handles 10 to 12 before war, speaking without invitation is a grave offense.
- Vatican Offices table: all 9 High Offices with salary and current holder, plus 4
  additional benefices (cardinalships, abbacies, armies, Golden Rose).
- Coronation sequence: 3 steps (crowned, cardinals kneel in order, monarchs enter in order).
- Inquisition: three evidence types, Secret Archive, investigation consequences, fine
  amounts, your status (none: it was blackmail). Humanism/heresy question.
- Benedictine monastic status: how to gain status (books, courtiers, cardinal recruits,
  monarch patron).
- Ottoman Invasion trigger: no pope by vote 9 consequences.

**Not included:** War rules (territory tables, army movement, navy rules). You cannot
command armies due to Spinal Compression. Allies who need war tables have their own
rules printouts.

### Section 10: Pronunciation Guide (1 page)

Three tables covering all 40 player characters plus key game terms.

- Cardinals (25 rows): nametag surname, phonetic pronunciation, one-line ID (role, age, origin)
- Functionaries (8 rows): same format
- Monarchs (6 rows): same format
- Key Terms (6 rows): papabile, Temptemus Papam, Guelph, Ghibelline, Camerlengo, condottiero

### Section 11 & 12: Game Logistics + Starting State Checklist (1 page combined)

Top half: schedule (4 days with times and vote numbers), locations (Sistine Chapel =
Lighthaven E, Outside Powers = TBD), out-of-character signal (fist to forehead), key
contacts (orchestrators, Notary, Maffei, Vote Counters), between-session communication
rules.

Bottom half: envelope verification checklist with checkboxes for every card type you
should have on Day 1 (money, port, unsigned contracts, 6 courtiers, 14 brides, 14 grooms,
nunnery, 11 possessions, back brace, special power card). Confirms zero assassins, zero
debt, zero evidence of crime. Includes identity block (name, title, age, rank, combat
value, faction, order, territory, property in Rome).

### Section 13: Map Reference (1 page)

The `assets/europe-1492-map.jpg` image printed full-width. Below it, a compact text
legend annotating:
- Your lands (Caiazzo, Castelnuovo Scrivia, Salerno, Sora)
- Key mercenary regions with controller and army count (Urbino, Mantua, Bologna,
  Rimini, Ferrara, Florence, Milan, Genoa, Rome)
- Outside powers with one-line summary (France, Spain, Empire, England, Ottomans)

## Implementation Approach

Edit the existing `reference-booklet.html` to append sections 9 through 13 after
section 8. Use the same CSS classes and design patterns already in the file
(`.page-break`, `.reminder`, `table` styles, `.qr-box` for the logistics card).
Embed the map as an `<img>` tag referencing the asset path.

Create matching content in `reference-booklet-print.html` (the auto-print variant).

No changes to `worksheets.html` or `worksheets-print.html`.

## What This Does Not Include

- War territory/port value tables (not needed for your role)
- Full rules text (internalize before June 8, reference the printed rules pp. 7-10
  if needed for edge cases)
- Timeline (background reading, not in-game reference)
- Changes to existing sections 1 through 8
