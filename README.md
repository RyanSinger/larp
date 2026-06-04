# Temptemus Papam — Design System

> *Tentemus Papam* — "Let us attempt a pope." The design system for a
> Renaissance papal-election LARP set in the year of Our Lord **1492**.

This system lets a design agent (or a human) produce **player-facing LARP
materials** — character booklets, negotiation worksheets, reference sheets,
hand-outs — that look like documents drawn from a 15th-century papal chancery,
yet remain legible and writable when printed and carried into the game.

---

## 1. What this is

**Temptemus Papam** is a live-action role-play simulation of a papal conclave
in 1492. ~40 players take real historical figures — cardinals, papal
functionaries, and the monarchs of Europe — each with private goals, resources,
and secrets, and spend up to four days electing (or blocking) a pope. It is an
**alternate history**, not a reconstruction: most characters are real people,
but some are shifted in time. There is no single winner; each player pursues
their own tangle of goals.

The "product," from a design standpoint, is the **packet of printed materials**
every player receives: a character sheet, a reference booklet, negotiation
worksheets, rules, a map, and lore documents. The design system codifies the
look of those materials.

### The world in brief
- The pope is dead; 25 cardinals vote, 8 functionaries run the election, and
  outside monarchs (France, Spain, England, the Empire…) meddle from afar.
- Up to nine votes over three days; **13 votes = a new pope**. No pope by the
  ninth vote and **the Ottomans invade Europe**, triggering a War Phase.
- Politics run on money, marriages, mercenary contracts, papal petitions,
  binding contracts, the canonization of saints, and the favor of the Roman Mob.
- Italy is split between **Guelphs** (papal party, led by the Orsini) and
  **Ghibellines** (imperial party, led by the Colonna).

---

## 2. Sources

Everything here was derived from materials supplied by the game's organizer.
The reader may not have access, but they are recorded for provenance:

**GitHub — `RyanSinger/larp`** (the canonical handout source)
<https://github.com/RyanSinger/larp>
- `reference-booklet.html` — a 40-character reference booklet for Cardinal Sanseverino
- `worksheets.html` — five negotiation/tracking worksheets

> Explore that repository further to build new handouts faithfully — the two
> HTML files are the real, authored structure these designs recreate.

**Uploaded documents** (in `uploads/`)
- `Papal Election Quickstart.pdf` — onboarding slides
- `Papal Election Lighthaven - Character List.pdf` — the full Dramatis Personae
- `TEMPTEMUS PAPAM - Rules Lighthaven 2026.pdf` — full rules (42 pp.)
- `Temptemus Papam - Facts About the World.pdf` — the geopolitical setup
- `Renaissance Timeline Up To 1492.pdf` — in-world timeline (with a colour key)
- `Character Sheet - Sanseverino Federico CS.pdf` — a sample full character sheet
- `PapamMapUpdated-2026_With_Ports_in_Red.jpg` — the hand-drawn map of Europe in 1492
  (copied to `assets/europe-1492-map.jpg`)

---

## 3. Content fundamentals

The writing is the soul of these materials. It is **in-world, second-person,
and instructive** — the documents speak *to a specific cardinal* about *their*
goals, allies, and enemies.

- **Voice & person.** Direct second person — *"Pursue your character's goals.
  If they want to become pope, make that happen."* The reader is always
  addressed as their character. Organizer asides ("DMs", "the orchestrators")
  break the fourth wall only in the rules.
