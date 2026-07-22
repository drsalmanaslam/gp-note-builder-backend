from app.database import SessionLocal
from app.models import User, Template, Category

def seed_asthma_template():
    db = SessionLocal()

    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Admin user not found.")
        db.close()
        return

    category_name = "Respiratory"
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    template_data = {
        "title": "Asthma Annual Review",
        "description": "Annual asthma review including symptom control, inhaler technique, exacerbation history, and QOF indicators.",
        "category": "Respiratory",
        "content": {
            "sections": [
                {
                    "title": "Asthma Control Assessment",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "asthma_day_symptoms", "type": "slider", "label": "Daytime symptoms (days per week)", "required": True, "min": 0, "max": 7, "output_phrase": "Daytime symptoms: {value} days/week"},
                        {"id": "asthma_night_symptoms", "type": "slider", "label": "Night-time symptoms (nights per week)", "required": True, "min": 0, "max": 7, "output_phrase": "Night-time symptoms: {value} nights/week"},
                        {"id": "asthma_reliever_use", "type": "slider", "label": "Reliever inhaler use (times per week)", "required": True, "min": 0, "max": 28, "output_phrase": "Reliever use: {value} times/week"},
                        {"id": "asthma_activity_limit", "type": "single_select", "label": "Activity Limitation", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "asthma_control_level", "type": "single_select", "label": "Overall Control Level", "required": True, "options": ["Well Controlled", "Partially Controlled", "Uncontrolled"]}
                    ]
                },
                {
                    "title": "Objective Measurements",
                    "questions": [
                        {"id": "asthma_peak_flow", "type": "number", "label": "Peak Flow (L/min)", "required": True, "placeholder": "e.g., 400", "output_phrase": "Peak Flow: {value} L/min"},
                        {"id": "asthma_peak_flow_predicted", "type": "number", "label": "Predicted Peak Flow (L/min)", "required": False, "placeholder": "e.g., 500"},
                        {"id": "asthma_feNO", "type": "number", "label": "FeNO (ppb) - if available", "required": False, "placeholder": "e.g., 35"},
                        {"id": "asthma_spirometry", "type": "toggle", "label": "Spirometry Performed?", "required": False},
                        {"id": "asthma_fev1", "type": "number", "label": "FEV1 (L) - if performed", "required": False, "placeholder": "e.g., 3.2"}
                    ]
                },
                {
                    "title": "Inhaler Technique & Adherence",
                    "questions": [
                        {"id": "asthma_inhaler_technique", "type": "single_select", "label": "Inhaler Technique", "required": True, "options": ["Good", "Adequate", "Poor - Needs Education"]},
                        {"id": "asthma_inhaler_type", "type": "textarea", "label": "Current Inhalers", "required": True, "placeholder": "e.g., Clenil Modulite 200mcg BD, Salbutamol PRN..."},
                        {"id": "asthma_adherence", "type": "single_select", "label": "Medication Adherence", "required": True, "options": ["Taking as prescribed", "Occasional missed doses", "Frequent missed doses", "Not taking"]},
                        {"id": "asthma_spacer", "type": "toggle", "label": "Using Spacer Device?", "required": False}
                    ]
                },
                {
                    "title": "Exacerbation History",
                    "red_flag_threshold": 2,
                    "questions": [
                        {"id": "asthma_exacerbations_year", "type": "number", "label": "Exacerbations in Past 12 Months", "required": True, "placeholder": "e.g., 2"},
                        {"id": "asthma_ocs_courses", "type": "number", "label": "Oral Corticosteroid Courses in Past 12 Months", "required": True, "placeholder": "e.g., 1"},
                        {"id": "asthma_hospital_admissions", "type": "toggle", "label": "Hospital Admission for Asthma?", "required": True},
                        {"id": "asthma_itu", "type": "toggle", "label": "🔴 ITU Admission Ever? (High Risk)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous ITU admission for asthma. High-risk patient. Ensure specialist follow-up and personalised asthma action plan.", "red_flag_negative": "No ITU admission history."},
                        {"id": "asthma_severe", "type": "toggle", "label": "🔴 Frequent exacerbations (≥2 OCS courses/year)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Frequent exacerbations requiring OCS. Consider step-up therapy and specialist referral.", "red_flag_negative": "Exacerbation frequency within acceptable range."}
                    ]
                },
                {
                    "title": "Triggers & Lifestyle",
                    "questions": [
                        {"id": "asthma_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never Smoked", "Ex-Smoker", "Current Smoker"]},
                        {"id": "asthma_allergens", "type": "multi_select", "label": "Known Triggers", "required": False, "options": ["Pollen", "Dust Mites", "Pet Dander", "Cold Air", "Exercise", "Stress", "Smoke", "Perfume"]},
                        {"id": "asthma_occupational", "type": "toggle", "label": "Occupational Asthma Suspected?", "required": False}
                    ]
                },
                {
                    "title": "Action Plan & Follow-up",
                    "examination": "Chest auscultation, peak flow measurement, inhaler technique check, BMI, oxygen saturations if indicated",
                    "safety_netting": "If symptoms worsen rapidly, use your reliever inhaler and seek urgent medical attention. If you cannot speak in full sentences or your lips turn blue, call 999 immediately.",
                    "questions": [
                        {"id": "asthma_action_plan", "type": "toggle", "label": "Personalised Asthma Action Plan Provided?", "required": True, "output_phrase": "Action Plan: {value}"},
                        {"id": "asthma_step_therapy", "type": "single_select", "label": "Current BTS/SIGN Step", "required": True, "options": ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"]},
                        {"id": "asthma_followup", "type": "duration", "label": "Follow-up Interval", "required": True, "units": ["weeks", "months"]},
                        {"id": "asthma_review_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    seed_asthma_template()