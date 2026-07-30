from app.database import SessionLocal
from app.models import User, Template, Category

def seed_sinusitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Acute Bacterial Sinusitis",
        "description": "Focused assessment for acute sinusitis covering NICE antibiotic guidance (≤10 vs >10 days), red flags for periorbital infection, and symptomatic management.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "sin_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Facial pain and purulent nasal discharge for 5 days"},
                    {"id": "sin_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 5 days (Antibiotics only if >10 days per NICE)"},
                    {"id": "sin_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Frontal sinus tenderness / pain", "Teeth pain (maxillary sinus)", "Purulent nasal discharge", "Pyrexia / fever", "Reduced sense of smell (anosmia)", "None of the above"]},
                    {"id": "sin_facial_swelling", "type": "toggle", "label": "Facial or Periorbital Swelling?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Periorbital swelling = ?periorbital/orbital cellulitis. ESCALATE - urgent ENT/ophthalmology. Do NOT manage in primary care.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "sin_ent_tympanic", "type": "single_select", "label": "Tympanic Membranes", "required": False, "options": ["Normal B/L", "Abnormal"]},
                    {"id": "sin_ent_pharynx", "type": "single_select", "label": "Pharynx", "required": False, "options": ["Normal", "Erythematous"]},
                    {"id": "sin_ent_lymph", "type": "toggle", "label": "Lymphadenopathy?", "required": False},
                    {"id": "sin_ent_coryza", "type": "toggle", "label": "Coryza Present?", "required": False},
                    {"id": "sin_ent_turbinates", "type": "single_select", "label": "Nasal Turbinates", "required": False, "options": ["Normal", "Abnormal / swollen"]},
                    {"id": "sin_sinus_tenderness", "type": "single_select", "label": "Maxillary / Frontal Sinus Tenderness", "required": True, "options": ["Tenderness present", "No tenderness"]},
                    {"id": "sin_resp", "type": "single_select", "label": "Respiratory Examination", "required": False, "options": ["Air entry equal B/L, vesicular BS, no added sounds", "Reduced air entry", "Added sounds present"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Acute Viral Sinusitis (most common - <10 days)",
                    "Acute Bacterial Sinusitis (>10 days or severe)",
                    "Periorbital / Orbital Cellulitis (RED FLAG - facial swelling)",
                    "Dental Infection / Abscess",
                    "Giant Cell Arteritis (age >50, temporal headache)",
                    "Ophthalmic Shingles (vesicular rash, V1 distribution)",
                    "Temporomandibular Joint Dysfunction"
                ],
                "questions": [
                    {"id": "sin_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Acute Sinusitis - ≤10 Days (Viral / No Antibiotics)", "Acute Sinusitis - >10 Days (Consider Antibiotics)", "Suspected Periorbital Infection - ESCALATE", "Alternative Diagnosis"]}
                ]
            },
            {
                "title": "Antibiotic Decision (NICE Guidance)",
                "section_type": "plan",
                "questions": [
                    {"id": "sin_duration_category", "type": "single_select", "label": "Symptom Duration → Antibiotic Decision", "required": True, "options": ["≤10 Days: Do NOT offer antibiotics. Return if worsening/systemically unwell.", ">10 Days: Consider high-dose nasal steroids + back-up (delayed) antibiotic if not resolved after further 10 days."], "is_red_flag": True, "red_flag_positive": "RED FLAG: NICE: Antibiotics NOT indicated for symptoms ≤10 days. Reserve for >10 days or severe symptoms.", "red_flag_negative": ""},
                    {"id": "sin_antibiotic_choice", "type": "single_select", "label": "Antibiotic (If Indicated)", "required": False, "options": ["Amoxicillin (Pinamox) 500mg TDS for 5 days - confirm no penicillin allergy", "Doxycycline 100mg OD for 5 days - advise re photosensitivity", "Delayed / back-up prescription", "Not indicated"]},
                    {"id": "sin_penicillin_allergy", "type": "toggle", "label": "Penicillin Allergy? (If yes → Doxycycline)", "required": False}
                ]
            },
            {
                "title": "Symptomatic Management & Safety Netting",
                "section_type": "plan",
                "safety_netting": "RED FLAGS - return immediately if: worsening facial swelling, periorbital swelling, severe headache, neurological symptoms (confusion, visual changes), or systemically unwell. Average recovery time is around 2.5 weeks. Return if no improvement or sooner if red flags develop. Nasal decongestants (Otrivine/Sudafed): check patient is NOT on regular amitriptyline before advising (interaction risk). Analgesia: Paracetamol + Ibuprofen (if no contraindications). Steam inhalation may help. Avoid antibiotics for symptoms ≤10 days per NICE guidance.",
                "questions": [
                    {"id": "sin_analgesia", "type": "toggle", "label": "Analgesia Advised? (Paracetamol + Ibuprofen)", "required": False},
                    {"id": "sin_decongestant", "type": "toggle", "label": "Nasal Decongestant Advised? (Otrivine / Sudafed)", "required": False},
                    {"id": "sin_amitriptyline_check", "type": "toggle", "label": "Checked NOT on Amitriptyline Before Decongestant? (Interaction Risk)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Decongestants + Amitriptyline = interaction risk. Check before advising.", "red_flag_negative": ""},
                    {"id": "sin_red_flags_discussed", "type": "toggle", "label": "Red Flags Discussed? (Facial swelling, periorbital, neuro symptoms)", "required": True},
                    {"id": "sin_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if no improvement after 10 days, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_sinusitis()