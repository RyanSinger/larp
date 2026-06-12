# Source files and what they feed

The game hands each player a packet of PDFs plus a shared map. Some content is the
**same for every character** (the world); some is **framed from this character's
seat** (the sheet). Below is the mapping from source to database table.

## The files (in `uploads/`)

| File | Kind | Feeds |
|---|---|---|
| `Character Sheet - <Name>.pdf` | PC-specific | `pc` (identity, `role`, cover fields), `goals`, `possessions`, `courtiers`, `siblings`, `relationships`, `strategic_insights`, and all PC-relative framing on `characters` / `mercenaries` / `marriage_candidates`; `families.our_connection`. For a **Monarch** also `claims` (thrones and territorial claims) and `forces` (royal armies, fleets, commanders). |
| `... Character List.pdf` | shared | base facts for `characters` (name, age, rank, role, faction, location, papabile) |
| `... Rules ....pdf` | shared | `rules`, `vatican_offices`, `monastic_orders`, `forms_of_address`, `ports`, `territories`, `logistics`; mercenary and marriage roster mechanics |
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
- `mercenaries`: **shared** = specs (faction, experience, specializes_in,
  wont_attack, num_armies, min_price). **PC-relative** = natural_buyers, priority,
  and the angle in notes.
- `marriage_candidates`: **shared** = name, type, family, rank.
  **PC-relative** = relation_to_pc, the angle in notes.
- `families`: **shared** = name, seat, faction, key_members.
  **PC-relative** = our_connection.

## Porting to a new character

When the world tables (`rules`, `world_facts`, `timeline`, `forms_of_address`,
`ports`, `territories`, `vatican_offices`, `monastic_orders`, and the base facts of
`characters` / `mercenaries` / `marriage_candidates`) are already captured for one
character, they can be **copied** into the new DB unchanged. Only the PC-relative
content and the `pc` row need to be rebuilt from the new character's sheet. (Beware:
the new sheet may reveal different secrets about the same world figures, so review
`notes` fields.)
