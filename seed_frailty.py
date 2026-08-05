from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_frailty():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Geriatrics").first()
    if not category:
        category = Category(name="Geriatrics")
        db.add(category)
        db.commit()

    t = {
        "title": "Frailty Assessment (Older Person)",
        "description": "Comprehensive frailty assessment for older adults. Covers Clinical Frailty Scale, falls risk, polypharmacy, cognition, nutrition, continence, and MDT care planning.",
        "category": "Geriatrics",
        "content": {
            "sections": [
                {
                    "title": "Frailty Screening",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "frail_age",
                            "type": "number",
                            "label": "Age",
                            "required": True,
                            "placeholder": "e.g., 82",
                            "output_phrase": "Age: {value}"
                        },
                        {
                            "id": "frail_cfs",
                            "type": "single_select",
                            "label": "Clinical Frailty Scale (1=Very Fit to 9=Terminally Ill)",
                            "required": True,
                            "options": [
                                "1-3 — Fit / Managing Well (not frail)",
                                "4 — Vulnerable (mild frailty)",
                                "5 — Mildly Frail (needs help with IADLs)",
                                "6 — Moderately Frail (needs help with ADLs)",
                                "7 — Severely Frail (fully dependent or terminal)",
                                "8 — Very Severely Frail (approaching end of life)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: CFS ≥6 = moderate-severe frailty. High risk of falls, hospitalisation, and adverse outcomes. Individualised care plan essential.",
                            "red_flag_negative": "",
                            "output_phrase": "Frailty score: {value}"
                        },
                        {
                            "id": "frail_living",
                            "type": "single_select",
                            "label": "Living Situation",
                            "required": True,
                            "options": [
                                "Independent — no support",
                                "Independent — with family support",
                                "Home with carers — daily",
                                "Sheltered housing / assisted living",
                                "Nursing home"
                            ],
                            "output_phrase": "Living situation: {value}"
                        }
                    ]
                },
                {
                    "title": "Falls & Mobility",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "frail_falls",
                            "type": "single_select",
                            "label": "Falls in Last 12 Months?",
                            "required": True,
                            "options": [
                                "None",
                                "1 fall — no injury",
                                "1 fall — with injury",
                                "Multiple falls (≥2)",
                                "Recurrent falls — ≥3 or with injury"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: ≥2 falls in 12 months or fall with injury = high risk. Falls assessment, OT home hazard review, consider bone health.",
                            "red_flag_negative": "",
                            "output_phrase": "Falls: {value}"
                        },
                        {
                            "id": "frail_mobility",
                            "type": "single_select",
                            "label": "Mobility",
                            "required": True,
                            "options": [
                                "Independent — walks without aid",
                                "Uses walking stick",
                                "Uses walking frame / rollator",
                                "Requires assistance to mobilise",
                                "Chairbound / bedbound"
                            ],
                            "output_phrase": "Mobility: {value}"
                        }
                    ]
                },
                {
                    "title": "Polypharmacy & Medications",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "frail_med_count",
                            "type": "single_select",
                            "label": "Number of Regular Medications",
                            "required": True,
                            "options": [
                                "0-4",
                                "5-9 (polypharmacy)",
                                "≥10 (hyperpolypharmacy)"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: ≥5 medications = polypharmacy. Medication review — identify anticholinergic burden, sedatives, hypotensive agents, and potentially inappropriate medications (STOPP/START criteria).",
                            "red_flag_negative": "",
                            "output_phrase": "Medication count: {value}"
                        },
                        {
                            "id": "frail_sedating",
                            "type": "toggle",
                            "label": "On Sedating Meds? (benzos, Z-drugs, sedating antihistamines, opioids, antipsychotics)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Sedating medications = significantly increased falls and confusion risk in frail elderly. Deprescribe where possible.",
                            "red_flag_negative": "",
                            "output_phrase": "Sedating meds: {value}"
                        },
                        {
                            "id": "frail_anticholinergic",
                            "type": "toggle",
                            "label": "Anticholinergic Burden? (amitriptyline, oxybutynin, tolterodine, promethazine)",
                            "required": False,
                            "output_phrase": "Anticholinergics: {value}"
                        }
                    ]
                },
                {
                    "title": "Cognition & Mood",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "frail_memory",
                            "type": "toggle",
                            "label": "Memory Concerns / Cognitive Decline?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Cognitive decline + frailty = high risk. Cognitive screening (MMSE/MoCA), consider dementia workup. Safety risk — kitchen, finances, driving.",
                            "red_flag_negative": "",
                            "output_phrase": "Cognitive concerns: {value}"
                        },
                        {
                            "id": "frail_mood",
                            "type": "toggle",
                            "label": "Low Mood / Depression / Social Withdrawal?",
                            "required": True,
                            "output_phrase": "Mood: {value}"
                        }
                    ]
                },
                {
                    "title": "Nutrition & Continence",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "frail_weight_loss",
                            "type": "toggle",
                            "label": "Unintentional Weight Loss? (>5% in 3 months)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Weight loss = malnutrition risk. MUST screening, dietitian referral, consider underlying cause (malignancy, depression, dementia).",
                            "red_flag_negative": "",
                            "output_phrase": "Weight loss: {value}"
                        },
                        {
                            "id": "frail_continence",
                            "type": "single_select",
                            "label": "Continence",
                            "required": True,
                            "options": [
                                "Continent",
                                "Urinary incontinence — occasional",
                                "Urinary incontinence — regular / pads",
                                "Faecal incontinence",
                                "Catheterised"
                            ],
                            "output_phrase": "Continence: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment & Care Plan",
                    "section_type": "assessment",
                    "differentials": [
                        "Frailty — mild/moderate (manage in community with MDT)",
                        "Frailty — severe (needs intensive community support / nursing home care)",
                        "Frailty + Dementia — complex care needs",
                        "Frailty + Recurrent Falls — multifactorial intervention",
                        "End-of-Life Frailty — palliative approach, advance care planning"
                    ],
                    "questions": [
                        {
                            "id": "frail_care_plan",
                            "type": "single_select",
                            "label": "Overall Care Plan",
                            "required": True,
                            "options": [
                                "Community MDT — GP + PHN + physio + OT",
                                "Medication review + deprescribing",
                                "Refer geriatric medicine / falls clinic",
                                "Advance care planning discussion",
                                "Nursing home / long-term care application",
                                "Palliative / end-of-life care approach"
                            ],
                            "output_phrase": "Care plan: {value}"
                        }
                    ]
                },
                {
                    "title": "Management & Follow-Up",
                    "section_type": "plan",
                    "safety_netting": "MDT approach: Public Health Nurse referral, Physiotherapy (strength and balance), Occupational Therapy (home hazard assessment, equipment), Dietitian if weight loss/MUST ≥2, Social worker if safeguarding concerns. Advance care planning: Discuss treatment escalation plan (TEP), preferred place of care/death, lasting power of attorney. Medication review: STOPP/START criteria — stop sedatives/anticholinergics where possible, optimise bone health (Vitamin D, calcium, consider bisphosphonate if indicated), review antihypertensives (target <150/90, avoid over-treatment). Safety-net: Crisis plan — who to contact if deterioration, red flags (confusion, falls, inability to cope at home).",
                    "questions": [
                        {
                            "id": "frail_referrals",
                            "type": "multi_select",
                            "label": "Referrals Made",
                            "required": True,
                            "options": [
                                "Public Health Nurse",
                                "Physiotherapy",
                                "Occupational Therapy",
                                "Dietitian",
                                "Social Worker",
                                "Geriatric Medicine",
                                "Falls Clinic",
                                "Palliative Care",
                                "None"
                            ],
                            "output_phrase": "Referrals: {value}"
                        },
                        {
                            "id": "frail_advance_care",
                            "type": "toggle",
                            "label": "Advance Care Planning Discussed? (TEP, preferred place of care)",
                            "required": True,
                            "output_phrase": "Advance care plan: {value}"
                        },
                        {
                            "id": "frail_crisis_plan",
                            "type": "toggle",
                            "label": "Crisis Plan in Place? (who to contact, red flags for deterioration)",
                            "required": True,
                            "output_phrase": "Crisis plan: {value}"
                        },
                        {
                            "id": "frail_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., GP review in 1 month. PHN visiting weekly. Physio assessment booked.",
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
    seed_frailty()