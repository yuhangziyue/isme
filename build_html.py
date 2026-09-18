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
<meta name="theme-color" content="#f7f0e4">
<title>我是谁转世 · 历史名人人格原型测评</title>
<style>
:root{
  --paper:#f7f0e4; --paper-warm:#fffaf2; --paper-deep:#ede2d0;
  --card:#fffdf8; --ink:#2b2620; --muted:#74695d; --faint:#9b8e7c;
  --red:#8a1f1f; --red-2:#b64a3c; --red-bg:#f9ebe6;
  --gold:#a98a45; --gold-bg:#f7eddb; --blue:#7188ad; --blue-bg:#eef2f8;
  --line:#ddd2bd; --green:#3e5c48; --shadow:0 10px 30px rgba(72,50,20,.07);
}
*{box-sizing:border-box;margin:0;padding:0;scrollbar-width:none;-ms-overflow-style:none}
*::-webkit-scrollbar{width:0;height:0;display:none;background:transparent}
html,body{height:100dvh;overflow:hidden}
body{
  background:linear-gradient(180deg,#fffaf2 0%,var(--paper) 42%,#f1e6d6 100%);
  color:var(--ink);
  font-family:"Songti SC","Noto Serif SC","STSong","SimSun",serif;
  line-height:1.7;-webkit-font-smoothing:antialiased;
  overscroll-behavior-y:none;
}
button{font-family:inherit}
.wrap{height:100dvh;max-width:760px;margin:0 auto;padding:64px 20px 34px;overflow:hidden;position:relative;display:flex;flex-direction:column}
.screen{animation:fadeScreen .28s ease both;flex:1 1 auto;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch}
#screen-quiz{overflow:hidden}
@keyframes fadeScreen{from{opacity:0}to{opacity:1}}

.card{background:var(--card);border:1px solid rgba(169,138,69,.22);border-radius:18px;
  padding:22px 24px;margin-top:16px;box-shadow:var(--shadow)}
.seal{display:inline-block;border:1.5px solid var(--red);color:var(--red);
  font-size:12px;letter-spacing:3px;padding:4px 10px;border-radius:6px;transform:rotate(-1.5deg);font-weight:700}
h1{font-size:38px;line-height:1.2;margin:18px 0 8px;letter-spacing:7px}
.slogan{font-size:19px;color:var(--red);letter-spacing:2px;font-weight:700;margin-top:12px}
.slogan::before{content:"「";color:var(--gold)}
.slogan::after{content:"」";color:var(--gold)}
.sub{color:var(--muted);font-size:15px;letter-spacing:1px}
.intro-hero{padding:12px 4px 0}
.intro-copy{font-size:14.5px;color:var(--muted);margin:16px 0 14px}
.intro-copy b{color:var(--ink)}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:4px 0 16px}
.stat{background:#fbf4e8;border:1px solid #eadfc9;border-radius:14px;padding:13px 8px;text-align:center}
.stat b{display:block;font-size:25px;line-height:1.15;color:var(--red);letter-spacing:0}
.stat span{display:block;font-size:12px;color:var(--muted);margin-top:4px;white-space:nowrap}
.guide-card{background:#fbf6ec;border:1px solid #eadfc9;border-radius:14px;padding:14px 16px}
.guide-card h3{font-size:15px;letter-spacing:2px;margin-bottom:7px;color:var(--ink)}
.guide-card ul{list-style:none}
.guide-card li{position:relative;padding:5px 0 5px 17px;font-size:13.5px;color:var(--muted)}
.guide-card li::before{content:"";position:absolute;left:2px;top:14px;width:6px;height:6px;border-radius:50%;background:var(--gold)}
.intro-actions{display:flex;gap:12px;margin-top:18px}
.intro-actions .btn{flex:1}
.saved-tip{text-align:center;min-height:22px;font-size:12.5px;color:var(--faint);margin-top:10px}
.text-link{border:none;background:transparent;color:var(--gold);font-size:12.5px;cursor:pointer;padding:4px 8px;text-decoration:underline}
.btn{appearance:none;border:none;cursor:pointer;min-height:46px;
  background:var(--red);color:#fdf6e9;font-size:16px;letter-spacing:3px;
  padding:12px 24px;border-radius:999px;transition:transform .16s,background .2s,box-shadow .2s;
  box-shadow:0 8px 20px rgba(138,31,31,.16)}
.btn:hover{background:var(--red-2)}
.btn:active{transform:scale(.97)}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line);box-shadow:none}
.btn.ghost:hover{border-color:var(--gold);color:var(--gold)}
.btn:disabled{opacity:.38;cursor:not-allowed;box-shadow:none}
.btn.small{min-height:34px;padding:7px 15px;font-size:13px;letter-spacing:1.5px}

/* 答题 */
#screen-quiz{display:none;flex:1 1 auto;min-height:0;flex-direction:column}
.quiz-content{flex:1;min-height:0;display:flex;flex-direction:column}
.quiz-head{flex:none;padding:4px 2px 8px}
.progress{height:8px;background:#e8ddcb;border-radius:999px;overflow:hidden}
.progress i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--red),var(--gold));border-radius:999px;transition:width .25s ease}
.quiz-meta{display:flex;justify-content:space-between;align-items:center;color:var(--faint);font-size:12.5px;margin-top:7px}
.quiz-meta em{font-style:normal;color:var(--red);font-weight:700;font-size:14px}
.question-card{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;
  background:var(--card);border:1px solid rgba(169,138,69,.22);border-radius:20px;
  padding:22px 24px;box-shadow:var(--shadow)}
