import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="What-If Scenario Simulator",
    layout="wide"
)

st.title("🔮 What-If Scenario Simulator")
st.caption("Strategic AI simulation for metro operational planning")

left, right = st.columns([2, 3])

with left:
    st.subheader("⚙️ Scenario Inputs")

    with st.container(border=True):
        demand_increase = st.slider(
            "Passenger Demand Increase (%)",
            0, 100, 20
        )

        unavailable_trains = st.slider(
            "Trains Unavailable",
            0, 10, 2
        )

        st.markdown("### 🌦️ Special Events")
        rain = st.toggle("Rain")
        festival = st.toggle("Festival / City Event")

        run_simulation = st.button(
            "🔁 Run Simulation",
            use_container_width=True
        )

BASE_DEMAND = 12000
BASE_TRAINS = 12
TRAIN_CAPACITY = 1000
BASE_HEADWAY = 4  # minutes

def simulate_scenario(demand_inc, trains_down, rain, festival):
    demand = BASE_DEMAND * (1 + demand_inc / 100)

    if rain:
        demand *= 1.1
    if festival:
        demand *= 1.25

    available_trains = max(2, BASE_TRAINS - trains_down)

    load_factor = demand / (available_trains * TRAIN_CAPACITY)

    waiting_time = round(BASE_HEADWAY * load_factor, 1)
    energy_use = round(available_trains * 1.2, 1)

    if load_factor > 1.1:
        risk = "High"
    elif load_factor > 0.85:
        risk = "Medium"
    else:
        risk = "Low"

    return demand, available_trains, waiting_time, energy_use, risk

with right:
    st.subheader("📊 Simulation Results")

    if run_simulation:
        sim_demand, sim_trains, sim_wait, sim_energy, sim_risk = simulate_scenario(
            demand_increase,
            unavailable_trains,
            rain,
            festival
        )

        with st.container(border=True):
            c1, c2, c3, c4 = st.columns(4)

            c1.metric("👥 Passenger Demand",
                      f"{int(sim_demand)}",
                      f"+{int(sim_demand - BASE_DEMAND)}")

            c2.metric("🚆 Trains Available",
                      sim_trains,
                      f"-{unavailable_trains}")

            c3.metric("⏱ Avg Waiting Time",
                      f"{sim_wait} min",
                      f"+{round(sim_wait - BASE_HEADWAY,1)}")

            if sim_risk == "Low":
                c4.success("🟢 Overcrowding: Low")
            elif sim_risk == "Medium":
                c4.warning("🟡 Overcrowding: Medium")
            else:
                c4.error("🔴 Overcrowding: High")

        st.markdown("### 📈 Before vs After Comparison")

        labels = ["Demand", "Waiting Time", "Energy Usage"]
        before = [BASE_DEMAND, BASE_HEADWAY, BASE_TRAINS * 1.2]
        after = [sim_demand, sim_wait, sim_energy]

        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(labels))

        ax.bar(x - 0.2, before, width=0.4, label="Normal")
        ax.bar(x + 0.2, after, width=0.4, label="Scenario")

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.grid(alpha=0.3)

        st.pyplot(fig)

        st.info(
            f"""
            **AI Strategic Insight:**  
            The simulated scenario shows a **{demand_increase}% demand surge**
            with **{unavailable_trains} trains unavailable**.
            This leads to a **{sim_risk.lower()} overcrowding risk** and
            increased waiting time of **{sim_wait} minutes**.
            """
        )

    else:
        st.info("Adjust scenario parameters and click **Run Simulation**")

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        padding: 15px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
