import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import matplotlib.pyplot as plt

# ------------------ LOAD MODELS ------------------
model = joblib.load("./model/demand_forecast_model.pkl")
features = joblib.load("./model/model_features.pkl")

# ------------------ CONSTANTS ------------------
TRAIN_CAPACITY = 1000
MIN_TRAINS = 2
MAX_TRAINS = 10

STATIONS = [
    "Aluva", "Pulinchodu", "Companypady", "Ambattukavu",
    "Muttom", "Kalamassery", "CUSAT", "Edappally",
    "Kaloor", "MG Road", "Maharaja’s", "Ernakulam South"
]

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="KMRL AI Operations Dashboard",
    layout="wide"
)

st.title("🚆 Kochi Metro – AI Operations Control Dashboard")

# =================================================
# INPUT PANEL (TOP)
# =================================================
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    hour = col1.slider("Hour", 0, 23, 9)
    day_type = col2.selectbox("Day Type", ["Weekday", "Weekend"])
    trains_per_hour = col3.slider("Trains / Hour", 1, 10, 5)
    direction_id = col4.selectbox("Direction", [0, 1])
    run_ai = col5.button("🔮 Run AI")

is_weekend = 1 if day_type == "Weekend" else 0
is_peak = 1 if (8 <= hour <= 10 or 17 <= hour <= 20) else 0

# =================================================
# AI PREDICTION
# =================================================
predicted_demand = 0
recommended_trains = 0
confidence = 0

if run_ai:
    input_df = pd.DataFrame([{
        "hour": hour,
        "is_weekend": is_weekend,
        "is_peak_hour": is_peak,
        "trains_per_hour": trains_per_hour,
        "direction_id": direction_id
    }])

    input_df = input_df[features]

    predicted_demand = int(model.predict(input_df)[0])

    base_trains = np.ceil(predicted_demand / TRAIN_CAPACITY)
    recommended_trains = int(
        min(max(base_trains + (1 if is_peak else 0), MIN_TRAINS), MAX_TRAINS)
    )

    confidence = min(95, 70 + recommended_trains * 3)

# =================================================
# MAIN DASHBOARD LAYOUT
# =================================================
left, center, right = st.columns([2.2, 3, 2])

# -------------------------------------------------
# LEFT: METRO LINE MAP
# -------------------------------------------------
with left:
    st.subheader("🗺️ Metro Line Status")

    congestion = np.clip(predicted_demand / 800, 0, 1)

    for i, station in enumerate(STATIONS):
        if congestion < 0.6:
            color = "🟢"
        elif congestion < 0.9:
            color = "🟡"
        else:
            color = "🔴"

        train_icon = "🚆" if i == (hour % len(STATIONS)) else "➖"
        st.markdown(f"{color} **{station}** {train_icon}")

# -------------------------------------------------
# CENTER: AI RECOMMENDATION CARD
# -------------------------------------------------
with center:
    st.subheader("🤖 AI Recommendation")

    if run_ai:
        st.markdown(
            f"""
            ### 🚆 Recommended Trains: **{recommended_trains}**
            **Priority Corridor:** {"Aluva → Ernakulam" if direction_id == 0 else "Ernakulam → Aluva"}  
            **Confidence:** {confidence}%  

            _Reason:_  
            Peak demand detected with predicted load of **{predicted_demand} passengers**.
            """
        )

        c1, c2 = st.columns(2)
        c1.button("✅ Accept Plan")
        c2.button("🔁 Recalculate")
    else:
        st.info("Run AI to generate recommendations")

# -------------------------------------------------
# RIGHT: KPI CARDS
# -------------------------------------------------
with right:
    st.subheader("📊 Key Performance Indicators")

    if run_ai:
        avg_wait = max(2, 10 - recommended_trains)
        load_pct = min(100, int((predicted_demand / (recommended_trains * TRAIN_CAPACITY)) * 100))
        energy_eff = max(60, 100 - recommended_trains * 4)
        comfort = max(50, 100 - load_pct)

        st.metric("⏱ Avg Waiting Time (min)", avg_wait)
        st.metric("👥 Passenger Load %", f"{load_pct}%")
        st.metric("⚡ Energy Efficiency", f"{energy_eff}%")
        st.metric("🙂 Comfort Index", f"{comfort}%")
    else:
        st.metric("⏱ Avg Waiting Time", "-")
        st.metric("👥 Passenger Load %", "-")
        st.metric("⚡ Energy Efficiency", "-")
        st.metric("🙂 Comfort Index", "-")

# =================================================
# BOTTOM: DEMAND TREND GRAPH
# =================================================
st.subheader("📈 Passenger Demand Trend")

history_hours = list(range(24))
historical = np.random.randint(200, 900, size=24)
predicted = historical.copy()
predicted[hour] = predicted_demand

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(history_hours, historical, label="Historical Demand")
ax.plot(history_hours, predicted, label="AI Predicted", linestyle="--")
ax.axvline(hour, linestyle=":", label="Peak Hour")

ax.set_xlabel("Hour")
ax.set_ylabel("Passengers")
ax.legend()
st.pyplot(fig)
