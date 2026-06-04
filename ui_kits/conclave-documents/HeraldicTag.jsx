/* HeraldicTag — small status/faction label in a blazon tincture.
   kind: ally | priority | avoid | locked | neutral  (or pass custom {fg,bg})  */
function HeraldicTag({ kind = "neutral", children }) {
  const tinctures = {
    ally:     { fg: "#2f5d3a", bg: "#e3e8d9" },
    priority: { fg: "#7a5e15", bg: "#f1e7c6" },
    avoid:    { fg: "#8c1d18", bg: "#f0dcd6" },
    locked:   { fg: "#8c7f68", bg: "#e7dabb" },
    neutral:  { fg: "#2c4a6e", bg: "#dde3ec" },
  };
  const t = tinctures[kind] || tinctures.neutral;
  return (
    <span style={{
      fontFamily: "'IM Fell English SC', serif",
      fontSize: "7.5pt",
      letterSpacing: "0.04em",
      padding: "0 4pt",
      border: "0.5pt solid " + t.fg,
      color: t.fg,
      background: t.bg,
      whiteSpace: "nowrap",
      verticalAlign: "middle",
    }}>{children}</span>
  );
}
Object.assign(window, { HeraldicTag });
