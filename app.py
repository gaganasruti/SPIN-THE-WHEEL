import streamlit as st
import streamlit.components.v1 as components
import json
import base64
import os



# =========================================================
# STREAMLIT PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Spin the Wheel",
    page_icon="🎡",
    layout="wide"
)


# =========================================================
# QUESTION BANK
# =========================================================

bank = {
    "easy": [
        " Which process do green plants use to make their own food? ",
        " Through which plant part does absorption of water mainly take place? ",
        " Which scientific instrument is used to measure temperature? ",
        " Which acid is naturally found in lemons? ",
        " What is known as the basic structural and functional unit of life?",
    ],

    "medium": [
        " In coordinate geometry, what are the coordinates of the origin? ",
        " An object's velocity will change if there is a change in its speed, direction, or both ? Which defines that change? ",
        " Which of the following formulas correctly represents pressure? ",
        " Which is a common practical application of a convex mirror? ",
        " What is the standard SI unit used to measure electric current? ",
    ],

    "hard": [
        " If the radius of a circle is doubled, how does its total area change? ",
        " Acceleration is defined as the rate of change of which quantity? ",
        " The law stating that mass can neither be created nor destroyed in a chemical reaction is known as: ",
        " What is Heron's formula primarily used to calculate? ",
        " Approximately what percentage of Earth's atmosphere consists of nitrogen gas? ",
    ],
}


# =========================================================
# LOAD LOGOS
# =========================================================

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSIR_LOGO_PATH = os.path.join(
    BASE_DIR,
    "CSIR-Logo-removebg-preview.png"
)

FOUNDATION_LOGO_PATH = os.path.join(
    BASE_DIR,
    "HOjbKMObQAIrYlw-removebg-preview.png"
)

if not os.path.exists(CSIR_LOGO_PATH):
    st.error("CSIR logo not found. Keep 'CSIR-Logo-removebg-preview.png' in the same folder as app.py.")
    st.stop()

if not os.path.exists(FOUNDATION_LOGO_PATH):
    st.error("85th Foundation logo not found. Keep 'HOjbKMObQAIrYlw-removebg-preview.png' in the same folder as app.py.")
    st.stop()

csir_logo = get_base64_image(CSIR_LOGO_PATH)
foundation_logo = get_base64_image(FOUNDATION_LOGO_PATH)

# =========================================================
# PAGE BACKGROUND + LOGOS
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background: linear-gradient(
            135deg,
            #ffe3ec 0%,
            #fff6db 35%,
            #dcf5ea 65%,
            #e3ecff 100%
        );
    }}

    h1,
    .stCaption,
    p {{
        color: #3a3550 !important;
    }}

    .top-left-logo {{
        position: fixed;
        top: 18px;
        left: 25px;
        width: 105px;
        height: 105px;
        object-fit: contain;
        z-index: 9999;
    }}

    .top-right-logo {{
        position: fixed;
        top: 20px;
        right: 25px;
        width: 125px;
        height: 90px;
        object-fit: contain;
        z-index: 9999;
    }}

    </style>

    <img
        class="top-left-logo"
        src="data:image/png;base64,{csir_logo}"
    >

    <img
        class="top-right-logo"
        src="data:image/png;base64,{foundation_logo}"
    >
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.title("🎡 QUIZ")


# =========================================================
# WHEEL HTML
# =========================================================

wheel_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Poppins', sans-serif; background: transparent; }

.main-area {
    width: 100%;
    min-height: 680px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 45px;
    align-items: center;
    padding: 20px 35px 30px 35px;
}

.left-side, .right-side {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.wheel-wrap {
    position: relative;
    width: 540px;
    height: 540px;
    max-width: 100%;
    max-height: 80vh;
    margin-bottom: 1.4rem;
}

.glow {
    position: absolute;
    inset: -50px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0) 70%);
    z-index: 0;
}

.pointer {
    position: absolute;
    top: -18px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 5;
    width: 0;
    height: 0;
    border-left: 22px solid transparent;
    border-right: 22px solid transparent;
    border-top: 36px solid #2d6cdf;
    filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.2));
}

svg#wheel {
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100%;
    display: block;
    border-radius: 50%;
    box-shadow: 0 0 0 9px #ffffff, 0 18px 45px rgba(90, 80, 120, 0.25);
    transition: transform 4.2s cubic-bezier(.17, .67, .16, 1);
}

.seg-label {
    font-weight: 800;
    font-size: 19px;
    fill: #2d2a3a;
    letter-spacing: 0.5px;
}

.label-g {
    transform-box: fill-box;
    transform-origin: 50% 50%;
    transition: transform 4.2s cubic-bezier(.17, .67, .16, 1);
}

.hub {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 125px;
    height: 125px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #6fa2ff, #2d6cdf 75%);
    border: 5px solid #ffffff;
    color: #ffffff;
    font-weight: 800;
    font-size: 1.25rem;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 6;
    cursor: pointer;
    box-shadow: 0 7px 18px rgba(45, 108, 223, 0.4);
    transition: transform 0.15s ease;
    user-select: none;
}

