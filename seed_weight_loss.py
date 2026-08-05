from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_weight_loss():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Gastrointestinal").first()
    if not category:
        category = Category(name="Gastrointestinal")
        db.add(category)
        db.commit()

    t = {
        "title": "Unintentional Weight Loss — Red Flag",
        "description": "Focused assessment for unintentional weight loss. Screens for malignancy, chronic disease, and psychosocial causes. Guides investigation and 2-week wait referral where indicated.",
        "category": "Gastrointestinal",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "wl_amount",
                            "type": "text",
                            "label": "Weight Loss — How Much and Over How Long?",
                            "required": True,
                            "placeholder": "e.g., 6kg over 2 months",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: >5% body weight in 6-12 months without explanation = significant. Needs full workup for malignancy/chronic disease.",
                            "red_flag_negative": "",
                            "output_phrase": "Weight loss: {value}"
                        },
                        {
                            "id": "wl_appetite",
                            "type": "single_select",
                            "label": "Appetite",
                            "required": True,
                            "options": [
                                "Normal — eating well, still losing weight",
                                "Reduced appetite",
                                "Normal appetite — suggests malabsorption/hypermetabolic state",
                                "Increased appetite — ?thyroid, diabetes"
                            ],
                            "output_phrase": "Appetite: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flag Symptoms — Malignancy Screen",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "wl_dysphagia",
                            "type": "toggle",
                            "label": "Dysphagia? (oesophageal cancer)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Dysphagia + weight loss = ?oesophageal cancer. Urgent OGD — 2-week wait referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Dysphagia: {value}"
                        },
                        {
                            "id": "wl_bleeding",
                            "type": "toggle",
                            "label": "Rectal Bleeding / Change in Bowel Habit? (colorectal cancer)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Rectal bleeding/change in bowel habit + weight loss = ?colorectal cancer. 2-week wait referral.",
                            "red_flag_negative": "",
                            "output_phrase": "GI bleeding: {value}"
                        },
                        {
                            "id": "wl_abdominal_mass",
                            "type": "toggle",
                            "label": "Abdominal Pain / Mass / Distension? (ovarian, pancreatic, gastric)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Abdominal mass + weight loss = ?malignancy. Urgent imaging + 2-week wait.",
                            "red_flag_negative": "",
                            "output_phrase": "Abdominal symptoms: {value}"
                        },
                        {
                            "id": "wl_haemoptysis",
                            "type": "toggle",
                            "label": "Haemoptysis / Persistent Cough? (lung cancer)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Haemoptysis/cough >3 weeks + weight loss = ?lung cancer. Urgent CXR + 2-week wait.",
                            "red_flag_negative": "",
                            "output_phrase": "Respiratory symptoms: {value}"
                        },
                        {
                            "id": "wl_night_sweats",
                            "type": "toggle",
                            "label": "Night Sweats / Fever? (?lymphoma, TB, infection)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Drenching night sweats + weight loss = ?lymphoma/TB. Urgent CXR, bloods, consider referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Night sweats: {value}"
                        }
                    ]
                },
                {
                    "title": "Other Causes — Systematic Enquiry",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "wl_bowels",
                            "type": "toggle",
                            "label": "Diarrhoea / Steatorrhoea? (?malabsorption, coeliac, IBD, pancreatic)",
                            "required": True,
                            "output_phrase": "Bowel symptoms: {value}"
                        },
                        {
                            "id": "wl_polyuria",
                            "type": "toggle",
                            "label": "Polyuria / Polydipsia? (?diabetes mellitus)",
                            "required": True,
                            "output_phrase": "Diabetes symptoms: {value}"
                        },
                        {
                            "id": "wl_tremor_heat",
                            "type": "toggle",
                            "label": "Heat Intolerance / Tremor / Palpitations? (?hyperthyroidism)",
                            "required": True,
                            "output_phrase": "Thyroid symptoms: {value}"
                        },
                        {
                            "id": "wl_mood",
                            "type": "toggle",
                            "label": "Low Mood / Anhedonia? (?depression as cause)",
                            "required": True,
                            "output_phrase": "Mood: {value}"
                        },
                        {
                            "id": "wl_alcohol",
                            "type": "toggle",
                            "label": "Excess Alcohol / Substance Use?",
                            "required": False,
                            "output_phrase": "Alcohol/substance: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "wl_lymph_nodes",
                            "type": "single_select",
                            "label": "Lymph Nodes",
                            "required": True,
                            "options": [
                                "No lymphadenopathy",
                                "Localised lymphadenopathy",
                                "Generalised lymphadenopathy — ?lymphoma",
                                "Not examined"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Generalised lymphadenopathy + weight loss = ?lymphoma. Urgent referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Lymph nodes: {value}"
                        },
                        {
                            "id": "wl_abdominal_exam",
                            "type": "single_select",
                            "label": "Abdominal Examination",
                            "required": True,
                            "options": [
                                "Normal",
                                "Mass palpable",
                                "Hepatomegaly",
                                "Ascites",
                                "Not examined"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Mass/hepatomegaly/ascites + weight loss = ?malignancy. Urgent imaging.",
                            "red_flag_negative": "",
                            "output_phrase": "Abdominal exam: {value}"
                        },
                        {
                            "id": "wl_bmi_current",
                            "type": "number",
                            "label": "Current BMI (kg/m²)",
                            "required": False,
                            "placeholder": "e.g., 18.5",
                            "output_phrase": "BMI: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Malignancy — GI, lung, lymphoma, gynaecological, urological",
                        "Hyperthyroidism",
                        "Diabetes mellitus (uncontrolled)",
                        "Malabsorption — coeliac disease, chronic pancreatitis, IBD",
                        "Chronic infection — TB, HIV",
                        "Depression / anxiety",
                        "Chronic organ failure — CKD, heart failure, COPD",
                        "Dementia (in elderly)"
                    ],
                    "questions": [
                        {
                            "id": "wl_diagnosis",
                            "type": "single_select",
                            "label": "Clinical Impression",
                            "required": True,
                            "options": [
                                "?Malignancy — 2-week wait referral",
                                "?Non-malignant organic cause — investigate",
                                "?Psychosocial cause — depression/stress",
                                "Mixed / unclear — full workup"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If red flags for malignancy: 2-week wait referral to appropriate specialty. Investigations: FBC, U&E, LFT, bone profile, CRP/ESR, TFTs, HbA1c, coeliac screen (tTG-IgA), CXR. Consider: FIT (if bowel symptoms), PSA (if male >50), LDH (if ?lymphoma). Review with results in 1-2 weeks. If all investigations normal and weight loss continues: consider CT TAP or urgent medical referral. Safety-net: Return if new red flags develop — dysphagia, bleeding, masses, night sweats, or further weight loss.",
                    "questions": [
                        {
                            "id": "wl_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "2-week wait cancer referral",
                                "Routine specialist referral",
                                "Bloods + CXR + review with results",
                                "Safety-net + watchful waiting",
                                "Treat underlying cause (e.g., depression, hyperthyroidism)"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "wl_investigations",
                            "type": "text",
                            "label": "Investigations Ordered",
                            "required": True,
                            "placeholder": "e.g., FBC, U&E, LFT, TFTs, HbA1c, coeliac screen, CXR",
                            "output_phrase": "Investigations: {value}"
                        },
                        {
                            "id": "wl_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if new red flags or further loss)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "wl_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review with bloods/CXR in 2 weeks. If ongoing loss and normal results, consider CT TAP.",
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
    seed_weight_loss()