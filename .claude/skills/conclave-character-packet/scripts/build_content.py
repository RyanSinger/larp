#!/usr/bin/env python3
"""Generate booklet-content.js (the flow content) from a character database.

The booklet is a faithful mirror of the schema: every reference section and
worksheet is rendered from the tables, in the canonical Temptemus Papam design
(class names match booklet.css). The single source of truth is the database;
re-run this after any DB edit, then render with generate_pdf.cjs.

Usage:
    python3 build_content.py [DB_PATH] [OUT_PATH]

Defaults: DB_PATH=conclave.db, OUT_PATH=booklet/booklet-content.js

Section selection rules (deterministic):
  - Section 2 "Key Profiles": characters with is_ally=1 OR papabile=1, as cards.
  - Section 3 "All Other Characters": the rest, grouped by role, as tables.
  - Worksheets prefill writable rows from mercenaries / marriage_candidates /
    characters (cardinals) / possessions / courtiers.
"""
import os
import re
import sys
import json
import html
import sqlite3

CROSS = "&#10016;"      # heavy cross used as rubric ornament
FLEUR = "&#10070;"      # fleuron
BOX = "&#9744;"         # ballot box (empty checkbox)
KICK = ('<span class="keys">' + CROSS + '</span>&ensp;Sede Vacante &middot; '
        'Anno Domini MCDXCII&ensp;<span class="keys">' + CROSS + '</span>')


def esc(v):
    if v is None:
        return ""
    return html.escape(str(v), quote=False)


def cols(con, table):
    return [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]


def rows(con, sql, params=()):
    cur = con.execute(sql, params)
    names = [d[0] for d in cur.description]
    return [dict(zip(names, r)) for r in cur.fetchall()]


def pc_row(con):
    """The single PC row, or {} if the table is empty/absent."""
    try:
        r = rows(con, "select * from pc where id=1")
        return r[0] if r else {}
    except sqlite3.OperationalError:
        return {}


def writerows(n, ncells, first_class=None, first_text=""):
    """Blank writable rows for handwriting."""
    out = []
    for _ in range(n):
        cells = []
        for i in range(ncells):
            if i == 0 and first_class:
                cells.append(f'<td class="{first_class}">{first_text}</td>')
            else:
                cells.append("<td></td>")
        out.append('<tr class="write-row">' + "".join(cells) + "</tr>")
    return "\n".join(out)


# ---------------------------------------------------------------- sections
def sec_personal(con):
    pc = pc_row(con)
    name = esc(pc.get("name") or "The Cardinal")
    sub = esc(pc.get("subtitle") or "")
    st = " &bull; ".join(filter(None, [
        f"Age {pc['age']}" if pc.get("age") else None,
        esc(pc.get("rank")), esc(pc.get("faction")), esc(pc.get("monastic_order"))]))
    origin = esc(pc.get("origin"))
    cv = esc(pc.get("combat_value"))
    metas = [
        ("Territory", pc.get("territory")),
        ("Money", pc.get("money")),
        ("Port", pc.get("port")),
        ("Special Power", pc.get("special_power")),
        ("Evidence of Crime", pc.get("evidence_of_crime")),
        ("Property in Rome", pc.get("property_in_rome")),
    ]
    meta_html = "<br>\n".join(f"<strong>{k}:</strong> {esc(v)}"
                              for k, v in metas if v)

    goals = rows(con, "select * from goals order by priority")
    goals_html = "\n".join(f"<li>{esc(g['description'])}</li>" for g in goals)

    allies = rows(con, "select name, title from characters where is_ally=1 order by id")
    allies_html = "<br>\n".join(esc(a["name"]) for a in allies)

    rem = esc(pc.get("key_reminders") or "")

    h = [f'<h2>1. Personal Quick Reference</h2>']
    h.append('<div class="namebar">')
    h.append(f'  <div class="nm">{name}<small>{sub}</small></div>')
    bottom = st + (f"<br>{origin}" if origin else "") + (f" &bull; Combat Value {cv}" if cv else "")
    h.append(f'  <div class="st">{bottom}</div>')
    h.append('</div>')
    if meta_html:
        h.append(f'<div class="qr-meta">\n{meta_html}\n</div>')
    if goals_html:
        h.append('<h3>Goals (Ranked)</h3>')
        h.append(f'<ol class="goals">\n{goals_html}\n</ol>')
    if allies_html:
        h.append('<h3>Starting Allies <span class="note" style="text-transform:none;font-size:7pt;">'
                 '&mdash; may communicate between sessions</span></h3>')
        h.append(f'<div class="qr-cols">\n{allies_html}\n</div>')
    if rem:
        h.append('<h3>Key Reminders</h3>')
        h.append(f'<div class="qr-box">{rem}</div>')
    return "\n".join(h)


