from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_tennis_elbow():
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
        "title": "Tennis Elbow (Lateral Epicondylitis)",
        "description": "Assessment and management of lateral epicondylitis. Covers typical history, provocative tests, conservative measures, injection therapy, and when to refer.",
        "category": "Musculoskeletal",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "te_pain_location",
                            "type": "single_select",
                            "label": "Pain Location",
                            "required": True,
                            "options": [
                                "Lateral elbow / epicondyle (classic)",
                                "Radiates down forearm",
                                "Medial elbow (golfer's elbow)",
                                "Diffuse elbow pain"
                            ],
                            "output_phrase": "Pain location: {value}"
                        },
                        {
                            "id": "te_onset",
                            "type": "single_select",
                            "label": "Onset",
                            "required": True,
                            "options": [
                                "Gradual — over weeks (typical overuse)",
                                "After unaccustomed activity",
                                "Sudden — specific injury/trauma",
                                "No clear trigger"
                            ],
                            "output_phrase": "Onset: {value}"
                        },
                        {
                            "id": "te_aggravating",
                            "type": "multi_select",
                            "label": "Aggravating Activities",
                            "required": True,
                            "options": [
                                "Gripping / lifting",
                                "Wrist extension against resistance",
                                "Repetitive manual work",
                                "Sports (tennis, golf, DIY)",
                                "Computer / keyboard use",
                                "Shaking hands",
                                "Turning door handle"
                            ],
                            "output_phrase": "Aggravating: {value}"
                        },
                        {
                            "id": "te_occupation",
                            "type": "text",
                            "label": "Occupation / Repetitive Activity",
                            "required": False,
                            "placeholder": "e.g., Manual worker, painter, chef",
                            "output_phrase": "Occupation: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Alternative Diagnoses",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "te_neck_pain",
                            "type": "toggle",
                            "label": "Neck Pain / Radiating from C-spine? (?cervical radiculopathy)",
                            "required": True,
                            "output_phrase": "Neck pain: {value}"
                        },
                        {
                            "id": "te_clicking_locking",
                            "type": "toggle",
                            "label": "Clicking / Locking / Instability? (?loose body, instability)",
                            "required": True,
                            "output_phrase": "Mechanical symptoms: {value}"
                        },
                        {
                            "id": "te_night_pain",
                            "type": "toggle",
                            "label": "Night Pain / Constant Pain? (?infection, tumour, inflammatory)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Constant pain, night pain, or systemic symptoms = ?infection, tumour, inflammatory arthritis. Investigate further.",
                            "red_flag_negative": "",
                            "output_phrase": "Night pain: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "te_tenderness",
                            "type": "toggle",
                            "label": "Tenderness Over Lateral Epicondyle? (1-2cm distal to epicondyle)",
                            "required": True,
                            "output_phrase": "Lateral epicondyle tenderness: {value}"
                        },
                        {
                            "id": "te_cozen",
                            "type": "toggle",
                            "label": "Cozen's Test Positive? (resisted wrist extension with elbow extended — pain at lateral epicondyle)",
                            "required": False,
                            "output_phrase": "Cozen's test: {value}"
                        },
                        {
                            "id": "te_mill",
                            "type": "toggle",
                            "label": "Mill's Test Positive? (passive wrist flexion with elbow extended — pain)",
                            "required": False,
                            "output_phrase": "Mill's test: {value}"
                        },
                        {
                            "id": "te_grip",
                            "type": "single_select",
                            "label": "Grip Strength",
                            "required": False,
                            "options": [
                                "Normal",
                                "Reduced — pain-limited",
                                "Significantly reduced",
                                "Not tested"
                            ],
                            "output_phrase": "Grip: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Lateral Epicondylitis (Tennis Elbow) — extensor carpi radialis brevis tendinopathy",
                        "Medial Epicondylitis (Golfer's Elbow)",
                        "Cervical Radiculopathy (C6-C7) — neck pain, neurological signs",
                        "Elbow Osteoarthritis",
                        "Radial Tunnel Syndrome — pain more distal, no epicondylar tenderness",
                        "Olecranon Bursitis — posterior swelling",
                        "Referred Pain — shoulder or cervical spine"
                    ],
                    "questions": [
                        {
                            "id": "te_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Lateral Epicondylitis — typical",
                                "Lateral Epicondylitis — severe / chronic",
                                "Medial Epicondylitis (Golfer's Elbow)",
                                "Other — see differentials"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Condition is self-limiting — 80-90% resolve within 12 months with conservative treatment. First-line: Activity modification (avoid aggravating activities), simple analgesia (Paracetamol ± topical NSAID gel). Physiotherapy: Eccentric strengthening exercises, forearm extensor stretches, deep friction massage. Counterforce brace/strap may help short-term. If no improvement at 6-12 weeks: Consider corticosteroid injection — short-term relief but may increase recurrence long-term. Platelet-Rich Plasma (PRP) injections — some evidence for chronic cases. Refer orthopaedics if: >6-12 months despite conservative + injection, diagnostic uncertainty, or severe functional impairment. Surgery (extensor tendon release) is last resort. Safety-net: Return if worsening pain, new neurological symptoms, or no improvement with conservative care.",
                    "questions": [
                        {
                            "id": "te_management",
                            "type": "multi_select",
                            "label": "Management Advised",
                            "required": True,
                            "options": [
                                "Activity modification / rest from aggravating activities",
                                "Physiotherapy referral — eccentric exercises",
                                "Simple analgesia / topical NSAIDs",
                                "Counterforce brace / strap",
                                "Corticosteroid injection",
                                "Orthopaedic referral"
                            ],
                            "output_phrase": "Management: {value}"
                        },
                        {
                            "id": "te_injection",
                            "type": "toggle",
                            "label": "Corticosteroid Injection Given? (discuss short-term benefit vs recurrence risk)",
                            "required": False,
                            "output_phrase": "Injection: {value}"
                        },
                        {
                            "id": "te_physio",
                            "type": "toggle",
                            "label": "Physiotherapy Referral Made?",
                            "required": False,
                            "output_phrase": "Physio referral: {value}"
                        },
                        {
                            "id": "te_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 6-8 weeks. Physio + exercises. Consider injection if no improvement.",
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
    seed_tennis_elbow()