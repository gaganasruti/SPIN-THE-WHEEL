import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Spin & Solve", page_icon="🎡", layout="centered")
bank = {
    "easy": [
       " Which process do green plants use to make their own food? " ,

" Through which plant part does absorption of water mainly take place? ",

"  Which scientific instrument is used to measure temperature? ",

"  Which acid is naturally found in lemons? ",

" What is known as the basic structural and functional unit of life?",
    ],
    "medium": [
      "  In coordinate geometry, what are the coordinates of the origin?" ,

" An object's velocity will change if there is a change in its speed, direction, or both ? Which defines that change? ",

"  Which of the following formulas correctly represents pressure? ",

"  Which is a common practical application of a convex mirror?",

"  What is the standard SI unit used to measure electric current?" ,
    ],
    "hard": [
       "  If the radius of a circle is doubled, how does its total area change? ",

"  Acceleration is defined as the rate of change of which quantity? ",

"  The law stating that mass can neither be created nor destroyed in a chemical reaction is known as: ",

"  What is Heron's formula primarily used to calculate? ",

"  Approximately what percentage of Earth's atmosphere consists of nitrogen gas? ",
    ],
}

# --- Page-level background ---

st.markdown(
    """
    <style>
    .stApp {
       background: linear-gradient(135deg, #ffe3ec 0%, #fff6db 35%, #dcf5ea 65%, #e3ecff 100%);
    }
    h1, .stCaption, p { color: #3a3550 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("🎡 Spin & Solve")
st.caption("Click the blue SPIN hub in the middle of the wheel.")
 
wheel_html = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<style>
  *{{ box-sizing:border-box; }}
  body{{ margin:0; font-family:'Poppins',sans-serif; background:transparent; }}
  .wrap{{ display:flex; flex-direction:column; align-items:center; padding-top:14px; }}
 
  .wheel-wrap{{
    position:relative; width:420px; height:420px; max-width:90vw; max-height:90vw; margin-bottom:1.4rem;
  }}
  .glow{{
    position:absolute; inset:-40px; border-radius:50%;
    background:radial-gradient(circle, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0) 70%);
    z-index:0;
  }}
  .pointer{{
    position:absolute; top:-16px; left:50%; transform:translateX(-50%); z-index:5;
    width:0; height:0; border-left:18px solid transparent; border-right:18px solid transparent;
    border-top:30px solid #2d6cdf; filter:drop-shadow(0 2px 3px rgba(0,0,0,.2));
  }}
  svg#wheel{{
    position:relative; z-index:2; width:100%; height:100%; display:block; border-radius:50%;
    box-shadow:0 0 0 8px #ffffff, 0 14px 40px rgba(90,80,120,.25);
    transition: transform 4.2s cubic-bezier(.17,.67,.16,1);
  }}
  .seg-label{{ font-weight:800; font-size:18px; fill:#2d2a3a; letter-spacing:.5px; }}
  .label-g{{
    transform-box: fill-box;
    transform-origin: 50% 50%;
    transition: transform 4.2s cubic-bezier(.17,.67,.16,1);
  }}
  .hub{{
    position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:106px; height:106px;
    border-radius:50%; background:radial-gradient(circle at 35% 30%,#6fa2ff,#2d6cdf 75%);
    border:4px solid #ffffff; color:#fff; font-weight:800; font-size:1.1rem; letter-spacing:1px;
    display:flex; align-items:center; justify-content:center; z-index:6; cursor:pointer;
    box-shadow:0 6px 16px rgba(45,108,223,.4); transition:transform .15s ease; user-select:none;
  }}
  .hub:hover{{ filter:brightness(1.06); }}
  .hub:active{{ transform:translate(-50%,-50%) scale(.94); }}
  .hub.disabled{{ opacity:.65; cursor:default; pointer-events:none; }}
 
  .result{{
    width:420px; max-width:90vw; background:#ffffff;
    border-radius:18px; padding:1.3rem 1.6rem; border:1px solid #f0e4ee;
    min-height:100px; color:#2d2a3a; box-shadow:0 10px 28px rgba(90,80,120,.15);
    display:flex; flex-direction:column; justify-content:center; gap:.55rem;
    opacity:0; transition:opacity .4s ease;
  }}
  .result.show{{ opacity:1; }}
  .badge{{ align-self:flex-start; padding:.28rem .8rem; border-radius:999px; font-size:.78rem; font-weight:700; color:#2d2a3a; }}
  .badge.easy{{background:#2ecc71;}} .badge.medium{{background:#f1c40f;}} .badge.hard{{background:#e74c3c;}}
  .question{{ font-size:1.12rem; line-height:1.55; color:#2d2a3a; }}
  .placeholder{{ color:#8b8599; font-size:.95rem; }}
  .score{{ margin-top:.9rem; color:#8b8599; font-size:.9rem; }}
  .score span{{ color:#3a3550; font-weight:700; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="wheel-wrap">
    <div class="glow"></div>
    <div class="pointer"></div>
    <svg id="wheel" viewBox="0 0 300 300">
      <path d="M150,150 L150,10 A140,140 0 0,1 271.24,220 Z" fill="#2ecc71"></path>
      <path d="M150,150 L271.24,220 A140,140 0 0,1 28.76,220 Z" fill="#f1c40f"></path>
      <path d="M150,150 L28.76,220 A140,140 0 0,1 150,10 Z" fill="#e74c3c"></path>
      <g class="label-g"><text x="223.6" y="107.5" text-anchor="middle" class="seg-label">EASY</text></g>
      <g class="label-g"><text x="150" y="240" text-anchor="middle" class="seg-label">MEDIUM</text></g>
      <g class="label-g"><text x="76.4" y="107.5" text-anchor="middle" class="seg-label">HARD</text></g>
    </svg>
    <div class="hub" id="hub">SPIN</div>
  </div>
  <div class="result" id="result">
    <p class="placeholder" id="placeholder">Click SPIN to get your question.</p>
  </div>
  <div class="score">Questions asked: <span id="count">0</span></div>
</div>
 
<script>
  const bank = {json.dumps(bank)};
  const centers = {{ easy: 60, medium: 180, hard: 300 }};
  const wheel = document.getElementById('wheel');
  const hub = document.getElementById('hub');
  const result = document.getElementById('result');
  const countEl = document.getElementById('count');
  const labelGroups = document.querySelectorAll('.label-g');
 
  let currentRotation = 0;
  let spinning = false;
  let asked = 0;
 
  // per-category "shuffle bag": each question is asked once before any repeat
  const pools = {{}};
  Object.keys(bank).forEach(cat => {{ pools[cat] = []; }});
 
  function shuffledCopy(arr) {{
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {{
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }}
    return a;
  }}
 
  function nextQuestion(category) {{
    if (pools[category].length === 0) {{
      pools[category] = shuffledCopy(bank[category]);
    }}
    return pools[category].pop();
  }}
 
  hub.addEventListener('click', () => {{
    if (spinning) return;
    spinning = true;
    hub.classList.add('disabled');
    hub.textContent = '...';
    result.classList.remove('show');
 
    const names = Object.keys(bank);
    const category = names[Math.floor(Math.random() * names.length)];
    const question = nextQuestion(category);
 
    const center = centers[category];
    const targetMod = (360 - center + 360) % 360;
    const extraSpins = 5 + Math.floor(Math.random() * 3);
    const jitter = (Math.random() * 20) - 10;
    currentRotation = currentRotation - (currentRotation % 360) + extraSpins * 360 + targetMod + jitter;
 
    wheel.style.transform = `rotate(${{currentRotation}}deg)`;
    // counter-rotate every label around its own center so it stays upright
    labelGroups.forEach(g => {{
      g.style.transform = `rotate(${{-currentRotation}}deg)`;
    }});
 
    setTimeout(() => {{
      asked++;
      countEl.textContent = asked;
      result.innerHTML = `
        <span class="badge ${{category}}">${{category.toUpperCase()}}</span>
        <div class="question">${{question}}</div>
      `;
      result.classList.add('show');
      spinning = false;
      hub.classList.remove('disabled');
      hub.textContent = 'SPIN';
    }}, 4300);
  }});
</script>
</body>
</html>
"""
 
components.html(wheel_html, height=740, scrolling=False)
