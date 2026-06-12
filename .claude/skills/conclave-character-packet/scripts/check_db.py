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

    # Advisory notes on curation and depth (quality, not errors)
    notes = []
    char_cols = [r[1] for r in con.execute("PRAGMA table_info(characters)")]
    if "is_key" not in char_cols:
        notes.append("characters has no is_key column: this DB predates the curation flag, so "
                     "Section 2 falls back to all papabili + allies. Migrate to the current schema "
                     "and flag ~10-14 figures with is_key for a tighter, play-usable section.")
    else:
        nkey = con.execute("select count(*) from characters where is_key=1").fetchone()[0]
        if nkey == 0:
            notes.append("no characters flagged is_key: Section 2 will render every papabile and "
                         "ally (a busier, uncurated set). Flag ~10-14 with is_key for a tighter section.")
        elif nkey > 16:
            notes.append(f"is_key flags {nkey} characters: consider trimming to ~10-14 so Section 2 "
                         "stays usable at the table.")
    ins = counts.get("strategic_insights", 0)
    if ins < 6:
        notes.append(f"only {ins} strategic_insights: these are the heart of the playbook "
                     "(commitments, phased strategy, and the off-roster situation a monarch's game "
                     "depends on). Author more, and keep adding them as the game unfolds.")

    print()
    if warns:
        print("WARNINGS:")
        for w in warns:
            print(f"  ! {w}")
    else:
        print("OK: all required tables present and populated.")
    if notes:
        print("\nNOTES (quality):")
        for n in notes:
            print(f"  - {n}")
    con.close()


if __name__ == "__main__":
    main(sys.argv[1:])