- **Register.** Plain, brisk, and practical sitting *inside* a period frame.
  Sentences are short and imperative on worksheets (*"The coin goes to the
  mercenaries, never to your own purse."*) and warmer, more narrative in
  character profiles.
- **Period diction, modern clarity.** Honorifics and forms of address are
  exact and matter ("Your Eminence", "Caesar" for the Emperor, "Your
  Puissance" for the Sultan; calling the Emperor "Austria" is *mildly rude*).
  But explanations are crisp modern English — never faux-archaic ("forsooth").
- **Structure.** Heavy use of labelled mini-fields: **They want / You want /
  You offer / Avoid / Your opinion** for relationships; **Pricing / Remember**
  for rules. Ranked lists for goals. Tables for everything countable.
- **Tone.** Wry and knowing. The stakes are deadly (assassination, invasion)
  but the prose has a glint of humour — *"Enough Peacocks", "useless coward",
  "Play your age. You're 17. Let people underestimate you."*
- **Casing.** Title Case for headings and proper titles; UPPERCASE for hard
  warnings (`LOCKED`, `AVOID`, `DO NOT LOSE YOUR PACKETS`). Roman numerals and
  Latin dates for flourish (*Anno Domini MCDXCII*, *Sede Vacante*).
- **No emoji.** Ever. Ornament is typographic (`✠`, fleurons), never pictographic.
- **Numbers.** Money in florins ("40,000 fl."), with the comma. Ages and vote
  counts are bare numerals.

---

## 4. Visual foundations

A **rubricated chancery manuscript**, reproduced for the laser printer. The
governing idea: a scribe's ledger — aged paper, iron-gall text, **red
rubrication** for emphasis, gilt hairlines, and ornaments — but with tables
clean and open enough to write in by hand during play.

- **Colour.** Warm **parchment** page (`#f4ecd8`) over a darker desk
  (`#d8cba8`); **iron-gall ink** body text (`#2b2218`); **cardinal vermillion**
  rubric (`#8c1d18`) for all headers and the brand; **ochre/gilt** (`#9a7b33`)
  for fine rules and kickers. Status and faction use **heraldic tinctures**
  (gules, vert, or, azure, purpure, sable). See `colors_and_type.css`.
- **Type.** Four roles: **UnifrakturCook** blackletter for titles & the
  wordmark; **IM Fell English SC** (incunabula small caps) for section bars,
  table heads, kickers; **Cardo** (a humanist serif made for medieval
  scholarship) for all running text and tables; **IM Fell English italic** for
  edicts, quotes, and bylines. Family trees use a plain monospace. Fonts are
  **embedded** (woff2 in `fonts/`, declared in `fonts.css`); the print handouts
  inline them as base64 so they print offline.
- **Backgrounds.** Flat parchment fills — **no** gradients, photos, or
  textures behind text (they muddy print and waste toner). The only image is
  the hand-drawn **map**, used as full-bleed brand imagery. `print-color-adjust:
  exact` forces the parchment and red bars to print even without "Background
  graphics" enabled.
- **Borders & rules.** The signature is the **double rubric rule** (2.4pt
  double red) top-and-bottom of every table, with **0.5pt sepia hairlines** for
  the grid and a **1.25pt gilt** under-rule beneath header rows. Edict boxes get
  a gold border with an offset gold outline (a "ruled-twice" frame). Dossier
  cards get a **3pt rubric spine** on the left edge.
- **Cards.** Two kinds. *Dossier cards* (character profiles): faint lifted
  parchment fill, hairline border, red left spine, red name, italic subtitle.
  *Edict boxes*: panel parchment, double gold frame, Fell italic text. No
  rounded corners anywhere — everything is square, like cut paper.
- **Shadows / elevation.** Essentially none. Depth is expressed through
  **borders and rule weight**, not drop shadows. The one soft touch is a 2.5pt
  gilt "shadow line" under the divider rules to suggest gold leaf.
- **Corner radius.** `0` throughout. This is paper and ink, not glass.
- **Ornament & iconography.** Typographic only — `✠` (cross) and `❦ / ❧`
  fleurons as dividers and bullets; see §5.
- **Layout.** Letter-size, single column, generous line height (1.4). Each
  handout opens with a centred **SheetHeader** (kicker → blackletter title →
  italic byline → fleuron rule) and closes with a small footer mark. Sections
  begin with a full-width red bar. New worksheets force a page break.
- **Motion & states.** These are print documents — no animation. In the
  interactive UI kit, hover lifts a control's text to rubric red and its border
  to gold; the active/pressed state fills with rubric red and parchment text
  (a wax-seal feel). No transitions longer than an instant.
- **Imagery vibe.** The map is high-contrast black ink on white with
  **red port markers** — a hand-lettered, slightly nervous cartographic line.
  When used as brand imagery it gets a faint sepia wash to sit on parchment.

---

## 5. Iconography

The brand is **deliberately icon-free** in the modern sense. There is no icon
font, no SVG sprite, no PNG glyph set in the source materials, and **no emoji**.
Iconography is **typographic and heraldic**:

- **Unicode ornaments as icons.** `✠` (U+2720 Maltese-style cross) marks
  kickers, section bars, and footers — it stands in for the crossed Keys of
  St. Peter. `❦`/`❧` (U+2766/2767 floral hearts) and `❖` (U+2756) are used as
  fleuron dividers and bullets. `☐` (U+2610 ballot box) is the checkbox on
  checklists. These are real printer's ornaments of the era — period-correct,
  not decoration-for-its-own-sake.
- **Heraldic tinctures as "status icons."** Rather than symbols, *colour* + a
  small-caps word communicates state: `ALLY` (vert), `PRIORITY` (or), `AVOID`
  (gules), `LOCKED` (sable/edge), `NEUTRAL` (azure). See the `HeraldicTag`
  component and the Colors cards.
- **Substitution flag.** No brand icon set existed to import, so none was
  substituted. If you need true pictographic icons (a galero, tiara, crossed
  keys) source period woodcut engravings or commission heraldry — do **not**
  reach for a generic modern icon library, which would break the aesthetic.

---

## 6. Index — what's in this folder

**Foundations**
- `fonts.css` + `fonts/` — the four embedded webfont families (woff2)
- `colors_and_type.css` — all colour & type **tokens** and semantic helpers
- `conclave.css` — the print-document component layer built on those tokens

**Canonical handouts** (the real, print-ready deliverables — fonts embedded)
- `reference-booklet.html` — Cardinal Sanseverino's 40-character reference booklet
- `worksheets.html` — five negotiation/tracking worksheets
- `*-print.html` — auto-printing variants (open → Save as PDF)

**Design System tab** (`preview/`)
- 16 specimen cards: type, colours, ornaments/borders, components, brand

**UI kit** (`ui_kits/conclave-documents/`)
- `index.html` — live component showcase (with a working faction filter)
- JSX primitives: `SheetHeader`, `FleuronRule`, `EdictBox`, `HeraldicTag`,
  `DossierCard`, `LedgerTable`
- `README.md` — load order & component API

**Assets** (`assets/`)
- `europe-1492-map.jpg` — the hand-drawn map of Europe in 1492

**Other**
- `SKILL.md` — makes this folder usable as a Claude Agent Skill
- `uploads/` — original source PDFs + map (provenance; safe to omit from git)

---

## 7. Working with this system

- **Building a new handout?** Use the UI kit primitives, or copy the structure
  of `worksheets.html` / `reference-booklet.html`. Pull colours and type from
  `colors_and_type.css` — never invent new hexes.
- **Printing for the table?** Use the `-print.html` variants (Save as PDF).
  Keep the HTML as the editable master.
- **Retheming?** Edit the tokens in `colors_and_type.css`; everything cascades.
