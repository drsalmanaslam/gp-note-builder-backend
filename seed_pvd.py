from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_pvd():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category:
        category = Category(name="Cardiovascular")
        db.add(category)
        db.commit()

    t = {
        "title": "Peripheral Vascular Disease (PVD)",
        "description": "Assessment of peripheral arterial disease including claudication history, ABPI interpretation, cardiovascular risk management, and criteria for vascular surgical referral.",
        "category": "Cardiovascular",
        "content": {
            "sections": [
                {
                    "title": "History — Claudication",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "pvd_pain_location",
                            "type": "single_select",
                            "label": "Location of Pain on Walking",
                            "required": True,
                            "options": [
                                "Calf (most common)",
                                "Thigh",
                                "Buttock / hip",
                                "Foot",
                                "Bilateral",
                                "Unilateral"
                            ],
                            "output_phrase": "Pain location: {value}"
                        },
                        {
                            "id": "pvd_claudication_distance",
                            "type": "text",
                            "label": "Claudication Distance (before pain stops walking)",
                            "required": True,
                            "placeholder": "e.g., 100 metres",
                            "output_phrase": "Claudication distance: {value}"
                        },
                        {
                            "id": "pvd_relief",
                            "type": "toggle",
                            "label": "Pain Relieved by Rest Within 2-5 Minutes? (classic claudication)",
                            "required": True,
                            "output_phrase": "Relief with rest: {value}"
                        }
                    ]
                },
                {
                    "title": "Critical Limb Ischaemia — Red Flags",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "pvd_rest_pain",
                            "type": "toggle",
                            "label": "Rest Pain? (forefoot — worse at night, relieved by hanging foot down)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Rest pain = critical limb ischaemia. Urgent vascular referral — same day. Risk of limb loss.",
                            "red_flag_negative": "",
                            "output_phrase": "Rest pain: {value}"
                        },
                        {
                            "id": "pvd_ulcer",
                            "type": "toggle",
                            "label": "Non-Healing Ulcer / Gangrene? (toes, heel, pressure points)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Non-healing ulcer/gangrene = critical limb ischaemia. Urgent same-day vascular referral. Do not delay.",
                            "red_flag_negative": "",
                            "output_phrase": "Ulcer/gangrene: {value}"
                        },
                        {
                            "id": "pvd_colour_change",
                            "type": "toggle",
                            "label": "Colour Change? (pale on elevation, dependent rubor)",
                            "required": True,
                            "output_phrase": "Colour change: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors & Comorbidities",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "pvd_risk_factors",
                            "type": "multi_select",
                            "label": "Cardiovascular Risk Factors",
                            "required": True,
                            "options": [
                                "Smoking (most important modifiable risk factor)",
                                "Diabetes mellitus",
                                "Hypertension",
                                "Hyperlipidaemia",
                                "Known coronary artery disease",
                                "Previous stroke/TIA",
                                "Age >50",
                                "Chronic kidney disease"
                            ],
                            "output_phrase": "Risk factors: {value}"
                        },
                        {
                            "id": "pvd_other_vascular",
                            "type": "toggle",
                            "label": "Symptoms of Other Vascular Disease? (angina, TIA, carotid disease)",
                            "required": True,
                            "output_phrase": "Other vascular: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "pvd_pulses",
                            "type": "single_select",
                            "label": "Peripheral Pulses",
                            "required": True,
                            "options": [
                                "All palpable — femoral, popliteal, dorsalis pedis, posterior tibial",
                                "Reduced — one or more",
                                "Absent — dorsalis pedis and/or posterior tibial",
                                "Not examined"
                            ],
                            "output_phrase": "Pulses: {value}"
                        },
                        {
                            "id": "pvd_abpi",
                            "type": "text",
                            "label": "ABPI (Ankle-Brachial Pressure Index) — if available",
                            "required": False,
                            "placeholder": "e.g., 0.6 right, 0.9 left",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: ABPI <0.5 = severe PVD / critical ischaemia. Urgent vascular referral. ABPI >1.3 = non-compressible (calcified vessels — diabetes/CKD).",
                            "red_flag_negative": "",
                            "output_phrase": "ABPI: {value}"
                        },
                        {
                            "id": "pvd_buerger",
                            "type": "single_select",
                            "label": "Buerger's Test (pallor on elevation, rubor on dependency)",
                            "required": False,
                            "options": [
                                "Normal",
                                "Positive — pallor at <30° elevation",
                                "Dependent rubor present",
                                "Not tested"
                            ],
                            "output_phrase": "Buerger's test: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Peripheral Arterial Disease — intermittent claudication (stable)",
                        "Critical Limb Ischaemia — rest pain ± ulcer/gangrene (urgent)",
                        "Spinal Stenosis — bilateral, relieved by leaning forward, not rest alone",
                        "Peripheral Neuropathy — burning/numbness, not exercise-induced",
                        "Musculoskeletal pain — not relieved quickly by rest",
                        "DVT — acute unilateral swelling/pain, not chronic",
                        "Buerger's Disease (young male smokers)"
                    ],
                    "questions": [
                        {
                            "id": "pvd_severity",
                            "type": "single_select",
                            "label": "Fontaine Classification",
                            "required": True,
                            "options": [
                                "I — Asymptomatic",
                                "IIa — Mild claudication (>200m)",
                                "IIb — Moderate-severe claudication (<200m)",
                                "III — Rest pain (critical ischaemia)",
                                "IV — Ulceration/gangrene (critical ischaemia)"
                            ],
                            "output_phrase": "Fontaine: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "CRITICAL LIMB ISCHAEMIA (Fontaine III-IV): Same-day urgent vascular referral. Limb salvage depends on early revascularisation. INTERMITTENT CLAUDICATION: Smoking cessation — single most effective intervention. Supervised exercise programme — 3x/week, 30-45 min walking to near-max pain. Cardiovascular risk optimisation: Antiplatelet (Aspirin 75mg or Clopidogrel 75mg), Statin (Atorvastatin 80mg), BP control (<140/90 or <130/80 if diabetic), HbA1c optimisation if diabetic. Refer vascular surgery if: Claudication interfering with daily life despite 3-6 months conservative management, critical limb ischaemia, or ABPI <0.5. Safety-net: Return immediately if rest pain, non-healing ulcer, or gangrene develops.",
                    "questions": [
                        {
                            "id": "pvd_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Conservative — exercise + risk factor management",
                                "Start antiplatelet + statin + BP control",
                                "Routine vascular referral (lifestyle-limiting claudication)",
                                "Urgent vascular referral (critical ischaemia)",
                                "Smoking cessation referral"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "pvd_antiplatelet",
                            "type": "toggle",
                            "label": "Antiplatelet Started? (Aspirin 75mg or Clopidogrel 75mg)",
                            "required": False,
                            "output_phrase": "Antiplatelet: {value}"
                        },
                        {
                            "id": "pvd_statin",
                            "type": "toggle",
                            "label": "High-Intensity Statin Started? (Atorvastatin 80mg)",
                            "required": False,
                            "output_phrase": "Statin: {value}"
                        },
                        {
                            "id": "pvd_exercise",
                            "type": "toggle",
                            "label": "Supervised Exercise Programme Advised?",
                            "required": False,
                            "output_phrase": "Exercise advice: {value}"
                        },
                        {
                            "id": "pvd_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 3 months. Exercise programme. If no improvement, refer vascular.",
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
    seed_pvd()