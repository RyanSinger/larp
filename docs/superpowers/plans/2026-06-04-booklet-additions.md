# Booklet Additions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add five new reference sections (9 through 13) to the end of the existing reference booklet, then sync the print variant.

**Architecture:** Append HTML to `reference-booklet.html` before `</body>`, using the existing CSS classes (`.page-break`, `.reminder`, `.qr-box`, `table`, `th/td`, `h2`, `h3`). The print variant `reference-booklet-print.html` is identical except for a `<script>` block before `</body>` that triggers `window.print()`. After editing the main file, copy it to the print variant and re-add the script block.

**Tech Stack:** Static HTML, existing `conclave.css` design system (already embedded in the file as inline styles and base64 fonts).

---

### Task 1: Update table of contents

**Files:**
- Modify: `reference-booklet.html:152-161` (the `<ol class="toc">` element)

- [ ] **Step 1: Add items 9 through 13 to the TOC**

Find the existing TOC at line 152 and replace:

```html
<ol class="toc" style="font-size:9pt;">
  <li>Personal Quick Reference</li>
  <li>Key Character Profiles (12)</li>
  <li>All Other Characters (28)</li>
  <li>Mercenary Reference</li>
  <li>Marriage Candidates</li>
  <li>Possessions &amp; Courtiers</li>
  <li>Forms of Address</li>
  <li>Key Family Relationships</li>
</ol>
```

Replace with:

```html
<ol class="toc" style="font-size:9pt;">
  <li>Personal Quick Reference</li>
  <li>Key Character Profiles (12)</li>
  <li>All Other Characters (28)</li>
  <li>Mercenary Reference</li>
  <li>Marriage Candidates</li>
  <li>Possessions &amp; Courtiers</li>
  <li>Forms of Address</li>
  <li>Key Family Relationships</li>
  <li>Rules Mechanics Quick Reference</li>
  <li>Pronunciation Guide</li>
  <li>Game Logistics &amp; Starting State</li>
  <li>Map of Europe in 1492</li>
</ol>
```

- [ ] **Step 2: Commit**

```bash
git add reference-booklet.html
git commit -m "Add new sections to booklet table of contents"
```

---

### Task 2: Add Section 9, Rules Mechanics Quick Reference (page 1)

**Files:**
- Modify: `reference-booklet.html` (insert before `</body></html>` at line 1087)

- [ ] **Step 1: Insert Section 9 page 1 after the closing `</ul>` of section 8 (line 1085)**

Insert immediately after line 1085 (`</ul>`), before `</body>`:

