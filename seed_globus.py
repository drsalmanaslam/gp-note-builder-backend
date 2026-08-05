from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_globus():
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
        "title": "Globus Sensation (Lump in Throat)",
        "description": "Assessment of globus pharyngeus. Differentiates functional from organic causes, red flags for malignancy, and management including reflux treatment and reassurance.",
        "category": "ENT",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "globus_duration",
                            "type": "text",
                            "label": "Duration",
                            "required": True,
                            "placeholder": "e.g., 3 months — intermittent",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "globus_character",
                            "type": "multi_select",
                            "label": "Characteristics (classic features)",
                            "required": True,
                            "options": [
                                "Lump in throat — between meals",
                                "Improves with eating / drinking (classic)",
                                "Worse when swallowing saliva only",
                                "No true dysphagia — food passes normally",
                                "Worse with stress / anxiety",
                                "Associated throat clearing / hawking"
                            ],
                            "output_phrase": "Characteristics: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Rule Out Malignancy",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "globus_dysphagia",
                            "type": "toggle",
                            "label": "True Dysphagia? (food sticking, progressive, solids then liquids)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: True dysphagia (especially progressive solids→liquids) = ?oesophageal cancer/stricture. Urgent OGD — 2-week wait.",
                            "red_flag_negative": "",
                            "output_phrase": "Dysphagia: {value}"
                        },
                        {
                            "id": "globus_weight_loss",
                            "type": "toggle",
                            "label": "Unintentional Weight Loss?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Weight loss + globus = ?malignancy. Urgent 2-week wait OGD.",
                            "red_flag_negative": "",
                            "output_phrase": "Weight loss: {value}"
                        },
                        {
                            "id": "globus_hoarseness",
                            "type": "toggle",
                            "label": "Persistent Hoarseness >3 Weeks? (?laryngeal cancer)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Hoarseness >3 weeks + globus = ?laryngeal cancer. Urgent ENT 2-week wait referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Hoarseness: {value}"
                        },
                        {
                            "id": "globus_odynophagia",
                            "type": "toggle",
                            "label": "Pain on Swallowing (Odynophagia)?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Odynophagia = ?oesophagitis, candida, or malignancy. Needs investigation — OGD.",
                            "red_flag_negative": "",
                            "output_phrase": "Odynophagia: {value}"
                        }
                    ]
                },
                {
                    "title": "Associated Factors",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "globus_reflux",
                            "type": "toggle",
                            "label": "GORD Symptoms? (heartburn, regurgitation, acid taste)",
                            "required": True,
                            "output_phrase": "Reflux symptoms: {value}"
                        },
                        {
                            "id": "globus_pnd",
                            "type": "toggle",
                            "label": "Post-Nasal Drip / Rhinitis?",
                            "required": False,
                            "output_phrase": "PND: {value}"
                        },
                        {
                            "id": "globus_stress",
                            "type": "toggle",
                            "label": "Stress / Anxiety Related? (worsens with stress, improves when relaxed)",
                            "required": True,
                            "output_phrase": "Stress: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Globus Pharyngeus (functional) — classic features, no red flags",
                        "GORD / Laryngopharyngeal Reflux (LPR) — associated heartburn/regurgitation",
                        "Oesophageal Carcinoma — red flags: progressive dysphagia, weight loss",
                        "Laryngeal / Hypopharyngeal Carcinoma — hoarseness, odynophagia",
                        "Pharyngeal Pouch (Zenker's) — halitosis, regurgitation of undigested food",
                        "Cricopharyngeal Spasm",
                        "Anxiety / Somatic Symptom Disorder",
                        "Thyroid Mass / Goitre — palpable neck mass"
                    ],
                    "questions": [
                        {
                            "id": "globus_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Globus Pharyngeus — functional, reassure",
                                "LPR / GORD-related — trial PPI",
                                "Anxiety-related — reassurance + manage stress",
                                "?Organic — refer ENT / OGD",
                                "Red flags present — urgent 2-week wait"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If NO red flags and typical globus history: Reassure — benign condition, no serious pathology. Trial PPI: Omeprazole 20mg BD or Esomeprazole 40mg OD for 4-8 weeks (LPR requires higher doses/longer course than GORD). If no improvement: refer ENT for nasendoscopy to confirm diagnosis and exclude subtle pathology. Address post-nasal drip if present (intranasal steroid). If stress-related: explain link between anxiety and globus. Simple techniques: sipping water, yawning, relaxation. If red flags: Urgent 2-week wait OGD or ENT depending on dominant symptom. Safety-net: Return if develops true dysphagia, weight loss, hoarseness, or odynophagia.",
                    "questions": [
                        {
                            "id": "globus_treatment",
                            "type": "single_select",
                            "label": "Management",
                            "required": True,
                            "options": [
                                "Reassurance + watchful waiting",
                                "Trial PPI (high-dose, 4-8 weeks)",
                                "Reassurance + stress management",
                                "Refer ENT (routine)",
                                "Urgent 2-week wait (red flags)"
                            ],
                            "output_phrase": "Management: {value}"
                        },
                        {
                            "id": "globus_ppi",
                            "type": "text",
                            "label": "PPI Prescribed (if trial)",
                            "required": False,
                            "placeholder": "e.g., Omeprazole 20mg BD for 8 weeks",
                            "output_phrase": "PPI: {value}"
                        },
                        {
                            "id": "globus_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if dysphagia/weight loss/hoarseness/odynophagia)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "globus_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 8 weeks post-PPI trial. If no improvement, refer ENT for nasendoscopy.",
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
    seed_globus()