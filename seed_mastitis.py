from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_mastitis():
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
        "title": "Mastitis & Breast Abscess",
        "description": "Assessment of mastitis including lactational vs non-lactational, infection severity, abscess detection, and management including antibiotic choice and breastfeeding advice.",
        "category": "Women's Health",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "mas_lactating",
                            "type": "toggle",
                            "label": "Lactating / Breastfeeding?",
                            "required": True,
                            "output_phrase": "Lactating: {value}"
                        },
                        {
                            "id": "mas_postpartum",
                            "type": "text",
                            "label": "If Lactating — Weeks Postpartum?",
                            "required": False,
                            "placeholder": "e.g., 3 weeks",
                            "output_phrase": "Postpartum: {value}"
                        },
                        {
                            "id": "mas_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms",
                            "required": True,
                            "options": [
                                "Focal breast pain / tenderness",
                                "Erythema / warmth",
                                "Swelling / induration",
                                "Fever / rigors / flu-like symptoms",
                                "Nipple fissure / cracked nipple",
                                "Purulent nipple discharge",
                                "Palpable fluctuant mass (?abscess)"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        },
                        {
                            "id": "mas_duration",
                            "type": "text",
                            "label": "Duration of Symptoms",
                            "required": True,
                            "placeholder": "e.g., 2 days",
                            "output_phrase": "Duration: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "mas_abscess",
                            "type": "toggle",
                            "label": "Fluctuant Mass / Pointing Abscess?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Fluctuant mass = breast abscess. Refer same-day surgery/breast clinic for drainage. Antibiotics alone insufficient.",
                            "red_flag_negative": "",
                            "output_phrase": "Abscess: {value}"
                        },
                        {
                            "id": "mas_sepsis",
                            "type": "toggle",
                            "label": "Systemically Unwell? (high fever, rigors, tachycardia, hypotension)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Systemic sepsis = IV antibiotics required. Same-day hospital admission.",
                            "red_flag_negative": "",
                            "output_phrase": "Sepsis: {value}"
                        },
                        {
                            "id": "mas_inflammatory",
                            "type": "toggle",
                            "label": "Peau d'orange / Skin Changes Suggesting Inflammatory Breast Cancer?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Peau d'orange/breast skin changes + no response to antibiotics = ?inflammatory breast cancer. 2-week wait breast clinic.",
                            "red_flag_negative": "",
                            "output_phrase": "Skin changes: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "mas_location",
                            "type": "single_select",
                            "label": "Location",
                            "required": True,
                            "options": [
                                "Upper outer quadrant",
                                "Upper inner quadrant",
                                "Lower outer quadrant",
                                "Lower inner quadrant",
                                "Periareolar",
                                "Diffuse / whole breast"
                            ],
                            "output_phrase": "Location: {value}"
                        },
                        {
                            "id": "mas_nipple",
                            "type": "toggle",
                            "label": "Nipple Fissure / Crack Present? (portal of entry)",
                            "required": False,
                            "output_phrase": "Nipple fissure: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Lactational Mastitis (milk stasis + infection)",
                        "Non-Lactational Mastitis / Periductal Mastitis",
                        "Breast Abscess",
                        "Inflammatory Breast Cancer (urgent — peau d'orange, no fever, no response to antibiotics)",
                        "Simple Engorgement (bilateral, no erythema/fever)",
                        "Galactocoele (milk-filled cyst)",
                        "Fungal Infection (Candida — bilateral nipple pain, shiny skin)"
                    ],
                    "questions": [
                        {
                            "id": "mas_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Lactational Mastitis — early, no abscess",
                                "Lactational Mastitis — ?abscess",
                                "Breast Abscess — refer drainage",
                                "Non-Lactational Mastitis",
                                "?Inflammatory Breast Cancer — 2-week wait",
                                "Simple Engorgement"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If lactating: Continue breastfeeding/pumping — essential for resolution. Feed from affected side first. Ensure good latch and positioning. Warm compress before feeds, cold after. Antibiotics: Flucloxacillin 500mg QDS for 7 days (1st line). If penicillin-allergic: Clarithromycin 500mg BD. If abscess: Same-day referral for ultrasound-guided aspiration or surgical drainage. If no improvement in 48-72 hours: Re-examine — ?abscess or alternative diagnosis. Non-lactational: Same antibiotics + investigate underlying cause (duct ectasia, periductal mastitis). Safety-net: Return immediately if: worsening pain, increasing swelling, new fluctuant mass, high fever, or no improvement in 48h.",
                    "questions": [
                        {
                            "id": "mas_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Antibiotics + continue breastfeeding/pumping",
                                "Antibiotics + same-day abscess drainage referral",
                                "Hospital admission — IV antibiotics (severe/septic)",
                                "2-week wait breast clinic (?inflammatory cancer)",
                                "Reassurance + breastfeeding support only (engorgement)"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "mas_antibiotics",
                            "type": "text",
                            "label": "Antibiotics Prescribed",
                            "required": True,
                            "placeholder": "e.g., Flucloxacillin 500mg QDS 7 days",
                            "output_phrase": "Antibiotics: {value}"
                        },
                        {
                            "id": "mas_breastfeeding_advice",
                            "type": "toggle",
                            "label": "Breastfeeding/Pumping Advice Given? (continue, feed affected side first)",
                            "required": False,
                            "output_phrase": "Breastfeeding advice: {value}"
                        },
                        {
                            "id": "mas_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if no improvement in 48h / worsening)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "mas_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 48-72h. If no improvement, re-examine for abscess.",
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
    seed_mastitis()