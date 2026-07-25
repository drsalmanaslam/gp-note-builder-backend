from app.database import SessionLocal
from app.models import User, Template, Category

def seed_infective_conjunctivitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    t = {
        "title": "Infective Conjunctivitis Assessment",
        "description": "Focused assessment for infective conjunctivitis covering bacterial vs viral differentiation, antibiotic stewardship, and red flags.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "ic_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Red, sticky eye with discharge for 2 days"},
                    {"id": "ic_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 32"},
                    {"id": "ic_side", "type": "single_select", "label": "Affected Eye(s)", "required": True, "options": ["Right", "Left", "Both (started unilateral → bilateral)"]},
                    {"id": "ic_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 days"},
                    {"id": "ic_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Itching", "Gritty sensation", "Purulent/mucoid discharge", "Morning crusting/sticking", "Watery discharge (viral)", "Burning", "Tearing"]},
                    {"id": "ic_type", "type": "single_select", "label": "Likely Type Based on Discharge", "required": True, "options": ["Purulent/mucoid (bacterial)", "Watery (viral)", "Mixed", "Uncertain"]},
                    {"id": "ic_contact_lenses", "type": "toggle", "label": "Contact Lens Wearer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Contact lens + red eye = ?Pseudomonas keratitis. Quinolone coverage needed (Levofloxacin/Moxifloxacin). Fusidic acid ineffective. Urgent ophthalmology if corneal involvement.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Serious Ocular Pathology",
                "section_type": "history",
                "questions": [
                    {"id": "ic_eye_pain", "type": "toggle", "label": "True Ocular Pain? (Not just discomfort)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: True eye pain = ?keratitis, uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "ic_photophobia", "type": "toggle", "label": "Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Photophobia = ?keratitis, uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "ic_visual_loss", "type": "toggle", "label": "Visual Loss / Blurring?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual loss = ?keratitis, uveitis, acute glaucoma. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "ic_foreign_body", "type": "toggle", "label": "Foreign Body Sensation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Foreign body sensation = ?corneal FB/abrasion. Evert lids + fluorescein stain.", "red_flag_negative": ""},
                    {"id": "ic_unilateral_severe", "type": "toggle", "label": "Severe Unilateral Redness?", "required": False},
                    {"id": "ic_neonatal", "type": "toggle", "label": "Neonate? (<1 month)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neonatal conjunctivitis = urgent ophthalmology. ?Chlamydia/Gonococcal. Needs systemic treatment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ic_conjunctiva", "type": "single_select", "label": "Conjunctiva", "required": True, "options": ["Diffuse injection + purulent exudate", "Diffuse injection + watery discharge", "Follicles (viral/chlamydial)", "Papillae", "Mild injection"]},
                    {"id": "ic_va_right", "type": "text", "label": "Visual Acuity - Right", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "ic_va_left", "type": "text", "label": "Visual Acuity - Left", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "ic_preauricular_ln", "type": "toggle", "label": "Pre-Auricular Lymphadenopathy? (Viral/Chlamydial)", "required": False},
                    {"id": "ic_cornea", "type": "single_select", "label": "Cornea", "required": True, "options": ["Clear", "Opacity/ulcer - RED FLAG", "Fluorescein uptake", "Not assessed"]},
                    {"id": "ic_lids", "type": "toggle", "label": "Molluscum Contagiosum on Eyelids? (Chronic follicular conjunctivitis)", "required": False},
                    {"id": "ic_blepharitis", "type": "toggle", "label": "Blepharitis Present?", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Bacterial Conjunctivitis (purulent discharge, crusting)",
                    "Viral Conjunctivitis (watery, preauricular node, often bilateral)",
                    "Chlamydial Conjunctivitis (chronic, follicles, preauricular node)",
                    "Allergic Conjunctivitis (itchy, watery, bilateral, history of atopy)",
                    "Gonococcal Conjunctivitis (RED FLAG - severe purulent, rapid onset)",
                    "Keratitis (RED FLAG - pain + photophobia + corneal opacity)",
                    "Anterior Uveitis / Iritis (RED FLAG)",
                    "Acute Angle-Closure Glaucoma (RED FLAG - mid-dilated pupil, hazy cornea)",
                    "Contact Lens-Associated Keratitis (RED FLAG - Pseudomonas)"
                ],
                "questions": [
                    {"id": "ic_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Bacterial conjunctivitis", "Viral conjunctivitis", "Mixed infective conjunctivitis", "Suspected chlamydial - REFER", "Suspected keratitis - REFER URGENTLY", "Suspected uveitis - REFER URGENTLY"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: severe eye pain, photophobia, marked redness around the iris (limbal flush), or visual changes develop. Infective conjunctivitis is usually self-limiting (5-7 days without treatment). Topical antibiotics shorten symptom duration by only ~6 hours by Day 5 - no significant difference by Day 7. Antibiotics may reduce contagiousness marginally. Highly contagious: strict hand hygiene, avoid sharing towels/pillowcases. Bathe/clean eyelids with cotton wool + sterile saline or cooled boiled water to remove crusts. No routine school/work exclusion required unless outbreak or child unwell. If contact lens wearer: remove lenses, do NOT wear until fully resolved.",
                "questions": [
                    {"id": "ic_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassurance + hygiene only (self-limiting)", "Chloramphenicol 0.5% drops QDS for 5 days", "Chloramphenicol 1% ointment QDS for 5 days", "Fusidic Acid 1% (Fucithalmic) BD for 5 days", "Refer ophthalmology (urgent)", "Refer ophthalmology (routine)"]},
                    {"id": "ic_antibiotic_counselling", "type": "toggle", "label": "Antibiotic Stewardship Counselled? (Only ~6h benefit by Day 5)", "required": False},
                    {"id": "ic_hygiene", "type": "toggle", "label": "Hygiene Advice Given? (Hand washing, no shared towels, lid cleaning)", "required": True},
                    {"id": "ic_exclusion", "type": "toggle", "label": "School/Work Exclusion Advised? (Not routinely required)", "required": False},
                    {"id": "ic_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 5-7 days if not resolving, sooner if red flags"}
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
    seed_infective_conjunctivitis()