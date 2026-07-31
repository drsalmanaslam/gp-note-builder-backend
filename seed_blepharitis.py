from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_blepharitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    t = {
        "title": "Blepharitis",
        "description": "Focused assessment for blepharitis and meibomian gland dysfunction covering lid hygiene routine, complications, and management escalation.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "bleph_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Sore, gritty, dry eyes with crusting at eyelash roots for months"},
                    {"id": "bleph_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 48"},
                    {"id": "bleph_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., Several months"},
                    {"id": "bleph_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Soreness", "Grittiness / foreign body sensation", "Dry itchy eyes", "Flaking/crusting at lash roots", "Eyelids stuck together on waking", "Burning", "Watery eyes", "Red eyes"]},
                    {"id": "bleph_previous", "type": "multi_select", "label": "Previous Episodes / History", "required": False, "options": ["Stye", "Chalazion", "Previous blepharitis", "None"]},
                    {"id": "bleph_side", "type": "single_select", "label": "Affected Eye(s)", "required": True, "options": ["Bilateral symmetrical", "Right more than left", "Left more than right"]}
                ]
            },
            {
                "title": "RED FLAGS & Dermatological",
                "section_type": "history",
                "questions": [
                    {"id": "bleph_eye_pain", "type": "toggle", "label": "Eye Pain? (Not just soreness/grittiness)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Significant eye pain = ?keratitis, uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "bleph_photophobia", "type": "toggle", "label": "Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Photophobia = ?keratitis, uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "bleph_unilateral_redness", "type": "toggle", "label": "Severe Unilateral Redness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral severe redness = ?orbital cellulitis, uveitis. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "bleph_visual_loss", "type": "toggle", "label": "Blurred Vision / Visual Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual loss = ?keratitis, uveitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "bleph_eczema", "type": "toggle", "label": "Eyelid Eczema / Dermatitis?", "required": False},
                    {"id": "bleph_psoriasis", "type": "toggle", "label": "Psoriasis?", "required": False},
                    {"id": "bleph_seb_derm", "type": "toggle", "label": "Seborrhoeic Dermatitis?", "required": False},
                    {"id": "bleph_rosacea", "type": "toggle", "label": "Rosacea? (Posterior MGD association)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "bleph_lid_margins", "type": "single_select", "label": "Eyelid Margins", "required": True, "options": ["B/L scaly, crusty, erythematous margins", "Yellow plugs on meibomian glands", "Telangiectasia", "Ulceration - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lid ulceration = ?BCC/SCC. Urgent ophthalmology/dermatology.", "red_flag_negative": ""},
                    {"id": "bleph_conjunctiva", "type": "single_select", "label": "Conjunctiva", "required": True, "options": ["Mild injection", "Significant injection", "Normal"]},
                    {"id": "bleph_chalazion", "type": "toggle", "label": "Active Chalazion?", "required": False},
                    {"id": "bleph_trichiasis", "type": "toggle", "label": "Trichiasis? (Misdirected lashes rubbing cornea)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Trichiasis = corneal abrasion risk. Needs epilation or ophthalmology referral.", "red_flag_negative": ""},
                    {"id": "bleph_madarosis", "type": "toggle", "label": "Madarosis? (Loss of eyelashes)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Madarosis = ?SCC, chronic blepharitis. Ophthalmology referral.", "red_flag_negative": ""},
                    {"id": "bleph_cornea", "type": "single_select", "label": "Cornea", "required": True, "options": ["Clear", "Punctate erosions", "Opacities - RED FLAG", "Not assessed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Anterior Blepharitis (Staphylococcal / Seborrhoeic)",
                    "Posterior Blepharitis / Meibomian Gland Dysfunction (MGD)",
                    "Mixed Anterior + Posterior Blepharitis",
                    "Dry Eye Syndrome (often co-exists)",
                    "Chalazion / Stye",
                    "Rosacea-Associated Blepharitis",
                    "Eyelid Eczema / Contact Dermatitis",
                    "Ocular Rosacea",
                    "Trichiasis",
                    "BCC / SCC of Eyelid (RED FLAG - ulceration, madarosis)"
                ],
                "questions": [
                    {"id": "bleph_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Anterior blepharitis", "Posterior blepharitis / MGD", "Mixed anterior + posterior", "Blepharitis + chalazion", "Rosacea-associated blepharitis"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: severe eye pain, worsening redness, photophobia, reduced vision, or new eyelid ulceration develops. Blepharitis is a chronic condition - goal is long-term control, not cure. Lid hygiene must continue indefinitely even when symptoms improve. If anterior staphylococcal blepharitis severe/unresponsive: Chloramphenicol 1% ointment to lid margins BD for 4 weeks. If refractory posterior MGD/rosacea: consider oral Doxycycline 50-100mg OD for 4-12 weeks (off-label). Avoid eye makeup (especially eyeliner on inner lid margin) during flares. Replace eye makeup every 3 months to reduce bacterial load.",
                "questions": [
                    {"id": "bleph_warm_compress", "type": "toggle", "label": "Warm Compresses Advised? (5-10 mins daily, e.g., Optase lid mask)", "required": True},
                    {"id": "bleph_lid_scrub", "type": "toggle", "label": "Lid Scrub/Cleaning Advised? (Blephaclean / Optase wipes / dilute baby shampoo)", "required": True},
                    {"id": "bleph_lid_massage", "type": "toggle", "label": "Lid Massage Advised? (Express meibomian glands after compress)", "required": True},
                    {"id": "bleph_artificial_tears", "type": "single_select", "label": "Artificial Tears / Lubrication", "required": False, "options": ["None", "Hyloforte TDS", "Thealoz Duo TDS", "Optase dry eye spray", "Other preservative-free drops"]},
                    {"id": "bleph_vaseline", "type": "toggle", "label": "Vaseline to Lash Roots? (If severe crusting/dry skin)", "required": False},
                    {"id": "bleph_antibiotic_ointment", "type": "toggle", "label": "Chloramphenicol 1% Ointment? (Severe anterior staph blepharitis - BD to lid margins for 4 weeks)", "required": False},
                    {"id": "bleph_doxycycline", "type": "toggle", "label": "Oral Doxycycline? (Refractory MGD/rosacea - 50-100mg OD 4-12 weeks)", "required": False},
                    {"id": "bleph_nizoral", "type": "toggle", "label": "Nizoral Shampoo? (If co-existing seborrhoeic dermatitis)", "required": False},
                    {"id": "bleph_makeup_advice", "type": "toggle", "label": "Avoid Eye Makeup During Flares Advised?", "required": False},
                    {"id": "bleph_chronic_counselling", "type": "toggle", "label": "Chronic Nature Explained? (Control not cure)", "required": True},
                    {"id": "bleph_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4-6 weeks if not improving, sooner if red flags"}
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
    seed_blepharitis()