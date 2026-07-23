from app.database import SessionLocal
from app.models import User, Template, Category

def seed_diabetes_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "Diabetes Review",
        "description": "Comprehensive diabetes review covering glycaemic control, complications screening, cardiovascular risk, and management optimisation.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Current Status",
                "section_type": "history",
                "questions": [
                    {"id": "dm_presenting_complaint", "type": "text", "label": "Reason for Review", "required": True, "placeholder": "e.g., Routine annual review / poor control / new symptoms"},
                    {"id": "dm_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 58"},
                    {"id": "dm_type", "type": "single_select", "label": "Diabetes Type", "required": True, "options": ["Type 1", "Type 2 - diet controlled", "Type 2 - oral agents", "Type 2 - insulin", "Type 2 - GLP-1"]},
                    {"id": "dm_duration", "type": "number", "label": "Duration (years)", "required": True, "placeholder": "e.g., 8"},
                    {"id": "dm_hba1c", "type": "number", "label": "Latest HbA1c (mmol/mol)", "required": True, "placeholder": "e.g., 64", "is_red_flag": True, "red_flag_positive": "RED FLAG: HbA1c >75 mmol/mol = poor control. >86 mmol/mol = very poor. Intensify treatment.", "red_flag_negative": ""},
                    {"id": "dm_hba1c_date", "type": "text", "label": "Date of HbA1c", "required": True, "placeholder": "e.g., 2 weeks ago"},
                    {"id": "dm_hba1c_target", "type": "single_select", "label": "HbA1c Target", "required": True, "options": ["<48 mmol/mol (tight)", "<53 mmol/mol (standard)", "<58 mmol/mol (relaxed/elderly)", "<64 mmol/mol (frail)"]}
                ]
            },
            {
                "title": "Glycaemic Control & Monitoring",
                "section_type": "history",
                "questions": [
                    {"id": "dm_glucose_monitoring", "type": "single_select", "label": "Self-Monitoring Method", "required": True, "options": ["Blood glucose meter", "Flash glucose monitor (Libre)", "CGM (Dexcom)", "No monitoring"]},
                    {"id": "dm_fasting_glucose", "type": "text", "label": "Typical Fasting Glucose (mmol/L)", "required": False, "placeholder": "e.g., 7-9"},
                    {"id": "dm_postprandial", "type": "text", "label": "Typical Post-Meal Glucose (mmol/L)", "required": False, "placeholder": "e.g., 10-14"},
                    {"id": "dm_hypoglycaemia", "type": "single_select", "label": "Hypoglycaemic Episodes (requiring assistance)", "required": True, "options": ["None", "1-2 in 12 months", "≥3 in 12 months", "Severe (hospital admission)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe/recurrent hypos = medication review urgently. DVLA implications if on insulin/sulfonylureas.", "red_flag_negative": ""},
                    {"id": "dm_hypo_awareness", "type": "single_select", "label": "Hypoglycaemia Awareness", "required": False, "options": ["Normal awareness", "Impaired awareness", "Loss of warning signs - URGENT"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Impaired hypo awareness = URGENT. Must not drive. Immediate specialist referral.", "red_flag_negative": ""},
                    {"id": "dm_sick_day_rules", "type": "toggle", "label": "Sick Day Rules Understood?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Patient must understand sick day rules. Risk of DKA (T1) or HHS (T2).", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Current Medications",
                "section_type": "history",
                "questions": [
                    {"id": "dm_medications", "type": "textarea", "label": "Current Diabetes Medications", "required": True, "placeholder": "e.g., Metformin 1g BD\nGliclazide 80mg BD\nEmpagliflozin 10mg OD\nSemaglutide 1mg weekly"},
                    {"id": "dm_insulin", "type": "toggle", "label": "On Insulin?", "required": False},
                    {"id": "dm_insulin_regimen", "type": "text", "label": "Insulin Regimen", "required": False, "placeholder": "e.g., Levemir 30 units nocte, Novorapid 8 units TDS"},
                    {"id": "dm_adherence", "type": "single_select", "label": "Medication Adherence", "required": True, "options": ["Good", "Fair - occasional misses", "Poor - frequent misses", "Not taking as prescribed"]},
                    {"id": "dm_side_effects", "type": "multi_select", "label": "Side Effects", "required": False, "options": ["GI upset (Metformin)", "Hypos (Sulfonylurea/Insulin)", "Genital thrush (SGLT2i)", "Weight gain", "Weight loss (GLP-1)", "Injection site reaction", "None"]}
                ]
            },
            {
                "title": "Complications Screening - Eyes & Kidneys",
                "section_type": "history",
                "questions": [
                    {"id": "dm_retinal_screening", "type": "single_select", "label": "Retinal Screening", "required": True, "options": ["Up to date - no retinopathy", "Up to date - background retinopathy", "Up to date - pre-proliferative/proliferative", "Up to date - maculopathy", "Overdue - book urgently", "Under hospital eye service"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Overdue retinal screening = book urgently. Proliferative retinopathy/maculopathy = needs hospital eye service.", "red_flag_negative": ""},
                    {"id": "dm_egfr", "type": "number", "label": "Latest eGFR (ml/min/1.73m²)", "required": True, "placeholder": "e.g., 65", "is_red_flag": True, "red_flag_positive": "RED FLAG: eGFR <60 = CKD. <30 = nephrology referral. Check ACR.", "red_flag_negative": ""},
                    {"id": "dm_acr", "type": "number", "label": "Urine Albumin:Creatinine Ratio (mg/mmol)", "required": True, "placeholder": "e.g., 3.5", "is_red_flag": True, "red_flag_positive": "RED FLAG: ACR ≥3 = microalbuminuria (ACEi/ARB). ACR ≥30 = proteinuria (nephrology).", "red_flag_negative": ""},
                    {"id": "dm_acei_arb", "type": "toggle", "label": "On ACEi / ARB? (Renoprotection if ACR raised)", "required": False}
                ]
            },
            {
                "title": "Complications Screening - Feet & Nerves",
                "section_type": "history",
                "questions": [
                    {"id": "dm_foot_risk", "type": "single_select", "label": "Foot Risk Classification", "required": True, "options": ["Low risk (normal sensation + pulses)", "Moderate risk (loss of sensation OR absent pulses)", "High risk (loss of sensation AND absent pulses / deformity / previous ulcer)", "Active foot problem - URGENT"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Active foot problem = same-day podiatry. High risk = regular podiatry.", "red_flag_negative": ""},
                    {"id": "dm_neuropathy", "type": "toggle", "label": "Peripheral Neuropathy Symptoms? (Numbness, tingling, burning)", "required": False},
                    {"id": "dm_monofilament", "type": "single_select", "label": "10g Monofilament Sensation", "required": True, "options": ["Normal (felt at all sites)", "Abnormal (absent at ≥1 site)", "Not tested"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Loss of protective sensation = high ulcer risk. Podiatry referral.", "red_flag_negative": ""},
                    {"id": "dm_pulses", "type": "single_select", "label": "Foot Pulses", "required": True, "options": ["Both palpable", "One or both reduced/absent", "Not tested"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent pulses = PAD. ABPI + vascular assessment.", "red_flag_negative": ""},
                    {"id": "dm_foot_deformity", "type": "toggle", "label": "Foot Deformity / Callus?", "required": False}
                ]
            },
            {
                "title": "Cardiovascular Risk",
                "section_type": "examination",
                "questions": [
                    {"id": "dm_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 138/82", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP ≥140/80 (or ≥130/80 if albuminuria) = needs treatment. ≥180/120 = urgent.", "red_flag_negative": ""},
                    {"id": "dm_cholesterol", "type": "text", "label": "Lipid Profile", "required": False, "placeholder": "e.g., TC 4.8, HDL 1.1, LDL 2.9, Trig 2.2"},
                    {"id": "dm_statin", "type": "single_select", "label": "Statin Therapy", "required": True, "options": ["On statin (Atorvastatin 20mg or equivalent)", "On statin - lower dose", "Not on statin - should be offered", "Not on statin - contraindicated/declined"]},
                    {"id": "dm_antiplatelet", "type": "toggle", "label": "On Antiplatelet? (If established CVD)", "required": False},
                    {"id": "dm_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
                    {"id": "dm_qrisk", "type": "number", "label": "QRISK3 Score (%)", "required": False, "placeholder": "e.g., 18%"}
                ]
            },
            {
                "title": "Lifestyle",
                "section_type": "history",
                "questions": [
                    {"id": "dm_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 32", "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI >30 = weight management. Consider GLP-1 if HbA1c above target.", "red_flag_negative": ""},
                    {"id": "dm_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 88"},
                    {"id": "dm_diet", "type": "single_select", "label": "Dietary Habits", "required": True, "options": ["Good - balanced, portion control", "Fair - some unhealthy choices", "Poor - high sugar/fat"]},
                    {"id": "dm_exercise", "type": "single_select", "label": "Physical Activity", "required": True, "options": ["≥150 min/week", "Some but less than target", "Sedentary"]},
                    {"id": "dm_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess"]},
                    {"id": "dm_education", "type": "multi_select", "label": "Structured Education", "required": False, "options": ["DESMOND / X-PERT attended", "DAFNE (Type 1)", "Not attended - offered today", "Declined"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Type 1 Diabetes",
                    "Type 2 Diabetes - Well Controlled",
                    "Type 2 Diabetes - Suboptimal Control",
                    "Type 2 Diabetes - Poor Control",
                    "Diabetic Nephropathy",
                    "Diabetic Retinopathy",
                    "Diabetic Peripheral Neuropathy",
                    "Diabetic Autonomic Neuropathy",
                    "Peripheral Arterial Disease",
                    "Diabetic Foot - Low/Moderate/High Risk",
                    "Cardiovascular Disease (established)",
                    "Hypoglycaemia Unawareness",
                    "Recurrent Hypoglycaemia"
                ],
                "questions": [
                    {"id": "dm_diagnosis_impression", "type": "single_select", "label": "Overall Assessment", "required": True, "options": ["Well controlled - continue", "Suboptimal - needs intensification", "Poor control - significant changes needed", "Complications present - needs specialist input", "Hypoglycaemia concerns - urgent review"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: blood glucose persistently >15 mmol/L with ketones (T1: risk of DKA), signs of infection at foot, visual disturbance, symptoms of hypoglycaemia, or any new concerning symptoms. Sick day rules: never stop insulin (T1), may need to stop SGLT2i if unwell (risk of euglycaemic DKA), monitor glucose closely, stay hydrated. DVLA: must inform if on insulin or sulfonylureas. Test glucose before driving and every 2 hours on long journeys. Do not drive if glucose <5 mmol/L. Foot care: daily inspection, appropriate footwear, never walk barefoot. Retinal screening and foot checks must be booked. Medication review: ensure on ACEi/ARB if albuminuria, statin unless contraindicated, consider SGLT2i/GLP-1 for cardiovascular/renal protection.",
                "questions": [
                    {"id": "dm_plan", "type": "single_select", "label": "Management Decision", "required": True, "options": ["Continue same treatment", "Intensify oral therapy", "Add GLP-1 receptor agonist", "Start insulin", "Adjust insulin doses", "Refer diabetes specialist", "Refer podiatry", "Refer dietitian", "Refer nephrology"]},
                    {"id": "dm_medication_changes", "type": "textarea", "label": "Medication Changes", "required": False, "placeholder": "e.g., Add Empagliflozin 10mg OD. Increase Metformin to 1g BD."},
                    {"id": "dm_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3 months with repeat HbA1c, renal function. Annual review."}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_diabetes_review()