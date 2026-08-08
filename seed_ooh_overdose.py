from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_overdose():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Overdose / Poisoning",
        "description": "Rapid out-of-hours assessment of overdose and poisoning. Triage severity, identify agent, and guide emergency management including Toxbase consultation.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_od_agent", "type": "text", "label": "Agent(s) Taken + Dose", "required": True, "placeholder": "e.g., Paracetamol 20 x 500mg, alcohol", "is_red_flag": True, "red_flag_positive": "RED FLAG: Paracetamol >75mg/kg, tricyclics, opioids, or multiple agents = emergency. Check Toxbase.", "red_flag_negative": "", "output_phrase": "Agent: {value}"},
                    {"id": "ooh_od_time", "type": "text", "label": "Time of Ingestion", "required": True, "placeholder": "e.g., 2 hours ago", "output_phrase": "Time: {value}"},
                    {"id": "ooh_od_intent", "type": "single_select", "label": "Intent", "required": True, "options": ["Deliberate self-harm", "Accidental", "Recreational", "Unknown"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Deliberate self-harm = psychiatric assessment required after medical clearance.", "red_flag_negative": "", "output_phrase": "Intent: {value}"}
                ]
            },
            {
                "title": "Red Flags — Severity Assessment",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_od_gcs", "type": "single_select", "label": "Conscious Level (GCS)", "required": True, "options": ["15 — Alert", "13-14 — Drowsy", "9-12 — Responds to voice", "<9 — Responds to pain / unresponsive"], "is_red_flag": True, "red_flag_positive": "RED FLAG: GCS <15 or deteriorating = EMERGENCY. Call 999. Airway protection needed.", "red_flag_negative": "", "output_phrase": "GCS: {value}"},
                    {"id": "ooh_od_rr", "type": "number", "label": "Respiratory Rate", "required": True, "placeholder": "e.g., 8", "is_red_flag": True, "red_flag_positive": "RED FLAG: RR <12 = ?opioid/benzodiazepine toxicity. Risk of respiratory arrest. Call 999.", "red_flag_negative": "", "output_phrase": "RR: {value}"},
                    {"id": "ooh_od_seizures", "type": "toggle", "label": "Seizures / Arrhythmia / Hypotension?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Seizures/arrhythmia = ?TCA toxicity or severe poisoning. Emergency 999.", "red_flag_negative": "", "output_phrase": "Seizures/arrhythmia: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Paracetamol Overdose", "Opioid Toxicity", "Benzodiazepine Toxicity", "Tricyclic Antidepressant Overdose", "SSRI/SNRI Overdose", "Alcohol Intoxication", "Mixed Overdose"],
                "questions": [
                    {"id": "ooh_od_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Serious — emergency 999", "?Paracetamol — needs levels + NAC", "Moderate — admit for monitoring", "Minor — observe + discharge", "Recreational — monitor"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Unconscious/reduced GCS: Call 999. Recovery position. Naloxone if ?opioids. Paracetamol: If >75mg/kg or staggered overdose, admit for levels + NAC. Check Toxbase for specific antidotes. All deliberate self-harm: Requires psychiatric assessment before discharge. Safety-net for carers: Return immediately if drowsiness, vomiting, seizures, or respiratory depression.",
                "questions": [
                    {"id": "ooh_od_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 ambulance", "Direct medical admission", "Admit for monitoring + psych assessment", "Home with safety-net"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_od_toxbase", "type": "toggle", "label": "Toxbase Checked?", "required": True, "output_phrase": "Toxbase: {value}"},
                    {"id": "ooh_od_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_od_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Admitted under medics. Psych liaison review.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_overdose()