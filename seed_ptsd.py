from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_ptsd():
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
        "title": "PTSD (Post-Traumatic Stress Disorder)",
        "description": "Assessment of PTSD including trauma history, core symptom clusters (re-experiencing, avoidance, hyperarousal), screening tools, and referral for trauma-focused CBT or EMDR.",
        "category": "Mental Health",
        "content": {
            "sections": [
                {
                    "title": "Trauma History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ptsd_trauma_type",
                            "type": "multi_select",
                            "label": "Type of Trauma",
                            "required": True,
                            "options": [
                                "Road traffic accident",
                                "Physical assault / violence",
                                "Sexual assault / abuse",
                                "Childhood abuse / neglect",
                                "Combat / military trauma",
                                "Witnessing death / serious injury",
                                "Domestic violence",
                                "Medical trauma (ICU, emergency surgery)",
                                "Natural disaster",
                                "Other"
                            ],
                            "output_phrase": "Trauma type: {value}"
                        },
                        {
                            "id": "ptsd_when",
                            "type": "text",
                            "label": "When Did Trauma Occur?",
                            "required": True,
                            "placeholder": "e.g., 6 months ago — RTA",
                            "output_phrase": "Timing: {value}"
                        }
                    ]
                },
                {
                    "title": "Core Symptom Clusters (DSM-5)",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ptsd_re_experiencing",
                            "type": "multi_select",
                            "label": "Re-experiencing (≥1 required)",
                            "required": True,
                            "options": [
                                "Intrusive memories / flashbacks",
                                "Nightmares of the event",
                                "Distress when reminded of trauma",
                                "Physical reactions to triggers (sweating, palpitations)",
                                "None"
                            ],
                            "output_phrase": "Re-experiencing: {value}"
                        },
                        {
                            "id": "ptsd_avoidance",
                            "type": "multi_select",
                            "label": "Avoidance (≥1 required)",
                            "required": True,
                            "options": [
                                "Avoiding thoughts / feelings about trauma",
                                "Avoiding people, places, activities that remind of trauma",
                                "Emotional numbing",
                                "Unable to recall parts of the trauma",
                                "None"
                            ],
                            "output_phrase": "Avoidance: {value}"
                        },
                        {
                            "id": "ptsd_hyperarousal",
                            "type": "multi_select",
                            "label": "Hyperarousal & Reactivity (≥2 required)",
                            "required": True,
                            "options": [
                                "Hypervigilance / constantly on guard",
                                "Exaggerated startle response",
                                "Irritability / angry outbursts",
                                "Poor concentration",
                                "Sleep disturbance",
                                "Reckless / self-destructive behaviour",
                                "None"
                            ],
                            "output_phrase": "Hyperarousal: {value}"
                        }
                    ]
                },
                {
                    "title": "Impact & Risk Assessment",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "ptsd_duration",
                            "type": "single_select",
                            "label": "Duration of Symptoms",
                            "required": True,
                            "options": [
                                "<1 month (Acute Stress Disorder)",
                                "1-3 months",
                                ">3 months (PTSD)",
                                ">1 year"
                            ],
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "ptsd_functional",
                            "type": "single_select",
                            "label": "Functional Impairment",
                            "required": True,
                            "options": [
                                "Mild — functioning well, some distress",
                                "Moderate — affecting work/relationships",
                                "Severe — unable to work, isolated, significant distress"
                            ],
                            "output_phrase": "Impact: {value}"
                        },
                        {
                            "id": "ptsd_suicide",
                            "type": "toggle",
                            "label": "Suicidal Ideation / Self-Harm?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Suicidal ideation = urgent psychiatric assessment. Do not leave alone if imminent risk.",
                            "red_flag_negative": "",
                            "output_phrase": "Suicidal ideation: {value}"
                        },
                        {
                            "id": "ptsd_substance",
                            "type": "toggle",
                            "label": "Alcohol / Substance Misuse as Coping?",
                            "required": True,
                            "output_phrase": "Substance use: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "PTSD (symptoms >1 month, significant impairment)",
                        "Acute Stress Disorder (<1 month since trauma)",
                        "Complex PTSD (prolonged/repeated trauma + affect dysregulation, negative self-concept, interpersonal difficulties)",
                        "Adjustment Disorder (symptoms not meeting PTSD criteria)",
                        "Depression / Anxiety (comorbid or primary)",
                        "Traumatic Brain Injury (if head injury involved)"
                    ],
                    "questions": [
                        {
                            "id": "ptsd_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "PTSD — refer trauma-focused CBT / EMDR",
                                "Acute Stress Disorder — watchful waiting, review in 1 month",
                                "Complex PTSD — refer specialist trauma service",
                                "Adjustment Disorder — supportive care",
                                "Comorbid PTSD + Depression"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "First-line: Trauma-focused CBT or EMDR — refer to psychology / HSE counselling / specialist trauma service. Do NOT recommend routine debriefing — may worsen outcomes. Mild symptoms <1 month: watchful waiting — many resolve spontaneously. Self-help: PTSD UK resources, HSE stress control. Pharmacotherapy: If CBT declined/unavailable or severe depression: Sertraline 50-100mg or Paroxetine 20-40mg. Venlafaxine as alternative. Benzodiazepines: AVOID — worsens long-term outcomes. Sleep: Address sleep hygiene. Avoid hypnotics long-term. If suicidal: urgent psychiatric assessment. Safety-net: Return if suicidal ideation, severe functional decline, or substance misuse escalation.",
                    "questions": [
                        {
                            "id": "ptsd_treatment",
                            "type": "single_select",
                            "label": "Management",
                            "required": True,
                            "options": [
                                "Trauma-focused CBT / EMDR referral",
                                "Watchful waiting — review in 1 month (mild/<1 month)",
                                "SSRI + therapy referral",
                                "Refer specialist trauma service (complex/severe)",
                                "Urgent psychiatric assessment (suicidal)"
                            ],
                            "output_phrase": "Treatment: {value}"
                        },
                        {
                            "id": "ptsd_therapy_referral",
                            "type": "toggle",
                            "label": "CBT / EMDR Referral Made?",
                            "required": False,
                            "output_phrase": "Therapy referral: {value}"
                        },
                        {
                            "id": "ptsd_ssri",
                            "type": "text",
                            "label": "SSRI Prescribed?",
                            "required": False,
                            "placeholder": "e.g., Sertraline 50mg OD",
                            "output_phrase": "SSRI: {value}"
                        },
                        {
                            "id": "ptsd_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 2-4 weeks. Therapy referral sent. Monitor for suicidal ideation.",
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
    seed_ptsd()