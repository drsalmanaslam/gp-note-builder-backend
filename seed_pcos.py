from app.database import SessionLocal
from app.models import User, Template, Category

def seed_pcos():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "PCOS / Polycystic Ovarian Syndrome Assessment",
        "description": "Focused assessment for PCOS including Rotterdam criteria, metabolic screening, and management of hirsutism, oligomenorrhoea, and insulin resistance.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    {"id": "pcos_consult_type", "type": "single_select", "label": "Consultation Type", "required": True, "options": ["F2F Consultation - ID Confirmed", "Telephone Consultation - ID Confirmed", "Seen Alone", "Seen With Family/Carer"]},
                    {"id": "pcos_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 26"},
                    {"id": "pcos_menarche", "type": "number", "label": "Age at Menarche", "required": True, "placeholder": "e.g., 13"}
                ]
            },
            {
                "title": "Rotterdam Criteria - Hyperandrogenism",
                "section_type": "history",
                "questions": [
                    {"id": "pcos_hirsutism", "type": "toggle", "label": "Hirsutism? (Male-pattern hair growth)", "required": True},
                    {"id": "pcos_hirsutism_areas", "type": "multi_select", "label": "Areas of Hirsutism", "required": False, "options": ["Upper lip", "Chin", "Side of face", "Chest", "Abdomen", "Lower back", "Upper arms", "Thighs", "None"]},
                    {"id": "pcos_acne", "type": "toggle", "label": "Acne? (Face, chest, back)", "required": True},
                    {"id": "pcos_alopecia", "type": "toggle", "label": "Scalp Hair Thinning / Male-Pattern Baldness?", "required": False},
                    {"id": "pcos_most_distressing", "type": "text", "label": "Most Distressing Symptom", "required": True, "placeholder": "e.g., Facial hair growth, acne, weight, irregular periods"}
                ]
            },
            {
                "title": "Rotterdam Criteria - Ovulatory Dysfunction",
                "section_type": "history",
                "questions": [
                    {"id": "pcos_cycle", "type": "single_select", "label": "Menstrual Cycle Pattern", "required": True, "options": ["Regular (21-35 days)", "Oligomenorrhoea (cycles >35 days or <9 periods/year)", "Amenorrhoea (>6 months no periods)"]},
                    {"id": "pcos_lmp", "type": "text", "label": "Last Menstrual Period", "required": True, "placeholder": "e.g., 2 months ago"},
                    {"id": "pcos_period_flow", "type": "single_select", "label": "Period Flow", "required": False, "options": ["Light", "Moderate", "Heavy", "Variable"]},
                    {"id": "pcos_period_duration", "type": "number", "label": "Duration of Bleeding (days)", "required": False, "placeholder": "e.g., 4"}
                ]
            },
            {
                "title": "Key History",
                "section_type": "history",
                "questions": [
                    {"id": "pcos_weight_changes", "type": "toggle", "label": "Weight Gain / Difficulty Losing Weight?", "required": True},
                    {"id": "pcos_family_history", "type": "multi_select", "label": "Family History", "required": False, "options": ["PCOS", "Diabetes (Type 2)", "Infertility", "Hirsutism", "None"]},
                    {"id": "pcos_fatigue_headaches", "type": "toggle", "label": "Daily Fatigue / Headaches?", "required": False},
                    {"id": "pcos_sleep_apnoea", "type": "toggle", "label": "Snoring / Cessation of Breathing During Sleep? (OSA)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Possible obstructive sleep apnoea - common in PCOS especially if BMI >30. Consider respiratory referral for sleep studies.", "red_flag_negative": ""},
                    {"id": "pcos_smoking", "type": "toggle", "label": "Smoking?", "required": True},
                    {"id": "pcos_alcohol", "type": "toggle", "label": "Alcohol?", "required": False},
                    {"id": "pcos_contraception", "type": "single_select", "label": "Current Contraception / Oestrogen Use", "required": True, "options": ["None", "COCP", "POP", "Implant", "IUS", "Depo-Provera"]},
                    {"id": "pcos_pregnancy_test", "type": "single_select", "label": "β-hCG (Pregnancy Test)", "required": True, "options": ["Negative", "Positive", "Not done"]},
                    {"id": "pcos_obstetric", "type": "text", "label": "Obstetric History (Gravida / Para)", "required": True, "placeholder": "e.g., G0P0"},
                    {"id": "pcos_fertility_concerns", "type": "toggle", "label": "Fertility Concerns / Planning Pregnancy?", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "pcos_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 32", "is_red_flag": True, "red_flag_positive": "RED FLAG: Raised BMI is common in PCOS and worsens insulin resistance. 5-10% weight loss can restore ovulation and improve symptoms.", "red_flag_negative": ""},
                    {"id": "pcos_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 122"},
                    {"id": "pcos_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 84"},
                    {"id": "pcos_hirsutism_exam", "type": "multi_select", "label": "Hirsutism on Examination", "required": True, "options": ["Face (mild)", "Face (moderate/severe)", "Chest/abdomen", "Back", "None", "Not examined"]},
                    {"id": "pcos_acne_exam", "type": "toggle", "label": "Acne on Examination?", "required": False},
                    {"id": "pcos_alopecia_exam", "type": "toggle", "label": "Alopecia / Hair Thinning (Male Pattern)?", "required": False},
                    {"id": "pcos_acanthosis", "type": "toggle", "label": "Acanthosis Nigricans? (Nape of neck, axillae - insulin resistance)", "required": False},
                    {"id": "pcos_pelvic_exam", "type": "toggle", "label": "Pelvic Examination Indicated?", "required": False}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "PCOS (meets Rotterdam criteria - 2 of: oligo/anovulation, hyperandrogenism, polycystic ovaries)",
                    "Idiopathic Hirsutism",
                    "Congenital Adrenal Hyperplasia (Non-classical)",
                    "Cushing Syndrome",
                    "Androgen-Secreting Tumour (Ovarian/Adrenal)",
                    "Hypothyroidism",
                    "Hyperprolactinaemia",
                    "Hypothalamic Amenorrhoea (if amenorrhoeic)",
                    "Premature Ovarian Insufficiency"
                ],
                "questions": [
                    {"id": "pcos_fsh", "type": "number", "label": "FSH (IU/L)", "required": False, "placeholder": "Day 2-4 if cycling. e.g., 5.2"},
                    {"id": "pcos_lh", "type": "number", "label": "LH (IU/L)", "required": False, "placeholder": "e.g., 18 (Raised LH:FSH ratio >2:1 common in PCOS)"},
                    {"id": "pcos_oestradiol", "type": "number", "label": "Oestradiol (pmol/L)", "required": False, "placeholder": "Day 2-4. e.g., 165"},
                    {"id": "pcos_testosterone", "type": "number", "label": "Testosterone (nmol/L)", "required": True, "placeholder": "e.g., 2.8 (NR: <1.8)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Testosterone >5 nmol/L requires investigation for androgen-secreting tumour.", "red_flag_negative": ""},
                    {"id": "pcos_shbg", "type": "number", "label": "SHBG (nmol/L)", "required": False, "placeholder": "e.g., 18 (Low in PCOS/insulin resistance)"},
                    {"id": "pcos_fai", "type": "number", "label": "Free Androgen Index (FAI)", "required": False, "placeholder": "e.g., 8.5 (NR: <4.5)"},
                    {"id": "pcos_tsh", "type": "number", "label": "TSH (mIU/L)", "required": False, "placeholder": "e.g., 2.1 (NR: 0.4-4.0)"},
                    {"id": "pcos_prolactin", "type": "number", "label": "Prolactin (mIU/L)", "required": False, "placeholder": "e.g., 320 (NR: 100-500)"},
                    {"id": "pcos_hba1c", "type": "number", "label": "HbA1c (mmol/mol)", "required": False, "placeholder": "e.g., 38 (NR: 20-42)"},
                    {"id": "pcos_fasting_glucose", "type": "number", "label": "Fasting Glucose (mmol/L)", "required": False, "placeholder": "e.g., 5.2 (NR: 3.5-5.5)"},
                    {"id": "pcos_lipids", "type": "textarea", "label": "Lipid Profile", "required": False, "placeholder": "e.g., Total Chol 5.2, HDL 0.9, LDL 3.4, Trig 2.1"},
                    {"id": "pcos_bloods_ordered", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FSH, LH (Day 2-4)", "Oestradiol (Day 2-4)", "Total Testosterone", "SHBG + Free Androgen Index", "TSH", "Prolactin", "HbA1c", "Fasting Glucose", "Lipid Profile", "17-OH Progesterone (if CAH suspected)", "None yet"]},
                    {"id": "pcos_pelvic_uss", "type": "toggle", "label": "Pelvic Ultrasound? (>8 years from menarche)", "required": False},
                    {"id": "pcos_uss_result", "type": "single_select", "label": "USS Result", "required": False, "options": ["Pending", "Polycystic ovaries (≥20 follicles/ovary or volume >10ml)", "Normal ovaries", "Not indicated"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return for review with blood results. Return sooner if: rapid worsening of hirsutism, development of virilisation signs (deepening voice, male-pattern baldness, clitoromegaly), severe pelvic pain, or fertility concerns. If using spironolactone: monitor renal function at baseline, check potassium after 6 weeks if combined with OCP or age >45. Avoid trimethoprim concurrently. Contraception essential as spironolactone is teratogenic (feminisation of male fetus). Weight loss of 5-10% can restore ovulation, regulate periods, and improve hirsutism. COCP improves hirsutism and acne over 6-9 months. If planning pregnancy - refer for preconception counselling, optimise weight, start folic acid 5mg (if BMI>30), and refer fertility clinic if no conception after 6-12 months of regular cycles.",
                "questions": [
                    {"id": "pcos_rotterdam", "type": "textarea", "label": "Rotterdam Criteria Met? (Need 2 of 3)", "required": True, "placeholder": "1. Oligo/anovulation: Yes/No\n2. Clinical/biochemical hyperandrogenism: Yes/No\n3. Polycystic ovaries on USS: Yes/No/Not assessed\nDiagnosis = PCOS / Awaiting results"},
                    {"id": "pcos_explanation", "type": "toggle", "label": "PCOS Explained? (Ovarian androgens → hirsutism/acne, anovulation, insulin resistance)", "required": True},
                    {"id": "pcos_lifestyle", "type": "toggle", "label": "Lifestyle Advice Given? (Weight loss 5-10%, diet, 30 mins exercise 5x/week, smoking cessation)", "required": True},
                    {"id": "pcos_spironolactone", "type": "toggle", "label": "Spironolactone Prescribed? (Hirsutism/Alopecia)", "required": False},
                    {"id": "pcos_spironolactone_dose", "type": "text", "label": "Spironolactone Dose", "required": False, "placeholder": "e.g., 50mg OD 2 weeks then 100mg OD for 6 months"},
                    {"id": "pcos_spironolactone_counselling", "type": "textarea", "label": "Spironolactone Counselling", "required": False, "placeholder": "Baseline renal function checked. Avoid trimethoprim. If combined with OCP or age >45 - check potassium after 6 weeks. Contraception essential (teratogenic). May take 6 months to see full effect."},
                    {"id": "pcos_cocp", "type": "toggle", "label": "COCP Offered? (Anti-androgenic: Dianette/Yasmin, regulates cycles, improves hirsutism/acne)", "required": False},
                    {"id": "pcos_metformin", "type": "toggle", "label": "Metformin Considered? (Menstrual regulation, subfertility, insulin resistance)", "required": False},
                    {"id": "pcos_metformin_detail", "type": "textarea", "label": "Metformin Details", "required": False, "placeholder": "e.g., 500mg OD with food, titrate up to 500mg TDS over several weeks. Warn GI side effects."},
                    {"id": "pcos_sleep_referral", "type": "toggle", "label": "Refer Respiratory for Sleep Studies? (OSA suspected)", "required": False},
                    {"id": "pcos_referral", "type": "single_select", "label": "Other Referrals", "required": False, "options": ["None", "Endocrinology", "Gynaecology", "Fertility Clinic", "Dietitian", "Dermatology"]}
                ]
            },
            {
                "title": "Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "pcos_followup_value", "type": "number", "label": "Follow-up in (Number)", "required": True, "placeholder": "e.g., 4"},
                    {"id": "pcos_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["weeks", "months"]}
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
    seed_pcos()