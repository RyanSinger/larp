#!/usr/bin/env python3
"""Small helpers for authoring a character database safely.

Hand-written `INSERT ... VALUES (?, ?, ...)` with positional tuples is the source
of the binding-count slips that bit every build (one stray `?`, one missing
value, and the whole transaction rolls back). Author with these instead: the
statement is built from the dict keys, so columns and values can never drift.

    from dbhelpers import insert, insert_many, update
    insert(con, "pc", id=1, name="Cardinal ...", role="Cardinal", age=49)
    insert_many(con, "goals", [
        {"priority": 1, "description": "..."},
        {"priority": 2, "description": "...", "sub_goals": "..."},
    ])
    update(con, "characters", "id=?", (7,), is_ally=1, is_key=1, our_opinion="...")

Call con.commit() yourself when done.
"""


def _quote(name):
    return '"' + name.replace('"', '""') + '"'


def insert(con, table, **fields):
    """Insert one row from keyword fields. Returns the new rowid."""
    cols = list(fields)
    placeholders = ", ".join("?" for _ in cols)
    sql = f'insert into {_quote(table)} ({", ".join(_quote(c) for c in cols)}) values ({placeholders})'
    return con.execute(sql, [fields[c] for c in cols]).lastrowid


def insert_many(con, table, rows):
    """Insert a list of dict rows. Rows may have different keys; each is built
    independently, so optional columns can simply be omitted."""
    for r in rows:
        insert(con, table, **r)


def update(con, table, where, params=(), **fields):
    """UPDATE table SET <fields> WHERE <where>, with positional <params> bound
    after the field values. Example: update(con,'characters','id=?',(7,),is_key=1)."""
    cols = list(fields)
    sets = ", ".join(f"{_quote(c)}=?" for c in cols)
    sql = f'update {_quote(table)} set {sets} where {where}'
    return con.execute(sql, [fields[c] for c in cols] + list(params))
