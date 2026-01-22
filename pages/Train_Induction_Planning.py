import streamlit as st
import numpy as np

st.set_page_config(
    page_title="AI Train Induction Planning",
    layout="wide"
)

st.title("🚆 AI-Assisted Train Induction Planning")
st.caption("Decision-support system for metro scheduling & headway optimization")

left, right = st.columns([2, 3])

with left:
    st.subheader("⚙️ Planning Inputs")

    with st.container(border=True):
        available_trains = st.slider(
            "Available Trains",
            min_value=2,
            max_value=20,
            value=10
        )

        optimization_priority = st.radio(
            "Optimization Priority",
            [
                "Minimize Waiting Time",
                "Energy Saving",
                "Balanced"
            ]
        )

        peak_mode = st.toggle("Peak Hour Mode", value=True)

        generate = st.button("🤖 Generate AI Plan", use_container_width=True)

def ai_train_planner(trains, priority, peak):
    """
    AI-inspired rule-based planner
    (Can be replaced with RL / optimization later)
    """

    if priority == "Minimize Waiting Time":
        deploy = int(trains * 0.9)
        headway = 2.5 if peak else 4
    elif priority == "Energy Saving":
        deploy = int(trains * 0.6)
        headway = 6 if not peak else 4.5
    else: 
        deploy = int(trains * 0.75)
        headway = 3.5 if peak else 5

    deploy = max(2, deploy)

    expected_wait = round(headway / 2, 1)

    overcrowding_risk = "Low"
    if peak and deploy < trains * 0.7:
        overcrowding_risk = "High"
    elif peak:
        overcrowding_risk = "Medium"

    return deploy, headway, expected_wait, overcrowding_risk

with right:
    st.subheader("📊 AI Output Preview")

    if generate:
        deploy, headway, wait_time, risk = ai_train_planner(
            available_trains,
            optimization_priority,
            peak_mode
        )

        with st.container(border=True):
            st.markdown("### 🤖 AI Deployment Recommendation")

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            col1.metric(
                "🚆 Trains to Deploy",
                deploy
            )

            col2.metric(
                "⏱ Headway (min)",
                f"{headway}"
            )

            col3.metric(
                "⌛ Expected Waiting Time",
                f"{wait_time} min"
            )

            if risk == "Low":
                col4.success("🟢 Overcrowding Risk: Low")
            elif risk == "Medium":
                col4.warning("🟡 Overcrowding Risk: Medium")
            else:
                col4.error("🔴 Overcrowding Risk: High")

            st.markdown("---")

            st.info(
                f"""
                **AI Insight:**  
                Based on **{optimization_priority.lower()}** priority and
                {'peak-hour conditions' if peak_mode else 'off-peak conditions'},
                the system recommends deploying **{deploy} trains**
                with an optimized **{headway}-minute headway**.
                """
            )

    else:
        st.info("Adjust inputs and click **Generate AI Plan** to view recommendations")