```html

<!-- ============================================================ -->
<!-- SECTION 9: RULES MECHANICS QUICK REFERENCE -->
<!-- ============================================================ -->

<div class="page-break"></div>
<h2>9. Rules Mechanics Quick Reference</h2>

<h3>Contracts</h3>
<ul style="font-size:8.5pt; margin:4pt 0; padding-left:16pt;">
<li>Parchment with signature lines. All signatures needed, then take to <strong>Notary at Orchestrator Desk</strong>. Notary cuts in half; you keep one copy.</li>
<li>Only binding after notarized. Cannot create new contracts during game (pre-made only).</li>
<li>Cannot make illegal contracts (murder for hire, vote buying).</li>
<li>Contracts are <strong>public record</strong>: others can discover them through spies.</li>
</ul>

<div class="reminder">
<strong>Breaking a contract: EXTREMELY SEVERE.</strong> You lose a large sum of money, items may be stolen or destroyed, courtiers abandon you, spies and assassins leave, mercenaries refuse to fight, allies suffer, bride/groom rank penalized, kin face consequences, monks face monastic discipline, public announcement, possible murder at endgame. Must go to Orchestrator table <em>before</em> breaking.<br><br>
<strong>Three exceptions</strong> (dissolve without severe penalty): (1) all parties agree, (2) a Special Power interferes, (3) circumstances change extremely (assassination, betrayal discovered, unexpected war).
</div>

<h3>Public Declarations</h3>
<ul style="font-size:8.5pt; margin:4pt 0; padding-left:16pt;">
<li>Alternative to contracts for things that cannot be contracted ("I think France should get Naples").</li>
<li>Announced to everyone. Cannot be kept secret. Serious commitment.</li>
<li>Can be broken, but with faction-level consequences (allies stop trusting you).</li>
<li>Can sign one and not yet bring to notary: it is not binding until announced.</li>
</ul>

<h3>Marriage Rules Recap</h3>
<ul style="font-size:8.5pt; margin:4pt 0; padding-left:16pt;">
<li>One bride card + one groom card + dowry, turned in to orchestrators.</li>
<li>Bride's family provides dowry. Match within one rank grade (A to C = scandal).</li>
<li>Natural (illegitimate) children: one rank below normal. Legitimization only by pope.</li>
<li>Marriages dissolve only before pope elected. After election, months pass per round; marriages permanent (only dissolved by papal annulment or death/assassination of bride or groom).</li>
<li>Cardinals cannot marry but can take a mistress (bride card counts as Evidence of Sinful Living if Inquisition investigates).</li>
</ul>

<h3>Mercenary Pricing</h3>
<table>
<tr><th style="width:15%;">Price</th><th>What It Means</th></tr>
<tr><td><strong>50,000</strong></td><td>Normal price. Commander and men are happy.</td></tr>
<tr><td><strong>40,000</strong></td><td>Good deal. Commander and men will be ok.</td></tr>
<tr><td><strong>30,000</strong></td><td>Very low. Kinsmen discount only. Risk of looting.</td></tr>
<tr><td><strong>20,000</strong></td><td>Bare minimum. No profit. Will almost certainly loot.</td></tr>
</table>
<p style="font-size:8pt; margin-top:2pt;">Fledgling commanders <strong>cannot</strong> accept less than 40,000. Money goes to the mercenaries, not to you.</p>

<h3>Courtier Rules</h3>
<ul style="font-size:8.5pt; margin:4pt 0; padding-left:16pt;">
<li>Trade freely to any cardinal or monarch (not most functionaries since they cannot support them).</li>
<li>Give status to a court or place. More different types of courtier = more status.</li>
<li>Player character courtiers (some functionaries) cannot be given to a direct enemy.</li>
</ul>
```

- [ ] **Step 2: Verify in browser**

Open `reference-booklet.html` in browser, scroll to end, confirm section 9 page 1 renders correctly with proper styling.

- [ ] **Step 3: Commit**

```bash
git add reference-booklet.html
git commit -m "Add rules mechanics quick reference page 1 (contracts, marriages, pricing)"
```

---

### Task 3: Add Section 9, Rules Mechanics Quick Reference (page 2)

**Files:**
- Modify: `reference-booklet.html` (append after the content added in Task 2, before `</body>`)

- [ ] **Step 1: Insert Section 9 page 2**

Insert immediately after the courtier rules `</ul>` added in Task 2:

