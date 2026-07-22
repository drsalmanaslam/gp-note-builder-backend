from app.database import SessionLocal
from app.models import User, Template, Category

def seed_af_template():
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
        "title": "Atrial Fibrillation Annual Review",
        "description": "Annual AF review including CHA₂DS₂-VASc score, anticoagulation, rate/rhythm control, and QOF indicators.",
        "category": "Cardiovascular",
        "content": {
            "sections": [
                {
                    "title": "AF Status & Symptoms",
                    "questions": [
                        {"id": "af_type", "type": "single_select", "label": "AF Type", "required": True, "options": ["Paroxysmal", "Persistent", "Permanent", "Long-standing Persistent"]},
                        {"id": "af_diagnosis_date", "type": "date", "label": "Date of Diagnosis", "required": False},
                        {"id": "af_symptoms", "type": "multi_select", "label": "Current Symptoms", "required": True, "options": ["Palpitations", "Shortness of Breath", "Fatigue", "Dizziness", "Chest Pain", "None"]},
                        {"id": "af_ehra_score", "type": "single_select", "label": "EHRA Symptom Score", "required": True, "options": ["I: No symptoms", "IIa: Mild, normal daily activity unaffected", "IIb: Moderate, normal daily activity not affected but bothered", "III: Severe, normal daily activity affected", "IV: Disabling, normal daily activity discontinued"]}
                    ]
                },
                {
                    "title": "Stroke Risk - CHA₂DS₂-VASc Score",
                    "questions": [
                        {"id": "af_chf", "type": "toggle", "label": "Congestive Heart Failure? (+1)", "required": True},
                        {"id": "af_hypertension", "type": "toggle", "label": "Hypertension? (+1)", "required": True},
                        {"id": "af_age_75", "type": "toggle", "label": "Age ≥75? (+2)", "required": True},
                        {"id": "af_age_65", "type": "toggle", "label": "Age 65-74? (+1)", "required": True},
                        {"id": "af_diabetes", "type": "toggle", "label": "Diabetes? (+1)", "required": True},
                        {"id": "af_stroke_prev", "type": "toggle", "label": "Previous Stroke/TIA/Thromboembolism? (+2)", "required": True},
                        {"id": "af_vascular_disease", "type": "toggle", "label": "Vascular Disease? (+1)", "required": True},
                        {"id": "af_female", "type": "toggle", "label": "Female Sex? (+1)", "required": True},
                        {"id": "af_chads_vasc_total", "type": "number", "label": "Total CHA₂DS₂-VASc Score", "required": True, "placeholder": "e.g., 3", "output_phrase": "CHA₂DS₂-VASc Score: {value}"}
                    ]
                },
                {
                    "title": "Bleeding Risk - ORBIT Score & Anticoagulation",
                    "questions": [
                        {"id": "af_anticoagulation", "type": "single_select", "label": "Current Anticoagulation", "required": True, "options": ["DOAC (Apixaban, Rivaroxaban, Edoxaban)", "Warfarin", "Dabigatran", "None", "Aspirin Only"], "output_phrase": "Anticoagulation: {value}"},
                        {"id": "af_anticoag_contra", "type": "toggle", "label": "Contraindication to Anticoagulation?", "required": True},
                        {"id": "af_anticoag_indicated", "type": "toggle", "label": "🔴 CHA₂DS₂-VASc ≥2 and Not Anticoagulated? (QOF)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Patient at high stroke risk without appropriate anticoagulation. Discuss risks and benefits urgently.", "red_flag_negative": "Anticoagulation status appropriate for stroke risk."},
                        {"id": "af_inr", "type": "number", "label": "INR (if on Warfarin)", "required": False, "placeholder": "e.g., 2.5"},
                        {"id": "af_tir", "type": "number", "label": "Time in Therapeutic Range - TTR (%)", "required": False, "placeholder": "e.g., 68"}
                    ]
                },
                {
                    "title": "Rate/Rhythm Control",
                    "questions": [
                        {"id": "af_rate_control", "type": "textarea", "label": "Rate Control Medications", "required": True, "placeholder": "e.g., Bisoprolol 5mg OD, Digoxin 125mcg OD..."},
                        {"id": "af_heart_rate", "type": "number", "label": "Resting Heart Rate (bpm)", "required": True, "placeholder": "e.g., 75"},
                        {"id": "af_rate_controlled", "type": "toggle", "label": "Rate Controlled? (Resting HR <80)", "required": True},
                        {"id": "af_rhythm_control", "type": "toggle", "label": "On Rhythm Control Strategy?", "required": False},
                        {"id": "af_cardioversion", "type": "toggle", "label": "Previous Cardioversion?", "required": False},
                        {"id": "af_ablation", "type": "toggle", "label": "Previous Ablation?", "required": False}
                    ]
                },
                {
                    "title": "Lifestyle & Follow-up",
                    "examination": "Heart rate (apical and radial), BP, heart sounds, signs of heart failure",
                    "safety_netting": "If you experience sudden severe palpitations, chest pain, fainting, or stroke symptoms (facial droop, arm weakness, speech difficulty), call 999 immediately.",
                    "questions": [
                        {"id": "af_alcohol", "type": "number", "label": "Alcohol Units per Week", "required": True, "placeholder": "e.g., 8"},
                        {"id": "af_alcohol_advice", "type": "toggle", "label": "Alcohol Reduction Advised?", "required": False},
                        {"id": "af_weight", "type": "number", "label": "Weight (kg)", "required": False},
                        {"id": "af_exercise", "type": "single_select", "label": "Exercise Level", "required": True, "options": ["Regular", "Some Activity", "Sedentary"]},
                        {"id": "af_followup", "type": "duration", "label": "Follow-up Interval", "required": True, "units": ["weeks", "months"]},
                        {"id": "af_review_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    seed_af_template()