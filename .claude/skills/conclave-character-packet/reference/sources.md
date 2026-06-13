# Source files and what they feed

The game hands each player a packet of PDFs plus a shared map. Some content is the
**same for every character** (the world); some is **framed from this character's
seat** (the sheet). Below is the mapping from source to database table.

## The files (in `uploads/`)

| File | Kind | Feeds |
|---|---|---|
| `Character Sheet - <Name>.pdf` | PC-specific | `pc` (identity, `role`, cover fields), `goals`, `possessions`, `courtiers`, `siblings`, `relationships`, `strategic_insights`, and all PC-relative framing on `characters` / `mercenaries` / `marriage_candidates`; `families.our_connection`. For a **Monarch** also `claims` (thrones and territorial claims), `forces` (royal armies, fleets, commanders), and `external_powers` (Electors, foreign kings, creditors, the Sultan: the off-roster figures the monarch's game turns on). |
| `... Character List.pdf` | shared | base facts for `characters` (name, age, rank, role, faction, location, papabile) |
| `... Rules ....pdf` | shared | `rules`, `vatican_offices`, `monastic_orders`, `forms_of_address`, `ports`, `territories`, `logistics`; the mercenary roster and marriage mechanics |
| `... Facts About the World.pdf` | shared | `world_facts` |
| `... Timeline ....pdf` | shared | `timeline` |
| `... Quickstart.pdf` | shared | reinforces rules, logistics, the schedule and signals |
| `...Map....jpg` | shared | becomes `booklet/europe-1492-map.jpg` (Section 13 + cover) |

## Shared vs PC-relative columns

Even within one table the columns split:

- `characters`: **shared** = name, title, surname, nickname, age, rank, role,
  faction, location, papabile, monastic_order, pronunciation.
  **PC-relative** = our_opinion, what_they_want, what_we_want, what_we_offer,
  what_to_avoid, is_ally, is_contact, is_key (the skill's judgment, made while
  reading the sheet, of who earns a full Section 2 profile card: allies and chief
  rivals alike).
- `mercenaries`: **shared** = the roster and specs (faction, experience,
  specializes_in, wont_attack, num_armies, min_price). **PC-relative** =
  natural_buyers, priority, notes.
- `marriage_candidates`: **entirely PC-specific.** These are the PC's OWN brides
  and grooms (their kin to marry off), listed on the sheet. Different for every
  character, so rebuild them; do not copy them across.
- `families`: **shared** = name, seat, faction, key_members, notes.
  **PC-relative** = our_connection.
- `what_they_want` and `notes` on `characters` are objective enough to carry over
  as a starting point (`copy_shared.py` does), then refine from the new sheet.

## Porting to a new character

When a finished packet already exists, seed the new database from it with
`scripts/copy_shared.py SOURCE_DB TARGET_DB` instead of re-extracting the world
from the PDFs. It copies the nine world tables verbatim, the base character facts
(plus `what_they_want` and `notes` as a baseline), the mercenary specs, and the
family roster, and leaves every PC-relative column blank.

Two cautions after copying:
- A shared name or title may still carry the source character's framing (a name
  like "Uncle Giovanni della Rovere" or "Aunt Costanza" is relative to that PC).
  Relabel those relatives for the new character.
- A new sheet may reveal different secrets about the same world figures, so review
  the copied `notes` and `what_they_want` and adjust.
