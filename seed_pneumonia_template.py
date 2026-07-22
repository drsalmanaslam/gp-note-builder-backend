from app.database import SessionLocal
from app.models import User, Template, Category

def seed_pneumonia_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    template_data = {
        "title": "Community Acquired Pneumonia Assessment",
        "description": "Assessment for suspected community acquired pneumonia including CURB-65 scoring, severity assessment, and management plan.",
        "category": "Respiratory",
        "content": {
            "sections": [
                {
                    "title": "Presenting Symptoms",
                    "questions": [
                        {"id": "cap_cough", "type": "single_select", "label": "Cough", "required": True, "options": ["Dry", "Productive - White/Clear", "Productive - Yellow/Green", "Productive - Rust Coloured", "Productive - Blood-stained"]},
                        {"id": "cap_breathlessness", "type": "single_select", "label": "Breathlessness", "required": True, "options": ["None", "Mild (on exertion)", "Moderate (on minimal exertion)", "Severe (at rest)"]},
                        {"id": "cap_pleuritic", "type": "toggle", "label": "Pleuritic Chest Pain?", "required": True},
                        {"id": "cap_fever", "type": "toggle", "label": "Fever/Rigors?", "required": True},
                        {"id": "cap_temp", "type": "number", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 38.5"},
                        {"id": "cap_duration", "type": "duration", "label": "Duration of Symptoms", "required": True, "units": ["days"]}
                    ]
                },
                {
                    "title": "CURB-65 Severity Score",
                    "red_flag_threshold": 2,
                    "questions": [
                        {"id": "cap_confusion", "type": "toggle", "label": "Confusion? (AMTS <8) (+1)", "required": True},
                        {"id": "cap_bun", "type": "toggle", "label": "Urea >7 mmol/L? (+1)", "required": False},
                        {"id": "cap_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 24"},
                        {"id": "cap_rr_high", "type": "toggle", "label": "RR ≥30/min? (+1)", "required": True},
                        {"id": "cap_bp_systolic", "type": "number", "label": "Systolic BP (mmHg)", "required": True, "placeholder": "e.g., 110"},
                        {"id": "cap_bp_low", "type": "toggle", "label": "SBP <90 or DBP ≤60? (+1)", "required": True},
                        {"id": "cap_age_65", "type": "toggle", "label": "Age ≥65? (+1)", "required": True},
                        {"id": "cap_curb_total", "type": "number", "label": "Total CURB-65 Score", "required": True, "placeholder": "0-5"},
                        {"id": "cap_severe", "type": "toggle", "label": "🔴 CURB-65 ≥3 or Severe Hypoxia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe pneumonia (CURB-65 ≥3). Urgent hospital admission required.", "red_flag_negative": "CURB-65 below threshold for admission."}
                    ]
                },
                {
                    "title": "Examination & Oxygenation",
                    "questions": [
                        {"id": "cap_o2_sats", "type": "number", "label": "Oxygen Saturations (%)", "required": True, "placeholder": "e.g., 92"},
                        {"id": "cap_hypoxia", "type": "toggle", "label": "🔴 SpO2 <92% on Air?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Significant hypoxia. Urgent admission and oxygen therapy required.", "red_flag_negative": "Oxygen saturations acceptable."},
                        {"id": "cap_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 100"},
                        {"id": "cap_chest_exam", "type": "textarea", "label": "Chest Examination Findings", "required": True, "placeholder": "e.g., Bronchial breathing, crackles left base, dullness to percussion..."},
                        {"id": "cap_consolidation", "type": "single_select", "label": "Signs of Consolidation?", "required": True, "options": ["None", "Unilateral", "Bilateral"]}
                    ]
                },
                {
                    "title": "Risk Factors & Comorbidities",
                    "questions": [
                        {"id": "cap_comorbidities", "type": "multi_select", "label": "Relevant Comorbidities", "required": False, "options": ["COPD", "Asthma", "Heart Failure", "Diabetes", "CKD", "Immunosuppression", "None"]},
                        {"id": "cap_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never", "Ex-Smoker", "Current Smoker"]},
                        {"id": "cap_alcohol", "type": "number", "label": "Alcohol Units/Week", "required": False},
                        {"id": "cap_immuno", "type": "toggle", "label": "Immunosuppressed? (Steroids/Chemo/Biologics)", "required": True}
                    ]
                },
                {
                    "title": "Investigations & Management",
                    "examination": "Full respiratory exam, oxygen saturations, BP, HR, RR, temperature, AMTS if indicated",
                    "safety_netting": "If breathing worsens, you develop confusion, or cannot speak in full sentences, seek urgent medical attention. Call 999 if lips turn blue or you become severely breathless at rest.",
                    "differentials": ["Community Acquired Pneumonia", "COVID-19 Pneumonitis", "Aspiration Pneumonia", "Pulmonary Embolism", "Lung Cancer", "Pulmonary Oedema"],
                    "questions": [
                        {"id": "cap_cxr", "type": "toggle", "label": "Chest X-ray Performed?", "required": False},
                        {"id": "cap_cxr_findings", "type": "textarea", "label": "CXR Findings", "required": False, "placeholder": "e.g., Left lower lobe consolidation..."},
                        {"id": "cap_bloods", "type": "toggle", "label": "Blood Tests Taken? (FBC, U&E, CRP)", "required": False},
                        {"id": "cap_crp", "type": "number", "label": "CRP (mg/L)", "required": False, "placeholder": "e.g., 85"},
                        {"id": "cap_wcc", "type": "number", "label": "White Cell Count", "required": False},
                        {"id": "cap_antibiotics", "type": "textarea", "label": "Antibiotic Prescribed", "required": True, "placeholder": "e.g., Amoxicillin 500mg TDS for 5 days (or Doxycycline if penicillin allergic)"},
                        {"id": "cap_management", "type": "single_select", "label": "Management Decision", "required": True, "options": ["Community Management (CURB-65 0-1)", "Community with Close Follow-up (CURB-65 2)", "Hospital Admission (CURB-65 ≥3)", "ICU Consideration"]},
                        {"id": "cap_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["days", "weeks"]},
                        {"id": "cap_notes", "type": "textarea", "label": "Additional Notes", "required": False}
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_pneumonia_template()