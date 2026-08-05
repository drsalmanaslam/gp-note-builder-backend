from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_fertility_concerns():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category:
        category = Category(name="Women's Health")
        db.add(category)
        db.commit()

    t = {
        "title": "Fertility Concerns — Initial Assessment",
        "description": "Initial assessment of couples presenting with fertility concerns. Covers duration of infertility, key history for both partners, basic investigations in primary care, and criteria for referral.",
        "category": "Women's Health",
        "content": {
            "sections": [
                {
                    "title": "Basic Information",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "fert_duration",
                            "type": "text",
                            "label": "Duration of Trying to Conceive",
                            "required": True,
                            "placeholder": "e.g., 18 months",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: >12 months (<35 years) or >6 months (≥35 years) = infertility. Start investigations and consider referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "fert_previous_pregnancy",
                            "type": "single_select",
                            "label": "Previous Pregnancies?",
                            "required": True,
                            "options": [
                                "No previous pregnancies (primary infertility)",
                                "Previous pregnancy — same partner",
                                "Previous pregnancy — different partner",
                                "Previous miscarriage(s)"
                            ],
                            "output_phrase": "Previous pregnancies: {value}"
                        }
                    ]
                },
                {
                    "title": "Female Partner History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "fert_female_age",
                            "type": "number",
                            "label": "Female Age",
                            "required": True,
                            "placeholder": "e.g., 34",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Age ≥35 = declining fertility. Investigate after 6 months (not 12). Refer earlier if other risk factors.",
                            "red_flag_negative": "",
                            "output_phrase": "Female age: {value}"
                        },
                        {
                            "id": "fert_menstrual",
                            "type": "single_select",
                            "label": "Menstrual Cycle",
                            "required": True,
                            "options": [
                                "Regular — 21-35 days (likely ovulatory)",
                                "Irregular — oligomenorrhoea",
                                "Amenorrhoea (>6 months no period)",
                                "Heavy / painful periods (?endometriosis/fibroids)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Irregular/absent periods = ?PCOS, hypothalamic amenorrhoea, POI. Needs investigation — may require earlier referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Menstrual cycle: {value}"
                        },
                        {
                            "id": "fert_pcos",
                            "type": "toggle",
                            "label": "Known PCOS / Endometriosis / Fibroids?",
                            "required": False,
                            "output_phrase": "Gynae conditions: {value}"
                        },
                        {
                            "id": "fert_pid",
                            "type": "toggle",
                            "label": "History of PID / STI / Ectopic / Pelvic Surgery?",
                            "required": False,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: History of PID/ectopic/pelvic surgery = ?tubal factor infertility. Early referral to fertility clinic.",
                            "red_flag_negative": "",
                            "output_phrase": "PID/pelvic history: {value}"
                        }
                    ]
                },
                {
                    "title": "Male Partner History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "fert_male_age",
                            "type": "number",
                            "label": "Male Age",
                            "required": False,
                            "placeholder": "e.g., 36",
                            "output_phrase": "Male age: {value}"
                        },
                        {
                            "id": "fert_male_history",
                            "type": "multi_select",
                            "label": "Male Risk Factors",
                            "required": False,
                            "options": [
                                "Undescended testis (cryptorchidism)",
                                "Testicular surgery / trauma / torsion",
                                "Mumps orchitis",
                                "STI history",
                                "Erectile dysfunction / ejaculatory problems",
                                "Occupational — heat/chemical exposure",
                                "Anabolic steroid use",
                                "Medications (sulfasalazine, finasteride, chemotherapy)",
                                "None"
                            ],
                            "output_phrase": "Male risk factors: {value}"
                        }
                    ]
                },
                {
                    "title": "General Health & Lifestyle",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "fert_bmi",
                            "type": "number",
                            "label": "BMI (both partners — ideally 19-25)",
                            "required": False,
                            "placeholder": "e.g., 28",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: BMI <19 or >30 = reduced fertility in both sexes. Weight optimisation is first-line management.",
                            "red_flag_negative": "",
                            "output_phrase": "BMI: {value}"
                        },
                        {
                            "id": "fert_smoking",
                            "type": "single_select",
                            "label": "Smoking (either partner)",
                            "required": True,
                            "options": [
                                "Neither smokes",
                                "Female smoker",
                                "Male smoker",
                                "Both smoke"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Smoking significantly reduces fertility and increases miscarriage risk. Smoking cessation referral for both.",
                            "red_flag_negative": "",
                            "output_phrase": "Smoking: {value}"
                        },
                        {
                            "id": "fert_alcohol",
                            "type": "toggle",
                            "label": "Excess Alcohol? (>14 units/week either partner)",
                            "required": False,
                            "output_phrase": "Alcohol: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment & Investigations",
                    "section_type": "assessment",
                    "differentials": [
                        "Ovulatory Dysfunction — PCOS, hypothalamic, POI, hyperprolactinaemia",
                        "Tubal Factor — PID, endometriosis, previous surgery",
                        "Male Factor — semen analysis abnormal",
                        "Unexplained Infertility — all investigations normal",
                        "Combined Factors"
                    ],
                    "questions": [
                        {
                            "id": "fert_diagnosis",
                            "type": "single_select",
                            "label": "Working Impression",
                            "required": True,
                            "options": [
                                "?Ovulatory dysfunction — check day 21 progesterone",
                                "?Tubal factor — refer for assessment",
                                "?Male factor — semen analysis",
                                "Mixed / unclear — full couple investigations",
                                "Unexplained (after investigations)"
                            ],
                            "output_phrase": "Impression: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Pre-conception advice: Folic acid 400mcg OD for female partner (5mg if BMI >30, diabetic, or on antiepileptics). Rubella immunity check. Lifestyle: smoking cessation, alcohol reduction, healthy BMI. Investigations in primary care (BOTH partners): Female — Day 21 progesterone (to confirm ovulation), FSH/LH, TFTs, prolactin, rubella serology. Consider pelvic ultrasound if ?PCOS/endometriosis. Male — Semen analysis (after 3-5 days abstinence). Refer fertility clinic if: female age ≥35 + >6 months trying, female age <35 + >12 months, known tubal/male factor/poor semen analysis, or anovulation after basic workup. Safety-net: Return if new symptoms (pain, irregular bleeding) or if pregnant — early booking.",
                    "questions": [
                        {
                            "id": "fert_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Basic investigations + lifestyle advice — review results",
                                "Refer fertility clinic (criteria met)",
                                "Pre-conception advice only (not yet meeting infertility criteria)",
                                "Urgent gynae referral (suspected pathology — mass, severe PID)"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "fert_investigations",
                            "type": "text",
                            "label": "Investigations Ordered",
                            "required": True,
                            "placeholder": "e.g., Day 21 progesterone, FSH/LH, TFTs, prolactin, semen analysis",
                            "output_phrase": "Investigations: {value}"
                        },
                        {
                            "id": "fert_folic_acid",
                            "type": "toggle",
                            "label": "Folic Acid 400mcg Prescribed?",
                            "required": True,
                            "output_phrase": "Folic acid: {value}"
                        },
                        {
                            "id": "fert_lifestyle",
                            "type": "toggle",
                            "label": "Lifestyle Advice Given? (smoking, alcohol, BMI, timing intercourse)",
                            "required": True,
                            "output_phrase": "Lifestyle advice: {value}"
                        },
                        {
                            "id": "fert_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review with bloods + semen analysis results in 4-6 weeks. Refer if abnormal.",
                            "output_phrase": "Follow-up: {value}"
                        }
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(
        Template.title == t["title"],
        Template.created_by == admin.id
    ).first()

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
    seed_fertility_concerns()