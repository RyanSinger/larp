#!/usr/bin/env python3
"""Build shared-world.db: the canonical, player-neutral shared game world.

The shared world is identical for every character and comes from the game
documents, NOT from any one player. Seeding a new packet from another player's
database carried that player's perspective into supposedly-shared columns
("Uncle Fabrizio", their starting state, "your ally Isabella"). This produces a
neutral seed instead.

Two kinds of shared data, two sources:

  The cast (characters table) comes from the canonical roster file
  reference/cast.json, which is derived directly from the game's Dramatis
  Personae (the Character List PDF), the public and player-neutral description
  of everyone in play. Sourcing the cast from the document, rather than from one
  player's packet, is what keeps second-person framing out of the shared world.

  The objective reference tables (rules, world facts, timeline, offices, ports,
  territories, forms of address, monastic orders, mercenary combat specs, the
  family roster, and the run-of-play logistics) are harvested from a populated
  BASE_DB. These carry no perspective: they are the same document-derived facts
  for every player. The family key_members and logistics are filtered so no one
  player's framing or starting state leaks through.

Usage:
    python3 build_shared_world.py BASE_DB [OUT_DB]
where BASE_DB is any populated packet to harvest the objective reference tables
from, and OUT_DB defaults to <skill>/shared-world.db. Regenerate this if the
game materials change. copy_shared.py seeds from the result by default.
"""
import os
import json
import sys
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "..", "schema.sql")
CAST = os.path.join(HERE, "..", "reference", "cast.json")

VERBATIM = ["rules", "world_facts", "timeline", "forms_of_address", "ports",
            "territories", "vatican_offices", "monastic_orders"]
MERC_SPECS = ["id", "name", "faction", "experience", "specializes_in", "wont_attack",
              "num_armies", "reserve_commander", "min_price"]
# logistics rows that are the PC's own state, not shared run-of-play info
PC_LOGISTICS = ("Your Starting State", "Special Power")
# neutral, third-person family rosters (no "Uncle/Aunt/your" framing)
FAM_KEY = {
    "Sanseverino": "Cardinal Federico Sanseverino and his mercenary brothers; Antonello, Prince of Salerno (exiled).",
    "Montefeltro": "Duke Guidobaldo of Urbino and Duchess Elizabetta Gonzaga; Antonio da Montefeltro (captain).",
    "della Rovere": "Cardinal Giuliano della Rovere; his heir Cardinal Raffaele Riario; Giovanni della Rovere, Duke of Sora; cousin Domenico.",
    "Colonna": "Cardinal Giovanni Colonna; Fabrizio Colonna, Grand Constable of Naples; the generals Prospero and Sciarra.",
    "Malatesta": "Pandolfo Malatesta, Lord of Rimini; the mercenaries Carlo and Troilo.",
}


def main(argv):
    if not argv:
        sys.exit("usage: build_shared_world.py BASE_DB [OUT_DB]")
    base = sqlite3.connect(argv[0])
    out_path = argv[1] if len(argv) > 1 else os.path.join(HERE, "..", "shared-world.db")
    if os.path.exists(out_path):
        os.remove(out_path)
    out = sqlite3.connect(out_path)
    out.executescript(open(SCHEMA).read())

    def cols(con, t):
        return [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]

    for t in VERBATIM:
        rows = base.execute(f'select * from "{t}"').fetchall()
        names = cols(base, t)
        use = [c for c in names if c in cols(out, t)]
        idx = [names.index(c) for c in use]
        out.executemany(f'insert into "{t}" ({",".join(use)}) values ({",".join("?"*len(use))})',
                        [[r[i] for i in idx] for r in rows])

    # cast: the canonical, document-derived roster (Dramatis Personae). Only the
    # base, public columns; every PC-relative column stays blank for each player.
    cast = json.load(open(CAST))["characters"]
    out_cols = cols(out, "characters")
    keys = [k for k in cast[0].keys() if k in out_cols] if cast else []
    out.executemany(
        f'insert into characters ({",".join(keys)}) values ({",".join("?"*len(keys))})',
        [[r.get(k) for k in keys] for r in cast])

    # mercenaries: combat specs only
    mn = cols(base, "mercenaries")
    muse = [c for c in MERC_SPECS if c in mn]
    out.executemany(f'insert into mercenaries ({",".join(muse)}) values ({",".join("?"*len(muse))})',
                    base.execute(f'select {",".join(muse)} from mercenaries').fetchall())

    # families: roster with neutral key_members, no our_connection
    for r in base.execute("select name, seat, faction, key_members, notes from families"):
        name, seat, faction, km, notes = r
        for k, v in FAM_KEY.items():
            if k.lower() in (name or "").lower():
                km = v
                break
        out.execute("insert into families (name,seat,faction,key_members,notes) values (?,?,?,?,?)",
                    (name, seat, faction, km, notes))

    # logistics: run-of-play only, not the PC's own state
    for r in base.execute("select topic, details from logistics"):
        if r[0] not in PC_LOGISTICS:
            out.execute("insert into logistics (topic, details) values (?,?)", (r[0], r[1]))

    out.commit()
    counts = {t: out.execute(f'select count(*) from "{t}"').fetchone()[0]
              for t in ["characters", "mercenaries", "families", "logistics"] + VERBATIM}
    out.close()
    print(f"wrote {out_path}")
    print(f"  cast from {os.path.relpath(CAST, HERE)}")
    for t, n in counts.items():
        print(f"  {t}: {n}")


if __name__ == "__main__":
    main(sys.argv[1:])
