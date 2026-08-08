from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_knee_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Knee Pain",
        "description": "Rapid out-of-hours assessment of acute knee pain. Rule out septic arthritis, fracture, and locked knee.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_kp_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden — during activity (ligament/meniscus)", "After trauma/fall", "Gradual — over days", "Woke up with it"], "output_phrase": "Onset: {value}"},
                    {"id": "ooh_kp_swelling", "type": "single_select", "label": "Swelling Onset", "required": True, "options": ["Immediate — within minutes (haemarthrosis — ?ACL/fracture)", "Hours later (effusion)", "No swelling"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Immediate swelling = haemarthrosis. ?ACL tear or fracture. Urgent orthopaedic assessment.", "red_flag_negative": "", "output_phrase": "Swelling: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_kp_septic", "type": "toggle", "label": "Fever + Red/Hot/Warm Joint? (?septic arthritis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Septic arthritis = ORTHOPAEDIC EMERGENCY. Same-day aspiration + IV antibiotics.", "red_flag_negative": "", "output_phrase": "?Septic: {value}"},
                    {"id": "ooh_kp_locked", "type": "toggle", "label": "Locked Knee? (cannot fully extend — ?meniscal tear)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Locked knee = ?bucket handle meniscal tear. Urgent orthopaedic referral.", "red_flag_negative": "", "output_phrase": "Locked: {value}"},
                    {"id": "ooh_kp_deformity", "type": "toggle", "label": "Gross Deformity / Unable to Weight Bear? (?fracture/dislocation)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Deformity + unable to WB = ?fracture or dislocation. Urgent X-ray + orthopaedics.", "red_flag_negative": "", "output_phrase": "Deformity: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Septic Arthritis", "Anterior Cruciate Ligament Tear", "Meniscal Tear (locked knee)", "Patellar Dislocation", "Fracture (tibial plateau, patella)", "Gout / Pseudogout", "Bursitis", "Ligament Sprain"],
                "questions": [
                    {"id": "ooh_kp_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Septic arthritis — emergency admission", "?Fracture — X-ray + orthopaedics", "?Locked knee — urgent orthopaedics", "?ACL tear — refer orthopaedics", "Sprain/bursitis — manage in community", "Gout — treat + safety-net"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Septic arthritis: Emergency admission. Fracture/dislocation: NBM, analgesia, X-ray + orthopaedics. Locked knee: Urgent orthopaedic referral. Sprain: RICE, analgesia, weight bear as tolerated. Safety-net: Return if increasing pain, swelling, fever, redness, or unable to weight bear.",
                "questions": [
                    {"id": "ooh_kp_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["Emergency admission (septic)", "Urgent orthopaedic referral", "X-ray + review", "Home with RICE + safety-net"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_kp_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_kp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Orthopaedic referral made. GP review in 1 week.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_knee_pain()