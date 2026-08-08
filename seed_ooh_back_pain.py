from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_back_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Back Pain",
        "description": "Rapid out-of-hours assessment of acute back pain. Rule out cauda equina syndrome, AAA, spinal fracture, and infection.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "Red Flags — Must Rule Out",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_bp_cauda", "type": "multi_select", "label": "Cauda Equina Symptoms", "required": True, "options": ["Saddle anaesthesia / perineal numbness", "New urinary retention / incontinence", "Faecal incontinence", "Bilateral sciatica / leg weakness", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Cauda Equina = SPINAL EMERGENCY. Same-day neurosurgery referral. MRI within hours.", "red_flag_negative": "", "output_phrase": "Cauda equina: {value}"},
                    {"id": "ooh_bp_aaa", "type": "toggle", "label": "AAA? (age >50, pulsatile mass, hypotension, tearing pain)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Ruptured AAA = EMERGENCY. Call 999.", "red_flag_negative": "", "output_phrase": "?AAA: {value}"},
                    {"id": "ooh_bp_infection", "type": "toggle", "label": "Fever + IVDU + Recent Surgery? (?spinal infection/abscess)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Spinal infection = EMERGENCY. Same-day admission for IV antibiotics + MRI.", "red_flag_negative": "", "output_phrase": "?Infection: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Cauda Equina Syndrome", "Ruptured AAA", "Spinal Epidural Abscess", "Vertebral Fracture", "Renal Colic", "Pyelonephritis", "Mechanical Back Pain", "Sciatica"],
                "questions": [
                    {"id": "ooh_bp_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Cauda Equina — emergency neurosurgery", "?AAA — 999", "?Spinal infection — admit", "Musculoskeletal — safe for home", "Renal colic — manage"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Cauda equina: Emergency neurosurgery referral. Do not delay for imaging in primary care — refer directly. AAA: Call 999. If mechanical back pain: Analgesia (Paracetamol + NSAIDs + codeine if severe). Safety-net: Return immediately if saddle anaesthesia, incontinence, bilateral leg weakness, or unable to pass urine.",
                "questions": [
                    {"id": "ooh_bp_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 ambulance", "Emergency neurosurgery referral", "Medical admission", "Home with analgesia + safety-net"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_bp_safety_net", "type": "toggle", "label": "Cauda Equina Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_bp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Neurosurgery referral made. GP follow-up post-discharge.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_back_pain()