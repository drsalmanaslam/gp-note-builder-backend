from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_sudden_vision_loss():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Eye").first()
    if not category:
        category = Category(name="Eye")
        db.add(category)
        db.commit()

    t = {
        "title": "Sudden Vision Loss — Urgent Assessment",
        "description": "Rapid triage of acute vision loss. Differentiates between ocular emergencies (CRAO, retinal detachment, GCA) requiring same-day ophthalmology referral.",
        "category": "Eye",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "svl_onset",
                            "type": "single_select",
                            "label": "Onset",
                            "required": True,
                            "options": [
                                "Sudden — seconds/minutes",
                                "Over hours",
                                "Over days",
                                "Woke up with it"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Sudden painless vision loss = ?CRAO/CRVO/retinal detachment. Emergency ophthalmology referral same day.",
                            "red_flag_negative": "",
                            "output_phrase": "Onset: {value}"
                        },
                        {
                            "id": "svl_laterality",
                            "type": "single_select",
                            "label": "One Eye or Both?",
                            "required": True,
                            "options": ["Unilateral", "Bilateral"],
                            "output_phrase": "Laterality: {value}"
                        },
                        {
                            "id": "svl_pain",
                            "type": "toggle",
                            "label": "Pain? (if yes = ?optic neuritis, acute glaucoma, GCA)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Pain + vision loss = ?acute angle-closure glaucoma (hard eye, nausea, halos) or optic neuritis. Same-day ophthalmology.",
                            "red_flag_negative": "",
                            "output_phrase": "Pain: {value}"
                        },
                        {
                            "id": "svl_flashes_floaters",
                            "type": "toggle",
                            "label": "Flashes / Floaters Preceding? (curtain/shadow = ?retinal detachment)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Flashes/floaters + curtain/shadow = ?retinal detachment. Emergency ophthalmology — same day.",
                            "red_flag_negative": "",
                            "output_phrase": "Flashes/floaters: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flags — Must Ask",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "svl_gca",
                            "type": "toggle",
                            "label": "Scalp Tenderness / Jaw Claudication / Headache? (?GCA — age >50)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: ?Giant Cell Arteritis — risk of bilateral blindness. Start high-dose steroids (Prednisolone 60mg) IMMEDIATELY if suspected. Same-day ophthalmology. Check ESR/CRP.",
                            "red_flag_negative": "",
                            "output_phrase": "GCA symptoms: {value}"
                        },
                        {
                            "id": "svl_amaurosis",
                            "type": "toggle",
                            "label": "Transient Vision Loss Before? (Amaurosis Fugax — ?TIA)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Amaurosis fugax = ?retinal TIA. Same-day TIA clinic. Check carotids, start aspirin 300mg. Vascular risk assessment.",
                            "red_flag_negative": "",
                            "output_phrase": "Amaurosis fugax: {value}"
                        },
                        {
                            "id": "svl_trauma",
                            "type": "toggle",
                            "label": "Recent Trauma / Surgery?",
                            "required": False,
                            "output_phrase": "Trauma: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "svl_visual_acuity",
                            "type": "single_select",
                            "label": "Visual Acuity (Snellen)",
                            "required": True,
                            "options": [
                                "6/6 normal",
                                "6/9 to 6/12 — mild loss",
                                "6/18 to 6/36 — moderate loss",
                                "6/60 or worse — severe",
                                "Hand movements only",
                                "Perception of light only",
                                "No perception of light"
                            ],
                            "output_phrase": "Visual acuity: {value}"
                        },
                        {
                            "id": "svl_rapd",
                            "type": "single_select",
                            "label": "RAPD (Swinging Light Test)?",
                            "required": False,
                            "options": [
                                "Normal — no RAPD",
                                "RAPD present",
                                "Not tested"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: RAPD present = optic nerve pathology or severe retinal disease. Urgent ophthalmology referral.",
                            "red_flag_negative": "",
                            "output_phrase": "RAPD: {value}"
                        },
                        {
                            "id": "svl_red_reflex",
                            "type": "single_select",
                            "label": "Red Reflex",
                            "required": False,
                            "options": [
                                "Normal",
                                "Absent / dark — ?vitreous haemorrhage, retinal detachment, cataract",
                                "Not tested"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Absent red reflex = significant ocular pathology. Urgent ophthalmology.",
                            "red_flag_negative": "",
                            "output_phrase": "Red reflex: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Central Retinal Artery Occlusion (CRAO) — painless, sudden, unilateral",
                        "Central Retinal Vein Occlusion (CRVO) — painless, subacute",
                        "Retinal Detachment — flashes/floaters, curtain/shadow",
                        "Acute Angle-Closure Glaucoma — painful, red eye, halos, N/V",
                        "Giant Cell Arteritis — >50, headache, scalp tenderness, jaw claudication",
                        "Optic Neuritis — painful eye movements, reduced colour vision, ?MS",
                        "Amaurosis Fugax — transient, vascular origin",
                        "Vitreous Haemorrhage"
                    ],
                    "questions": [
                        {
                            "id": "svl_diagnosis",
                            "type": "single_select",
                            "label": "Clinical Impression",
                            "required": True,
                            "options": [
                                "CRAO — emergency ophthalmology",
                                "CRVO — urgent ophthalmology",
                                "Retinal detachment — emergency",
                                "Acute glaucoma — emergency",
                                "?GCA — start steroids + urgent ophthalmology",
                                "Amaurosis fugax — TIA workup",
                                "Other"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Emergency (same-day ophthalmology): CRAO, CRVO, retinal detachment, acute glaucoma, ?GCA. If ?GCA: Start Prednisolone 60mg PO immediately — do not wait for investigation results. Check ESR/CRP urgently. Temporal artery biopsy within 2 weeks. If amaurosis fugax: Aspirin 300mg stat, urgent TIA clinic. Driving: Must not drive with sudden vision loss — notify insurance/DVLA. Patient advised: Return immediately if vision worsens, pain develops, or second eye becomes affected.",
                    "questions": [
                        {
                            "id": "svl_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Same-day ophthalmology referral (emergency)",
                                "Urgent ophthalmology (within 48h)",
                                "Start steroids + refer (suspected GCA)",
                                "TIA clinic referral (amaurosis fugax)",
                                "Routine ophthalmology referral"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "svl_steroids",
                            "type": "toggle",
                            "label": "High-Dose Steroids Started? (if ?GCA — Prednisolone 60mg)",
                            "required": False,
                            "output_phrase": "Steroids: {value}"
                        },
                        {
                            "id": "svl_driving",
                            "type": "toggle",
                            "label": "Driving Advice Given? (Must not drive)",
                            "required": True,
                            "output_phrase": "Driving advice: {value}"
                        },
                        {
                            "id": "svl_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Ophthalmology same day. GP to check ESR/CRP results tomorrow.",
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
    seed_sudden_vision_loss()