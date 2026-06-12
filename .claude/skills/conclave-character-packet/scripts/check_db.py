#!/usr/bin/env python3
"""Sanity report for a character-packet database before building the booklet.

Usage: python3 check_db.py [DB_PATH]   (default conclave.db)

Prints row counts and warns about empty tables that the booklet needs.
"""
import sys
import sqlite3

PC_CRITICAL = ["pc", "characters", "goals"]
SHARED_EXPECTED = ["rules", "world_facts", "forms_of_address", "mercenaries",
                   "marriage_candidates", "territories", "timeline"]


def main(argv):
    db = argv[0] if argv else "conclave.db"
    con = sqlite3.connect(db)
    tables = [r[0] for r in con.execute(
        "select name from sqlite_master where type='table' and name not like 'sqlite_%' order by name")]
    counts = {t: con.execute(f'select count(*) from "{t}"').fetchone()[0] for t in tables}
    width = max(len(t) for t in tables)
    print(f"{db}: {len(tables)} tables")
    for t in tables:
        print(f"  {t.ljust(width)}  {counts[t]}")

    warns = []
    for t in PC_CRITICAL + SHARED_EXPECTED:
        if t not in counts:
            warns.append(f"missing table: {t}")
        elif counts[t] == 0:
            warns.append(f"empty table: {t}")
    if counts.get("pc", 0) > 1:
        warns.append("pc table should have exactly one row")
    if not con.execute("select count(*) from characters where is_ally=1 or papabile=1").fetchone()[0]:
        warns.append("no characters flagged is_ally or papabile -> Section 2 will be empty")

    print()
    if warns:
        print("WARNINGS:")
        for w in warns:
            print(f"  ! {w}")
    else:
        print("OK: all required tables present and populated.")
    con.close()


if __name__ == "__main__":
    main(sys.argv[1:])
