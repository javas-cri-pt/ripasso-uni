#!/usr/bin/env python3
"""Ripasso Uni — build the self-contained webapp from curriculum.yml + lessons/*.md.
Run after each new lesson is generated. Output: ripasso.html (open in browser)."""
import re, json, glob, html
from pathlib import Path
import yaml

ROOT = Path(__file__).parent
CURR = yaml.safe_load((ROOT/"curriculum.yml").read_text())

def topic_index():
    """flatten curriculum → ordered list of {id,name,course,area} + adjacency."""
    order=[]
    for c in CURR.get("courses",[]):
        for t in c.get("topics",[]):
            order.append({"id":t["id"],"name":t["name"],"course":c["name"],"area":c["area"]})
    for c in CURR.get("cross_cutting",[]):
        for t in c.get("topics",[]):
            order.append({"id":t["id"],"name":t["name"],"course":c["name"],"area":"cross-cutting"})
    return order

def parse_lesson(p):
    raw=Path(p).read_text()
    m=re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    meta=yaml.safe_load(m.group(1)) if m else {}
    body=m.group(2) if m else raw
    # split off quiz
    quiz=[]
    qm=re.split(r"\n##\s*Quiz.*?\n", body, maxsplit=1)
    lesson_body=qm[0].strip()
    if len(qm)>1:
        qblock=qm[1]
        det=re.split(r"<details>.*?<summary>.*?</summary>", qblock, maxsplit=1, flags=re.DOTALL)
        qpart=det[0]
        apart=det[1].replace("</details>","") if len(det)>1 else ""
        qs={int(n):t.strip() for n,t in re.findall(r"^\s*(\d+)\.\s*(.+?)(?=\n\s*\d+\.|\Z)", qpart, re.DOTALL|re.MULTILINE)}
        ans={int(n):t.strip() for n,t in re.findall(r"^\s*(\d+)\.\s*(.+?)(?=\n\s*\d+\.|\Z)", apart, re.DOTALL|re.MULTILINE)}
        for k in sorted(qs):
            quiz.append({"q":qs[k],"a":ans.get(k,"")})
    return {"meta":meta,"body":lesson_body,"quiz":quiz}

lessons=[]
for p in sorted(glob.glob(str(ROOT/"lessons"/"*.md"))):
    d=parse_lesson(p)
    lessons.append({
        "day":d["meta"].get("day"),
        "topic_id":d["meta"].get("topic_id"),
        "title":d["meta"].get("title",""),
        "course":d["meta"].get("course",""),
        "area":d["meta"].get("area",""),
        "adjacent":d["meta"].get("adjacent",[]),
        "body":d["body"],
        "quiz":d["quiz"],
    })

order=topic_index()
DATA=json.dumps({"lessons":lessons,"order":order,"total":len(order)},ensure_ascii=False)

APP=r"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0d5c62"><title>Ripasso Uni</title>
<style>
:root{
 --ink:#181b1e;--soft:#3f464d;--muted:#69707a;--accent:#0d5c62;--accent-ink:#0a4a4f;
 --accent2:#9a4a1a;--bg:#f6f8f7;--card:#ffffff;--card2:#eef2f1;--rule:#e0e5e5;
 --good:#0e7c5a;--bad:#b23a3a;--shadow:0 1px 2px rgba(20,40,40,.05),0 8px 24px rgba(20,40,40,.06);
 --sans:"Avenir Next","Segoe UI",system-ui,-apple-system,sans-serif;--serif:"Charter","Iowan Old Style",Georgia,serif;
 --z-topbar:30;--z-scrim:40;--z-drawer:50;--ease:cubic-bezier(.22,.61,.36,1);}
