---
name: temptemus-papam-design
description: Use this skill to generate well-branded interfaces and assets for Temptemus Papam (a 1492 Renaissance papal-election LARP), either for production or throwaway prototypes/mocks/handouts. Contains essential design guidelines, colors, type, fonts, assets, and a UI kit of document components for prototyping player materials.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

If creating visual artifacts (handouts, worksheets, character sheets, reference
booklets, mocks, throwaway prototypes, etc), copy assets out and create static
HTML files for the user to view and print. If working on production code, you can
copy assets and read the rules here to become an expert in designing with this
brand.

Key files to orient yourself:
- `README.md` — product context, content fundamentals, visual foundations, iconography, and an index of everything here.
- `colors_and_type.css` — all colour & type tokens (import alongside `fonts.css`).
- `conclave.css` — the print-document component layer.
- `fonts/` + `fonts.css` — the four embedded webfonts (Cardo, IM Fell English, IM Fell English SC, UnifrakturCook).
- `ui_kits/conclave-documents/` — reusable JSX primitives (`SheetHeader`, `EdictBox`, `HeraldicTag`, `DossierCard`, `LedgerTable`, `FleuronRule`) and a live showcase `index.html`.
- `reference-booklet.html` / `worksheets.html` — the canonical, print-ready handouts (fonts embedded as base64). Good structural references.
- `assets/europe-1492-map.jpg` — the hand-drawn brand map.

House rules when designing for this brand:
- It is a **rubricated chancery manuscript** for the laser printer: parchment page, iron-gall ink, **cardinal-vermillion** rubric headers, gilt hairlines, square corners, no shadows, no gradients, **no emoji**. Ornament is typographic (`✠`, fleurons) and heraldic (vert/or/gules tinctures for status).
- Tables get the signature **double rubric rule** top & bottom; keep writable cells light and open for ink.
- Voice is **in-world second person**, brisk and practical, period honorifics exact but explanations in clear modern English. Use the **They want / You want / You offer / Avoid** field pattern for relationships.
- Pull every colour and type value from `colors_and_type.css`. Never invent new hexes. Set `print-color-adjust: exact` so fills print.
- For anything printed, keep an editable HTML master and export PDF via an auto-printing `-print.html`.

If the user invokes this skill without any other guidance, ask them what they
want to build or design (a new handout? a tracker? a character packet? a poster?),
ask a few focused questions (which character/faction, how it will be used, print
or screen), and act as an expert designer who outputs HTML artifacts — or
production code — depending on the need.