.hub:hover { filter: brightness(1.06); }
.hub:active { transform: translate(-50%, -50%) scale(0.94); }
.hub.disabled { opacity: 0.65; cursor: default; pointer-events: none; }

.result {
    width: 100%;
    max-width: 600px;
    min-height: 260px;
    background: #ffffff;
    border-radius: 22px;
    padding: 2rem 2.2rem;
    border: 1px solid #f0e4ee;
    color: #2d2a3a;
    box-shadow: 0 12px 35px rgba(90, 80, 120, 0.15);
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.75rem;
    opacity: 0;
    transition: opacity 0.4s ease;
}

.result.show { opacity: 1; }

.badge {
    align-self: flex-start;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #2d2a3a;
}

.badge.easy { background: #2ecc71; }
.badge.medium { background: #f1c40f; }
.badge.hard { background: #e74c3c; }

.question { font-size: 1.25rem; line-height: 1.65; color: #2d2a3a; }
.placeholder { color: #8b8599; font-size: 1.05rem; text-align: center; }
.score { margin-top: 1.1rem; color: #8b8599; font-size: 0.95rem; text-align: center; }
.score span { color: #3a3550; font-weight: 700; }

@media (max-width: 900px) {
    .main-area { grid-template-columns: 1fr; gap: 25px; padding: 10px 15px 30px 15px; }
    .wheel-wrap { width: 460px; height: 460px; }
}

@media (max-width: 550px) {
    .main-area { padding: 10px; }
    .wheel-wrap { width: 360px; height: 360px; }
    .hub { width: 100px; height: 100px; font-size: 1rem; }
    .seg-label { font-size: 16px; }
    .result { padding: 1.4rem; min-height: 220px; }
    .question { font-size: 1.05rem; }
}
</style>
</head>
<body>

<div class="main-area">
    <div class="left-side">
        <div class="wheel-wrap">
            <div class="glow"></div>
            <div class="pointer"></div>

            <svg id="wheel" viewBox="0 0 300 300">
                <path d="M150,150 L150,10 A140,140 0 0,1 271.24,220 Z" fill="#2ecc71"></path>
                <path d="M150,150 L271.24,220 A140,140 0 0,1 28.76,220 Z" fill="#f1c40f"></path>
                <path d="M150,150 L28.76,220 A140,140 0 0,1 150,10 Z" fill="#e74c3c"></path>

                <g class="label-g">
                    <text x="223.6" y="107.5" text-anchor="middle" class="seg-label">EASY</text>
                </g>
                <g class="label-g">
                    <text x="150" y="240" text-anchor="middle" class="seg-label">MEDIUM</text>
                </g>
                <g class="label-g">
                    <text x="76.4" y="107.5" text-anchor="middle" class="seg-label">HARD</text>
                </g>
            </svg>

            <div class="hub" id="hub">SPIN</div>
        </div>
    </div>

  
    </div>
</div>

<script>
const bank = __QUESTION_BANK__;

const centers = {
    easy: 60,
    medium: 180,
    hard: 300
};

const wheel = document.getElementById("wheel");
const hub = document.getElementById("hub");
const result = document.getElementById("result");
const countEl = document.getElementById("count");
const labelGroups = document.querySelectorAll(".label-g");

let currentRotation = 0;
let spinning = false;
let asked = 0;

const pools = {};
Object.keys(bank).forEach(function (cat) { pools[cat] = []; });

function shuffledCopy(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        const temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }
    return a;
}

function nextQuestion(category) {
    if (pools[category].length === 0) {
        pools[category] = shuffledCopy(bank[category]);
    }
    return pools[category].pop();
}

hub.addEventListener("click", function () {
    if (spinning) return;
    spinning = true;
    hub.classList.add("disabled");
    hub.textContent = "...";
    result.classList.remove("show");

    const names = Object.keys(bank);
    const category = names[Math.floor(Math.random() * names.length)];
    const question = nextQuestion(category);
    const center = centers[category];
    const targetMod = (360 - center + 360) % 360;
    const extraSpins = 5 + Math.floor(Math.random() * 3);
    const jitter = (Math.random() * 20) - 10;

    currentRotation = currentRotation - (currentRotation % 360) + extraSpins * 360 + targetMod + jitter;

    wheel.style.transform = "rotate(" + currentRotation + "deg)";

    labelGroups.forEach(function (g) {
        g.style.transform = "rotate(" + (-currentRotation) + "deg)";
    });

    setTimeout(function () {
        asked++;
        countEl.textContent = asked;

        result.innerHTML =
            '<span class="badge ' + category + '">' + category.toUpperCase() + '</span>' +
            '<div class="question">' + question + '</div>' +
            '<div class="score">Questions asked: <span>' + asked + '</span></div>';

        result.classList.add("show");
        spinning = false;
        hub.classList.remove("disabled");
        hub.textContent = "SPIN";
    }, 4300);
});
</script>

</body>
</html>
"""

# =========================================================
# INSERT QUESTION BANK
# =========================================================

wheel_html = wheel_html.replace(
    "__QUESTION_BANK__",
    json.dumps(bank)
)


# =========================================================
# DISPLAY WHEEL
# =========================================================

components.html(
    wheel_html,
    height=760,
    scrolling=False
)
