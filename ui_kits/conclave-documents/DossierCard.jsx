/* DossierCard — a character profile: rubric spine, red name,
   italic subtitle, and labelled rows. props:
     name, sub, tag (<HeraldicTag> kind or null), rows:[{label,text}] */
function DossierCard({ name, sub, tag, rows = [] }) {
  return (
    <div style={{
      background: "var(--parchment-lift,#faf6ea)",
      border: "0.6pt solid var(--sepia-line,#b9a988)",
      borderLeft: "3pt solid var(--rubric,#8c1d18)",
      padding: "6pt 10pt 7pt",
      marginBottom: "10pt",
    }}>
      <div style={{ fontFamily: "'Cardo',serif", fontWeight: 700, fontSize: "11pt",
        color: "var(--rubric-deep,#6d130f)", marginBottom: "2pt" }}>
        {name}{" "}{tag && <HeraldicTag kind={tag.kind}>{tag.label}</HeraldicTag>}
      </div>
      {sub && <div style={{ fontFamily: "'IM Fell English','Cardo',serif", fontStyle: "italic",
        fontSize: "9pt", color: "var(--ink-soft,#5a4d3a)", marginBottom: "5pt" }}>{sub}</div>}
      {rows.map((r, i) => (
        <div key={i} style={{ fontSize: "9.5pt", marginBottom: "2pt", lineHeight: 1.4 }}>
          <strong style={{ color: "var(--rubric-deep,#6d130f)" }}>{r.label}:</strong> {r.text}
        </div>
      ))}
    </div>
  );
}
Object.assign(window, { DossierCard });
