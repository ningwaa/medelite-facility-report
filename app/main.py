import os
from flask import Flask, render_template, request, send_from_directory
from app.utils.report import generate_pdf

app = Flask(__name__, template_folder="templates")

def get_facility(facility_id):
    mock_database = {
        "1001": {
            "name": "Sunrise Care Center",
            "hospitalizations": 12,
            "star_rating": 4,
            "staffing_score": 3.8,
            "inspection_score": 88
        },
        "1002": {
            "name": "Grand Valley Pavilion",
            "hospitalizations": 4,
            "star_rating": 5,
            "staffing_score": 4.7,
            "inspection_score": 95
        },
        "1003": {
            "name": "Mercy Health Infirmary",
            "hospitalizations": 22,
            "star_rating": 2,
            "staffing_score": 1.9,
            "inspection_score": 62
        }
    }
    
    clean_id = str(facility_id).strip() if facility_id else ""
    if clean_id in mock_database:
        return mock_database[clean_id]
    else:
        id_hash = sum(ord(char) for char in clean_id) if clean_id else 105
        return {
            "name": f"Facility Profile #{clean_id or '999'}",
            "hospitalizations": (id_hash % 15) + 3,
            "star_rating": (id_hash % 4) + 2,
            "staffing_score": round(2.5 + (id_hash % 20) / 10, 1),
            "inspection_score": 65 + (id_hash % 30)
        }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    facility_id = request.form.get("facility_id")
    facility = get_facility(facility_id)
    cms_data = facility

    name_override = request.form.get("facility_name_override")
    if name_override and name_override.strip():
        cms_data["name"] = name_override.strip()

    location_input = request.form.get("location", "").strip()
    
    # Simple logic to find a state abbreviation from input 
    state_code = "US"
    if location_input:
        parts = [p.strip().upper() for p in location_input.replace(",", " ").split()]
        for part in parts:
            if len(part) == 2 and part.isalpha():
                state_code = part
                break

    manual_data = {
        "name_override": name_override,
        "location": location_input,
        "state_code": state_code,
        "emr": request.form.get("emr"),
        "capacity": request.form.get("capacity"),
        "census": request.form.get("census"),
        "patient_type": request.form.get("patient_type"),
        "prev_coverage": request.form.get("prev_coverage"),
        "provider_performance": request.form.get("provider_performance"),
        "medical_coverage": request.form.get("medical_coverage"),
        "notes": request.form.get("notes"),
    }

    risk_score = (
        cms_data["hospitalizations"] * 2
        + (5 - cms_data["star_rating"]) * 10
        + (100 - cms_data["inspection_score"]) * 0.5
    )

    if risk_score < 30:
        risk_level = "Low"
    elif risk_score < 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    pdf_path = generate_pdf(facility_id, cms_data, manual_data["notes"])

    return render_template(
        "result.html",
        facility=cms_data,
        facility_id=facility_id,
        pdf_path=pdf_path,
        risk_score=round(risk_score, 1),
        risk_level=risk_level,
        data=manual_data
    )

@app.route("/reports/<filename>")
def download_report(filename):
    return send_from_directory(
        directory=os.path.abspath("reports"),
        path=filename,
        as_attachment=True
    )

if __name__ == "__main__":
     port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)