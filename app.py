import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Spin & Solve", page_icon="🎡", layout="centered")

bank = {
    "easy": [
        "Which process makes food in green plants?",
        "Plants absorb water mainly through?",
        "Which instrument measures temperature?",
        "Which acid is present in lemon?",
        "Basic unit of life is?",
    ],
    "medium": [
        "Origin in coordinate geometry?",
        "Velocity changes when?",
        "Pressure = ?",
        "Convex mirror is used in?",
        "Electric current is measured in?",
    ],
    "hard": [
        "If radius doubles, area becomes?",
        "Acceleration is change in?",
        "Mass is neither created nor destroyed, which law states this?",
        "Heron's formula gives?",
        "Nitrogen in atmosphere is about ______ % ?",
    ],
}

st.title("Spin & Solve")
st.caption("Click the blue SPIN button in the middle of the wheel.")

wheel_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body{{ margin:0; font-family:'Segoe UI',sans-serif; background:transparent; }}
  .wrap{{ display:flex; flex-direction:column; align-items:center; padding-top:10px; }}
  .wheel-wrap{{ position:relative; width:420px; height:420px; max-width:90vw; max-height:90vw; margin-bottom:1.2rem;}}
  .pointer{{
    position:absolute; top:-16px; left:50%; transform:translateX(-50%); z-index:5;
    width:0; height:0; border-left:18px solid transparent; border-right:18px solid transparent;
    border-top:30px solid #0d0d0d; filter:drop-shadow(0 2px 3px rgba(0,0,0,.5));
  }}
  svg#wheel{{
    width:100%; height:100%; display:block; border-radius:50%;
    box-shadow:0 0 0 8px #262b38, 0 14px 40px rgba(0,0,0,.5);
    transition: transform 4.2s cubic-bezier(.17,.67,.16,1);
  }}
  .seg-label{{ font-weight:800; font-size:18px; fill:#0d0f15; letter-spacing:.5px; }}
  .hub{{
    position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:104px; height:104px;
    border-radius:50%; background:radial-gradient(circle at 35% 30%,#4a86f5,#2d6cdf 75%);
    border:4px solid #1c3f8f; color:#fff; font-weight:800; font-size:1.1rem; letter-spacing:1px;
    display:flex; align-items:center; justify-content:center; z-index:6; cursor:pointer;
    box-shadow:0 4px 16px rgba(0,0,0,.5); transition:transform .15s ease; user-select:none;
  }}
  .hub:active{{ transform:translate(-50%,-50%) scale(.94); }}
  .hub.disabled{{ opacity:.6; cursor:default; pointer-events:none; }}
  .result{{
    width:420px; max-width:90vw; background:#1b1f2a; border-radius:16px; padding:1.2rem 1.5rem;
    border:1px solid #2a2f3d; min-height:100px; color:#eef0f4;
    display:flex; flex-direction:column; justify-content:center; gap:.5rem;
    opacity:0; transition:opacity .4s ease;
  }}
  .result.show{{ opacity:1; }}
  .badge{{ align-self:flex-start; padding:.25rem .7rem; border-radius:999px; font-size:.78rem; font-weight:700; color:#0d0f15; }}
  .badge.easy{{background:#2ecc71;}} .badge.medium{{background:#f1c40f;}} .badge.hard{{background:#e74c3c;}}
  .question{{ font-size:1.1rem; line-height:1.5; }}
  .placeholder{{ color:#9aa3b5; font-size:.95rem; }}
  .score{{ margin-top:.8rem; color:#9aa3b5; font-size:.9rem; }}
  .score span{{ color:#eef0f4; font-weight:700; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="wheel-wrap">
    <div class="pointer"></div>
    <svg id="wheel" viewBox="0 0 300 300">
      <path d="M150,150 L150,10 A140,140 0 0,1 271.24,220 Z" fill="#2ecc71"></path>
      <path d="M150,150 L271.24,220 A140,140 0 0,1 28.76,220 Z" fill="#f1c40f"></path>
      <path d="M150,150 L28.76,220 A140,140 0 0,1 150,10 Z" fill="#e74c3c"></path>
      <text x="223.6" y="107.5" text-anchor="middle" class="seg-label">EASY</text>
      <text x="150" y="240" text-anchor="middle" class="seg-label">MEDIUM</text>
      <text x="76.4" y="107.5" text-anchor="middle" class="seg-label">HARD</text>
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

  let currentRotation = 0;
  let spinning = false;
  let asked = 0;

  hub.addEventListener('click', () => {{
    if (spinning) return;
    spinning = true;
    hub.classList.add('disabled');
    hub.textContent = '...';
    result.classList.remove('show');

    const names = Object.keys(bank);
    const category = names[Math.floor(Math.random() * names.length)];
    const question = bank[category][Math.floor(Math.random() * bank[category].length)];

    const center = centers[category];
    const targetMod = (360 - center + 360) % 360;
    const extraSpins = 5 + Math.floor(Math.random() * 3);
    const jitter = (Math.random() * 20) - 10;
    currentRotation = currentRotation - (currentRotation % 360) + extraSpins * 360 + targetMod + jitter;
    wheel.style.transform = `rotate(${{currentRotation}}deg)`;

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

components.html(wheel_html, height=700, scrolling=False)
