from app.database import SessionLocal
from app.models import User, Template, Category

def seed_heartfailure_template():
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
        "title": "Heart Failure Annual Review",
        "description": "Annual heart failure review including NYHA class, echocardiogram, medication optimisation, and QOF indicators.",
        "category": "Cardiovascular",
        "content": {
            "sections": [
                {
                    "title": "Clinical Status & NYHA Class",
                    "questions": [
                        {"id": "hf_nyha_class", "type": "single_select", "label": "NYHA Classification", "required": True, "options": ["Class I: No limitation", "Class II: Slight limitation", "Class III: Marked limitation", "Class IV: Symptoms at rest"], "output_phrase": "NYHA Class: {value}"},
                        {"id": "hf_breathlessness", "type": "single_select", "label": "Breathlessness Severity", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "hf_orthopnoea", "type": "toggle", "label": "Orthopnoea Present?", "required": True},
                        {"id": "hf_pnd", "type": "toggle", "label": "Paroxysmal Nocturnal Dyspnoea?", "required": True},
                        {"id": "hf_oedema", "type": "single_select", "label": "Peripheral Oedema", "required": True, "options": ["None", "Ankle only", "Below knee", "Above knee"]}
                    ]
                },
                {
                    "title": "Investigations",
                    "questions": [
                        {"id": "hf_echo_date", "type": "date", "label": "Last Echocardiogram Date", "required": False},
                        {"id": "hf_ef", "type": "number", "label": "Ejection Fraction (%)", "required": True, "placeholder": "e.g., 35"},
                        {"id": "hf_type", "type": "single_select", "label": "Heart Failure Type", "required": True, "options": ["HFrEF (EF ≤40%)", "HFmrEF (EF 41-49%)", "HFpEF (EF ≥50%)"]},
                        {"id": "hf_bnp", "type": "number", "label": "BNP/NT-proBNP", "required": False, "placeholder": "e.g., 450"},
                        {"id": "hf_egfr", "type": "number", "label": "eGFR (ml/min)", "required": True, "placeholder": "e.g., 50"},
                        {"id": "hf_potassium", "type": "number", "label": "Potassium (mmol/L)", "required": True, "placeholder": "e.g., 4.5"}
                    ]
                },
                {
                    "title": "Medication Optimisation (QOF)",
                    "questions": [
                        {"id": "hf_acei_arb_arni", "type": "toggle", "label": "On ACEi/ARB/ARNI? (QOF indicator)", "required": True, "output_phrase": "ACEi/ARB/ARNI: {value}"},
                        {"id": "hf_betablocker", "type": "toggle", "label": "On Beta-Blocker? (QOF indicator)", "required": True, "output_phrase": "Beta-Blocker: {value}"},
                        {"id": "hf_mra", "type": "toggle", "label": "On MRA (Spironolactone/Eplerenone)?", "required": False, "output_phrase": "MRA: {value}"},
                        {"id": "hf_sglt2", "type": "toggle", "label": "On SGLT2 Inhibitor?", "required": False},
                        {"id": "hf_diuretics", "type": "text", "label": "Diuretic Regime & Dose", "required": True, "placeholder": "e.g., Furosemide 40mg OD"},
                        {"id": "hf_dose_optimised", "type": "toggle", "label": "Medications at Optimal/Target Doses?", "required": True},
                        {"id": "hf_deterioration", "type": "toggle", "label": "🔴 Clinical Deterioration Despite Optimal Therapy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Clinical deterioration despite optimal therapy. Urgent cardiology review required.", "red_flag_negative": "Patient stable on current therapy."}
                    ]
                },
                {
                    "title": "Lifestyle & Self-Management",
                    "questions": [
                        {"id": "hf_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 75"},
                        {"id": "hf_weight_change", "type": "number", "label": "Weight Change Since Last Review (kg)", "required": False, "placeholder": "e.g., +2"},
                        {"id": "hf_daily_weights", "type": "toggle", "label": "Patient Monitoring Daily Weights?", "required": True},
                        {"id": "hf_fluid_restriction", "type": "toggle", "label": "Fluid Restriction Advised?", "required": False},
                        {"id": "hf_salt_restriction", "type": "toggle", "label": "Salt Restriction Advised?", "required": True},
                        {"id": "hf_alcohol", "type": "number", "label": "Alcohol Units per Week", "required": False},
                        {"id": "hf_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never Smoked", "Ex-Smoker", "Current Smoker"]}
                    ]
                },
                {
                    "title": "Plan & Follow-up",
                    "examination": "JVP assessment, chest auscultation, peripheral oedema check, BP, heart rate, oxygen saturations",
                    "safety_netting": "If you experience sudden worsening of breathlessness, chest pain, or rapid weight gain (>2kg in 2 days), seek urgent medical attention. Call 999 if you cannot breathe when sitting up.",
                    "questions": [
                        {"id": "hf_flu_vaccine", "type": "toggle", "label": "Flu Vaccine Given?", "required": True},
                        {"id": "hf_pneumo_vaccine", "type": "toggle", "label": "Pneumococcal Vaccine Given?", "required": True},
                        {"id": "hf_cardiac_rehab", "type": "toggle", "label": "Cardiac Rehabilitation Offered?", "required": False},
                        {"id": "hf_palliative", "type": "toggle", "label": "Palliative Care/DNACPR Discussion Appropriate?", "required": False},
                        {"id": "hf_followup", "type": "duration", "label": "Follow-up Interval", "required": True, "units": ["weeks", "months"]},
                        {"id": "hf_review_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    seed_heartfailure_template()