```html

<div class="page-break"></div>

<h3>Papal Petitions</h3>
<ul style="font-size:8.5pt; margin:4pt 0; padding-left:16pt;">
<li>Must be <strong>(A) signed</strong> by a petitioner and <strong>(B) turned in</strong> to Chief Secretary Maffei before the audience.</li>
<li>Vice-Chancellor (currently Borgia) decides reading order. Befriend Maffei too; he organizes them for the V-C.</li>
<li>Pope rarely has time for more than <strong>10 to 12 petitions</strong> before war. Get yours near the top.</li>
<li>Petitions have value beyond submitting: show to allies or enemies as leverage, or offer to withhold.</li>
<li><strong>Speaking without being called on</strong> at the audience is a grave violation: arrest, torture, fines, expulsion.</li>
</ul>

<h3>Vatican Offices &amp; Salaries</h3>
<table>
<tr><th style="width:32%;">Office</th><th style="width:15%;">Salary/yr</th><th style="width:25%;">Current Holder</th><th style="width:28%;">Key Power</th></tr>
<tr><td>Camerlengo</td><td>5,500</td><td>Riario</td><td>24/7 pope access. Can grant people permission to speak at audience.</td></tr>
<tr><td>Vice-Chancellor</td><td>2,000</td><td>Borgia</td><td>Controls petition order. Can speak at audience uninvited. Rehires functionaries after election.</td></tr>
<tr><td>Legatus General</td><td>1,500</td><td>VACANT</td><td>Chief diplomat. Envoys and appointments.</td></tr>
<tr><td>Major Penitentiary</td><td>3,500</td><td>della Rovere</td><td>Pardons excommunicates. Can contact outside world during election.</td></tr>
<tr><td>Master Sacred Palace</td><td>1,500</td><td>Torriani</td><td>Highest theological authority. Traditionally Dominican.</td></tr>
<tr><td>Postulator General</td><td>1,000</td><td>Sangiorgio</td><td>Canonizes saints. Narrows 40 candidates to 5 finalists.</td></tr>
<tr><td>Standard-Bearer</td><td>15,000</td><td>Niccolò Orsini</td><td>Supreme commander title. High Noble rank. +1 Army.</td></tr>
<tr><td>Captain General</td><td>10,000</td><td>Niccolò Orsini</td><td>Field commander. High Noble rank. +3 Armies.</td></tr>
<tr><td>Gov. Castel Sant'Angelo</td><td>5,000</td><td>Domenico d.R.</td><td>Papal fortress, prison, Vatican defense.</td></tr>
</table>
<p style="font-size:8pt; margin-top:2pt;"><strong>Pope also distributes:</strong> 4 new cardinalships (10,000 each to family), 2 abbacies (15,000 immediate + 8,000/yr), 5 papal armies, 1 Golden Rose (priceless honor).</p>

<h3>Coronation Sequence</h3>
<ol style="font-size:8.5pt; margin:4pt 0; padding-left:18pt;">
<li>Vote Counters announce pope. Pope crowned by Papal Chaplain (Farnese). <strong>Rips up all fealty cards.</strong></li>
<li>Pope calls all Cardinals and others to kneel and pledge loyalty. <strong>Order indicates favorites.</strong> May call functionaries before out-of-favor cardinals.</li>
<li>Outside Players (monarchs) enter one by one. <strong>Order indicates papal favor</strong> toward their nation.</li>
</ol>

<h3>The Inquisition</h3>
<ul style="font-size:8.5pt; margin:4pt 0; padding-left:16pt;">
<li>Run by Dominicans (leader: your uncle Carafa). Three evidence types: <strong>Heresy</strong> (radical theology), <strong>Sinful Living</strong> (breaking vows), <strong>Simony</strong> (bribes).</li>
<li>Secret Archive has a file on every character. Can investigate a few people per session.</li>
<li>If crimes found that are NOT already notorious: (1) Inquisitor may offer private repentance via "donation" (bribe), or (2) denounce you publicly.</li>
<li>Public denouncement: <strong>10,000 florin fine per crime type</strong> for cardinals (1,000 for functionaries). Allies may dissolve. Courtiers possibly arrested.</li>
<li><strong>Your status:</strong> Evidence of Crime: None. It was blackmail, not simony.</li>
<li>Warning: some Inquisitors consider humanism a form of heresy (no ruling yet). If declared heresy, everyone with humanist courtiers gets investigated.</li>
</ul>

<h3>Benedictine Monastic Status</h3>
<ul style="font-size:8.5pt; margin:4pt 0; padding-left:16pt;">
<li>+1 per library or book collection item card. +1 per 3 individual books. +1 per library project completed.</li>
<li>+1 per artist, musician, or sculptor courtier at monastery end of last day. +1 bonus for a complete set of all three types.</li>
<li>+3 for official papal favor.</li>
<li>+1 for each cardinal <strong>under 40</strong> who joins the order (older cardinals do not count).</li>
<li>+1 for each new monarch who becomes Benedictine patron (<strong>you currently have no patron</strong>).</li>
</ul>

<div class="reminder">
<strong>Ottoman Invasion (if no pope by Vote 9):</strong> Whoever had plurality becomes pope. All players lose half their money. Papal Treasury emptied. All small wars abandoned for defensive war. This happens at end of Day 3 if no pope elected.
</div>
```

