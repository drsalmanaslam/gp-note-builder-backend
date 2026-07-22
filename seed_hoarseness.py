from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hoarseness():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Hoarseness / Dysphonia Assessment",
        "description": "Focused assessment for hoarseness with red flags for laryngeal malignancy, differential diagnosis, and ENT referral criteria.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "hoarse_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Hoarseness / voice change for 3 weeks"},
                    {"id": "hoarse_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 52", "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >45 with hoarseness >3 weeks = 2WW ENT referral for ?laryngeal cancer.", "red_flag_negative": ""},
                    {"id": "hoarse_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (acute)", "Gradual (weeks-months)"]},
                    {"id": "hoarse_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 4 weeks", "is_red_flag": True, "red_flag_positive": "RED FLAG: Hoarseness >3 weeks unexplained = URGENT ENT referral (2WW if risk factors).", "red_flag_negative": ""},
                    {"id": "hoarse_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Persistent (constant)", "Intermittent (comes and goes)", "Progressive worsening"]},
                    {"id": "hoarse_progressive", "type": "toggle", "label": "Progressive Worsening?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Progressive worsening suggests pathology - needs ENT referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Laryngeal Malignancy",
                "section_type": "history",
                "questions": [
                    {"id": "hoarse_smoking", "type": "single_select", "label": "Smoking History", "required": True, "options": ["Never smoked", "Ex-smoker", "Current smoker"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Smoking + hoarseness >3 weeks = high risk laryngeal cancer. 2WW ENT referral.", "red_flag_negative": ""},
                    {"id": "hoarse_smoking_pack_years", "type": "text", "label": "Pack Years (if smoker/ex)", "required": False, "placeholder": "e.g., 30 pack years"},
                    {"id": "hoarse_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within limits", "Excess (>14 units/week)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol excess + smoking + hoarseness = very high risk laryngeal cancer.", "red_flag_negative": ""},
                    {"id": "hoarse_neck_lump", "type": "toggle", "label": "Neck Lump?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neck lump with hoarseness = possible metastatic lymph node from laryngeal cancer. Urgent ENT.", "red_flag_negative": ""},
                    {"id": "hoarse_dysphagia", "type": "toggle", "label": "Dysphagia / Pain on Swallowing (Odynophagia)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysphagia + hoarseness = concern for pharyngeal/laryngeal malignancy. 2WW ENT.", "red_flag_negative": ""},
                    {"id": "hoarse_otalgia", "type": "toggle", "label": "Referred Ear Pain (Otalgia)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Otalgia with hoarseness = referred pain from laryngeal/pharyngeal pathology. Needs ENT assessment.", "red_flag_negative": ""},
                    {"id": "hoarse_haemoptysis", "type": "toggle", "label": "Haemoptysis?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemoptysis + hoarseness = possible laryngeal/lung malignancy. Urgent CXR + ENT referral.", "red_flag_negative": ""},
                    {"id": "hoarse_weight_loss", "type": "toggle", "label": "Unexplained Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + hoarseness = concern for malignancy. Urgent ENT referral.", "red_flag_negative": ""},
                    {"id": "hoarse_stridor", "type": "toggle", "label": "Stridor?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Stridor = airway emergency. Same-day emergency ENT assessment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hoarse_cough", "type": "single_select", "label": "Cough", "required": False, "options": ["None", "Dry cough", "Productive cough"]},
                    {"id": "hoarse_sore_throat", "type": "toggle", "label": "Sore Throat?", "required": False},
                    {"id": "hoarse_reflux", "type": "toggle", "label": "Heartburn / Acid Reflux? (GORD/LPR)", "required": True},
                    {"id": "hoarse_postnasal_drip", "type": "toggle", "label": "Post-Nasal Drip / Nasal Congestion?", "required": False},
                    {"id": "hoarse_fever_urti", "type": "toggle", "label": "Fever / Recent URTI Symptoms?", "required": False},
                    {"id": "hoarse_voice_overuse", "type": "toggle", "label": "Voice Overuse? (Teacher, singer, shouting)", "required": True},
                    {"id": "hoarse_globus", "type": "toggle", "label": "Globus Sensation? (Lump in throat)", "required": False}
                ]
            },
            {
                "title": "Past History & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "hoarse_recent_urti", "type": "toggle", "label": "Recent URTI?", "required": False},
                    {"id": "hoarse_gord", "type": "toggle", "label": "Known GORD / Hiatus Hernia?", "required": False},
                    {"id": "hoarse_thyroid", "type": "single_select", "label": "Thyroid Disease", "required": False, "options": ["None", "Hypothyroidism", "Goitre", "Thyroid surgery", "Thyroid nodule/mass"]},
                    {"id": "hoarse_neck_surgery", "type": "toggle", "label": "Previous Neck / Thyroid / Chest Surgery? (Recurrent laryngeal nerve risk)", "required": False},
                    {"id": "hoarse_intubation", "type": "toggle", "label": "Recent Intubation?", "required": False},
                    {"id": "hoarse_radiotherapy", "type": "toggle", "label": "Previous Radiotherapy to Neck?", "required": False},
                    {"id": "hoarse_autoimmune", "type": "multi_select", "label": "Autoimmune Disease", "required": False, "options": ["Rheumatoid Arthritis", "Sjögren's Syndrome", "SLE", "None"]},
                    {"id": "hoarse_acei", "type": "toggle", "label": "Taking ACE Inhibitor? (Ramipril, Lisinopril - can cause cough)", "required": True},
                    {"id": "hoarse_inhaled_steroids", "type": "toggle", "label": "Inhaled Corticosteroids? (Can cause dysphonia/candidiasis)", "required": False},
                    {"id": "hoarse_drying_meds", "type": "toggle", "label": "Antihistamines / Diuretics? (Drying effect on vocal cords)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hoarse_neck_exam", "type": "single_select", "label": "Neck Examination", "required": True, "options": ["Normal", "Thyroid enlargement/nodule", "Lymphadenopathy", "Neck mass"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Neck mass/lymphadenopathy + hoarseness = 2WW ENT referral.", "red_flag_negative": ""},
                    {"id": "hoarse_oropharynx", "type": "single_select", "label": "Oropharynx Inspection", "required": False, "options": ["Normal", "Erythema", "Exudate", "Ulcer/lesion", "Candidiasis", "Not visualised fully"]},
                    {"id": "hoarse_chest", "type": "single_select", "label": "Chest Auscultation", "required": False, "options": ["Clear", "Crackles", "Wheeze", "Reduced air entry"]},
                    {"id": "hoarse_cranial_nerves", "type": "toggle", "label": "Cranial Nerve Abnormalities? (If neurological cause suspected)", "required": False},
                    {"id": "hoarse_hypothyroid_signs", "type": "toggle", "label": "Signs of Hypothyroidism? (Goitre, bradycardia, dry skin, slow reflexes)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Acute Viral Laryngitis (most common)",
                    "GORD / Laryngopharyngeal Reflux (LPR)",
                    "Vocal Cord Nodules/Polyps (voice overuse)",
                    "Chronic Laryngitis (smoking/irritant)",
                    "Hypothyroidism",
                    "Vocal Cord Palsy (recurrent laryngeal nerve - check lung Ca, thyroid, aortic aneurysm, iatrogenic)",
                    "Laryngeal Carcinoma (squamous cell - smoking/alcohol)",
                    "Functional / Muscle Tension Dysphonia",
                    "Inhaled Corticosteroid-Related Dysphonia/Candidiasis",
                    "ACE Inhibitor-Induced Cough",
                    "Autoimmune (RA cricoarytenoid arthritis, Sjögren's)"
                ],
                "questions": [
                    {"id": "hoarse_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Acute laryngitis (viral)", "GORD/LPR", "Vocal cord nodules/polyps", "Chronic laryngitis", "Suspected laryngeal malignancy", "Vocal cord palsy suspected", "Hypothyroidism-related", "Functional dysphonia", "Uncertain"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "hoarse_tfts", "type": "toggle", "label": "TFTs Ordered? (If hypothyroidism suspected)", "required": False},
                    {"id": "hoarse_cxr", "type": "toggle", "label": "Chest X-Ray? (Smoker/red flags - apical lung lesion can cause nerve palsy)", "required": False},
                    {"id": "hoarse_ent_referral", "type": "single_select", "label": "ENT Referral for Laryngoscopy", "required": True, "options": ["Not needed (<3 weeks, no red flags)", "Urgent 2WW (hoarseness >3 weeks + red flags)", "Routine ENT (persistent >3 weeks, no red flags)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Hoarseness >3 weeks unexplained = ENT referral. 2WW if: age >45, smoker, alcohol excess, neck lump, dysphagia, otalgia, haemoptysis, weight loss.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If acute (<3 weeks) with no red flags: conservative management - voice rest (avoid whispering - it strains cords more), adequate hydration, avoid irritants (smoking, alcohol, caffeine), treat underlying cause (GORD - PPI trial, URTI - supportive). Steam inhalation may help. If red flags present or >3 weeks unexplained: urgent ENT referral for laryngoscopy (2WW if malignancy risk). Return immediately if: stridor (difficulty breathing), haemoptysis, dysphagia develops, neck lump appears, pain becomes severe, or voice changes progress. If on ACE inhibitor - consider trial cessation (after discussion) to see if cough/voice improves. If inhaled steroids - check inhaler technique, use spacer, rinse mouth after use.",
                "questions": [
                    {"id": "hoarse_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Conservative - voice rest, hydration, treat cause", "PPI trial (suspected GORD/LPR)", "Stop/review ACE inhibitor", "Review inhaled steroid technique", "Routine ENT referral", "Urgent 2WW ENT referral", "Trial voice rest + safety-net review"]},
                    {"id": "hoarse_voice_rest", "type": "toggle", "label": "Voice Rest Advised? (No whispering, limit talking, no throat clearing)", "required": False},
                    {"id": "hoarse_ppi", "type": "toggle", "label": "PPI Trial? (High-dose, e.g., Omeprazole 20mg BD for 8 weeks if LPR suspected)", "required": False},
                    {"id": "hoarse_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2 weeks if acute laryngitis, or review after ENT appointment"}
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
    seed_hoarseness()