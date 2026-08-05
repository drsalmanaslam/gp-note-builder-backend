from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_palliative():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Geriatrics").first()
    if not category:
        category = Category(name="Geriatrics")
        db.add(category)
        db.commit()

    t = {
        "title": "Palliative & End-of-Life Care",
        "description": "Structured palliative care assessment covering symptom control, advance care planning, preferred place of care, medications review, and MDT coordination.",
        "category": "Geriatrics",
        "content": {"sections": [
            {
                "title": "Current Status",
                "section_type": "history",
                "questions": [
                    {"id": "pal_diagnosis", "type": "text", "label": "Primary Life-Limiting Diagnosis", "required": True, "placeholder": "e.g., Metastatic lung cancer", "output_phrase": "Diagnosis: {value}"},
                    {"id": "pal_performance", "type": "single_select", "label": "Performance Status (ECOG / AKPS)", "required": True, "options": ["0-1 — Fully active / restricted but ambulatory", "2 — Up >50% of day, limited self-care", "3 — In bed/chair >50%, limited self-care", "4 — Completely bedbound, fully dependent"], "output_phrase": "Performance: {value}"},
                    {"id": "pal_trajectory", "type": "single_select", "label": "Disease Trajectory", "required": True, "options": ["Stable — months", "Gradual decline — weeks-months", "Rapid decline — days-weeks", "Actively dying — hours-days"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Rapid decline or actively dying = urgent MDT review. Ensure anticipatory medications prescribed. Preferred place of death discussed.", "red_flag_negative": "", "output_phrase": "Trajectory: {value}"}
                ]
            },
            {
                "title": "Symptom Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "pal_pain", "type": "single_select", "label": "Pain", "required": True, "options": ["Well controlled", "Moderate — breakthrough pain", "Severe — uncontrolled", "No pain"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Uncontrolled pain = urgent palliative care review. Follow WHO ladder. Consider syringe driver if unable to take oral.", "red_flag_negative": "", "output_phrase": "Pain: {value}"},
                    {"id": "pal_nausea", "type": "toggle", "label": "Nausea / Vomiting?", "required": True, "output_phrase": "Nausea: {value}"},
                    {"id": "pal_sob", "type": "toggle", "label": "Breathlessness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Breathlessness = consider opioids (morphine 2.5mg SC PRN), fan therapy, benzodiazepines for anxiety. Palliative care input.", "red_flag_negative": "", "output_phrase": "Breathlessness: {value}"},
                    {"id": "pal_agitation", "type": "toggle", "label": "Agitation / Terminal Restlessness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Terminal agitation = Midazolam SC. Consider reversible causes (urinary retention, pain, opioid toxicity).", "red_flag_negative": "", "output_phrase": "Agitation: {value}"},
                    {"id": "pal_secretions", "type": "toggle", "label": "Respiratory Secretions / Death Rattle?", "required": False, "output_phrase": "Secretions: {value}"}
                ]
            },
            {
                "title": "Advance Care Planning",
                "section_type": "history",
                "questions": [
                    {"id": "pal_ppc", "type": "single_select", "label": "Preferred Place of Care / Death", "required": True, "options": ["Home", "Hospice", "Nursing home", "Hospital", "Not discussed yet"], "output_phrase": "Preferred place: {value}"},
                    {"id": "pal_dnar", "type": "toggle", "label": "DNACPR / Treatment Escalation Plan in Place?", "required": True, "output_phrase": "DNACPR/TEP: {value}"},
                    {"id": "pal_lpa", "type": "toggle", "label": "Lasting Power of Attorney / Advance Directive?", "required": False, "output_phrase": "LPA: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Anticipatory medications (just-in-case box): Morphine SC for pain/breathlessness, Midazolam SC for agitation/seizures, Levomepromazine or Haloperidol SC for nausea, Hyoscine butylbromide SC for secretions. Syringe driver if unable to take oral. Regular review of medications — stop non-essentials (statins, antihypertensives, vitamins). MDT coordination: Community palliative care team, public health nurse, GP. Family/carer support — bereavement counselling. Safety-net: Provide 24/7 contact numbers (palliative care hotline, out-of-hours GP). If crisis at home: who to call, when to admit to hospice/hospital.",
                "questions": [
                    {"id": "pal_anticipatory", "type": "toggle", "label": "Anticipatory Medications Prescribed? (just-in-case box)", "required": True, "output_phrase": "Anticipatory meds: {value}"},
                    {"id": "pal_deprescribing", "type": "toggle", "label": "Non-Essential Medications Stopped? (statins, antihypertensives, etc.)", "required": False, "output_phrase": "Deprescribed: {value}"},
                    {"id": "pal_mdt", "type": "toggle", "label": "Palliative Care Team / PHN Referral Made?", "required": True, "output_phrase": "MDT referral: {value}"},
                    {"id": "pal_carer_support", "type": "toggle", "label": "Family/Carer Support + Bereavement Info Given?", "required": True, "output_phrase": "Carer support: {value}"},
                    {"id": "pal_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Daily phone check. Palliative care team visiting. Review medications weekly.", "output_phrase": "Follow-up: {value}"}
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
    seed_palliative()