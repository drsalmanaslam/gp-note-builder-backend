from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hirsutism():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Hirsutism Assessment",
        "description": "Focused assessment for hirsutism including PCOS evaluation, hormonal workup, and management options from lifestyle to medical treatment.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "hirs_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 24"}
                ]
            },
            {
                "title": "Hair Growth Pattern",
                "section_type": "history",
                "questions": [
                    {"id": "hirs_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Gradual (since puberty)", "Recent onset (months)", "Rapidly progressive"]},
                    {"id": "hirs_progression", "type": "single_select", "label": "Progression", "required": True, "options": ["Stable", "Slowly worsening", "Rapidly worsening"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Rapidly progressive hirsutism with virilisation may indicate androgen-secreting tumour. Urgent investigation.", "red_flag_negative": ""},
                    {"id": "hirs_areas", "type": "multi_select", "label": "Areas of Excess Hair Growth", "required": True, "options": ["Face (upper lip, chin, sideburns)", "Chest", "Abdomen (linea alba)", "Lower back", "Upper arms", "Thighs", "Buttocks"]},
                    {"id": "hirs_impact", "type": "single_select", "label": "Psychosocial Impact", "required": True, "options": ["Minimal - coping well", "Moderate - affecting confidence", "Significant - affecting daily life/relationships", "Severe distress/depression"]},
                    {"id": "hirs_current_methods", "type": "multi_select", "label": "Current Hair Removal Methods", "required": True, "options": ["Shaving", "Waxing", "Threading", "Bleaching", "Depilatory creams", "Laser (private)", "Electrolysis", "Eflornithine cream", "None"]},
                    {"id": "hirs_method_satisfaction", "type": "toggle", "label": "Satisfied with Current Method?", "required": False}
                ]
            },
            {
                "title": "Menstrual History & PCOS Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "hirs_menarche", "type": "number", "label": "Age at Menarche", "required": True, "placeholder": "e.g., 13", "is_red_flag": True, "red_flag_positive": "RED FLAG: If <8 years from menarche - pelvic USS should NOT be used to diagnose PCOS (multi-follicular ovaries are normal).", "red_flag_negative": ""},
                    {"id": "hirs_cycle", "type": "single_select", "label": "Menstrual Cycle", "required": True, "options": ["Regular (21-35 days)", "Oligomenorrhoea (>35 days)", "Amenorrhoea (>6 months)", "Irregular"]},
                    {"id": "hirs_period_duration", "type": "number", "label": "Duration of Bleeding (days)", "required": False, "placeholder": "e.g., 5"},
                    {"id": "hirs_acne", "type": "toggle", "label": "Acne?", "required": True},
                    {"id": "hirs_scalp_hair_loss", "type": "toggle", "label": "Scalp Hair Thinning / Loss?", "required": False},
                    {"id": "hirs_weight_changes", "type": "toggle", "label": "Weight Gain / Difficulty Losing Weight?", "required": True},
                    {"id": "hirs_virilisation", "type": "multi_select", "label": "Signs of Virilisation", "required": True, "options": ["Deepened voice", "Increased muscle mass", "Clitoromegaly", "Breast atrophy", "Male-pattern baldness", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Virilisation suggests androgen-secreting tumour (ovarian/adrenal). Urgent investigation required.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Key History",
                "section_type": "history",
                "questions": [
                    {"id": "hirs_family_history", "type": "multi_select", "label": "Family History", "required": False, "options": ["PCOS", "Hirsutism", "Infertility", "Diabetes", "Congenital adrenal hyperplasia", "None"]},
                    {"id": "hirs_contraception", "type": "single_select", "label": "Current Contraception", "required": True, "options": ["None", "COCP", "POP", "Implant", "IUS", "Depo-Provera", "Barrier methods"]},
                    {"id": "hirs_pregnancy_plans", "type": "toggle", "label": "Planning Pregnancy?", "required": True},
                    {"id": "hirs_smoking", "type": "toggle", "label": "Smoking?", "required": False},
                    {"id": "hirs_alcohol", "type": "toggle", "label": "Alcohol?", "required": False},
                    {"id": "hirs_meds", "type": "multi_select", "label": "Medications / Supplements", "required": True, "options": ["Anabolic steroids", "Testosterone supplements", "Valproate", "Danazol", "Progestogen-only contraception", "OTC bodybuilding supplements", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hirs_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 32", "is_red_flag": True, "red_flag_positive": "RED FLAG: Raised BMI common in PCOS. Weight loss of even 5-10% can significantly improve symptoms.", "red_flag_negative": ""},
                    {"id": "hirs_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 128"},
                    {"id": "hirs_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 82"},
                    {"id": "hirs_acne_exam", "type": "toggle", "label": "Acne on Examination?", "required": False},
                    {"id": "hirs_acanthosis", "type": "toggle", "label": "Acanthosis Nigricans? (Insulin resistance)", "required": False},
                    {"id": "hirs_alopecia", "type": "toggle", "label": "Scalp Hair Loss (Androgenic Pattern)?", "required": False},
                    {"id": "hirs_abdominal_exam", "type": "toggle", "label": "Abdominal/Pelvic Mass?", "required": False},
                    {"id": "hirs_cushingoid", "type": "toggle", "label": "Cushingoid Features? (Striae, buffalo hump, central obesity)", "required": False}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "PCOS (most common cause)",
                    "Idiopathic Hirsutism",
                    "Congenital Adrenal Hyperplasia (Non-classical)",
                    "Cushing Syndrome",
                    "Androgen-Secreting Tumour (Ovarian/Adrenal)",
                    "Medication-Induced (Anabolic Steroids, Valproate)",
                    "Hypothyroidism",
                    "Hyperprolactinaemia",
                    "Familial Hirsutism",
                    "Acromegaly"
                ],
                "questions": [
                    {"id": "hirs_testosterone", "type": "number", "label": "Testosterone (nmol/L)", "required": False, "placeholder": "e.g., 3.2 (NR: <1.8)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Testosterone >5 nmol/L requires urgent investigation for androgen-secreting tumour.", "red_flag_negative": ""},
                    {"id": "hirs_fai", "type": "number", "label": "Free Androgen Index (FAI)", "required": False, "placeholder": "e.g., 8.5 (NR: <4.5)"},
                    {"id": "hirs_shbg", "type": "number", "label": "SHBG (nmol/L)", "required": False, "placeholder": "e.g., 18 (Low SHBG common in PCOS/insulin resistance)"},
                    {"id": "hirs_lh_fsh", "type": "text", "label": "LH : FSH Ratio", "required": False, "placeholder": "e.g., LH 18, FSH 5 (LH:FSH >2:1 suggests PCOS)"},
                    {"id": "hirs_bloods_ordered", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["Total Testosterone", "SHBG + Free Androgen Index", "LH, FSH", "TSH", "Prolactin", "HbA1c", "Lipid Profile", "17-OH Progesterone (if CAH suspected)", "DHEAS (adrenal source)", "Cortisol (if Cushing's suspected)"]},
                    {"id": "hirs_pelvic_uss", "type": "toggle", "label": "Pelvic Ultrasound? (>8 years from menarche)", "required": False},
                    {"id": "hirs_uss_result", "type": "single_select", "label": "USS Result", "required": False, "options": ["Pending", "Polycystic ovaries (PCOS morphology)", "Normal ovaries", "Ovarian mass", "Not indicated"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return for review after blood results. Return sooner if: rapid increase in hair growth, development of male-pattern baldness, deepening voice, increased muscle mass (virilisation), severe pelvic pain, or new menstrual irregularities. Weight loss of even 5-10% can significantly improve symptoms and hormone balance. Treatments take time - allow 6-9 months to see full effect of COCP or eflornithine. If using eflornithine: apply thin layer to affected areas twice daily, at least 8 hours apart. Benefits seen within 4-8 weeks. Discontinue if no improvement after 4 months. Laser hair removal: multiple sessions needed, not permanent but long-term reduction, usually not covered by HSE/NHS.",
                "questions": [
                    {"id": "hirs_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["PCOS-associated hirsutism", "Idiopathic hirsutism", "Medication-induced", "Suspected CAH", "Suspected Cushing's", "Uncertain - awaiting results"]},
                    {"id": "hirs_lifestyle", "type": "toggle", "label": "Lifestyle Advice Given? (Diet, exercise, 5-10% weight loss)", "required": True},
                    {"id": "hirs_mechanical", "type": "toggle", "label": "Mechanical Methods Discussed? (Shaving, waxing, threading, bleaching)", "required": False},
                    {"id": "hirs_eflornithine", "type": "toggle", "label": "Eflornithine Cream Prescribed? (Facial hirsutism, age ≥19, not pregnant)", "required": False},
                    {"id": "hirs_eflornithine_detail", "type": "textarea", "label": "Eflornithine Instructions", "required": False, "placeholder": "Apply thin layer to affected areas twice daily, 8 hours apart. Benefits 4-8 weeks. Discontinue if no improvement at 4 months. Not licensed <19 years or in pregnancy."},
                    {"id": "hirs_cocp", "type": "single_select", "label": "Combined Oral Contraceptive", "required": False, "options": ["Not indicated", "Offered - anti-androgenic COCP (e.g., Dianette, Yasmin)", "Offered - standard COCP", "Contraindicated", "Declined"]},
                    {"id": "hirs_cocp_counselling", "type": "textarea", "label": "COCP Counselling", "required": False, "placeholder": "Can help regulate periods and reduce hair growth. Takes 6-9 months for full effect on hirsutism. Discuss risks/benefits."},
                    {"id": "hirs_laser", "type": "toggle", "label": "Laser Hair Removal Discussed? (Long-term, not HSE/NHS funded)", "required": False},
                    {"id": "hirs_metformin", "type": "toggle", "label": "Metformin Considered? (PCOS with insulin resistance/impaired glucose)", "required": False},
                    {"id": "hirs_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None", "Endocrinology", "Gynaecology", "Dermatology", "Dietitian"]}
                ]
            },
            {
                "title": "Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "hirs_followup_value", "type": "number", "label": "Follow-up in (Number)", "required": True, "placeholder": "e.g., 4"},
                    {"id": "hirs_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["weeks", "months"]}
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
    seed_hirsutism()