- [ ] **Step 2: Verify in browser**

Open in browser, confirm page 2 renders correctly. Check that the Vatican offices table is readable and the page break falls between the two pages.

- [ ] **Step 3: Commit**

```bash
git add reference-booklet.html
git commit -m "Add rules mechanics quick reference page 2 (petitions, offices, coronation, Inquisition)"
```

---

### Task 4: Add Section 10, Pronunciation Guide

**Files:**
- Modify: `reference-booklet.html` (append after Section 9, before `</body>`)

- [ ] **Step 1: Insert Section 10**

Insert after the Ottoman Invasion reminder `</div>`:

```html

<!-- ============================================================ -->
<!-- SECTION 10: PRONUNCIATION GUIDE -->
<!-- ============================================================ -->

<div class="page-break"></div>
<h2>10. Pronunciation Guide</h2>

<h3>Cardinals</h3>
<table>
<tr><th style="width:22%;">Nametag</th><th style="width:22%;">Say</th><th style="width:56%;">Quick ID</th></tr>
<tr><td><strong>BORGIA</strong></td><td>Boar-jah</td><td>Vice-Chancellor, 61, Spanish</td></tr>
<tr><td><strong>CARAFA</strong></td><td>Car-rah-fuh</td><td>Your uncle, 62, Naples, Dominican leader</td></tr>
<tr><td><strong>COLONNA</strong></td><td>Coe-low-nuh</td><td>Ghibelline leader, 57, Roman</td></tr>
<tr><td><strong>NANNI</strong> "Samson"</td><td>Nah-nee</td><td>Franciscan head, 78, Siena</td></tr>
<tr><td><strong>ORSINI</strong></td><td>Or-see-nee</td><td>Guelph leader, 57, Roman</td></tr>
<tr><td><strong>PICCOLOMINI</strong></td><td>Pea-coal-low-me-nee</td><td>Guidobaldo's godfather, 63, Siena</td></tr>
<tr><td><strong>DELLA ROVERE</strong></td><td>del-luh Row-ver-ray</td><td>Uncle Julius, 49, Genoa</td></tr>
<tr><td><strong>SFORZA</strong></td><td>Svor-tsuh</td><td>Milan, 41, Ghibelline</td></tr>
<tr><td><strong>TORRIANI</strong></td><td>Tor-ee-ah-nee</td><td>Inquisitor General, 60, Milan</td></tr>
<tr><td><strong>D'AUBUSSON</strong></td><td>Dow-boo-son</td><td>Knights Hospitaller, 69, French</td></tr>
<tr><td><strong>BRI&Ccedil;ONNET</strong></td><td>Bree-sown-neigh</td><td>French king's man, 47</td></tr>
<tr><td><strong>CAMPOFREGOSO</strong></td><td>Cahm-po-freh-go-so</td><td>Pirate Doge, 62, Genoa</td></tr>
<tr><td><strong>DA COSTA</strong></td><td>Dah Cost-uh</td><td>Portuguese, 86</td></tr>
<tr><td><strong>GHERARDI</strong></td><td>Geh-rar-dee</td><td>Patriarch of Venice, 97</td></tr>
<tr><td><strong>SANGIORGIO</strong></td><td>San-jor-joe</td><td>Canonization, 53, Milan</td></tr>
<tr><td><strong>SODERINI</strong></td><td>Saw-deh-ree-nee</td><td>Anti-Medici, 51, Florence</td></tr>
<tr><td><strong>ZEN</strong></td><td>Zen</td><td>Venetian, 53</td></tr>
<tr><td><strong>BEMBO</strong></td><td>Bem-bo</td><td>Humanist, 22, Venice</td></tr>
<tr><td><strong>DE BUCY</strong></td><td>Deh Boo-see</td><td>French prince, 21</td></tr>
<tr><td><strong>CASTELLESI</strong></td><td>Cah-steh-leh-see</td><td>"Hadrian," ambassador, 32</td></tr>
<tr><td><strong>D'ESTE</strong></td><td>Deh Es-stay</td><td>Ferrara, 22, Benedictine</td></tr>
<tr><td><strong>DE MEDICI</strong></td><td>De Meh-dih-chee</td><td>"Leo," banker, 17, Florence</td></tr>
<tr><td><strong>RIARIO</strong></td><td>Ree-are-ee-oh</td><td>Camerlengo, 31, della Rovere heir</td></tr>
<tr><td><strong>SANSEVERINO</strong></td><td>San-sever-reno</td><td>YOU, 17</td></tr>
<tr><td><strong>SCHINER</strong></td><td>Shine-er</td><td>Swiss mercenary, 35</td></tr>
</table>

<h3>Functionaries</h3>
<table>
<tr><th style="width:22%;">Nametag</th><th style="width:22%;">Say</th><th style="width:56%;">Quick ID</th></tr>
<tr><td><strong>BORGIA</strong> "Valentino"</td><td>Val-en-tee-no</td><td>Treasurer, 17, Borgia's son</td></tr>
<tr><td><strong>FARNESE</strong></td><td>Far-nay-zay</td><td>Chaplain, 18, Roman</td></tr>
<tr><td><strong>CORELLA</strong></td><td>Cor-el-lah</td><td>Papal Guard Captain, 22, Spanish</td></tr>
<tr><td><strong>MAFFEI</strong></td><td>Mah-fay</td><td>Chief Secretary, 71, retiring</td></tr>
<tr><td><strong>BURCHARD</strong></td><td>Bur-chard</td><td>Master of Ceremonies, 42, German</td></tr>
<tr><td><strong>DES PREZ</strong></td><td>Jus-ken day Pray</td><td>Choir Director, 42, Burgundian</td></tr>
<tr><td><strong>CONSTANTINE</strong></td><td>Con-stan-teen</td><td>Clerk, 33, Greek refugee</td></tr>
<tr><td><strong>TILLIO</strong></td><td>Tea-lee-oh</td><td>Clerk, 21, Benedictine</td></tr>
</table>

<h3>Monarchs</h3>
<table>
<tr><th style="width:22%;">Name</th><th style="width:22%;">Say</th><th style="width:56%;">Quick ID</th></tr>
<tr><td><strong>MAXIMILIAN</strong></td><td>Max-ih-mil-ee-an</td><td>Emperor, 41, Hapsburg</td></tr>
<tr><td><strong>CHARLES VIII</strong></td><td>Sharl</td><td>King of France, 22</td></tr>
<tr><td><strong>ISABELLA</strong></td><td>Iz-ah-bell-ah</td><td>Queen of Castile, 41</td></tr>
<tr><td><strong>HENRY VII</strong></td><td>Henry</td><td>King of England, 43</td></tr>
<tr><td><strong>ANNE</strong></td><td>Ann</td><td>Duchess of Brittany, 19</td></tr>
<tr><td><strong>BEATRICE</strong></td><td>Bay-ah-tree-chay</td><td>Queen of Hungary, 35</td></tr>
</table>

<h3>Key Terms</h3>
<table>
<tr><th style="width:22%;">Term</th><th style="width:22%;">Say</th><th style="width:56%;">Meaning</th></tr>
<tr><td><strong>Papabile</strong></td><td>Pah-pah-bee-lay</td><td>Declared candidate for pope</td></tr>
<tr><td><strong>Temptemus Papam</strong></td><td>Temp-teh-moos Pah-pahm</td><td>"Let us attempt a pope"</td></tr>
<tr><td><strong>Guelph</strong></td><td>Gwelf</td><td>Papal party (Orsini led)</td></tr>
<tr><td><strong>Ghibelline</strong></td><td>Gib-eh-leen</td><td>Imperial party (Colonna led)</td></tr>
<tr><td><strong>Camerlengo</strong></td><td>Cah-mer-len-go</td><td>Papal household head (Riario)</td></tr>
<tr><td><strong>Condottiero</strong></td><td>Con-dot-tee-air-oh</td><td>Mercenary captain</td></tr>
</table>
```

