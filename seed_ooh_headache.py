from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_headache():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Headache",
        "description": "Rapid out-of-hours assessment of acute headache. Rule out SAH, meningitis, GCA, and carbon monoxide poisoning.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_ha_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Thunderclap — instantaneous peak (SAH)", "Rapid — hours", "Gradual — days", "Woke up with it"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Thunderclap headache = ?SAH. Emergency CT + LP. Call 999 or direct admission.", "red_flag_negative": "", "output_phrase": "Onset: {value}"},
                    {"id": "ooh_ha_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Worst ever — unlike any before", "Severe", "Moderate", "Mild"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Worst ever headache = ?SAH/meningitis. Emergency.", "red_flag_negative": "", "output_phrase": "Severity: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_ha_meningitis", "type": "toggle", "label": "Fever + Neck Stiffness + Photophobia? (?meningitis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Meningitis = EMERGENCY. IM Benzylpenicillin if meningococcal suspected. Call 999.", "red_flag_negative": "", "output_phrase": "?Meningitis: {value}"},
                    {"id": "ooh_ha_gca", "type": "toggle", "label": "Age >50 + Scalp Tenderness + Jaw Claudication? (?GCA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?GCA = risk of blindness. Start Prednisolone 60mg immediately. Same-day ophthalmology.", "red_flag_negative": "", "output_phrase": "?GCA: {value}"},
                    {"id": "ooh_ha_neuro", "type": "toggle", "label": "New Neurological Deficit? (weakness, speech, visual field)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Focal neurology = ?stroke, SOL, bleed. Emergency CT.", "red_flag_negative": "", "output_phrase": "Neuro deficit: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Subarachnoid Haemorrhage", "Meningitis / Encephalitis", "Giant Cell Arteritis", "Acute Angle-Closure Glaucoma", "Carbon Monoxide Poisoning", "Migraine", "Cluster Headache"],
                "questions": [
                    {"id": "ooh_ha_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?SAH — 999 / ED", "?Meningitis — 999", "?GCA — start steroids + refer", "Migraine — treat in community", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If ?SAH/meningitis: Call 999. If ?GCA: Prednisolone 60mg PO immediately. If migraine: Sumatriptan 50mg PO or 6mg SC + Paracetamol 1g. If safe for home: Return if headache becomes worst ever, neck stiffness, fever, vision loss, or neurological symptoms.",
                "questions": [
                    {"id": "ooh_ha_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 ambulance", "Direct medical admission", "Start steroids + refer (GCA)", "Home with treatment + safety-net"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_ha_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_ha_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., GP review in 24h. ED if deteriorates.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_headache()