import streamlit as st
import base64
from cta import STATION_OPTIONS, get_train_arrivals, LINE_COLORS
from ai import ask_demon
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AskDemon – DePaul Assistant",
    layout="centered",
    page_icon="📘"
)

# --- LOGO + HEADER ---
with open("depaul_logo.png", "rb") as f:
    img_data = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <div style='text-align: center; padding-bottom: 10px;'>
        <img src="data:image/png;base64,{img_data}" width="120"/>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='color:#1E4BA1; text-align:center;'>AskDemon</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>Your Campus Companion at DePaul</h4>",
    unsafe_allow_html=True
)

# ---------- CTA TRAIN TRACKER (COLLAPSIBLE) ----------
with st.expander("🚇 CTA Train Arrivals", expanded=True):  # starts open
    selected_station = st.selectbox("Choose your CTA station", list(STATION_OPTIONS.keys()))

    if st.button("Check Arrivals"):
        stop_id = STATION_OPTIONS[selected_station]
        trains = get_train_arrivals(stop_id)

        for train in trains:
            line = train.get("line", "Unknown")
            color = LINE_COLORS.get(line, "#D3D3D3")

            box_style = f"""
                background-color: {color};
                padding: 10px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                margin-bottom: 10px;
            """
            st.markdown(
                f"<div style='{box_style}'>🚇 {line} Line → {train['destination']} arriving at {train['arrival_time']}</div>",
                unsafe_allow_html=True
            )


# ---------- AI CHATBOT ----------
st.divider()
st.subheader("💬 Ask Anything About DePaul")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("What's on your mind?")

if user_input:
    with st.spinner("Thinking..."):
        reply = ask_demon(user_input)
        st.session_state.history.append((user_input, reply))
        st.success(reply)

st.markdown("### 🗂️ Chat History")
for q, a in reversed(st.session_state.history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")

#Streamlit