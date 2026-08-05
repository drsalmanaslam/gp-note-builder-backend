from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_croup():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category:
        category = Category(name="Paediatrics")
        db.add(category)
        db.commit()

    t = {
        "title": "Croup (Acute Laryngotracheobronchitis)",
        "description": "Assessment and management of croup in children. Covers Westley Croup Score, severity grading, dexamethasone dosing, and red flags for hospital admission.",
        "category": "Paediatrics",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "croup_age",
                            "type": "number",
                            "label": "Age (typically 6 months — 3 years)",
                            "required": True,
                            "placeholder": "e.g., 2",
                            "output_phrase": "Age: {value} years"
                        },
                        {
                            "id": "croup_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms",
                            "required": True,
                            "options": [
                                "Barking cough (seal-like)",
                                "Stridor — inspiratory",
                                "Hoarse voice",
                                "Coryza / fever preceding",
                                "Respiratory distress",
                                "Worse at night"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        },
                        {
                            "id": "croup_duration",
                            "type": "text",
                            "label": "Duration & Progression",
                            "required": True,
                            "placeholder": "e.g., 1 day — started with coryza, now barking cough at night",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "croup_vaccination",
                            "type": "toggle",
                            "label": "Up to Date with Vaccinations? (including Hib)",
                            "required": True,
                            "output_phrase": "Vaccinations: {value}"
                        }
                    ]
                },
                {
                    "title": "Severity Assessment (Westley Croup Score)",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "croup_stridor",
                            "type": "single_select",
                            "label": "Stridor",
                            "required": True,
                            "options": [
                                "None",
                                "Only when agitated/crying",
                                "At rest — intermittent",
                                "At rest — continuous"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Stridor at rest = moderate-severe croup. Urgent admission if continuous or with recession.",
                            "red_flag_negative": "",
                            "output_phrase": "Stridor: {value}"
                        },
                        {
                            "id": "croup_recession",
                            "type": "single_select",
                            "label": "Chest Wall Recession",
                            "required": True,
                            "options": [
                                "None",
                                "Mild — subcostal/intercostal",
                                "Moderate — suprasternal",
                                "Severe — all areas + nasal flaring"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Moderate-severe recession = significant respiratory distress. Emergency admission.",
                            "red_flag_negative": "",
                            "output_phrase": "Recession: {value}"
                        },
                        {
                            "id": "croup_air_entry",
                            "type": "single_select",
                            "label": "Air Entry",
                            "required": True,
                            "options": [
                                "Normal",
                                "Decreased",
                                "Severely decreased / silent chest"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Decreased air entry / silent chest = near-complete obstruction. Call 999 immediately.",
                            "red_flag_negative": "",
                            "output_phrase": "Air entry: {value}"
                        },
                        {
                            "id": "croup_conscious",
                            "type": "single_select",
                            "label": "Conscious Level / Colour",
                            "required": True,
                            "options": [
                                "Alert, pink, normal",
                                "Restless / anxious",
                                "Drowsy / lethargic / cyanosed"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Drowsiness/cyanosis = impending respiratory failure. Call 999 immediately. Do not distress child.",
                            "red_flag_negative": "",
                            "output_phrase": "Conscious level: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment & Severity Grade",
                    "section_type": "assessment",
                    "differentials": [
                        "Croup — viral laryngotracheobronchitis (most common)",
                        "Epiglottitis (rare — toxic, drooling, no cough, tripod position)",
                        "Foreign body aspiration (sudden onset, afebrile)",
                        "Bacterial tracheitis (toxic, high fever, no response to adrenaline)",
                        "Angioedema / anaphylaxis",
                        "Retropharyngeal abscess"
                    ],
                    "questions": [
                        {
                            "id": "croup_severity",
                            "type": "single_select",
                            "label": "Severity (Westley Score)",
                            "required": True,
                            "options": [
                                "Mild (0-2) — barking cough, no stridor at rest",
                                "Moderate (3-5) — stridor at rest + mild recession",
                                "Severe (6-11) — stridor + marked recession + distress",
                                "Impending respiratory failure (>11) — decreased air entry, cyanosis, lethargy"
                            ],
                            "output_phrase": "Severity: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "MILD (Westley 0-2): Dexamethasone 0.15mg/kg PO single dose (or Prednisolone 1mg/kg). Manage at home. Advise: croup is worse at night, steam/humidified air not evidence-based but may comfort. MODERATE (3-5): Dexamethasone 0.15-0.6mg/kg PO + observe 1-2 hours. If no improvement, consider nebulised budesonide or admit. SEVERE (≥6): Call 999 / urgent admission. Nebulised adrenaline (0.5ml/kg of 1:1000, max 5ml) + Dexamethasone 0.6mg/kg PO/IM. Do not examine throat (may trigger laryngospasm). IMPENDING RESPIRATORY FAILURE: Call 999 immediately. High-flow O2. Minimise distress — do not examine throat. Parent/Carer advised: Return immediately if stridor at rest, recession, difficulty breathing, drowsy, or unable to drink.",
                    "questions": [
                        {
                            "id": "croup_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Home management — dexamethasone given, safety-net",
                                "Observe in practice 1-2h post-dexamethasone",
                                "Urgent paediatric admission",
                                "999 ambulance — severe / impending respiratory failure"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "croup_dexamethasone",
                            "type": "toggle",
                            "label": "Dexamethasone Given? (0.15mg/kg for mild, 0.6mg/kg for moderate-severe)",
                            "required": False,
                            "output_phrase": "Dexamethasone: {value}"
                        },
                        {
                            "id": "croup_adrenaline",
                            "type": "toggle",
                            "label": "Nebulised Adrenaline Given? (severe croup, prior to transfer)",
                            "required": False,
                            "output_phrase": "Adrenaline: {value}"
                        },
                        {
                            "id": "croup_safety_net",
                            "type": "toggle",
                            "label": "Parent/Carer Safety-Net Given? (return if stridor at rest / recession / drowsy)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "croup_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 24-48h if not improving. Admitted to paediatrics if moderate-severe.",
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
    seed_croup()