.dk{--ink:#e8eaea;--soft:#bcc3c5;--muted:#868e92;--accent:#3fb0b6;--accent-ink:#7fd0d4;--accent2:#d9945a;
 --bg:#101315;--card:#191d20;--card2:#20262a;--rule:#2b3236;--good:#4bbd93;--bad:#df6b6b;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.35);}
:root[data-theme=dark]{--ink:#e8eaea;--soft:#bcc3c5;--muted:#868e92;--accent:#3fb0b6;--accent-ink:#7fd0d4;--accent2:#d9945a;
 --bg:#101315;--card:#191d20;--card2:#20262a;--rule:#2b3236;--good:#4bbd93;--bad:#df6b6b;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.35);}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#e8eaea;--soft:#bcc3c5;--muted:#868e92;--accent:#3fb0b6;--accent-ink:#7fd0d4;--accent2:#d9945a;
 --bg:#101315;--card:#191d20;--card2:#20262a;--rule:#2b3236;--good:#4bbd93;--bad:#df6b6b;
 --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.35);}}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.6;font-size:15.5px;-webkit-font-smoothing:antialiased}
.app{display:grid;grid-template-columns:264px 1fr;min-height:100vh}
/* ---- topbar (mobile) ---- */
.topbar{display:none;position:sticky;top:0;z-index:var(--z-topbar);align-items:center;gap:12px;
 padding:10px 14px;padding-top:max(10px,env(safe-area-inset-top));background:color-mix(in oklab,var(--bg) 88%,transparent);
 backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--rule)}
.topbar .tt{font-family:var(--serif);font-size:17px;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.iconbtn{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;flex:none;
 border:1px solid var(--rule);background:var(--card);border-radius:10px;cursor:pointer;color:var(--ink);font-size:17px;transition:border-color .15s}
.iconbtn:hover{border-color:var(--accent)}
.burger{flex-direction:column;gap:4px}.burger span{display:block;width:17px;height:2px;background:var(--ink);border-radius:2px}
.scrim{display:none}
/* ---- sidebar ---- */
aside{border-right:1px solid var(--rule);padding:24px 16px 40px;position:sticky;top:0;height:100vh;overflow:auto;
 background:linear-gradient(180deg,color-mix(in oklab,var(--accent) 5%,var(--bg)),var(--bg) 220px)}
.brand{display:flex;align-items:center;gap:8px;margin-bottom:2px}
.brand h1{font-family:var(--serif);font-size:22px;letter-spacing:-.01em;flex:1}
.brand .dot{width:9px;height:9px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px color-mix(in oklab,var(--accent) 18%,transparent)}
.sclose{display:none}
.prog{color:var(--muted);font-size:12px;margin:2px 0 9px}
.bar{height:7px;background:var(--card2);border-radius:99px;overflow:hidden;margin-bottom:18px}
.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),color-mix(in oklab,var(--accent) 60%,var(--good)));border-radius:99px;transition:width .5s var(--ease)}
.daynav{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:-8px 0 16px;font-size:12px;color:var(--muted)}
.daynav .dl b{color:var(--ink);font-size:13px}
.daynav .dctl{display:flex;align-items:center;gap:5px}
.daynav .dctl button{width:26px;height:26px;padding:0;border-radius:7px;font-size:15px;line-height:1;font-weight:700}
.daynav .dctl a{color:var(--accent-ink);cursor:pointer;font-weight:600;font-size:11.5px}
.locked .cta.ghost{background:transparent;color:var(--accent-ink);border-color:color-mix(in oklab,var(--accent) 30%,var(--rule));margin-left:8px}
.quick{list-style:none;display:flex;gap:7px;margin-bottom:20px}
.quick li{flex:1;text-align:center;padding:9px 6px;border:1px solid var(--rule);border-radius:10px;cursor:pointer;
 font-size:12.5px;font-weight:600;color:var(--soft);background:var(--card);transition:.15s;display:flex;flex-direction:column;gap:3px;align-items:center}
