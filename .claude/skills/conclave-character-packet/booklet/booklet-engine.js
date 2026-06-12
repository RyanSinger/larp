/* ============================================================
   TEMPTEMUS PAPAM — booklet engine
   Paginates the single-source flow content into 5.5x8.5 trim
   pages, then renders EITHER:
     MODE 'linear'  -> one trim page per sheet, +bleed +crop marks
                       (send this PDF to a print shop)
     MODE 'imposed' -> 2-up landscape, saddle-stitch order
                       (print double-sided at home, fold, staple)
   Geometry (px @96dpi) mirrors booklet.css :root.
   ============================================================ */
(function(){
  "use strict";

  var GEOM = {
    TRIM_W:528, TRIM_H:816, BLEED:12,
    M_TOP:40, M_BOT:44, M_INNER:52, M_OUTER:34
  };
  GEOM.CONTENT_W = GEOM.TRIM_W - GEOM.M_INNER - GEOM.M_OUTER; // 442
  GEOM.USABLE_H  = GEOM.TRIM_H - GEOM.M_TOP - GEOM.M_BOT - 2; // 730

  var MODE = window.BOOKLET_MODE || "linear";
  var COVER_KEY = "tp_booklet_cover";
  var cover = localStorage.getItem(COVER_KEY) || "map";

  // -------- helpers --------
  function el(tag, cls, html){
    var e=document.createElement(tag);
    if(cls) e.className=cls;
    if(html!=null) e.innerHTML=html;
    return e;
  }
  function isHeading(n){ return n && n.nodeType===1 && /^H[23]$/.test(n.tagName); }
  function isTable(n){ return n && n.nodeType===1 && n.tagName==="TABLE"; }

  // -------- measuring host --------
  var host = el("div","",""); 
  host.style.cssText="position:absolute;left:-99999px;top:0;visibility:hidden;"+
    "width:"+GEOM.CONTENT_W+"px;";
  document.body.appendChild(host);
  function newCol(){
    var c=el("div","leaf-body");
    c.style.width=GEOM.CONTENT_W+"px";
    return c;
  }
  function overflow(col){ return col.scrollHeight > GEOM.USABLE_H; }

  // -------- pagination --------
  // returns { pages:[Element(leaf-body)], headings:[{text,sel,page}] }
  function paginate(blocks){
    var pages=[];
    var cur=newCol(); host.appendChild(cur);

    function commit(){
      if(cur.childNodes.length){ host.removeChild(cur); pages.push(cur); }
      cur=newCol(); host.appendChild(cur);
    }

    function shellFor(tbl, headerTR){
      var t=el("table"); t.className=tbl.className;
      if(headerTR) t.appendChild(headerTR.cloneNode(true));
      return t;
    }
    function splitTable(tbl){
      var trs=[].slice.call(tbl.querySelectorAll(":scope > tr, :scope > tbody > tr"));
      var headerTR = trs.length ? trs[0] : null;
      var rows = trs.slice(1);
      var work=shellFor(tbl, headerTR);
      cur.appendChild(work);
      if(overflow(cur)){
        // header doesn't fit here — move to a fresh page (carry trailing heading too)
        cur.removeChild(work);
        var carry=[];
        while(cur.lastChild && isHeading(cur.lastChild) && cur.childNodes.length>1)
          carry.unshift(cur.removeChild(cur.lastChild));
        commit();
        carry.forEach(function(c){ cur.appendChild(c); });
        work=shellFor(tbl, headerTR); cur.appendChild(work);
      }
      for(var i=0;i<rows.length;i++){
        var r=rows[i].cloneNode(true);
        work.appendChild(r);
        if(overflow(cur)){
          work.removeChild(r);
          commit();
          work=shellFor(tbl, headerTR); cur.appendChild(work);
          work.appendChild(r); // single row on a fresh page; accept if it still overflows
        }
      }
    }

    for(var bi=0; bi<blocks.length; bi++){
      var src=blocks[bi];
      if(src.nodeType!==1) continue;
      var block=src.cloneNode(true);
      var isPB = block.classList && block.classList.contains("pb");
      var isHalf = block.classList && block.classList.contains("halftitle");

      if(isPB && cur.childNodes.length) commit();

      cur.appendChild(block);

      if(overflow(cur)){
        // remove and decide
        cur.removeChild(block);
        if(cur.childNodes.length){
          if(isTable(block)){ splitTable(block); }
          else {
            // carry any trailing heading(s) to the next page with this block
            var carry=[];
            while(cur.lastChild && isHeading(cur.lastChild) && cur.childNodes.length>1)
              carry.unshift(cur.removeChild(cur.lastChild));
            commit();
            carry.forEach(function(c){ cur.appendChild(c); });
            cur.appendChild(block);
            if(overflow(cur) && isTable(block)){ cur.removeChild(block); splitTable(block); }
          }
        } else {
          // empty page, single block too tall
          if(isTable(block)){ splitTable(block); }
          else { cur.appendChild(block); } // accept overflow (rare)
        }
      }
      if(isHalf) commit(); // half-title stands alone
    }
    if(cur.childNodes.length){ host.removeChild(cur); pages.push(cur); }
    else host.removeChild(cur);
    return { pages:pages };
  }

  // -------- fixed page builders --------
  var KICK = '<span style="color:var(--rubric)">&#10016;</span>&ensp;Sede Vacante &middot; Anno Domini MCDXCII&ensp;<span style="color:var(--rubric)">&#10016;</span>';

  // PC identity is supplied by booklet-content.js (window.BookletContent.identity);
  // fall back to literals so the engine still renders if it is absent.
  function _id(){ return (window.BookletContent && window.BookletContent.identity) || {}; }
  function idTitle(){   return _id().coverTitle  || 'Cardinal<br>Sanseverino'; }
  function idByline(){  return _id().coverByline || 'Federico Sanseverino &middot; Cardinal Deacon of San Teodoro'; }
  function idTocName(){ return _id().tocName     || 'His Eminence Cardinal Federico Sanseverino'; }
  function idKick(def){ return _id().coverKicker || def; }

  function coverHTML(v){
    if(v==="type"){
      return '<div class="cover cover--type">'+
        '<div class="cross">&#10016;</div>'+
        '<div class="kick">'+idKick('Sede Vacante &middot; A Conclave at Rome')+'</div>'+
        '<div class="ti">'+idTitle()+'</div>'+
        '<div class="frabar"></div>'+
        '<div class="by">A Reference Booklet for the Election of a Pope</div>'+
        '<div class="yr">Anno Domini MCDXCII</div>'+
      '</div>';
    }
    if(v==="frame"){
      return '<div class="cover cover--frame"><div class="fr">'+
        '<div class="cross">&#10016;</div>'+
        '<div class="kick">'+idKick('Sede Vacante')+'</div>'+
        '<div class="ti">'+idTitle()+'</div>'+
        '<div class="fdiv"></div>'+
        '<div class="by">A Reference Booklet for the Conclave at Rome, that the reader may know his allies, his enemies, his armies, and his kin.</div>'+
        '<div class="yr">Anno Domini MCDXCII &middot; Roma</div>'+
      '</div></div>';
    }
    // map (default)
    return '<div class="cover cover--map">'+
      '<div class="mapwrap"><img src="europe-1492-map.jpg" alt=""></div>'+
      '<div class="scrim"></div>'+
      '<div class="cap">'+
        '<div class="kick">'+idKick(KICK)+'</div>'+
        '<div class="ti">'+idTitle()+'</div>'+
      '</div>'+
      '<div class="foot">'+
        '<div class="by">A Reference Booklet for the Conclave at Rome</div>'+
        '<div class="yr">'+idByline()+'</div>'+
      '</div>'+
    '</div>';
  }

  function tocHTML(entries){
    var rows = entries.map(function(e){
      if(e.part){
        return '<li class="part"><span class="tt">'+e.label+'</span></li>';
      }
      return '<li><span class="rn">'+(e.rn||"")+'</span>'+
        '<span class="tt">'+e.label+'</span><span class="dots"></span>'+
        '<span class="pg">'+e.page+'</span></li>';
    }).join("");
    return '<div class="toc-page">'+
      '<div class="toc-head">'+
        '<div class="cross">&#10016;</div>'+
        '<div class="ti">Contents</div>'+
        '<div class="by">'+idTocName()+'</div>'+
      '</div>'+
      '<ol class="toc-list">'+rows+'</ol>'+
    '</div>';
  }

  function notesHTML(title){
    return '<div class="notes-page">'+
      '<div class="nh">'+(title||"Notes")+'</div>'+
      '<div class="rules"></div>'+
    '</div>';
  }

  function colophonHTML(){
    return '<div class="colophon">'+
      '<div class="cross">&#10016;</div>'+
      '<div class="mark">Temptemus<br>Papam</div>'+
      '<div class="body">&ldquo;Let us attempt a pope.&rdquo; This booklet was set for the '+
        'Conclave at Rome in the year of Our Lord 1492, in the rubricated hand of the '+
        'papal chancery &mdash; iron-gall ink, cardinal vermillion, and gold &mdash; that a '+
        'cardinal might carry his whole intrigue in one small folio.</div>'+
      '<div class="fdiv"></div>'+
      '<div class="imprint">'+
        '<span class="keys">&#10016;</span>&ensp;Temptemus Papam &middot; Lighthaven MMXXVI&ensp;<span class="keys">&#10016;</span>'+
        '<br>Keep your packets. Do not lose them.'+
      '</div>'+
    '</div>';
  }

  // -------- leaf assembly --------
  function leafEl(side, contentNode, pageNo, showFolio){
    var leaf=el("div","leaf"+(side==="verso"?" verso":""));
    var body=el("div","leaf-body");
    if(typeof contentNode==="string") body.innerHTML=contentNode;
    else body.appendChild(contentNode);
    leaf.appendChild(body);
    if(showFolio){
      var f=el("div","folio",
        '<span class="keys">&#10016;</span>&ensp;'+pageNo+'&ensp;<span class="keys">&#10016;</span>');
      leaf.appendChild(f);
    }
    return leaf;
  }
  function noFolio(node){
    if(typeof node==="string") return /class="(cover|toc-page|halftitle|colophon)/.test(node);
    return node.querySelector && !!node.querySelector(".cover,.toc-page,.halftitle,.colophon");
  }

  // -------- crop marks --------
  function cropMarks(bleed){
    ["tl","tr","bl","br"].forEach(function(c){ bleed.appendChild(el("span","cm cm-"+c)); });
  }

  // -------- renderers --------
  function renderLinear(leaves){
    var doc=el("div","flowdoc");
    leaves.forEach(function(lf, i){
      var pageNo=i+1;
      var side = (pageNo%2===1)?"recto":"verso"; // p1 recto
      var bleed=el("div","bleed print-page");
      var leaf=leafEl(side, lf.content.cloneNode ? lf.content.cloneNode(true) : lf.content,
                      pageNo, !lf.noFolio);
      bleed.appendChild(leaf);
      cropMarks(bleed);
      doc.appendChild(bleed);
    });
    return doc;
  }

  function impositionOrder(N){
    var sheets=N/4, out=[];
    for(var s=0;s<sheets;s++){
      out.push([N-2*s, 1+2*s]);     // front
      out.push([2+2*s, N-1-2*s]);   // back
    }
    return out; // array of [leftPage,rightPage] (1-indexed)
  }
  function renderImposed(leaves){
    var doc=el("div","flowdoc");
    var N=leaves.length;
    var order=impositionOrder(N);
    order.forEach(function(pair, idx){
      var sheet=el("div","imp-sheet print-page");
      var lp=leaves[pair[0]-1], rp=leaves[pair[1]-1];
      var left = leafEl("verso", lp.content.cloneNode(true), pair[0], !lp.noFolio);
      var right= leafEl("recto", rp.content.cloneNode(true), pair[1], !rp.noFolio);
      sheet.appendChild(left); sheet.appendChild(right);
      sheet.appendChild(el("div","imp-spine"));
      var face = idx%2===0 ? "front" : "back";
      sheet.appendChild(el("div","imp-label",
        "sheet "+(Math.floor(idx/2)+1)+" &middot; "+face+" &middot; pp. "+pair[0]+"\u2013"+pair[1]));
      doc.appendChild(sheet);
    });
    return doc;
  }

  // -------- build --------
  function build(){
    // parse source flow
    var srcWrap=el("div","",window.BookletContent.flowHTML);
    var blocks=[].slice.call(srcWrap.children);
    var res=paginate(blocks);
    var flowed=res.pages;

    // Derive the table of contents from the flowed content (flowed index ->
    // absolute page = +3, because cover and toc precede). Part I sections are
    // each <h2>; the worksheets begin at a .halftitle divider; each worksheet
    // is a .sheet-head h1. This stays correct for any section set or order.
    function roman(n){
      var R=["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII",
             "XIV","XV","XVI","XVII","XVIII","XIX","XX","XXI","XXII","XXIII","XXIV"];
      return R[n-1] || (""+n);
    }
    var toc=[], secNo=0;
    for(var pi=0; pi<flowed.length; pi++){
      var pageNum=pi+3;
      var nodes=flowed[pi].querySelectorAll("h2, .halftitle, .sheet-head h1");
      for(var ni=0; ni<nodes.length; ni++){
        var node=nodes[ni];
        if(node.tagName==="H2"){
          secNo++;
          var lab=node.textContent.replace(/\s+/g," ").replace(/^\s*\d+\.\s*/,"").trim();
          toc.push({rn:roman(secNo), label:lab, page:pageNum});
        } else if(node.classList && node.classList.contains("halftitle")){
          var ti=node.querySelector(".ti");
          var pl=ti ? ti.innerHTML.replace(/<br\s*\/?>/gi," ").replace(/<[^>]+>/g,"")
                        .replace(/\s+/g," ").trim() : "Worksheets";
          toc.push({part:true, label:"Part II \u00b7 "+pl});
        } else { // .sheet-head h1
          toc.push({rn:"", label:node.textContent.replace(/\s+/g," ").trim(), page:pageNum});
        }
      }
    }

    // assemble ordered leaves: cover, toc, ...flowed, notes(pad), colophon
    var leaves=[];
    function wrap(html){ var d=el("div"); d.innerHTML=html; return d.firstChild; }

    leaves.push({content: wrap(coverHTML(cover)), noFolio:true});
    leaves.push({content: wrap(tocHTML(toc)),     noFolio:true});
    flowed.forEach(function(pg){
      leaves.push({content: pg, noFolio: !!pg.querySelector(".halftitle")});
    });

    // pad to multiple of 4 with ruled notes; guarantee a notes spread (>=2)
    var base = leaves.length + 1; // +1 for colophon to come
    var need = (4 - (base % 4)) % 4;
    if(need < 2) need += 4;
    var titles=["Notes","Notes","Tallies & Reminders","Notes","Notes","Notes","Notes","Notes"];
    for(var n=0;n<need;n++) leaves.push({content: wrap(notesHTML(titles[n%titles.length])), noFolio:false});

    leaves.push({content: wrap(colophonHTML()), noFolio:true});

    // safety: must be multiple of 4
    while(leaves.length % 4 !==0){
      leaves.splice(leaves.length-1, 0, {content: wrap(notesHTML("Notes")), noFolio:false});
    }

    // render
    var mount=document.getElementById("mount");
    mount.innerHTML="";
    var doc = (MODE==="imposed") ? renderImposed(leaves) : renderLinear(leaves);
    mount.appendChild(doc);

    // status line
    var st=document.getElementById("statline");
    if(st){
      var sheets=leaves.length/4;
      st.innerHTML = "<b>"+leaves.length+"</b> pages &middot; "+
        (MODE==="imposed"
          ? "<b>"+sheets+"</b> sheets (2-up, double-sided) &middot; fold &amp; staple"
          : "trim 5.5&times;8.5 in &middot; 0.125 in bleed &middot; crop marks &middot; "+sheets+" folded sheets");
    }
    document.body.setAttribute("data-mode",MODE);
  }

  // -------- cover switcher --------
  function initControls(){
    var sel=document.getElementById("coverSel");
    if(sel){
      sel.value=cover;
      sel.addEventListener("change",function(){
        cover=sel.value; localStorage.setItem(COVER_KEY,cover); build();
      });
    }
  }

  function go(){ initControls(); build(); }
  function start(){
    var waits=[];
    if(document.fonts && document.fonts.ready) waits.push(document.fonts.ready);
    waits.push(new Promise(function(res){
      var im=new Image(); im.onload=res; im.onerror=res; im.src="europe-1492-map.jpg";
    }));
    Promise.all(waits).then(go);
  }
  start();
  // expose for the other view
  window.__bookletBuild=build;
})();
