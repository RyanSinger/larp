# Design house rules

The booklet is a **rubricated chancery manuscript for the laser printer**. Read this
before editing any HTML, CSS, or the generator's markup. (Condensed from the
project's `temptemus-papam-design` guide.)

- **Surface:** parchment page, iron-gall ink, **cardinal-vermillion** rubric
  headers, gilt hairlines. Square corners. **No shadows, no gradients, no emoji.**
- **Ornament is typographic and heraldic:** the cross `✠` (`&#10016;`), the fleuron
  `❖`/`&#10070;`, the vert/or/gules tinctures for status. Nothing decorative beyond
  the type.
- **Tables** carry the signature **double rubric rule** top and bottom (from
  `booklet.css`). Keep writable cells light and open for ink; prefilled cells use
  class `prefilled`, faction shorthand uses `note`, writable rows use `write-row`.
- **Voice** is in-world **second person**, brisk and practical. Period honorifics
  exact; explanations in clear modern English. Relationships use the
  **They want / You want / You offer / Avoid** field pattern (plus *Your opinion*).
- **Never invent colours or type.** Every value comes from the design tokens baked
  into `booklet.css`. Set `print-color-adjust: exact` so fills print (already in the
  stylesheet).
- **Writing rules (match the project CLAUDE.md):** no dashes as separators (em, en,
  or hyphen). Use colons, commas, periods, or rewrite. No emoji. Honorifics and
  Latin tags (Sede Vacante, Anno Domini MCDXCII) stay exact.
- **Print workflow:** keep the database as the editable master and always export the
  PDF via `generate_pdf.cjs`, which verifies the page count is complete and a
  multiple of four. Do not trust a browser "Save as PDF" for the final artifact; it
  has silently truncated the worksheets before.
- **Covers:** three options ship in the engine (`map`, `type`, `frame`), selectable
  in the print-shop page; `map` is the default and uses `europe-1492-map.jpg`.
