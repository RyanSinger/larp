#!/usr/bin/env python3
"""Create an empty character-packet database from schema.sql.

Usage:
    python3 init_db.py [DB_PATH] [SCHEMA_PATH]

Defaults: DB_PATH=conclave.db, SCHEMA_PATH=<skill>/schema.sql
Refuses to overwrite an existing database unless --force is given.
"""
import os
import sys
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SCHEMA = os.path.join(HERE, "..", "schema.sql")


def main(argv):
    force = "--force" in argv
    args = [a for a in argv if a != "--force"]
    db_path = args[0] if len(args) > 0 else "conclave.db"
    schema_path = args[1] if len(args) > 1 else DEFAULT_SCHEMA

    if os.path.exists(db_path) and not force:
        sys.exit(f"refusing to overwrite existing {db_path} (pass --force)")
    if force and os.path.exists(db_path):
        os.remove(db_path)

    with open(schema_path) as f:
        schema = f.read()
    con = sqlite3.connect(db_path)
    con.executescript(schema)
    con.commit()
    tables = [r[0] for r in con.execute(
        "select name from sqlite_master where type='table' and name not like 'sqlite_%' order by name")]
    con.close()
    print(f"created {db_path} with {len(tables)} tables:")
    print("  " + ", ".join(tables))


if __name__ == "__main__":
    main(sys.argv[1:])
