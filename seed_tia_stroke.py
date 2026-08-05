from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_tia_stroke():
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
        "title": "TIA / Stroke — Urgent Assessment",
        "description": "Rapid assessment for suspected TIA/stroke using FAST/ROSIER criteria. Guides urgent referral to acute stroke unit or TIA clinic.",
        "category": "Neurology",
        "content": {
            "sections": [
                {
                    "title": "FAST Assessment",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "tia_face",
                            "type": "single_select",
                            "label": "FACE — Facial Drooping?",
                            "required": True,
                            "options": ["Normal", "Unilateral droop / asymmetry"],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Facial droop = ?stroke. Call 999 immediately. Time of onset documented.",
                            "red_flag_negative": "",
                            "output_phrase": "Face: {value}"
                        },
                        {
                            "id": "tia_arms",
                            "type": "single_select",
                            "label": "ARMS — Arm Weakness / Drift?",
                            "required": True,
                            "options": ["Normal — both arms lift equally", "Unilateral weakness / drift"],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Arm weakness = ?stroke. Call 999 immediately.",
                            "red_flag_negative": "",
                            "output_phrase": "Arms: {value}"
                        },
                        {
                            "id": "tia_speech",
                            "type": "single_select",
                            "label": "SPEECH — Slurred or Difficulty Speaking?",
                            "required": True,
                            "options": ["Normal speech", "Slurred / dysarthric", "Expressive dysphasia", "Receptive dysphasia"],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Speech disturbance = ?stroke. Call 999 immediately.",
                            "red_flag_negative": "",
                            "output_phrase": "Speech: {value}"
                        },
                        {
                            "id": "tia_time",
                            "type": "text",
                            "label": "TIME — Time of Onset (or when last seen well)",
                            "required": True,
                            "placeholder": "e.g., 14:30 today",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: If onset <4.5 hours = eligible for thrombolysis. Call 999 immediately — time-critical.",
                            "red_flag_negative": "",
                            "output_phrase": "Time of onset: {value}"
                        }
                    ]
                },
                {
                    "title": "Additional ROSIER Criteria",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tia_visual",
                            "type": "toggle",
                            "label": "Visual Field Defect / Diplopia?",
                            "required": True,
                            "output_phrase": "Visual disturbance: {value}"
                        },
                        {
                            "id": "tia_gait",
                            "type": "toggle",
                            "label": "Acute Gait Disturbance / Vertigo?",
                            "required": True,
                            "output_phrase": "Gait/vertigo: {value}"
                        },
                        {
                            "id": "tia_syncope",
                            "type": "toggle",
                            "label": "Loss of Consciousness / Syncope at Onset?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: LOC at onset = ?posterior circulation stroke or seizure. Urgent assessment.",
                            "red_flag_negative": "",
                            "output_phrase": "LOC: {value}"
                        },
                        {
                            "id": "tia_resolved",
                            "type": "toggle",
                            "label": "Symptoms Fully Resolved? (if yes = ?TIA not stroke)",
                            "required": True,
                            "output_phrase": "Symptoms resolved: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors & History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tia_af",
                            "type": "toggle",
                            "label": "Known AF / Irregular Pulse?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: AF = high stroke risk. Check if anticoagulated. If TIA despite anticoagulation, needs urgent review.",
                            "red_flag_negative": "",
                            "output_phrase": "AF: {value}"
                        },
                        {
                            "id": "tia_anticoagulated",
                            "type": "toggle",
                            "label": "On Anticoagulation? (warfarin/DOAC)",
                            "required": False,
                            "output_phrase": "Anticoagulated: {value}"
                        },
                        {
                            "id": "tia_previous",
                            "type": "toggle",
                            "label": "Previous TIA / Stroke?",
                            "required": True,
                            "output_phrase": "Previous TIA/stroke: {value}"
                        },
                        {
                            "id": "tia_htn_dm",
                            "type": "toggle",
                            "label": "Hypertension / Diabetes / Hyperlipidaemia?",
                            "required": False,
                            "output_phrase": "Vascular risk factors: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment & ABCD2 Score",
                    "section_type": "assessment",
                    "differentials": [
                        "Stroke (acute ischaemic/haemorrhagic) — symptoms persisting",
                        "TIA — symptoms resolved within 24 hours",
                        "Migraine with aura",
                        "Hypoglycaemia",
                        "Seizure with Todd's paresis",
                        "Functional neurological disorder"
                    ],
                    "questions": [
                        {
                            "id": "tia_diagnosis",
                            "type": "single_select",
                            "label": "Clinical Impression",
                            "required": True,
                            "options": [
                                "Suspected ACUTE STROKE — call 999",
                                "TIA (symptoms resolved) — urgent TIA clinic",
                                "Not stroke/TIA — alternative diagnosis"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        },
                        {
                            "id": "tia_abcd2",
                            "type": "single_select",
                            "label": "ABCD2 Score (if TIA, symptoms resolved)",
                            "required": False,
                            "options": [
                                "Low risk (0-3) — TIA clinic within 1 week",
                                "High risk (4-7) — TIA clinic within 24 hours"
                            ],
                            "output_phrase": "ABCD2: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Suspected stroke with ongoing symptoms: Call 999 immediately — time is brain. Thrombolysis window = 4.5 hours. Do not give aspirin in community if stroke suspected (may be haemorrhagic). TIA (resolved): Aspirin 300mg stat and daily until seen in TIA clinic. Refer to TIA clinic — high risk (ABCD2 ≥4 or AF or >1 episode in week): within 24 hours. Low risk: within 1 week. If on anticoagulant and TIA occurs: refer urgently — may need switch of agent. Driving: Must not drive for 1 month post-stroke or TIA. Notify insurance. Patient/carer advised: If any new facial droop, arm weakness, speech difficulty — call 999 immediately.",
                    "questions": [
                        {
                            "id": "tia_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "999 ambulance — acute stroke pathway",
                                "Aspirin 300mg stat + urgent TIA clinic (within 24h)",
                                "Aspirin 300mg stat + TIA clinic (within 1 week)",
                                "Not TIA/stroke — alternative management"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "tia_aspirin",
                            "type": "toggle",
                            "label": "Aspirin 300mg Given? (only if TIA and not haemorrhagic)",
                            "required": False,
                            "output_phrase": "Aspirin given: {value}"
                        },
                        {
                            "id": "tia_driving",
                            "type": "toggle",
                            "label": "Driving Advice Given? (Must not drive for 1 month)",
                            "required": True,
                            "output_phrase": "Driving advice: {value}"
                        },
                        {
                            "id": "tia_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., TIA clinic referral sent. GP review in 1 week.",
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
    seed_tia_stroke()