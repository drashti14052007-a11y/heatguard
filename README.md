# 🌡️ HeatGuard

**Thermal Process Optimization for Food Safety**

A Python-based web dashboard that helps Indian MSME food processors find the most energy-efficient and FSSAI-compliant pasteurization process — without expensive industrial software.

---

## 🎯 What Problem Does HeatGuard Solve?

Small and mid-scale Indian food processors often **over-process** their products — running higher temperatures or longer times than needed — just to "play it safe." This leads to:
- Wasted energy and higher electricity bills
- Degraded product quality (flavour, nutrients, texture)
- No scientific basis for the process used

HeatGuard solves this by **simulating microbial kill kinetics** and finding the **minimum safe processing time** at any given temperature — saving energy while staying FSSAI compliant.

---

## 🧪 What HeatGuard Calculates

| Output | Description |
|---|---|
| Log Reduction | How many powers of 10 the pathogen population is reduced |
| PU Value | Pasteurization Units — total heat dose delivered |
| Optimal Time | Minimum time needed at a given temperature to meet FSSAI requirements |
| Energy Consumed | kWh used to heat the batch |
| Cost Saving | ₹ saved compared to over-processing at 95°C / 30 min |
| FSSAI Compliance | Green/Red badge showing if the process meets minimum safety standards |

---

## 🥛 Supported Products & Pathogens

**Products:** Milk, Juice, Coconut Water, Tomato Puree, Beer

**Target Pathogens:** Salmonella, Listeria monocytogenes, E. coli O157:H7, Mycobacterium tuberculosis

---

## 🔧 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| Streamlit | Web dashboard framework |
| Plotly | Interactive kill curve charts |
| Pandas | CSV data loading |
| NumPy | Numerical calculations |
| SciPy | Process optimization (minimize_scalar) |
| FPDF2 | PDF report generation |

---

## 📁 Project Structure
---

## 🚀 How to Run Locally

**Step 1 — Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/heatguard.git
cd heatguard
```

**Step 2 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the app:**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## ⚠️ Disclaimer

This is a **simulation tool for educational and planning purposes only.**
It is not a certified FSSAI instrument and should not replace validated thermal process studies.

**Model limitations:**
- Come-up time (heat penetration lag) is not modeled
- Water activity (Aw) effects are not included
- Assumes uniform temperature throughout the product

---

## 👨‍🔬 Built By

Food Technology B.Tech Student
Built as part of an academic food safety engineering project.

---

## 📜 License

For educational use only.