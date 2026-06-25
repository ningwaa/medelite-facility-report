import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(facility_id, facility, notes, state_code="US"):
    """
    Generates a professional compliance PDF report matching the internal corporate brand matrix.
    Includes a dynamic clickable hyperlink to the official Medicare Care Compare source profile.
    """
    os.makedirs("reports", exist_ok=True)

    filename = f"{facility_id}_report.pdf"
    file_path = os.path.join("reports", filename)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # 
    # Visual requirements
    # 
    # Static Corporate Brand Line
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.117, 0.251, 0.686)  # MedElite Navy Blue (#1e40af)
    c.drawString(50, height - 45, "INFINITE — Managed by MEDELITE")
    
    # Required Document Header with Dynamic State code
    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0.058, 0.090, 0.165)  # Dark Slate Ink
    c.drawString(50, height - 68, f"FACILITY ASSESSMENT SNAPSHOT ({state_code.upper()})")
    
    # Visual Separator Line
    c.setLineWidth(1.5)
    c.setStrokeColorRGB(0.117, 0.251, 0.686)
    c.line(50, height - 78, width - 50, height - 78)

    #
    # Report body
    # 
    c.setFillColorRGB(0.117, 0.251, 0.686)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 110, "CMS DATA METRICS")
    
    # Divider line for section
    c.setLineWidth(0.5)
    c.setStrokeColorRGB(0.88, 0.91, 0.94)
    c.line(50, height - 115, width - 50, height - 115)

    c.setFillColorRGB(0.09, 0.11, 0.16)
    c.setFont("Helvetica", 11)
    
    # Critical Guardrail: Facility name belongs strictly inside the report body layout
    facility_name = facility.get('name', f"Facility {facility_id}")
    
    c.drawString(50, height - 140, f"Name of Facility: {facility_name}")
    c.drawString(50, height - 160, f"Facility ID Identifier: {facility_id}")
    c.drawString(50, height - 180, f"Overall Star Rating: {facility.get('star_rating', 'N/A')} / 5")
    c.drawString(50, height - 200, f"Hospitalization Incidence: {facility.get('hospitalizations', 'N/A')}")
    c.drawString(50, height - 220, f"Staffing Index Metric: {facility.get('staffing_score', 'N/A')}")
    c.drawString(50, height - 240, f"Health Inspection Profile: {facility.get('inspection_score', 'N/A')}")

    # 
    # Dynamic Medicare Source Hyperlink (
    # 
    medicare_url = f"https://www.medicare.gov/care-compare/details/nursing-home/{facility_id}"
    
    c.setFillColorRGB(0.176, 0.424, 0.875)  # Action Link Blue (#2d6cdf)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 265, "→ View Official Medicare Care Compare Profile")
    
    # Invisible clickable canvas rectangle bound over the text link coordinates
    c.linkURL(medicare_url, (50, height - 270, 300, height - 250), relative=1)

    # 
    # Report body (director notes)
    # 
    c.setFillColorRGB(0.117, 0.251, 0.686)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 300, "OPERATIONAL DIRECTOR NOTES")
    
    c.setLineWidth(0.5)
    c.setStrokeColorRGB(0.88, 0.91, 0.94)
    c.line(50, height - 305, width - 50, height - 305)
    
    c.setFillColorRGB(0.278, 0.333, 0.412)  # Muted Dark Grey
    c.setFont("Helvetica-Oblique", 10.5)
    
    clean_notes = str(notes).strip() if notes else "No specific operational notes attached to this facility intake profile."
    
    # 
    y_position = height - 325
    for line in [clean_notes[i:i+85] for i in range(0, len(clean_notes), 85)]:
        if y_position > 60:
            c.drawString(50, y_position, line)
            y_position -= 18

    # 
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.557, 0.612, 0.686)
    c.drawString(50, 40, "CONFIDENTIAL — FOR INTERNAL MEDELITE EVALUATION USE ONLY")

    c.save()
    return filename