def _profile_card(c):
    name = esc(c.get("title") and f"{c['title']} {c['name']}" or c["name"])
    # prefer "Title Name"; fall back to plain name
    disp = esc(c["name"])
    if c.get("nickname"):
        disp += f' (&ldquo;{esc(c["nickname"])}&rdquo;)'
    tag = ' <span class="ally-tag">ALLY</span>' if c.get("is_ally") else ""
    sub = " &bull; ".join(filter(None, [
        f"Age {c['age']}" if c.get("age") else None,
        esc(c.get("location")), esc(c.get("rank")),
        esc(c.get("monastic_order")), esc(c.get("title")),
        "Papabile" if c.get("papabile") else None]))
    out = ['<div class="profile">']
    out.append(f'<div class="profile-header">{disp}{tag}</div>')
    out.append(f'<div class="profile-sub">{sub}</div>')
    for label, key in [("They want", "what_they_want"), ("You want", "what_we_want"),
                       ("You offer", "what_we_offer"), ("Avoid", "what_to_avoid"),
                       ("Your opinion", "our_opinion")]:
        if c.get(key):
            out.append(f'<div class="profile-row"><strong>{label}:</strong> {esc(c[key])}</div>')
    out.append('</div>')
    return "\n".join(out)


def _key_ids(con):
    """Section 2 full-profile set. Primary path: the figures the skill flagged
    is_key while reading the character sheet, the people this PC will deal with
    most (allies AND the chief rivals they must outmaneuver), kept to a readable
    dozen or so so the section stays useful at the table. Fallback for a DB with
    nothing flagged: every papal contender and ally who is not a family NPC."""
    if "is_key" in cols(con, "characters"):
        keyed = rows(con, "select id from characters where is_key=1")
        if keyed:
            return {r["id"] for r in keyed}
    return {r["id"] for r in rows(
        con, "select id from characters where (papabile=1 or is_ally=1) "
             "and (role is null or role != 'NPC')")}


def sec_key_profiles(con):
    ids = _key_ids(con)
    allc = rows(con, "select * from characters order by (role='Cardinal') desc, is_ally desc, id")
    cs = [c for c in allc if c["id"] in ids]
    body = "\n\n".join(_profile_card(c) for c in cs)
    return f'<h2>2. Key Character Profiles</h2>\n\n{body}'


def _other_table(con, title, role, keyids):
    cs = [c for c in rows(con, "select * from characters where role=? order by id", (role,))
          if c["id"] not in keyids]
    if not cs:
        return ""
    head = (f'<h3>{title}</h3>\n<table class="t-tight">\n<tr>'
            '<th style="width:16%;">Character</th><th style="width:5%;">Age</th>'
            '<th style="width:9%;">Faction</th><th style="width:6%;">Ally?</th>'
            '<th style="width:22%;">They Want</th><th style="width:24%;">Your Angle</th>'
            '<th style="width:18%;">Watch Out</th></tr>')
    body = []
    for c in cs:
        ally = '<span class="ally-tag">YES</span>' if c.get("is_ally") else "No"
        body.append("<tr>"
                    f'<td><strong>{esc(c["name"])}</strong></td>'
                    f'<td>{esc(c.get("age"))}</td>'
                    f'<td>{esc(c.get("faction"))}</td>'
                    f'<td>{ally}</td>'
                    f'<td>{esc(c.get("what_they_want"))}</td>'
                    f'<td>{esc(c.get("what_we_want") or c.get("our_opinion"))}</td>'
                    f'<td>{esc(c.get("what_to_avoid"))}</td></tr>')
    return head + "\n" + "\n".join(body) + "\n</table>"


def sec_all_other(con):
    parts = ['<h2>3. All Other Characters</h2>']
    keyids = _key_ids(con)
    for title, role in [("Remaining Cardinals", "Cardinal"),
                        ("Functionaries", "Functionary"),
                        ("Monarchs", "Monarch"),
                        ("Other Figures", "NPC")]:
        t = _other_table(con, title, role, keyids)
        if t:
            parts.append(t)
    return "\n\n".join(parts)


