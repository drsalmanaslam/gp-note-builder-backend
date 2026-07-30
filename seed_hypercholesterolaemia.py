from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hypercholesterolaemia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Hypercholesterolaemia",
        "description": "Focused assessment for elevated cholesterol covering QRISK3 risk stratification, statin prescribing, familial hypercholesterolaemia red flags, and lifestyle management.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Presentation & History",
                "section_type": "history",
                "questions": [
                    {"id": "chol_presenting_complaint", "type": "text", "label": "Reason for Assessment", "required": True, "placeholder": "e.g., Incidental raised cholesterol on routine bloods"},
                    {"id": "chol_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 48"},
                    {"id": "chol_total_chol", "type": "number", "label": "Total Cholesterol (mmol/L)", "required": False, "placeholder": "e.g., 6.8"},
                    {"id": "chol_ldl", "type": "number", "label": "LDL Cholesterol (mmol/L)", "required": False, "placeholder": "e.g., 4.5"},
                    {"id": "chol_hdl", "type": "number", "label": "HDL Cholesterol (mmol/L)", "required": False, "placeholder": "e.g., 1.1"},
                    {"id": "chol_triglycerides", "type": "number", "label": "Triglycerides (mmol/L)", "required": False, "placeholder": "e.g., 2.2"},
                    {"id": "chol_non_hdl", "type": "number", "label": "Non-HDL Cholesterol (TC - HDL)", "required": False, "placeholder": "e.g., 5.7"},
                    {"id": "chol_diet", "type": "single_select", "label": "Diet", "required": True, "options": ["Mediterranean / Balanced", "High saturated fat (milk, meats, fried)", "High processed foods", "Vegetarian/Vegan", "Uncertain"]},
                    {"id": "chol_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
                    {"id": "chol_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess"]}
                ]
            },
            {
                "title": "QRISK3 & Cardiovascular Risk",
                "section_type": "assessment",
                "questions": [
                    {"id": "chol_htn", "type": "toggle", "label": "Hypertension?", "required": True},
                    {"id": "chol_diabetes", "type": "toggle", "label": "Diabetes Mellitus?", "required": True},
                    {"id": "chol_ckd", "type": "toggle", "label": "Chronic Kidney Disease? (eGFR <60)", "required": True},
                    {"id": "chol_cvd", "type": "toggle", "label": "Established CVD? (IHD, stroke, PAD)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Established CVD = secondary prevention. Statin indicated regardless of QRISK.", "red_flag_negative": ""},
                    {"id": "chol_family_cvd", "type": "toggle", "label": "Family History Premature CVD? (<60 years 1st degree)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx premature CVD = higher risk. Consider genetic FH screen.", "red_flag_negative": ""},
                    {"id": "chol_qrisk", "type": "number", "label": "QRISK3 Score (%)", "required": True, "placeholder": "e.g., 14", "is_red_flag": True, "red_flag_positive": "RED FLAG: QRISK >10% = offer statin for primary prevention.", "red_flag_negative": ""},
                    {"id": "chol_statin_indicated", "type": "toggle", "label": "Statin Indicated? (QRISK >10% or CVD or FH)", "required": True}
                ]
            },
            {
                "title": "Familial Hypercholesterolaemia (FH) Red Flags",
                "section_type": "examination",
                "questions": [
                    {"id": "chol_xanthomas", "type": "toggle", "label": "Tendon Xanthomas?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Tendon xanthomas = probable FH. Refer lipid clinic + genetic testing.", "red_flag_negative": ""},
                    {"id": "chol_xanthelasma", "type": "toggle", "label": "Xanthelasma?", "required": False},
                    {"id": "chol_corneal_arcus", "type": "toggle", "label": "Corneal Arcus? (<50 years)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Corneal arcus <50 = ?FH. Check lipids + family history.", "red_flag_negative": ""},
                    {"id": "chol_fh_criteria", "type": "single_select", "label": "Simon Broome / DLCN FH Criteria", "required": False, "options": ["Possible FH - needs lipid clinic referral", "Definite FH - URGENT lipid clinic + cascade screening", "Unlikely FH", "Not assessed"]}
                ]
            },
            {
                "title": "Statin Safety Check",
                "section_type": "history",
                "questions": [
                    {"id": "chol_muscle_pain", "type": "toggle", "label": "Unexplained Muscle Pain / Myopathy History?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Muscle pain = check CK before starting statin. If CK >5x ULN: do NOT start statin. If CK <5x ULN: start at lower dose.", "red_flag_negative": ""},
                    {"id": "chol_ck", "type": "number", "label": "Baseline CK (if muscle symptoms)", "required": False, "placeholder": "e.g., 180"},
                    {"id": "chol_lfts", "type": "toggle", "label": "Baseline LFTs Checked?", "required": True},
                    {"id": "chol_pregnancy", "type": "toggle", "label": "Pregnant / Planning Pregnancy? (Statin CI)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Statins contraindicated in pregnancy/planning pregnancy. Stop 3 months before conception.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "chol_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 128/90"},
                    {"id": "chol_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 32"},
                    {"id": "chol_waist", "type": "number", "label": "Waist Circumference (cm)", "required": False, "placeholder": "e.g., 102"},
                    {"id": "chol_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": False, "options": ["HS 1+2 Normal", "Murmur present", "Not assessed"]},
                    {"id": "chol_pulses", "type": "single_select", "label": "DP + PT Pulses", "required": False, "options": ["B/L present + normal", "Reduced/absent", "Not assessed"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Primary Hypercholesterolaemia",
                    "Familial Hypercholesterolaemia (FH)",
                    "Secondary Hyperlipidaemia (Hypothyroidism, CKD, Diabetes)",
                    "Diet-Induced Hyperlipidaemia",
                    "Combined Hyperlipidaemia",
                    "Metabolic Syndrome"
                ],
                "questions": [
                    {"id": "chol_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["Lipid Profile (non-fasting)", "HbA1c / Fasting Glucose", "TFTs", "U&E / eGFR", "LFTs (baseline)", "CK (if muscle symptoms)", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Report promptly if: unexplained muscle pain, tenderness, or weakness (myalgia/rhabdomyolysis) while on statin. Stop statin and check CK. Non-fasting lipid testing is now standard (non-HDL = TC - HDL). Fasting only needed for formal LDL/triglycerides or combined glucose. Statin target: >40% reduction in non-HDL cholesterol at 3 months. If not achieved: titrate Atorvastatin to 80mg OD or add Ezetimibe 10mg OD. LFTs: baseline pre-statin, repeat at 3 months, then annually. Transient transaminase rise <3x ULN is common and not an indication to stop statin. True hepatotoxicity is extremely rare.",
                "questions": [
                    {"id": "chol_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Lifestyle trial for 6 months (recheck lipids)", "Atorvastatin 20mg OD", "Atorvastatin 40-80mg OD", "Rosuvastatin 10-20mg OD", "Add Ezetimibe 10mg OD", "Refer lipid clinic (?FH)"]},
                    {"id": "chol_lifestyle", "type": "toggle", "label": "Mediterranean Diet Advised? (Reduce saturated fats, oily fish x2/week)", "required": True},
                    {"id": "chol_exercise", "type": "toggle", "label": "Exercise Advised? (150 min/week moderate)", "required": True},
                    {"id": "chol_decision_aid", "type": "toggle", "label": "Mayo Clinic Statin Decision Aid Used?", "required": False},
                    {"id": "chol_non_fasting", "type": "toggle", "label": "Non-Fasting Lipids Acceptable Explained?", "required": False},
                    {"id": "chol_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3 months lipids + LFTs if statin started, 6 months if lifestyle trial"}
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
    seed_hypercholesterolaemia()