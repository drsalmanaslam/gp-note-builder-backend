from app.database import SessionLocal
from app.models import User, Template, Category

def seed_episcleritis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    t = {
        "title": "Episcleritis",
        "description": "Focused assessment for episcleritis covering differentiation from scleritis, red flags, phenylephrine test, and management.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "epi_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Mild discomfort and redness in right eye"},
                    {"id": "epi_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 35"},
                    {"id": "epi_side", "type": "single_select", "label": "Affected Eye", "required": True, "options": ["Right", "Left", "Both"]},
                    {"id": "epi_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 days"},
                    {"id": "epi_pain_severity", "type": "single_select", "label": "Pain Severity (0-10)", "required": True, "options": ["Mild (1-3) - episcleritis typical", "Moderate (4-6)", "Severe (7-9) - ?scleritis RED FLAG", "Excruciating (10) - scleritis RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe/deep boring pain = SCLERITIS until proven otherwise. Same-day ophthalmology referral.", "red_flag_negative": ""},
                    {"id": "epi_wakes_from_sleep", "type": "toggle", "label": "Pain Wakes Patient from Sleep?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pain waking from sleep = classic scleritis feature. Episcleritis does NOT wake from sleep. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "epi_self_limiting", "type": "toggle", "label": "Self-Limiting / Previous Episodes?", "required": False},
                    {"id": "epi_radiation", "type": "toggle", "label": "Pain Radiates to Face/Temple?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pain radiating to face/temple = suggests scleritis. Urgent ophthalmology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Scleritis & Complications",
                "section_type": "history",
                "questions": [
                    {"id": "epi_photophobia", "type": "toggle", "label": "Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Photophobia = ?uveitis/scleritis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "epi_discharge", "type": "toggle", "label": "Discharge?", "required": True},
                    {"id": "epi_visual_loss", "type": "toggle", "label": "Reduced Vision / Blurring?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual loss = ?scleritis with posterior involvement. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "epi_systemic", "type": "multi_select", "label": "Systemic Disease History", "required": True, "options": ["Rheumatoid Arthritis", "Inflammatory Bowel Disease (Crohn's/UC)", "Vasculitis", "SLE", "Ankylosing Spondylitis", "Gout", "Herpes Zoster Ophthalmicus", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Systemic autoimmune disease = ?scleritis (up to 50% association). Urgent ophthalmology referral.", "red_flag_negative": ""},
                    {"id": "epi_recurrent", "type": "toggle", "label": "Frequent Recurrent Episodes?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent/severe = warrant systemic screening (FBC, ESR/CRP, RF, ANCA, ANA, uric acid).", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "epi_injection", "type": "single_select", "label": "Vascular Injection Pattern", "required": True, "options": ["Localized/sectoral episcleral injection", "Diffuse injection", "Deep scleral (violaceous) - RED FLAG", "Ciliary flush (circumcorneal) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Deep violaceous injection or ciliary flush = ?scleritis/uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "epi_phenylephrine_test", "type": "single_select", "label": "Phenylephrine 2.5% Test", "required": False, "options": ["Vessels blanch - confirming EPISCLERITIS", "Vessels do NOT blanch - ?SCLERITIS RED FLAG", "Not performed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Non-blanching vessels = deep scleral involvement (scleritis). Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "epi_nodule", "type": "toggle", "label": "Nodule Present? (Nodular episcleritis)", "required": False},
                    {"id": "epi_va_right", "type": "text", "label": "Visual Acuity - Right", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "epi_va_left", "type": "text", "label": "Visual Acuity - Left", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "epi_cornea", "type": "single_select", "label": "Cornea", "required": True, "options": ["Clear", "Opacity - RED FLAG", "Not assessed"]},
                    {"id": "epi_anterior_chamber", "type": "single_select", "label": "Anterior Chamber", "required": False, "options": ["Normal", "Cells/flare (uveitis) - RED FLAG", "Not assessed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Episcleritis - Simple (benign, self-limiting)",
                    "Episcleritis - Nodular",
                    "Scleritis - Anterior (RED FLAG - severe pain, deep violaceous injection)",
                    "Scleritis - Posterior (RED FLAG - visual loss, retinal involvement)",
                    "Conjunctivitis (allergic/viral/bacterial)",
                    "Anterior Uveitis / Iritis (RED FLAG)",
                    "Keratitis (RED FLAG)",
                    "Subconjunctival Haemorrhage",
                    "Herpes Zoster Ophthalmicus (RED FLAG)"
                ],
                "questions": [
                    {"id": "epi_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Episcleritis - simple", "Episcleritis - nodular", "Suspected scleritis - REFER URGENTLY", "Suspected uveitis - REFER URGENTLY", "Uncertain - ophthalmology assessment"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: pain worsens significantly (especially if becomes deep/throbbing), photophobia develops, visual loss/blurring occurs, or pain starts waking from sleep. Episcleritis is benign and self-limiting (resolves in 1-3 weeks without treatment). Topical corticosteroids should NOT be initiated in primary care (risk of IOP spikes, steroid-induced cataracts, masking HSV keratitis). If recurrent or severe: screen for systemic disease (FBC, ESR/CRP, RF, ANCA, ANA, uric acid). Refer ophthalmology if: no resolution after 2 weeks of treatment, frequent recurrences, or any suspicion of scleritis.",
                "questions": [
                    {"id": "epi_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassurance + observation (mild)", "Oral NSAID (Naproxen) + topical NSAID", "Topical lubricants only", "Refer ophthalmology (urgent - ?scleritis)", "Refer ophthalmology (routine - recurrent/persistent)"]},
                    {"id": "epi_naproxen", "type": "toggle", "label": "Oral Naproxen Prescribed?", "required": False},
                    {"id": "epi_topical_nsaid", "type": "toggle", "label": "Topical Ketorolac QDS Prescribed?", "required": False},
                    {"id": "epi_artificial_tears", "type": "toggle", "label": "Lubricating Artificial Tears?", "required": False},
                    {"id": "epi_reassurance", "type": "toggle", "label": "Benign Self-Limiting Nature Explained?", "required": True},
                    {"id": "epi_no_steroids", "type": "toggle", "label": "NO Topical Steroids Warning Given?", "required": True},
                    {"id": "epi_systemic_screen", "type": "toggle", "label": "Systemic Screening Bloods? (If recurrent/severe)", "required": False},
                    {"id": "epi_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1-2 weeks if not resolved, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_episcleritis()