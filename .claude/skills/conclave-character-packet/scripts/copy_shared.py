#!/usr/bin/env python3
"""Seed a new character's database with the shared game world from an existing
packet, so you only have to author the PC-relative content from the new sheet.

Usage:
    python3 copy_shared.py SOURCE_DB TARGET_DB

The game world is identical for every player, so re-extracting it from the PDFs
for each character is wasted effort and a source of error. This copies it across:

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
    pc, goals, possessions, courtiers, siblings, relationships,
    strategic_insights, messages, marriage_candidates, claims, forces

Caveat: a shared roster may still carry the SOURCE character's framing in a few
names or titles (e.g. "Uncle Giovanni della Rovere", "Aunt Costanza"). Relabel
those relatives for the new PC after copying.
"""
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
    if len(argv) < 2:
        sys.exit("usage: python3 copy_shared.py SOURCE_DB TARGET_DB")
    src = sqlite3.connect(argv[0])
    dst = sqlite3.connect(argv[1])

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
