from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_diabetes_template():
    db = SessionLocal()

    # Get admin user
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Admin user not found. Please create admin first.")
        db.close()
        return

    # Get or create category
    category_name = "Endocrinology"
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
        print(f"Category '{category_name}' created")

    template_data = {
        "title": "Diabetes Annual Review",
        "description": "Comprehensive annual review for patients with diabetes. Includes QOF indicators, medication review, and complications screening.",
        "category": "Endocrinology",
        "content": {
            "sections": [
                {
                    "title": "Patient Information",
                    "questions": [
                        {
                            "id": "diab_review_type",
                            "type": "select",
                            "label": "Review Type",
                            "required": True,
                            "options": ["Annual Review", "6-Month Review", "New Diagnosis", "Post-Hospital Follow-up"]
                        },
                        {
                            "id": "diab_diagnosis_date",
                            "type": "date",
                            "label": "Date of Diagnosis",
                            "required": False
                        },
                        {
                            "id": "diab_type",
                            "type": "single_select",
                            "label": "Diabetes Type",
                            "required": True,
                            "options": ["Type 1", "Type 2", "Gestational", "MODY", "Other"]
                        }
                    ]
                },
                {
                    "title": "Clinical Measurements & QOF Targets",
                    "red_flag_alert_text": "",
                    "red_flag_threshold": 1,
                    "questions": [
                        {
                            "id": "diab_hba1c",
                            "type": "number",
                            "label": "HbA1c (mmol/mol)",
                            "required": True,
                            "placeholder": "e.g., 48",
                            "output_phrase": "HbA1c: {value} mmol/mol"
                        },
                        {
                            "id": "diab_hba1c_target",
                            "type": "single_select",
                            "label": "HbA1c Target Met? (QOF: ≤59 for new, ≤64 for established)",
                            "required": True,
                            "options": ["Target Met (≤59)", "Target Met (≤64)", "Above Target", "Not Recorded"],
                            "output_phrase": "HbA1c Target Status: {value}"
                        },
                        {
                            "id": "diab_bp_systolic",
                            "type": "number",
                            "label": "Blood Pressure - Systolic (mmHg)",
                            "required": True,
                            "placeholder": "e.g., 130"
                        },
                        {
                            "id": "diab_bp_diastolic",
                            "type": "number",
                            "label": "Blood Pressure - Diastolic (mmHg)",
                            "required": True,
                            "placeholder": "e.g., 80"
                        },
                        {
                            "id": "diab_bp_target",
                            "type": "single_select",
                            "label": "BP Target Met? (QOF: ≤140/80, or ≤130/80 if renal disease)",
                            "required": True,
                            "options": ["Target Met", "Above Target", "Not Recorded"],
                            "output_phrase": "BP Target Status: {value}"
                        },
                        {
                            "id": "diab_cholesterol",
                            "type": "number",
                            "label": "Total Cholesterol (mmol/L)",
                            "required": True,
                            "placeholder": "e.g., 4.5"
                        },
                        {
                            "id": "diab_chol_target",
                            "type": "single_select",
                            "label": "Cholesterol Target Met? (QOF: ≤5.0)",
                            "required": True,
                            "options": ["Target Met", "Above Target", "Not Recorded"],
                            "output_phrase": "Cholesterol Target Status: {value}"
                        },
                        {
                            "id": "diab_egfr",
                            "type": "number",
                            "label": "eGFR (ml/min/1.73m²)",
                            "required": True,
                            "placeholder": "e.g., 75"
                        },
                        {
                            "id": "diab_acr",
                            "type": "number",
                            "label": "Urine ACR (mg/mmol)",
                            "required": False,
                            "placeholder": "e.g., 3.5"
                        },
                        {
                            "id": "diab_bmi",
                            "type": "number",
                            "label": "BMI (kg/m²)",
                            "required": True,
                            "placeholder": "e.g., 28.5"
                        }
                    ]
                },
                {
                    "title": "Complications Screening",
                    "questions": [
                        {
                            "id": "diab_retinopathy",
                            "type": "toggle",
                            "label": "Retinopathy Screening Completed",
                            "required": True,
                            "is_red_flag": False,
                            "output_phrase": "Retinopathy Screening: {value}"
                        },
                        {
                            "id": "diab_retinopathy_result",
                            "type": "single_select",
                            "label": "Retinopathy Result",
                            "required": False,
                            "options": ["No Retinopathy (R0)", "Background (R1)", "Pre-proliferative (R2)", "Proliferative (R3)", "Maculopathy"],
                            "condition": {"questionId": "diab_retinopathy", "value": True},
                            "has_condition": True
                        },
                        {
                            "id": "diab_foot_check",
                            "type": "toggle",
                            "label": "Foot Examination Completed",
                            "required": True,
                            "is_red_flag": False,
                            "output_phrase": "Foot Examination: {value}"
                        },
                        {
                            "id": "diab_foot_risk",
                            "type": "single_select",
                            "label": "Foot Risk Status",
                            "required": False,
                            "options": ["Low Risk", "Moderate Risk", "High Risk", "Active Ulcer"],
                            "condition": {"questionId": "diab_foot_check", "value": True},
                            "has_condition": True,
                            "is_red_flag": False
                        },
                        {
                            "id": "diab_foot_high_risk",
                            "type": "toggle",
                            "label": "🔴 High Risk Foot — Urgent Podiatry Referral Needed?",
                            "required": False,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: High risk diabetic foot identified. Urgent podiatry referral required.",
                            "red_flag_negative": "Diabetic foot risk assessed and managed appropriately.",
                            "condition": {"questionId": "diab_foot_risk", "value": "High Risk"},
                            "has_condition": True
                        },
                        {
                            "id": "diab_neuropathy",
                            "type": "toggle",
                            "label": "Peripheral Neuropathy Screening",
                            "required": True,
                            "output_phrase": "Neuropathy Screening: {value}"
                        },
                        {
                            "id": "diab_nephropathy",
                            "type": "toggle",
                            "label": "Nephropathy Monitoring (eGFR + ACR)",
                            "required": True,
                            "output_phrase": "Nephropathy Monitoring: {value}"
                        }
                    ]
                },
                {
                    "title": "Medication Review",
                    "questions": [
                        {
                            "id": "diab_medication_current",
                            "type": "textarea",
                            "label": "Current Diabetes Medications",
                            "required": True,
                            "placeholder": "e.g., Metformin 1g BD, Gliclazide 80mg OD..."
                        },
                        {
                            "id": "diab_medication_adherence",
                            "type": "single_select",
                            "label": "Medication Adherence",
                            "required": True,
                            "options": ["Taking as prescribed", "Occasional missed doses", "Frequent missed doses", "Not taking"],
                            "output_phrase": "Adherence: {value}"
                        },
                        {
                            "id": "diab_medication_changes",
                            "type": "textarea",
                            "label": "Medication Changes Made Today",
                            "required": False,
                            "placeholder": "e.g., Increased Metformin to 1g BD..."
                        },
                        {
                            "id": "diab_insulin",
                            "type": "toggle",
                            "label": "On Insulin Therapy?",
                            "required": True
                        },
                        {
                            "id": "diab_insulin_regime",
                            "type": "textarea",
                            "label": "Insulin Regime Details",
                            "required": False,
                            "placeholder": "e.g., Lantus 20 units at night, Novorapid 6 units TDS...",
                            "condition": {"questionId": "diab_insulin", "value": True},
                            "has_condition": True
                        },
                        {
                            "id": "diab_hypoglycaemia",
                            "type": "toggle",
                            "label": "🔴 History of Hypoglycaemic Episodes?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Patient reports hypoglycaemic episodes. Review medication and provide sick day rules.",
                            "red_flag_negative": "No significant hypoglycaemic episodes reported.",
                            "output_phrase": "Hypoglycaemia: {value}"
                        }
                    ]
                },
                {
                    "title": "Lifestyle & Education",
                    "questions": [
                        {
                            "id": "diab_smoking",
                            "type": "single_select",
                            "label": "Smoking Status",
                            "required": True,
                            "options": ["Never Smoked", "Ex-Smoker", "Current Smoker"],
                            "output_phrase": "Smoking Status: {value}"
                        },
                        {
                            "id": "diab_smoking_advice",
                            "type": "toggle",
                            "label": "Smoking Cessation Advice Given?",
                            "required": False,
                            "condition": {"questionId": "diab_smoking", "value": "Current Smoker"},
                            "has_condition": True
                        },
                        {
                            "id": "diab_exercise",
                            "type": "single_select",
                            "label": "Exercise Level",
                            "required": True,
                            "options": ["Regular (≥150 min/week)", "Some Activity", "Sedentary"],
                            "output_phrase": "Exercise: {value}"
                        },
                        {
                            "id": "diab_diet",
                            "type": "textarea",
                            "label": "Dietary Assessment & Advice",
                            "required": False,
                            "placeholder": "e.g., Advised on carbohydrate counting, portion control..."
                        },
                        {
                            "id": "diab_education",
                            "type": "toggle",
                            "label": "Structured Education Offered (e.g., DESMOND, DAFNE)?",
                            "required": True,
                            "output_phrase": "Structured Education: {value}"
                        }
                    ]
                },
                {
                    "title": "Annual Review Checklist",
                    "examination": "General inspection, BMI measurement, BP measurement, foot examination (monofilament + pulses), injection site check (if on insulin)",
                    "questions": [
                        {
                            "id": "diab_review_complete",
                            "type": "toggle",
                            "label": "All Annual Review Items Completed",
                            "required": True
                        },
                        {
                            "id": "diab_review_followup",
                            "type": "duration",
                            "label": "Follow-up Interval",
                            "required": True,
                            "units": ["weeks", "months"]
                        },
                        {
                            "id": "diab_review_notes",
                            "type": "textarea",
                            "label": "Additional Review Notes",
                            "required": False,
                            "placeholder": "Any other findings, concerns, or actions..."
                        }
                    ],
                    "safety_netting": "If you experience symptoms of hypoglycaemia (sweating, trembling, confusion) or hyperglycaemia (thirst, frequent urination, blurred vision), please contact the surgery. In an emergency, call 999.",
                    "differentials": []
                }
            ]
        },
        "is_public": True
    }

    # Check if template already exists
    existing_template = db.query(Template).filter(
        Template.title == template_data["title"],
        Template.created_by == admin.id
    ).first()

    if existing_template:
        db.delete(existing_template)
        db.commit()
        print(f"Removing old '{template_data['title']}' template")

    new_template = Template(
        title=template_data["title"],
        description=template_data["description"],
        category=template_data["category"],
        content=template_data["content"],
        is_public=template_data["is_public"],
        created_by=admin.id,
        version=1
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    print(f"Template '{template_data['title']}' created successfully!")
    print(f"  - Sections: {len(template_data['content']['sections'])}")
    total_questions = sum(len(s['questions']) for s in template_data['content']['sections'])
    print(f"  - Total Questions: {total_questions}")

    print("\nDiabetes Annual Review template seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_diabetes_template()