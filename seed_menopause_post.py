from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_menopause_post():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Menopausal Symptoms - Postmenopausal (No Periods)",
        "description": "Postmenopausal consultation covering clinical diagnosis (no period 1-2 years), continuous HRT options, urogenital atrophy treatment, and alternatives to HRT.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Diagnostic Criteria (Clinical Diagnosis)",
                "section_type": "history",
                "questions": [
                    {"id": "meno2_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 53"},
                    {"id": "meno2_diagnostic", "type": "single_select", "label": "Diagnostic Criteria", "required": True, "options": ["No Period for ≥2 Years + Age <50 = Postmenopausal", "No Period for ≥1 Year + Age ≥50 = Postmenopausal", "Surgical Menopause (Bilateral Oophorectomy)", "Uncertain - Check FSH"]},
                    {"id": "meno2_symptoms", "type": "multi_select", "label": "Symptom Screen (Modified Greene Climacteric Scale Available)", "required": True, "options": ["Vasomotor Flushes/Sweats", "Poor Sleep", "Anxiety", "Low Mood", "Cognitive Impairment / Brain Fog", "Muscle/Joint Pain", "Urinary Incontinence", "Hair/Skin Changes", "Low Libido", "Vaginal Dryness"]},
                    {"id": "meno2_severity", "type": "single_select", "label": "Symptom Severity", "required": True, "options": ["Mild - Coping Well", "Moderate - Affecting QoL", "Severe - Significant Impact"]}
                ]
            },
            {
                "title": "HRT Safety Screen",
                "section_type": "history",
                "questions": [
                    {"id": "meno2_breast_ca", "type": "toggle", "label": "Personal History Breast Cancer? (Refer Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Personal breast cancer = REFER menopause clinic.", "red_flag_negative": ""},
                    {"id": "meno2_endometrial_ca", "type": "toggle", "label": "Personal History Endometrial/Ovarian Cancer? (Refer Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Refer menopause clinic.", "red_flag_negative": ""},
                    {"id": "meno2_vte_history", "type": "toggle", "label": "Personal History VTE/Angina/CVA/TIA? (Transdermal with Caution - Consider Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: VTE/CVA = transdermal preferred. Consider menopause clinic.", "red_flag_negative": ""},
                    {"id": "meno2_porphyria", "type": "toggle", "label": "Personal History Porphyria? (Refer Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Refer menopause clinic.", "red_flag_negative": ""},
                    {"id": "meno2_endometriosis", "type": "toggle", "label": "Personal History Severe Endometriosis? (Consider Menopause Clinic)", "required": False},
                    {"id": "meno2_family_history", "type": "multi_select", "label": "Family History", "required": True, "options": ["Breast Cancer", "Ovarian Cancer", "Hormone-Provoked VTE", "None"]},
                    {"id": "meno2_smoking", "type": "single_select", "label": "Smoking (Transdermal Preferred Over Oral)", "required": True, "options": ["Non-Smoker", "Current Smoker - Transdermal Preferred"]},
                    {"id": "meno2_liver_enzyme", "type": "toggle", "label": "On Liver Enzyme-Inducing Medication?", "required": False},
                    {"id": "meno2_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": False, "options": ["None", "Within Limits", "Excess"]}
                ]
            },
            {
                "title": "Preventative Care & Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "meno2_screening", "type": "multi_select", "label": "Cervical Screening + Mammography UTD?", "required": True, "options": ["Cervical Screening UTD", "Mammography UTD", "Overdue - Advise", "Not Applicable"]},
                    {"id": "meno2_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 126/82"},
                    {"id": "meno2_bmi", "type": "number", "label": "BMI (kg/m²) - Not Essential if Transdermal Planned", "required": False, "placeholder": "e.g., 27"},
                    {"id": "meno2_breast_exam", "type": "single_select", "label": "Breast Examination (Only if Symptoms - Not Routine)", "required": False, "options": ["Normal", "Abnormal - Refer", "Not Performed"]}
                ]
            },
            {
                "title": "Patient Education",
                "section_type": "plan",
                "questions": [
                    {"id": "meno2_edu_resources", "type": "multi_select", "label": "Patient Resources Given", "required": False, "options": ["HSE South Menopause Leaflet", "www.menopausematters.co.uk", "CBT for Menopausal Symptoms (WHC Factsheet)"]},
                    {"id": "meno2_edu_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Smoking Cessation", "Reduced Alcohol", "Exercise", "Healthy Diet", "Wear Layers", "CBT for Flushes/Sweats"]},
                    {"id": "meno2_risk_breast", "type": "toggle", "label": "Breast Cancer: No Increased Risk First 5 Years. Slight Increase Thereafter (Less Than Obesity/Alcohol)?", "required": True},
                    {"id": "meno2_risk_vte", "type": "toggle", "label": "Thrombosis: ORAL Oestrogen Only. Transdermal NOT Associated with Increased VTE Risk?", "required": True},
                    {"id": "meno2_risk_side_effects", "type": "toggle", "label": "Initial Side Effects: Bloating, Breast Tenderness, Headache - Usually Self-Limiting?", "required": True}
                ]
            },
            {
                "title": "Continuous HRT (Non-Bleed-Producing - For Postmenopausal)",
                "section_type": "plan",
                "safety_netting": "Review at 3 months after starting, then 6-12 monthly. Continuous regimen appropriate ONLY because patient meets postmenopausal criteria. Using continuous regimen in perimenopausal = irregular bleeding. Can stop HRT anytime. Risk tools: FRAX (Irish-adapted), QRISK3 (qrisk.org/three/). Breast cancer risk: bcrisktool.cancer.gov. Evidence: gpevidence.org/conditions/menopause/.",
                "questions": [
                    {"id": "meno2_hrt_route", "type": "single_select", "label": "Continuous HRT Route (Non-Bleed-Producing)", "required": False, "options": ["Oral: Livial, Femoston Conti 1/5mg or 0.5/2.5mg, Indivina, Angeliq, Kliogest (If No VTE Risk)", "Transdermal Patch: Evorel Conti Twice Weekly", "Transdermal Oestrogen + Progesterone Separately", "Mirena IUS + Oestrogen (Evorel/Estradot/Oestrogel/Divigel/Lenzetto)", "Oestrogen Only (No Uterus/Mirena): Patch/Gel/Spray/Estrofem/Fematab", "None - HRT Declined/Contraindicated"]},
                    {"id": "meno2_progesterone", "type": "single_select", "label": "Progesterone Dose (If Uterus Present + Separate Oestrogen)", "required": False, "options": ["Utrogestan 100mg Nightly (Oestrogen ≤50mcg)", "Utrogestan 200mg Nightly (Oestrogen 75-100mcg)", "Dydrogesterone 10-20mg Daily (Oestrogen ≤50mcg)", "Dydrogesterone 20mg Daily (Oestrogen 75-100mcg)", "Not Required (No Uterus / Mirena In Situ <5 Years)"]},
                    {"id": "meno2_urogenital", "type": "single_select", "label": "Urogenital Atrophy Treatment", "required": False, "options": ["Vagifem 10mcg Nightly 2 Weeks → Twice Weekly", "Imvaggis Pessary Nightly 2 Weeks → Twice Weekly", "Blissel Gel Nightly 3 Weeks → Twice Weekly", "Ovestin Cream Daily 4 Weeks → Twice Weekly", "Vaginal Lubricants (Replens, YES, KY)", "Not Required"]},
                    {"id": "meno2_alternatives", "type": "single_select", "label": "Alternatives to HRT (If Declined/Contraindicated)", "required": False, "options": ["Citalopram / Escitalopram", "Fluoxetine", "Venlafaxine", "Fezolinetant", "Digital CBT for Insomnia (Sleepio)", "None - HRT Prescribed"]},
                    {"id": "meno2_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Postmenopausal - Starting Continuous HRT", "Postmenopausal - HRT Contraindicated (Alternatives)", "Postmenopausal - Lifestyle Only", "Refer Menopause Clinic"]},
                    {"id": "meno2_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3 months review, then 6-12 monthly"}
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
    seed_menopause_post()