def sec_mercenaries(con):
    parts = ['<h2>4. Mercenary Reference</h2>']
    for label, exp, note in [("Experienced Commanders", "Experienced", ""),
                             ("Fledgling Commanders (need 40,000 to raise army)", "Fledgling", "")]:
        ms = rows(con, "select * from mercenaries where experience=? order by "
                       "(priority='AVOID'), name", (exp,))
        if not ms:
            continue
        parts.append(f'<h3>{label}</h3>\n<table class="t-tight">\n<tr>'
                     '<th style="width:20%;">Commander</th><th style="width:7%;">Fact.</th>'
                     '<th style="width:24%;">Specializes / Won\'t Attack</th>'
                     '<th style="width:9%;">Min</th><th style="width:9%;">Priority</th>'
                     '<th style="width:31%;">Notes</th></tr>')
        body = []
        for m in ms:
            spec = esc(m.get("specializes_in"))
            wont = esc(m.get("wont_attack"))
            sw = spec + (f"<br><em>Won't: {wont}</em>" if wont else "")
            body.append("<tr>"
                        f'<td><strong>{esc(m["name"])}</strong></td>'
                        f'<td>{esc(m.get("faction"))}</td>'
                        f'<td>{sw}</td>'
                        f'<td>{esc(m.get("min_price"))}</td>'
                        f'<td>{esc(m.get("priority"))}</td>'
                        f'<td>{esc(m.get("notes"))}</td></tr>')
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n\n".join(parts)


def _marriage_table(con, title, typ):
    ms = rows(con, "select * from marriage_candidates where type=? order by id", (typ,))
    if not ms:
        return ""
    rel_col = "relation_to_pc" if "relation_to_pc" in cols(con, "marriage_candidates") else "relation_to_federico"
    head = (f'<h3>{title}</h3>\n<table class="t-tight">\n<tr>'
            '<th style="width:22%;">Name</th><th style="width:18%;">Family</th>'
            '<th style="width:14%;">Rank</th><th style="width:20%;">Relation</th>'
            '<th style="width:26%;">Notes</th></tr>')
    body = []
    for m in ms:
        body.append("<tr>"
                    f'<td><strong>{esc(m["name"])}</strong></td>'
                    f'<td>{esc(m.get("family"))}</td>'
                    f'<td>{esc(m.get("rank"))}</td>'
                    f'<td>{esc(m.get(rel_col))}</td>'
                    f'<td>{esc(m.get("notes"))}</td></tr>')
    return head + "\n" + "\n".join(body) + "\n</table>"


def sec_marriages(con):
    parts = ['<h2>5. Marriage Candidates</h2>']
    for title, typ in [("Brides", "Bride"), ("Grooms", "Groom"), ("Nunnery", "Nunnery")]:
        t = _marriage_table(con, title, typ)
        if t:
            parts.append(t)
    return "\n\n".join(parts)


def sec_possessions(con):
    parts = ['<h2>6. Possessions &amp; Courtiers</h2>']
    ps = rows(con, "select * from possessions order by id")
    if ps:
        parts.append('<h3>Tradeable Possessions</h3>\n<table class="t-tight">\n<tr>'
                     '<th style="width:26%;">Item</th><th style="width:16%;">Value</th>'
                     '<th style="width:58%;">Use in Negotiation</th></tr>')
        body = [("<tr>"
                 f'<td><strong>{esc(p["name"])}</strong></td>'
                 f'<td>{esc(p.get("value") or p.get("value_florins"))}</td>'
                 f'<td>{esc(p.get("negotiation_use") or p.get("notes"))}</td></tr>') for p in ps]
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    cs = rows(con, "select * from courtiers order by id")
    if cs:
        parts.append('<h3>Courtiers</h3>\n<table class="t-tight">\n<tr>'
                     '<th style="width:22%;">Name</th><th style="width:24%;">Specialty</th>'
                     '<th style="width:54%;">Deployment Ideas</th></tr>')
        body = [("<tr>"
                 f'<td><strong>{esc(c["name"])}</strong></td>'
                 f'<td>{esc(c.get("specialty"))}</td>'
                 f'<td>{esc(c.get("deployment_ideas") or c.get("notes"))}</td></tr>') for c in cs]
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n\n".join(parts)


def sec_forms(con):
    fs = rows(con, "select * from forms_of_address order by id")
    parts = ['<h2>7. Forms of Address</h2>',
             '<table class="t-tight">\n<tr><th style="width:26%;">Rank or Person</th>'
             '<th style="width:30%;">Proper Address</th><th style="width:24%;">Rude / Insulting</th>'
             '<th style="width:20%;">Notes</th></tr>']
    body = [("<tr>"
             f'<td><strong>{esc(f["rank_or_name"])}</strong></td>'
             f'<td>{esc(f.get("formal_address"))}</td>'
             f'<td>{esc(f.get("rude_address"))}</td>'
             f'<td>{esc(f.get("notes"))}</td></tr>') for f in fs]
    return parts[0] + "\n" + parts[1] + "\n" + "\n".join(body) + "\n</table>"


