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
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Ripasso Uni</title>
<style>
:root{--ink:#1a1c1f;--soft:#464c54;--muted:#6b7178;--accent:#0e5d63;--accent2:#7a3d12;--bg:#fbfcfd;--card:#fff;--rule:#e6e8ec;--good:#0e7c5a;--bad:#b23a3a;
--sans:"Avenir Next","Segoe UI",system-ui,sans-serif;--serif:"Charter",Georgia,serif;}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--ink:#e9eaec;--soft:#c2c6cc;--muted:#8a9098;--bg:#131417;--card:#1b1d21;--rule:#2a2d33;}}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.55;font-size:15px}
.layout{display:grid;grid-template-columns:250px 1fr;min-height:100vh}
aside{border-right:1px solid var(--rule);padding:22px 16px;position:sticky;top:0;height:100vh;overflow:auto}
aside h1{font-family:var(--serif);font-size:20px}.prog{color:var(--muted);font-size:12px;margin:4px 0 14px}
.bar{height:6px;background:var(--rule);border-radius:6px;overflow:hidden;margin-bottom:16px}.bar i{display:block;height:100%;background:var(--accent)}
.nav{list-style:none;font-size:12.5px}.nav li{padding:5px 8px;border-radius:7px;cursor:pointer;color:var(--soft);display:flex;gap:7px;align-items:baseline}
.nav li:hover{background:color-mix(in oklab,var(--accent) 8%,transparent)}.nav li.on{background:color-mix(in oklab,var(--accent) 14%,transparent);color:var(--ink);font-weight:600}
.nav .grp{margin:15px 0 3px;font-family:var(--serif);font-size:12.5px;color:var(--accent);font-weight:700;letter-spacing:.03em;pointer-events:none;border-bottom:1px solid var(--rule);padding-bottom:3px}
.nav .st{width:14px;flex:none}.done .st{color:var(--good)}.rep .st{color:var(--accent2)}
main{padding:34px 40px;max-width:820px}
.crumb{color:var(--accent);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.08em}
h2.tt{font-family:var(--serif);font-size:27px;margin:6px 0 18px;line-height:1.15}
.lesson h1{font-family:var(--serif);font-size:23px;margin:22px 0 8px}
.lesson h2{font-size:17px;margin:22px 0 8px;color:var(--accent);border-bottom:1px solid var(--rule);padding-bottom:4px}
.lesson h3{font-size:15px;margin:16px 0 6px}
.lesson p{margin:9px 0}.lesson ul,.lesson ol{margin:8px 0 8px 22px}.lesson li{margin:4px 0}
.lesson code{background:color-mix(in oklab,var(--accent) 10%,transparent);padding:1px 5px;border-radius:5px;font-size:13px}
.lesson blockquote{border-left:3px solid var(--accent);padding:6px 14px;margin:12px 0;background:color-mix(in oklab,var(--accent) 6%,transparent);border-radius:0 8px 8px 0;color:var(--soft)}
.lesson a{color:var(--accent)}.lesson hr{border:0;border-top:1px solid var(--rule);margin:20px 0}
.quiz{margin-top:28px;border-top:2px solid var(--rule);padding-top:18px}
.quiz h2{font-family:var(--serif);font-size:20px;margin-bottom:6px}
.qcard{background:var(--card);border:1px solid var(--rule);border-radius:11px;padding:14px 16px;margin:11px 0}
.qq{font-weight:600}.qa{margin-top:9px;padding-top:9px;border-top:1px dashed var(--rule);color:var(--soft);display:none}
.qcard.open .qa{display:block}
.qbtns{margin-top:10px;display:flex;gap:8px;flex-wrap:wrap}
button{font:inherit;border:1px solid var(--rule);background:var(--card);color:var(--ink);padding:6px 12px;border-radius:8px;cursor:pointer}
button:hover{border-color:var(--accent)}button.rev{color:var(--accent);font-weight:600}
button.ok.sel{background:var(--good);color:#fff;border-color:var(--good)}button.no.sel{background:var(--bad);color:#fff;border-color:var(--bad)}
.result{margin-top:18px;padding:14px 16px;border-radius:11px;border:1px solid var(--rule);background:var(--card)}
.result b{font-size:17px}.done-btn{margin-top:12px}
.empty{color:var(--muted);margin-top:40px}
@media(max-width:720px){.layout{grid-template-columns:1fr}aside{position:static;height:auto;border-right:0;border-bottom:1px solid var(--rule)}}
</style></head><body>
<div class="layout">
<aside>
  <h1>Ripasso Uni</h1><div class="prog" id="prog"></div><div class="bar"><i id="barfill"></i></div>
  <ul class="nav" id="nav"></ul>
</aside>
<main id="main"></main>
</div>
<script>
const DATA=__DATA__;
const KEY="ripasso_progress_v1";
let ST=JSON.parse(localStorage.getItem(KEY)||"{}"); // {topic_id:{status,score,ts}}
function save(){localStorage.setItem(KEY,JSON.stringify(ST));}
const byId=Object.fromEntries(DATA.lessons.map(l=>[l.topic_id,l]));
// mini markdown → html
function md(s){
 s=s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
 const lines=s.split("\n");let out=[],i=0;
 function inline(t){return t
   .replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/(^|[^*])\*(?!\s)(.+?)\*/g,"$1<i>$2</i>")
   .replace(/`([^`]+)`/g,"<code>$1</code>").replace(/\[(.+?)\]\((.+?)\)/g,'<a href="$2" target="_blank">$1</a>');}
 while(i<lines.length){let l=lines[i];
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
function renderNav(){
 const nav=document.getElementById("nav");let done=0;
 const AREAS={"computer-science":"Informatica","management":"Gestionale","cross-cutting":"Trasversale"};
 let out="",last=null;
 DATA.order.forEach(t=>{const s=statusOf(t.id);if(s==="mastered")done++;
   if(t.area!==last){out+=`<li class="grp">${AREAS[t.area]||t.area}</li>`;last=t.area;}
   const has=byId[t.id];const cls=(s==="mastered"?"done":s==="to-repeat"?"rep":"")+(cur===t.id?" on":"");
   const icon=s==="mastered"?"✓":s==="to-repeat"?"↻":has?"•":"·";
   out+=`<li class="${cls}" ${has?`onclick="openLesson('${t.id}')"`:""} title="${t.course}"><span class="st">${icon}</span><span>${t.name}</span></li>`;
 });
 nav.innerHTML=out;
 document.getElementById("prog").textContent=`${done}/${DATA.total} padroneggiati · ${DATA.lessons.length} lezioni pronte`;
 document.getElementById("barfill").style.width=(done/DATA.total*100)+"%";}

let cur=null;
function openLesson(tid){cur=tid;const l=byId[tid];const m=document.getElementById("main");
 if(!l){m.innerHTML='<p class="empty">Lezione non ancora generata.</p>';return;}
 let q=l.quiz.map((x,idx)=>`<div class="qcard" id="q${idx}"><div class="qq">${idx+1}. ${md(x.q).replace(/^<p>|<\/p>$/g,"")}</div>
   <div class="qa">${md(x.a)}</div>
   <div class="qbtns"><button class="rev" onclick="reveal(${idx})">Mostra risposta</button>
   <button class="ok" onclick="mark(${idx},1)">✓ la sapevo</button>
   <button class="no" onclick="mark(${idx},0)">✗ non la sapevo</button></div></div>`).join("");
 m.innerHTML=`<div class="crumb">${l.area} · ${l.course}${l.day?" · Giorno "+l.day:""}</div>
   <div class="lesson">${md(l.body)}</div>
   <div class="quiz"><h2>Quiz</h2>${q}<div id="res"></div></div>`;
 window.scrollTo(0,0);renderNav();grade();}
function reveal(i){document.getElementById("q"+i).classList.add("open");}
window._marks={};
function mark(i,ok){const c=document.getElementById("q"+i);c.classList.add("open");
 c.querySelector(".ok").classList.toggle("sel",ok===1);c.querySelector(".no").classList.toggle("sel",ok===0);
 window._marks[i]=ok;grade();}
function grade(){const l=byId[cur];const tot=l.quiz.length;const ansd=Object.keys(window._marks).length;
 const res=document.getElementById("res");if(!res)return;
 if(ansd<tot){res.innerHTML=`<div class="result">Rispondi a tutte (${ansd}/${tot}) per chiudere la lezione.</div>`;return;}
 const score=Object.values(window._marks).reduce((a,b)=>a+b,0);const pct=Math.round(score/tot*100);
 const pass=pct>=70;
 res.innerHTML=`<div class="result"><b>${score}/${tot} (${pct}%)</b> — ${pass?"padroneggiato ✅":"da ripassare ↻ (torna tra qualche giorno)"}.
   <div class="done-btn"><button onclick="finish(${pass?1:0})">${pass?"Segna completata":"Segna da ripassare"}</button></div></div>`;}
function finish(pass){ST[cur]={status:pass?"mastered":"to-repeat",score:Object.values(window._marks).reduce((a,b)=>a+b,0),ts:Date.now()};
 save();window._marks={};renderNav();
 // go to newest unseen lesson
 const next=DATA.lessons.slice().reverse().find(l=>statusOf(l.topic_id)==="todo");
 if(next)openLesson(next.topic_id);else openLesson(cur);}
// start: newest not-mastered lesson, else the last one
function start(){const todo=DATA.lessons.slice().reverse().find(l=>statusOf(l.topic_id)!=="mastered");
 openLesson((todo||DATA.lessons[DATA.lessons.length-1]||{}).topic_id);}
renderNav();
if(DATA.lessons.length){start();}else{document.getElementById("main").innerHTML='<p class="empty">Nessuna lezione ancora. Genera la prima con il loop.</p>';}
</script></body></html>"""

out=APP.replace("__DATA__",DATA)
(ROOT/"index.html").write_text(out)
print(f"index.html scritta · {len(lessons)} lezione/i · {len(order)} topic totali")
