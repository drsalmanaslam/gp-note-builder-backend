from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_hip_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Hip Pain",
        "description": "Rapid out-of-hours assessment of acute hip pain. Rule out fracture, septic arthritis, and vascular compromise.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_hp_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute — after fall/trauma", "Acute — spontaneous (pathological #)", "Gradual — days/weeks", "Unable to weight bear since onset"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to weight bear = ?fracture. Urgent X-ray + orthopaedic referral.", "red_flag_negative": "", "output_phrase": "Onset: {value}"},
                    {"id": "ooh_hp_trauma", "type": "single_select", "label": "Trauma", "required": True, "options": ["Fall from standing height", "High-energy trauma (RTA, fall >1m)", "No trauma — spontaneous", "Minor twist/trip"], "output_phrase": "Trauma: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_hp_septic", "type": "toggle", "label": "Fever + Red/Hot Joint + Unable to Move? (?septic arthritis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Septic arthritis = ORTHOPAEDIC EMERGENCY. Same-day admission for aspiration + IV antibiotics.", "red_flag_negative": "", "output_phrase": "?Septic: {value}"},
                    {"id": "ooh_hp_neurovascular", "type": "toggle", "label": "Pale/Cold Limb + Absent Pulses? (?vascular compromise)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Vascular compromise = EMERGENCY. Same-day vascular/orthopaedic referral.", "red_flag_negative": "", "output_phrase": "Vascular: {value}"},
                    {"id": "ooh_hp_shortened", "type": "toggle", "label": "Leg Shortened + Externally Rotated? (?NOF fracture)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Shortened + externally rotated = ?NOF fracture. Urgent X-ray + orthopaedic admission.", "red_flag_negative": "", "output_phrase": "Deformity: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["NOF Fracture", "Intertrochanteric Fracture", "Septic Arthritis", "Trochanteric Bursitis", "Osteoarthritis Flare", "Referred from Lumbar Spine", "Avascular Necrosis"],
                "questions": [
                    {"id": "ooh_hp_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?NOF fracture — admit orthopaedics", "?Septic arthritis — emergency admission", "Bursitis — manage in community", "OA flare — analgesia + safety-net", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Fracture suspected: NBM, analgesia, urgent X-ray + orthopaedic referral. Septic arthritis: Emergency admission. Bursitis: NSAIDs + rest. Safety-net: Return immediately if unable to weight bear, fever, redness, or worsening pain.",
                "questions": [
                    {"id": "ooh_hp_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["Admit orthopaedics", "999 ambulance", "Home with analgesia + safety-net", "Urgent X-ray + review"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_hp_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_hp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Admitted under orthopaedics. GP to follow up post-discharge.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_hip_pain()