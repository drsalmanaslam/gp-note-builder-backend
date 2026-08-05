from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_stye_chalazion():
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
        "title": "Stye & Chalazion",
        "description": "Assessment of eyelid lumps. Differentiates stye (acute infection) from chalazion (blocked meibomian gland), management from warm compresses to incision, and red flags for referral.",
        "category": "Eye",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "sc_type", "type": "single_select", "label": "Type of Lesion", "required": True, "options": ["Acute painful lump — pointing at lid margin (external stye)", "Acute painful lump — inside eyelid (internal stye)", "Chronic painless lump (chalazion)", "Recurrent styes/chalazia", "Unsure"], "output_phrase": "Type: {value}"},
                    {"id": "sc_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3 days — painful, red", "output_phrase": "Duration: {value}"},
                    {"id": "sc_recurrent", "type": "toggle", "label": "Recurrent or Multiple? (consider blepharitis, rosacea, diabetes)", "required": True, "output_phrase": "Recurrent: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "sc_preseptal", "type": "toggle", "label": "Eyelid Swelling Beyond the Lump? (preseptal cellulitis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Diffuse eyelid swelling/erythema beyond the stye = preseptal cellulitis. Oral antibiotics (Co-amoxiclav). If orbital signs: admit.", "red_flag_negative": "", "output_phrase": "Preseptal: {value}"},
                    {"id": "sc_orbital", "type": "toggle", "label": "Reduced Eye Movements / Diplopia / Proptosis / Reduced Vision? (?orbital cellulitis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Orbital cellulitis = EMERGENCY. Same-day hospital admission for IV antibiotics. Risk of vision loss and intracranial spread.", "red_flag_negative": "", "output_phrase": "Orbital signs: {value}"},
                    {"id": "sc_bcc", "type": "toggle", "label": "Persistent Ulcerating/Nodular Lesion? (?BCC/SCC — especially if eyelash loss)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Persistent non-healing lesion + madarosis (eyelash loss) = ?BCC. Urgent dermatology/ophthalmology referral.", "red_flag_negative": "", "output_phrase": "?Malignancy: {value}"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "sc_location", "type": "single_select", "label": "Location", "required": True, "options": ["External — lash follicle (stye/hordeolum)", "Internal — meibomian gland (chalazion)", "Upper lid", "Lower lid", "Both lids"], "output_phrase": "Location: {value}"},
                    {"id": "sc_pointing", "type": "toggle", "label": "Pointing / Head of Pus Visible?", "required": False, "output_phrase": "Pointing: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["External Stye (Hordeolum) — acute, painful, pointing at lid margin", "Internal Stye — acute, inside eyelid", "Chalazion — chronic, painless, blocked meibomian gland", "Preseptal Cellulitis — diffuse lid swelling beyond lump", "Orbital Cellulitis — proptosis, diplopia, reduced vision (EMERGENCY)", "BCC — pearly nodule, telangiectasia, madarosis", "Dacryocystitis — swelling at medial canthus"],
                "questions": [
                    {"id": "sc_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Stye (acute) — conservative management", "Chalazion (chronic) — warm compress + observe", "Preseptal Cellulitis — oral antibiotics", "?Orbital Cellulitis — EMERGENCY admission", "?Malignancy — urgent referral"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "STYE (acute): Warm compress 5-10 min QDS — most resolve spontaneously. Epilate the affected lash if pointing. Do NOT squeeze — risk of spreading infection. Topical antibiotic (Chloramphenicol ointment QDS) if secondary infection. CHALAZION: Warm compress + lid massage. Most resolve within weeks-months. If persistent >3 months or large/symptomatic: Refer ophthalmology for incision & curettage or steroid injection. Recurrent: Treat underlying blepharitis (lid hygiene, artificial tears). Check HbA1c if recurrent. Safety-net: Return immediately if swelling spreads beyond eyelid, eye movements reduced, vision changes, or pain severe.",
                "questions": [
                    {"id": "sc_treatment", "type": "single_select", "label": "Treatment", "required": True, "options": ["Warm compress only — self-limiting", "Warm compress + topical antibiotic", "Oral antibiotics (preseptal cellulitis)", "Refer ophthalmology (persistent chalazion / ?malignancy)", "Emergency admission (orbital cellulitis)"], "output_phrase": "Treatment: {value}"},
                    {"id": "sc_antibiotic", "type": "text", "label": "Antibiotic Prescribed", "required": False, "placeholder": "e.g., Chloramphenicol ointment QDS 7 days", "output_phrase": "Antibiotic: {value}"},
                    {"id": "sc_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if swelling spreads / vision change / diplopia)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "sc_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review if not resolved in 2 weeks. Refer if persistent >3 months.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created!")
    db.close()

if __name__ == "__main__":
    seed_stye_chalazion()