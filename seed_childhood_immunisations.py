from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_childhood_immunisations():
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
        "title": "Childhood Immunisations — Routine Schedule",
        "description": "Template for childhood vaccination visits. Covers the Irish routine immunisation schedule, contraindications, catch-up guidance, and documentation of consent and vaccine administration.",
        "category": "Paediatrics",
        "content": {
            "sections": [
                {
                    "title": "Child Details & Consent",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "vax_age",
                            "type": "number",
                            "label": "Child's Age (months/years)",
                            "required": True,
                            "placeholder": "e.g., 2 months",
                            "output_phrase": "Age: {value}"
                        },
                        {
                            "id": "vax_visit",
                            "type": "single_select",
                            "label": "Scheduled Visit",
                            "required": True,
                            "options": [
                                "2 months — 6-in-1 + MenB + Rotavirus",
                                "4 months — 6-in-1 + MenB + Rotavirus",
                                "6 months — 6-in-1 + MenC",
                                "12 months — MMR + MenB",
                                "13 months — Hib/MenC + PCV",
                                "4-5 years — 4-in-1 + MMR",
                                "11-14 years — Tdap + MenACWY + HPV",
                                "Catch-up / delayed schedule",
                                "Other"
                            ],
                            "output_phrase": "Visit: {value}"
                        },
                        {
                            "id": "vax_consent",
                            "type": "toggle",
                            "label": "Parental/Guardian Consent Obtained? (verbal or written)",
                            "required": True,
                            "output_phrase": "Consent: {value}"
                        }
                    ]
                },
                {
                    "title": "Pre-Vaccination Assessment — Contraindications",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "vax_unwell",
                            "type": "toggle",
                            "label": "Acutely Unwell Today? (fever >38°C — defer until recovered)",
                            "required": True,
                            "output_phrase": "Unwell: {value}"
                        },
                        {
                            "id": "vax_allergy",
                            "type": "single_select",
                            "label": "Previous Allergic Reaction to Vaccines?",
                            "required": True,
                            "options": [
                                "No previous reaction",
                                "Mild — local redness/swelling",
                                "Moderate — fever, irritability",
                                "Severe — anaphylaxis (CONTRANDICATED — discuss with paediatrician)",
                                "Egg allergy (MMR safe — egg-free)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Previous anaphylaxis to vaccine or vaccine component = contraindication. Discuss with paediatric immunologist before vaccinating.",
                            "red_flag_negative": "",
                            "output_phrase": "Allergy: {value}"
                        },
                        {
                            "id": "vax_immunocompromised",
                            "type": "toggle",
                            "label": "Immunocompromised? (chemotherapy, high-dose steroids, transplant, primary immunodeficiency)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Live vaccines (MMR, BCG, rotavirus, varicella) CONTRAINDICATED in immunocompromised. Inactivated vaccines safe but may have reduced efficacy. Discuss with specialist.",
                            "red_flag_negative": "",
                            "output_phrase": "Immunocompromised: {value}"
                        },
                        {
                            "id": "vax_seizures",
                            "type": "toggle",
                            "label": "History of Seizures / Febrile Convulsions? (not contraindicated — advise paracetamol if history of febrile seizures)",
                            "required": False,
                            "output_phrase": "Seizure history: {value}"
                        },
                        {
                            "id": "vax_bleeding",
                            "type": "toggle",
                            "label": "Bleeding Disorder / On Anticoagulants? (IM injection — apply firm pressure 5 min)",
                            "required": False,
                            "output_phrase": "Bleeding risk: {value}"
                        }
                    ]
                },
                {
                    "title": "Vaccines Given Today",
                    "section_type": "plan",
                    "questions": [
                        {
                            "id": "vax_given",
                            "type": "multi_select",
                            "label": "Vaccines Administered",
                            "required": True,
                            "options": [
                                "6-in-1 (DTaP/IPV/Hib/HepB)",
                                "MenB (Bexsero)",
                                "Rotavirus (Rotarix — oral)",
                                "MenC (NeisVac-C)",
                                "MMR (Priorix)",
                                "Hib/MenC (Menitorix)",
                                "PCV (Prevenar 13)",
                                "4-in-1 (DTaP/IPV)",
                                "Tdap (Boostrix)",
                                "MenACWY (Nimenrix)",
                                "HPV (Gardasil 9)",
                                "Other"
                            ],
                            "output_phrase": "Vaccines given: {value}"
                        },
                        {
                            "id": "vax_batch",
                            "type": "text",
                            "label": "Batch Numbers + Expiry",
                            "required": True,
                            "placeholder": "e.g., 6-in-1: A21CB123A Exp 06/27, MenB: BX789 Exp 03/27",
                            "output_phrase": "Batch: {value}"
                        },
                        {
                            "id": "vax_site",
                            "type": "single_select",
                            "label": "Administration Site",
                            "required": True,
                            "options": [
                                "Right thigh",
                                "Left thigh",
                                "Right deltoid (older children)",
                                "Left deltoid (older children)",
                                "Oral (rotavirus)",
                                "Multiple sites"
                            ],
                            "output_phrase": "Site: {value}"
                        }
                    ]
                },
                {
                    "title": "Post-Vaccination Advice",
                    "section_type": "plan",
                    "safety_netting": "Common side effects (resolve within 24-48h): Mild fever (give Paracetamol 15mg/kg 4-6 hourly if needed), redness/swelling at injection site, irritability, reduced feeding. Rotavirus: Mild diarrhoea/vomiting possible. MMR: Fever/rash may occur 7-10 days later (not contagious). When to seek urgent help: High fever >39°C unresponsive to paracetamol, persistent crying >3 hours, seizures/convulsions, limp/unresponsive, or signs of allergic reaction (urticaria, facial swelling, breathing difficulty — extremely rare, usually within minutes). Record all vaccines in child's immunisation passport and practice IT system. Schedule next visit.",
                    "questions": [
                        {
                            "id": "vax_advice",
                            "type": "toggle",
                            "label": "Post-Vaccination Advice Given? (fever management, red flags, next appointment)",
                            "required": True,
                            "output_phrase": "Advice given: {value}"
                        },
                        {
                            "id": "vax_next_visit",
                            "type": "text",
                            "label": "Next Scheduled Vaccination",
                            "required": True,
                            "placeholder": "e.g., 4-month vaccines: 6-in-1, MenB, Rotavirus — appointment booked for [date]",
                            "output_phrase": "Next visit: {value}"
                        },
                        {
                            "id": "vax_recorded",
                            "type": "toggle",
                            "label": "Recorded in Immunisation Passport & IT System?",
                            "required": True,
                            "output_phrase": "Recorded: {value}"
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
    seed_childhood_immunisations()