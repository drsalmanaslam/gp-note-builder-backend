from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_self_harm_suicide():
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
        "title": "Self-Harm & Suicidal Ideation Risk Assessment",
        "description": "Structured risk assessment for self-harm and suicidal ideation in general practice. Covers immediate risk, protective factors, safety planning, and referral pathways for urgent and non-urgent presentations.",
        "category": "Mental Health",
        "content": {
            "sections": [
                {
                    "title": "Presenting Complaint & Context",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "sh_presentation",
                            "type": "single_select",
                            "label": "Presentation",
                            "required": True,
                            "options": [
                                "Self-harm — recent episode",
                                "Suicidal ideation (thoughts/plan/intent)",
                                "Both self-harm and suicidal ideation",
                                "Third-party concern (family/friend)",
                                "Routine mental health review — no acute concern"
                            ],
                            "output_phrase": "Presentation: {value}"
                        },
                        {
                            "id": "sh_method",
                            "type": "text",
                            "label": "Method of Self-Harm (if applicable)",
                            "required": False,
                            "placeholder": "e.g., Laceration to forearm, overdose of paracetamol",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: High-lethality method (hanging, jumping, firearms, overdose with delayed toxicity) = urgent ED referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Method: {value}"
                        },
                        {
                            "id": "sh_medical_attention",
                            "type": "toggle",
                            "label": "Does Patient Require Immediate Medical Attention? (overdose, wound, etc.)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Medical stabilisation takes priority. Arrange immediate transfer to ED. Do not delay for psychiatric assessment.",
                            "red_flag_negative": "",
                            "output_phrase": "Medical attention needed: {value}"
                        }
                    ]
                },
                {
                    "title": "Suicidal Ideation Assessment",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "sh_thoughts",
                            "type": "single_select",
                            "label": "Current Suicidal Thoughts",
                            "required": True,
                            "options": [
                                "No suicidal thoughts",
                                "Passive death wish (wishing not to wake up)",
                                "Active suicidal thoughts — no plan",
                                "Active suicidal thoughts — with plan",
                                "Active suicidal thoughts — plan + intent to act soon"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Active suicidal thoughts with plan and/or intent = HIGH RISK. Needs urgent psychiatric assessment. Do not leave alone.",
                            "red_flag_negative": "",
                            "output_phrase": "Suicidal thoughts: {value}"
                        },
                        {
                            "id": "sh_plan",
                            "type": "textarea",
                            "label": "Details of Plan (if any)",
                            "required": False,
                            "placeholder": "e.g., Specific method, location, timing, preparations made...",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Specific plan with access to means and intent to act = VERY HIGH RISK. Emergency referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Plan details: {value}"
                        },
                        {
                            "id": "sh_intent",
                            "type": "single_select",
                            "label": "Intent to Act",
                            "required": True,
                            "options": [
                                "No intent — thoughts only",
                                "Uncertain / ambivalent",
                                "Intent to act — but not today",
                                "Intent to act — within hours/days",
                                "Already acted (self-harm attempt today)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Intent to act imminently = emergency. Arrange urgent assessment and do not leave patient alone.",
                            "red_flag_negative": "",
                            "output_phrase": "Intent to act: {value}"
                        },
                        {
                            "id": "sh_previous_attempts",
                            "type": "single_select",
                            "label": "Previous Self-Harm / Suicide Attempts",
                            "required": True,
                            "options": [
                                "None",
                                "One previous episode — >12 months ago",
                                "Multiple episodes — all >12 months ago",
                                "Recent episode — within last 12 months",
                                "Recent episode — within last month"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Recent or multiple previous attempts = strongest predictor of completed suicide. HIGH RISK.",
                            "red_flag_negative": "",
                            "output_phrase": "Previous attempts: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "sh_risk_factors",
                            "type": "multi_select",
                            "label": "Risk Factors Present",
                            "required": True,
                            "options": [
                                "Male gender",
                                "Age <25 or >65",
                                "Mental illness (depression, bipolar, psychosis)",
                                "Substance misuse (alcohol/drugs)",
                                "Chronic physical illness/pain",
                                "Recent crisis/loss (relationship, job, bereavement)",
                                "Social isolation / living alone",
                                "Family history of suicide",
                                "Access to lethal means",
                                "Forensic/legal problems",
                                "None identified"
                            ],
                            "output_phrase": "Risk factors: {value}"
                        }
                    ]
                },
                {
                    "title": "Protective Factors",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "sh_protective",
                            "type": "multi_select",
                            "label": "Protective Factors",
                            "required": True,
                            "options": [
                                "Willing to engage with support",
                                "Family/social support",
                                "Children/dependents at home",
                                "Religious/spiritual beliefs",
                                "Employment / education",
                                "Future plans / goals",
                                "Good insight into illness",
                                "Therapeutic relationship with GP/MDT",
                                "None identified"
                            ],
                            "output_phrase": "Protective factors: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment & Risk Stratification",
                    "section_type": "assessment",
                    "differentials": [
                        "HIGH RISK — Active plan + intent + access to means",
                        "MODERATE RISK — Suicidal thoughts + risk factors, no immediate plan",
                        "LOW RISK — Passive thoughts, good protective factors, engaged",
                        "Depressive episode — suicidal ideation secondary",
                        "Personality disorder — chronic suicidal ideation",
                        "Acute stress reaction / adjustment disorder",
                        "Substance-induced mental state"
                    ],
                    "questions": [
                        {
                            "id": "sh_risk_level",
                            "type": "single_select",
                            "label": "Risk Level",
                            "required": True,
                            "options": [
                                "LOW — passive thoughts, protective factors strong, engaged",
                                "MODERATE — suicidal ideation + risk factors, ambivalent intent",
                                "HIGH — active plan, intent, multiple risk factors",
                                "VERY HIGH — plan + intent to act imminently, or recent serious attempt"
                            ],
                            "output_phrase": "Risk level: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "HIGH/VERY HIGH RISK: Do not leave alone. Arrange immediate transfer to ED or crisis team (call 999 if patient refuses and risk is imminent). Contact local crisis/home treatment team. MODERATE RISK: Urgent referral to crisis team/psychiatry liaison (within 24-48 hours). Agree safety plan — remove access to means, identify support contacts, agree coping strategies. LOW RISK: Safety plan + GP follow-up within 1 week. Provide crisis helpline numbers: Samaritans 116 123, Pieta House 1800 247 247, Text HELLO to 50808. If patient declines help but risk is significant: assess capacity, document thoroughly, and consider contacting family/carer with consent. Always document risk assessment clearly.",
                    "questions": [
                        {
                            "id": "sh_plan_action",
                            "type": "single_select",
                            "label": "Immediate Action",
                            "required": True,
                            "options": [
                                "999/ED transfer — high risk, cannot keep safe in community",
                                "Urgent crisis team referral (within 24 hours)",
                                "Routine psychiatry referral",
                                "GP follow-up with safety plan",
                                "Patient declined referral — capacity assessed"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "sh_safety_plan",
                            "type": "toggle",
                            "label": "Safety Plan Agreed? (removal of means, support contacts, coping strategies)",
                            "required": True,
                            "output_phrase": "Safety plan agreed: {value}"
                        },
                        {
                            "id": "sh_helpline_given",
                            "type": "toggle",
                            "label": "Crisis Helpline Numbers Given? (Samaritans 116 123, Pieta 1800 247 247)",
                            "required": True,
                            "output_phrase": "Helpline given: {value}"
                        },
                        {
                            "id": "sh_family_informed",
                            "type": "single_select",
                            "label": "Family/Carer Informed?",
                            "required": True,
                            "options": [
                                "Yes — with patient consent",
                                "Not informed — patient declined",
                                "Not applicable — no family/carer",
                                "Informed without consent — risk justified breach"
                            ],
                            "output_phrase": "Family informed: {value}"
                        },
                        {
                            "id": "sh_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Crisis team to contact within 4 hours. GP review in 3 days. Safety plan in place.",
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
    seed_self_harm_suicide()