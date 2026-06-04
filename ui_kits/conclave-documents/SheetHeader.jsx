/* SheetHeader — the title block atop every handout:
   kicker line, blackletter title, italic byline, fleuron rule. */
function SheetHeader({ kicker, title, byline }) {
  return (
    <header style={{ textAlign: "center", marginBottom: "14pt" }}>
      {kicker && (
        <div style={{ fontFamily: "'IM Fell English SC','Cardo',serif", fontSize: "9pt",
          letterSpacing: "0.2em", textTransform: "uppercase", color: "var(--gold,#9a7b33)", marginBottom: "3pt" }}>
          <span style={{ color: "var(--rubric,#8c1d18)" }}>{"\u2720"}</span>
          {"\u2002"}{kicker}{"\u2002"}
          <span style={{ color: "var(--rubric,#8c1d18)" }}>{"\u2720"}</span>
        </div>
      )}
      <h1 style={{ fontFamily: "'UnifrakturCook','Cardo',serif", fontWeight: 700, fontSize: "30pt",
        lineHeight: 1, color: "var(--rubric,#8c1d18)", margin: "2pt 0 4pt" }}>{title}</h1>
      {byline && (
        <div style={{ fontFamily: "'IM Fell English','Cardo',serif", fontStyle: "italic",
          fontSize: "11pt", color: "var(--ink-soft,#5a4d3a)", marginBottom: "6pt" }}>{byline}</div>
      )}
      <FleuronRule glyph={"\u2766"} maxWidth="4.5in" />
    </header>
  );
}
Object.assign(window, { SheetHeader });
