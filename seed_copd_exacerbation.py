from app.database import SessionLocal
from app.models import User, Template, Category

def seed_copd_exacerbation():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "COPD Exacerbation",
        "description": "Acute COPD exacerbation management covering steroid/antibiotic decisions, NICE NG114 vs GOLD guidance, admission criteria, and patient education resources.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Current Exacerbation",
                "section_type": "history",
                "questions": [
                    {"id": "copde_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Worsening SOB and purulent sputum for 4 days"},
                    {"id": "copde_duration", "type": "text", "label": "Duration of Worsening Symptoms", "required": True, "placeholder": "e.g., 4 days"},
                    {"id": "copde_dyspnoea", "type": "single_select", "label": "Dyspnoea Compared to Baseline", "required": True, "options": ["Worse at rest", "Worse on exertion (stairs/hills)", "Both"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB at rest = ?severe exacerbation. Consider admission if SpO2 <90%.", "red_flag_negative": ""},
                    {"id": "copde_sputum_change", "type": "multi_select", "label": "Sputum Changes", "required": True, "options": ["Change in sputum colour", "Change in sputum volume / thickness"]},
                    {"id": "copde_sputum_volume", "type": "text", "label": "Sputum Volume", "required": False, "placeholder": "e.g., 2 teaspoons daily"},
                    {"id": "copde_sputum_character", "type": "single_select", "label": "Sputum Character", "required": True, "options": ["Purulent (yellow/green)", "Mucoid (white/clear)", "Clear"]},
                    {"id": "copde_haemoptysis", "type": "single_select", "label": "Haemoptysis?", "required": True, "options": ["No blood", "Blood present - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemoptysis = ?lung cancer, pneumonia. CXR urgently.", "red_flag_negative": ""},
                    {"id": "copde_associated", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Wheeze", "Chest tightness"]}
                ]
            },
            {
                "title": "Exacerbation History & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "copde_prior_exacerbations", "type": "number", "label": "Prior Exacerbations in Last Year", "required": True, "placeholder": "e.g., 3"},
                    {"id": "copde_prior_steroids", "type": "number", "label": "Courses of Systemic Steroids/Antibiotics in Last Year", "required": False, "placeholder": "e.g., 2"},
                    {"id": "copde_prior_admissions", "type": "single_select", "label": "Prior Hospital Admissions", "required": True, "options": ["None", "1 admission", "≥2 admissions"]},
                    {"id": "copde_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Current smoker", "Ex-smoker", "Never smoked"]},
                    {"id": "copde_systemic", "type": "multi_select", "label": "Systemic Symptoms", "required": True, "options": ["Fever", "Chills / rigors", "Weight loss", "Night sweats", "None present"]},
                    {"id": "copde_cardiac", "type": "multi_select", "label": "Cardiac Screen", "required": True, "options": ["Chest pain", "Chest pressure / tightness", "Peripheral oedema", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain + SOB = ?ACS, PE. ECG + troponin. Peripheral oedema = ?cor pulmonale.", "red_flag_negative": ""},
                    {"id": "copde_urti", "type": "toggle", "label": "URTI Symptoms (Preceding)?", "required": False},
                    {"id": "copde_cat", "type": "number", "label": "CAT Score (0-40)", "required": False, "placeholder": "e.g., 28"}
                ]
            },
            {
                "title": "Vaccination Status",
                "section_type": "history",
                "questions": [
                    {"id": "copde_flu_vax", "type": "toggle", "label": "Flu Vaccine Received This Year?", "required": True},
                    {"id": "copde_pneumo_vax", "type": "toggle", "label": "Pneumococcal Vaccine Within Last 5 Years?", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "copde_vitals", "type": "text", "label": "Vital Signs", "required": True, "placeholder": "e.g., HR 80, Temp 37°C, SpO2 99%, RR 20"},
                    {"id": "copde_spo2_value", "type": "number", "label": "SpO2 (%)", "required": False, "placeholder": "e.g., 92", "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 <90% = severe exacerbation. Consider hospital admission.", "red_flag_negative": ""},
                    {"id": "copde_resp", "type": "multi_select", "label": "Respiratory Examination", "required": True, "options": ["Decreased breath sounds", "Expiratory wheeze", "Inspiratory crackles at lung base", "Normal"]},
                    {"id": "copde_clubbing", "type": "toggle", "label": "Clubbing?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Clubbing = ?lung cancer. CXR.", "red_flag_negative": ""},
                    {"id": "copde_weight", "type": "number", "label": "Weight (kg) - Steroid Dosing", "required": False, "placeholder": "e.g., 68 (Pred 40mg if ≥60kg, 30mg if <60kg)"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Infective COPD Exacerbation (viral/bacterial)",
                    "Non-Infective COPD Exacerbation (pollution, weather, comorbidity)",
                    "Pneumonia (focal crackles, fever, consolidation on CXR)",
                    "Pneumothorax (acute unilateral pain + SOB)",
                    "Heart Failure / Cor Pulmonale (peripheral oedema, elevated JVP)",
                    "PE (acute SOB + chest pain)"
                ],
                "questions": [
                    {"id": "copde_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["COPD Exacerbation - Mild/Moderate", "COPD Exacerbation - Severe (?Admission)", "COPD Exacerbation with Pneumonia", "Alternative diagnosis suspected"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: worsening SOB at rest, SpO2 <90%, new chest pain, haemoptysis, confusion, or inability to cope at home. Review in 48-72 hours or at end of steroid/antibiotic course. Steroids: NICE NG114 = Prednisolone 30mg OD 5 days. GOLD 2021 = 40mg OD 5 days. Use 40mg if weight ≥60kg or severe exacerbation. Antibiotics: indicated ONLY if change in sputum colour AND increased volume/thickness. Amoxicillin 500mg TDS 5 days first-line. Doxycycline 200mg OD 5 days if penicillin allergy. Quinolones NOT appropriate first-line in community. Smoking cessation: Niquitin patch 21mg→14mg→7mg. HSE COPD Communication Card + Self Care Plan provided. Inhaler technique checked. Vaccinations: flu yearly, pneumococcal every 5 years.",
                "questions": [
                    {"id": "copde_steroids", "type": "single_select", "label": "Steroid Therapy", "required": True, "options": ["Prednisolone 40mg PO OD for 5 days (GOLD / weight ≥60kg)", "Prednisolone 30mg PO OD for 5 days (NICE / weight <60kg)", "Not indicated"]},
                    {"id": "copde_antibiotic_indicated", "type": "toggle", "label": "Antibiotic Indicated? (Change in sputum colour + volume/thickness)", "required": True},
                    {"id": "copde_antibiotic", "type": "single_select", "label": "Antibiotic Choice", "required": False, "options": ["Amoxicillin 500mg TDS PO for 5 days", "Doxycycline 200mg PO OD for 5 days (penicillin allergy)", "Not indicated"]},
                    {"id": "copde_allergy", "type": "single_select", "label": "Allergy Status", "required": False, "options": ["No known allergies", "Penicillin allergy - use alternative"]},
                    {"id": "copde_vaccination_advice", "type": "toggle", "label": "Vaccination Importance Counselled?", "required": False},
                    {"id": "copde_resources", "type": "multi_select", "label": "Resources Provided", "required": False, "options": ["COPD Communication Card (HSE)", "COPD Self Care Plan (HSE)"]},
                    {"id": "copde_smoking_cessation", "type": "single_select", "label": "Smoking Cessation", "required": False, "options": ["Advice given", "Niquitin patch 21mg→14mg→7mg discussed", "Not applicable - non-smoker"]},
                    {"id": "copde_inhaler_technique", "type": "toggle", "label": "Inhaler Technique Reviewed/Checked?", "required": False},
                    {"id": "copde_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 48-72 hours, at end of course, admit if deteriorating"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_copd_exacerbation()