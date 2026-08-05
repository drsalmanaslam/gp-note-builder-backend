from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_plantar_fasciitis():
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
        "title": "Plantar Fasciitis",
        "description": "Assessment and management of plantar fasciitis. Covers typical history, red flags for alternative diagnoses, conservative measures, and when to refer.",
        "category": "Musculoskeletal",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "pf_pain_location",
                            "type": "single_select",
                            "label": "Pain Location",
                            "required": True,
                            "options": [
                                "Medial heel / plantar fascia origin (classic)",
                                "Diffuse heel pain",
                                "Arch of foot",
                                "Bilateral"
                            ],
                            "output_phrase": "Pain location: {value}"
                        },
                        {
                            "id": "pf_pain_pattern",
                            "type": "single_select",
                            "label": "Pain Pattern",
                            "required": True,
                            "options": [
                                "Worst with first steps in morning — improves with activity (classic)",
                                "Worse with prolonged standing/walking",
                                "Constant pain — not relieved by rest",
                                "Pain at rest / night"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Constant pain, night pain, or pain at rest = ?stress fracture, infection, tumour. Investigate further.",
                            "red_flag_negative": "",
                            "output_phrase": "Pain pattern: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "pf_risk_factors",
                            "type": "multi_select",
                            "label": "Risk Factors",
                            "required": True,
                            "options": [
                                "Prolonged standing / walking (occupation)",
                                "Recent increase in activity / training",
                                "Obesity / overweight",
                                "Flat feet (pes planus) / high arches (pes cavus)",
                                "Inappropriate footwear",
                                "Tight calf muscles / Achilles",
                                "Age 40-60",
                                "None identified"
                            ],
                            "output_phrase": "Risk factors: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "pf_tenderness",
                            "type": "single_select",
                            "label": "Point of Maximum Tenderness",
                            "required": True,
                            "options": [
                                "Medial calcaneal tuberosity (plantar fascia origin)",
                                "Mid-foot / arch",
                                "Posterior heel (Achilles insertion)",
                                "Diffuse / non-specific"
                            ],
                            "output_phrase": "Tenderness: {value}"
                        },
                        {
                            "id": "pf_windlass",
                            "type": "toggle",
                            "label": "Windlass Test Positive? (passive dorsiflexion of toes increases pain)",
                            "required": False,
                            "output_phrase": "Windlass test: {value}"
                        },
                        {
                            "id": "pf_calf_tightness",
                            "type": "toggle",
                            "label": "Calf / Achilles Tightness?",
                            "required": False,
                            "output_phrase": "Calf tightness: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Plantar Fasciitis",
                        "Calcaneal Stress Fracture",
                        "Tarsal Tunnel Syndrome",
                        "Achilles Tendinopathy",
                        "Fat Pad Atrophy",
                        "Baxter's Nerve Entrapment",
                        "Seronegative Arthropathy (enthesitis)",
                        "Gout"
                    ],
                    "questions": [
                        {
                            "id": "pf_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Plantar Fasciitis — typical history",
                                "Plantar Fasciitis — atypical features, consider imaging",
                                "Other — see differentials"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Condition is self-limiting in 80-90% within 12 months with conservative treatment. First-line: Calf stretches (3x/day, hold 30s), plantar fascia stretch, ice bottle massage, supportive footwear (avoid flat shoes, walking barefoot), weight loss if BMI >25. Second-line: Physiotherapy referral, night splints, silicone heel cups/orthotics. Persistent >6 months despite conservative measures: Consider corticosteroid injection (ultrasound-guided preferred — risk of fat pad atrophy and plantar fascia rupture). Extracorporeal shockwave therapy (ESWT) if available. Refer orthopaedics if >12 months and failed all above. Surgery (plantar fascia release) rarely needed. Return if: worsening pain, new night pain, or no improvement after 6 weeks of exercises.",
                    "questions": [
                        {
                            "id": "pf_management",
                            "type": "multi_select",
                            "label": "Management Advised",
                            "required": True,
                            "options": [
                                "Calf/plantar fascia stretches",
                                "Ice bottle massage",
                                "Supportive footwear advice",
                                "Weight loss advice",
                                "Simple analgesia (paracetamol/NSAIDs)",
                                "Physiotherapy referral",
                                "Night splint / orthotics",
                                "Corticosteroid injection",
                                "Orthopaedic referral"
                            ],
                            "output_phrase": "Management: {value}"
                        },
                        {
                            "id": "pf_injection",
                            "type": "toggle",
                            "label": "Corticosteroid Injection Given? (discuss risk of fat pad atrophy/rupture)",
                            "required": False,
                            "output_phrase": "Injection: {value}"
                        },
                        {
                            "id": "pf_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 6 weeks. Physio referral sent. If no improvement consider injection.",
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
    seed_plantar_fasciitis()