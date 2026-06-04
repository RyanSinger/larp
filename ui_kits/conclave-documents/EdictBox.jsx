/* EdictBox — bordered callout for rules, pricing, reminders.
   Renders children as HTML; use <strong> for rubricated lead-ins. */
function EdictBox({ children }) {
  return (
    <div style={{
      border: "1pt solid var(--gold,#9a7b33)",
      outline: "0.5pt solid var(--gold,#9a7b33)",
      outlineOffset: "2pt",
      background: "var(--parchment-2,#efe6cf)",
      padding: "8pt 12pt",
      margin: "4pt 0 12pt",
      fontFamily: "'IM Fell English','Cardo',serif",
      fontSize: "9.5pt",
      lineHeight: 1.45,
    }}>{children}</div>
  );
}
Object.assign(window, { EdictBox });