- [ ] **Step 2: Verify in browser**

Confirm all four tables render cleanly on one page. Check that pronunciation column is wide enough to be readable.

- [ ] **Step 3: Commit**

```bash
git add reference-booklet.html
git commit -m "Add pronunciation guide for all 40 characters and key terms"
```

---

### Task 5: Add Sections 11 & 12, Game Logistics and Starting State

**Files:**
- Modify: `reference-booklet.html` (append after Section 10, before `</body>`)

- [ ] **Step 1: Insert Sections 11 and 12**

Insert after the Key Terms table `</table>`:

```html

<!-- ============================================================ -->
<!-- SECTIONS 11 & 12: GAME LOGISTICS + STARTING STATE -->
<!-- ============================================================ -->

<div class="page-break"></div>
<h2>11. Game Logistics</h2>

<table>
<tr><th style="width:22%;">Day</th><th style="width:30%;">Events</th><th style="width:22%;">Time</th><th style="width:26%;">Notes</th></tr>
<tr><td><strong>Day 1</strong> (June 8)</td><td>Votes 1, 2, 3</td><td>3:30 to 6:30 PM</td><td>First day of election</td></tr>
<tr><td><strong>Day 2</strong> (June 9)</td><td>Votes 4, 5, 6</td><td>3:30 to 6:30 PM</td><td>Ally scheming between sessions</td></tr>
<tr><td><strong>Day 3</strong> (June 10)</td><td>Votes 7, 8, 9</td><td>3:30 to 6:30 PM</td><td>War orders due by <strong>9 PM</strong></td></tr>
<tr><td><strong>Day 4</strong> (June 11)</td><td>Post-war, ransoms, papal audience, final vote</td><td>3:30 to 6:30 PM</td><td>Income distributed</td></tr>
</table>

<table style="margin-top:6pt;">
<tr><th style="width:22%;">Topic</th><th>Details</th></tr>
<tr><td><strong>Sistine Chapel</strong></td><td>Lighthaven E. Sealed during election. Cardinals and functionaries inside.</td></tr>
<tr><td><strong>Outside Powers</strong></td><td>Separate room (TBD). Monarchs communicate via letters and agents.</td></tr>
<tr><td><strong>OOC Signal</strong></td><td><strong>Fist pressed to forehead.</strong> Signals you are not your character at that moment.</td></tr>
<tr><td><strong>Touching</strong></td><td>Go out of character first (fist to head), then describe the action verbally.</td></tr>
<tr><td><strong>Arrive Early</strong></td><td>New letters may be waiting. Read them before session starts.</td></tr>
<tr><td><strong>Between Sessions</strong></td><td>Communicate freely with allies (Discord, DM, email, call). Do NOT negotiate with non-allies outside of sessions.</td></tr>
<tr><td><strong>Orchestrators</strong></td><td>Ask for advice at any time. They will not reveal secrets but will point out resources or pros and cons of plans.</td></tr>
<tr><td><strong>Notary</strong></td><td>At Orchestrator Desk. Finalizes contracts (cuts in half, you keep one copy).</td></tr>
<tr><td><strong>Chief Secretary</strong></td><td>Maffei collects papal petitions. Turn them in before the papal audience.</td></tr>
<tr><td><strong>Vote Counters</strong></td><td>Functionaries who tally votes. They know who voted for whom and may act on or sell that knowledge.</td></tr>
</table>

<h2 style="margin-top:14pt;">12. Starting State Checklist</h2>

<div class="qr-box">
<table style="border:none; margin-bottom:6pt;">
<tr>
  <td style="border:none; width:50%;"><strong>Cardinal Federico (da Montefeltro) Sanseverino</strong><br>Cardinal Deacon of San Teodoro</td>
  <td style="border:none; width:50%; text-align:right;">Age 17 &bull; Noble &bull; Ghibelline &bull; Benedictine<br>Combat Value: 1* &bull; Territory: Castelnuovo Scrivia</td>
</tr>
</table>

<h3>Verify Your Envelope on Day 1</h3>
<table style="border:none; font-size:8.5pt;">
<tr><td style="border:none; width:4%; vertical-align:top;">&#9744;</td><td style="border:none;">Money cards totaling <strong>20,000 florins</strong></td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">15,000 per Sanseverino sister (dowry reserve, if provided separately)</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Port card: <strong>Salerno</strong> (tradeable only with King Ferrante permission)</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Unsigned Contracts: safe passage through Urbino and Mantua (for Uncle Guidobaldo)</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">6 Courtier cards: Reuchlin, Seusenhofer, de Orto, Alberti, Scappi, Varesi</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">14 Bride cards</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">14 Groom cards (check: includes Malatesta, Fregoso, Malavolti)</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Nunnery card: San Maurizio, Milan</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Possessions: Father's Diary, Chariot (8K), Courser (4K), Reliquary (3K), Shadow Boat, Carved Gems, Tiger Cub, Peacocks, Children's Clothes (&times;2), Petrarch's <em>Secretum</em></td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Back Brace (on your person, not in envelope)</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Special Power card: Spinal Compression</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Confirm: NO assassin or spy cards (you start with 0)</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Confirm: NO debt cards</td></tr>
<tr><td style="border:none; vertical-align:top;">&#9744;</td><td style="border:none;">Confirm: NO evidence of crime cards</td></tr>
</table>
<p style="font-size:8pt; margin-top:4pt;"><strong>If anything is missing or wrong, tell an orchestrator immediately.</strong></p>
</div>
```

