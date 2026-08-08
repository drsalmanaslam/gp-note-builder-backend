from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ooh_acute_abdo():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH")
        db.add(category)
        db.commit()

    t = {
        "title": "OOH - Acute Abdominal Pain",
        "description": "Rapid out-of-hours assessment of acute abdominal pain. Rule out surgical emergencies, AAA, and gynaecological causes. Guide to admission vs community management.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "Pain Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_abdo_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden — seconds/minutes", "Rapid — over hours", "Gradual — days"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden onset = ?perforation, AAA, volvulus. Emergency admission.", "red_flag_negative": "", "output_phrase": "Onset: {value}"},
                    {"id": "ooh_abdo_location", "type": "single_select", "label": "Location", "required": True, "options": ["RUQ", "Epigastric", "LUQ", "RLQ — ?appendicitis", "LLQ — ?diverticulitis", "Diffuse / generalised", "Back / flank — ?AAA, renal"], "output_phrase": "Location: {value}"},
                    {"id": "ooh_abdo_severity", "type": "single_select", "label": "Severity (0-10)", "required": True, "options": ["Mild 1-4", "Moderate 5-7", "Severe 8-10", "Worst pain ever"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe/worst ever pain = ?AAA, perforation, mesenteric ischaemia. Emergency admission.", "red_flag_negative": "", "output_phrase": "Severity: {value}"}
                ]
            },
            {
                "title": "Red Flags — Must Rule Out",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_abdo_aaa", "type": "toggle", "label": "AAA Risk? (age >50, pulsatile mass, hypotension, collapse)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Ruptured AAA = EMERGENCY. Call 999. Do not delay for investigations.", "red_flag_negative": "", "output_phrase": "?AAA: {value}"},
                    {"id": "ooh_abdo_peritonitis", "type": "toggle", "label": "Peritonism? (guarding, rebound, rigid abdomen)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Peritonism = surgical emergency. Same-day surgical admission.", "red_flag_negative": "", "output_phrase": "Peritonism: {value}"},
                    {"id": "ooh_abdo_ectopic", "type": "toggle", "label": "?Ectopic Pregnancy (female of childbearing age, PV bleeding, adnexal mass)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Ectopic = LIFE-THREATENING. Emergency gynaecology admission. Urgent pregnancy test.", "red_flag_negative": "", "output_phrase": "?Ectopic: {value}"},
                    {"id": "ooh_abdo_obstruction", "type": "toggle", "label": "Obstruction? (absolute constipation, vomiting, distension, tinkling bowel sounds)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Obstruction = surgical emergency. NBM, IV fluids, surgical admission.", "red_flag_negative": "", "output_phrase": "?Obstruction: {value}"}
                ]
            },
            {
                "title": "Vitals & Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_abdo_hr", "type": "number", "label": "Heart Rate", "required": True, "placeholder": "e.g., 110", "is_red_flag": True, "red_flag_positive": "RED FLAG: Tachycardia + abdo pain = ?sepsis, haemorrhage, perforation. Emergency.", "red_flag_negative": "", "output_phrase": "HR: {value}"},
                    {"id": "ooh_abdo_bp", "type": "text", "label": "Blood Pressure", "required": True, "placeholder": "e.g., 90/60", "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypotension + abdo pain = ?AAA, perforation, pancreatitis. Emergency admission.", "red_flag_negative": "", "output_phrase": "BP: {value}"},
                    {"id": "ooh_abdo_temp", "type": "number", "label": "Temperature", "required": True, "placeholder": "e.g., 38.5", "output_phrase": "Temp: {value}°C"}
                ]
            },
            {
                "title": "Assessment & Disposition",
                "section_type": "assessment",
                "differentials": ["Ruptured AAA", "Appendicitis", "Bowel Obstruction", "Perforated Viscus", "Acute Pancreatitis", "Ectopic Pregnancy", "Diverticulitis", "Biliary Colic / Cholecystitis", "Renal Colic", "Non-specific Abdominal Pain"],
                "questions": [
                    {"id": "ooh_abdo_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Surgical emergency — admit", "?AAA — 999", "?Ectopic — emergency gynae", "?Obstruction — admit", "Non-specific — likely safe for home with safety-net", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If surgical emergency/AAA/ectopic: Call 999 or direct admission. NBM until surgical review. IV access, fluids if hypotensive. Analgesia: Paracetamol 1g PO/IV. Avoid NSAIDs if ?surgical. If safe for home: Clear safety-net — return immediately if pain worsens, becomes constant, vomiting, collapse, or new symptoms. Advise to attend ED if concerned overnight. Arrange GP follow-up within 24-48h.",
                "questions": [
                    {"id": "ooh_abdo_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 ambulance — emergency", "Direct admission — surgical/medical", "Home with safety-net + GP follow-up", "Refer to on-call surgical team"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_abdo_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if worsening/collapse/vomiting)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_abdo_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., GP review in 24h. Admit if deteriorating.", "output_phrase": "Follow-up: {value}"}
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
    seed_ooh_acute_abdo()