from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hypertension_template():
    db = SessionLocal()

    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Admin user not found. Please create admin first.")
        db.close()
        return

    category_name = "Cardiovascular"
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    template_data = {
        "title": "Hypertension Annual Review",
        "description": "Annual review for patients with hypertension. Includes QOF targets, medication review, and cardiovascular risk assessment.",
        "category": "Cardiovascular",
        "content": {
            "sections": [
                {
                    "title": "Patient Information",
                    "questions": [
                        {"id": "htn_review_type", "type": "select", "label": "Review Type", "required": True, "options": ["Annual Review", "New Diagnosis", "Post-Treatment Check", "Uncontrolled BP Follow-up"]},
                        {"id": "htn_diagnosis_date", "type": "date", "label": "Date of Diagnosis", "required": False}
                    ]
                },
                {
                    "title": "Blood Pressure Readings",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "htn_bp_systolic", "type": "number", "label": "Systolic BP (mmHg)", "required": True, "placeholder": "e.g., 140", "output_phrase": "BP: {value}/"},
                        {"id": "htn_bp_diastolic", "type": "number", "label": "Diastolic BP (mmHg)", "required": True, "placeholder": "e.g., 90", "output_phrase": "{value} mmHg"},
                        {"id": "htn_bp_target", "type": "single_select", "label": "BP Target Met? (QOF: ≤140/90, or ≤130/80 if diabetes/CKD)", "required": True, "options": ["Target Met (≤140/90)", "Target Met (≤130/80)", "Above Target", "Not Recorded"]},
                        {"id": "htn_severe", "type": "toggle", "label": "🔴 BP ≥180/120? (Severe Hypertension)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe hypertension (≥180/120). Urgent assessment and management required.", "red_flag_negative": "BP below severe hypertension threshold."},
                        {"id": "htn_postural", "type": "toggle", "label": "Postural Hypotension Checked?", "required": False, "output_phrase": "Postural BP: {value}"},
                        {"id": "htn_pulse", "type": "number", "label": "Pulse Rate (bpm)", "required": True, "placeholder": "e.g., 72"}
                    ]
                },
                {
                    "title": "Cardiovascular Risk Assessment",
                    "questions": [
                        {"id": "htn_cholesterol", "type": "number", "label": "Total Cholesterol (mmol/L)", "required": True, "placeholder": "e.g., 5.2"},
                        {"id": "htn_hdl", "type": "number", "label": "HDL Cholesterol (mmol/L)", "required": False, "placeholder": "e.g., 1.2"},
                        {"id": "htn_qrisk", "type": "number", "label": "QRISK3 Score (%)", "required": False, "placeholder": "e.g., 15"},
                        {"id": "htn_egfr", "type": "number", "label": "eGFR (ml/min/1.73m²)", "required": True, "placeholder": "e.g., 70"},
                        {"id": "htn_ecg", "type": "toggle", "label": "ECG Performed?", "required": False, "output_phrase": "ECG: {value}"},
                        {"id": "htn_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never Smoked", "Ex-Smoker", "Current Smoker"]},
                        {"id": "htn_alcohol", "type": "number", "label": "Alcohol Units per Week", "required": False, "placeholder": "e.g., 10"}
                    ]
                },
                {
                    "title": "End Organ Damage Screening",
                    "questions": [
                        {"id": "htn_lvh", "type": "toggle", "label": "Left Ventricular Hypertrophy?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Evidence of LVH. Tight BP control essential. Consider cardiology referral.", "red_flag_negative": "No evidence of LVH."},
                        {"id": "htn_retinopathy", "type": "toggle", "label": "Hypertensive Retinopathy?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypertensive retinopathy present. Urgent ophthalmology referral.", "red_flag_negative": "No hypertensive retinopathy."},
                        {"id": "htn_proteinuria", "type": "toggle", "label": "Proteinuria Present?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Proteinuria detected. Monitor renal function closely.", "red_flag_negative": "No significant proteinuria."}
                    ]
                },
                {
                    "title": "Medication Review",
                    "questions": [
                        {"id": "htn_medication_current", "type": "textarea", "label": "Current Antihypertensives", "required": True, "placeholder": "e.g., Ramipril 5mg OD, Amlodipine 5mg OD..."},
                        {"id": "htn_medication_adherence", "type": "single_select", "label": "Medication Adherence", "required": True, "options": ["Taking as prescribed", "Occasional missed doses", "Frequent missed doses", "Not taking"]},
                        {"id": "htn_side_effects", "type": "textarea", "label": "Side Effects Reported", "required": False, "placeholder": "e.g., Dry cough with ACE inhibitor..."},
                        {"id": "htn_medication_changes", "type": "textarea", "label": "Medication Changes Made Today", "required": False}
                    ]
                },
                {
                    "title": "Lifestyle & Plan",
                    "examination": "BP measurement (both arms initially), pulse check, BMI, cardiovascular exam, fundoscopy if indicated",
                    "safety_netting": "If you experience severe headache, chest pain, visual disturbance, or shortness of breath, seek urgent medical attention. Call 999 if symptoms are severe.",
                    "questions": [
                        {"id": "htn_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 29"},
                        {"id": "htn_exercise", "type": "single_select", "label": "Exercise Level", "required": True, "options": ["Regular (≥150 min/week)", "Some Activity", "Sedentary"]},
                        {"id": "htn_diet_salt", "type": "toggle", "label": "Dietary Salt Reduction Advised?", "required": False},
                        {"id": "htn_followup", "type": "duration", "label": "Follow-up Interval", "required": True, "units": ["weeks", "months"]},
                        {"id": "htn_review_notes", "type": "textarea", "label": "Additional Notes", "required": False}
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing:
        db.delete(existing)
        db.commit()

    new_template = Template(
        title=template_data["title"], description=template_data["description"],
        category=template_data["category"], content=template_data["content"],
        is_public=template_data["is_public"], created_by=admin.id, version=1
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    print(f"Template '{template_data['title']}' created! Sections: {len(template_data['content']['sections'])}")
    db.close()

if __name__ == "__main__":
    seed_hypertension_template()