/* LedgerTable — the chancery double-ruled table.
   props: columns:[{key,label,width}], rows:[{...}], writable (bool)
   Cells render row[col.key]; empty string leaves a blank writable cell. */
function LedgerTable({ columns = [], rows = [], writable = false }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: "10pt",
      fontSize: "8.75pt",
      borderTop: "2.4pt double var(--rubric-deep,#6d130f)",
      borderBottom: "2.4pt double var(--rubric-deep,#6d130f)" }}>
      <tbody>
        <tr>
          {columns.map((c) => (
            <th key={c.key} style={{ width: c.width, background: "var(--parchment-2,#efe6cf)",
              fontFamily: "'IM Fell English SC','Cardo',serif", fontWeight: 400, fontSize: "8.5pt",
              letterSpacing: "0.05em", textTransform: "uppercase", color: "var(--rubric-deep,#6d130f)",
              border: "0.5pt solid var(--sepia-line,#b9a988)", borderBottom: "1.25pt solid var(--gold,#9a7b33)",
              padding: "3pt 5pt", textAlign: "left", verticalAlign: "top" }}>{c.label}</th>
          ))}
        </tr>
        {rows.map((row, i) => (
          <tr key={i}>
            {columns.map((c) => (
              <td key={c.key} style={{ border: "0.5pt solid var(--sepia-line,#b9a988)",
                padding: "3pt 5pt", textAlign: "left", verticalAlign: "top",
                height: writable ? "19pt" : "auto",
                background: writable ? (i % 2 ? "#f6efdd" : "#fbf7ec")
                                     : (i % 2 ? "#faf6ea" : "transparent") }}>
                {row[c.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
Object.assign(window, { LedgerTable });
