from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_quinsy():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category:
        category = Category(name="ENT")
        db.add(category)
        db.commit()

    t = {
        "title": "Peritonsillar Abscess (Quinsy) — Urgent",
        "description": "Urgent assessment for suspected quinsy. Key differentiating features from tonsillitis, red flags for airway compromise, and management including same-day ENT referral.",
        "category": "ENT",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "quinsy_duration",
                            "type": "text",
                            "label": "Duration of Symptoms",
                            "required": True,
                            "placeholder": "e.g., 4 days — worsening despite antibiotics",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "quinsy_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms",
                            "required": True,
                            "options": [
                                "Severe unilateral sore throat",
                                "Odynophagia (pain swallowing) — severe",
                                "Drooling (unable to swallow saliva)",
                                "Trismus (difficulty opening mouth)",
                                "Hot potato voice (muffled speech)",
                                "Otalgia (referred ear pain)",
                                "Fever / rigors",
                                "Neck swelling"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        },
                        {
                            "id": "quinsy_antibiotics",
                            "type": "toggle",
                            "label": "Already on Antibiotics? (treatment failure suggests abscess)",
                            "required": True,
                            "output_phrase": "Prior antibiotics: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Airway Assessment",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "quinsy_drooling",
                            "type": "toggle",
                            "label": "Drooling / Unable to Swallow Saliva?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Drooling = inability to manage secretions = ?airway compromise. Call 999/ENT emergency.",
                            "red_flag_negative": "",
                            "output_phrase": "Drooling: {value}"
                        },
                        {
                            "id": "quinsy_stridor",
                            "type": "toggle",
                            "label": "Stridor / Respiratory Distress?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Stridor = airway emergency. Call 999 immediately. Do not examine throat — may precipitate complete obstruction.",
                            "red_flag_negative": "",
                            "output_phrase": "Stridor: {value}"
                        },
                        {
                            "id": "quinsy_trismus",
                            "type": "toggle",
                            "label": "Trismus (Unable to Open Mouth Fully)?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Trismus = parapharyngeal involvement. Same-day ENT referral for drainage.",
                            "red_flag_negative": "",
                            "output_phrase": "Trismus: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "quinsy_throat",
                            "type": "single_select",
                            "label": "Throat Examination (if safe to examine)",
                            "required": True,
                            "options": [
                                "Unilateral tonsillar swelling + uvula deviation to opposite side",
                                "Bilateral tonsillar swelling — no deviation",
                                "Unable to visualise (trismus / patient distress)",
                                "Not examined — airway concern"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Unilateral swelling + uvula deviation = quinsy until proven otherwise. Same-day ENT for drainage.",
                            "red_flag_negative": "",
                            "output_phrase": "Throat exam: {value}"
                        },
                        {
                            "id": "quinsy_neck",
                            "type": "single_select",
                            "label": "Neck — Lymphadenopathy / Swelling?",
                            "required": False,
                            "options": [
                                "Unilateral tender lymphadenopathy",
                                "Bilateral lymphadenopathy",
                                "Neck swelling/induration beyond tonsillar area",
                                "No lymphadenopathy"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Neck swelling beyond tonsillar area = ?spreading infection/parapharyngeal abscess. Emergency ENT.",
                            "red_flag_negative": "",
                            "output_phrase": "Neck: {value}"
                        },
                        {
                            "id": "quinsy_temp",
                            "type": "number",
                            "label": "Temperature (°C)",
                            "required": True,
                            "placeholder": "e.g., 38.8",
                            "output_phrase": "Temp: {value}°C"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Peritonsillar Abscess (Quinsy)",
                        "Severe Tonsillitis (no abscess)",
                        "Parapharyngeal Abscess",
                        "Retropharyngeal Abscess (children)",
                        "Epiglottitis (rare — airway emergency)",
                        "Glandular Fever (EBV)",
                        "Dental Abscess",
                        "Lemierre's Syndrome (rare — IJV thrombophlebitis)"
                    ],
                    "questions": [
                        {
                            "id": "quinsy_diagnosis",
                            "type": "single_select",
                            "label": "Clinical Impression",
                            "required": True,
                            "options": [
                                "Quinsy — same-day ENT referral",
                                "Severe tonsillitis — observe closely",
                                "Airway compromise — call 999",
                                "Other"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If quinsy suspected: Same-day ENT referral for incision and drainage OR needle aspiration. IV antibiotics (Benzylpenicillin + Metronidazole OR Co-amoxiclav). If no stridor/drooling and ENT unavailable same day: start oral Co-amoxiclav 625mg TDS + Metronidazole 400mg TDS. Analgesia: Paracetamol + Ibuprofen (if no contraindications). If diabetic or immunocompromised: lower threshold for admission. Return immediately if: difficulty breathing, stridor, increased swelling, unable to swallow fluids, or symptoms worsen despite treatment.",
                    "questions": [
                        {
                            "id": "quinsy_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "999 ambulance — airway compromise",
                                "Same-day ENT referral — drainage",
                                "Start antibiotics — ENT referral within 24h",
                                "Tonsillitis management — safety-net"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "quinsy_antibiotics_given",
                            "type": "text",
                            "label": "Antibiotics Prescribed",
                            "required": True,
                            "placeholder": "e.g., Co-amoxiclav 625mg TDS + Metronidazole 400mg TDS",
                            "output_phrase": "Antibiotics: {value}"
                        },
                        {
                            "id": "quinsy_safety_net",
                            "type": "toggle",
                            "label": "Airway Safety-Net Given? (return if breathing difficulty/stridor)",
                            "required": True,
                            "output_phrase": "Safety-net given: {value}"
                        },
                        {
                            "id": "quinsy_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., ENT assessment today. Review in 48 hours if not admitted.",
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
    seed_quinsy()