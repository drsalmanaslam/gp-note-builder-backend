from app.database import SessionLocal
from app.models import User, Template, Category

def seed_amenorrhoea():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Amenorrhoea / Oligomenorrhoea",
        "description": "Focused assessment for amenorrhoea and oligomenorrhoea including key history, examination, investigations, and management.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "amen_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 28"},
                    {"id": "amen_type", "type": "single_select", "label": "Type", "required": True, "options": ["Primary amenorrhoea (never menstruated by 16)", "Secondary amenorrhoea (≥6 months no periods)", "Oligomenorrhoea (>35 day cycles or <9/year)"]},
                    {"id": "amen_duration", "type": "text", "label": "Duration of Amenorrhoea", "required": True, "placeholder": "e.g., 8 months"},
                    {"id": "amen_previous_cycles", "type": "single_select", "label": "Previous Cycles Were", "required": True, "options": ["Previously regular (21-35 days)", "Always irregular", "Never menstruated"]}
                ]
            },
            {
                "title": "Key History",
                "section_type": "history",
                "questions": [
                    {"id": "amen_pregnant", "type": "toggle", "label": "Pregnant? (β-hCG checked)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Always exclude pregnancy first. Most common cause of secondary amenorrhoea.", "red_flag_negative": "Not pregnant."},
                    {"id": "amen_breastfeeding", "type": "toggle", "label": "Breastfeeding?", "required": True},
                    {"id": "amen_contraception", "type": "single_select", "label": "Current Contraception", "required": True, "options": ["None", "COCP", "POP", "Implant", "IUS (Mirena/Jaydess)", "Depo-Provera injection", "Recently stopped COCP (<6 months)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Progestogen-only methods (implant, IUS, injection) commonly cause amenorrhoea - may be normal.", "red_flag_negative": ""},
                    {"id": "amen_galactorrhoea", "type": "toggle", "label": "Galactorrhoea (milky nipple discharge)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Galactorrhoea + amenorrhoea = hyperprolactinaemia/prolactinoma. Check prolactin.", "red_flag_negative": ""},
                    {"id": "amen_hirsutism", "type": "toggle", "label": "Hirsutism / Acne / Hair Loss? (Hyperandrogenism)", "required": False},
                    {"id": "amen_hot_flushes", "type": "toggle", "label": "Hot Flushes / Night Sweats? (Oestrogen deficiency/POI)", "required": False},
                    {"id": "amen_headaches_visual", "type": "toggle", "label": "Headaches or Visual Disturbance? (Pituitary mass)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Headaches + visual symptoms + amenorrhoea = pituitary macroadenoma. Urgent MRI + endocrinology.", "red_flag_negative": ""},
                    {"id": "amen_weight_loss", "type": "toggle", "label": "Significant Weight Loss or Low BMI?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss/BMI <18.5 causes hypothalamic amenorrhoea. Screen for eating disorder.", "red_flag_negative": ""},
                    {"id": "amen_excess_exercise", "type": "toggle", "label": "Excessive Exercise? (Athlete/compulsive)", "required": False},
                    {"id": "amen_stress", "type": "toggle", "label": "Significant Stress?", "required": False},
                    {"id": "amen_thyroid_symptoms", "type": "toggle", "label": "Thyroid Symptoms? (Weight change, fatigue, temperature intolerance)", "required": False},
                    {"id": "amen_meds_antipsychotic", "type": "toggle", "label": "On Antipsychotics / Metoclopramide / SSRIs?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: These medications commonly cause hyperprolactinaemia. Check prolactin.", "red_flag_negative": ""},
                    {"id": "amen_chemotherapy", "type": "toggle", "label": "History of Chemotherapy or Pelvic Radiotherapy?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Can cause premature ovarian insufficiency.", "red_flag_negative": ""},
                    {"id": "amen_secondary_causes", "type": "multi_select", "label": "Other Relevant History", "required": False, "options": ["PCOS known", "Thyroid disease", "Coeliac disease", "Diabetes", "CKD", "Pelvic surgery/D&C", "Family history early menopause", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "amen_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 21.3", "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI <18.5 = hypothalamic amenorrhoea. BMI >30 = consider PCOS.", "red_flag_negative": ""},
                    {"id": "amen_hirsutism_exam", "type": "toggle", "label": "Hirsutism / Acne / Acanthosis Nigricans?", "required": False},
                    {"id": "amen_galactorrhoea_exam", "type": "toggle", "label": "Galactorrhoea Expressible?", "required": False},
                    {"id": "amen_cushingoid", "type": "toggle", "label": "Cushingoid Features? (Striae, buffalo hump, central obesity)", "required": False},
                    {"id": "amen_pelvic_exam", "type": "toggle", "label": "Pelvic Examination Indicated?", "required": False},
                    {"id": "amen_pelvic_findings", "type": "textarea", "label": "Pelvic Findings", "required": False, "placeholder": "Uterine size, adnexal masses, anatomical abnormalities..."},
                    {"id": "amen_visual_fields", "type": "single_select", "label": "Visual Fields (Confrontation)", "required": True, "options": ["Intact", "Bitemporal Hemianopia (optic chiasm compression)", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bitemporal hemianopia = pituitary macroadenoma. Urgent MRI + neurosurgery.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Pregnancy",
                    "PCOS",
                    "Functional Hypothalamic Amenorrhoea (stress/weight/exercise)",
                    "Hyperprolactinaemia / Prolactinoma",
                    "Primary Ovarian Insufficiency / Premature Menopause",
                    "Hypothyroidism",
                    "Medication-Induced (contraception, antipsychotics)",
                    "Cushing Syndrome",
                    "Asherman's Syndrome (intrauterine adhesions)",
                    "Eating Disorder",
                    "Pituitary Macroadenoma",
                    "Congenital Adrenal Hyperplasia",
                    "Turner Syndrome (primary amenorrhoea)",
                    "Chronic Disease (coeliac, IBD, CKD)"
                ],
                "questions": [
                    {"id": "amen_fsh", "type": "number", "label": "FSH (IU/L)", "required": False, "placeholder": "e.g., 65 (High = POI/menopause, Low = hypothalamic/pituitary)"},
                    {"id": "amen_lh", "type": "number", "label": "LH (IU/L)", "required": False, "placeholder": "e.g., 18 (High LH:FSH ratio suggests PCOS)"},
                    {"id": "amen_oestradiol", "type": "number", "label": "Oestradiol (pmol/L)", "required": False, "placeholder": "e.g., 85 (Low in POI/hypothalamic amenorrhoea)"},
                    {"id": "amen_prolactin", "type": "number", "label": "Prolactin (mIU/L)", "required": True, "placeholder": "e.g., 1250 (NR: 100-500)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Elevated prolactin - exclude medication causes, hypothyroidism. If >1000 persistent, needs MRI pituitary.", "red_flag_negative": ""},
                    {"id": "amen_tsh", "type": "number", "label": "TSH (mIU/L)", "required": True, "placeholder": "e.g., 3.2 (NR: 0.4-4.0)"},
                    {"id": "amen_testosterone", "type": "number", "label": "Testosterone (nmol/L) - if hyperandrogenism", "required": False, "placeholder": "e.g., 2.8 (NR: <1.8)"},
                    {"id": "amen_pelvic_uss", "type": "toggle", "label": "Pelvic Ultrasound Requested?", "required": False},
                    {"id": "amen_pelvic_uss_finding", "type": "single_select", "label": "Ultrasound Finding", "required": False, "options": ["Normal", "Polycystic ovaries (PCOS morphology)", "Ovarian cyst/mass", "Endometrial abnormality", "Uterine anomaly", "Pending"]},
                    {"id": "amen_mri_pituitary", "type": "toggle", "label": "MRI Pituitary (if prolactin elevated or visual symptoms)", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: periods do not resume within 3-6 months, new galactorrhoea/headaches/visual disturbance, severe pelvic pain, or trying to conceive without success for 6-12 months. If oestrogen deficient >12 months - ensure calcium 1200mg + vitamin D 10mcg daily for bone protection. If functional hypothalamic amenorrhoea: target BMI 19-25, reduce excessive exercise, manage stress. If PCOS: 5-10% weight loss first-line. If POI: needs HRT until at least age of natural menopause for bone/cardiovascular protection. If eating disorder suspected: urgent referral to eating disorder service.",
                "questions": [
                    {"id": "amen_plan_type", "type": "single_select", "label": "Management Approach", "required": True, "options": ["Treat underlying cause", "Reassurance + lifestyle advice", "Hormonal therapy (COCP/HRT)", "Refer to specialist", "Awaiting investigation results"]},
                    {"id": "amen_lifestyle", "type": "textarea", "label": "Lifestyle Advice", "required": False, "placeholder": "e.g., Weight gain to BMI >19, reduce exercise, stress management..."},
                    {"id": "amen_hormonal_rx", "type": "single_select", "label": "Hormonal Treatment", "required": False, "options": ["None", "COCP (cycle regulation + bone protection)", "Cyclical progestogen (e.g., Medroxyprogesterone 10mg BD 10 days every 3 months)", "HRT (if POI/menopause)", "None - awaiting endocrinology"]},
                    {"id": "amen_referral", "type": "multi_select", "label": "Referrals", "required": False, "options": ["Gynaecology", "Endocrinology", "Fertility clinic", "Dietitian", "Eating disorder service", "None required"]}
                ]
            },
            {
                "title": "Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "amen_followup_value", "type": "number", "label": "Follow-up in (Number)", "required": True, "placeholder": "e.g., 3"},
                    {"id": "amen_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["weeks", "months"]}
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
    seed_amenorrhoea()