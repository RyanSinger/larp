-- ============================================================
-- Temptemus Papam — character packet database schema
-- ============================================================
-- One SQLite database per player character (PC). Two kinds of table:
--
--   SHARED (identical for every PC, taken from the rules / world-facts /
--   timeline / character-list / map source files):
--     forms_of_address, logistics, monastic_orders, ports, rules,
--     territories, timeline, vatican_offices, world_facts,
--     and the BASE facts (name/age/rank/faction) of characters,
--     mercenaries, marriage_candidates.
--
--   PC-RELATIVE (framed from THIS character's point of view, taken from
--   the PC's own character sheet — "our/we/you" always means the PC):
--     pc, goals, possessions, courtiers, siblings, families.our_connection,
--     relationships, strategic_insights, messages, and the
--     our_opinion / what_they_want / what_we_want / what_we_offer /
--     what_to_avoid / is_ally / is_contact framing on characters,
--     mercenaries.natural_buyers/priority, marriage_candidates.relation_to_pc.
--
-- Convention: keep all first-person framing in the PC's voice (second
-- person "you"), period honorifics exact, explanations in clear English.
-- ============================================================

-- The protagonist. Exactly one row. Drives the cover, the title pages,
-- and Section 1 (Personal Quick Reference) of the booklet.
CREATE TABLE pc (
  id INTEGER PRIMARY KEY CHECK(id = 1),
  name TEXT NOT NULL,           -- e.g. "Cardinal Federico Sanseverino"
  role TEXT DEFAULT 'Cardinal', -- 'Cardinal' or 'Monarch'; selects the booklet packet profile
  styled_name TEXT,             -- honorific form for cover/TOC, e.g. "His Eminence Cardinal Federico Sanseverino"
  cover_title TEXT,             -- big cover line, may contain <br>, e.g. "Cardinal<br>Sanseverino"
  cover_kicker TEXT,            -- optional override for the cover kicker line (non-cardinals)
  subtitle TEXT,                -- e.g. "Cardinal Deacon of San Teodoro"
  age INTEGER,
  rank TEXT,
  faction TEXT,
  monastic_order TEXT,
  origin TEXT,                  -- "From Caiazzo, near Naples"
  combat_value TEXT,
  territory TEXT,
  money TEXT,
  port TEXT,
  special_power TEXT,
  evidence_of_crime TEXT,
  property_in_rome TEXT,
  house TEXT,                   -- family-tree header line, e.g. "SANSEVERINO (your house, through father Roberto)"
  key_reminders TEXT,           -- free text shown in the quick-reference panel
  notes TEXT
);

-- Monarch packets only (empty for cardinals): dynastic and territorial claims.
CREATE TABLE claims (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,           -- e.g. "Throne of Naples"
  target TEXT,                  -- who/what it is against, e.g. "Ferrante of Aragon"
  basis TEXT,                   -- the legal/dynastic basis
  status TEXT,                  -- pressed / dormant / renounced / won
  notes TEXT
);

-- Monarch packets only (empty for cardinals): standing armies and commanders,
-- distinct from the hireable mercenaries table.
CREATE TABLE forces (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  kind TEXT,                    -- e.g. "Royal army", "Fleet", "Levy"
  strength TEXT,
  location TEXT,
  commander TEXT,
  notes TEXT
);

CREATE TABLE characters (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  title TEXT,
  surname TEXT,
  nickname TEXT,
  age INTEGER,
  rank TEXT CHECK(rank IN ('Commoner','Noble','High Noble','Monarch')),
  role TEXT CHECK(role IN ('Cardinal','Functionary','Monarch','NPC')),
  faction TEXT,
  location TEXT,
  papabile INTEGER DEFAULT 0,
  is_ally INTEGER DEFAULT 0,
  is_contact INTEGER DEFAULT 0,
  monastic_order TEXT,
  pronunciation TEXT,
  our_opinion TEXT,
  what_they_want TEXT,
  what_we_want TEXT,
  what_we_offer TEXT,
  what_to_avoid TEXT,
  notes TEXT
);

