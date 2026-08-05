from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_bronchiolitis():
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
        "title": "Bronchiolitis",
        "description": "Assessment and management of bronchiolitis in infants. Covers severity grading, feeding assessment, red flags for admission, and supportive care advice.",
        "category": "Paediatrics",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "bronch_age",
                            "type": "number",
                            "label": "Age (typically <12 months, peak 3-6 months)",
                            "required": True,
                            "placeholder": "e.g., 4 months",
                            "output_phrase": "Age: {value} months"
                        },
                        {
                            "id": "bronch_duration",
                            "type": "text",
                            "label": "Duration of Symptoms",
                            "required": True,
                            "placeholder": "e.g., 3 days — started with coryza, now cough + breathing difficulty",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "bronch_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms",
                            "required": True,
                            "options": [
                                "Coryza / runny nose (prodrome)",
                                "Dry wheezy cough",
                                "Increased work of breathing",
                                "Grunting",
                                "Apnoeas (RED FLAG — especially <6 weeks)",
                                "Poor feeding",
                                "Lethargy / irritable",
                                "Fever (usually <38.5°C)"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        }
                    ]
                },
                {
                    "title": "Feeding & Hydration (critical assessment)",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "bronch_feeding",
                            "type": "single_select",
                            "label": "Feeding — Last 24 Hours",
                            "required": True,
                            "options": [
                                "Normal — feeding well, no reduction",
                                "Reduced — taking 50-75% of normal",
                                "Significantly reduced — <50% of normal",
                                "Not feeding / unable to feed"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: <50% normal feeds or unable to feed = admit. Infants decompensate quickly with dehydration.",
                            "red_flag_negative": "",
                            "output_phrase": "Feeding: {value}"
                        },
                        {
                            "id": "bronch_wet_nappies",
                            "type": "single_select",
                            "label": "Wet Nappies — Last 12 Hours",
                            "required": True,
                            "options": [
                                "Normal — 3+ wet nappies",
                                "Reduced — 1-2",
                                "None / dry — <1 in 12 hours"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: <2 wet nappies in 12h = dehydration. Admit for NG/IV fluids.",
                            "red_flag_negative": "",
                            "output_phrase": "Wet nappies: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination — Severity Assessment",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "bronch_rr",
                            "type": "number",
                            "label": "Respiratory Rate (breaths/min)",
                            "required": True,
                            "placeholder": "e.g., 55",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: RR >60/min (any age) or >70/min (infants) = severe respiratory distress. Admit.",
                            "red_flag_negative": "",
                            "output_phrase": "RR: {value}/min"
                        },
                        {
                            "id": "bronch_sats",
                            "type": "number",
                            "label": "O2 Saturations (%) on Air",
                            "required": True,
                            "placeholder": "e.g., 93",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: SpO2 ≤92% on air = admit for oxygen. SpO2 ≤90% = emergency.",
                            "red_flag_negative": "",
                            "output_phrase": "SpO2: {value}%"
                        },
                        {
                            "id": "bronch_recession",
                            "type": "single_select",
                            "label": "Chest Recession",
                            "required": True,
                            "options": [
                                "None / mild",
                                "Moderate — subcostal/intercostal",
                                "Severe — suprasternal + nasal flaring + head bobbing"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Severe recession/head bobbing/nasal flaring = impending respiratory failure. Admit immediately.",
                            "red_flag_negative": "",
                            "output_phrase": "Recession: {value}"
                        },
                        {
                            "id": "bronch_auscultation",
                            "type": "single_select",
                            "label": "Auscultation",
                            "required": True,
                            "options": [
                                "Fine end-inspiratory crackles + wheeze (typical)",
                                "Wheeze only",
                                "Reduced air entry",
                                "Silent chest (ominous)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Reduced air entry/silent chest = severe obstruction / exhaustion. Emergency admission.",
                            "red_flag_negative": "",
                            "output_phrase": "Auscultation: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors for Severe Disease",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "bronch_risk",
                            "type": "multi_select",
                            "label": "Risk Factors",
                            "required": True,
                            "options": [
                                "Age <6 weeks (highest risk for apnoeas)",
                                "Prematurity (<32 weeks)",
                                "Congenital heart disease",
                                "Chronic lung disease / BPD",
                                "Immunodeficiency",
                                "Neuromuscular disease",
                                "Down syndrome",
                                "None"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: High-risk infant = lower threshold for admission. Discuss with paediatric team even if mildly unwell.",
                            "red_flag_negative": "",
                            "output_phrase": "Risk factors: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Bronchiolitis (RSV — most common, November-March)",
                        "Viral-induced wheeze (older infant/toddler, recurrent, family history atopy)",
                        "Asthma (unusual <12 months — consider if recurrent wheeze + eczema/allergy)",
                        "Pneumonia (focal crackles, higher fever, CXR changes)",
                        "Foreign body aspiration (sudden onset, asymmetrical breath sounds)",
                        "Heart failure (hepatomegaly, murmur, poor weight gain)",
                        "Pertussis (paroxysmal cough, whoop, apnoea)"
                    ],
                    "questions": [
                        {
                            "id": "bronch_severity",
                            "type": "single_select",
                            "label": "Severity",
                            "required": True,
                            "options": [
                                "Mild — feeding well, RR normal/mildly raised, no recession, SpO2 >95%",
                                "Moderate — reduced feeds, RR raised, mild-moderate recession, SpO2 92-95%",
                                "Severe — not feeding, RR >60, marked recession, SpO2 ≤92% (ADMIT)",
                                "Life-threatening — apnoeas, exhaustion, silent chest, SpO2 <90% (EMERGENCY)"
                            ],
                            "output_phrase": "Severity: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "MILD (manage at home): Supportive care only. Nose suction/saline drops before feeds. Smaller, more frequent feeds. Monitor wet nappies. Paracetamol if fever/distressed. No routine bronchodilators, steroids, antibiotics, or chest physio (NICE — not recommended). Advise: illness peaks day 3-5, cough may persist 2-4 weeks. MODERATE: Consider admission if feeding <50%, RR >60, SpO2 <95%, or high-risk infant. Discuss with paediatrics. SEVERE: Admit for oxygen, NG feeds, and monitoring. Safety-net: Return immediately if: apnoea/cyanosis, grunting, marked recession, <50% feeds, <2 wet nappies in 12h, or parental concern. Do not smoke around infant.",
                    "questions": [
                        {
                            "id": "bronch_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Home — supportive care + safety-net",
                                "Home — with close follow-up (moderate, high-risk)",
                                "Admit — paediatric ward",
                                "Emergency admission — HDU/ICU (severe/life-threatening)",
                                "Discuss with paediatrics (borderline)"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "bronch_nasal_suction",
                            "type": "toggle",
                            "label": "Nasal Saline / Suction Advised? (before feeds)",
                            "required": False,
                            "output_phrase": "Nasal care: {value}"
                        },
                        {
                            "id": "bronch_feeding_advice",
                            "type": "toggle",
                            "label": "Feeding Advice Given? (smaller, more frequent feeds, monitor wet nappies)",
                            "required": True,
                            "output_phrase": "Feeding advice: {value}"
                        },
                        {
                            "id": "bronch_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if apnoea/cyanosis/grunting/<50% feeds/<2 wet nappies)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "bronch_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 24-48h if not improving. If moderate, daily phone check. Admit if deteriorating.",
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
    seed_bronchiolitis()