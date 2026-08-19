from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_t1_diabetes():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Endocrinology").first()
    if not category: 
        category = Category(name="Endocrinology")
        db.add(category)
        db.commit()

    t = {
        "title": "Type 1 Diabetes Review",
        "description": "Comprehensive review for patients with Type 1 Diabetes, covering glycemic control, complications screening, and insulin management.",
        "category": "Endocrinology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "t1d_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Routine T1DM annual review",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "t1d_duration",
                        "type": "text",
                        "label": "Duration of Diabetes",
                        "required": True,
                        "placeholder": "e.g., 10 years",
                        "output_phrase": "Diabetes duration: {value}"
                    },
                    {
                        "id": "t1d_insulin_regimen",
                        "type": "single_select",
                        "label": "Insulin Regimen",
                        "required": True,
                        "options": ["Basal-bolus (MDI)", "Insulin pump", "Mixed insulin (twice daily)", "Other"],
                        "output_phrase": "Insulin regimen: {value}"
                    },
                    {
                        "id": "t1d_insulin_doses",
                        "type": "text",
                        "label": "Insulin Doses",
                        "required": False,
                        "placeholder": "e.g., Levemir 20u BD, Novorapid 6u TDS",
                        "output_phrase": "Doses: {value}"
                    },
                    {
                        "id": "t1d_hba1c",
                        "type": "text",
                        "label": "Latest HbA1c",
                        "required": True,
                        "placeholder": "e.g., 65 mmol/mol (8.1%)",
                        "output_phrase": "HbA1c: {value}"
                    },
                    {
                        "id": "t1d_blood_glucose",
                        "type": "text",
                        "label": "Blood Glucose Monitoring",
                        "required": False,
                        "placeholder": "e.g., Fasting 6-8 mmol/L, post-meal 8-10 mmol/L",
                        "output_phrase": "BM levels: {value}"
                    },
                    {
                        "id": "t1d_cgm",
                        "type": "toggle",
                        "label": "Using CGM / Flash Glucose Monitoring?",
                        "required": False,
                        "output_phrase": "CGM/FGM: {value}"
                    },
                    {
                        "id": "t1d_hypoglycaemia",
                        "type": "single_select",
                        "label": "Hypoglycaemia Episodes",
                        "required": True,
                        "options": ["None", "Rare (<1/month)", "Occasional (1-3/month)", "Frequent (>1/week)", "Severe (needing assistance) - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Frequent/severe hypoglycaemia - consider insulin adjustment, DVLA guidance, specialist input.",
                        "red_flag_negative": "",
                        "output_phrase": "Hypoglycaemia: {value}"
                    },
                    {
                        "id": "t1d_hyperglycaemia",
                        "type": "single_select",
                        "label": "Hyperglycaemia Episodes",
                        "required": True,
                        "options": ["None", "Rare", "Occasional", "Frequent DKA risk - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Frequent hyperglycaemia/DKA risk - urgent review and diabetes team referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Hyperglycaemia: {value}"
                    },
                    {
                        "id": "t1d_ckd_screening",
                        "type": "text",
                        "label": "Latest eGFR / Creatinine",
                        "required": False,
                        "placeholder": "e.g., eGFR 90, Creatinine 70",
                        "output_phrase": "eGFR: {value}"
                    },
                    {
                        "id": "t1d_microalbumin",
                        "type": "text",
                        "label": "Latest Microalbuminuria",
                        "required": False,
                        "placeholder": "e.g., <2.0 mg/mmol (normal)",
                        "output_phrase": "Microalbumin: {value}"
                    },
                    {
                        "id": "t1d_retinopathy",
                        "type": "single_select",
                        "label": "Latest Retinal Screening",
                        "required": True,
                        "options": ["No retinopathy", "Background retinopathy", "Pre-proliferative", "Proliferative - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Pre-proliferative/proliferative retinopathy - urgent ophthalmology referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Retinopathy: {value}"
                    },
                    {
                        "id": "t1d_neuropathy",
                        "type": "toggle",
                        "label": "Peripheral Neuropathy Symptoms?",
                        "required": False,
                        "output_phrase": "Neuropathy: {value}"
                    },
                    {
                        "id": "t1d_smoking",
                        "type": "single_select",
                        "label": "Smoking Status",
                        "required": True,
                        "options": ["Current smoker", "Ex-smoker", "Non-smoker"],
                        "output_phrase": "Smoking: {value}"
                    },
                    {
                        "id": "t1d_bp",
                        "type": "text",
                        "label": "Blood Pressure (clinic)",
                        "required": True,
                        "placeholder": "e.g., 132/82",
                        "output_phrase": "BP: {value}"
                    },
                    {
                        "id": "t1d_cholesterol",
                        "type": "text",
                        "label": "Latest Lipid Profile",
                        "required": False,
                        "placeholder": "e.g., Total 4.5, LDL 2.2, HDL 1.4, Trig 1.8",
                        "output_phrase": "Lipids: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "t1d_vitals",
                        "type": "text",
                        "label": "Vital Signs",
                        "required": True,
                        "placeholder": "e.g., BP 132/82, HR 78, BMI 27, SpO2 99%",
                        "output_phrase": "Vitals: {value}"
                    },
                    {
                        "id": "t1d_feet",
                        "type": "single_select",
                        "label": "Foot Examination",
                        "required": True,
                        "options": ["Normal pulses + sensation", "Reduced pulses - need Doppler", "Reduced sensation - need monofilament", "Ulceration - RED FLAG", "Normal"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Foot ulceration - urgent podiatry referral and vascular assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Feet: {value}"
                    },
                    {
                        "id": "t1d_bmi",
                        "type": "number",
                        "label": "BMI",
                        "required": False,
                        "placeholder": "e.g., 26",
                        "output_phrase": "BMI: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Type 1 Diabetes (established)",
                    "Poor glycaemic control",
                    "Complications: retinopathy, nephropathy, neuropathy",
                    "Hypoglycaemia unawareness",
                    "Insulin resistance",
                    "Coexisting autoimmune conditions: thyroid, coeliac",
                    "Psychological impact / diabetes distress"
                ],
                "questions": [
                    {
                        "id": "t1d_control",
                        "type": "single_select",
                        "label": "Glycaemic Control",
                        "required": True,
                        "options": ["Good (HbA1c target <58 mmol/mol)", "Suboptimal (58-69 mmol/mol)", "Poor (>69 mmol/mol) - needs review", "Excellent"],
                        "output_phrase": "Control: {value}"
                    },
                    {
                        "id": "t1d_complications",
                        "type": "multi_select",
                        "label": "Present Complications",
                        "required": False,
                        "options": ["Retinopathy", "Nephropathy", "Neuropathy", "Foot disease", "Cardiovascular disease", "Cerebrovascular disease", "None detected"],
                        "output_phrase": "Complications: {value}"
                    }
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Return if: Acute illness (sick day rules), recurrent hypoglycaemia, ketones present, symptoms of DKA (nausea, vomiting, abdominal pain, confusion), new foot ulcer/neuropathy, or visual changes. Check DVLA guidance - MUST notify DVLA if insulin-treated.",
                "questions": [
                    {
                        "id": "t1d_insulin_adjustment",
                        "type": "toggle",
                        "label": "Insulin Adjustment Advised?",
                        "required": False,
                        "output_phrase": "Insulin adjustment: {value}"
                    },
                    {
                        "id": "t1d_diabetes_education",
                        "type": "toggle",
                        "label": "Diabetes Education Offered?",
                        "required": False,
                        "output_phrase": "Diabetes education: {value}"
                    },
                    {
                        "id": "t1d_referrals",
                        "type": "multi_select",
                        "label": "Referrals",
                        "required": False,
                        "options": ["Diabetes Specialist Nurse", "Dietitian", "Podiatry", "Ophthalmology", "Cardiology", "Renal", "Psychologist", "None"],
                        "output_phrase": "Referrals: {value}"
                    },
                    {
                        "id": "t1d_followup",
                        "type": "text",
                        "label": "Follow-up Plan",
                        "required": True,
                        "placeholder": "e.g., Annual review, 3-month diabetes clinic, or sooner if issues",
                        "output_phrase": "Follow-up: {value}"
                    }
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(
            title=t["title"], 
            description=t["description"], 
            category=t["category"], 
            content=t["content"], 
            is_public=True, 
            created_by=admin.id, 
            version=1
        )
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    
    db.close()

if __name__ == "__main__":
    seed_t1_diabetes()