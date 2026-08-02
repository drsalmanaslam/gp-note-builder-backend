from app.database import SessionLocal
from app.models import User, Template

def seed_prediabetes():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Pre-Diabetes / Impaired Fasting Glucose"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Management of pre-diabetes (HbA1c 42-47 mmol/mol or IFG 6.1-6.9) covering lifestyle intervention, NHS Diabetes Prevention Programme referral, annual monitoring, and cardiovascular risk management.", category="Chronic Disease Reviews", content={"sections": [
        {"title": "Diagnostic Results", "section_type": "assessment", "questions": [
            {"id": "pred_hba1c", "type": "number", "label": "HbA1c (mmol/mol)", "required": True, "placeholder": "e.g., 44"},
            {"id": "pred_hba1c_date", "type": "text", "label": "Date of HbA1c", "required": True, "placeholder": "e.g., 2 weeks ago"},
            {"id": "pred_fasting_glucose", "type": "number", "label": "Fasting Glucose (if done)", "required": False, "placeholder": "e.g., 6.4"},
            {"id": "pred_previous_hba1c", "type": "text", "label": "Previous HbA1c & Date", "required": False, "placeholder": "e.g., 42 (6 months ago)"},
            {"id": "pred_category", "type": "single_select", "label": "Category", "required": True, "options": ["Pre-diabetes (HbA1c 42-47)", "Impaired Fasting Glucose (6.1-6.9)", "High risk (previous GDM, ethnicity, family history)"]}
        ]},
        {"title": "Risk Factors", "section_type": "history", "questions": [
            {"id": "pred_age", "type": "text", "label": "Age", "required": False},
            {"id": "pred_ethnicity", "type": "single_select", "label": "Ethnicity (High Risk Groups)", "required": True, "options": ["White European", "South Asian", "African-Caribbean", "Middle Eastern", "Other"]},
            {"id": "pred_family_dm", "type": "toggle", "label": "Family History of Diabetes?", "required": True},
            {"id": "pred_previous_gdm", "type": "toggle", "label": "Previous Gestational Diabetes?", "required": False},
            {"id": "pred_bmi", "type": "number", "label": "BMI", "required": True, "placeholder": "e.g., 31"},
            {"id": "pred_waist", "type": "number", "label": "Waist Circumference (cm)", "required": False, "placeholder": "e.g., 98"},
            {"id": "pred_bp", "type": "text", "label": "Blood Pressure", "required": True, "placeholder": "e.g., 138/86"},
            {"id": "pred_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
            {"id": "pred_exercise", "type": "single_select", "label": "Physical Activity (minutes/week)", "required": True, "options": ["<30 min", "30-90 min", "90-150 min", ">150 min"]},
            {"id": "pred_diet", "type": "single_select", "label": "Diet Quality", "required": True, "options": ["Healthy/balanced", "Moderate - some improvement needed", "Poor - high sugar/processed foods"]}
        ]},
        {"title": "Cardiovascular Risk", "section_type": "assessment", "questions": [
            {"id": "pred_qrisk", "type": "number", "label": "QRISK3 Score (%)", "required": False, "placeholder": "e.g., 15"},
            {"id": "pred_cholesterol", "type": "number", "label": "Total Cholesterol / HDL Ratio", "required": False, "placeholder": "e.g., 5.2 / 1.1"},
            {"id": "pred_statin", "type": "toggle", "label": "On Statin?", "required": False},
            {"id": "pred_ckd", "type": "toggle", "label": "CKD? (eGFR <60 or ACR >3)", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Pre-diabetes (HbA1c 42-47 mmol/mol)", "Impaired Fasting Glucose", "Type 2 Diabetes (needs repeat HbA1c to confirm if ≥48)", "Steroid-induced hyperglycaemia", "Stress hyperglycaemia"], "questions": [
            {"id": "pred_progression_risk", "type": "single_select", "label": "Risk of Progression to T2DM", "required": True, "options": ["Low - 1 risk factor, normal BMI", "Moderate - 2-3 risk factors", "High - multiple risk factors, HbA1c rising"]},
            {"id": "pred_readiness", "type": "single_select", "label": "Readiness to Change Lifestyle", "required": True, "options": ["Ready and motivated", "Willing to try", "Ambivalent", "Not interested"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Pre-diabetes is reversible with lifestyle changes. 50% reduction in progression to T2DM with intensive lifestyle intervention (Diabetes Prevention Programme). Targets: lose 5-10% body weight, 150 min moderate exercise/week, reduce sugar/refined carbs, increase fibre. Repeat HbA1c annually (or sooner if symptomatic: thirst, polyuria, weight loss). If HbA1c reaches 48 mmol/mol on repeat testing, diagnose T2DM. Return if: increased thirst, frequent urination, unexplained weight loss, blurred vision, or infections.", "questions": [
            {"id": "pred_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["NHS Diabetes Prevention Programme referral", "Dietary advice (Mediterranean diet, reduce sugar)", "Exercise prescription (150 min/week moderate)", "Weight loss target (5-10%)", "Smoking cessation", "Statin if QRISK ≥10%", "Annual HbA1c monitoring", "Self-refer to weight management"]},
            {"id": "pred_weight_target", "type": "text", "label": "Weight Loss Target", "required": False, "placeholder": "e.g., 5% weight loss in 6 months (4.5kg)"},
            {"id": "pred_dpp_referral", "type": "toggle", "label": "Diabetes Prevention Programme Referral Made?", "required": True},
            {"id": "pred_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., 6-month weight review, annual HbA1c, DPP programme attendance"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_prediabetes()