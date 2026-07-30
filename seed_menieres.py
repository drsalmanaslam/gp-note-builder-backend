from app.database import SessionLocal
from app.models import User, Template, Category

def seed_menieres():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Ménière's Disease",
        "description": "Focused assessment for Ménière's disease covering classic triad, vestibular schwannoma exclusion, medication trials, and lifestyle advice.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "men_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Episodic spinning sensation with hearing loss and tinnitus"},
                    {"id": "men_duration_episode", "type": "text", "label": "Duration of Current Episode", "required": True, "placeholder": "e.g., 2 hours (Typically 20 min to several hours)"},
                    {"id": "men_vertigo_character", "type": "single_select", "label": "Vertigo Characteristics", "required": True, "options": ["Spinning sensation (true vertigo)", "Lightheaded / floating", "Unsteadiness only"]},
                    {"id": "men_vertigo_duration_typical", "type": "single_select", "label": "Typical Episode Duration", "required": True, "options": ["Seconds (<30 sec = BPPV)", "20 minutes to several hours (MÉNIÈRE'S)", "Hours to days", "Constant"]},
                    {"id": "men_posture_trigger", "type": "toggle", "label": "Affected by Posture or Position? (If yes = ?BPPV, not Ménière's)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Positional vertigo = ?BPPV, not Ménière's. Dix-Hallpike test.", "red_flag_negative": ""},
                    {"id": "men_associated", "type": "multi_select", "label": "Associated Symptoms (Classic Triad)", "required": True, "options": ["Nausea / vomiting", "Intermittent hearing loss (sensorineural)", "Dizziness", "Ear fullness / pressure", "Tinnitus (roaring)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Triad = episodic vertigo + fluctuating hearing loss + tinnitus = Ménière's.", "red_flag_negative": ""},
                    {"id": "men_recent_urti", "type": "toggle", "label": "Recent URTI?", "required": False},
                    {"id": "men_neuro_screen", "type": "multi_select", "label": "Neurological Screen", "required": True, "options": ["Paraesthesia", "Weakness", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Neurological symptoms = ?central cause (CVA). Urgent neurology.", "red_flag_negative": ""},
                    {"id": "men_unilateral_tinnitus", "type": "toggle", "label": "Unilateral Tinnitus or Hearing Loss? (New/Progressive)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: New/progressive unilateral tinnitus/hearing loss = ?vestibular schwannoma (acoustic neuroma). ENT referral for MRI.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "men_ent_tm", "type": "single_select", "label": "Tympanic Membranes", "required": False, "options": ["Normal B/L", "Abnormal"]},
                    {"id": "men_ent_pharynx", "type": "single_select", "label": "Pharynx", "required": False, "options": ["Normal", "Erythematous"]},
                    {"id": "men_ent_lymph", "type": "toggle", "label": "Lymphadenopathy?", "required": False},
                    {"id": "men_ent_coryzal", "type": "toggle", "label": "Coryzal?", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Ménière's Disease (Classic Triad: Episodic Vertigo + Fluctuating Hearing Loss + Tinnitus)",
                    "BPPV (Brief positional vertigo <30 sec, no hearing loss)",
                    "Vestibular Neuritis (Single prolonged episode, no hearing loss)",
                    "Vestibular Schwannoma / Acoustic Neuroma (Unilateral progressive hearing loss + tinnitus)",
                    "Labyrinthitis (Vertigo + hearing loss + recent URTI)",
                    "Migrainous Vertigo",
                    "Central Cause - CVA/TIA (RED FLAG - neurological symptoms)"
                ],
                "questions": [
                    {"id": "men_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Ménière's Disease - Classic Triad", "Suspected BPPV (Positional)", "Suspected Vestibular Schwannoma - ENT Referral", "Suspected Central Cause - URGENT Neurology", "Uncertain - Needs ENT Assessment"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if no improvement - may require ENT referral. Avoid caffeine and alcohol (both can trigger attacks). Medication trial: Prochlorperazine (Stemetil) for acute vertigo/nausea, OR Betahistine for prophylaxis (note: limited evidence base for betahistine). Signpost to Ménière's Society for patient information and support (menieres.org.uk). If new/progressive unilateral tinnitus or hearing loss: ENT referral for MRI to exclude vestibular schwannoma. If neurological symptoms: urgent neurology referral. During acute attack: lie still, avoid bright lights, take prochlorperazine. Attacks typically last 20 minutes to several hours and may occur in clusters.",
                "questions": [
                    {"id": "men_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Avoid caffeine", "Avoid alcohol"]},
                    {"id": "men_medication", "type": "single_select", "label": "Medication Trial", "required": False, "options": ["Prochlorperazine (Stemetil) 5mg TDS PRN (Acute Vertigo)", "Betahistine 16mg TDS (Prophylaxis - Limited Evidence)", "Both", "None"]},
                    {"id": "men_support", "type": "toggle", "label": "Signposted to Ménière's Society? (menieres.org.uk)", "required": False},
                    {"id": "men_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "ENT (Routine - Persistent Symptoms)", "ENT (Urgent - ?Vestibular Schwannoma)", "Neurology (Urgent - ?Central Cause)"]},
                    {"id": "men_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if no improvement, routine ENT referral, or sooner if red flags"}
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
    seed_menieres()