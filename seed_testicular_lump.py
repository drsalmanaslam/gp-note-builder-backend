from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_testicular_lump():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category:
        category = Category(name="Men's Health")
        db.add(category)
        db.commit()

    t = {
        "title": "Testicular Lump — Urgent Assessment",
        "description": "Urgent assessment of testicular lumps. Key red flags for testicular cancer, examination findings, and 2-week wait referral pathway.",
        "category": "Men's Health",
        "content": {
            "sections": [
                {
                    "title": "History",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tl_age",
                            "type": "number",
                            "label": "Age (peak incidence 15-35 years)",
                            "required": True,
                            "placeholder": "e.g., 28",
                            "output_phrase": "Age: {value}"
                        },
                        {
                            "id": "tl_discovery",
                            "type": "single_select",
                            "label": "How Was Lump Discovered?",
                            "required": True,
                            "options": [
                                "Self-examination",
                                "Incidental finding",
                                "Partner noticed",
                                "Pain led to examination",
                                "Routine check"
                            ],
                            "output_phrase": "Discovery: {value}"
                        },
                        {
                            "id": "tl_duration",
                            "type": "text",
                            "label": "Duration",
                            "required": True,
                            "placeholder": "e.g., 3 weeks",
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Any testicular lump >2 weeks = urgent 2-week wait referral for ?testicular cancer. Do not delay.",
                            "red_flag_negative": "",
                            "output_phrase": "Duration: {value}"
                        }
                    ]
                },
                {
                    "title": "Red Flag Symptoms",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tl_pain",
                            "type": "toggle",
                            "label": "Pain? (testicular cancer often painless)",
                            "required": True,
                            "output_phrase": "Pain: {value}"
                        },
                        {
                            "id": "tl_size_change",
                            "type": "toggle",
                            "label": "Increasing in Size?",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Enlarging testicular mass = ?malignancy until proven otherwise. 2-week wait urology.",
                            "red_flag_negative": "",
                            "output_phrase": "Size change: {value}"
                        },
                        {
                            "id": "tl_back_pain",
                            "type": "toggle",
                            "label": "Back Pain / SOB / Weight Loss? (?metastatic disease)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Back pain/weight loss + testicular lump = ?metastatic testicular cancer. Urgent same-day urology referral.",
                            "red_flag_negative": "",
                            "output_phrase": "Systemic symptoms: {value}"
                        },
                        {
                            "id": "tl_trauma",
                            "type": "toggle",
                            "label": "Recent Trauma?",
                            "required": False,
                            "output_phrase": "Trauma: {value}"
                        },
                        {
                            "id": "tl_infection",
                            "type": "toggle",
                            "label": "Fever / Dysuria / Urethral Discharge? (?epididymo-orchitis)",
                            "required": False,
                            "output_phrase": "Infection symptoms: {value}"
                        }
                    ]
                },
                {
                    "title": "Risk Factors",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "tl_risk",
                            "type": "multi_select",
                            "label": "Risk Factors",
                            "required": True,
                            "options": [
                                "Undescended testis (cryptorchidism) — even if corrected",
                                "Previous testicular cancer (contralateral risk)",
                                "Family history — father/brother",
                                "Infertility",
                                "HIV",
                                "None"
                            ],
                            "output_phrase": "Risk factors: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "tl_laterality",
                            "type": "single_select",
                            "label": "Side",
                            "required": True,
                            "options": ["Left", "Right", "Bilateral"],
                            "output_phrase": "Side: {value}"
                        },
                        {
                            "id": "tl_site",
                            "type": "single_select",
                            "label": "Site of Lump",
                            "required": True,
                            "options": [
                                "Within testis (intratesticular) — RED FLAG",
                                "Epididymis / paratesticular",
                                "Spermatic cord",
                                "Scrotal skin",
                                "Diffuse testicular swelling"
                            ],
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Intratesticular mass = ?testicular cancer until proven otherwise. 2-week wait urology. Do NOT delay for ultrasound.",
                            "red_flag_negative": "",
                            "output_phrase": "Site: {value}"
                        },
                        {
                            "id": "tl_consistency",
                            "type": "single_select",
                            "label": "Consistency",
                            "required": True,
                            "options": [
                                "Hard / firm — irregular",
                                "Smooth / cystic",
                                "Soft",
                                "Tender",
                                "Unable to get above swelling"
                            ],
                            "output_phrase": "Consistency: {value}"
                        },
                        {
                            "id": "tl_transilluminate",
                            "type": "toggle",
                            "label": "Transilluminates? (hydrocoele)",
                            "required": False,
                            "output_phrase": "Transillumination: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Testicular Cancer (seminoma / non-seminoma) — intratesticular, hard, non-tender",
                        "Epididymal Cyst — separate from testis, smooth, transilluminates",
                        "Hydrocoele — transilluminable, can get above it",
                        "Epididymo-orchitis — tender, fever, dysuria",
                        "Varicocoele — bag of worms, left-sided, disappears lying down",
                        "Inguinal Hernia — cough impulse, can get above it",
                        "Testicular Torsion — acute pain, high-riding, absent cremasteric (emergency)"
                    ],
                    "questions": [
                        {
                            "id": "tl_diagnosis",
                            "type": "single_select",
                            "label": "Clinical Impression",
                            "required": True,
                            "options": [
                                "?Testicular Cancer — 2-week wait urology",
                                "?Testicular Cancer with systemic symptoms — urgent same-day urology",
                                "Epididymal cyst / hydrocoele — benign, reassure",
                                "Epididymo-orchitis — treat + safety-net",
                                "Varicocoele — routine referral if symptomatic",
                                "Other — see differentials"
                            ],
                            "output_phrase": "Diagnosis: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If intratesticular mass: 2-week wait urology referral. Do NOT wait for ultrasound — refer directly. Scrotal ultrasound is investigation of choice but should not delay referral. If epididymal cyst / hydrocoele: Reassure — benign. Routine ultrasound if diagnostic uncertainty. If epididymo-orchitis: Antibiotics, safety-net, ensure testicular exam normal after infection resolves. If varicocoele: Refer if symptomatic or infertility. Safety-net: Return if lump enlarges, becomes painful, or systemic symptoms develop. Testicular cancer is highly curable (>95% if early stage) — early diagnosis is critical.",
                    "questions": [
                        {
                            "id": "tl_action",
                            "type": "single_select",
                            "label": "Action",
                            "required": True,
                            "options": [
                                "2-week wait urology referral — ?testicular cancer",
                                "Same-day urology — systemic symptoms / metastatic concern",
                                "Routine urology referral (varicocoele / benign)",
                                "Reassure + discharge (epididymal cyst/hydrocoele)",
                                "Treat infection + safety-net review"
                            ],
                            "output_phrase": "Action: {value}"
                        },
                        {
                            "id": "tl_ultrasound",
                            "type": "toggle",
                            "label": "Scrotal Ultrasound Requested? (not for cancer referral — refer directly)",
                            "required": False,
                            "output_phrase": "Ultrasound: {value}"
                        },
                        {
                            "id": "tl_safety_net",
                            "type": "toggle",
                            "label": "Safety-Net Given? (return if enlarges / pain / systemic symptoms)",
                            "required": True,
                            "output_phrase": "Safety-net: {value}"
                        },
                        {
                            "id": "tl_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., 2-week wait urology referral sent. Review if not seen within 2 weeks.",
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
    seed_testicular_lump()