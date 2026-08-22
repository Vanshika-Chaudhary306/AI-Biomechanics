import streamlit as st
from tracker import process_video
import tempfile
import os
import base64
import time

# 1. Page Configuration (Must be the very first Streamlit call)
st.set_page_config(
    page_title="AI Sports Coach",
    page_icon="⚽",
    layout="wide"
)

# Initialize theme state in session_state
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

# 2. Splash Screen: Rotating Cyber Football & Progress Ring
splash_placeholder = st.empty()

with splash_placeholder.container():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&display=swap');

    .splash-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: radial-gradient(circle at center, #0d1527 0%, #05070d 100%);
        z-index: 999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOut 0.8s ease-in-out 2.0s forwards;
    }

    .ball-wrapper {
        position: relative;
        width: 120px;
        height: 120px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .glowing-ball {
        font-size: 75px;
        animation: spinAndPulse 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        filter: drop-shadow(0 0 25px #00e5ff) drop-shadow(0 0 45px #ff007f);
    }

    .ring {
        position: absolute;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        border: 2px dashed rgba(0, 229, 255, 0.6);
        animation: rotateRing 3s linear infinite;
    }

    .splash-title {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 26px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 4px;
        margin-top: 25px;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.8);
    }

    .splash-subtitle {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 12px;
        font-weight: 500;
        color: #00e5ff;
        letter-spacing: 2px;
        margin-top: 8px;
    }

    @keyframes spinAndPulse {
        0% { transform: rotate(0deg) scale(0.9); }
        50% { transform: rotate(180deg) scale(1.15); }
        100% { transform: rotate(360deg) scale(0.9); }
    }

    @keyframes rotateRing {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(-360deg); }
    }

    @keyframes fadeOut {
        0% { opacity: 1; pointer-events: all; }
        100% { opacity: 0; pointer-events: none; }
    }
    </style>

    <div class="splash-container">
        <div class="ball-wrapper">
            <div class="ring"></div>
            <div class="glowing-ball">⚽</div>
        </div>
        <div class="splash-title">AI BIOMECHANICS COACH</div>
        <div class="splash-subtitle">INITIALIZING AI BIOMECHANICS COACH...</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2.2)

splash_placeholder.empty()

