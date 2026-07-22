from app.database import SessionLocal
from app.models import User, Template, Category

def seed_ihd_template():
    db = SessionLocal()

    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Admin user not found.")
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
        "title": "IHD Annual Review",
        "description": "Annual ischaemic heart disease review including symptoms, risk factors, medication optimisation, and QOF indicators.",
        "category": "Cardiovascular",
        "content": {
            "sections": [
                {
                    "title": "IHD Status & Symptoms",
                    "questions": [
                        {"id": "ihd_type", "type": "multi_select", "label": "IHD Manifestations", "required": True, "options": ["Stable Angina", "Previous MI", "PCI/Stent", "CABG", "Silent Ischaemia"]},
                        {"id": "ihd_angina_frequency", "type": "single_select", "label": "Angina Frequency", "required": True, "options": ["None", "Monthly", "Weekly", "Daily"]},
                        {"id": "ihd_ccs_class", "type": "single_select", "label": "CCS Angina Class", "required": False, "options": ["Class I: Strenuous exertion", "Class II: Moderate exertion", "Class III: Mild exertion", "Class IV: At rest"]},
                        {"id": "ihd_unstable", "type": "toggle", "label": "🔴 Unstable Angina Symptoms? (New/worsening/at rest)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unstable angina symptoms. Urgent cardiology assessment required. Consider admission.", "red_flag_negative": "Stable angina pattern."}
                    ]
                },
                {
                    "title": "Risk Factor Management (QOF)",
                    "questions": [
                        {"id": "ihd_bp_systolic", "type": "number", "label": "Systolic BP (mmHg)", "required": True, "placeholder": "e.g., 130"},
                        {"id": "ihd_bp_diastolic", "type": "number", "label": "Diastolic BP (mmHg)", "required": True, "placeholder": "e.g., 80"},
                        {"id": "ihd_bp_target", "type": "single_select", "label": "BP Target Met? (≤140/90)", "required": True, "options": ["Target Met", "Above Target"]},
                        {"id": "ihd_cholesterol", "type": "number", "label": "Total Cholesterol (mmol/L)", "required": True, "placeholder": "e.g., 4.0"},
                        {"id": "ihd_ldl", "type": "number", "label": "LDL Cholesterol (mmol/L)", "required": False, "placeholder": "e.g., 2.0"},
                        {"id": "ihd_chol_target", "type": "single_select", "label": "Cholesterol Target Met? (≤5.0, or ≤4.0 if post-MI)", "required": True, "options": ["Target Met", "Above Target"]},
                        {"id": "ihd_hba1c", "type": "number", "label": "HbA1c (if diabetic) - mmol/mol", "required": False, "placeholder": "e.g., 48"},
                        {"id": "ihd_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never Smoked", "Ex-Smoker", "Current Smoker"]},
                        {"id": "ihd_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 28"}
                    ]
                },
                {
                    "title": "Medication Review (QOF)",
                    "questions": [
                        {"id": "ihd_antiplatelet", "type": "toggle", "label": "On Antiplatelet? (Aspirin/Clopidogrel) - QOF", "required": True, "output_phrase": "Antiplatelet: {value}"},
                        {"id": "ihd_statin", "type": "toggle", "label": "On Statin? - QOF", "required": True, "output_phrase": "Statin: {value}"},
                        {"id": "ihd_betablocker", "type": "toggle", "label": "On Beta-Blocker? (post-MI)", "required": False, "output_phrase": "Beta-Blocker: {value}"},
                        {"id": "ihd_acei_arb", "type": "toggle", "label": "On ACEi/ARB?", "required": False, "output_phrase": "ACEi/ARB: {value}"},
                        {"id": "ihd_gtn", "type": "toggle", "label": "GTN Prescribed?", "required": False},
                        {"id": "ihd_medication_current", "type": "textarea", "label": "All Current Cardiovascular Medications", "required": True, "placeholder": "e.g., Aspirin 75mg, Atorvastatin 80mg, Bisoprolol 5mg..."},
                        {"id": "ihd_medication_side_effects", "type": "textarea", "label": "Side Effects Reported", "required": False}
                    ]
                },
                {
                    "title": "Lifestyle & Cardiac Rehab",
                    "questions": [
                        {"id": "ihd_exercise", "type": "single_select", "label": "Exercise Level", "required": True, "options": ["Regular (≥150 min/week)", "Some Activity", "Sedentary"]},
                        {"id": "ihd_cardiac_rehab", "type": "toggle", "label": "Cardiac Rehabilitation Completed?", "required": False},
                        {"id": "ihd_diet", "type": "toggle", "label": "Mediterranean Diet Advised?", "required": True},
                        {"id": "ihd_alcohol", "type": "number", "label": "Alcohol Units per Week", "required": False, "placeholder": "e.g., 6"},
                        {"id": "ihd_stress", "type": "single_select", "label": "Stress/Anxiety Level", "required": False, "options": ["Well Managed", "Moderate", "Significant - Affecting Daily Life"]}
                    ]
                },
                {
                    "title": "Plan & Follow-up",
                    "examination": "Heart rate, BP, heart sounds, peripheral pulses, signs of heart failure, BMI",
                    "safety_netting": "If you experience central chest pain lasting more than 15 minutes not relieved by GTN, call 999 immediately. If symptoms worsen or new symptoms develop, seek urgent medical review.",
                    "questions": [
                        {"id": "ihd_flu_vaccine", "type": "toggle", "label": "Flu Vaccine Given?", "required": True},
                        {"id": "ihd_pneumo_vaccine", "type": "toggle", "label": "Pneumococcal Vaccine Given?", "required": False},
                        {"id": "ihd_annual_review", "type": "toggle", "label": "Full Annual Review Completed?", "required": True},
                        {"id": "ihd_followup", "type": "duration", "label": "Follow-up Interval", "required": True, "units": ["weeks", "months"]},
                        {"id": "ihd_review_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    seed_ihd_template()