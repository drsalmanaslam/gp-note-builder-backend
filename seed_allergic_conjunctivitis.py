from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_allergic_conjunctivitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    t = {
        "title": "Allergic Conjunctivitis",
        "description": "Focused assessment for allergic conjunctivitis covering red flags for serious ocular pathology, topical treatment, and safety netting.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "ac_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Bilateral itchy, watery, red eyes with runny nose"},
                    {"id": "ac_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 28"},
                    {"id": "ac_side", "type": "single_select", "label": "Affected Eye(s)", "required": True, "options": ["Bilateral", "Right only", "Left only"]},
                    {"id": "ac_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 1 week"},
                    {"id": "ac_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Seasonal (spring/summer)", "Perennial (year-round)", "Acute episode", "First episode", "Recurrent"]},
                    {"id": "ac_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Itching (predominant)", "Watery discharge", "Redness", "Swelling", "Burning", "Gritty sensation"]},
                    {"id": "ac_rhinitis", "type": "toggle", "label": "Associated Rhinitis? (Runny nose, sneezing, nasal itch)", "required": True},
                    {"id": "ac_contact_lenses", "type": "toggle", "label": "Contact Lens Wearer?", "required": True},
                    {"id": "ac_recent_surgery", "type": "toggle", "label": "Recent Ocular Surgery?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent eye surgery + red eye = urgent ophthalmology review.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Serious Ocular Pathology",
                "section_type": "history",
                "questions": [
                    {"id": "ac_eye_pain", "type": "toggle", "label": "Eye Pain? (Not just itch/irritation)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Significant eye pain = ?keratitis, uveitis, acute glaucoma. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "ac_photophobia", "type": "toggle", "label": "Photophobia? (Light sensitivity)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Photophobia = ?keratitis, uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "ac_foreign_body", "type": "toggle", "label": "Foreign Body Sensation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Foreign body sensation = ?corneal foreign body/abrasion. Evert lids + fluorescein stain.", "red_flag_negative": ""},
                    {"id": "ac_purulent_discharge", "type": "toggle", "label": "Purulent / Crusty Discharge?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Purulent discharge = bacterial conjunctivitis. Watery discharge = allergic/viral.", "red_flag_negative": ""},
                    {"id": "ac_blurring", "type": "toggle", "label": "Blurred Vision / Visual Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual loss = ?keratitis, uveitis, acute glaucoma. Emergency ophthalmology.", "red_flag_negative": ""},
                    {"id": "ac_diplopia", "type": "toggle", "label": "Diplopia (Double Vision)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Diplopia = ?orbital cellulitis, neurological. Urgent assessment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ac_conjunctiva", "type": "single_select", "label": "Conjunctiva", "required": True, "options": ["B/L injection (redness) + chemosis (swelling)", "Unilateral injection", "Cobblestone papillae", "Normal"]},
                    {"id": "ac_cornea", "type": "single_select", "label": "Cornea", "required": True, "options": ["Clear - no opacities", "Corneal opacity - RED FLAG", "Limbal changes", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Corneal opacity/ulcer = urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "ac_fluorescein", "type": "single_select", "label": "Fluorescein Staining", "required": False, "options": ["Negative (no uptake)", "Positive - corneal abrasion", "Positive - dendritic ulcer (HSV) - RED FLAG", "Not performed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Dendritic ulcer = HSV keratitis. NEVER give topical steroids. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "ac_va_right", "type": "text", "label": "Visual Acuity - Right", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "ac_va_left", "type": "text", "label": "Visual Acuity - Left", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "ac_visual_fields", "type": "single_select", "label": "Visual Fields", "required": False, "options": ["Normal", "Reduced - RED FLAG", "Not assessed"]},
                    {"id": "ac_eomi", "type": "single_select", "label": "Eye Movements (CN III, IV, VI)", "required": True, "options": ["Normal (EOMI)", "Abnormal - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Restricted eye movements = ?orbital cellulitis, neurological. Urgent.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Allergic Conjunctivitis (Seasonal / Perennial)",
                    "Viral Conjunctivitis (watery, tender preauricular node)",
                    "Bacterial Conjunctivitis (purulent discharge, crusting)",
                    "Vernal / Atopic Keratoconjunctivitis",
                    "Dry Eye Syndrome",
                    "Blepharitis",
                    "Contact Lens-Associated Conjunctivitis",
                    "Corneal Abrasion / Foreign Body",
                    "Herpes Simplex Keratitis (RED FLAG - dendritic ulcer)",
                    "Anterior Uveitis / Iritis (RED FLAG - pain + photophobia + circumcorneal injection)",
                    "Acute Angle-Closure Glaucoma (RED FLAG - severe pain, mid-dilated fixed pupil, hazy cornea)"
                ],
                "questions": [
                    {"id": "ac_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Allergic conjunctivitis - seasonal", "Allergic conjunctivitis - perennial", "Viral conjunctivitis", "Bacterial conjunctivitis", "Suspected HSV keratitis - REFER URGENTLY", "Suspected uveitis - REFER URGENTLY", "Suspected acute glaucoma - EMERGENCY"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: severe eye pain, photophobia, reduced visual acuity, purulent discharge, or symptoms worsen despite treatment. Do NOT rub eyes (mechanical mast cell degranulation worsens symptoms). Cold compresses provide rapid symptom relief. Artificial tears help dilute allergens. NEVER prescribe topical corticosteroids in primary care (risk of glaucoma, cataracts, or exacerbating undiagnosed HSV keratitis). If contact lens wearer: remove lenses and do not wear until symptoms fully resolved. Consider oral non-sedating antihistamine (Cetirizine/Loratadine) + nasal steroid spray if prominent allergic rhinitis. If severe/recurrent: refer ophthalmology for consideration of topical cyclosporine or immunotherapy.",
                "questions": [
                    {"id": "ac_topical", "type": "single_select", "label": "Topical Treatment", "required": True, "options": ["Sodium Cromoglicate (Opticrom) eye drops QDS", "Olopatadine (Opatanol) eye drops BD", "Lubricating/Artificial tears only", "None - self-care advice only"]},
                    {"id": "ac_oral_antihistamine", "type": "toggle", "label": "Oral Antihistamine Added? (Cetirizine/Loratadine/Fexofenadine)", "required": False},
                    {"id": "ac_nasal_spray", "type": "toggle", "label": "Nasal Steroid Spray Added? (If rhinitis prominent)", "required": False},
                    {"id": "ac_cold_compress", "type": "toggle", "label": "Cold Compresses Advised?", "required": True},
                    {"id": "ac_avoid_rubbing", "type": "toggle", "label": "Avoid Eye Rubbing Advised?", "required": True},
                    {"id": "ac_no_steroids", "type": "toggle", "label": "NO Topical Steroids Warning Given?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Topical corticosteroids should NOT be initiated in primary care for red eye.", "red_flag_negative": ""},
                    {"id": "ac_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1-2 weeks if not improving, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_allergic_conjunctivitis()