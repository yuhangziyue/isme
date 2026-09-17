# -*- coding: utf-8 -*-
import json, os
BASE = "."
SRC = "data"
Q = open(f"{SRC}/questions.json", encoding="utf-8").read()
F = open(f"{SRC}/figures.json", encoding="utf-8").read()

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>我是谁转世 · 历史名人人格原型测评</title>
<style>
:root{
  --paper:#f6f1e7; --paper2:#efe7d6; --ink:#2b2620; --ink2:#6b6155;
  --red:#8a1f1f; --red2:#a8402e; --gold:#a98a45; --line:#d8cdb6;
  --green:#3e5c48;
}
*{box-sizing:border-box;margin:0;padding:0;scrollbar-width:none;-ms-overflow-style:none}
*::-webkit-scrollbar{width:0;height:0;display:none;background:transparent}
html,body{background:var(--paper);color:var(--ink);
  font-family:"Songti SC","Noto Serif SC","STSong","SimSun",serif;
  line-height:1.75;-webkit-font-smoothing:antialiased}
body{overscroll-behavior-y:none;min-height:100dvh}
.wrap{max-width:760px;margin:0 auto;padding:32px 20px 80px}
.seal{display:inline-block;border:2px solid var(--red);color:var(--red);
  font-size:13px;letter-spacing:4px;padding:4px 10px;border-radius:4px;
  transform:rotate(-2deg);font-weight:700}
h1{font-size:34px;margin:18px 0 6px;letter-spacing:6px}
.slogan{font-size:19px;color:var(--red);letter-spacing:2px;font-weight:700;margin-top:14px}
.slogan::before{content:"「";color:var(--gold)}
.slogan::after{content:"」";color:var(--gold)}
.sub{color:var(--ink2);font-size:15px;letter-spacing:1px}
.card{background:#fffdf7;border:1px solid var(--line);border-radius:10px;
  padding:26px 28px;margin-top:22px;box-shadow:0 2px 14px rgba(80,60,20,.06)}
.meta-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px 18px;margin:14px 0;font-size:14px;color:var(--ink2)}
.meta-grid b{color:var(--ink)}
.btn{appearance:none;border:none;cursor:pointer;font-family:inherit;
  background:var(--red);color:#fdf6e9;font-size:17px;letter-spacing:4px;
  padding:13px 34px;border-radius:8px;transition:.2s}
.btn:hover{background:var(--red2)}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
.btn.ghost:hover{border-color:var(--gold);color:var(--gold)}
.btn:disabled{opacity:.35;cursor:not-allowed}
.btn.small{padding:8px 16px;font-size:14px;letter-spacing:2px}
.row{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:22px}
.note{font-size:12.5px;color:var(--ink2);margin-top:16px;border-top:1px dashed var(--line);padding-top:12px}
.guide{background:var(--paper);border-radius:8px;padding:12px 16px;margin-top:18px;
  font-size:13.5px;color:var(--ink2);border:1px solid var(--line)}
.guide b{color:var(--ink);letter-spacing:2px}
ul.clean{list-style:none}
ul.clean li{padding:7px 0 7px 20px;position:relative;font-size:15px}
ul.clean li::before{content:"";position:absolute;left:2px;top:15px;width:7px;height:7px;
  background:var(--gold);border-radius:50%}
