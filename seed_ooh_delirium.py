from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_delirium():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Acute Confusion / Delirium",
        "description": "Rapid out-of-hours assessment of acute confusion. Rule out sepsis, head injury, metabolic causes, and acute neurology.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_del_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute — hours (delirium)", "Subacute — days", "Chronic — weeks/months (dementia)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute onset confusion = DELIRIUM until proven otherwise. Medical emergency.", "red_flag_negative": "", "output_phrase": "Onset: {value}"},
                    {"id": "ooh_del_cause", "type": "multi_select", "label": "Potential Cause", "required": True, "options": ["?Infection — chest, UTI, skin", "?Head injury / fall", "?Metabolic — glucose, sodium, calcium", "?Drugs — new medication, opioids, anticholinergics", "?Alcohol withdrawal", "?Hypoxia", "?Neurological — stroke, seizure", "Unknown"], "output_phrase": "Cause: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_del_sepsis", "type": "toggle", "label": "Fever / Hypotension / Tachycardia? (?sepsis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Sepsis = EMERGENCY. Call 999. IV antibiotics within 1 hour.", "red_flag_negative": "", "output_phrase": "?Sepsis: {value}"},
                    {"id": "ooh_del_head_injury", "type": "toggle", "label": "Head Injury / On Anticoagulants? (?intracranial bleed)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Intracranial bleed = EMERGENCY. Call 999. Urgent CT head.", "red_flag_negative": "", "output_phrase": "?Head injury: {value}"},
                    {"id": "ooh_del_hypoglycaemia", "type": "toggle", "label": "Known Diabetes? Check Capillary Glucose", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypoglycaemia = treat immediately. Glucogel / IV dextrose.", "red_flag_negative": "", "output_phrase": "Glucose: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Sepsis", "Intracranial Haemorrhage", "Hypoglycaemia", "Alcohol Withdrawal / Wernicke's", "Opioid / Drug Toxicity", "Post-Ictal State", "Stroke", "Metabolic Derangement"],
                "questions": [
                    {"id": "ooh_del_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Sepsis — admit", "?Intracranial bleed — 999", "?Hypoglycaemia — treat", "?Alcohol withdrawal — admit", "?Metabolic — admit for workup", "Mild — community management"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If sepsis/bleed/hypoglycaemia: Emergency admission. If alcohol withdrawal: Consider Chlordiazepoxide. Thiamine 100mg IM/IV if ?Wernicke's. If safe for home with carers: Safety-net. Return if worsening confusion, fever, reduced consciousness.",
                "questions": [
                    {"id": "ooh_del_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 ambulance", "Direct medical admission", "Home with safety-net + GP follow-up"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_del_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_del_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Admitted. GP to review post-discharge.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_delirium()