from app.database import SessionLocal
from app.models import User, Template, Category

def seed_otitis_media():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Acute Otitis Media",
        "description": "Focused assessment for acute otitis media covering mastoiditis/facial nerve red flags, watchful waiting, delayed antibiotic prescribing, and safety netting.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Complications",
                "section_type": "history",
                "questions": [
                    {"id": "aom_facial_weakness", "type": "toggle", "label": "Facial Weakness, Numbness, or Tingling? (CN VII Involvement)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Facial nerve involvement = complication of AOM. URGENT ENT referral. Do NOT manage as simple AOM.", "red_flag_negative": ""},
                    {"id": "aom_mastoid_pain", "type": "toggle", "label": "Pain or Swelling in Bone Behind Ear? (Mastoiditis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Mastoid tenderness/swelling = ACUTE MASTOIDITIS. URGENT ENT referral. Do NOT manage as simple AOM.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "aom_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Ear pain and fever for 24 hours"},
                    {"id": "aom_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 24 hours (Symptoms typically take ~4 days to improve)"},
                    {"id": "aom_side", "type": "single_select", "label": "Affected Ear", "required": True, "options": ["Right", "Left", "Both"]},
                    {"id": "aom_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Otalgia (ear pain)", "Fever / pyrexia", "Sleep disturbance", "Irritability / crying (children)"]},
                    {"id": "aom_otorrhoea", "type": "toggle", "label": "Otorrhoea? (If Present = ?TM Perforation)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Purulent otorrhoea = TM perforation likely. Use non-ototoxic topical antibiotics if needed.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "aom_tm", "type": "single_select", "label": "Tympanic Membrane", "required": True, "options": ["Fullness / bulging + dullness + hyperaemia (AOM)", "Perforated (visible hole + discharge)", "Retracted (Eustachian dysfunction)", "Normal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bulging TM = acute otitis media. Perforated = treat accordingly (safe topical antibiotics).", "red_flag_negative": ""},
                    {"id": "aom_ent_pharynx", "type": "single_select", "label": "Pharynx", "required": False, "options": ["Normal", "Abnormal"]},
                    {"id": "aom_ent_lymph", "type": "toggle", "label": "Lymphadenopathy?", "required": False},
                    {"id": "aom_ent_coryza", "type": "toggle", "label": "Coryza?", "required": False},
                    {"id": "aom_mastoid", "type": "single_select", "label": "Mastoid", "required": True, "options": ["Non-tender, no swelling", "Tenderness / swelling present - RED FLAG (Mastoiditis)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Mastoid tenderness = ACUTE MASTOIDITIS. URGENT ENT.", "red_flag_negative": ""},
                    {"id": "aom_resp", "type": "single_select", "label": "Respiratory Examination", "required": False, "options": ["Air entry equal B/L, vesicular BS, no added sounds", "Reduced air entry", "Added sounds"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Acute Otitis Media (Viral - Most Common)",
                    "Acute Otitis Media (Bacterial)",
                    "Otitis Media with Effusion (Glue Ear - retracted TM, no inflammation)",
                    "Acute Mastoiditis (RED FLAG - mastoid tenderness/swelling)",
                    "TM Perforation (otorrhoea)",
                    "Referred Pain from Pharyngitis / Tonsillitis / Dental"
                ],
                "questions": [
                    {"id": "aom_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Acute Otitis Media - Likely Viral", "Acute Otitis Media - Bacterial Features", "AOM with TM Perforation", "Suspected Mastoiditis - URGENT ENT", "Facial Nerve Involvement - URGENT ENT"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: facial weakness/numbness/tingling, pain or swelling behind the ear (mastoiditis), symptoms worsen significantly, or no improvement after 4 days. Red flags discussed. Advise patient aware of out-of-hours services and A&E. Most AOM is viral and self-limiting - antibiotics NOT routinely indicated. Symptoms typically take ~4 days on average to improve. Analgesia: Paracetamol + Ibuprofen (if no CI) for pain and fever. Delayed (back-up) antibiotic prescription for Amoxicillin 500mg TDS for 5 days - use ONLY if symptoms have not started improving by Day 4 or if they worsen. Confirm no penicillin allergy before prescribing amoxicillin.",
                "questions": [
                    {"id": "aom_analgesia", "type": "toggle", "label": "Analgesia Advised? (Paracetamol + Ibuprofen)", "required": False},
                    {"id": "aom_delayed_abx", "type": "toggle", "label": "Delayed (Back-Up) Antibiotic Prescription Given? (Use if No Improvement at Day 4)", "required": False},
                    {"id": "aom_antibiotic", "type": "single_select", "label": "Antibiotic Choice (If Indicated)", "required": False, "options": ["Amoxicillin 500mg TDS for 5 Days", "Clarithromycin (Penicillin Allergy)", "Not prescribed"]},
                    {"id": "aom_penicillin_allergy", "type": "toggle", "label": "Penicillin Allergy?", "required": False},
                    {"id": "aom_red_flags_discussed", "type": "toggle", "label": "Red Flags Discussed? (Facial Weakness, Mastoid Pain, Deterioration)", "required": True},
                    {"id": "aom_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Use delayed script if no improvement by Day 4, return if red flags or concerns"}
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
    seed_otitis_media()