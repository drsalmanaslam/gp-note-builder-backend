from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_red_eye():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Red Eye",
        "description": "Rapid out-of-hours assessment of acute red eye. Rule out acute glaucoma, keratitis, and orbital cellulitis.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_re_pain", "type": "single_select", "label": "Pain", "required": True, "options": ["Severe — deep, boring (glaucoma, scleritis)", "Moderate — gritty (keratitis)", "Mild — itchy (conjunctivitis)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe deep pain + nausea/vomiting = ?acute angle-closure glaucoma. Same-day ophthalmology.", "red_flag_negative": "", "output_phrase": "Pain: {value}"},
                    {"id": "ooh_re_vision", "type": "toggle", "label": "Reduced Vision / Halos Around Lights?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced vision + halos = ?acute glaucoma. Emergency ophthalmology.", "red_flag_negative": "", "output_phrase": "Vision loss: {value}"},
                    {"id": "ooh_re_photophobia", "type": "toggle", "label": "Severe Photophobia? (?keratitis, iritis)", "required": True, "output_phrase": "Photophobia: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_re_hazy", "type": "toggle", "label": "Hazy Cornea + Mid-Dilated Fixed Pupil? (glaucoma)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hazy cornea + fixed pupil = acute glaucoma. Emergency. Same-day ophthalmology for pilocarpine/acetazolamide.", "red_flag_negative": "", "output_phrase": "Glaucoma signs: {value}"},
                    {"id": "ooh_re_orbital", "type": "toggle", "label": "Proptosis + Reduced Eye Movements + Fever? (?orbital cellulitis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Orbital cellulitis = EMERGENCY. Same-day admission for IV antibiotics.", "red_flag_negative": "", "output_phrase": "?Orbital cellulitis: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Acute Angle-Closure Glaucoma", "Orbital Cellulitis", "Bacterial Keratitis (contact lens wearers)", "Scleritis", "Anterior Uveitis / Iritis", "Conjunctivitis", "Subconjunctival Haemorrhage"],
                "questions": [
                    {"id": "ooh_re_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Acute glaucoma — emergency ophthalmology", "?Orbital cellulitis — admit", "?Keratitis — urgent ophthalmology", "Conjunctivitis — topical antibiotics", "Subconjunctival haemorrhage — reassure"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Glaucoma: Same-day ophthalmology. Orbital cellulitis: Emergency admission IV antibiotics. Keratitis: Urgent ophthalmology (especially contact lens wearers). Conjunctivitis: Chloramphenicol drops QDS. Safety-net: Return if pain worsens, vision deteriorates, or new symptoms develop.",
                "questions": [
                    {"id": "ooh_re_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["Emergency ophthalmology", "Medical admission", "Urgent ophthalmology (within 24h)", "Home with treatment"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_re_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_re_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Ophthalmology review. GP follow-up post-treatment.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]; existing.content = t["content"]; existing.category = t["category"]; existing.is_public = t["is_public"]; existing.updated_at = datetime.now(timezone.utc)
        db.commit(); print(f"Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t); db.commit(); print(f"Created: {t['title']}")
    db.close()

if __name__ == "__main__":
    seed_ooh_red_eye()