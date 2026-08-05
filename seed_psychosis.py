from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_psychosis():
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
        "title": "Psychosis — Urgent Assessment",
        "description": "Urgent assessment of suspected first-episode psychosis or acute psychotic episode. Covers key symptoms, risk assessment, organic cause exclusion, and urgent referral to psychiatry.",
        "category": "Mental Health",
        "content": {
            "sections": [
                {
                    "title": "Presenting Symptoms",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "psy_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms (core features of psychosis)",
                            "required": True,
                            "options": [
                                "Hallucinations — auditory (hearing voices)",
                                "Hallucinations — visual",
                                "Hallucinations — other (tactile, olfactory)",
                                "Delusions — paranoid/persecutory",
                                "Delusions — grandiose",
                                "Delusions — control (thought insertion/broadcast)",
                                "Disorganised speech / thought disorder",
                                "Disorganised / catatonic behaviour",
                                "Negative symptoms — flat affect, social withdrawal, apathy"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        },
                        {
                            "id": "psy_duration",
                            "type": "single_select",
                            "label": "Duration of Symptoms",
                            "required": True,
                            "options": [
                                "<1 week — acute onset",
                                "1-4 weeks",
                                ">1 month",
                                ">6 months — ?chronic"
                            ],
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "psy_first_episode",
                            "type": "toggle",
                            "label": "First Episode? (vs known diagnosis / relapse)",
                            "required": True,
                            "output_phrase": "First episode: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Assessment (CRITICAL)",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "psy_self_harm",
                            "type": "single_select",
                            "label": "Risk to Self — Suicidal Ideation / Self-Harm?",
                            "required": True,
                            "options": [
                                "None",
                                "Passive thoughts — no plan",
                                "Active thoughts — with plan",
                                "Command hallucinations telling patient to harm self",
                                "Recent self-harm / suicide attempt"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Active suicidal ideation with plan or command hallucinations = HIGH RISK. Urgent psychiatric assessment. Do not leave alone.",
                            "red_flag_negative": "",
                            "output_phrase": "Risk to self: {value}"
                        },
                        {
                            "id": "psy_risk_others",
                            "type": "single_select",
                            "label": "Risk to Others — Violent Ideation / Threatening Behaviour?",
                            "required": True,
                            "options": [
                                "None",
                                "Verbal aggression — no physical violence",
                                "Threats of violence — no action yet",
                                "Physical aggression — recent episode",
                                "Command hallucinations telling patient to harm others"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Threats of violence or command hallucinations to harm others = HIGH RISK. Urgent psychiatric assessment ± police if imminent danger.",
                            "red_flag_negative": "",
                            "output_phrase": "Risk to others: {value}"
                        },
                        {
                            "id": "psy_insight",
                            "type": "single_select",
                            "label": "Insight",
                            "required": True,
                            "options": [
                                "Good insight — recognises symptoms as illness",
                                "Partial insight — uncertain",
                                "No insight — firmly believes delusions/hallucinations are real"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: No insight + risk to self/others = may require involuntary admission (Mental Health Act). Urgent psychiatric assessment.",
                            "red_flag_negative": "",
                            "output_phrase": "Insight: {value}"
                        }
                    ]
                },
                {
                    "title": "Rule Out Organic Causes",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "psy_substance",
                            "type": "multi_select",
                            "label": "Substance Use (common triggers for drug-induced psychosis)",
                            "required": True,
                            "options": [
                                "Cannabis (most common)",
                                "Stimulants — cocaine, amphetamines, methamphetamine",
                                "Hallucinogens — LSD, psilocybin",
                                "Alcohol withdrawal",
                                "Benzodiazepine withdrawal",
                                "Prescribed steroids",
                                "None"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Drug-induced psychosis may resolve in days-weeks but can unmask underlying schizophrenia. Needs psychiatric assessment regardless.",
                            "red_flag_negative": "",
                            "output_phrase": "Substance use: {value}"
                        },
                        {
                            "id": "psy_delirium",
                            "type": "toggle",
                            "label": "Acute Confusion / Fluctuating Consciousness? (?delirium — medical emergency)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Fluctuating consciousness + acute onset = ?delirium. Medical emergency — investigate for infection, metabolic, neurological causes. Admit.",
                            "red_flag_negative": "",
                            "output_phrase": "?Delirium: {value}"
                        },
                        {
                            "id": "psy_neurological",
                            "type": "toggle",
                            "label": "Neurological Symptoms? (seizures, headache, focal deficit — ?brain lesion)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Neurological symptoms + psychosis = ?brain tumour/encephalitis/TLE. Urgent medical admission + neuroimaging.",
                            "red_flag_negative": "",
                            "output_phrase": "Neurological: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "First-Episode Psychosis — schizophrenia, schizoaffective, bipolar with psychosis",
                        "Acute Psychotic Episode — known diagnosis, relapse",
                        "Drug-Induced Psychosis — cannabis, stimulants, steroids",
                        "Delirium — acute confusion, fluctuating, medical cause",
                        "Severe Depression with Psychotic Features",
                        "Bipolar Disorder — manic episode with psychosis",
                        "Organic Brain Disease — tumour, encephalitis, temporal lobe epilepsy",
                        "Brief Psychotic Disorder — <1 month, stress-related"
                    ],
                    "questions": [
                        {
                            "id": "psy_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "?First-Episode Psychosis — refer early intervention psychiatry",
                                "?Schizophrenia / Schizoaffective",
                                "?Drug-Induced Psychosis",
                                "?Bipolar with Psychosis",
                                "?Organic — medical admission for investigation",
                                "?Delirium — emergency medical admission"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "IMMEDIATE RISK to self/others: Urgent psychiatric crisis team assessment. If patient refuses and risk is imminent, consider Mental Health Act detention (involuntary admission) — contact local approved mental health professional (AMHP) / Gardaí if necessary. Do not leave high-risk patient alone. If ?delirium or ?organic cause: Emergency medical admission for investigation and management. FIRST EPISODE PSYCHOSIS: Urgent referral to Early Intervention in Psychosis (EIP) team — ideally within 14 days. Start antipsychotic only under specialist guidance (unless severe/urgent). If patient agitated: Offer oral Lorazepam 0.5-1mg or Olanzapine 5-10mg if willing. Avoid haloperidol in first episode if possible. Safety-net for family/carer: Return immediately or call 999 if patient becomes threatening, refuses help, or deteriorates.",
                    "questions": [
                        {
                            "id": "psy_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Urgent crisis team / EIP referral (within 24h)",
                                "Emergency medical admission (?organic/delirium)",
                                "Mental Health Act assessment (risk + no insight + refusing help)",
                                "Routine psychiatry referral (stable, low risk)",
                                "Discuss with psychiatrist on-call"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "psy_safety_plan",
                            "type": "toggle",
                            "label": "Safety Plan in Place? (crisis numbers, family/carer informed, remove access to means)",
                            "required": True,
                            "output_phrase": "Safety plan: {value}"
                        },
                        {
                            "id": "psy_carer_informed",
                            "type": "toggle",
                            "label": "Family/Carer Informed? (with consent or in best interests if risk high)",
                            "required": True,
                            "output_phrase": "Carer informed: {value}"
                        },
                        {
                            "id": "psy_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Crisis team to assess today. EIP referral sent. GP to review in 1 week.",
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
    seed_psychosis()