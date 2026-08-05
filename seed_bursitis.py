from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_bursitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category:
        category = Category(name="Musculoskeletal")
        db.add(category)
        db.commit()

    t = {
        "title": "Bursitis",
        "description": "Assessment of common bursitis presentations (olecranon, trochanteric, prepatellar, subacromial). Covers differentiating from infection, management including aspiration and injection.",
        "category": "Musculoskeletal",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "bur_location",
                            "type": "single_select",
                            "label": "Location",
                            "required": True,
                            "options": [
                                "Olecranon (elbow)",
                                "Prepatellar (knee — housemaid's knee)",
                                "Infrapatellar (clergyman's knee)",
                                "Trochanteric (hip)",
                                "Subacromial (shoulder)",
                                "Retrocalcaneal (Achilles)",
                                "Other"
                            ],
                            "output_phrase": "Location: {value}"
                        },
                        {
                            "id": "bur_onset",
                            "type": "single_select",
                            "label": "Onset",
                            "required": True,
                            "options": [
                                "Acute — hours/days",
                                "Gradual — weeks",
                                "Chronic — months",
                                "Recurrent episodes"
                            ],
                            "output_phrase": "Onset: {value}"
                        },
                        {
                            "id": "bur_cause",
                            "type": "multi_select",
                            "label": "Likely Cause",
                            "required": True,
                            "options": [
                                "Pressure / kneeling (prepatellar)",
                                "Repetitive friction / leaning on elbow",
                                "Trauma / direct blow",
                                "Overuse / running (trochanteric, retrocalcaneal)",
                                "Inflammatory arthritis (gout, RA)",
                                "Idiopathic",
                                "Unknown"
                            ],
                            "output_phrase": "Cause: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Septic Bursitis",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "bur_redness",
                            "type": "toggle",
                            "label": "Overlying Erythema / Warmth?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Erythema + warmth + swelling = ?septic bursitis. Aspirate for culture. Do NOT inject steroids into potentially infected bursa.",
                            "red_flag_negative": "",
                            "output_phrase": "Erythema: {value}"
                        },
                        {
                            "id": "bur_fever",
                            "type": "toggle",
                            "label": "Fever / Systemic Symptoms?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Fever + bursitis = septic until proven otherwise. Aspirate + send for MC&S. Start antibiotics. Refer if severe.",
                            "red_flag_negative": "",
                            "output_phrase": "Fever: {value}"
                        },
                        {
                            "id": "bur_wound",
                            "type": "toggle",
                            "label": "Overlying Skin Break / Wound? (portal of entry for infection)",
                            "required": True,
                            "output_phrase": "Skin break: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "bur_swelling",
                            "type": "single_select",
                            "label": "Swelling",
                            "required": True,
                            "options": [
                                "Fluctuant — discrete, well-defined",
                                "Diffuse — ill-defined",
                                "Firm / solid — ?chronic",
                                "Mild / minimal"
                            ],
                            "output_phrase": "Swelling: {value}"
                        },
                        {
                            "id": "bur_pain_rom",
                            "type": "single_select",
                            "label": "Pain on Range of Motion?",
                            "required": True,
                            "options": [
                                "Painful in all directions (suggests bursitis)",
                                "Pain only in specific arc (suggests tendinopathy)",
                                "Minimal pain — full ROM",
                                "Unable to move due to pain"
                            ],
                            "output_phrase": "ROM: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Aseptic Bursitis — mechanical / overuse / inflammatory",
                        "Septic Bursitis — erythema, warmth, fever, elevated WCC/CRP",
                        "Gout / Pseudogout — acute, red, hot, crystals on aspiration",
                        "Rheumatoid Arthritis — other joints affected, symmetrical",
                        "Cellulitis — overlying skin infection without discrete fluctuance",
                        "Tendinopathy — pain on resisted movement, not passive",
                        "Bursal Cyst / Ganglion"
                    ],
                    "questions": [
                        {
                            "id": "bur_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Aseptic Bursitis — conservative / injection",
                                "?Septic Bursitis — aspirate + antibiotics",
                                "Gouty Bursitis — aspirate, treat gout",
                                "Chronic Bursitis — refer if persistent",
                                "Other"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "ASEPTIC: RICE (Rest, Ice, Compression, Elevation). NSAIDs (Ibuprofen 400mg TDS or Naproxen 500mg BD) if no contraindications. Avoid aggravating activity/pressure. If persistent >2 weeks or severe: Aspiration (send fluid for MC&S + crystals). Corticosteroid injection (e.g., Methylprednisolone 40mg) — after infection excluded. SEPTIC: Aspirate for MC&S. Antibiotics: Flucloxacillin 500mg QDS (or Clarithromycin if penicillin-allergic). If systemically unwell or diabetic/immunocompromised: Admit for IV antibiotics. Refer orthopaedics if: recurrent, chronic (>3 months), or failed conservative management. Safety-net: Return if increasing redness, warmth, fever, or no improvement in 48h on antibiotics.",
                    "questions": [
                        {
                            "id": "bur_management",
                            "type": "single_select",
                            "label": "Management",
                            "required": True,
                            "options": [
                                "Conservative — RICE + NSAIDs",
                                "Aspiration ± steroid injection (aseptic)",
                                "Aspiration + antibiotics (?septic)",
                                "Antibiotics only (mild septic, no aspiration)",
                                "Refer orthopaedics (chronic/recurrent)",
                                "Admit — IV antibiotics (severe septic)"
                            ],
                            "output_phrase": "Management: {value}"
                        },
                        {
                            "id": "bur_aspiration",
                            "type": "toggle",
                            "label": "Aspiration Performed? (send fluid for MC&S + crystals)",
                            "required": False,
                            "output_phrase": "Aspirated: {value}"
                        },
                        {
                            "id": "bur_antibiotics",
                            "type": "text",
                            "label": "Antibiotics (if septic suspected)",
                            "required": False,
                            "placeholder": "e.g., Flucloxacillin 500mg QDS 7 days",
                            "output_phrase": "Antibiotics: {value}"
                        },
                        {
                            "id": "bur_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if worsening redness/fever/no improvement)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "bur_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 1 week. If aspirated, check MC&S results. If no improvement, refer.",
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
    seed_bursitis()