# 3. Dynamic Theme & Universal Orbitron Style Injector
def apply_theme(image_file, mode="Dark"):
    encoded = ""
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

    if mode == "Dark":
        overlay = "rgba(10, 15, 29, 0.88)"
        text_color = "#FFFFFF"
        sub_text_color = "#E2E8F0"
        accent_color = "#00E5FF"
        input_bg = "rgba(15, 23, 42, 0.65)"
    else:
        overlay = "rgba(248, 250, 252, 0.92)"
        text_color = "#0F172A"
        sub_text_color = "#334155"
        accent_color = "#0284C7"
        input_bg = "rgba(255, 255, 255, 0.75)"

    bg_css = f'url("data:image/jpeg;base64,{encoded}")' if encoded else "none"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&display=swap');

    /* Safe Global Orbitron Typography */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp label {{
        font-family: 'Orbitron', sans-serif !important;
    }}

    .stApp {{
        background: linear-gradient({overlay}, {overlay}), {bg_css};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    h1, h2, h3, h4 {{
        font-weight: 700 !important;
        color: {text_color} !important;
    }}

    p, span, label {{
        color: {text_color};
        font-weight: 400;
    }}

    .stMarkdown {{
        color: {sub_text_color} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {accent_color} !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* Scoped styling ONLY for the theme toggle icon */
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"] button {{
        background: {input_bg} !important;
        border: 1px solid rgba(0, 229, 255, 0.35) !important;
        border-radius: 50px !important;
        color: {accent_color} !important;
        padding: 4px 14px !important;
        font-size: 18px !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.15) !important;
        transition: all 0.3s ease !important;
    }}

    div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"] button:hover {{
        border-color: #ff007f !important;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.4) !important;
        transform: scale(1.05);
    }}

    /* Fix File Uploader UI Box */
    [data-testid="stFileUploader"] {{
        font-family: 'Orbitron', sans-serif !important;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        border: 1px dashed rgba(0, 229, 255, 0.4) !important;
        border-radius: 8px !important;
        background: {input_bg} !important;
    }}

    /* Animated AI BIOMECHANICS COACH Banner */
    .branding-container {{
        width: 100%;
        overflow: hidden;
        margin: 5px 0 15px 0;
        padding: 6px 0;
        background: rgba(0, 229, 255, 0.05);
        border-top: 1px solid rgba(0, 229, 255, 0.2);
        border-bottom: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 8px;
    }}

    .branding-track {{
        display: inline-block;
        white-space: nowrap;
        animation: marqueeBrand 16s linear infinite;
    }}

    .branding-text {{
        font-family: 'Orbitron', sans-serif !important;
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 4px;
        color: {accent_color};
        text-shadow: 0 0 12px {accent_color}, 0 0 25px rgba(255, 0, 127, 0.6);
        padding: 0 2rem;
    }}

    @keyframes marqueeBrand {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Header Bar with Compact Top-Right Theme Toggle
header_col1, header_col2 = st.columns([0.92, 0.08])

with header_col2:
    toggle_icon = "☀️" if st.session_state.theme_mode == "Dark" else "🌙"
    if st.button(toggle_icon, key="theme_toggle_btn", help="Toggle Light/Dark Theme"):
        st.session_state.theme_mode = "Light" if st.session_state.theme_mode == "Dark" else "Dark"
        st.rerun()

# Apply theme styling
apply_theme("bg3.jpeg", mode=st.session_state.theme_mode)

# 5. Prominent Animated Branding Banner (Marquee Animation)
st.markdown("""
<div class="branding-container">
    <div class="branding-track">
        <span class="branding-text">⚡ AI BIOMECHANICS COACH ⚡</span>
        <span class="branding-text">⚡ AI BIOMECHANICS COACH ⚡</span>
        <span class="branding-text">⚡ AI BIOMECHANICS COACH ⚡</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Title and Description
st.title("AI Sports Mechanics Coach 🏀⚽")
st.markdown(
    "Upload your video to compare your biomechanical form with a professional athlete."
)

# 7. User Selections
col_in1, col_in2 = st.columns(2)
with col_in1:
    sport_choice = st.selectbox(
        "Select Sport",
        ["Basketball", "Football"]
    )
with col_in2:
    dominant_side = st.selectbox(
        "Dominant Side (Shooting Hand / Kicking Leg)",
        ["Right-Side", "Left-Side"]
    )

# 8. Main Dual-Column Comparison Layout
col1, col2 = st.columns(2)

# Left Column: Reference Video
with col1:
    st.header("Pro Form (Reference)")

    if sport_choice == "Basketball":
        pro_video_url = "Basketball.mp4"
        if os.path.exists(pro_video_url):
            st.video(pro_video_url)
        st.success("Target: Maintain a 90-degree shooting elbow prior to release.")
    else:
        pro_video_url = "Football.mp4"
        if os.path.exists(pro_video_url):
            st.video(pro_video_url)
        st.success("Target: Deep knee bend (< 100 deg) on the backswing for maximum striking power.")

# Right Column: User Analysis
with col2:
    st.header("Your Analysis")

    feedback = {}
    accuracy = 0

    uploaded_file = st.file_uploader(
        f"Upload your .mp4 {sport_choice} video",
        type=["mp4"]
    )

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_file.read())
        tfile.close()

        input_video_path = tfile.name
        output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".webm").name

        st_frame = st.empty()

        with st.spinner(f"Running {sport_choice} Biomechanical Analysis..."):
            feedback, accuracy = process_video(
                input_video_path,
                output_video_path,
                sport=sport_choice,
                dominant_side=dominant_side,
                st_frame=st_frame
            )

        st.success("Analysis Complete! Review the footage below.")
        st.video(output_video_path)

        # Performance Metrics & Breakdown
        st.subheader("📊 Final Performance Analysis")
        st.metric("Accuracy", f"{int(accuracy)}%")
        st.progress(int(accuracy) / 100)

        if feedback and "areas" in feedback:
            st.subheader("📌 Areas to Improve")
            for point in feedback["areas"]:
                st.markdown(f"- **{point}**")

        if feedback and "technical" in feedback:
            st.subheader("⚙️ Technical Feedback")
            for tip in feedback["technical"]:
                st.markdown(f"- {tip}")

        # Cleanup temporary files safely
        for path in [input_video_path, output_video_path]:
            try:
                os.remove(path)
            except Exception:
                pass