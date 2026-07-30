from app.database import SessionLocal
from app.models import User, Template, Category

def seed_tinnitus():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Tinnitus",
        "description": "Focused assessment for tinnitus covering unilateral vs bilateral differentiation, acoustic neuroma exclusion, ototoxic medication review, and management strategies.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "KEY DIFFERENTIATOR - Unilateral vs Bilateral",
                "section_type": "history",
                "questions": [
                    {"id": "tin_laterality", "type": "single_select", "label": "Laterality", "required": True, "options": ["Bilateral (Typical Tinnitus)", "Unilateral - RED FLAG (Acoustic Neuroma)", "Unilateral + Hearing Loss - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: UNILATERAL tinnitus = ENT referral for MRI IAM to exclude acoustic neuroma. Do NOT manage via routine pathway.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "tin_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Bilateral ringing in ears for 3 months"},
                    {"id": "tin_character", "type": "single_select", "label": "Character", "required": True, "options": ["Ringing", "Buzzing", "Clicking", "Hissing", "Pulsatile - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Pulsatile tinnitus = ?vascular cause (AV malformation, carotid stenosis, glomus tumour). ENT + vascular referral.", "red_flag_negative": ""},
                    {"id": "tin_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3 months"},
                    {"id": "tin_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Continuous", "Intermittent"]},
                    {"id": "tin_impact", "type": "single_select", "label": "Impact on Quality of Life / Sleep", "required": True, "options": ["Minimal - coping well", "Moderate - affecting sleep/concentration", "Severe - significant distress"]},
                    {"id": "tin_associated", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Headache", "Hearing loss", "Dizziness / vertigo", "Ear fullness", "Nausea / vomiting", "Gait disturbance", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Tinnitus + hearing loss + vertigo = ?Ménière's, acoustic neuroma. ENT referral.", "red_flag_negative": ""},
                    {"id": "tin_otorrhoea", "type": "toggle", "label": "Otorrhoea?", "required": False},
                    {"id": "tin_recent_urti", "type": "toggle", "label": "Recent Cough / Cold?", "required": False},
                    {"id": "tin_noise_exposure", "type": "toggle", "label": "Previous Loud Noise Exposure?", "required": True},
                    {"id": "tin_head_injury", "type": "toggle", "label": "Head Injury?", "required": False},
                    {"id": "tin_ear_infections", "type": "toggle", "label": "Previous Ear Infections?", "required": False},
                    {"id": "tin_ototoxic_meds", "type": "multi_select", "label": "Ototoxic Medications", "required": True, "options": ["Loop Diuretics (Furosemide)", "Aspirin (High Dose)", "NSAIDs", "Aminoglycosides", "Quinine", "None of the above"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "tin_ent_tm", "type": "single_select", "label": "Tympanic Membranes", "required": False, "options": ["Normal B/L", "Abnormal"]},
                    {"id": "tin_ent_pharynx", "type": "single_select", "label": "Pharynx", "required": False, "options": ["Normal", "Erythematous"]},
                    {"id": "tin_ent_lymph", "type": "toggle", "label": "Lymphadenopathy?", "required": False},
                    {"id": "tin_ent_coryza", "type": "toggle", "label": "Coryza?", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Idiopathic Bilateral Tinnitus (Most Common)",
                    "Noise-Induced Hearing Loss",
                    "Presbycusis (Age-Related Hearing Loss)",
                    "Ménière's Disease (Triad: Tinnitus + Vertigo + Hearing Loss)",
                    "Acoustic Neuroma / Vestibular Schwannoma (RED FLAG - Unilateral)",
                    "Pulsatile Tinnitus (Vascular - RED FLAG)",
                    "Ototoxic Medication-Induced",
                    "Anaemia (Contributing Factor)",
                    "Impacted Cerumen (Wax)",
                    "TMJ Dysfunction"
                ],
                "questions": [
                    {"id": "tin_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Bilateral Tinnitus - No Red Flags", "Bilateral Tinnitus - ?Ménière's", "Unilateral Tinnitus - ENT Referral for MRI IAM", "Pulsatile Tinnitus - URGENT ENT/Vascular", "Ototoxic Medication-Related"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "UNILATERAL tinnitus: ENT referral for MRI IAM to exclude acoustic neuroma - do NOT manage via routine pathway. PULSATILE tinnitus: ENT + vascular referral. Bilateral tinnitus with no red flags: FBC to exclude anaemia. Signpost to Tinnitus Association / British Tinnitus Association for support and information. Consider tinnitus masker (white noise generator, hearing aid if hearing loss). Avoid silence (background music/TV). Stress management and relaxation techniques. May require ENT referral for audiometry (bilateral, typical tinnitus). Review ototoxic medications - consider alternatives if appropriate.",
                "questions": [
                    {"id": "tin_fbc", "type": "toggle", "label": "FBC Ordered? (Exclude Anaemia)", "required": False},
                    {"id": "tin_support", "type": "toggle", "label": "Signposted to Tinnitus Association?", "required": False},
                    {"id": "tin_masker", "type": "toggle", "label": "Tinnitus Masker Considered? (White Noise / Hearing Aid)", "required": False},
                    {"id": "tin_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["None - GP Managed (Bilateral, No Red Flags)", "ENT - Routine (Audiometry - Bilateral Tinnitus)", "ENT - Urgent (Unilateral - MRI IAM)", "ENT + Vascular (Pulsatile Tinnitus)"]},
                    {"id": "tin_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Routine ENT referral, review with FBC result, sooner if red flags"}
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
    seed_tinnitus()