.qtext{flex:none;min-height:78px;display:flex;align-items:center;font-size:20px;line-height:1.65;font-weight:700;letter-spacing:.4px}
.opts{display:flex;flex-direction:column;gap:11px;width:100%}
.opt{display:flex;align-items:center;gap:12px;min-height:50px;border:1px solid var(--line);
  border-radius:15px;padding:12px 15px;cursor:pointer;transition:transform .15s,border-color .15s,background .15s;
  background:#fffefb;font-size:15.5px;color:var(--ink);-webkit-tap-highlight-color:transparent}
.opt:hover{border-color:var(--gold)}
.opt:active{transform:scale(.985)}
.opt.sel{border-color:var(--red);background:var(--red-bg);font-weight:700}
.opt .dot{width:18px;height:18px;border:2px solid #b9ac92;border-radius:50%;flex:none;position:relative;transition:.15s}
.opt.sel .dot{border-color:var(--red)}
.opt.sel .dot::after{content:"";position:absolute;inset:3px;border-radius:50%;background:var(--red)}
.warn{flex:none;min-height:22px;color:var(--red);font-size:13px;margin-top:9px}
.autohint{flex:none;text-align:center;color:var(--faint);font-size:12px;letter-spacing:1px;margin:9px 0 2px}
.quiz-bottombar{flex:none;background:rgba(255,253,248,.96);border:1px solid rgba(169,138,69,.2);
  border-radius:18px;padding:10px;box-shadow:0 -6px 22px rgba(72,50,20,.06);backdrop-filter:blur(8px)}
.bottom-inner{display:flex;gap:10px}
.bottom-inner .btn{flex:1}
.bottom-inner .prev{background:var(--red-bg);color:var(--red);border:1px solid rgba(138,31,31,.15);box-shadow:none}

/* 结果 */
.hero-card{text-align:center;padding:28px 24px}
.era{color:var(--faint);font-size:13.5px;letter-spacing:2px}
.hero-card h2{font-size:42px;line-height:1.2;letter-spacing:9px;margin:10px 0 6px}
.tagline{display:inline-block;color:var(--red);font-size:17px;font-weight:700;letter-spacing:3px}
.verdict-card{display:flex;gap:10px;align-items:flex-start;background:#fff8f4;border-left:4px solid var(--red);
  border-radius:0 14px 14px 0;padding:16px 18px;margin-top:12px;box-shadow:var(--shadow)}
.verdict-card .quote{font-size:30px;line-height:1;color:var(--gold);font-family:Georgia,serif}
.verdict-card p{font-size:15px;color:var(--ink);line-height:1.85;text-align:left}
.dual{margin-top:14px;padding:11px 13px;border:1px dashed var(--gold);border-radius:12px;
  background:var(--gold-bg);font-size:13.5px;color:var(--muted);text-align:left}
.dual b{color:var(--red)}
.section-title{font-size:17px;letter-spacing:3px;padding-left:12px;border-left:4px solid var(--gold);margin-bottom:16px}
.section-title.center{text-align:center;border-left:none;padding-left:0}
.radar-card svg{width:100%;max-width:430px;display:block;margin:0 auto}
.legend-row{display:flex;justify-content:center;gap:24px;flex-wrap:wrap;margin-top:4px;font-size:12.5px;color:var(--muted)}
.legend-item{display:flex;align-items:center;gap:7px}
.legend-dot{width:9px;height:9px;border-radius:50%}
.legend-dot.user{background:var(--red)}
.legend-dot.figure{background:var(--gold)}

.dim-row{margin-bottom:15px}
.dim-row:last-child{margin-bottom:0}
.dim-labels{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;font-size:13px;color:var(--faint);margin-bottom:6px}
.dim-labels .r{text-align:right}
.dim-labels .on{color:var(--ink);font-weight:700}
.dim-score{font-weight:700;color:var(--red);min-width:34px;text-align:center}
.dim-track{position:relative;height:10px;background:#ede4d4;border-radius:999px;overflow:hidden}
.dim-mid{position:absolute;left:50%;top:-3px;bottom:-3px;width:1px;background:#c9b996}
.dim-fill{position:absolute;top:0;bottom:0;border-radius:999px}
.dim-fill.high{background:linear-gradient(90deg,var(--red-2),var(--red))}
.dim-fill.low{background:linear-gradient(90deg,#93a6c5,var(--blue))}

.advice-grid{display:flex;flex-direction:column;gap:12px}
.advice-card{border-radius:15px;padding:16px 17px;border:1px solid transparent}
.advice-card.strength{background:linear-gradient(135deg,var(--red-bg),#fffaf7);border-color:rgba(138,31,31,.16)}
.advice-card.weakness{background:linear-gradient(135deg,var(--blue-bg),#fbfcff);border-color:rgba(113,136,173,.2)}
.advice-card.neutral{background:linear-gradient(135deg,var(--gold-bg),#fffdf8);border-color:rgba(169,138,69,.2)}
.advice-tag{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:1px;border-radius:999px;padding:4px 11px;margin-bottom:9px}
.strength .advice-tag{color:var(--red);background:rgba(138,31,31,.1)}
.weakness .advice-tag{color:var(--blue);background:rgba(113,136,173,.14)}
.neutral .advice-tag{color:var(--gold);background:rgba(169,138,69,.14)}
.advice-card h4{font-size:15.5px;margin-bottom:5px}
.advice-card p{font-size:13.5px;color:var(--muted);line-height:1.75}

.info-section{margin-bottom:18px}
.info-section:last-child{margin-bottom:0}
.info-section h4{font-size:15px;letter-spacing:2px;color:var(--ink);margin-bottom:9px}
.info-list{display:flex;flex-direction:column;gap:8px}
.info-list p{background:#fbf6ec;border:1px solid #eee3d0;border-radius:12px;padding:10px 12px;
  font-size:13.8px;line-height:1.72;color:var(--ink)}
.info-list.anchor p{color:var(--muted);font-size:13px;background:#f8f2e8}
.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.detail-grid .info-section{margin:0}
.neigh-list{display:flex;flex-wrap:wrap;gap:10px}
.pill{display:inline-flex;align-items:center;gap:6px;border:1px solid #eadfc9;background:#fffaf2;
  color:var(--red);border-radius:999px;padding:7px 13px;font-size:13px;cursor:pointer}
.pill b{color:var(--gold);font-size:11.5px}
.result-actions{display:flex;flex-direction:column;gap:10px}
.result-actions .btn{width:100%}
.disclaimer{font-size:12px;color:var(--faint);line-height:1.7;margin:12px 2px 0;text-align:center}

#archiveEntry{position:fixed;top:max(12px,env(safe-area-inset-top));right:12px;z-index:60;
  background:rgba(255,253,248,.94);border:1px solid var(--gold);color:var(--red);
  font-size:13px;letter-spacing:2px;font-weight:700;padding:8px 13px;border-radius:999px;
  cursor:pointer;box-shadow:0 2px 10px rgba(80,60,20,.12);-webkit-tap-highlight-color:transparent}
#archiveEntry:active{transform:scale(.96)}
#screen-archive{position:fixed;inset:0;z-index:100;background:linear-gradient(180deg,#fffaf2,#f1e6d6);
  display:none;flex-direction:column}
.arc-head{flex:none;border-bottom:1px solid var(--line);padding:max(10px,env(safe-area-inset-top)) 14px 10px;
  display:flex;align-items:center;gap:10px;background:rgba(247,240,228,.96);z-index:3}
.arc-head .t{flex:1;text-align:center;font-weight:700;letter-spacing:3px;font-size:16px}
.arc-head .cnt{color:var(--muted);font-size:13px;min-width:54px;text-align:right}
.arc-stage{flex:1;min-height:0;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;touch-action:pan-y}
.arc-track{display:flex;transition:transform .28s ease;will-change:transform}
.arc-page{flex:0 0 100%;max-width:100%;padding:14px 14px 34px}
.arc-nav{position:fixed;top:50%;z-index:6;width:40px;height:40px;border-radius:50%;
  border:1px solid var(--line);background:rgba(255,253,248,.92);color:var(--red);
  font-size:20px;cursor:pointer;display:flex;align-items:center;justify-content:center;
  transform:translateY(-50%);box-shadow:0 2px 8px rgba(80,60,20,.12)}
.arc-nav:disabled{opacity:.35;cursor:not-allowed}
#arcPrev{left:8px}#arcNext{right:8px}
.arc-dots{flex:none;background:rgba(247,240,228,.96);text-align:center;padding:9px 0 max(10px,env(safe-area-inset-bottom));border-top:1px solid var(--line)}
.arc-dots i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#cdbf9f;margin:0 3px;cursor:pointer}
.arc-dots i.on{background:var(--red);transform:scale(1.25)}
.arc-hint{flex:none;text-align:center;font-size:12px;color:var(--faint);padding:0 0 7px;letter-spacing:1px;background:rgba(247,240,228,.96)}
.toast{position:fixed;left:50%;bottom:calc(28px + env(safe-area-inset-bottom));transform:translateX(-50%) translateY(10px);
  background:rgba(43,38,32,.92);color:#fff;font-size:13px;padding:10px 16px;border-radius:999px;
  opacity:0;pointer-events:none;transition:.2s;z-index:200;white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

@media(max-width:720px){
  .wrap{padding:max(54px,calc(env(safe-area-inset-top) + 46px)) 12px calc(10px + env(safe-area-inset-bottom))}
  .card{padding:16px;border-radius:16px;margin-top:12px}
  h1{font-size:clamp(27px,8vw,34px);letter-spacing:5px;margin:14px 0 6px}
  .sub{font-size:12.5px;line-height:1.6}
  .slogan{font-size:clamp(15px,4.5vw,17px)}
  .intro-hero{padding-top:8px}
  .stats-grid{gap:6px;margin-bottom:13px}
  .stat{padding:10px 4px;border-radius:12px}
  .stat b{font-size:clamp(19px,6vw,24px)}
  .stat span{font-size:10.8px}
  .intro-copy{font-size:13px;line-height:1.7;margin:12px 0}
  .guide-card{padding:12px}
  .guide-card li{font-size:12.5px;padding:4px 0 4px 15px}
  .intro-actions{gap:9px;margin-top:14px}
  .btn{min-height:44px;font-size:15px;letter-spacing:2px;padding:10px 16px}

  #screen-quiz{flex:1 1 auto;min-height:0}
  .question-card{padding:16px 14px;border-radius:17px}
  .qtext{min-height:68px;font-size:clamp(16px,4.35vw,18px);line-height:1.58}
  .opts{gap:8px}
  .opt{min-height:46px;padding:10px 12px;font-size:14.5px;border-radius:13px;gap:10px}
  .opt .dot{width:16px;height:16px}
  .autohint{margin:7px 0 1px;font-size:11px}
  .quiz-bottombar{border-radius:15px;padding:8px}
  .bottom-inner{gap:8px}
  .bottom-inner .btn{min-height:42px}

  .hero-card{padding:22px 16px}
  .hero-card h2{font-size:clamp(31px,9vw,38px);letter-spacing:6px}
  .tagline{font-size:15px}
  .verdict-card{padding:13px 14px}
  .verdict-card p{font-size:13.8px;line-height:1.75}
  .section-title{font-size:15.5px;margin-bottom:12px}
  .dim-labels{font-size:12px}
  .detail-grid{grid-template-columns:1fr;gap:0}
  .info-list p{font-size:13px;padding:9px 10px}
  .arc-page{padding:10px 10px 28px}
  .arc-nav{width:34px;height:34px;font-size:18px}
  #archiveEntry{top:max(10px,env(safe-area-inset-top));right:10px;font-size:12px;padding:7px 11px}
}
@media(max-width:720px) and (max-height:740px){
  .question-card{padding:12px}
  .qtext{min-height:50px;margin-bottom:8px}
  .opt{min-height:42px;padding:8px 11px}
  .autohint{display:none}
  .warn{min-height:18px;margin-top:6px}
}
@media(max-width:380px){
  .stats-grid{gap:5px}
  .stat span{font-size:10px}
  .intro-actions{flex-direction:column}
  .opt{font-size:13.8px}
}
</style>
</head>
<body>

<button id="archiveEntry" onclick="App.openArchive()">人物档案</button>

<div class="wrap">
  <section id="screen-intro" class="screen">
    <div class="intro-hero">
      <span class="seal">正史认证 · v1.2</span>
      <h1>我是谁转世</h1>
      <p class="sub">中国历史名人人格原型测评 · 16 位正史人物 · 男女各半</p>
      <div class="slogan">更好地了解自己，解锁天赋吧</div>
    </div>
    <div class="card">
      <div class="stats-grid">
        <div class="stat"><b>48</b><span>道单选题</span></div>
        <div class="stat"><b>6</b><span>个人格维度</span></div>
        <div class="stat"><b>16</b><span>位正史人物</span></div>
        <div class="stat"><b>10</b><span>分钟左右</span></div>
      </div>
      <p class="intro-copy">基于<b>大五人格模型（OCEAN）</b>本土化的六个维度，把你的行为倾向与 16 位<b>正史有传、事迹可考</b>的真实决策者做原型匹配。性别不参与计分，只看处事方式。</p>
      <div class="guide-card">
        <h3>填写说明</h3>
        <ul>
          <li>按“真实的你”作答，而不是“理想中的你”。</li>
          <li>每题没有对错，凭第一直觉选择即可。</li>
          <li>选择后自动进入下一题，也可以返回修改。</li>
          <li>进度会自动保存在本机浏览器，中途退出可继续。</li>
        </ul>
      </div>
      <div class="intro-actions">
        <button class="btn" id="startBtn" onclick="App.start(false)">开始测评</button>
        <button class="btn ghost" onclick="App.openArchive()">浏览人物原型</button>
      </div>
      <div class="saved-tip" id="savedTip"></div>
    </div>
  </section>

  <section id="screen-quiz" class="screen">
    <div class="quiz-content">
      <div class="quiz-head">
        <div class="progress"><i id="bar"></i></div>
        <div class="quiz-meta"><span id="saveState">进度自动保存</span><span><em id="pnow">1</em> / 48</span></div>
      </div>
      <div class="question-card">
        <div class="qtext" id="qtext"></div>
        <div class="opts" id="opts"></div>
        <div class="warn" id="warn"></div>
      </div>
      <div class="autohint">点选后自动进入下一题 · 可随时返回修改</div>
    </div>
    <div class="quiz-bottombar">
      <div class="bottom-inner">
        <button class="btn prev" id="btnPrev" onclick="App.prev()">上一题</button>
        <button class="btn" id="btnNext" onclick="App.next()">下一题</button>
      </div>
    </div>
  </section>

  <section id="screen-result" class="screen" style="display:none"></section>
</div>

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
  <div class="arc-hint">左滑看下一位 · 右滑看上一位</div>
</div>
<div class="toast" id="toast"></div>

<script type="application/json" id="data-questions">__QUESTIONS__</script>
<script type="application/json" id="data-figures">__FIGURES__</script>
<script>
const Q = JSON.parse(document.getElementById('data-questions').textContent);
const F = JSON.parse(document.getElementById('data-figures').textContent);
const DIMS = ['d1','d2','d3','d4','d5','d6'];
const STORAGE_KEY = 'isme_answers_v1';
const N = Q.questions.length;

function loadAnswers(){
  try{
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    const clean = {};
    Q.questions.forEach(q=>{
      const v = saved[q.id];
      if([1,2,3,4,5].includes(v)) clean[q.id] = v;
    });
    return clean;
  }catch(e){ return {}; }
}
const answers = loadAnswers();
let idx = 0;
let advanceTimer = null;
let isFinishing = false;
let topResult = null;

const NEI = F.figures.map(f=>{
  const arr = F.figures.filter(g=>g.id!==f.id).map(g=>({
    id:g.id, name:g.name,
    dist:Math.sqrt(DIMS.reduce((s,d,i)=>s+Math.pow(f.scores[i]-g.scores[i],2),0))
  }));
  arr.sort((a,b)=>a.dist-b.dist);
  return arr.slice(0,3);
});

const App = {
  answeredCount(){
    return Q.questions.filter(q=>answers[q.id]!==undefined).length;
  },
  saveAnswers(){
    try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(answers)); }catch(e){}
  },
  updateIntroCta(){
    const done = this.answeredCount();
    const btn = document.getElementById('startBtn');
    const tip = document.getElementById('savedTip');
    if(done === 0){
      btn.textContent = '开始测评';
      tip.textContent = '答题进度仅保存在本机浏览器';
    }else if(done < N){
      btn.textContent = `继续测评（${done}/${N}）`;
      tip.innerHTML = `已自动保存 ${done}/${N} · <button class="text-link" onclick="App.restart()">清空重答</button>`;
    }else{
      btn.textContent = '查看上次结果';
      tip.innerHTML = `48 题已完成 · <button class="text-link" onclick="App.restart()">重新测一次</button>`;
    }
  },
  start(reset){
    if(advanceTimer){clearTimeout(advanceTimer);advanceTimer=null;}
    if(reset){
      Object.keys(answers).forEach(k=>delete answers[k]);
      this.saveAnswers();
    }
    document.getElementById('screen-intro').style.display='none';
    document.getElementById('screen-result').style.display='none';
    document.getElementById('screen-quiz').style.display='flex';
    const done = this.answeredCount();
    if(done === N){
      this.finish();
      return;
    }
    idx = Q.questions.findIndex(q=>answers[q.id]===undefined);
    if(idx < 0) idx = 0;
    this.renderQ();
    document.querySelector('.wrap').scrollTo(0,0);
  },
  go(n){
    idx = Math.max(0, Math.min(N-1, idx+n));
    this.renderQ();
  },
  renderQ(){
    if(advanceTimer){clearTimeout(advanceTimer);advanceTimer=null;}
    const q = Q.questions[idx];
    const done = this.answeredCount();
    document.getElementById('qtext').textContent = `${idx+1}. ${q.text}`;
    document.getElementById('pnow').textContent = idx+1;
    document.getElementById('bar').style.width = `${(idx+1)/N*100}%`;
    document.getElementById('saveState').textContent = `已保存 ${done}/${N}`;
    document.getElementById('warn').textContent = '';

    const box = document.getElementById('opts');
    box.innerHTML = '';
    Q.scale_labels.forEach((lab,v)=>{
      const val = v+1;
      const div = document.createElement('div');
      div.className = 'opt' + (answers[q.id]===val ? ' sel' : '');
      div.innerHTML = `<span class="dot"></span><span>${lab}</span>`;
      div.onclick = ()=>this.selectAnswer(val);
      box.appendChild(div);
    });

    document.getElementById('btnPrev').disabled = idx===0;
    const nextBtn = document.getElementById('btnNext');
    nextBtn.disabled = answers[q.id]===undefined;
    nextBtn.textContent = idx===N-1 ? '查看结果' : '下一题';
  },
  selectAnswer(val){
    if(isFinishing) return;
    const q = Q.questions[idx];
    answers[q.id] = val;
    this.saveAnswers();
    this.renderQ();
    const last = idx===N-1;
    advanceTimer = setTimeout(()=>{
      advanceTimer = null;
      if(last) this.finish();
      else this.go(1);
    }, last ? 240 : 180);
  },
  prev(){ this.go(-1); },
  next(){
    const q = Q.questions[idx];
    if(answers[q.id]===undefined){
      document.getElementById('warn').textContent = '请选择一个选项后继续（没有对错，凭直觉即可）';
      return;
    }
    if(idx < N-1) this.go(1);
    else this.finish();
  },
  scores(){
    const acc = {};
    DIMS.forEach(d=>acc[d]=[]);
    Q.questions.forEach(q=>{
      const v = answers[q.id];
      acc[q.dim].push(q.key==='+' ? (v-1)/4*100 : (5-v)/4*100);
    });
    return DIMS.map(d=>acc[d].reduce((a,b)=>a+b,0)/acc[d].length);
  },
  match(vec){
    const arr = F.figures.map(f=>({
      f,
      dist:Math.sqrt(DIMS.reduce((s,d,i)=>s+Math.pow(vec[i]-f.scores[i],2),0))
    }));
    arr.sort((a,b)=>a.dist-b.dist);
    return arr;
  },
  finish(){
    const missing = Q.questions.find(q=>answers[q.id]===undefined);
    if(missing){
      idx = Q.questions.indexOf(missing);
      document.getElementById('screen-result').style.display='none';
      document.getElementById('screen-quiz').style.display='flex';
      this.renderQ();
      document.getElementById('warn').textContent = '请继续完成剩余题目';
      return;
    }
    if(isFinishing) return;
    isFinishing = true;
    const vec = this.scores();
    const m = this.match(vec);
    topResult = {vec,m};
    document.getElementById('bar').style.width = '100%';
    document.getElementById('screen-quiz').style.display='none';
    const el = document.getElementById('screen-result');
    el.style.display='block';
    el.innerHTML = this.resultHTML(vec,m);
    document.querySelector('.wrap').scrollTo(0,0);
    requestAnimationFrame(()=>{isFinishing=false;});
  },
  restart(){
    if(advanceTimer){clearTimeout(advanceTimer);advanceTimer=null;}
    isFinishing = false;
    topResult = null;
    this.start(true);
  },

  radar(figVec, userVec){
    const cx=180, cy=172, R=118, n=6;
    const point=(arr,i,r)=>{
      const a=-Math.PI/2+i*2*Math.PI/n;
      return [cx+Math.cos(a)*r*(arr[i]/100), cy+Math.sin(a)*r*(arr[i]/100)];
    };
    const poly=arr=>arr.map((_,i)=>point(arr,i,R).join(',')).join(' ');
    let grid='';
    [.25,.5,.75,1].forEach(k=>{
      const p=DIMS.map((_,i)=>{
        const a=-Math.PI/2+i*2*Math.PI/n;
        return [cx+Math.cos(a)*R*k,cy+Math.sin(a)*R*k].join(',');
      }).join(' ');
      grid += `<polygon points="${p}" fill="none" stroke="#e1d5bf" stroke-width="1"/>`;
    });
    for(let i=0;i<n;i++){
      const a=-Math.PI/2+i*2*Math.PI/n;
      grid += `<line x1="${cx}" y1="${cy}" x2="${cx+Math.cos(a)*R}" y2="${cy+Math.sin(a)*R}" stroke="#e1d5bf"/>`;
    }
    const labels = DIMS.map((d,i)=>{
      const a=-Math.PI/2+i*2*Math.PI/n;
      return `<text x="${cx+Math.cos(a)*(R+36)}" y="${cy+Math.sin(a)*(R+31)+4}" text-anchor="middle" font-size="13" fill="#74695d">${Q.dimensions[d].name}</text>`;
    }).join('');
    const user = userVec ? `<polygon points="${poly(userVec)}" fill="rgba(138,31,31,.16)" stroke="#8a1f1f" stroke-width="2.2"/>
      ${userVec.map((_,i)=>{const [x,y]=point(userVec,i,R);return `<circle cx="${x}" cy="${y}" r="3.6" fill="#8a1f1f"/>`;}).join('')}` : '';
    const legend = userVec ? `
      <div class="legend-row">
        <span class="legend-item"><i class="legend-dot user"></i>你的画像</span>
        <span class="legend-item"><i class="legend-dot figure"></i>人物原型</span>
      </div>` : `
      <div class="legend-row"><span class="legend-item"><i class="legend-dot figure"></i>人物原型（六维分数）</span></div>`;
    return `<svg viewBox="0 0 360 350" role="img" aria-label="六维人格雷达图">
      ${grid}${labels}
      <polygon points="${poly(figVec)}" fill="rgba(169,138,69,.16)" stroke="#a98a45" stroke-width="1.8" stroke-dasharray="6 4"/>
      ${figVec.map((_,i)=>{const [x,y]=point(figVec,i,R);return `<circle cx="${x}" cy="${y}" r="3" fill="#a98a45"/>`;}).join('')}
      ${user}
    </svg>${legend}`;
  },
  dimBars(vec){
    return DIMS.map((d,i)=>{
      const meta = Q.dimensions[d];
      const v = Math.round(vec[i]);
      const high = v >= 50;
      const left = high ? '50%' : `${v}%`;
      const width = high ? `${v-50}%` : `${50-v}%`;
      return `<div class="dim-row">
        <div class="dim-labels">
          <span class="${high?'on':''}">${meta.name}</span>
          <span class="dim-score">${v}</span>
          <span class="r ${!high?'on':''}">${meta.opposite}</span>
        </div>
        <div class="dim-track"><i class="dim-mid"></i><i class="dim-fill ${high?'high':'low'}" style="left:${left};width:${width}"></i></div>
      </div>`;
    }).join('');
  },
  dimSegment(meta, high){
    const parts = meta.desc.split(/[；;]/).map(x=>x.trim()).filter(Boolean);
    const hit = parts.find(p=>p.startsWith(high ? '高分：' : '低分：'));
    return (hit || meta.desc).replace(/^[高低]分：/, '');
  },
  adviceHTML(vec){
    const items = DIMS.map((d,i)=>({d,i,value:vec[i]}));
    const si = items.reduce((a,b)=>b.value>a.value?b:a).i;
    const wi = items.reduce((a,b)=>b.value<a.value?b:a).i;
    const rest = items.filter(x=>x.i!==si && x.i!==wi);
    const ni = rest.reduce((a,b)=>Math.abs(b.value-50)<Math.abs(a.value-50)?b:a).i;
    const make = (kind,i)=>{
      const item = items[i], meta = Q.dimensions[DIMS[i]], v = Math.round(item.value);
      const high = v>=50;
      const dimName = `${meta.name} ↔ ${meta.opposite}`;
      let tag, title, text;
      if(kind==='strength'){
        tag = '优势 · 天赋 · 适合';
        title = `${meta.name}（${v}分）`;
        text = `你的天赋区最偏向「${meta.name}」。${this.dimSegment(meta,true)} 重要场景里把它放大成核心竞争力，比平均用力更容易形成辨识度。`;
      }else if(kind==='weakness'){
        tag = '短板 · 提醒 · 容易吃亏';
        title = `${meta.opposite}（${v}分）`;
        text = `你的提醒区靠近「${meta.opposite}」。${this.dimSegment(meta,false)} 高压决策时主动设置检查点，或找一位能力互补的人，会比临场硬扛更稳。`;
      }else{
        tag = '弹性 · 中庸 · 可进可退';
        title = `${dimName}（${v}分）`;
        const balanced = Math.abs(item.value-50) < 25;
        const lead = balanced
          ? `你最接近中值的是「${dimName}」。`
          : `你的六维倾向整体较鲜明，相对更能在两端间切换的是「${dimName}」。`;
        text = `${lead}${this.dimSegment(meta,high)} 你不完全怵任何一端，适合按场景切换；但要刻意沉淀自己的默认打法，避免每次都临场摇摆。`;
      }
      return `<div class="advice-card ${kind}"><span class="advice-tag">${tag}</span><h4>${title}</h4><p>${text}</p></div>`;
    };
    return make('strength',si)+make('weakness',wi)+make('neutral',ni);
  },
  infoSection(title, arr, anchor){
    return `<div class="info-section"><h4>${title}</h4><div class="info-list ${anchor?'anchor':''}">
      ${arr.map(x=>`<p>${x}</p>`).join('')}
    </div></div>`;
  },
  neighborPills(fi){
    return NEI[fi].map(g=>`<span class="pill" onclick="App.openArchiveAt(${g.id})">${g.name} <b>${g.dist.toFixed(1)}</b></span>`).join('');
  },
  openArchiveAt(id){ this.openArchive(id); },
  heroCard(f, dual){
    return `<div class="card hero-card">
      <div class="era">${f.era} · ${f.role}</div>
      <h2>${f.name}</h2>
      <div class="tagline">${f.tagline}</div>
      ${dual || ''}
    </div>`;
  },
  figureDetail(f){
    return `<div class="card">
      <h3 class="section-title">关于「${f.name}」</h3>
      ${this.infoSection('人物风格', f.style)}
      <div class="detail-grid">
        ${this.infoSection('盲点（和优点同源）', f.blind)}
        ${this.infoSection(`给${f.name}式人的建议`, f.advice)}
      </div>
      ${this.infoSection('史料锚点（凭什么这么说）', f.anchors, true)}
    </div>`;
  },
  resultHTML(vec,m){
    const top=m[0], sec=m[1], f=top.f;
    const dual = (sec.dist-top.dist)<15
      ? `<div class="dual">你处在 <b>${f.name}</b> 与 <b>${sec.f.name}</b> 之间（距离差仅 ${(sec.dist-top.dist).toFixed(1)}）：两个人物都看一遍，你会更认得自己。</div>`
      : '';
    return `
      ${this.heroCard(f, dual)}
      <div class="verdict-card"><span class="quote">“</span><p>${f.verdict}</p></div>
      <div class="card radar-card">
        <h3 class="section-title center">你与「${f.name}」的六维对比</h3>
        ${this.radar(f.scores, vec)}
        <div class="disclaimer">原型距离：<b>${top.dist.toFixed(1)}</b>（数值越小越像）</div>
      </div>
      <div class="card">
        <h3 class="section-title">你的六维画像</h3>
        ${this.dimBars(vec)}
      </div>
      <div class="card">
        <h3 class="section-title">给你的基本建议</h3>
        <div class="advice-grid">${this.adviceHTML(vec)}</div>
      </div>
      ${this.figureDetail(f)}
      <div class="card">
        <h3 class="section-title">相近人物</h3>
        <div class="neigh-list">${this.neighborPills(F.figures.indexOf(f))}</div>
      </div>
      <div class="card result-actions">
        <button class="btn" onclick="App.shareResult()">分享我的结果</button>
        <button class="btn ghost" onclick="App.restart()">再测一次</button>
      </div>
      <p class="disclaimer">主要史料：${f.source}。本结果为自我省察工具，不是心理诊断；人物分数由可考事迹编码得出。</p>`;
  },
  archiveFigureHTML(f){
    const fi = F.figures.indexOf(f);
    return `
      ${this.heroCard(f)}
      <div class="card radar-card">
        <h3 class="section-title center">${f.name}的六维原型</h3>
        ${this.radar(f.scores, null)}
      </div>
      <div class="card">
        <h3 class="section-title">人物原型画像</h3>
        ${this.dimBars(f.scores)}
      </div>
      ${this.figureDetail(f)}
      <div class="card">
        <h3 class="section-title">相近人物</h3>
        <div class="neigh-list">${this.neighborPills(fi)}</div>
      </div>
      <p class="disclaimer">主要史料：${f.source}</p>`;
  },
  showToast(msg){
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(()=>el.classList.remove('show'), 2200);
  },
  async shareResult(){
    const name = topResult ? topResult.m[0].f.name : '历史人物';
    const shareData = {
      title: '我是谁转世 · 历史名人人格原型测评',
      text: `我测出我是「${name}」转世，你呢？`,
      url: location.href
    };
    try{
      if(navigator.share){ await navigator.share(shareData); return; }
      throw new Error('unsupported');
    }catch(e){
      if(e && e.name === 'AbortError') return;
      const text = `${shareData.text}
${shareData.url}`;
      try{
        if(navigator.clipboard && window.isSecureContext){
          await navigator.clipboard.writeText(text);
        }else{
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position='fixed';ta.style.opacity='0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          ta.remove();
        }
        this.showToast('分享文案已复制，去粘贴给朋友吧');
      }catch(err){ this.showToast('复制失败，请手动复制链接'); }
    }
  },

  archiveFrom:'intro',
  arcIdx:0,
  arcBuilt:false,
  visibleScreen(){
    return ['intro','quiz','result'].find(s=>{
      const el = document.getElementById('screen-'+s);
      return el && el.style.display !== 'none';
    }) || 'intro';
  },
  openArchive(focusId){
    this.archiveFrom = this.visibleScreen();
    document.getElementById('archiveEntry').style.display='none';
    this.buildArchive();
    this.archiveToId(focusId || F.figures[0].id, false);
    document.getElementById('screen-archive').style.display='flex';
    document.getElementById('arcStage').scrollTop=0;
  },
  closeArchive(){
    document.getElementById('screen-archive').style.display='none';
    document.getElementById('archiveEntry').style.display='';
  },
  buildArchive(){
    if(this.arcBuilt) return;
    const track = document.getElementById('arcTrack');
    track.innerHTML = F.figures.map(f=>`<div class="arc-page" data-id="${f.id}">${this.archiveFigureHTML(f)}</div>`).join('');
    const dots = document.getElementById('arcDots');
    dots.innerHTML = F.figures.map((f,i)=>`<i data-i="${i}"></i>`).join('');
    dots.querySelectorAll('i').forEach(el=>{
      el.onclick=()=>this.archiveGo(parseInt(el.dataset.i,10)-this.arcIdx);
    });

    const stage=document.getElementById('arcStage');
    let sx=0,sy=0,dx=0,tracking=false,lockDir=null,pdown=false;
    const down=(x,y)=>{sx=x;sy=y;dx=0;tracking=true;lockDir=null;track.style.transition='none';};
    const move=(x,y)=>{
      if(!tracking)return;
      dx=x-sx;
      if(lockDir===null && (Math.abs(dx)>8 || Math.abs(y-sy)>8)){
        lockDir = Math.abs(dx)>Math.abs(y-sy) ? 'x' : 'y';
      }
      if(lockDir==='x'){
        stage.scrollTop = stage._sy || 0;
        track.style.transform=`translateX(calc(${-this.arcIdx*100}% + ${dx}px))`;
      }
    };
    const up=()=>{
      if(!tracking)return;
      tracking=false;
      track.style.transition='';
      if(lockDir==='x' && Math.abs(dx)>45) this.archiveGo(dx<0?1:-1);
      else this.snap();
      dx=0;lockDir=null;
    };
    stage.addEventListener('touchstart',e=>{stage._sy=stage.scrollTop;down(e.touches[0].clientX,e.touches[0].clientY);},{passive:true});
    stage.addEventListener('touchmove',e=>move(e.touches[0].clientX,e.touches[0].clientY),{passive:true});
    stage.addEventListener('touchend',up);
    stage.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'){pdown=true;stage._sy=stage.scrollTop;down(e.clientX,e.clientY);}});
    stage.addEventListener('pointermove',e=>{if(pdown)move(e.clientX,e.clientY);});
    stage.addEventListener('pointerup',()=>{if(pdown){pdown=false;up();}});
    stage.addEventListener('pointercancel',()=>{pdown=false;if(tracking){tracking=false;this.snap();}});
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
    document.getElementById('arcCount').textContent=`${i+1} / ${F.figures.length}`;
    document.getElementById('arcPrev').disabled = i===0;
    document.getElementById('arcNext').disabled = i===F.figures.length-1;
    document.querySelectorAll('#arcDots i').forEach((el,k)=>el.classList.toggle('on',k===i));
    document.getElementById('arcStage').scrollTop=0;
  },
  archiveGo(step){
    const next=Math.max(0,Math.min(F.figures.length-1,this.arcIdx+step));
    this.archiveToId(F.figures[next].id,true);
  }
};
App.updateIntroCta();
</script>
</body>
</html>
'''
html = HTML.replace("__QUESTIONS__", Q).replace("__FIGURES__", F)
open(f"{BASE}/index.html", "w", encoding="utf-8").write(html)
print("index.html 生成:", len(html), "bytes ->", BASE)