.quick li:hover{border-color:var(--accent);color:var(--ink)}.quick li.on{background:color-mix(in oklab,var(--accent) 12%,var(--card));border-color:var(--accent);color:var(--accent-ink)}
.quick .qi{font-size:16px;line-height:1}
.nav{list-style:none;font-size:13px}
.nav li{padding:6px 9px;border-radius:8px;cursor:pointer;color:var(--soft);display:flex;gap:8px;align-items:baseline;transition:background .12s}
.nav li:hover{background:color-mix(in oklab,var(--accent) 8%,transparent)}
.nav li.on{background:color-mix(in oklab,var(--accent) 15%,transparent);color:var(--ink);font-weight:600}
.nav li.lock{cursor:default;color:var(--muted)}.nav li.lock:hover{background:transparent}
.nav .grp{margin:18px 0 5px;font-family:var(--serif);font-size:12px;color:var(--accent-ink);font-weight:700;
 letter-spacing:.04em;text-transform:uppercase;pointer-events:none;border-bottom:1px solid var(--rule);padding-bottom:4px}
.nav .st{width:15px;flex:none;text-align:center;font-size:12px}
.done .st{color:var(--good)}.rep .st{color:var(--accent2)}.nav li .nm{overflow:hidden;text-overflow:ellipsis}
.nav li.note-flag .nm::after{content:"✎";color:var(--accent);margin-left:5px;font-size:11px}
/* ---- main ---- */
main{padding:40px clamp(20px,5vw,56px);max-width:820px;width:100%}
.crumb{color:var(--accent-ink);font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.09em;margin-bottom:4px}
.lesson{text-wrap:pretty}
.lesson>h1:first-child,.lesson h1{font-family:var(--serif);font-size:clamp(24px,5vw,30px);margin:8px 0 10px;line-height:1.15;letter-spacing:-.015em;text-wrap:balance}
.lesson h2{font-size:18px;margin:30px 0 8px;color:var(--accent-ink);border-bottom:1px solid var(--rule);padding-bottom:5px;font-weight:700}
.lesson h3{font-size:15.5px;margin:18px 0 6px;font-weight:700}
.lesson p{margin:10px 0}.lesson ul,.lesson ol{margin:9px 0 9px 22px}.lesson li{margin:5px 0}
.lesson strong,.lesson b{color:var(--ink)}
.lesson code{background:color-mix(in oklab,var(--accent) 12%,transparent);color:var(--accent-ink);padding:1.5px 6px;border-radius:6px;font-size:13px;font-family:"SF Mono",ui-monospace,Menlo,monospace}
.lesson blockquote{padding:12px 16px;margin:16px 0;background:color-mix(in oklab,var(--accent) 7%,var(--card));border:1px solid color-mix(in oklab,var(--accent) 22%,var(--rule));border-radius:12px;color:var(--soft)}
.lesson blockquote strong{color:var(--accent-ink)}
.lesson a{color:var(--accent-ink);text-underline-offset:2px}.lesson hr{border:0;border-top:1px solid var(--rule);margin:24px 0}
.lesson figure{margin:20px 0;padding:16px;background:var(--card);border:1px solid var(--rule);border-radius:14px;box-shadow:var(--shadow);overflow-x:auto}
.lesson figure svg{max-width:100%;height:auto;display:block;margin:0 auto}
.lesson figcaption{margin-top:10px;font-size:12.5px;color:var(--muted);text-align:center}
.lesson table{border-collapse:collapse;width:100%;margin:16px 0;font-size:14px}
.lesson th,.lesson td{border:1px solid var(--rule);padding:8px 11px;text-align:left}.lesson th{background:var(--card2)}
/* ---- quiz ---- */
.quiz{margin-top:36px;border-top:2px solid var(--rule);padding-top:22px}
.quiz-h{display:flex;align-items:baseline;gap:10px;margin-bottom:4px}
.quiz-h h2{font-family:var(--serif);font-size:21px}.quiz-h .sub{color:var(--muted);font-size:13px}
.qcard{background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:15px 17px;margin:12px 0;box-shadow:var(--shadow);transition:border-color .15s}
.qcard.open{border-color:color-mix(in oklab,var(--accent) 35%,var(--rule))}
.qq{font-weight:600;line-height:1.5}
.qa{margin-top:0;max-height:0;overflow:hidden;color:var(--soft);transition:max-height .3s var(--ease),margin-top .3s,padding-top .3s}
.qcard.open .qa{max-height:600px;margin-top:11px;padding-top:11px;border-top:1px dashed var(--rule)}
.qbtns{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}
button{font:inherit;font-weight:600;border:1px solid var(--rule);background:var(--card);color:var(--ink);padding:8px 14px;border-radius:9px;cursor:pointer;transition:.15s}
button:hover{border-color:var(--accent);transform:translateY(-1px)}
button:active{transform:translateY(0)}
button.rev{color:var(--accent-ink);border-color:color-mix(in oklab,var(--accent) 30%,var(--rule))}
button.ok.sel{background:var(--good);color:#fff;border-color:var(--good)}button.no.sel{background:var(--bad);color:#fff;border-color:var(--bad)}
.cta{background:var(--accent);color:#fff;border-color:var(--accent);padding:10px 18px}
.cta:hover{background:var(--accent-ink);border-color:var(--accent-ink)}
.result{margin-top:20px;padding:16px 18px;border-radius:14px;border:1px solid var(--rule);background:var(--card);box-shadow:var(--shadow)}
.result b{font-size:18px;font-family:var(--serif)}.done-btn{margin-top:12px}
/* ---- notes ---- */
.notes{margin-top:34px;border-top:1px solid var(--rule);padding-top:22px}
.notes h2{font-family:var(--serif);font-size:19px;display:flex;align-items:center;gap:8px}
.notes .hint{color:var(--muted);font-size:13px;margin:4px 0 10px}
.notes textarea{width:100%;min-height:120px;resize:vertical;padding:13px 15px;border:1px solid var(--rule);border-radius:12px;
 background:var(--card);color:var(--ink);font:inherit;line-height:1.6;box-shadow:var(--shadow)}
.notes textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in oklab,var(--accent) 18%,transparent)}
.saved{display:inline-block;margin-top:7px;font-size:12px;color:var(--good);opacity:0;transition:opacity .3s}
.saved.show{opacity:1}
/* ---- history / locked ---- */
.pagehead{font-family:var(--serif);font-size:clamp(24px,5vw,30px);margin-bottom:4px;letter-spacing:-.015em}
.lead{color:var(--muted);margin-bottom:22px}
.hist{list-style:none;display:flex;flex-direction:column;gap:10px}
.hrow{display:flex;align-items:center;gap:14px;padding:14px 16px;background:var(--card);border:1px solid var(--rule);border-radius:13px;cursor:pointer;box-shadow:var(--shadow);transition:.15s}
.hrow:hover{border-color:var(--accent);transform:translateY(-1px)}
.hbadge{width:42px;height:42px;flex:none;border-radius:11px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.hbadge.ok{background:color-mix(in oklab,var(--good) 16%,var(--card));color:var(--good)}
.hbadge.rep{background:color-mix(in oklab,var(--accent2) 16%,var(--card));color:var(--accent2)}
.hrow .ht{font-weight:600;line-height:1.35}.hrow .hm{color:var(--muted);font-size:12.5px;margin-top:2px}
.hrow .harrow{margin-left:auto;color:var(--muted)}
.locked{text-align:center;padding:56px 20px;color:var(--muted)}
.locked .lk{font-size:40px;margin-bottom:12px}.locked b{color:var(--ink);font-family:var(--serif);font-size:20px}
.empty{color:var(--muted);margin-top:40px}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
/* ---- responsive: off-canvas drawer ---- */
@media(max-width:820px){
 .app{grid-template-columns:1fr}
 .topbar{display:flex}
 aside{position:fixed;left:0;top:0;height:100dvh;width:min(84vw,330px);z-index:var(--z-drawer);
  transform:translateX(-100%);transition:transform .34s var(--ease);box-shadow:0 0 40px rgba(0,0,0,.28);border-right:1px solid var(--rule)}
 aside.open{transform:none}
 .sclose{display:inline-flex}
 .scrim{display:block;position:fixed;inset:0;z-index:var(--z-scrim);background:rgba(0,0,0,.45);
  opacity:0;pointer-events:none;transition:opacity .3s}
 .scrim.open{opacity:1;pointer-events:auto}
 main{padding:22px 18px 60px}
}
</style></head><body>
<div class="topbar">
 <button class="iconbtn burger" aria-label="Menu" onclick="openNav()"><span></span><span></span><span></span></button>
 <span class="tt" id="tbtitle">Ripasso Uni</span>
 <button class="iconbtn" aria-label="Tema" onclick="toggleTheme()">◐</button>
</div>
<div class="scrim" id="scrim" onclick="closeNav()"></div>
<div class="app">
<aside id="side">
  <div class="brand"><span class="dot"></span><h1>Ripasso Uni</h1>
    <button class="iconbtn" aria-label="Tema" onclick="toggleTheme()" style="width:32px;height:32px;font-size:15px">◐</button>
    <button class="iconbtn sclose" aria-label="Chiudi" onclick="closeNav()" style="width:32px;height:32px;font-size:15px">✕</button></div>
  <div class="prog" id="prog"></div><div class="bar"><i id="barfill"></i></div>
  <div class="daynav" id="daynav"></div>
  <ul class="quick">
    <li id="q-today" onclick="openToday()"><span class="qi">◉</span>Oggi</li>
    <li id="q-hist" onclick="openHistory()"><span class="qi">✓</span>Storico</li>
  </ul>
  <ul class="nav" id="nav"></ul>
</aside>
<main id="main"></main>
</div>
<script>
const DATA=__DATA__;
const KEY="ripasso_progress_v1",NKEY="ripasso_notes_v1",SKEY="ripasso_start_v1",TKEY="ripasso_theme";
let ST=JSON.parse(localStorage.getItem(KEY)||"{}");     // {topic_id:{status,score,ts}}
let NOTES=JSON.parse(localStorage.getItem(NKEY)||"{}"); // {topic_id:"..."}
function save(){localStorage.setItem(KEY,JSON.stringify(ST));}
function saveNotes(){localStorage.setItem(NKEY,JSON.stringify(NOTES));}
const byId=Object.fromEntries(DATA.lessons.map(l=>[l.topic_id,l]));
const escH=t=>(t||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
// ---- theme ----
function applyTheme(){const t=localStorage.getItem(TKEY);if(t)document.documentElement.setAttribute("data-theme",t);}
function toggleTheme(){const c=document.documentElement.getAttribute("data-theme");
 const dark=c?c==="dark":matchMedia("(prefers-color-scheme:dark)").matches;
 const n=dark?"light":"dark";localStorage.setItem(TKEY,n);document.documentElement.setAttribute("data-theme",n);}
applyTheme();
// ---- drawer ----
function openNav(){document.getElementById("side").classList.add("open");document.getElementById("scrim").classList.add("open");}
function closeNav(){document.getElementById("side").classList.remove("open");document.getElementById("scrim").classList.remove("open");}
// ---- date gating (uno al giorno, dom–ven; sabato riposo) ----
function anchor(){let s=localStorage.getItem(SKEY);if(!s){let d=new Date();d.setHours(0,0,0,0);s=d.toISOString();localStorage.setItem(SKEY,s);}return new Date(s);}
function studyDay(){let d=new Date(anchor());d.setHours(0,0,0,0);let e=new Date();e.setHours(0,0,0,0);let c=0;
 while(d<=e){if(d.getDay()!==6)c++;d.setDate(d.getDate()+1);}return Math.max(c,1);}
function unlockDateOf(n){let d=new Date(anchor());d.setHours(0,0,0,0);let c=0;
 while(true){if(d.getDay()!==6){c++;if(c>=n)return new Date(d);}d.setDate(d.getDate()+1);}}
function isUnlocked(l){return !l.day||l.day<=studyDay();}
const fmtDate=d=>d.toLocaleDateString("it-IT",{weekday:"long",day:"numeric",month:"long"});
// ---- posizionamento manuale del giorno (per riprendere da dove sei) ----
const maxDay=()=>DATA.lessons.reduce((m,l)=>Math.max(m,l.day||0),1);
function setDay(n){n=Math.max(1,Math.min(n,maxDay()));
 let d=new Date();d.setHours(0,0,0,0);let c=0;
 while(true){if(d.getDay()!==6){c++;if(c>=n)break;}d.setDate(d.getDate()-1);}
 localStorage.setItem(SKEY,d.toISOString());renderNav();openToday();}
function dayStep(k){setDay(Math.min(studyDay(),maxDay())+k);}
function renderDay(){const el=document.getElementById("daynav");if(!el)return;
 const tot=maxDay();const n=Math.min(studyDay(),tot);
 el.innerHTML=`<span class="dl">Giorno <b>${n}</b>/${tot}</span>
  <span class="dctl"><button onclick="dayStep(-1)" aria-label="giorno precedente">−</button>`+
  `<button onclick="dayStep(1)" aria-label="giorno successivo">+</button>`+
  `<a onclick="setDay(${tot})">all'ultima</a></span>`;}
// ---- mini markdown → html ----
function md(s){
 const esc=t=>t.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
 function inline(t){return esc(t)
   .replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/(^|[^*])\*(?!\s)(.+?)\*/g,"$1<i>$2</i>")
   .replace(/`([^`]+)`/g,"<code>$1</code>").replace(/\[(.+?)\]\((.+?)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');}
 const lines=s.split("\n");let out=[],i=0;
 while(i<lines.length){let l=lines[i];
  const hb=l.match(/^\s*<(svg|figure|div|table|img|pre)\b/i);
  if(hb){const tag=hb[1].toLowerCase();let buf=[];
    while(i<lines.length){buf.push(lines[i]);
      if(new RegExp("</"+tag+">","i").test(lines[i])||(tag==="img"&&/>/.test(lines[i]))){i++;break;}i++;}
    out.push(buf.join("\n"));continue;}
  if(/^###\s/.test(l)){out.push("<h3>"+inline(l.slice(4))+"</h3>");i++;continue;}
  if(/^##\s/.test(l)){out.push("<h2>"+inline(l.slice(3))+"</h2>");i++;continue;}
  if(/^#\s/.test(l)){out.push("<h1>"+inline(l.slice(2))+"</h1>");i++;continue;}
  if(/^---\s*$/.test(l)){out.push("<hr>");i++;continue;}
  if(/^>\s?/.test(l)){let b=[];while(i<lines.length&&/^>\s?/.test(lines[i])){b.push(inline(lines[i].replace(/^>\s?/,"")));i++;}out.push("<blockquote>"+b.join("<br>")+"</blockquote>");continue;}
  if(/^\s*[-*]\s/.test(l)){let b=[];while(i<lines.length&&/^\s*[-*]\s/.test(lines[i])){b.push("<li>"+inline(lines[i].replace(/^\s*[-*]\s/,""))+"</li>");i++;}out.push("<ul>"+b.join("")+"</ul>");continue;}
  if(/^\s*\d+\.\s/.test(l)){let b=[];while(i<lines.length&&/^\s*\d+\.\s/.test(lines[i])){b.push("<li>"+inline(lines[i].replace(/^\s*\d+\.\s/,""))+"</li>");i++;}out.push("<ol>"+b.join("")+"</ol>");continue;}
  if(l.trim()===""){i++;continue;}
  out.push("<p>"+inline(l)+"</p>");i++;}
 return out.join("\n");}

function statusOf(tid){return (ST[tid]||{}).status||"todo";}
let cur=null;
function setQuick(id){["q-today","q-hist"].forEach(x=>document.getElementById(x).classList.toggle("on",x===id));}
function renderNav(){
 const nav=document.getElementById("nav");let done=0;
 const AREAS={"computer-science":"Informatica","management":"Gestionale","cross-cutting":"Trasversale"};
 let out="",last=null;
 DATA.order.forEach(t=>{const s=statusOf(t.id);if(s==="mastered")done++;
   if(t.area!==last){out+=`<li class="grp">${AREAS[t.area]||t.area}</li>`;last=t.area;}
   const l=byId[t.id];const locked=l&&!isUnlocked(l);
   const cls=(s==="mastered"?"done":s==="to-repeat"?"rep":"")+(cur===t.id?" on":"")+(locked?" lock":"")+((NOTES[t.id]||"").trim()?" note-flag":"");
   const icon=locked?"🔒":s==="mastered"?"✓":s==="to-repeat"?"↻":l?"●":"·";
   const click=l?(locked?`onclick="openLesson('${t.id}')"`:`onclick="openLesson('${t.id}')"`):"";
   out+=`<li class="${cls}" ${click} title="${escH(t.course)}"><span class="st">${icon}</span><span class="nm">${escH(t.name)}</span></li>`;
 });
 nav.innerHTML=out;
 document.getElementById("prog").textContent=`${done}/${DATA.total} padroneggiati · ${DATA.lessons.length} lezioni pronte`;
 document.getElementById("barfill").style.width=(done/DATA.total*100)+"%";renderDay();}

function openLesson(tid){cur=tid;closeNav();setQuick(null);const l=byId[tid];const m=document.getElementById("main");
 document.getElementById("tbtitle").textContent=l?l.title.split("—")[0].trim():"Ripasso Uni";
 if(!l){m.innerHTML='<p class="empty">Lezione non ancora generata.</p>';renderNav();return;}
 if(!isUnlocked(l)){const ud=unlockDateOf(l.day);
   m.innerHTML=`<div class="crumb">${escH(l.area)} · Giorno ${l.day}</div>
     <div class="locked"><div class="lk">🔒</div><b>Ancora chiusa</b>
     <p style="margin-top:8px">Una lezione al giorno (dom–ven). Questa si sblocca<br><b style="font-size:15px">${fmtDate(ud)}</b>.</p>
     <p style="margin-top:14px"><button class="cta" onclick="openToday()">Vai alla lezione di oggi</button><button class="cta ghost" onclick="setDay(${l.day})">Riprendi da qui ora</button></p></div>`;
   window.scrollTo(0,0);renderNav();return;}
 window._marks={};
 let q=l.quiz.map((x,idx)=>`<div class="qcard" id="q${idx}"><div class="qq">${idx+1}. ${md(x.q).replace(/^<p>|<\/p>$/g,"")}</div>
   <div class="qa">${md(x.a)}</div>
   <div class="qbtns"><button class="rev" onclick="reveal(${idx})">Mostra risposta</button>
   <button class="ok" onclick="mark(${idx},1)">✓ la sapevo</button>
   <button class="no" onclick="mark(${idx},0)">✗ non la sapevo</button></div></div>`).join("");
 m.innerHTML=`<div class="crumb">${escH(l.area)} · ${escH(l.course)}${l.day?" · Giorno "+l.day:""}</div>
   <div class="lesson">${md(l.body)}</div>
   <div class="quiz"><div class="quiz-h"><h2>Quiz</h2><span class="sub">${l.quiz.length} domande · segna cosa sapevi</span></div>${q}<div id="res"></div></div>
   <section class="notes"><h2>✎ Le mie note</h2>
     <p class="hint">Appunti tuoi — es. un approfondimento fatto con l'AI che vuoi ritrovare. Si salvano da soli su questo dispositivo.</p>
     <textarea id="note" placeholder="Scrivi qui…" oninput="saveNote()">${escH(NOTES[tid]||"")}</textarea>
     <span class="saved" id="notesaved">salvato ✓</span></section>`;
 window.scrollTo(0,0);renderNav();grade();}

function saveNote(){const v=document.getElementById("note").value;
 if(v.trim())NOTES[cur]=v;else delete NOTES[cur];saveNotes();
 const s=document.getElementById("notesaved");s.classList.add("show");clearTimeout(window._nt);
 window._nt=setTimeout(()=>s.classList.remove("show"),1200);}
function reveal(i){document.getElementById("q"+i).classList.add("open");}
function mark(i,ok){const c=document.getElementById("q"+i);c.classList.add("open");
 c.querySelector(".ok").classList.toggle("sel",ok===1);c.querySelector(".no").classList.toggle("sel",ok===0);
 window._marks[i]=ok;grade();}
function grade(){const l=byId[cur];if(!l)return;const tot=l.quiz.length;const ansd=Object.keys(window._marks).length;
 const res=document.getElementById("res");if(!res)return;
 if(ansd<tot){res.innerHTML=`<div class="result">Rispondi a tutte (${ansd}/${tot}) per chiudere la lezione.</div>`;return;}
 const score=Object.values(window._marks).reduce((a,b)=>a+b,0);const pct=Math.round(score/tot*100);const pass=pct>=70;
 res.innerHTML=`<div class="result"><b>${score}/${tot} · ${pct}%</b> — ${pass?"padroneggiato ✅":"da ripassare ↻ (torna tra qualche giorno)"}.
   <div class="done-btn"><button class="cta" onclick="finish(${pass?1:0})">${pass?"Segna completata":"Segna da ripassare"}</button></div></div>`;}
function finish(pass){ST[cur]={status:pass?"mastered":"to-repeat",score:Object.values(window._marks).reduce((a,b)=>a+b,0),ts:Date.now()};
 save();window._marks={};renderNav();
 const next=DATA.lessons.slice().reverse().find(l=>statusOf(l.topic_id)==="todo"&&isUnlocked(l));
 if(next)openLesson(next.topic_id);else openHistory();}

function openToday(){closeNav();setQuick("q-today");
 const unlocked=DATA.lessons.filter(isUnlocked);
 const today=unlocked.find(l=>l.day===studyDay());
 const pick=today||unlocked.slice().reverse().find(l=>statusOf(l.topic_id)!=="mastered")||unlocked[unlocked.length-1];
 if(pick)openLesson(pick.topic_id);
 else document.getElementById("main").innerHTML='<p class="empty">Nessuna lezione ancora. Genera la prima con il loop.</p>';
 setQuick("q-today");}

function openHistory(){cur="__hist__";closeNav();setQuick("q-hist");renderNav();
 document.getElementById("tbtitle").textContent="Storico";
 const rows=DATA.lessons.filter(l=>{const s=statusOf(l.topic_id);return s==="mastered"||s==="to-repeat";})
   .map(l=>({l,s:ST[l.topic_id]})).sort((a,b)=>(b.s.ts||0)-(a.s.ts||0));
 const m=document.getElementById("main");
 let body;
 if(!rows.length){body=`<p class="lead">Qui compaiono le lezioni che hai già affrontato, con voto e data — per ritrovarle quando non ricordi qualcosa. Ancora nessuna: comincia da <b>Oggi</b>.</p>`;}
 else{body=`<p class="lead">${rows.length} lezione/i affrontate. Tocca per rileggerle (con le tue note).</p><ul class="hist">`+
   rows.map(({l,s})=>{const ok=s.status==="mastered";const d=s.ts?new Date(s.ts).toLocaleDateString("it-IT",{day:"numeric",month:"short"}):"";
     const tot=l.quiz.length;const note=(NOTES[l.topic_id]||"").trim()?" · ✎ note":"";
     return `<li class="hrow" onclick="openLesson('${l.topic_id}')">
       <div class="hbadge ${ok?"ok":"rep"}">${s.score!=null?s.score+"/"+tot:(ok?"✓":"↻")}</div>
       <div><div class="ht">${escH(l.title.split("—")[0].trim())}</div>
       <div class="hm">${ok?"padroneggiata":"da ripassare"} · ${d}${note}</div></div>
       <span class="harrow">›</span></li>`;}).join("")+`</ul>`;}
 m.innerHTML=`<div class="crumb">Il tuo percorso</div><h1 class="pagehead">Storico</h1>${body}`;
 window.scrollTo(0,0);}

renderNav();
if(DATA.lessons.length){openToday();}else{document.getElementById("main").innerHTML='<p class="empty">Nessuna lezione ancora. Genera la prima con il loop.</p>';}
</script></body></html>"""

out=APP.replace("__DATA__",DATA)
(ROOT/"index.html").write_text(out)
print(f"index.html scritta · {len(lessons)} lezione/i · {len(order)} topic totali")