/* 进度 */
.progress{height:6px;background:var(--paper2);border-radius:3px;overflow:hidden;margin:18px 0 4px}
.progress i{display:block;height:100%;background:linear-gradient(90deg,var(--red),var(--gold));width:0;transition:.25s}
.pcount{font-size:13px;color:var(--ink2);text-align:right;letter-spacing:2px}
.quiz-head{position:sticky;top:0;z-index:20;background:var(--paper);padding:12px 0 10px}
.autohint{font-size:12.5px;color:var(--ink2);text-align:center;margin-top:14px;letter-spacing:1px}
/* 题目 */
.qtext{font-size:20px;line-height:1.8;margin:26px 0 20px;font-weight:700}
.opts{display:flex;flex-direction:column;gap:10px}
.opt{display:flex;align-items:center;gap:12px;border:1px solid var(--line);
  border-radius:8px;padding:12px 16px;cursor:pointer;transition:.15s;background:#fffdf7;font-size:15.5px;-webkit-tap-highlight-color:transparent}
.opt:hover{border-color:var(--gold)}
.opt.sel{border-color:var(--red);background:#fbf0ea;font-weight:700}
.opt .dot{width:16px;height:16px;border:2px solid #b9ac92;border-radius:50%;flex:none;position:relative}
.opt.sel .dot{border-color:var(--red)}
.opt.sel .dot::after{content:"";position:absolute;inset:3px;border-radius:50%;background:var(--red)}
.warn{color:var(--red);font-size:13.5px;margin-top:10px;min-height:20px}
/* 结果 */
.hero{text-align:center;padding:8px 0 4px}
.hero .era{color:var(--ink2);font-size:14px;letter-spacing:2px;margin-top:6px}
.hero h2{font-size:40px;letter-spacing:8px;margin:10px 0 2px}
.hero .tag{color:var(--red);font-size:17px;letter-spacing:3px;font-weight:700}
.verdict{background:var(--paper);border-left:4px solid var(--red);padding:14px 18px;
  border-radius:0 8px 8px 0;margin:20px 0;font-size:15.5px}
h3.sec{font-size:17px;letter-spacing:3px;margin:26px 0 8px;padding-left:12px;
  border-left:4px solid var(--gold)}
.dimbar{margin:12px 0}
.dimbar .lab{display:flex;justify-content:space-between;flex-wrap:wrap;gap:0 8px;font-size:13.5px;color:var(--ink2);margin-bottom:3px}
.dimbar .track{height:8px;background:var(--paper2);border-radius:4px;position:relative;overflow:hidden}
.dimbar .fill{position:absolute;top:0;bottom:0;left:50%;background:var(--red);border-radius:4px}
.dimbar .mid{position:absolute;left:50%;top:-3px;bottom:-3px;width:1px;background:#b9ac92}
.dim-explain{font-size:13px;color:var(--ink2);margin-top:2px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:0 26px}
.neigh{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
.pill{border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-size:13.5px;background:#fffdf7}
.pill b{color:var(--red)}
.pill.link{cursor:pointer}
.pill.link:hover{border-color:var(--gold)}
.dual{background:#f3ece0;border:1px dashed var(--gold);border-radius:8px;padding:12px 16px;font-size:14.5px;margin:14px 0}
.footer-actions{margin-top:30px;text-align:center}
.histlist{font-size:13.5px;color:var(--ink2)}
.histlist b{color:var(--ink)}

/* 右上角「人物档案」入口 */
#archiveEntry{position:fixed;top:max(12px,env(safe-area-inset-top));right:12px;z-index:60;
  background:rgba(255,253,247,.94);border:1px solid var(--gold);color:var(--red);
  font-family:inherit;font-size:13.5px;letter-spacing:2px;font-weight:700;
  padding:9px 14px;border-radius:999px;cursor:pointer;box-shadow:0 2px 10px rgba(80,60,20,.12);
  -webkit-tap-highlight-color:transparent}
#archiveEntry:active{transform:scale(.96)}

/* 人物档案（全屏覆盖层） */
#screen-archive{position:fixed;inset:0;z-index:100;background:var(--paper);
  display:none;flex-direction:column}
.arc-head{position:sticky;top:0;z-index:5;background:var(--paper);
  border-bottom:1px solid var(--line);padding:max(10px,env(safe-area-inset-top)) 14px 10px;
  display:flex;align-items:center;gap:10px}
.arc-head .t{flex:1;text-align:center;font-weight:700;letter-spacing:3px;font-size:16px}
.arc-head .cnt{color:var(--ink2);font-size:13px;letter-spacing:1px;min-width:52px;text-align:right}
.arc-stage{flex:1;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;touch-action:pan-y}
.arc-track{display:flex;transition:transform .28s ease;will-change:transform}
.arc-page{flex:0 0 100%;max-width:100%;padding:14px 14px 40px;
  display:flex;flex-direction:column;gap:0}
.arc-page .card{margin-top:12px}
.arc-nav{position:fixed;top:50%;z-index:6;width:40px;height:40px;border-radius:50%;
  border:1px solid var(--line);background:rgba(255,253,247,.9);color:var(--red);
  font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;
  transform:translateY(-50%);box-shadow:0 2px 8px rgba(80,60,20,.12)}
#arcPrev{left:8px}#arcNext{right:8px}
.arc-dots{position:sticky;bottom:0;background:var(--paper);text-align:center;padding:10px 0 max(12px,env(safe-area-inset-bottom));
  border-top:1px solid var(--line)}
.arc-dots i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#cdbf9f;margin:0 3px;cursor:pointer}
.arc-dots i.on{background:var(--red);transform:scale(1.25)}
.arc-hint{text-align:center;font-size:12px;color:var(--ink2);padding:6px 0 0;letter-spacing:1px}
.arc-neigh{margin-top:26px}

/* ===== 移动化适配（≤720px 手机竖屏）：按宽高自适应，无可见滚动条 ===== */
@media(max-width:720px){
  html,body{height:100dvh;overflow:hidden}
  .wrap{height:100dvh;padding:54px 14px 12px;overflow-y:auto;overflow-x:hidden}
  section{max-width:100%}
  .card{padding:18px 15px;border-radius:8px;margin-top:16px}
  h1{font-size:clamp(24px,7.5vw,28px);letter-spacing:4px;margin:14px 0 4px}
  .slogan{font-size:clamp(15px,4.4vw,17px);margin-top:10px}
  .sub{font-size:12.5px;line-height:1.6}
  .seal{font-size:11.5px;padding:3px 8px}
  .meta-grid{grid-template-columns:1fr 1fr;gap:6px 12px;font-size:13px}
  .btn{padding:12px 14px;font-size:15.5px;letter-spacing:2px}
  .row{gap:10px;margin-top:16px}
  .row .btn{flex:1}
  .grid2{grid-template-columns:1fr;gap:10px}
  .guide{font-size:12.5px;padding:10px 12px;margin-top:14px}

  /* 答题屏：一屏完整容下，不滚动（显隐由 JS 内联样式控制）*/
  #screen-quiz{flex-direction:column;min-height:calc(100dvh - 96px)}
  #screen-quiz .card{flex:1;display:flex;flex-direction:column;margin-top:10px;padding:16px 14px}
  .quiz-head{padding:6px 0 8px}
  .qtext{font-size:clamp(16px,4.4vw,18px);line-height:1.65;margin:8px 0 14px}
  .opts{flex:1;justify-content:center;gap:8px}
  .opt{padding:10px 13px;font-size:15px;min-height:48px;gap:10px}
  .autohint{margin-top:10px;font-size:11.5px}
  #screen-quiz .row{margin-top:auto;padding-top:10px}

  /* 结果与档案：卡片内部信息紧凑，长文在容器内滑动，滚动条不可见 */
  .hero h2{font-size:30px;letter-spacing:6px}
  .hero .tag{font-size:15px;letter-spacing:2px}
  .hero .era{font-size:12.5px}
  .verdict{font-size:14.5px;padding:11px 13px;margin:14px 0}
  h3.sec{font-size:15.5px;letter-spacing:2px;margin:18px 0 5px}
  ul.clean li{font-size:14px;padding:5px 0 5px 18px}
  ul.clean li::before{top:13px}
  .dimbar{margin:9px 0}
  .pill{font-size:12.5px;padding:4px 11px}
  .histlist{font-size:12.5px}
  .note{font-size:11.5px}

  /* 档案覆盖层：自身管理全屏高度 */
  #screen-archive{height:100dvh}
  .arc-stage{flex:1;min-height:0}
  .arc-page{padding:10px 10px 30px}
  .arc-page .card{margin-top:10px}
  .arc-nav{width:34px;height:34px;font-size:16px}
  .arc-dots{padding:7px 0 8px}
  #archiveEntry{top:max(10px,env(safe-area-inset-top));right:10px;font-size:12.5px;padding:8px 12px}
}

/* 超矮屏（≤680px 高）进一步压缩答题屏 */
@media(max-width:720px) and (max-height:700px){
  .qtext{margin:4px 0 10px}
  .opt{min-height:44px;padding:8px 12px}
  .opts{gap:6px}
  .autohint{display:none}
}
</style>
</head>
<body>

<button id="archiveEntry" onclick="App.openArchive()">人物档案</button>

<div class="wrap">
  <!-- 封面 -->
  <section id="screen-intro">
    <span class="seal">正史认证 · v1.1</span>
    <h1>我是谁转世</h1>
    <div class="sub">中国历史名人人格原型测评 · 16 位正史人物 · 男女各半</div>
    <div class="slogan">更好的了解自己，解锁天赋吧</div>
    <div class="card">
      <div class="meta-grid">
        <div>题目：<b>共 48 个单选题</b></div>
        <div>用时：<b>需要 10 分钟左右</b></div>
        <div>计分：<b>5 点量表 · 六维 0–100</b></div>
        <div>输出：<b>主原型 + 雷达图 + 处事解析</b></div>
      </div>
      <p style="font-size:14.5px;color:var(--ink2)">基于<b style="color:var(--ink)">大五人格模型（OCEAN）</b>本土化的六个维度，
      把你的行为倾向与 16 位<b style="color:var(--ink)">正史有传、事迹可考</b>的真实决策者做原型匹配——曹操、诸葛亮、张良、韩信、苏轼、王安石、王阳明、曾国藩，
      以及吕雉、武则天、长孙皇后、冯太后、李清照、秦良玉、孝庄文皇后、冼夫人。</p>
      <div class="row" style="justify-content:center">
        <button class="btn" onclick="App.start()">开 始 测 评</button>
      </div>
      <div class="guide"><b>填写说明</b><br>
      提示：请按“真实的你”而非“理想的你”作答。本测评是自我省察与讨论工具，不是临床诊断或招聘评估；性别不参与计分，男性可匹配武则天，女性可匹配曹操。</div>
    </div>
  </section>

  <!-- 答题 -->
  <section id="screen-quiz" style="display:none">
    <div class="quiz-head">
      <div class="progress"><i id="bar"></i></div>
      <div class="pcount"><span id="pnow">1</span> / 48</div>
    </div>
    <div class="card">
      <div class="qtext" id="qtext"></div>
      <div class="opts" id="opts"></div>
      <div class="autohint">点选后自动进入下一题 · 可随时点「上一题」修改</div>
      <div class="warn" id="warn"></div>
      <div class="row">
        <button class="btn ghost" id="btnPrev" onclick="App.prev()">上一题</button>
        <button class="btn" id="btnNext" onclick="App.next()">下一题</button>
      </div>
    </div>
  </section>

  <!-- 结果 -->
  <section id="screen-result" style="display:none"></section>
</div>

<!-- 人物档案（全屏覆盖层，左滑右滑切换） -->
<div id="screen-archive">
  <div class="arc-head">
    <button class="btn ghost small" onclick="App.closeArchive()">‹ 返回</button>
    <div class="t">人物档案</div>
    <div class="cnt" id="arcCount"></div>
  </div>
  <div class="arc-stage" id="arcStage">
    <div class="arc-track" id="arcTrack"></div>
    <button class="arc-nav" id="arcPrev" onclick="App.archiveGo(-1)">‹</button>
    <button class="arc-nav" id="arcNext" onclick="App.archiveGo(1)">›</button>
  </div>
  <div class="arc-dots" id="arcDots"></div>
  <div class="arc-hint" id="arcHint">左滑看下一位 · 右滑看上一位</div>
</div>

<script type="application/json" id="data-questions">__QUESTIONS__</script>
<script type="application/json" id="data-figures">__FIGURES__</script>
<script>
const Q = JSON.parse(document.getElementById('data-questions').textContent);
const F = JSON.parse(document.getElementById('data-figures').textContent);
const DIMS = ['d1','d2','d3','d4','d5','d6'];
const answers = {};
let idx = 0;
let advanceTimer = null;

// 预计算每位人物的 Top3 近邻
const NEI = F.figures.map(f=>{
  const arr=F.figures.filter(g=>g.id!==f.id).map(g=>({id:g.id,name:g.name,
    dist:Math.sqrt(DIMS.reduce((s,d,i)=>s+Math.pow(f.scores[i]-g.scores[i],2),0))}));
  arr.sort((a,b)=>a.dist-b.dist);
  return arr.slice(0,3);
});
const figById = id=>F.figures.find(f=>f.id===id);

const App = {
  // ---------- 测评主流程 ----------
  start(){
    document.getElementById('screen-intro').style.display='none';
    document.getElementById('screen-result').style.display='none';
    document.getElementById('screen-quiz').style.display='flex';
    if(advanceTimer){clearTimeout(advanceTimer);advanceTimer=null;}
    idx = 0; this.renderQ(); window.scrollTo(0,0);
  },
  go(n){ idx = Math.max(0, Math.min(47, idx+n)); this.renderQ(); },
  renderQ(){
    if(advanceTimer){clearTimeout(advanceTimer);advanceTimer=null;}
    const q = Q.questions[idx];
    document.getElementById('qtext').textContent = (idx+1)+'. '+q.text;
    document.getElementById('pnow').textContent = idx+1;
    document.getElementById('bar').style.width = ((idx)/48*100)+'%';
    document.getElementById('warn').textContent='';
    const box = document.getElementById('opts'); box.innerHTML='';
    Q.scale_labels.forEach((lab,v)=>{
      const val=v+1;
      const div=document.createElement('div');
      div.className='opt'+(answers[q.id]===val?' sel':'');
      div.innerHTML='<span class="dot"></span><span>'+lab+'</span>';
      div.onclick=()=>{
        answers[q.id]=val;
        App.renderQ();
        const isLast = idx===47;
        advanceTimer = setTimeout(()=>{
          advanceTimer = null;
          isLast ? App.finish() : App.go(1);
        }, 320);
      };
      box.appendChild(div);
    });
    document.getElementById('btnPrev').style.visibility = idx===0?'hidden':'visible';
    document.getElementById('btnNext').textContent = idx===47?'查看结果':'下一题';
  },
  prev(){ this.go(-1); },
  next(){
    const q=Q.questions[idx];
    if(answers[q.id]===undefined){document.getElementById('warn').textContent='请选择一个选项后继续（没有对错，凭直觉即可）';return;}
    if(idx<47){idx++;this.renderQ();} else { this.finish(); }
  },
  scores(){
    const acc={}; DIMS.forEach(d=>acc[d]=[]);
    Q.questions.forEach(q=>{
      const v=answers[q.id];
      acc[q.dim].push(q.key==='+'?(v-1)/4*100:(5-v)/4*100);
    });
    return DIMS.map(d=>acc[d].reduce((a,b)=>a+b,0)/acc[d].length);
  },
  match(vec){
    const arr=F.figures.map(f=>({f,dist:Math.sqrt(DIMS.reduce((s,d,i)=>s+Math.pow(vec[i]-f.scores[i],2),0))}));
    arr.sort((a,b)=>a.dist-b.dist);
    return arr;
  },
  finish(){
    for(const q of Q.questions){ if(answers[q.id]===undefined){
      idx=Q.questions.indexOf(q);
      document.getElementById('screen-result').style.display='none';
      document.getElementById('screen-quiz').style.display='flex';
      this.renderQ(); return;} }
    document.getElementById('bar').style.width='100%';
    const vec=this.scores(), m=this.match(vec);
    document.getElementById('screen-quiz').style.display='none';
    document.getElementById('screen-result').style.display='';
    document.getElementById('screen-result').innerHTML = this.resultHTML(vec,m);
    window.scrollTo(0,0);
  },

  // ---------- 共享渲染 ----------
  radar(figVec, userVec){
    const cx=180,cy=175,R=120,n=6;
    const pt=(arr,i,r)=>{const a=-Math.PI/2+i*2*Math.PI/n;const v=arr[i]/100;
      return [cx+Math.cos(a)*r*v, cy+Math.sin(a)*r*v];};
    const poly=arr=>arr.map((_,i)=>pt(arr,i,R).join(',')).join(' ');
    let grid='';
    [0.25,0.5,0.75,1].forEach(k=>{
      const p=DIMS.map((_,i)=>{const a=-Math.PI/2+i*2*Math.PI/n;
        return [cx+Math.cos(a)*R*k,cy+Math.sin(a)*R*k].join(',')}).join(' ');
      grid+=`<polygon points="${p}" fill="none" stroke="#d8cdb6" stroke-width="1"/>`;
    });
    for(let i=0;i<n;i++){const a=-Math.PI/2+i*2*Math.PI/n;
      grid+=`<line x1="${cx}" y1="${cy}" x2="${cx+Math.cos(a)*R}" y2="${cy+Math.sin(a)*R}" stroke="#d8cdb6"/>`;}
    let labels='';
    DIMS.forEach((d,i)=>{const a=-Math.PI/2+i*2*Math.PI/n;
      labels+=`<text x="${cx+Math.cos(a)*(R+34)}" y="${cy+Math.sin(a)*(R+30)+4}" text-anchor="middle" font-size="13" fill="#6b6155">${Q.dimensions[d].name}</text>`;});
    const user = userVec? `<polygon points="${poly(userVec)}" fill="rgba(138,31,31,.20)" stroke="#8a1f1f" stroke-width="2.2"/>
      ${userVec.map((_,i)=>{const[x,y]=pt(userVec,i,R);return `<circle cx="${x}" cy="${y}" r="3.4" fill="#8a1f1f"/>`}).join('')}`:'';
    const legend = userVec
      ? '<span style="color:#8a1f1f">— 你的剖面</span> ｜ <span style="color:#a98a45">┄ 原型剖面</span>'
      : '<span style="color:#a98a45">┄ 原型剖面（六维分数）</span>';
    return `<svg viewBox="0 0 360 350" style="width:100%;max-width:420px;display:block;margin:auto">
      ${grid}${labels}
      <polygon points="${poly(figVec)}" fill="rgba(169,138,69,.18)" stroke="#a98a45" stroke-width="1.6" stroke-dasharray="5 3"/>
      ${user}
    </svg>
    <div style="text-align:center;font-size:12.5px;color:#6b6155">${legend}</div>`;
  },
  dimBars(vec){
    return DIMS.map((d,i)=>{
      const meta=Q.dimensions[d], v=Math.round(vec[i]);
      const pole = v>=50?meta.name:meta.opposite;
      return `<div class="dimbar">
        <div class="lab"><span><b>${meta.name}</b> ↔ ${meta.opposite}</span><span><b style="color:#8a1f1f">${v}</b> · 偏${pole}</span></div>
        <div class="track"><div class="mid"></div><div class="fill" style="left:${v>=50?'50%':v+'%'};width:${Math.abs(v-50)}%"></div></div>
      </div>`;
    }).join('');
  },
  bullets(arr){return '<ul class="clean">'+arr.map(x=>`<li>${x}</li>`).join('')+'</ul>';},
  neighPills(fi, clickable){
    return NEI[fi].map(g=>{
      const cls=clickable?'pill link':'pill';
      const onclick=clickable?` onclick="App.openArchiveAt(${g.id})"`:'';
      return `<span class="${cls}"${onclick}>${g.name} <b>${g.dist.toFixed(1)}</b></span>`;
    }).join('');
  },
  openArchiveAt(id){ this.openArchive(id); },
  // 单张人物卡（结果页与档案页共用）
  figureCard(f, opts){
    opts = opts||{};
    const fi = F.figures.indexOf(f);
    const radar = this.radar(f.scores, opts.userVec||null);
    const dims = this.dimBars(opts.userVec||f.scores);
    const distLine = opts.userDist!=null
      ? `<div style="font-size:12px;color:#6b6155;margin-top:6px">你与 ${f.name} 的原型距离：<b style="color:#8a1f1f">${opts.userDist.toFixed(1)}</b>（越小越像）</div>`
      : `<div style="font-size:12px;color:#6b6155;margin-top:6px">主要史料：${f.source}</div>`;
    const dual = opts.dual||'';
    return `
    <div class="card hero">
      <div class="era">${f.era} · ${f.role}</div>
      <h2>${f.name}</h2>
      <div class="tag">${f.tagline}</div>
      ${dual}
      <div class="verdict">${f.verdict}</div>
      <div class="grid2"><div>${radar}</div><div style="align-self:center">${dims}</div></div>
      ${distLine}
    </div>
    <div class="card">
      <h3 class="sec">他/她一般怎么处理事情</h3>
      ${this.bullets(f.style)}
      <h3 class="sec">史料锚点（凭什么这么说）</h3>
      <div class="histlist">${this.bullets(f.anchors)}</div>
      <div class="grid2">
        <div><h3 class="sec" style="border-color:#8a1f1f">盲区（和优点同源）</h3>${this.bullets(f.blind)}</div>
        <div><h3 class="sec" style="border-color:#3e5c48">行动建议</h3>${this.bullets(f.advice)}</div>
      </div>
      <h3 class="sec">与${f.name}相近的另外两位</h3>
      <div class="neigh arc-neigh">${this.neighPills(fi, !!opts.clickNeighbor)}</div>
      <div class="note">主要史料：${f.source}。本结果为自我省察工具，不是心理诊断；人物分数由可考事迹编码得出，方法与全部证据见随附设计文档（docs/ 目录）。</div>
    </div>`;
  },
  resultHTML(vec,m){
    const top=m[0], sec=m[1], third=m[2], f=top.f;
    const dual = (sec.dist-top.dist)<15
      ? `<div class="dual">你处在 <b>${f.name}</b> 与 <b>${sec.f.name}</b> 之间（距离差仅 ${(sec.dist-top.dist).toFixed(1)}）：两者都看一遍，你会更认得自己。</div>`
      : '';
    return this.figureCard(f,{userVec:vec,userDist:top.dist,dual,clickNeighbor:true}) + `
    <div class="footer-actions">
      <button class="btn ghost" onclick="location.reload()">重新测试</button>
    </div>`;
  },

  // ---------- 人物档案：左滑右滑 ----------
  archiveFrom: null,
  arcIdx: 0,
  arcBuilt: false,
  openArchive(focusId){
    this.archiveFrom = ['intro','quiz','result'].find(s=>
      document.getElementById('screen-'+s).style.display!=='none') || 'intro';
    document.getElementById('archiveEntry').style.display='none';
    this.buildArchive();
    this.archiveToId(focusId||F.figures[0].id, false);
    const el=document.getElementById('screen-archive');
    el.style.display='flex';
    document.getElementById('arcStage').scrollTop=0;
  },
  closeArchive(){
    document.getElementById('screen-archive').style.display='none';
    document.getElementById('archiveEntry').style.display='';
  },
  buildArchive(){
    if(this.arcBuilt) return;
    const track=document.getElementById('arcTrack');
    track.innerHTML = F.figures.map(f=>`<div class="arc-page" data-id="${f.id}">${this.figureCard(f,{clickNeighbor:true})}</div>`).join('');
    const dots=document.getElementById('arcDots');
    dots.innerHTML=F.figures.map((f,i)=>`<i data-i="${i}"></i>`).join('');
    dots.querySelectorAll('i').forEach(el=>el.onclick=()=>this.archiveGo(parseInt(el.dataset.i)-this.arcIdx));
    // 触摸滑动（同时兼容 Touch 与 Pointer）
    const stage=document.getElementById('arcStage');
    let sx=0,sy=0,dx=0,tracking=false,lockDir=null;
    const down=(x,y)=>{sx=x;sy=y;dx=0;tracking=true;lockDir=null;
      track.style.transition='none';};
    const move=(x,y)=>{if(!tracking)return;dx=x-sx;
      if(lockDir===null&&(Math.abs(dx)>8||Math.abs(y-sy)>8)){
        lockDir = Math.abs(dx)>Math.abs(y-sy)?'x':'y';
      }
      if(lockDir==='x'){stage.scrollTop=stage._sy||0;track.style.transform=`translateX(calc(${-this.arcIdx*100}% + ${dx}px))`;}
    };
    const up=()=>{if(!tracking)return;tracking=false;track.style.transition='';
      if(lockDir==='x'&&Math.abs(dx)>45){ this.archiveGo(dx<0?1:-1); }
      else { this.snap(); }
      dx=0;lockDir=null;};
    stage.addEventListener('touchstart',e=>{stage._sy=stage.scrollTop;down(e.touches[0].clientX,e.touches[0].clientY);},{passive:true});
    stage.addEventListener('touchmove',e=>move(e.touches[0].clientX,e.touches[0].clientY),{passive:true});
    stage.addEventListener('touchend',up);
    let pdown=false;
    stage.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'){pdown=true;stage._sy=stage.scrollTop;down(e.clientX,e.clientY);}});
    stage.addEventListener('pointermove',e=>{if(pdown)move(e.clientX,e.clientY);});
    stage.addEventListener('pointerup',()=>{if(pdown){pdown=false;up();}});
    stage.addEventListener('pointercancel',()=>{pdown=false;if(tracking){tracking=false;this.snap();}});
    // 键盘左右（桌面）
    document.addEventListener('keydown',e=>{
      if(document.getElementById('screen-archive').style.display!=='flex')return;
      if(e.key==='ArrowLeft')this.archiveGo(-1);
      if(e.key==='ArrowRight')this.archiveGo(1);
      if(e.key==='Escape')this.closeArchive();
    });
    this.arcBuilt=true;
  },
  snap(){
    document.getElementById('arcTrack').style.transform=`translateX(${-this.arcIdx*100}%)`;
  },
  archiveToId(id, animate){
    const i=F.figures.findIndex(f=>f.id===id);
    if(i<0)return;
    this.arcIdx=i;
    const track=document.getElementById('arcTrack');
    if(animate===false)track.style.transition='none';
    track.style.transform=`translateX(${-i*100}%)`;
    if(animate===false)requestAnimationFrame(()=>requestAnimationFrame(()=>track.style.transition=''));
    document.getElementById('arcCount').textContent=(i+1)+' / '+F.figures.length;
    document.getElementById('arcPrev').disabled = i===0;
    document.getElementById('arcNext').disabled = i===F.figures.length-1;
    document.querySelectorAll('#arcDots i').forEach((el,k)=>el.classList.toggle('on',k===i));
    document.getElementById('arcStage').scrollTop=0;
  },
  archiveGo(step){
    const next=Math.max(0,Math.min(F.figures.length-1,this.arcIdx+step));
    this.archiveToId(F.figures[next].id, true);
  }
};
</script>
</body>
</html>
'''
html = HTML.replace("__QUESTIONS__", Q).replace("__FIGURES__", F)
open(f"{BASE}/index.html", "w", encoding="utf-8").write(html)
print("index.html 生成:", len(html), "bytes ->", BASE)
