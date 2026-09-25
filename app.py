
import streamlit as st
import streamlit.components.v1 as components
import random

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
        "Nitrogen in atmosphere is about?",
    ],
}

if "category" not in st.session_state:
    st.session_state.category = None
    st.session_state.question = None
    st.session_state.count = 0
    st.session_state.spin_id = 0

st.title("Spin & Solve")
st.caption("Spin the wheel, land on a difficulty, answer the question.")

# --- Python decides the outcome ---
if st.button("🎡  SPIN THE WHEEL", use_container_width=True, type="primary"):
    category = random.choice(list(bank.keys()))
    question = random.choice(bank[category])
    st.session_state.category = category
    st.session_state.question = question
    st.session_state.count += 1
    st.session_state.spin_id += 1

target = st.session_state.category or "easy"
should_spin = str(st.session_state.spin_id > 0).lower()

# --- HTML/JS just plays the visual spin to land on `target` ---
wheel_html = f"""
<!-- spin_id: {st.session_state.spin_id} forces a fresh reload each click -->
<div style="display:flex; flex-direction:column; align-items:center; font-family:'Segoe UI',sans-serif;">
  <div style="position:relative; width:420px; height:420px; max-width:90vw; max-height:90vw;">
    <div style="position:absolute; top:-16px; left:50%; transform:translateX(-50%); z-index:5;
                width:0; height:0; border-left:18px solid transparent; border-right:18px solid transparent;
                border-top:30px solid #0d0d0d; filter:drop-shadow(0 2px 3px rgba(0,0,0,.5));"></div>
    <svg id="wheel" viewBox="0 0 300 300" style="width:100%; height:100%; display:block; border-radius:50%;
         box-shadow:0 0 0 8px #262b38, 0 14px 40px rgba(0,0,0,.5);">
      <path d="M150,150 L150,10 A140,140 0 0,1 271.24,220 Z" fill="#2ecc71"></path>
      <path d="M150,150 L271.24,220 A140,140 0 0,1 28.76,220 Z" fill="#f1c40f"></path>
      <path d="M150,150 L28.76,220 A140,140 0 0,1 150,10 Z" fill="#e74c3c"></path>
      <text x="223.6" y="107.5" text-anchor="middle" style="font-weight:800; font-size:18px; fill:#0d0f15;">EASY</text>
      <text x="150" y="240" text-anchor="middle" style="font-weight:800; font-size:18px; fill:#0d0f15;">MEDIUM</text>
      <text x="76.4" y="107.5" text-anchor="middle" style="font-weight:800; font-size:18px; fill:#0d0f15;">HARD</text>
    </svg>
    <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:104px; height:104px;
                border-radius:50%; background:radial-gradient(circle at 35% 30%,#4a86f5,#2d6cdf 75%);
                border:4px solid #1c3f8f; color:#fff; font-weight:800; font-size:1.1rem; letter-spacing:1px;
                display:flex; align-items:center; justify-content:center; z-index:6;
                box-shadow:0 4px 16px rgba(0,0,0,.5);">SPIN</div>
  </div>
</div>

<script>
  const centers = {{ easy: 60, medium: 180, hard: 300 }};
  const target = "{target}";
  const shouldSpin = {should_spin};

  window.addEventListener('load', () => {{
    const wheel = document.getElementById('wheel');
    if (!shouldSpin) return;
    const center = centers[target];
    const targetMod = (360 - center + 360) % 360;
    const extraSpins = 5 + Math.floor(Math.random() * 3);
    const jitter = (Math.random() * 20) - 10;
    const rotation = extraSpins * 360 + targetMod + jitter;
    requestAnimationFrame(() => {{
      wheel.style.transition = 'transform 4.2s cubic-bezier(.17,.67,.16,1)';
      wheel.style.transform = `rotate(${rotation}deg)`;
    }});
  }});
</script>
"""

components.html(wheel_html, height=460)

# --- Result shown below (Python-driven, already decided before the animation plays) ---
if st.session_state.question:
    badge_color = {"easy": "#2ecc71", "medium": "#f1c40f", "hard": "#e74c3c"}[st.session_state.category]
    st.markdown(
        f"<span style='background:{badge_color}; color:#0d0f15; padding:3px 12px; "
        f"border-radius:999px; font-weight:700; font-size:0.8rem;'>"
        f"{st.session_state.category.upper()}</span>",
        unsafe_allow_html=True,
    )
    st.subheader(st.session_state.question)
else:
    st.info("Press the button above to get your question.")

st.caption(f"Questions asked: {st.session_state.count}")