def _family_tree(con):
    """A scannable monospace family tree from the siblings table, grouped by
    mother (so multiple marriages read correctly) and split sister/brother.
    Header comes from pc.house, falling back to the PC name."""
    sibs = rows(con, "select * from siblings order by id")
    if not sibs:
        return ""
    pc = pc_row(con)
    header = pc.get("house") or (pc.get("name") or "Your House")
    lines = [esc(header)]
    you = esc(pc.get("name") or "You")
    lines.append(f" YOU: {you}" + (f", age {pc['age']}" if pc.get("age") else ""))

    # group by mother, preserving first-seen order; collapse unknown mothers
    # (e.g. "Unknown", "Unknown (earlier wife)") into one "earlier marriage" group
    order, groups, disp = [], {}, {}
    for s in sibs:
        m = s.get("mother") or ""
        k = "__earlier__" if "unknown" in m.lower() else m
        if k not in groups:
            order.append(k)
            groups[k] = []
            disp[k] = None if k == "__earlier__" else m
        groups[k].append(s)

    for k in order:
        g = groups[k]
        mother = disp[k]
        is_full = any("full" in (s.get("relation") or "").lower() for s in g)
        if k == "__earlier__":
            par = " (by an earlier marriage)"
        elif mother:
            par = f" ({'mother' if is_full else 'stepmother'}: {esc(mother)})"
        else:
            par = ""
        lines.append(" " + ("Full siblings" if is_full else "Half-siblings") + par)
        for word, needle in (("Sisters", "sister"), ("Brothers", "brother")):
            names = []
            for s in g:
                if needle in (s.get("relation") or "").lower():
                    nm = esc((s.get("name") or "").split()[0])
                    st = (s.get("status") or "").strip().rstrip(".")
                    if st and len(st) < 14:
                        nm += f" ({esc(st).lower()})"
                    names.append(nm)
            if names:
                lines.append(f"   {word}: " + ", ".join(names))
    return '<div class="family-tree">' + "\n".join(lines) + "</div>"


def sec_family(con):
    parts = ['<h2>8. Key Family Relationships</h2>']
    tree = _family_tree(con)
    if tree:
        parts.append('<h3>Your Direct Family</h3>\n' + tree)
    sibs = rows(con, "select * from siblings order by id")
    if sibs:
        parts.append('<h3>Siblings: What Each One Needs</h3>\n<table class="t-tight">\n<tr>'
                     '<th style="width:20%;">Name</th><th style="width:12%;">Age</th>'
                     '<th style="width:16%;">Status</th>'
                     '<th style="width:52%;">Needs / Notes</th></tr>')
        body = [("<tr>"
                 f'<td><strong>{esc(s["name"])}</strong></td>'
                 f'<td>{esc(s.get("age_approx"))}</td>'
                 f'<td>{esc(s.get("status"))}</td>'
                 f'<td>{esc(s.get("needs") or s.get("notes"))}</td></tr>') for s in sibs]
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    fams = rows(con, "select * from families order by id")
    if fams:
        parts.append('<h3>How You Connect to Each Major Family</h3>\n<table class="t-tight">\n<tr>'
                     '<th style="width:16%;">Family</th><th style="width:14%;">Seat</th>'
                     '<th style="width:10%;">Faction</th><th style="width:34%;">Your Connection</th>'
                     '<th style="width:26%;">Key Members</th></tr>')
        body = [("<tr>"
                 f'<td><strong>{esc(f["name"])}</strong></td>'
                 f'<td>{esc(f.get("seat"))}</td>'
                 f'<td>{esc(f.get("faction"))}</td>'
                 f'<td>{esc(f.get("our_connection"))}</td>'
                 f'<td>{esc(f.get("key_members"))}</td></tr>') for f in fams]
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n\n".join(parts)


def sec_rules(con):
    parts = ['<h2>9. Rules Mechanics Quick Reference</h2>']
    cats = [r["category"] for r in rows(con,
            "select category, min(id) m from rules group by category order by m")]
    for cat in cats:
        rs = rows(con, "select * from rules where category=? order by id", (cat,))
        parts.append(f'<h3>{esc(cat)}</h3>\n<table class="t-tight">\n<tr>'
                     '<th style="width:24%;">Topic</th><th style="width:54%;">Summary</th>'
                     '<th style="width:22%;">Details</th></tr>')
        body = [("<tr>"
                 f'<td><strong>{esc(r["topic"])}</strong></td>'
                 f'<td>{esc(r.get("summary"))}</td>'
                 f'<td>{esc(r.get("details"))}</td></tr>') for r in rs]
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n\n".join(parts)


