import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from models.kinetics import kill_curve
from models.lethality import pasteurization_units, required_time
from models.optimizer import find_optimal_time
from models.energy import energy_consumed, cost_saved
from utils.pdf_report import generate_report

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="HeatGuard",
    page_icon="🌡️",
    layout="wide"
)

# ── LOAD CSV DATA ─────────────────────────────────────────────
# Get the folder where app.py lives, then build path to data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

@st.cache_data
def load_data():
    pathogens_df = pd.read_csv(os.path.join(DATA_DIR, "pathogens.csv"))
    products_df  = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    energy_df    = pd.read_csv(os.path.join(DATA_DIR, "energy_costs.csv"))
    return pathogens_df, products_df, energy_df

pathogens_df, products_df, energy_df = load_data()

# Convert DataFrames to easy-lookup dictionaries
# Pathogen dict: { "Salmonella": {D_ref:..., T_ref:..., Z_value:..., target_log:...}, ... }
PATHOGENS = {
    row["name"]: {
        "D_ref":      row["D_ref"],
        "T_ref":      row["T_ref"],
        "Z_value":    row["Z_value"],
        "target_log": row["target_log"]
    }
    for _, row in pathogens_df.iterrows()
}

# Product dict: { "Milk": {Cp:..., T_ref:..., Z_value:...}, ... }
PRODUCTS = {
    row["name"]: {
        "Cp":      row["Cp"],
        "T_ref":   row["T_ref"],
        "Z_value": row["Z_value"]
    }
    for _, row in products_df.iterrows()
}

# Energy dict: { "Gujarat": 6.50, "Maharashtra": 8.20, ... }
ENERGY_TARIFFS = dict(zip(energy_df["state"], energy_df["tariff_INR_per_kWh"]))

# ── HEADER ────────────────────────────────────────────────────
st.title("🌡️ HeatGuard")
st.subheader("Thermal Process Optimization for Food Safety")
st.markdown("**For Indian MSME Food Processors** — Optimize pasteurization. Save energy. Stay compliant.")
st.divider()

# ── SIDEBAR INPUTS ────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Process Parameters")

    selected_product  = st.selectbox("Food Product",  list(PRODUCTS.keys()))
    selected_pathogen = st.selectbox("Target Pathogen", list(PATHOGENS.keys()))
    selected_state    = st.selectbox("State (for electricity tariff)", list(ENERGY_TARIFFS.keys()))

    st.divider()

    temperature = st.slider("Process Temperature (°C)", min_value=60, max_value=95, value=72, step=1)
    time        = st.slider("Process Time (minutes)",   min_value=1,  max_value=60, value=15, step=1)
    batch_size  = st.slider("Batch Size (kg)",          min_value=10, max_value=500, value=100, step=10)

    st.divider()
    st.caption("⚠️ This is a simulation tool. Not a certified FSSAI instrument.")
    st.caption("ℹ️ Model limitations: Come-up time not modeled. Water activity (Aw) effects not included.")

# ── RETRIEVE VALUES FROM LOADED DATA ─────────────────────────
product  = PRODUCTS[selected_product]
pathogen = PATHOGENS[selected_pathogen]
tariff   = ENERGY_TARIFFS[selected_state]

D_ref      = pathogen["D_ref"]
T_ref      = pathogen["T_ref"]
Z_value    = pathogen["Z_value"]
target_log = pathogen["target_log"]
Cp         = product["Cp"]
T_initial  = 25.0   # Assumed ambient start temperature

# ── CALCULATIONS ──────────────────────────────────────────────
from models.lethality import pasteurization_units, required_time
from models.energy import energy_consumed, cost_saved

log_red   = round(time / (D_ref * 10 ** ((T_ref - temperature) / Z_value)), 2)
pu_val    = round(pasteurization_units(temperature, time, T_ref, Z_value), 2)
energy    = energy_consumed(batch_size, temperature, T_initial, Cp)
opt_time  = find_optimal_time(D_ref, T_ref, Z_value, temperature, target_log)

# Compare against over-processing default: 95°C for 30 min
energy_diff, saving = cost_saved(
    temperature, opt_time,
    95, 30,
    batch_size, T_initial, Cp, tariff
)

# FSSAI compliance: minimum 6D reduction required
compliant = log_red >= target_log

# ── METRIC CARDS ──────────────────────────────────────────────
st.subheader("📊 Process Results")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Log Reduction",  f"{log_red} log",   help="Pathogen kill achieved at current settings")
col2.metric("PU Value",       f"{pu_val} PU",      help="Pasteurization Units — measure of heat dose")
col3.metric("Energy Used",    f"{energy} kWh",     help="Energy consumed for this batch")
col4.metric("Potential Saving", f"₹{saving}",      help="Savings vs over-processing at 95°C / 30 min")

# FSSAI Badge
st.divider()
if compliant:
    st.success(f"✅ FSSAI COMPLIANT — {log_red} log reduction achieved. Minimum required: {target_log} log.")
else:
    needed = round(required_time(D_ref, T_ref, Z_value, temperature, target_log), 2)
    st.error(f"❌ NOT COMPLIANT — Only {log_red} log reduction. Need {target_log} log. Increase time to {needed} min.")

# ── KILL CURVE CHART ──────────────────────────────────────────
st.divider()
st.subheader("📈 Microbial Kill Curve")

times, log_reductions = kill_curve(D_ref, T_ref, Z_value, temperature)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=list(times), y=list(log_reductions),
    mode="lines", name="Log Reduction",
    line=dict(color="#00cc88", width=3)
))
fig.add_hline(
    y=target_log, line_dash="dash",
    line_color="red",
    annotation_text=f"FSSAI Minimum ({target_log} log)",
    annotation_position="right"
)
fig.add_vline(
    x=time, line_dash="dot",
    line_color="orange",
    annotation_text=f"Your time ({time} min)",
    annotation_position="top right"
)
fig.update_layout(
    xaxis_title="Time (minutes)",
    yaxis_title="Log Reduction",
    template="plotly_dark",
    height=400,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# ── OPTIMIZATION RECOMMENDATION ───────────────────────────────
st.divider()
st.subheader("🎯 Optimization Recommendation")

st.info(
    f"**Minimum safe time at {temperature}°C = {opt_time} minutes**\n\n"
    f"Running at {time} min uses {'more' if time > opt_time else 'less'} time than needed. "
    f"{'Consider reducing to ' + str(opt_time) + ' min to save energy.' if time > opt_time else 'Increase time to meet FSSAI minimum.'}"
)

# ── PDF DOWNLOAD ──────────────────────────────────────────────
st.divider()
st.subheader("📄 Download Process Report")

pdf = generate_report(
    product=selected_product,
    pathogen=selected_pathogen,
    temperature=temperature,
    time=time,
    log_reduction=log_red,
    pu_value=pu_val,
    energy_kwh=energy,
    cost_saving=saving,
    compliance_status="COMPLIANT ✅" if compliant else "NOT COMPLIANT ❌"
)

pdf_bytes = bytes(pdf.output())
st.download_button(
    label="⬇️ Download PDF Report",
    data=pdf_bytes,
    file_name=f"HeatGuard_{selected_product}_{selected_pathogen}.pdf",
    mime="application/pdf"
)