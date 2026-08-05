from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_cluster_headache():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Neurology").first()
    if not category:
        category = Category(name="Neurology")
        db.add(category)
        db.commit()

    t = {
        "title": "Cluster Headache",
        "description": "Diagnosis and management of cluster headache. Covers characteristic features distinguishing from migraine, acute treatment (oxygen, triptans), and preventive options.",
        "category": "Neurology",
        "content": {
            "sections": [
                {
                    "title": "Headache Characteristics",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ch_pain",
                            "type": "single_select",
                            "label": "Pain Description",
                            "required": True,
                            "options": [
                                "Severe / excruciating — unilateral, orbital/supraorbital/temporal",
                                "Moderate — unilateral",
                                "Throbbing / pulsating",
                                "Sharp / stabbing"
                            ],
                            "output_phrase": "Pain: {value}"
                        },
                        {
                            "id": "ch_duration",
                            "type": "single_select",
                            "label": "Attack Duration (untreated)",
                            "required": True,
                            "options": [
                                "15-180 minutes",
                                "4-72 hours (migraine pattern)",
                                "Seconds to minutes (SUNCT/trigeminal neuralgia)",
                                "Continuous"
                            ],
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "ch_frequency",
                            "type": "single_select",
                            "label": "Attack Frequency",
                            "required": True,
                            "options": [
                                "1 every other day to 8 per day (cluster pattern)",
                                "Daily — same time (often nocturnal)",
                                "Weekly",
                                "Less frequent"
                            ],
                            "output_phrase": "Frequency: {value}"
                        }
                    ]
                },
                {
                    "title": "Autonomic Features (key to diagnosis)",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ch_autonomic",
                            "type": "multi_select",
                            "label": "Ipsilateral Autonomic Features (≥1 required)",
                            "required": True,
                            "options": [
                                "Conjunctival injection / red eye",
                                "Lacrimation (tearing)",
                                "Nasal congestion / rhinorrhoea",
                                "Eyelid oedema",
                                "Forehead/facial sweating",
                                "Miosis / ptosis (Horner's — partial)",
                                "Restlessness / agitation (pacing — unlike migraine where patient lies still)",
                                "None"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: No autonomic features = atypical. Consider alternative diagnosis. Refer neurology if uncertain.",
                            "red_flag_negative": "",
                            "output_phrase": "Autonomic features: {value}"
                        }
                    ]
                },
                {
                    "title": "Pattern & Triggers",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ch_pattern",
                            "type": "single_select",
                            "label": "Cluster Pattern",
                            "required": True,
                            "options": [
                                "Episodic — bouts lasting weeks-months, then remission months-years",
                                "Chronic — attacks for >1 year without remission (or remission <1 month)",
                                "First episode — pattern not yet established"
                            ],
                            "output_phrase": "Pattern: {value}"
                        },
                        {
                            "id": "ch_triggers",
                            "type": "multi_select",
                            "label": "Triggers (during cluster period)",
                            "required": False,
                            "options": [
                                "Alcohol (triggers within 1 hour)",
                                "Strong smells (paint, petrol, perfumes)",
                                "Nitroglycerin",
                                "Heat / exercise",
                                "Sleep / REM sleep (nocturnal attacks)",
                                "None identified"
                            ],
                            "output_phrase": "Triggers: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Cluster Headache — episodic or chronic",
                        "Migraine (autonomic features less prominent, patient avoids movement)",
                        "Trigeminal Neuralgia (seconds, electric shock, no autonomic features)",
                        "Paroxysmal Hemicrania (shorter 2-30min, responds to indomethacin)",
                        "SUNCT/SUNA (seconds, frequent, autonomic features)",
                        "Hemicrania Continua (continuous, responds to indomethacin)",
                        "Secondary — pituitary tumour, carotid dissection (red flags if atypical)"
                    ],
                    "questions": [
                        {
                            "id": "ch_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Episodic Cluster Headache — acute + preventive treatment",
                                "Chronic Cluster Headache — preventive + neurology referral",
                                "?Cluster — refer neurology for confirmation",
                                "Not cluster — alternative diagnosis"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "ACUTE ATTACK: High-flow 100% oxygen 12-15L/min via non-rebreather mask (first-line, effective in 15 mins). Sumatriptan 6mg SC (fastest) or Sumatriptan 20mg nasal spray. Oral triptans too slow — NOT recommended. Avoid triggers especially alcohol during cluster period. PREVENTIVE: Verapamil 80mg TDS titrated up to 960mg daily (first-line). ECG before and during titration — risk of heart block. Prednisolone 60mg OD for 5 days then taper (bridging therapy while verapamil takes effect). Refer neurology: All suspected cluster headache for confirmation + ongoing management. Chronic cluster or refractory: Greater occipital nerve block, galcanezumab (CGRP monoclonal antibody). Safety-net: Return if attack frequency increases or if new neurological signs develop.",
                    "questions": [
                        {
                            "id": "ch_acute",
                            "type": "single_select",
                            "label": "Acute Treatment",
                            "required": True,
                            "options": [
                                "High-flow O2 prescribed + Sumatriptan SC/nasal",
                                "Sumatriptan SC/nasal only",
                                "Oral triptan (suboptimal — advise SC/nasal)",
                                "Not applicable — preventive only"
                            ],
                            "output_phrase": "Acute treatment: {value}"
                        },
                        {
                            "id": "ch_preventive",
                            "type": "single_select",
                            "label": "Preventive Treatment",
                            "required": True,
                            "options": [
                                "Verapamil started (ECG booked)",
                                "Prednisolone bridging course",
                                "Verapamil + Prednisolone",
                                "Refer neurology for preventive management",
                                "None — first episode / watchful waiting"
                            ],
                            "output_phrase": "Preventive: {value}"
                        },
                        {
                            "id": "ch_neuro_referral",
                            "type": "toggle",
                            "label": "Neurology Referral Made?",
                            "required": True,
                            "output_phrase": "Neurology referral: {value}"
                        },
                        {
                            "id": "ch_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., ECG this week, start Verapamil 80mg TDS, titrate. Neuro referral sent. Review in 2 weeks.",
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
    seed_cluster_headache()