def sec_pronunciation(con):
    cs = rows(con, "select name, pronunciation, role from characters "
                   "where pronunciation is not null and pronunciation!='' order by role, name")
    parts = ['<h2>10. Pronunciation Guide</h2>']
    if not cs:
        return parts[0]
    by_role = {}
    for c in cs:
        by_role.setdefault(c.get("role") or "Other", []).append(c)
    for role, group in by_role.items():
        parts.append(f'<h3>{esc(role)}s</h3>\n<table class="t-tight">\n'
                     '<tr><th style="width:40%;">Name</th><th style="width:60%;">Say</th></tr>')
        body = [(f'<tr><td><strong>{esc(c["name"])}</strong></td>'
                 f'<td>{esc(c["pronunciation"])}</td></tr>') for c in group]
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n\n".join(parts)


def sec_logistics(con):
    ls = rows(con, "select * from logistics order by id")
    parts = ['<h2>11. Game Logistics</h2>',
             '<table class="t-tight">\n<tr><th style="width:26%;">Topic</th>'
             '<th style="width:74%;">Details</th></tr>']
    body = [(f'<tr><td><strong>{esc(l["topic"])}</strong></td>'
             f'<td>{esc(l["details"])}</td></tr>') for l in ls]
    return parts[0] + "\n" + parts[1] + "\n" + "\n".join(body) + "\n</table>"


def sec_checklist(con):
    pc = pc_row(con)
    name = esc(pc.get("name") or "The Cardinal")
    sub = esc(pc.get("subtitle") or "")
    right = " &bull; ".join(filter(None, [
        f"Age {pc['age']}" if pc.get("age") else None, esc(pc.get("rank")),
        esc(pc.get("faction")), esc(pc.get("monastic_order"))]))
    out = ['<h2 style="margin-top:14pt;">12. Starting State Checklist</h2>',
           '<div class="qr-box">',
           '<table style="border:none; margin-bottom:6pt;"><tr>',
           f'<td style="border:none; width:50%;"><strong>{name}</strong><br>{sub}</td>',
           f'<td style="border:none; width:50%; text-align:right;">{right}</td></tr></table>',
           '<h3>Verify Your Envelope on Day 1</h3>',
           '<table style="border:none; font-size:8.5pt;">']
    items = ["Character sheet and secret goals", "Starting money and dowry funds",
             "Mercenary contacts and any signed contracts", "Possessions and items of value",
             "Courtiers", "Letters of introduction", "Marriage candidate list",
             "Voting tokens"]
    for it in items:
        out.append(f'<tr><td style="border:none; width:4%; vertical-align:top;">{BOX}</td>'
                   f'<td style="border:none;">{esc(it)}</td></tr>')
    out.append('</table>\n</div>')
    return "\n".join(out)


