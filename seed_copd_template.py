from app.database import SessionLocal
from app.models import User, Template, Category

def seed_copd_template():
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
        "title": "COPD Annual Review",
        "description": "Annual COPD review including MRC dyspnoea score, exacerbation history, spirometry, medication review, and QOF indicators.",
        "category": "Respiratory",
        "content": {
            "sections": [
                {
                    "title": "Symptoms & MRC Dyspnoea Score",
                    "questions": [
                        {"id": "copd_mrc_score", "type": "single_select", "label": "MRC Dyspnoea Score", "required": True, "options": ["Grade 1: Breathless on strenuous exercise", "Grade 2: Short of breath hurrying or walking uphill", "Grade 3: Walks slower or stops for breath", "Grade 4: Stops after 100m or few minutes", "Grade 5: Too breathless to leave house"], "output_phrase": "MRC Score: {value}"},
                        {"id": "copd_cough", "type": "single_select", "label": "Cough Severity", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "copd_sputum", "type": "single_select", "label": "Sputum Production", "required": True, "options": ["None", "White/Clear", "Yellow/Green", "Blood-stained"]},
                        {"id": "copd_haemoptysis", "type": "toggle", "label": "🔴 Haemoptysis Present?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemoptysis reported. Urgent CXR and consideration of 2-week wait referral required.", "red_flag_negative": "No haemoptysis reported."}
                    ]
                },
                {
                    "title": "Objective Measurements",
                    "questions": [
                        {"id": "copd_fev1", "type": "number", "label": "FEV1 (L)", "required": True, "placeholder": "e.g., 1.5"},
                        {"id": "copd_fev1_percent", "type": "number", "label": "FEV1 (% Predicted)", "required": True, "placeholder": "e.g., 55"},
                        {"id": "copd_fvc", "type": "number", "label": "FVC (L)", "required": False, "placeholder": "e.g., 2.8"},
                        {"id": "copd_ratio", "type": "number", "label": "FEV1/FVC Ratio", "required": False, "placeholder": "e.g., 0.54"},
                        {"id": "copd_severity", "type": "single_select", "label": "COPD Severity (GOLD)", "required": True, "options": ["GOLD 1 (Mild, FEV1 ≥80%)", "GOLD 2 (Moderate, FEV1 50-79%)", "GOLD 3 (Severe, FEV1 30-49%)", "GOLD 4 (Very Severe, FEV1 <30%)"]},
                        {"id": "copd_o2_sats", "type": "number", "label": "Oxygen Saturations (%)", "required": True, "placeholder": "e.g., 94"},
                        {"id": "copd_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 24"}
                    ]
                },
                {
                    "title": "Exacerbation History",
                    "red_flag_threshold": 3,
                    "questions": [
                        {"id": "copd_exacerbations_year", "type": "number", "label": "Exacerbations in Past 12 Months", "required": True, "placeholder": "e.g., 3"},
                        {"id": "copd_hospital_admissions", "type": "number", "label": "Hospital Admissions for COPD in Past 12 Months", "required": True, "placeholder": "e.g., 1"},
                        {"id": "copd_antibiotics", "type": "number", "label": "Courses of Antibiotics for Chest in Past 12 Months", "required": False},
                        {"id": "copd_ocs_courses", "type": "number", "label": "Oral Corticosteroid Courses in Past 12 Months", "required": False},
                        {"id": "copd_frequent_exac", "type": "toggle", "label": "🔴 Frequent Exacerbations (≥2/year)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Frequent exacerbations. Review management plan, consider pulmonary rehabilitation and specialist referral.", "red_flag_negative": "Exacerbation frequency within acceptable range."}
                    ]
                },
                {
                    "title": "Inhaler Technique & Vaccination",
                    "questions": [
                        {"id": "copd_inhaler_technique", "type": "single_select", "label": "Inhaler Technique", "required": True, "options": ["Good", "Adequate", "Poor - Needs Education"]},
                        {"id": "copd_inhaler_type", "type": "textarea", "label": "Current Inhalers", "required": True, "placeholder": "e.g., Spiriva 18mcg OD, Symbicort 200/6 2 puffs BD..."},
                        {"id": "copd_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never Smoked", "Ex-Smoker", "Current Smoker"]},
                        {"id": "copd_flu_vaccine", "type": "toggle", "label": "Flu Vaccine Given?", "required": True, "output_phrase": "Flu Vaccine: {value}"},
                        {"id": "copd_pneumo_vaccine", "type": "toggle", "label": "Pneumococcal Vaccine Given?", "required": True, "output_phrase": "Pneumococcal Vaccine: {value}"},
                        {"id": "copd_covid_vaccine", "type": "toggle", "label": "COVID-19 Vaccine Up to Date?", "required": True}
                    ]
                },
                {
                    "title": "Pulmonary Rehabilitation & Self-Management",
                    "questions": [
                        {"id": "copd_pulmonary_rehab", "type": "toggle", "label": "Pulmonary Rehabilitation Offered/Completed?", "required": True, "output_phrase": "Pulmonary Rehab: {value}"},
                        {"id": "copd_action_plan", "type": "toggle", "label": "Self-Management Plan Provided?", "required": True, "output_phrase": "Self-Management Plan: {value}"},
                        {"id": "copd_rescue_pack", "type": "toggle", "label": "Rescue Pack (Antibiotics + Steroids) Provided?", "required": False},
                        {"id": "copd_exercise", "type": "single_select", "label": "Exercise Level", "required": True, "options": ["Regular", "Some Activity", "Very Limited by Breathlessness"]}
                    ]
                },
                {
                    "title": "Plan & Follow-up",
                    "examination": "Chest auscultation, spirometry, oxygen saturations, BMI, assessment for cor pulmonale",
                    "safety_netting": "If your breathing worsens rapidly, your sputum becomes green/brown, or you develop confusion or blue lips, seek urgent medical attention. Call 999 if you cannot speak in full sentences.",
                    "questions": [
                        {"id": "copd_ltot", "type": "toggle", "label": "Long Term Oxygen Therapy (LTOT) Assessment Needed?", "required": False},
                        {"id": "copd_palliative", "type": "toggle", "label": "Palliative Care/DNACPR Discussion Appropriate?", "required": False},
                        {"id": "copd_followup", "type": "duration", "label": "Follow-up Interval", "required": True, "units": ["weeks", "months"]},
                        {"id": "copd_review_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    seed_copd_template()