from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_dvt():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Suspected DVT",
        "description": "Rapid out-of-hours assessment of suspected DVT. Wells score, same-day pathway, and when to start treatment.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "Wells Score",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_dvt_wells", "type": "single_select", "label": "Wells Score (Pre-Test Probability)", "required": True, "options": ["DVT Likely (Wells ≥2)", "DVT Unlikely (Wells <2)"], "output_phrase": "Wells: {value}"},
                    {"id": "ooh_dvt_symptoms", "type": "multi_select", "label": "Clinical Features", "required": True, "options": ["Calf swelling >3cm vs other leg", "Entire leg swollen", "Pitting oedema", "Collateral superficial veins", "Tenderness along deep veins", "Previous DVT/PE", "Active cancer", "Immobilisation / recent surgery"], "output_phrase": "Features: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_dvt_pe", "type": "toggle", "label": "Chest Pain / SOB / Haemoptysis? (?PE)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?PE = EMERGENCY. Call 999 if hypotensive or severe hypoxia.", "red_flag_negative": "", "output_phrase": "?PE: {value}"},
                    {"id": "ooh_dvt_phlegmasia", "type": "toggle", "label": "Phlegmasia? (massive swelling, cyanosis, severe pain — limb-threatening)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Phlegmasia cerulea dolens = LIMB-THREATENING. Emergency admission.", "red_flag_negative": "", "output_phrase": "Phlegmasia: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["DVT", "PE", "Cellulitis", "Ruptured Baker's Cyst", "Calf Haematoma", "Lymphoedema", "Dependent Oedema"],
                "questions": [
                    {"id": "ooh_dvt_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["DVT Likely — start DOAC + same-day US", "DVT Unlikely — D-dimer + safety-net", "?PE — emergency", "Cellulitis — antibiotics", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "DVT Likely (Wells ≥2): Start Apixaban 10mg BD or Rivaroxaban 15mg BD. Arrange same-day leg ultrasound. DVT Unlikely (Wells <2): D-dimer. If positive, treat as DVT. If negative, consider alternative. Safety-net: Return immediately if chest pain, SOB, haemoptysis, or leg becomes pale/cold/blue.",
                "questions": [
                    {"id": "ooh_dvt_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["Start DOAC + same-day US", "D-dimer + safety-net", "Admit (phlegmasia / ?PE)", "Home with treatment"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_dvt_doac", "type": "text", "label": "DOAC Prescribed", "required": False, "placeholder": "e.g., Apixaban 10mg BD", "output_phrase": "DOAC: {value}"},
                    {"id": "ooh_dvt_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_dvt_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., US tomorrow. GP review with results.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_dvt()