from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_panic_disorder():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Mental Health").first()
    if not category:
        category = Category(name="Mental Health")
        db.add(category)
        db.commit()

    t = {
        "title": "Panic Disorder",
        "description": "Assessment and management of panic disorder. Covers diagnostic criteria, differentials, screening for cardiac/GI mimics, and stepped care from CBT to pharmacotherapy.",
        "category": "Mental Health",
        "content": {
            "sections": [
                {
                    "title": "Panic Attack Characteristics",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "panic_frequency",
                            "type": "single_select",
                            "label": "Frequency of Panic Attacks",
                            "required": True,
                            "options": [
                                "First episode",
                                "<1 per month",
                                "1-4 per month",
                                ">1 per week",
                                "Daily"
                            ],
                            "output_phrase": "Frequency: {value}"
                        },
                        {
                            "id": "panic_onset",
                            "type": "single_select",
                            "label": "Onset",
                            "required": True,
                            "options": [
                                "Sudden — peaks within minutes",
                                "Gradual build-up over hours",
                                "Situational (specific trigger)",
                                "Unexpected / spontaneous (out of the blue)"
                            ],
                            "output_phrase": "Onset: {value}"
                        },
                        {
                            "id": "panic_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms During Attack (≥4 for DSM-5 diagnosis)",
                            "required": True,
                            "options": [
                                "Palpitations / racing heart",
                                "Chest pain / tightness",
                                "Shortness of breath / choking sensation",
                                "Dizziness / lightheaded",
                                "Trembling / shaking",
                                "Sweating",
                                "Nausea / abdominal distress",
                                "Depersonalisation / derealisation",
                                "Fear of dying",
                                "Fear of losing control / going mad",
                                "Numbness / tingling (paraesthesia)",
                                "Chills or hot flushes"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        }
                    ]
                },
                {
                    "title": "Impact & Comorbidity",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "panic_avoidance",
                            "type": "toggle",
                            "label": "Avoidance Behaviour? (agoraphobia — avoiding places where escape difficult)",
                            "required": True,
                            "output_phrase": "Avoidance: {value}"
                        },
                        {
                            "id": "panic_ed_visits",
                            "type": "toggle",
                            "label": "Multiple ED Visits / Cardiac Workups? (negative)",
                            "required": False,
                            "output_phrase": "ED visits: {value}"
                        },
                        {
                            "id": "panic_depression",
                            "type": "toggle",
                            "label": "Co-existing Depression?",
                            "required": True,
                            "output_phrase": "Depression: {value}"
                        },
                        {
                            "id": "panic_substance",
                            "type": "single_select",
                            "label": "Alcohol / Substance / Caffeine Use?",
                            "required": False,
                            "options": [
                                "None",
                                "Moderate caffeine",
                                "Excess alcohol",
                                "Cannabis",
                                "Stimulants (cocaine, amphetamines)",
                                "Benzodiazepine use"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Substance-induced panic vs primary disorder. Withdrawal from alcohol/benzos can trigger panic. Address substance use first.",
                            "red_flag_negative": "",
                            "output_phrase": "Substance use: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Rule Out Medical Causes",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "panic_cardiac",
                            "type": "toggle",
                            "label": "Syncope / Exertional Symptoms? (?arrhythmia, not panic)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Syncope or exertional chest pain/SOB = ?cardiac arrhythmia. ECG, Holter, echo before diagnosing panic.",
                            "red_flag_negative": "",
                            "output_phrase": "Cardiac red flags: {value}"
                        },
                        {
                            "id": "panic_thyroid",
                            "type": "toggle",
                            "label": "Weight Loss / Heat Intolerance / Tremor? (?hyperthyroidism)",
                            "required": True,
                            "output_phrase": "Thyroid symptoms: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Panic Disorder (recurrent unexpected attacks + persistent worry about attacks)",
                        "Generalised Anxiety Disorder (persistent worry, not discrete attacks)",
                        "Hyperthyroidism",
                        "Cardiac arrhythmia (SVT, AF)",
                        "Phaeochromocytoma (rare — episodic hypertension, headache, sweating)",
                        "Substance-induced anxiety (caffeine, stimulants, alcohol withdrawal)",
                        "Depression with anxious distress"
                    ],
                    "questions": [
                        {
                            "id": "panic_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Panic Disorder — without agoraphobia",
                                "Panic Disorder — with agoraphobia",
                                "First panic attack — not disorder yet",
                                "Anxiety — not meeting panic criteria",
                                "?Medical cause — investigate first"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "First-line: CBT (individual or group) — refer to psychology / IAPT / SilverCloud (online CBT). Explain panic: adrenaline surge causing physical symptoms — not dangerous, peaks in 10 minutes, self-limiting. Breathing exercises, grounding techniques. If CBT unavailable or declined, or severe: SSRI — Escitalopram 10mg or Sertraline 50mg (start low, go slow — initially may worsen anxiety, warn patient). Review in 2-4 weeks. Benzodiazepines: AVOID for long-term use — risk of dependence. If essential for acute crisis: short course (max 2 weeks). Self-help: Anxiety Ireland, HSE stress control programme. Return if: symptoms worsen on SSRI, new suicidal ideation, or no improvement after 4-6 weeks.",
                    "questions": [
                        {
                            "id": "panic_treatment",
                            "type": "single_select",
                            "label": "Management",
                            "required": True,
                            "options": [
                                "CBT referral + self-help",
                                "SSRI started + CBT referral",
                                "SSRI alone (CBT unavailable/declined)",
                                "Self-help / watchful waiting (mild)",
                                "Refer psychiatry (severe / treatment-resistant)"
                            ],
                            "output_phrase": "Treatment: {value}"
                        },
                        {
                            "id": "panic_cbt_referral",
                            "type": "toggle",
                            "label": "CBT / Psychology Referral Made?",
                            "required": False,
                            "output_phrase": "CBT referral: {value}"
                        },
                        {
                            "id": "panic_ssri",
                            "type": "text",
                            "label": "SSRI Prescribed + Dose",
                            "required": False,
                            "placeholder": "e.g., Escitalopram 10mg OD — start 5mg for first week",
                            "output_phrase": "SSRI: {value}"
                        },
                        {
                            "id": "panic_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 2 weeks. Start Escitalopram 5mg. Warn initial anxiety may increase.",
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
    seed_panic_disorder()