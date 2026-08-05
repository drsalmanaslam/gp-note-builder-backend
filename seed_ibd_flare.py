from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_ibd_flare():
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
        "title": "IBD Flare (Crohn's / Ulcerative Colitis)",
        "description": "Assessment of suspected IBD flare. Differentiates Crohn's from UC, identifies severe flare requiring hospital admission, and guides initial management including steroids and gastroenterology referral.",
        "category": "Gastrointestinal",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ibd_diagnosis",
                            "type": "single_select",
                            "label": "Known IBD Diagnosis",
                            "required": True,
                            "options": [
                                "Crohn's Disease",
                                "Ulcerative Colitis",
                                "Indeterminate Colitis",
                                "?First presentation — no diagnosis yet"
                            ],
                            "output_phrase": "IBD type: {value}"
                        },
                        {
                            "id": "ibd_duration",
                            "type": "text",
                            "label": "Duration of Current Flare",
                            "required": True,
                            "placeholder": "e.g., 5 days worsening",
                            "output_phrase": "Flare duration: {value}"
                        }
                    ]
                },
                {
                    "title": "Symptoms — Assess Severity",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ibd_stool_frequency",
                            "type": "single_select",
                            "label": "Stool Frequency / 24hrs",
                            "required": True,
                            "options": [
                                "<4 — mild",
                                "4-6 — moderate",
                                ">6 — severe",
                                ">10 — very severe / ?toxic megacolon"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: >6 stools/24h = severe flare. Admit if bloody, systemically unwell, or not responding to oral steroids.",
                            "red_flag_negative": "",
                            "output_phrase": "Stool frequency: {value}"
                        },
                        {
                            "id": "ibd_blood",
                            "type": "toggle",
                            "label": "Rectal Bleeding / Blood in Stool?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Significant rectal bleeding = severe UC flare. Admit if haemoglobin dropping or haemodynamically unstable.",
                            "red_flag_negative": "",
                            "output_phrase": "Rectal bleeding: {value}"
                        },
                        {
                            "id": "ibd_pain",
                            "type": "single_select",
                            "label": "Abdominal Pain",
                            "required": True,
                            "options": [
                                "Mild — cramping",
                                "Moderate — constant, affecting daily activities",
                                "Severe — unable to function, ?obstruction/perforation"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Severe abdominal pain + distension = ?toxic megacolon (UC) or obstruction (Crohn's). Emergency admission.",
                            "red_flag_negative": "",
                            "output_phrase": "Abdominal pain: {value}"
                        }
                    ]
                },
                {
                    "title": "Systemic & Extra-Intestinal",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ibd_systemic",
                            "type": "multi_select",
                            "label": "Systemic Symptoms",
                            "required": True,
                            "options": [
                                "Fever",
                                "Tachycardia",
                                "Weight loss",
                                "Nausea / vomiting",
                                "Reduced oral intake",
                                "Fatigue / malaise",
                                "None"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Fever + tachycardia + weight loss = severe flare. Admit for IV steroids and gastroenterology review.",
                            "red_flag_negative": "",
                            "output_phrase": "Systemic symptoms: {value}"
                        },
                        {
                            "id": "ibd_extra_intestinal",
                            "type": "multi_select",
                            "label": "Extra-Intestinal Manifestations",
                            "required": False,
                            "options": [
                                "Arthralgia / arthritis",
                                "Erythema nodosum / pyoderma gangrenosum",
                                "Uveitis / episcleritis",
                                "Primary sclerosing cholangitis (PSC)",
                                "Oral ulcers",
                                "None"
                            ],
                            "output_phrase": "Extra-intestinal: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment — Severe Flare Criteria",
                    "section_type": "assessment",
                    "differentials": [
                        "UC Flare — mild/moderate (manage outpatient with oral/topical steroids)",
                        "UC Flare — severe (admit — >6 stools, bleeding, systemic upset)",
                        "Crohn's Flare — mild/moderate (oral steroids ± immunomodulator)",
                        "Crohn's Flare — severe (admit — obstruction, abscess, fistula)",
                        "Toxic Megacolon (UC — dilatation >6cm, systemic toxicity)",
                        "Infective Colitis (C.diff, CMV — always rule out in IBD flare)",
                        "Irritable Bowel Syndrome (superimposed on IBD — no blood/systemic features)"
                    ],
                    "questions": [
                        {
                            "id": "ibd_severity",
                            "type": "single_select",
                            "label": "Severity",
                            "required": True,
                            "options": [
                                "Mild — <4 stools, no systemic symptoms",
                                "Moderate — 4-6 stools, mild systemic features",
                                "Severe — >6 stools, bleeding, fever, tachycardia (ADMIT)",
                                "Life-threatening — toxic megacolon, perforation, shock (EMERGENCY)"
                            ],
                            "output_phrase": "Severity: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "MILD-MODERATE FLARE (outpatient): Start Prednisolone 40mg OD (reducing course) OR Budesonide 9mg OD (Crohn's — ileal/right colon). Topical: Mesalazine enema/suppositories (UC proctitis). Continue maintenance therapy (Mesalazine, Azathioprine, Biologics). DO NOT prescribe NSAIDs or antibiotics (unless C.diff confirmed). Stool cultures + C.diff toxin before escalating therapy. SEVERE FLARE: Admit for IV Hydrocortisone 100mg QDS or IV Methylprednisolone. Gastroenterology review. Surgical review if toxic megacolon/perforation. If first presentation ?IBD: Urgent gastroenterology referral. Do not start steroids before discussion if possible (may mask diagnosis). Safety-net: Return immediately if severe pain, distension, vomiting, high fever, or bloody diarrhoea >6/day.",
                    "questions": [
                        {
                            "id": "ibd_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Outpatient — oral prednisolone + continue maintenance",
                                "Outpatient — topical (mesalazine enema/suppositories)",
                                "Admit — IV steroids + gastroenterology review",
                                "Emergency admission — ?toxic megacolon / perforation",
                                "Urgent gastroenterology referral (first presentation)",
                                "Routine gastroenterology review (mild)"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "ibd_steroids",
                            "type": "text",
                            "label": "Steroids Prescribed",
                            "required": False,
                            "placeholder": "e.g., Prednisolone 40mg OD — reducing by 5mg/week",
                            "output_phrase": "Steroids: {value}"
                        },
                        {
                            "id": "ibd_stool_tests",
                            "type": "toggle",
                            "label": "Stool Cultures + C.diff Toxin Sent? (before escalating therapy)",
                            "required": True,
                            "output_phrase": "Stool tests: {value}"
                        },
                        {
                            "id": "ibd_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if severe pain/distension/vomiting/severe bleeding)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "ibd_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 1 week. If no improvement on prednisolone, refer gastroenterology.",
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
    seed_ibd_flare()