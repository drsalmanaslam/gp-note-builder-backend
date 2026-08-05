from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_cataracts():
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
        "title": "Cataracts — Assessment & Referral",
        "description": "Assessment of cataracts including symptoms, visual impact, red flags for other pathology, and criteria for routine ophthalmology referral for cataract surgery.",
        "category": "Eye",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "cat_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms",
                            "required": True,
                            "options": [
                                "Gradual painless blurring of vision",
                                "Glare / halos around lights (especially night driving)",
                                "Faded / yellowing colours",
                                "Frequent prescription changes",
                                "Double vision in one eye (monocular diplopia)",
                                "Difficulty reading / watching TV",
                                "Difficulty with night driving"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        },
                        {
                            "id": "cat_duration",
                            "type": "text",
                            "label": "Duration & Progression",
                            "required": True,
                            "placeholder": "e.g., 12 months — gradually worsening",
                            "output_phrase": "Duration: {value}"
                        },
                        {
                            "id": "cat_laterality",
                            "type": "single_select",
                            "label": "One Eye or Both?",
                            "required": True,
                            "options": [
                                "Unilateral",
                                "Bilateral — asymmetrical",
                                "Bilateral — symmetrical"
                            ],
                            "output_phrase": "Laterality: {value}"
                        }
                    ]
                },
                {
                    "title": "Impact on Daily Life",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "cat_driving",
                            "type": "single_select",
                            "label": "Effect on Driving",
                            "required": True,
                            "options": [
                                "No driving",
                                "Still driving safely",
                                "Difficulty with night driving",
                                "Given up driving due to vision",
                                "Concerned about driving safety"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Patient still driving with significant visual impairment = safety risk. Advise DVLA notification if below legal standard (6/12 binocular).",
                            "red_flag_negative": "",
                            "output_phrase": "Driving: {value}"
                        },
                        {
                            "id": "cat_reading",
                            "type": "toggle",
                            "label": "Difficulty Reading / Watching TV Despite Glasses?",
                            "required": True,
                            "output_phrase": "Reading difficulty: {value}"
                        },
                        {
                            "id": "cat_falls",
                            "type": "toggle",
                            "label": "Falls / Mobility Issues Due to Vision?",
                            "required": True,
                            "output_phrase": "Falls risk: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors & Red Flags",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "cat_risk_factors",
                            "type": "multi_select",
                            "label": "Risk Factors",
                            "required": True,
                            "options": [
                                "Age >65",
                                "Diabetes mellitus",
                                "Prolonged steroid use (oral or topical)",
                                "Previous eye surgery / trauma",
                                "UV exposure",
                                "Smoking",
                                "Family history",
                                "None"
                            ],
                            "output_phrase": "Risk factors: {value}"
                        },
                        {
                            "id": "cat_pain",
                            "type": "toggle",
                            "label": "Eye Pain / Redness? (not typical of cataract — ?other pathology)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Pain/redness not typical of cataract. Rule out acute angle-closure glaucoma, uveitis, keratitis. Same-day ophthalmology if acute.",
                            "red_flag_negative": "",
                            "output_phrase": "Pain/redness: {value}"
                        },
                        {
                            "id": "cat_flashes_floaters",
                            "type": "toggle",
                            "label": "Flashes / Floaters / Curtain? (?retinal detachment)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Flashes/floaters/curtain = ?retinal detachment. Emergency ophthalmology — same day.",
                            "red_flag_negative": "",
                            "output_phrase": "Flashes/floaters: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "cat_visual_acuity",
                            "type": "single_select",
                            "label": "Visual Acuity (Snellen — with pinhole correction)",
                            "required": True,
                            "options": [
                                "6/6 — normal",
                                "6/9 to 6/12 — mild impairment",
                                "6/18 to 6/36 — moderate",
                                "6/60 or worse — severe impairment",
                                "Counting fingers / hand movements only"
                            ],
                            "output_phrase": "Visual acuity: {value}"
                        },
                        {
                            "id": "cat_red_reflex",
                            "type": "single_select",
                            "label": "Red Reflex (direct ophthalmoscope — darkened room)",
                            "required": False,
                            "options": [
                                "Normal — clear red reflex",
                                "Dark patches / spoke-like opacities — cataract",
                                "Absent — dense cataract or other pathology",
                                "Not examined"
                            ],
                            "output_phrase": "Red reflex: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Cataract — age-related (most common)",
                        "Diabetic Cataract — younger age, rapid progression",
                        "Steroid-Induced Cataract — posterior subcapsular",
                        "Age-Related Macular Degeneration — central distortion, drusen on fundoscopy",
                        "Glaucoma — optic disc cupping, raised IOP, visual field loss",
                        "Diabetic Retinopathy — dot/blot haemorrhages, exudates",
                        "Corneal Opacity / Scarring"
                    ],
                    "questions": [
                        {
                            "id": "cat_diagnosis",
                            "type": "single_select",
                            "label": "Diagnosis",
                            "required": True,
                            "options": [
                                "Cataract — visually significant, refer for surgery",
                                "Cataract — mild, not yet affecting daily life, observe",
                                "Cataract + other pathology — refer ophthalmology",
                                "Not cataract — alternative diagnosis"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Refer for cataract surgery when: visual acuity 6/12 or worse (or significant impact on daily life — driving, reading, falls risk). Routine ophthalmology referral with visual acuity and impact on daily life documented. No need for further investigation in primary care — ophthalmology does pre-op assessment (biometry, IOP, dilated fundoscopy). While waiting: optimize lighting at home, update glasses if needed (though cataracts limit benefit). Discuss driving — must meet DVLA standard (6/12 binocular, able to read number plate at 20.5m). Control modifiable risk factors: smoking cessation, tight glucose control if diabetic. Safety-net: Return if sudden vision change, pain, redness, flashes/floaters, or significant deterioration while awaiting surgery.",
                    "questions": [
                        {
                            "id": "cat_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "Routine ophthalmology referral — cataract surgery",
                                "Observe — mild, review if deteriorates",
                                "Urgent ophthalmology — other pathology suspected",
                                "Driving advice only"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "cat_driving_advice",
                            "type": "toggle",
                            "label": "Driving Advice Given? (must meet DVLA standard — 6/12 binocular)",
                            "required": False,
                            "output_phrase": "Driving advice: {value}"
                        },
                        {
                            "id": "cat_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if sudden change / pain / flashes)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "cat_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Routine ophthalmology referral sent. Await pre-op assessment. Review if vision deteriorates.",
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
    seed_cataracts()