from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_osa():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category:
        category = Category(name="Respiratory")
        db.add(category)
        db.commit()

    t = {
        "title": "Obstructive Sleep Apnoea (OSA) Assessment",
        "description": "Screening and assessment for obstructive sleep apnoea using STOP-BANG criteria and Epworth Sleepiness Scale. Guides referral for sleep studies and driving advice.",
        "category": "Respiratory",
        "content": {
            "sections": [
                {
                    "title": "STOP-BANG Screening",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "osa_snoring",
                            "type": "toggle",
                            "label": "S — Do you SNORE loudly? (louder than talking / heard through door)",
                            "required": True,
                            "output_phrase": "Snoring: {value}"
                        },
                        {
                            "id": "osa_tired",
                            "type": "toggle",
                            "label": "T — Do you feel TIRED / fatigued during the day?",
                            "required": True,
                            "output_phrase": "Daytime tiredness: {value}"
                        },
                        {
                            "id": "osa_observed",
                            "type": "toggle",
                            "label": "O — Has anyone OBSERVED you stop breathing during sleep?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Witnessed apnoeas = high probability OSA. Urgent sleep study referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Observed apnoeas: {value}"
                        },
                        {
                            "id": "osa_pressure",
                            "type": "toggle",
                            "label": "P — Do you have high blood PRESSURE?",
                            "required": True,
                            "output_phrase": "Hypertension: {value}"
                        },
                        {
                            "id": "osa_bmi_stop",
                            "type": "toggle",
                            "label": "B — BMI >35 kg/m²?",
                            "required": True,
                            "output_phrase": "BMI >35: {value}"
                        },
                        {
                            "id": "osa_age_stop",
                            "type": "toggle",
                            "label": "A — AGE >50?",
                            "required": True,
                            "output_phrase": "Age >50: {value}"
                        },
                        {
                            "id": "osa_neck",
                            "type": "toggle",
                            "label": "N — NECK circumference >40cm?",
                            "required": False,
                            "output_phrase": "Neck >40cm: {value}"
                        },
                        {
                            "id": "osa_gender",
                            "type": "single_select",
                            "label": "G — GENDER",
                            "required": True,
                            "options": ["Male", "Female"],
                            "output_phrase": "Gender: {value}"
                        }
                    ]
                },
                {
                    "title": "Epworth Sleepiness Scale",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "osa_ess_score",
                            "type": "single_select",
                            "label": "ESS Score (chance of dozing: 0=never, 1=slight, 2=moderate, 3=high)",
                            "required": True,
                            "options": [
                                "0-5 — Normal",
                                "6-10 — Mild daytime sleepiness",
                                "11-15 — Moderate (consider referral)",
                                "16-24 — Severe (refer)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: ESS ≥11 = significant daytime sleepiness. Sleep study referral indicated.",
                            "red_flag_negative": "",
                            "output_phrase": "ESS score: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors & Impact",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "osa_driving",
                            "type": "toggle",
                            "label": "Sleepiness While DRIVING? (must notify DVLA if confirmed OSA + excessive sleepiness)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Sleepiness while driving = DANGEROUS. Must stop driving and notify DVLA if OSA confirmed. Advise not to drive until assessed.",
                            "red_flag_negative": "",
                            "output_phrase": "Driving risk: {value}"
                        },
                        {
                            "id": "osa_comorbidities",
                            "type": "multi_select",
                            "label": "Associated Conditions",
                            "required": True,
                            "options": [
                                "Obesity",
                                "Type 2 diabetes",
                                "Hypertension",
                                "AF",
                                "Heart failure",
                                "Stroke/TIA",
                                "Hypothyroidism",
                                "Acromegaly",
                                "None"
                            ],
                            "output_phrase": "Comorbidities: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Obstructive Sleep Apnoea (OSA)",
                        "Simple snoring (no apnoeas, normal ESS)",
                        "Obesity Hypoventilation Syndrome",
                        "Narcolepsy",
                        "Hypothyroidism",
                        "Insomnia / poor sleep hygiene",
                        "Shift work sleep disorder",
                        "Central sleep apnoea (rare — ?heart failure)"
                    ],
                    "questions": [
                        {
                            "id": "osa_stop_bang_score",
                            "type": "single_select",
                            "label": "STOP-BANG Score (≥3 = high risk OSA)",
                            "required": True,
                            "options": [
                                "0-2 — Low risk",
                                "3-4 — Intermediate risk",
                                "5-8 — High risk"
                            ],
                            "output_phrase": "STOP-BANG: {value}"
                        },
                        {
                            "id": "osa_diagnosis",
                            "type": "single_select",
                            "label": "Clinical Impression",
                            "required": True,
                            "options": [
                                "High probability OSA — refer sleep study",
                                "Possible OSA — refer sleep study",
                                "Simple snoring — conservative management",
                                "Other sleep disorder"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If high probability OSA (STOP-BANG ≥3 + ESS ≥11): Urgent referral for sleep study / respiratory physician. Driving: If excessive sleepiness at the wheel — must stop driving. Must notify DVLA/RSA if OSA confirmed. Treat modifiable factors: Weight loss (even 10% significantly reduces AHI), alcohol avoidance (worsens OSA), smoking cessation. CPAP is gold-standard treatment for moderate-severe OSA. Mandibular advancement devices for mild-moderate OSA or CPAP-intolerant. Do not delay referral if red flags present.",
                    "questions": [
                        {
                            "id": "osa_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Urgent sleep study referral",
                                "Routine sleep study referral",
                                "Conservative — weight loss, sleep hygiene, alcohol reduction",
                                "Not OSA — alternative diagnosis"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "osa_driving_advice",
                            "type": "toggle",
                            "label": "Driving Advice Given? (must stop if sleepy at wheel)",
                            "required": True,
                            "output_phrase": "Driving advice: {value}"
                        },
                        {
                            "id": "osa_weight_advice",
                            "type": "toggle",
                            "label": "Weight Loss / Lifestyle Advice Given?",
                            "required": False,
                            "output_phrase": "Lifestyle advice: {value}"
                        },
                        {
                            "id": "osa_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Refer sleep clinic. Review post-sleep study. Weight management programme.",
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
    seed_osa()