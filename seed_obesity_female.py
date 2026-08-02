from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_obesity_female():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Obesity - Female Consultation",
        "description": "Comprehensive obesity management for women covering BMI classification, GLP-1/GIP pharmacotherapy comparison (Saxenda, Mounjaro, Wegovy, Mysimba, Orlistat), bariatric referral criteria, and lifestyle support.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "obf_reason", "type": "single_select", "label": "Reason for Attendance", "required": True, "options": ["Requesting Weight Loss Medication", "Lifestyle Advice", "Medical Concern re Weight", "Routine Check"]},
                    {"id": "obf_weight_gain_meds", "type": "multi_select", "label": "Medications Causing Weight Gain", "required": True, "options": ["Antipsychotics (Olanzapine, Risperidone)", "Lithium", "Prednisolone / Steroids", "Amitriptyline / TCAs", "Valproic Acid", "Paroxetine", "Carbamazepine", "Gliclazide / Sulfonylureas", "Propranolol", "None"]},
                    {"id": "obf_cardiometabolic", "type": "multi_select", "label": "Cardiometabolic History", "required": True, "options": ["Hypertension", "High Cholesterol", "Diabetes / Pre-Diabetes", "Family History CVD", "None"]},
                    {"id": "obf_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Non-Smoker", "Ex-Smoker", "Current Smoker"]},
                    {"id": "obf_exercise", "type": "single_select", "label": "Exercise Level", "required": True, "options": ["Regular (≥150 Min/Week)", "Occasional", "Sedentary"]},
                    {"id": "obf_osa", "type": "toggle", "label": "Loud Snoring Reported by Partner? (OSA Screen)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Snoring + obesity = ?OSA. Epworth score + consider sleep study.", "red_flag_negative": ""},
                    {"id": "obf_hypothyroid", "type": "multi_select", "label": "Hypothyroidism Screen", "required": True, "options": ["Dry Skin", "Hair Loss", "Cold Intolerance", "None"]},
                    {"id": "obf_pcos", "type": "multi_select", "label": "PCOS Screen", "required": True, "options": ["Period Problems / Irregular Cycles", "Acne", "Hirsutism", "None"]},
                    {"id": "obf_contraception", "type": "toggle", "label": "Contraception Discussed? (ALL Pharmacological Options Contraindicated in Pregnancy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pregnancy must be avoided on all GLP-1/GIP agents, Mysimba, and Orlistat.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "obf_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 34"},
                    {"id": "obf_bmi_category", "type": "single_select", "label": "BMI Category", "required": True, "options": ["Overweight: 25-29.9", "Obese: ≥30", "Obesity Class 2: ≥35", "Obesity Class 3 (Morbid): ≥40"]},
                    {"id": "obf_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 138/86"},
                    {"id": "obf_waist", "type": "number", "label": "Waist Circumference (cm) - Just Above Iliac Crests", "required": False, "placeholder": "e.g., 95 (>80cm = Increased CV Risk in Women)"},
                    {"id": "obf_urinalysis_glucose", "type": "toggle", "label": "Urinalysis: Glucose?", "required": False},
                    {"id": "obf_hcg", "type": "toggle", "label": "hCG Negative? (MUST Be Negative Before Any Pharmacological Option)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive hCG = contraindication to ALL pharmacological options.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "obf_bloods", "type": "multi_select", "label": "Bloods Ordered (Via Nurse)", "required": False, "options": ["Fasting Glucose", "Fasting Lipids", "HbA1c", "LFTs (ALT - NAFLD Screen)", "TFTs"]}
                ]
            },
            {
                "title": "Patient Education - Key Messages",
                "section_type": "plan",
                "questions": [
                    {"id": "obf_edu_bmi", "type": "toggle", "label": "BMI Reflects Size, Not Health - Goal is Improved Health, Not Weight Loss Alone?", "required": False},
                    {"id": "obf_edu_response", "type": "toggle", "label": "Response Unpredictable; Motivation ≠ Success; Multiple Attempts Often Needed?", "required": False},
                    {"id": "obf_edu_independent", "type": "toggle", "label": "Diet + Exercise Help NAFLD, T2DM, HTN Independent of Weight Change?", "required": False}
                ]
            },
            {
                "title": "First-Line - Lifestyle & Support",
                "section_type": "plan",
                "questions": [
                    {"id": "obf_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Reduce Screen Time", "30 Min Exercise, 5 Days/Week (Brisk Walking, Cycling, Swimming)", "10k Steps Daily"]},
                    {"id": "obf_dietician", "type": "toggle", "label": "Dietician Referral - PHEW Programme? (Free 6-Week Community Programme if BMI ≥30, or ≥25 + Comorbidity)", "required": False},
                    {"id": "obf_community", "type": "multi_select", "label": "Community Weight Loss Groups", "required": False, "options": ["Slimming World", "Unislim", "Motivation Ireland", "Weight Watchers", "Why Weight Ireland", "The Physio Company"]},
                    {"id": "obf_resources", "type": "multi_select", "label": "Support Resources", "required": False, "options": ["www.asoi.info", "www.itsnotyourfault.ie", "www.weightmanagement.ie"]}
                ]
            },
            {
                "title": "Pharmacological Options - Eligibility",
                "section_type": "plan",
                "questions": [
                    {"id": "obf_eligibility", "type": "single_select", "label": "Eligibility for Pharmacotherapy", "required": True, "options": ["BMI ≥30 - Eligible", "BMI ≥27 + Risk Factor (Dyslipidaemia, HTN, Pre-DM, T2DM, OSA) - Eligible", "BMI <27 - Lifestyle Only", "Not Eligible - Contraindications Present"]},
                    {"id": "obf_contraindications", "type": "multi_select", "label": "Universal Contraindications (All GLP-1/GIP Agents)", "required": True, "options": ["History of IBD", "Diabetic Gastroparesis", "Gallstones", "Pancreatitis", "Medullary Thyroid Cancer", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any contraindication present = GLP-1/GIP agents contraindicated.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Pharmacological Options - Drug Selection",
                "section_type": "plan",
                "safety_netting": "UNIVERSAL GLP-1/GIP COUNSELLING: May cause nausea, vomiting, diarrhoea, constipation - delay dose escalation or reduce if significant GI symptoms. STOP + return if abdominal pain (?gallstones/pancreatitis). Eat small regular meals prioritising protein/fibre/water, minimise fat/processed food, no meals after 7pm, eat slowly, caution with fizzy drinks/alcohol/spicy food. Encourage resistance exercise. Dietician referral + review at 1 month. All options contraindicated in pregnancy. Discontinue if <5% weight loss at specified review point.",
                "questions": [
                    {"id": "obf_drug", "type": "single_select", "label": "Pharmacological Agent", "required": False, "options": ["Liraglutide (Saxenda) - BMI ≥30 / ≥27+RF. 0.6mg→3mg SC. Review 3 months. €250-300. GMS if MMP criteria.", "Mysimba (Naltrexone/Bupropion) - BMI ≥30 / ≥27+RF. Titrate to 2 BD. Review 16 weeks. €100-120.", "Tirzepatide (Mounjaro) - BMI ≥30 / ≥27+RF. 2.5mg→15mg weekly. Review 3 months. €250-300+.", "Semaglutide (Wegovy) - BMI ≥30 / ≥27+RF. 0.25mg→2.4mg weekly. Review 3 months. €250-300. Counsel NAION.", "Orlistat - BMI ≥30 / ≥28+RF. 120mg TDS with meals. Review 12 weeks. €50-100. Faecal urgency/oily discharge.", "None - Lifestyle Only"]},
                    {"id": "obf_glp_counselling", "type": "toggle", "label": "GLP-1/GIP Counselling Given? (GI Side Effects, Diet Advice, Stop if Abdo Pain)", "required": False},
                    {"id": "obf_discontinue_trigger", "type": "text", "label": "Discontinue If <5% Weight Loss at", "required": False, "placeholder": "e.g., 3 months on max dose"}
                ]
            },
            {
                "title": "Referral & Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "obf_bariatric", "type": "toggle", "label": "Bariatric Surgery Criteria Met? (BMI ≥40 / BMI ≥35 + Comorbidity / BMI ≥30 + T2DM <10 Years)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bariatric criteria met = refer for surgical assessment.", "red_flag_negative": ""},
                    {"id": "obf_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Obesity - Lifestyle Management", "Obesity - Pharmacotherapy Indicated", "Obesity - Bariatric Referral", "Overweight - Lifestyle Advice"]},
                    {"id": "obf_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1 month with dietician + weight check, 3 months drug review"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_obesity_female()