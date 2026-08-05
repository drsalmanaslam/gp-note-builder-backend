from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_parkinsons():
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
        "title": "Parkinson's Disease — Shared Care",
        "description": "Assessment for suspected Parkinson's disease and ongoing shared care. Covers key motor and non-motor symptoms, red flags for atypical parkinsonism, medication review, and when to refer neurology.",
        "category": "Neurology",
        "content": {
            "sections": [
                {
                    "title": "Motor Symptoms (TRAP)",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "park_tremor",
                            "type": "single_select",
                            "label": "Tremor",
                            "required": True,
                            "options": [
                                "Rest tremor — pill-rolling, unilateral onset (classic)",
                                "Action tremor — worse on movement (?essential tremor)",
                                "Both rest and action tremor",
                                "No tremor"
                            ],
                            "output_phrase": "Tremor: {value}"
                        },
                        {
                            "id": "park_rigidity",
                            "type": "single_select",
                            "label": "Rigidity / Stiffness",
                            "required": True,
                            "options": [
                                "Cogwheel rigidity (classic)",
                                "Lead-pipe rigidity",
                                "General stiffness — no rigidity on exam",
                                "None"
                            ],
                            "output_phrase": "Rigidity: {value}"
                        },
                        {
                            "id": "park_bradykinesia",
                            "type": "multi_select",
                            "label": "Bradykinesia (slowness of movement)",
                            "required": True,
                            "options": [
                                "Slowness initiating movement",
                                "Small handwriting (micrographia)",
                                "Reduced facial expression (hypomimia)",
                                "Soft / monotonous speech (hypophonia)",
                                "Difficulty with fine tasks (buttons, zips)",
                                "Shuffling gait / reduced arm swing",
                                "None"
                            ],
                            "output_phrase": "Bradykinesia: {value}"
                        },
                        {
                            "id": "park_postural",
                            "type": "single_select",
                            "label": "Postural Instability / Gait",
                            "required": True,
                            "options": [
                                "Normal gait",
                                "Shuffling / festinating gait",
                                "Reduced arm swing — unilateral",
                                "Freezing episodes",
                                "Falls (later stage)"
                            ],
                            "output_phrase": "Gait: {value}"
                        }
                    ]
                },
                {
                    "title": "Non-Motor Symptoms (often overlooked)",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "park_non_motor",
                            "type": "multi_select",
                            "label": "Non-Motor Symptoms",
                            "required": True,
                            "options": [
                                "Hyposmia / anosmia (loss of smell — early sign)",
                                "Constipation (often precedes motor symptoms)",
                                "REM sleep behaviour disorder (acting out dreams)",
                                "Depression / anxiety",
                                "Fatigue",
                                "Cognitive changes / memory problems",
                                "Orthostatic hypotension / dizziness",
                                "Urinary urgency / incontinence",
                                "Drooling / sialorrhoea",
                                "None"
                            ],
                            "output_phrase": "Non-motor: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — ?Atypical Parkinsonism",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "park_red_flags",
                            "type": "multi_select",
                            "label": "Red Flags for Atypical Parkinsonism (refer neurology if present)",
                            "required": True,
                            "options": [
                                "Early falls (within first year — ?PSP)",
                                "Early dementia / hallucinations (within first year — ?DLB)",
                                "Severe autonomic dysfunction early (prominent OH, incontinence — ?MSA)",
                                "Symmetrical onset (atypical)",
                                "Poor response to Levodopa",
                                "Rapid progression",
                                "Oculomotor abnormalities (vertical gaze palsy — PSP)",
                                "None — typical Parkinson's pattern"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Atypical features present = ?Progressive Supranuclear Palsy, Multiple System Atrophy, Dementia with Lewy Bodies. Urgent neurology referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Atypical features: {value}"
                        }
                    ]
                },
                {
                    "title": "Medication Review (if known diagnosis)",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "park_medication",
                            "type": "text",
                            "label": "Current Parkinson's Medications + Doses",
                            "required": False,
                            "placeholder": "e.g., Co-beneldopa 12.5/50mg TDS",
                            "output_phrase": "Medications: {value}"
                        },
                        {
                            "id": "park_motor_fluctuations",
                            "type": "toggle",
                            "label": "Motor Fluctuations? (wearing off, on-off phenomenon, dyskinesias)",
                            "required": False,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Motor fluctuations = complex management. Refer neurology for medication adjustment.",
                            "red_flag_negative": "",
                            "output_phrase": "Motor fluctuations: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Idiopathic Parkinson's Disease (classic TRAP, unilateral onset, good Levodopa response)",
                        "Progressive Supranuclear Palsy (early falls, vertical gaze palsy)",
                        "Multiple System Atrophy (prominent autonomic failure, poor Levodopa response)",
                        "Dementia with Lewy Bodies (early dementia, hallucinations, fluctuating cognition)",
                        "Drug-Induced Parkinsonism (antipsychotics, metoclopramide, prochlorperazine)",
                        "Essential Tremor (bilateral, action tremor, no rigidity/bradykinesia, familial)",
                        "Vascular Parkinsonism (lower body dominant, stepwise progression)"
                    ],
                    "questions": [
                        {
                            "id": "park_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "?Parkinson's Disease — refer neurology for diagnosis",
                                "Parkinson's Disease — known, stable, shared care",
                                "Parkinson's Disease — known, deteriorating, refer neurology",
                                "?Drug-Induced Parkinsonism — review medications",
                                "?Atypical Parkinsonism — urgent neurology referral",
                                "Essential Tremor — not Parkinson's"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If suspected new Parkinson's: Refer neurology for diagnosis and initiation of treatment (Levodopa/dopamine agonist). Do not start Levodopa in primary care without specialist guidance. If known Parkinson's on shared care: Annual review — motor and non-motor symptoms, medication side effects (impulse control disorders with dopamine agonists — hypersexuality, gambling, binge eating). Physiotherapy and OT referral for gait/balance and daily living. Speech and language therapy for hypophonia/dysphagia. Driving: Must notify DVLA/RSA. May continue driving if safe — neurology assessment. Avoid drugs that worsen parkinsonism: Metoclopramide, Prochlorperazine, Haloperidol, typical antipsychotics. Safety-net: Return if rapid deterioration, falls, hallucinations, confusion, or motor fluctuations.",
                    "questions": [
                        {
                            "id": "park_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Refer neurology — ?new diagnosis",
                                "Routine neurology referral — deterioration",
                                "Shared care — continue medications, GP review",
                                "Physio / OT / SLT referral",
                                "Driving advice + DVLA notification"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "park_driving",
                            "type": "toggle",
                            "label": "Driving Advice Given? (must notify DVLA)",
                            "required": False,
                            "output_phrase": "Driving advice: {value}"
                        },
                        {
                            "id": "park_mdt_referrals",
                            "type": "multi_select",
                            "label": "MDT Referrals",
                            "required": False,
                            "options": [
                                "Physiotherapy",
                                "Occupational Therapy",
                                "Speech & Language Therapy",
                                "Dietitian",
                                "Parkinson's Nurse Specialist",
                                "None"
                            ],
                            "output_phrase": "MDT referrals: {value}"
                        },
                        {
                            "id": "park_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Neurology referral sent. GP review in 3 months. Physio and OT referrals.",
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
    seed_parkinsons()