def sec_map(con):
    parts = ['<h2>13. Map of Europe in 1492</h2>',
             '<img src="europe-1492-map.jpg" alt="Map of Europe in 1492" '
             'style="width:100%; border:0.5pt solid #999; margin-bottom:6pt;">']
    ts = rows(con, "select * from territories order by id")
    if ts:
        parts.append('<table style="font-size:8pt;">\n<tr><th style="width:22%;">Territory</th>'
                     '<th style="width:14%;">Def</th><th style="width:18%;">Sack</th>'
                     '<th style="width:18%;">Tax</th><th style="width:28%;">Controller</th></tr>')
        body = [("<tr>"
                 f'<td><strong>{esc(t["name"])}</strong></td>'
                 f'<td>{esc(t.get("defense"))}</td>'
                 f'<td>{esc(t.get("sack_value"))}</td>'
                 f'<td>{esc(t.get("tax_value"))}</td>'
                 f'<td>{esc(t.get("controlled_by"))}</td></tr>') for t in ts]
        parts.append(parts.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n".join(parts)


# ---------------------------------------------------------------- worksheets
def sheet_head(title, pcname):
    return ('<header class="sheet-head pb">\n'
            f'  <div class="kicker">{KICK}</div>\n'
            f'  <h1>{title}</h1>\n'
            f'  <div class="byline">{pcname} &middot; In Conclave at Rome</div>\n'
            f'  <div class="rule"><span class="fleuron">{FLEUR}</span></div>\n'
            '</header>')


def ws_mercenary(con, pcname):
    out = [sheet_head("Mercenary Deal Tracker", pcname)]
    out.append('<div class="reminder-box">\n<strong>Pricing.</strong> 40,000 fl. minimum '
               '(real profit). 20,000 bare minimum. 50,000 is good pay; 60,000+ very good. '
               'Fledglings cannot go below 40,000.<br>\n<strong>Remember.</strong> The coin goes '
               'to the mercenaries, never your own purse. Your first contract sets your faction '
               'alignment for the rest. Mercenaries will not fight close kin. Alliances and '
               'marriages can be worth more than gold.\n</div>')
    for label, exp in [("Experienced Commanders", "Experienced"),
                       ("Fledgling Commanders (need 40,000)", "Fledgling")]:
        ms = rows(con, "select name, faction from mercenaries where experience=? order by name", (exp,))
        out.append(f'<h3>{label}</h3>\n<table>\n<tr>'
                   '<th style="width:22%;">Commander</th><th style="width:6%;">Fact.</th>'
                   '<th style="width:18%;">Buyer</th><th style="width:10%;">Price</th>'
                   '<th style="width:28%;">Other Terms (marriage, title, etc.)</th>'
                   '<th style="width:10%;">Status</th></tr>')
        body = [('<tr class="write-row">'
                 f'<td class="prefilled">{esc(m["name"])}</td>'
                 f'<td class="note">{esc((m.get("faction") or "")[:4])}</td>'
                 '<td></td><td></td><td></td><td></td></tr>') for m in ms]
        out.append(out.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n".join(out)


def ws_marriage(con, pcname):
    out = [sheet_head("Marriage Deal Tracker", pcname)]
    for label, typ in [("Brides You Are Placing", "Bride"), ("Grooms You Are Placing", "Groom")]:
        ms = rows(con, "select name, family from marriage_candidates where type=? order by id", (typ,))
        if not ms:
            continue
        out.append(f'<h3>{label}</h3>\n<table>\n<tr>'
                   '<th style="width:22%;">Candidate</th><th style="width:20%;">Matched To</th>'
                   '<th style="width:14%;">Dowry / Terms</th><th style="width:14%;">Faction Gain</th>'
                   '<th style="width:18%;">Notes</th><th style="width:12%;">Status</th></tr>')
        body = [('<tr class="write-row">'
                 f'<td class="prefilled">{esc(m["name"])}'
                 + (f' <span class="note">{esc(m["family"])}</span>' if m.get("family") else "")
                 + '</td><td></td><td></td><td></td><td></td><td></td></tr>') for m in ms]
        out.append(out.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n".join(out)


def ws_votes(con, pcname):
    out = [sheet_head("Vote Tracker", pcname)]
    out.append('<div class="reminder-box">\nVotes 1-3: Day 1 &middot; Votes 4-6: Day 2 &middot; '
               'Votes 7-9: Day 3. <strong>No pope by Vote 9 means the Ottomans invade.</strong>\n</div>')
    cs = rows(con, "select name, surname from characters where role='Cardinal' order by id")
    th = "".join(f'<th>V{i}</th>' for i in range(1, 10))
    out.append('<table>\n<tr><th style="width:22%;">Cardinal</th>' + th + "</tr>")
    body = []
    for c in cs:
        label = esc(c.get("surname") or c["name"])
        cells = "".join("<td></td>" for _ in range(9))
        body.append(f'<tr class="write-row"><td class="prefilled">{label}</td>{cells}</tr>')
    out.append(out.pop() + "\n" + "\n".join(body) + "\n</table>")
    return "\n".join(out)


def ws_favors(con, pcname):
    out = [sheet_head("Favors &amp; Promises", pcname)]
    out.append('<h3>What They Owe Me</h3>\n<table>\n<tr><th style="width:26%;">Who</th>'
               '<th style="width:54%;">What they owe</th><th style="width:20%;">Status</th></tr>\n'
               + writerows(8, 3) + "\n</table>")
    out.append('<h3>What I Owe Them</h3>\n<table>\n<tr><th style="width:26%;">Who</th>'
               '<th style="width:54%;">What I promised</th><th style="width:20%;">Status</th></tr>\n'
               + writerows(8, 3) + "\n</table>")
    out.append('<h3>My Vote Commitments</h3>\n<table>\n<tr><th style="width:26%;">To Whom</th>'
               '<th style="width:54%;">Promise</th><th style="width:20%;">Which Votes</th></tr>\n'
               + writerows(6, 3) + "\n</table>")
    out.append('<h3>Money Tracker</h3>\n<table>\n<tr><th style="width:46%;">Item</th>'
               '<th style="width:27%;">In</th><th style="width:27%;">Out</th></tr>\n'
               + writerows(8, 3) + "\n</table>")
    return "\n".join(out)


def ws_war(con, pcname):
    out = [sheet_head("Canonization &amp; War", pcname)]
    out.append('<h3>Canonization Tracker</h3>\n<table>\n<tr><th style="width:30%;">Candidate Saint</th>'
               '<th style="width:30%;">Helps Whom</th><th style="width:20%;">Push / Block</th>'
               '<th style="width:20%;">Status</th></tr>\n' + writerows(6, 4) + "\n</table>")
    out.append('<h3>War Tracker &mdash; Day 3, declarations due by 9 PM</h3>\n<table>\n'
               '<tr><th style="width:24%;">Commander</th><th style="width:24%;">Target</th>'
               '<th style="width:20%;">For Whom</th><th style="width:16%;">Defending?</th>'
               '<th style="width:16%;">Outcome</th></tr>\n' + writerows(8, 5) + "\n</table>")
    out.append('<h3>Family Safety Checklist</h3>\n<table>\n<tr><th style="width:30%;">Kin / Asset</th>'
               '<th style="width:50%;">Threat / Plan</th><th style="width:20%;">Safe?</th></tr>\n'
               + writerows(8, 3, "checkbox", BOX) + "\n</table>")
    return "\n".join(out)


def ws_assets(con, pcname):
    out = [sheet_head("Asset Status &amp; Letters", pcname)]
    ps = rows(con, "select name from possessions order by id")
    out.append('<h3>Possessions Status</h3>\n<table>\n<tr><th style="width:30%;">Item</th>'
               '<th style="width:30%;">Given / Traded To</th><th style="width:20%;">For What</th>'
               '<th style="width:20%;">Status</th></tr>')
    body = [('<tr class="write-row">'
             f'<td class="prefilled">{esc(p["name"])}</td><td></td><td></td><td></td></tr>') for p in ps]
    out.append(out.pop() + "\n" + "\n".join(body) + "\n</table>")
    out.append('<h3>Letters Received</h3>\n<table>\n<tr><th style="width:20%;">From</th>'
               '<th style="width:20%;">When</th><th style="width:40%;">Subject</th>'
               '<th style="width:20%;">Replied?</th></tr>\n' + writerows(10, 4) + "\n</table>")
    return "\n".join(out)


# ----------------------------------------------------- monarch-only sections
def sec_claims(con):
    """Dynastic and territorial claims (monarch packets). Empty -> omitted."""
    try:
        cs = rows(con, "select * from claims order by id")
    except sqlite3.OperationalError:
        cs = []
    if not cs:
        return ""
    out = ['<h2>0. Claims to Thrones and Lands</h2>',
           '<table class="t-tight">\n<tr><th style="width:22%;">Claim</th>'
           '<th style="width:18%;">Target</th><th style="width:34%;">Basis</th>'
           '<th style="width:14%;">Status</th><th style="width:12%;">Notes</th></tr>']
    body = [("<tr>"
             f'<td><strong>{esc(c["name"])}</strong></td>'
             f'<td>{esc(c.get("target"))}</td>'
             f'<td>{esc(c.get("basis"))}</td>'
             f'<td>{esc(c.get("status"))}</td>'
             f'<td>{esc(c.get("notes"))}</td></tr>') for c in cs]
    return out[0] + "\n" + out[1] + "\n" + "\n".join(body) + "\n</table>"


def sec_forces(con):
    """Standing armies and commanders (monarch packets). Empty -> omitted."""
    try:
        fs = rows(con, "select * from forces order by id")
    except sqlite3.OperationalError:
        fs = []
    if not fs:
        return ""
    out = ['<h2>0. Armies and Commanders</h2>',
           '<table class="t-tight">\n<tr><th style="width:22%;">Force</th>'
           '<th style="width:14%;">Kind</th><th style="width:12%;">Strength</th>'
           '<th style="width:18%;">Based</th><th style="width:18%;">Commander</th>'
           '<th style="width:16%;">Notes</th></tr>']
    body = [("<tr>"
             f'<td><strong>{esc(f["name"])}</strong></td>'
             f'<td>{esc(f.get("kind"))}</td>'
             f'<td>{esc(f.get("strength"))}</td>'
             f'<td>{esc(f.get("location"))}</td>'
             f'<td>{esc(f.get("commander"))}</td>'
             f'<td>{esc(f.get("notes"))}</td></tr>') for f in fs]
    return out[0] + "\n" + out[1] + "\n" + "\n".join(body) + "\n</table>"


def ws_campaign(con, pcname):
    """Campaign planner worksheet (monarch packets)."""
    out = [sheet_head("Campaign Tracker", pcname)]
    out.append('<div class="reminder-box">\nWar declarations are due Day 3 by 9 PM. '
               'Mercenaries will not fight close kin. Track every army you raise, hire, '
               'or send, and who defends what.\n</div>')
    out.append('<h3>Forces in the Field</h3>\n<table>\n<tr>'
               '<th style="width:22%;">Force / Commander</th><th style="width:22%;">Target</th>'
               '<th style="width:14%;">Cost / Terms</th><th style="width:22%;">Objective</th>'
               '<th style="width:20%;">Outcome</th></tr>\n' + writerows(10, 5) + "\n</table>")
    out.append('<h3>Claims Pressed This Conclave</h3>\n<table>\n<tr>'
               '<th style="width:26%;">Claim</th><th style="width:50%;">Move / Leverage</th>'
               '<th style="width:24%;">Status</th></tr>\n' + writerows(6, 3) + "\n</table>")
    return "\n".join(out)


# ---------------------------------------------------------------- assembly
def worksheets_intro():
    return ('<div class="halftitle pb">\n'
            f'  <div class="cross">{FLEUR}</div>\n'
            '  <div class="pt">Part the Second</div>\n'
            '  <div class="ti">The Conclave<br>Worksheets</div>\n'
            '  <div class="frabar"></div>\n'
            '  <div class="by">Living ledgers for the table &mdash; deals struck, votes cast, '
            'promises owed, and the war that may come. Keep them inked.</div>\n'
            '</div>')


def _renumber(sections):
    """Rewrite the leading 'N. ' of each section's first <h2> to be sequential,
    so sections can be reordered or subset per role and stay numbered 1..n."""
    out = []
    for i, s in enumerate([x for x in sections if x], 1):
        out.append(re.sub(r'(<h2[^>]*>)\s*\d+\.\s*', rf'\g<1>{i}. ', s, count=1))
    return out


def identity(con):
    """PC identity for the cover and contents page (consumed by the engine).
    Values are trusted author content and may contain markup (e.g. <br>)."""
    pc = pc_row(con)
    name = pc.get("name") or "His Eminence"
    sub = pc.get("subtitle")
    ident = {
        "coverTitle": pc.get("cover_title") or name,
        "coverByline": name + (f" &middot; {sub}" if sub else ""),
        "tocName": pc.get("styled_name") or name,
    }
    if pc.get("cover_kicker"):
        ident["coverKicker"] = pc["cover_kicker"]
    return ident


# Packet profiles: an ordered list of section/worksheet builders per PC role.
# Each builder is called with (con) for sections and (con, pcname) for sheets.
def _profile(role):
    cardinal_secs = [sec_personal, sec_key_profiles, sec_all_other, sec_mercenaries,
                     sec_marriages, sec_possessions, sec_forms, sec_family, sec_rules,
                     sec_pronunciation, sec_logistics, sec_checklist, sec_map]
    cardinal_ws = [ws_mercenary, ws_marriage, ws_votes, ws_favors, ws_war, ws_assets]
    if role == "Monarch":
        secs = [sec_personal, sec_key_profiles, sec_claims, sec_forces, sec_all_other,
                sec_marriages, sec_mercenaries, sec_possessions, sec_family, sec_rules,
                sec_forms, sec_pronunciation, sec_logistics, sec_map]
        ws = [ws_campaign, ws_marriage, ws_votes, ws_favors, ws_war, ws_assets]
        return secs, ws
    return cardinal_secs, cardinal_ws


def build(db_path):
    con = sqlite3.connect(db_path)
    pc = pc_row(con)
    pcname = esc(pc.get("name") or "His Eminence")
    role = pc.get("role") or "Cardinal"

    sec_builders, ws_builders = _profile(role)
    sections = _renumber([b(con) for b in sec_builders])
    worksheets = [worksheets_intro()] + [b(con, pcname) for b in ws_builders]
    ident = identity(con)
    con.close()
    return "\n\n".join(sections + worksheets), ident


def main(argv):
    db_path = argv[0] if len(argv) > 0 else "conclave.db"
    out_path = argv[1] if len(argv) > 1 else os.path.join("booklet", "booklet-content.js")
    flow, ident = build(db_path)
    payload = "window.BookletContent = " + json.dumps({"flowHTML": flow, "identity": ident}) + ";\n"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        f.write(payload)
    print(f"wrote {out_path}  ({len(flow)} chars of flow, role-aware identity emitted)")


if __name__ == "__main__":
    main(sys.argv[1:])
