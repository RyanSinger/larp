/* FleuronRule — centred gilt divider with a printer's ornament.
   glyph defaults to a fleuron; pass "✠" for a cross.  */
function FleuronRule({ glyph = "\u2766", maxWidth = "5in" }) {
  const line = {
    content: "",
    flex: 1,
    borderTop: "1pt solid var(--gold, #9a7b33)",
    boxShadow: "0 2.5pt 0 -1.5pt var(--gold-soft, #b89a52)",
  };
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10, justifyContent: "center",
      color: "var(--rubric, #8c1d18)", margin: "8pt auto 0", maxWidth }}>
      <span style={line} />
      <span style={{ fontSize: "13pt", lineHeight: 1 }}>{glyph}</span>
      <span style={line} />
    </div>
  );
}
Object.assign(window, { FleuronRule });