CREATE TABLE courtiers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  specialty TEXT,
  deployment_ideas TEXT,
  notes TEXT
);

CREATE TABLE families (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  seat TEXT,
  faction TEXT,
  our_connection TEXT,
  key_members TEXT,
  notes TEXT
);

CREATE TABLE forms_of_address (
  id INTEGER PRIMARY KEY,
  rank_or_name TEXT NOT NULL,
  formal_address TEXT NOT NULL,
  rude_address TEXT,
  notes TEXT
);

CREATE TABLE goals (
  id INTEGER PRIMARY KEY,
  priority INTEGER NOT NULL,
  description TEXT NOT NULL,
  sub_goals TEXT,
  notes TEXT
);

CREATE TABLE logistics (
  id INTEGER PRIMARY KEY,
  topic TEXT NOT NULL,
  details TEXT NOT NULL
);

CREATE TABLE marriage_candidates (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT CHECK(type IN ('Bride','Groom','Nunnery')),
  family TEXT,
  rank TEXT,
  relation_to_pc TEXT,
  notes TEXT
);

CREATE TABLE mercenaries (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  faction TEXT,
  experience TEXT CHECK(experience IN ('Experienced','Fledgling')),
  specializes_in TEXT,
  wont_attack TEXT,
  num_armies INTEGER DEFAULT 1,
  reserve_commander TEXT,
  min_price INTEGER DEFAULT 40000,
  natural_buyers TEXT,
  priority TEXT,
  notes TEXT
);

CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  channel TEXT NOT NULL,
  direction TEXT CHECK(direction IN ('received','sent')),
  from_character TEXT NOT NULL,
  to_character TEXT NOT NULL,
  timestamp TEXT,
  content TEXT NOT NULL,
  analysis TEXT,
  strategic_notes TEXT
);

CREATE TABLE monastic_orders (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  patron TEXT,
  leader TEXT,
  status_gain_method TEXT,
  notes TEXT
);

CREATE TABLE ports (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT CHECK(type IN ('Town','City','Fort City')),
  controlled_by TEXT,
  defense INTEGER,
  quality TEXT,
  tax_value INTEGER,
  notes TEXT
);

CREATE TABLE possessions (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  value TEXT,
  value_florins INTEGER,
  tradeable INTEGER DEFAULT 1,
  negotiation_use TEXT,
  notes TEXT
);

CREATE TABLE relationships (
  id INTEGER PRIMARY KEY,
  character_id INTEGER REFERENCES characters(id),
  related_to TEXT NOT NULL,
  relationship_type TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE rules (
  id INTEGER PRIMARY KEY,
  category TEXT NOT NULL,
  topic TEXT NOT NULL,
  summary TEXT NOT NULL,
  details TEXT,
  page_ref TEXT
);

CREATE TABLE siblings (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  relation TEXT NOT NULL,
  mother TEXT NOT NULL,
  age_approx TEXT,
  status TEXT NOT NULL,
  location TEXT,
  married_to TEXT,
  needs TEXT,
  also_in_table TEXT,
  notes TEXT
);

CREATE TABLE strategic_insights (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,
  category TEXT NOT NULL,
  title TEXT NOT NULL,
  detail TEXT NOT NULL
);

CREATE TABLE territories (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  region TEXT,
  defense INTEGER,
  coastal INTEGER DEFAULT 0,
  sack_value INTEGER,
  tax_value INTEGER,
  controlled_by TEXT,
  notes TEXT
);

CREATE TABLE timeline (
  id INTEGER PRIMARY KEY,
  year INTEGER,
  event TEXT NOT NULL,
  relevance TEXT
);

CREATE TABLE vatican_offices (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT,
  salary INTEGER,
  salary_display TEXT,
  current_holder TEXT,
  replaced_how TEXT,
  powers TEXT,
  notes TEXT
);

CREATE TABLE world_facts (
  id INTEGER PRIMARY KEY,
  number INTEGER,
  topic TEXT,
  summary TEXT NOT NULL
);
