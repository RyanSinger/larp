#!/usr/bin/env python3
"""Seed a new character's database with the shared game world, so you only have
to author the PC-relative content from the new sheet.

Usage:
    python3 copy_shared.py TARGET_DB            # from the bundled neutral world
    python3 copy_shared.py SOURCE_DB TARGET_DB  # from a specific packet

The game world (rules, the cast's base facts, mercenary specs, the family roster,
world facts, timeline, offices, ports, territories, forms of address, run-of-play
logistics) is identical for every player and comes from the game documents, not
from any one player. Seed from the bundled, player-neutral `shared-world.db`
(built by build_shared_world.py); do NOT seed from another character's packet
unless you mean to, because that carries their perspective ("Uncle Fabrizio",
their starting state) into supposedly-shared columns. This copies across:

  Verbatim (fully shared):
    rules, world_facts, timeline, forms_of_address, ports, territories,
    vatican_offices, monastic_orders, logistics
  Objective facts only (PC-relative columns left blank for you to author):
    characters   -> identity, age, rank, role, faction, location, papabile,
                    pronunciation, monastic_order, plus what_they_want and notes
                    as a neutral baseline. Reset: our_opinion, what_we_want,
                    what_we_offer, what_to_avoid, is_ally, is_contact, is_key.
    mercenaries  -> name and combat specs only. Reset: priority, natural_buyers, notes.
    families     -> name, seat, faction, key_members, notes. Reset: our_connection.

NOT copied (these are entirely the new PC's, author them from the sheet):
    pc, goals, possessions, courtiers, siblings, relationships, strategic_insights,
    messages, marriage_candidates, claims, forces, external_powers, agenda

The bundled shared-world.db is already neutral. If you instead seed from another
character's packet (two-arg form), scrub the source's perspective afterward:
relative names ("Uncle Fabrizio"), "your uncle" phrasing in notes/families/
logistics, and that player's starting state. check_db flags the clearest cases.
"""
import os
import sys
import sqlite3

VERBATIM = ['rules', 'world_facts', 'timeline', 'forms_of_address', 'ports',
            'territories', 'vatican_offices', 'monastic_orders', 'logistics']
CHAR_COLS = ['id', 'name', 'title', 'surname', 'nickname', 'age', 'rank', 'role',
             'faction', 'location', 'papabile', 'pronunciation', 'monastic_order',
             'what_they_want', 'notes']
MERC_COLS = ['id', 'name', 'faction', 'experience', 'specializes_in', 'wont_attack',
             'num_armies', 'reserve_commander', 'min_price']
FAM_COLS = ['name', 'seat', 'faction', 'key_members', 'notes']


def main(argv):
    if not argv:
        sys.exit("usage: python3 copy_shared.py [SOURCE_DB] TARGET_DB\n"
                 "  one arg: seed TARGET_DB from the bundled neutral shared-world.db\n"
                 "  two args: seed TARGET_DB from your own SOURCE_DB")
    if len(argv) == 1:
        here = os.path.dirname(os.path.abspath(__file__))
        source, target = os.path.join(here, "..", "shared-world.db"), argv[0]
        if not os.path.exists(source):
            sys.exit("no bundled shared-world.db; build it with build_shared_world.py, "
                     "or pass an explicit SOURCE_DB")
    else:
        source, target = argv[0], argv[1]
    src = sqlite3.connect(source)
    dst = sqlite3.connect(target)

    def cols(con, t):
        return [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]

    def copy(t, want):
        if t not in [r[0] for r in src.execute("select name from sqlite_master where type='table'")]:
            return 0
        use = [c for c in want if c in cols(src, t) and c in cols(dst, t)]
        rows = src.execute(f'select {",".join(use)} from "{t}"').fetchall()
        dst.executemany(
            f'insert into "{t}" ({",".join(use)}) values ({",".join("?" * len(use))})', rows)
        return len(rows)

    report = []
    for t in VERBATIM:
        report.append((t, copy(t, cols(src, t))))
    report.append(('characters', copy('characters', CHAR_COLS)))
    report.append(('mercenaries', copy('mercenaries', MERC_COLS)))
    report.append(('families', copy('families', FAM_COLS)))
    dst.commit()
    dst.close()

    for t, n in report:
        print(f"  copied {n:>3} rows -> {t}")
    print("\nNow author from the new sheet: pc, goals, marriage_candidates (the PC's own "
          "brides/grooms),\npossessions, courtiers, siblings, families.our_connection, "
          "strategic_insights, and the\nrelational framing on characters (our_opinion, what_we_*, "
          "is_ally, is_key) and mercenaries.")


if __name__ == "__main__":
    main(sys.argv[1:])