- [ ] **Step 2: Verify in browser**

Confirm logistics table and checklist render on one page. Check that checkboxes (&#9744;) display correctly.

- [ ] **Step 3: Commit**

```bash
git add reference-booklet.html
git commit -m "Add game logistics and starting state checklist"
```

---

### Task 6: Add Section 13, Map Reference

**Files:**
- Modify: `reference-booklet.html` (append after Section 12, before `</body>`)

- [ ] **Step 1: Insert Section 13**

Insert after the closing `</div>` of the qr-box in Section 12:

```html

<!-- ============================================================ -->
<!-- SECTION 13: MAP OF EUROPE IN 1492 -->
<!-- ============================================================ -->

<div class="page-break"></div>
<h2>12. Map of Europe in 1492</h2>

<img src="assets/europe-1492-map.jpg" alt="Simplified Map of Europe in 1492" style="width:100%; border:0.5pt solid #999; margin-bottom:6pt;">

<table style="font-size:8pt;">
<tr><th style="width:20%;">Region</th><th style="width:30%;">Controller</th><th style="width:50%;">Notes</th></tr>
<tr><td colspan="3" style="background:#e8e8e8; font-weight:bold; font-size:7.5pt; text-transform:uppercase;">Your Lands</td></tr>
<tr><td>Caiazzo</td><td>Sanseverino (you)</td><td>Inside Kingdom of Naples, near Naples city</td></tr>
<tr><td>Castelnuovo Scrivia</td><td>Sanseverino (you)</td><td>Your territory</td></tr>
<tr><td>Salerno</td><td>Your port (Ferrante permission)</td><td>Uncle Antonello banished from here</td></tr>
<tr><td>Sora</td><td>Della Rovere</td><td>Uncle Julius's brother. Border of Lazio and Naples.</td></tr>
<tr><td colspan="3" style="background:#e8e8e8; font-weight:bold; font-size:7.5pt; text-transform:uppercase;">Key Mercenary Regions</td></tr>
<tr><td>Urbino</td><td>Guidobaldo (2 armies)</td><td>Allied with Mantua. Your closest uncle.</td></tr>
<tr><td>Mantua</td><td>Gonzaga (2 armies)</td><td>Allied with Urbino. Wants a bride.</td></tr>
<tr><td>Bologna</td><td>Bentivoglio</td><td>Guelph but friendly. Wants ducal title.</td></tr>
<tr><td>Rimini</td><td>Malatesta</td><td>Wild. Coastal port. +1 army.</td></tr>
<tr><td>Ferrara</td><td>d'Este</td><td>Noblest house. Buffer vs. Ottomans.</td></tr>
<tr><td>Florence</td><td>Medici</td><td>Guelph. Richest sack value (250,000).</td></tr>
<tr><td>Milan</td><td>Sforza</td><td>Ghibelline. France threatening to invade.</td></tr>
<tr><td>Genoa</td><td>Sforza / della Rovere</td><td>Port city. Campofregoso exiled from here.</td></tr>
<tr><td>Rome</td><td>Pope + Roman Mob</td><td>Variable defense. Orsini vs. Colonna.</td></tr>
<tr><td colspan="3" style="background:#e8e8e8; font-weight:bold; font-size:7.5pt; text-transform:uppercase;">Outside Powers</td></tr>
<tr><td>France</td><td>Charles VIII</td><td>Mightiest monarchy. Claims Naples and Milan.</td></tr>
<tr><td>Castile + Aragon</td><td>Isabella + Ferdinand</td><td>Merging into Spain. Controls S. Naples, Sardinia.</td></tr>
<tr><td>Empire (HRE)</td><td>Maximilian</td><td>Huge but less wealthy. Your Ghibelline Caesar.</td></tr>
<tr><td>England</td><td>Henry VII</td><td>Distant. Holds part of Brittany.</td></tr>
<tr><td>Ottoman Empire</td><td>Sultan Bayezid II</td><td>Conquered Greece, Constantinople. Threatening Hungary.</td></tr>
</table>
```

- [ ] **Step 2: Verify in browser**

Confirm map image loads and displays full-width. Check that the legend table is readable below the map. Confirm the whole section fits on one page (may be tight; if not, the map can be slightly smaller via `max-height`).

- [ ] **Step 3: Commit**

```bash
git add reference-booklet.html
git commit -m "Add map of Europe with legend for mercenary regions and outside powers"
```

---

### Task 7: Sync the print variant

**Files:**
- Modify: `reference-booklet-print.html`

- [ ] **Step 1: Copy the main file to the print variant**

```bash
cp reference-booklet.html reference-booklet-print.html
```

- [ ] **Step 2: Add the auto-print script block before `</body>`**

Open `reference-booklet-print.html` and insert immediately before `</body>`:

```html

<script>
window.addEventListener('load', function(){
  var go = function(){ setTimeout(function(){ window.print(); }, 500); };
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(go); }
  else { setTimeout(go, 800); }
});
</script>
```

- [ ] **Step 3: Verify print variant**

Open `reference-booklet-print.html` in browser. Confirm it triggers the print dialog. Cancel print and verify content matches the main file.

- [ ] **Step 4: Commit and push**

```bash
git add reference-booklet.html reference-booklet-print.html
git commit -m "Sync print variant with updated booklet"
git push
```
