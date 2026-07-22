from app.database import SessionLocal
from app.models import User, Template, Category

def seed_ckd_template():
    db = SessionLocal()

    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Admin user not found.")
        db.close()
        return

    category_name = "Urology"
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    template_data = {
        "title": "CKD Annual Review",
        "description": "Annual chronic kidney disease review including eGFR staging, proteinuria, BP control, medication review, and QOF indicators.",
        "category": "Urology",
        "content": {
            "sections": [
                {
                    "title": "CKD Staging & Monitoring",
                    "questions": [
                        {"id": "ckd_egfr", "type": "number", "label": "eGFR (ml/min/1.73m²)", "required": True, "placeholder": "e.g., 42"},
                        {"id": "ckd_stage", "type": "single_select", "label": "CKD Stage", "required": True, "options": ["Stage 1 (eGFR ≥90 + proteinuria)", "Stage 2 (eGFR 60-89 + proteinuria)", "Stage 3a (eGFR 45-59)", "Stage 3b (eGFR 30-44)", "Stage 4 (eGFR 15-29)", "Stage 5 (eGFR <15)"], "output_phrase": "CKD Stage: {value}"},
                        {"id": "ckd_acr", "type": "number", "label": "Urine ACR (mg/mmol)", "required": True, "placeholder": "e.g., 15"},
                        {"id": "ckd_acr_category", "type": "single_select", "label": "ACR Category", "required": True, "options": ["A1 (<3)", "A2 (3-30)", "A3 (>30)"]},
                        {"id": "ckd_proteinuria_high", "type": "toggle", "label": "🔴 ACR >70 or PCR >100?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Heavy proteinuria. Nephrology referral indicated.", "red_flag_negative": "Proteinuria below referral threshold."}
                    ]
                },
                {
                    "title": "Blood Pressure & Cardiovascular Risk",
                    "questions": [
                        {"id": "ckd_bp_systolic", "type": "number", "label": "Systolic BP (mmHg)", "required": True, "placeholder": "e.g., 130"},
                        {"id": "ckd_bp_diastolic", "type": "number", "label": "Diastolic BP (mmHg)", "required": True, "placeholder": "e.g., 80"},
                        {"id": "ckd_bp_target", "type": "single_select", "label": "BP Target Met? (≤130/80 for CKD with proteinuria)", "required": True, "options": ["Target Met", "Above Target"]},
                        {"id": "ckd_cholesterol", "type": "number", "label": "Total Cholesterol (mmol/L)", "required": False},
                        {"id": "ckd_cardiovascular_risk", "type": "single_select", "label": "CV Risk Assessment", "required": True, "options": ["Low Risk", "Moderate Risk", "High Risk", "Very High Risk"]}
                    ]
                },
                {
                    "title": "Complications & Anaemia",
                    "questions": [
                        {"id": "ckd_hb", "type": "number", "label": "Haemoglobin (g/L)", "required": True, "placeholder": "e.g., 120"},
                        {"id": "ckd_anaemia", "type": "toggle", "label": "Anaemia Present? (Hb <110)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Renal anaemia detected. Check iron studies, B12, folate. Consider ESA therapy.", "red_flag_negative": "Hb within acceptable range."},
                        {"id": "ckd_potassium", "type": "number", "label": "Potassium (mmol/L)", "required": True, "placeholder": "e.g., 4.8"},
                        {"id": "ckd_hyperkalemia", "type": "toggle", "label": "🔴 K+ >6.0? (Hyperkalaemia)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hyperkalaemia (K+ >6.0). Urgent management required. Review medications.", "red_flag_negative": "Potassium within safe range."},
                        {"id": "ckd_phosphate", "type": "number", "label": "Phosphate (mmol/L)", "required": False, "placeholder": "e.g., 1.2"},
                        {"id": "ckd_pth", "type": "number", "label": "PTH (pmol/L)", "required": False, "placeholder": "e.g., 8.5"}
                    ]
                },
                {
                    "title": "Medication Review",
                    "questions": [
                        {"id": "ckd_medication_current", "type": "textarea", "label": "Current Medications (including OTC)", "required": True, "placeholder": "e.g., Ramipril 5mg, Atorvastatin 20mg..."},
                        {"id": "ckd_acei_arb", "type": "toggle", "label": "On ACEi/ARB? (QOF indicator)", "required": True, "output_phrase": "ACEi/ARB: {value}"},
                        {"id": "ckd_nephrotoxic", "type": "toggle", "label": "🔴 Taking Nephrotoxic Medications? (NSAIDs, Lithium, etc.)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Patient taking potentially nephrotoxic medications. Advise to stop NSAIDs and review.", "red_flag_negative": "No nephrotoxic medications identified."},
                        {"id": "ckd_medication_contra", "type": "toggle", "label": "Any Contraindicated Medications for eGFR?", "required": True}
                    ]
                },
                {
                    "title": "Nephrology Referral & Plan",
                    "examination": "BP measurement, cardiovascular exam, fluid status assessment, abdominal exam for renal masses",
                    "safety_netting": "If you experience reduced urine output, severe swelling, confusion, or nausea/vomiting, seek urgent medical attention. Attend A&E if symptoms are severe.",
                    "questions": [
                        {"id": "ckd_referral_criteria", "type": "toggle", "label": "Meets Nephrology Referral Criteria? (eGFR <30, rapid decline, ACR >70)", "required": True},
                        {"id": "ckd_renal_ultrasound", "type": "toggle", "label": "Renal Ultrasound Performed?", "required": False},
                        {"id": "ckd_egfr_decline", "type": "number", "label": "eGFR Decline Over 12 Months (ml/min)", "required": False, "placeholder": "e.g., 5"},
                        {"id": "ckd_dietary_advice", "type": "toggle", "label": "Dietary Advice Given? (salt, protein, potassium)", "required": False},
                        {"id": "ckd_followup", "type": "duration", "label": "Follow-up Interval", "required": True, "units": ["weeks", "months"]},
                        {"id": "ckd_review_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    print(f"Template '{template_data['title']}' created! Sections: {len(template_data['content']['sections'])}")
    db.close()

if __name__ == "__main__":
    seed_ckd_template()