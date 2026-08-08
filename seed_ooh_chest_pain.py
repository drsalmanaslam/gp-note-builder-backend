from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_chest_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Chest Pain",
        "description": "Rapid out-of-hours assessment of acute chest pain. Rule out MI, PE, aortic dissection, and pneumothorax. Guide to emergency admission vs community management.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "Pain Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_cp_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden — seconds (dissection/PE)", "Rapid — minutes (MI)", "Gradual — hours"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden onset = ?aortic dissection, PE, pneumothorax. Emergency.", "red_flag_negative": "", "output_phrase": "Onset: {value}"},
                    {"id": "ooh_cp_character", "type": "single_select", "label": "Character", "required": True, "options": ["Crushing / heavy / pressure (cardiac)", "Sharp / stabbing / pleuritic (PE, pneumothorax)", "Tearing / ripping (dissection)", "Burning (GORD)", "Atypical"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Tearing pain radiating to back = ?aortic dissection. Emergency 999.", "red_flag_negative": "", "output_phrase": "Character: {value}"},
                    {"id": "ooh_cp_radiation", "type": "multi_select", "label": "Radiation", "required": False, "options": ["Left arm", "Right arm", "Jaw / neck", "Back (between shoulder blades — ?dissection)", "Epigastric", "None"], "output_phrase": "Radiation: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_cp_dissection", "type": "toggle", "label": "Tearing Pain + BP Differential / Neuro Symptoms? (?aortic dissection)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Aortic dissection = EMERGENCY. Call 999 immediately.", "red_flag_negative": "", "output_phrase": "?Dissection: {value}"},
                    {"id": "ooh_cp_pe", "type": "toggle", "label": "Sudden SOB + Pleuritic Pain + Haemoptysis? (?PE)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Massive PE = EMERGENCY. Call 999 if hypotensive or severely hypoxic.", "red_flag_negative": "", "output_phrase": "?PE: {value}"},
                    {"id": "ooh_cp_mi", "type": "toggle", "label": "Ongoing Cardiac Pain >15 min + Diaphoresis / Nausea? (?MI)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?ACS = EMERGENCY. Call 999. Aspirin 300mg. Nitrates if available.", "red_flag_negative": "", "output_phrase": "?MI: {value}"}
                ]
            },
            {
                "title": "Vitals",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_cp_hr", "type": "number", "label": "Heart Rate", "required": True, "placeholder": "e.g., 110", "output_phrase": "HR: {value}"},
                    {"id": "ooh_cp_bp", "type": "text", "label": "Blood Pressure", "required": True, "placeholder": "e.g., 140/90", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP differential >20mmHg between arms = ?dissection. Hypotension = ?massive PE/MI.", "red_flag_negative": "", "output_phrase": "BP: {value}"},
                    {"id": "ooh_cp_sats", "type": "number", "label": "O2 Saturations (%)", "required": True, "placeholder": "e.g., 92", "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 <92% = severe hypoxia. O2 + emergency admission.", "red_flag_negative": "", "output_phrase": "SpO2: {value}%"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Acute Coronary Syndrome / MI", "Aortic Dissection", "Pulmonary Embolism", "Tension Pneumothorax", "Pericarditis", "GORD / Oesophageal Spasm", "Musculoskeletal", "Panic Attack"],
                "questions": [
                    {"id": "ooh_cp_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?ACS/MI — 999", "?Aortic Dissection — 999", "?PE — 999 if massive, admit if stable", "?Pneumothorax — admit", "Non-cardiac — safe for home", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If ?ACS: Call 999. Aspirin 300mg chewed. GTN spray if available and not hypotensive. Oxygen if SpO2 <94%. If ?Dissection: Call 999. Analgesia. Control BP. If ?Massive PE: Call 999. Oxygen. If non-cardiac and safe for home: Clear safety-net. Return immediately if pain persists >15min, becomes severe, SOB, collapse. GP follow-up in 24-48h.",
                "questions": [
                    {"id": "ooh_cp_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 ambulance", "Direct medical admission", "Home with safety-net"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_cp_aspirin", "type": "toggle", "label": "Aspirin 300mg Given? (if ?ACS)", "required": False, "output_phrase": "Aspirin: {value}"},
                    {"id": "ooh_cp_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_cp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Admitted under medics. GP to follow up post-discharge.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_chest_pain()