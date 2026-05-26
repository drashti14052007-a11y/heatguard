from fpdf import FPDF

def generate_report(product, pathogen, temperature, time,
                    log_reduction, pu_value, energy_kwh,
                    cost_saving, compliance_status):

    clean_status = compliance_status.replace("✅", "").replace("❌", "").strip()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 15, "HeatGuard Process Report", ln=True, align="C")

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, "Thermal Process Optimization for Food Safety", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Process Parameters", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Product         : {product}", ln=True)
    pdf.cell(0, 8, f"Target Pathogen : {pathogen}", ln=True)
    pdf.cell(0, 8, f"Temperature     : {temperature} C", ln=True)
    pdf.cell(0, 8, f"Time            : {time} minutes", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Results", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Log Reduction   : {log_reduction}", ln=True)
    pdf.cell(0, 8, f"PU Value        : {pu_value}", ln=True)
    pdf.cell(0, 8, f"Energy Used     : {energy_kwh} kWh", ln=True)
    pdf.cell(0, 8, f"Cost Saving     : Rs {cost_saving}", ln=True)
    pdf.cell(0, 8, f"FSSAI Status    : {clean_status}", ln=True)

    return pdf

