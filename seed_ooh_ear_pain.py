from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_ear_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Ear Pain",
        "description": "Rapid out-of-hours assessment of acute ear pain. Rule out mastoiditis, malignant otitis externa, and complications of AOM.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_ep_location", "type": "single_select", "label": "Pain Location", "required": True, "options": ["Deep ear pain (AOM)", "Pinna / ear canal (otitis externa)", "Behind the ear — mastoid area", "Referred — dental/TMJ/throat"], "output_phrase": "Location: {value}"},
                    {"id": "ooh_ep_discharge", "type": "single_select", "label": "Discharge", "required": True, "options": ["None", "Purulent — yellow/green (AOM with perf)", "Blood-stained", "Clear — ?CSF (head injury)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Clear discharge after head injury = ?CSF leak. Emergency CT + neurosurgery.", "red_flag_negative": "", "output_phrase": "Discharge: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_ep_mastoiditis", "type": "toggle", "label": "Swelling/Redness Behind Ear + Protruding Pinna? (?mastoiditis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Mastoiditis = EMERGENCY. Same-day ENT admission for IV antibiotics.", "red_flag_negative": "", "output_phrase": "?Mastoiditis: {value}"},
                    {"id": "ooh_ep_malignant_oe", "type": "toggle", "label": "Severe Pain + Granulation Tissue in Canal + Diabetic/Immunocompromised? (?malignant OE)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Malignant otitis externa = EMERGENCY. Same-day ENT for IV antibiotics + imaging.", "red_flag_negative": "", "output_phrase": "?Malignant OE: {value}"},
                    {"id": "ooh_ep_facial", "type": "toggle", "label": "Facial Weakness / Dizziness? (?complicated AOM)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Facial palsy + ear pain = ?complicated AOM. Emergency ENT referral.", "red_flag_negative": "", "output_phrase": "Facial nerve: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Acute Otitis Media", "Otitis Media with Perforation", "Otitis Externa", "Mastoiditis", "Malignant Otitis Externa", "Foreign Body", "Dental / TMJ Referred Pain"],
                "questions": [
                    {"id": "ooh_ep_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["AOM — antibiotics + analgesia", "Otitis externa — topical antibiotics", "?Mastoiditis — emergency ENT", "?Malignant OE — emergency ENT", "Dental/TMJ — treat accordingly"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "AOM: Amoxicillin 500mg TDS 5 days (if >2y and systemically well, consider watchful waiting). Analgesia: Paracetamol + Ibuprofen. Otitis externa: Topical antibiotic/steroid drops (Otomize or Sofradex). Mastoiditis/malignant OE: Emergency ENT admission. Safety-net: Return if swelling behind ear, facial weakness, worsening pain, or high fever.",
                "questions": [
                    {"id": "ooh_ep_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["Emergency ENT admission", "Home with oral/topical antibiotics", "Home with analgesia + safety-net", "Dental referral"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_ep_antibiotics", "type": "text", "label": "Antibiotics Prescribed", "required": False, "placeholder": "e.g., Amoxicillin 500mg TDS 5 days", "output_phrase": "Antibiotics: {value}"},
                    {"id": "ooh_ep_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_ep_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., GP review in 48h if not improving.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_ear_pain()