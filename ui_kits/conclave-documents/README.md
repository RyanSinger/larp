# Conclave Documents — UI Kit

Reusable components for building **Temptemus Papam** player handouts. Every
handout (character booklets, trackers, reference sheets) is assembled from
these primitives so the whole packet shares one chancery aesthetic and prints
cleanly on letter paper.

Open `index.html` for a live showcase, including a ledger with a working
faction filter.

## Load order

```html
<link rel="stylesheet" href="../../colors_and_type.css">  <!-- tokens + @font-face -->
<link rel="stylesheet" href="../../conclave.css">          <!-- document base styles -->
<!-- React 18.3.1 + ReactDOM + Babel standalone (pinned), then: -->
<script type="text/babel" src="HeraldicTag.jsx"></script>
<script type="text/babel" src="FleuronRule.jsx"></script>
<script type="text/babel" src="SheetHeader.jsx"></script>
<script type="text/babel" src="EdictBox.jsx"></script>
<script type="text/babel" src="DossierCard.jsx"></script>
<script type="text/babel" src="LedgerTable.jsx"></script>
```

Each component exports itself onto `window`, so files share scope across
separate Babel scripts.

## Components

| Component | Purpose | Key props |
|---|---|---|
| `SheetHeader` | Title block atop a handout | `kicker`, `title`, `byline` |
| `FleuronRule` | Gilt divider with printer's ornament | `glyph`, `maxWidth` |
| `EdictBox` | Callout for rules / pricing / reminders | `children` |
| `HeraldicTag` | Status or faction label in a tincture | `kind` = ally · priority · avoid · locked · neutral |
| `DossierCard` | Character profile with a rubric spine | `name`, `sub`, `tag`, `rows` |
| `LedgerTable` | Chancery double-ruled table | `columns`, `rows`, `writable` |

## Notes

- These are **cosmetic recreations** of the real handout structure — simple,
  composable, easy to lift into a new sheet. They are not a state-management
  framework.
- For print/PDF the canonical handouts (`reference-booklet.html`,
  `worksheets.html` at the project root) are hand-authored static HTML with the
  fonts embedded. This kit is for **building new** documents quickly.
- Colours and type come entirely from `colors_and_type.css` variables, so
  retheming is a token edit.
