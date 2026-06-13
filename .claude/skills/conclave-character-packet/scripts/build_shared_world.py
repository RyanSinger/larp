#!/usr/bin/env python3
"""Build shared-world.db: the canonical, player-neutral shared game world.

The shared world (rules, the cast's base facts, mercenary specs, the family
roster, world facts, timeline, offices, ports, territories, forms of address,
and the run-of-play logistics) is identical for every character and comes from
the game documents, NOT from any one player. Seeding a new packet from another
player's database carried that player's perspective into supposedly-shared
columns ("Uncle Fabrizio", their starting state). This produces a neutral seed
instead: the same document-derived facts with every player overlay stripped.

Usage:
    python3 build_shared_world.py BASE_DB [OUT_DB]
where BASE_DB is any populated packet to harvest the objective facts from, and
OUT_DB defaults to <skill>/shared-world.db. Regenerate this if the game
materials change. copy_shared.py seeds from the result by default.
"""
import os
import re
import sys
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "..", "schema.sql")

VERBATIM = ["rules", "world_facts", "timeline", "forms_of_address", "ports",
            "territories", "vatican_offices", "monastic_orders"]
# characters whose facts are shared (base columns only; all PC-relative framing
# is left blank for each character to author). PC-specific relatives that belong
# to one player's sheet are not part of the shared cast.
CHAR_BASE = ["id", "name", "title", "surname", "nickname", "age", "rank", "role",
             "faction", "location", "papabile", "pronunciation", "monastic_order",
             "what_they_want"]
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
# relative prefixes that are one player's framing of a shared figure
PREFIX = re.compile(r"^(Uncle|Aunt|Great-uncle|Great-aunt|Brother|Sister|Cousin)\s+", re.I)


def neutral_name(name):
    return PREFIX.sub("", name or "").strip()


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

    # characters: shared base facts only, names neutralised, framing blank
    names = cols(base, "characters")
    keep = [c for c in CHAR_BASE if c in names and c in cols(out, "characters")]
    ni = names.index("name")
    for r in base.execute("select * from characters order by id"):
        orig = r[ni] or ""
        # one player's private relatives (e.g. "Aunt Costanza") are not shared cast
        if re.match(r"^(Aunt|Great-aunt)\s+", orig, re.I):
            continue
        nm = neutral_name(orig)
        vals = []
        for c in keep:
            v = r[names.index(c)]
            vals.append(nm if c == "name" else v)
        out.execute(f'insert into characters ({",".join(keep)}) values ({",".join("?"*len(keep))})', vals)

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
    for t, n in counts.items():
        print(f"  {t}: {n}")


if __name__ == "__main__":
    main(sys.argv[1:])
