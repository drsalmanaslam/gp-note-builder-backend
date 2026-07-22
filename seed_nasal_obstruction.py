from app.database import SessionLocal
from app.models import User, Template, Category

def seed_nasal_obstruction():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Blocked Nose / Nasal Obstruction",
        "description": "Focused assessment for nasal obstruction with red flags for sinonasal tumour, differential diagnosis, and management including allergic and structural causes.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "nose_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 45", "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >50 with new unilateral symptoms = consider sinonasal tumour. Urgent ENT referral.", "red_flag_negative": ""},
                    {"id": "nose_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (<12 weeks)", "Chronic (>12 weeks)", "Acute on chronic"]},
                    {"id": "nose_side", "type": "single_select", "label": "Side", "required": True, "options": ["Bilateral", "Unilateral - Right", "Unilateral - Left", "Alternating sides"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral persistent obstruction = red flag for structural lesion/tumour/foreign body. Needs examination and ?ENT referral.", "red_flag_negative": ""},
                    {"id": "nose_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Constant", "Intermittent", "Alternating sides (rhinitis)", "Worse at night/lying down"]}
                ]
            },
            {
                "title": "RED FLAGS - Sinonasal Tumour / Serious Pathology",
                "section_type": "history",
                "questions": [
                    {"id": "nose_bloody_discharge", "type": "toggle", "label": "Blood-Stained Discharge / Epistaxis?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral blood-stained discharge = sinonasal tumour until proven otherwise. Urgent 2WW ENT referral.", "red_flag_negative": ""},
                    {"id": "nose_facial_pain_swelling", "type": "toggle", "label": "Facial Pain / Swelling?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Facial swelling + unilateral obstruction = possible sinonasal malignancy. Urgent ENT referral.", "red_flag_negative": ""},
                    {"id": "nose_visual_disturbance", "type": "toggle", "label": "Visual Disturbance / Diplopia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms + nasal obstruction = possible orbital extension of sinonasal tumour. Urgent ENT + ophthalmology.", "red_flag_negative": ""},
                    {"id": "nose_cranial_nerve", "type": "toggle", "label": "Cranial Nerve Symptoms? (Numbness, diplopia, facial weakness)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cranial nerve involvement suggests advanced sinonasal tumour. Urgent ENT referral.", "red_flag_negative": ""},
                    {"id": "nose_neck_lump", "type": "toggle", "label": "Neck Lump / Lymphadenopathy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neck lump + unilateral nasal symptoms = possible metastatic node. 2WW ENT.", "red_flag_negative": ""},
                    {"id": "nose_weight_loss", "type": "toggle", "label": "Unexplained Weight Loss?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + unilateral obstruction = concern for malignancy.", "red_flag_negative": ""},
                    {"id": "nose_foreign_body", "type": "toggle", "label": "Foreign Body? (Child - unilateral + offensive discharge)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral offensive discharge in child = foreign body until proven otherwise. Needs removal.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "nose_rhinorrhoea", "type": "single_select", "label": "Rhinorrhoea (Nasal Discharge)", "required": True, "options": ["None", "Clear (allergic/viral)", "Purulent (yellow/green - infection)", "Blood-stained", "Offensive (foreign body/anaerobic infection)"]},
                    {"id": "nose_sneezing_itch", "type": "toggle", "label": "Sneezing / Itching / Watery Eyes? (Allergic)", "required": False},
                    {"id": "nose_facial_pain_pressure", "type": "toggle", "label": "Facial Pain / Pressure? (Sinusitis)", "required": False},
                    {"id": "nose_anosmia", "type": "toggle", "label": "Loss of Smell (Anosmia/Hyposmia)?", "required": False},
                    {"id": "nose_postnasal_drip", "type": "toggle", "label": "Post-Nasal Drip?", "required": False},
                    {"id": "nose_snoring", "type": "toggle", "label": "Snoring / Mouth Breathing / Sleep Disturbance?", "required": False},
                    {"id": "nose_ear_symptoms", "type": "toggle", "label": "Ear Fullness / Eustachian Tube Dysfunction?", "required": False}
                ]
            },
            {
                "title": "Pattern & Triggers",
                "section_type": "history",
                "questions": [
                    {"id": "nose_seasonal", "type": "single_select", "label": "Pattern", "required": False, "options": ["Seasonal (spring/summer - pollens)", "Perennial (year-round - dust mite, mould)", "Occupational triggers", "No clear pattern"]},
                    {"id": "nose_triggers", "type": "multi_select", "label": "Triggers", "required": False, "options": ["Pollen/grass", "Dust", "Animals/pets", "Mould", "Smoke/irritants", "Temperature changes", "Exercise (improves = non-structural)", "Alcohol", "NSAIDs/Aspirin", "None identified"]}
                ]
            },
            {
                "title": "Past History & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "nose_atopy", "type": "multi_select", "label": "Atopic History", "required": False, "options": ["Allergic rhinitis / hay fever", "Asthma", "Eczema", "Food allergies", "None"]},
                    {"id": "nose_polyps", "type": "toggle", "label": "Known Nasal Polyps?", "required": False},
                    {"id": "nose_previous_surgery", "type": "toggle", "label": "Previous Nasal Trauma / Surgery / Septal Deviation?", "required": False},
                    {"id": "nose_chronic_sinusitis", "type": "toggle", "label": "Recurrent / Chronic Sinusitis?", "required": False},
                    {"id": "nose_cocaine", "type": "toggle", "label": "Cocaine Use? (Septal perforation risk)", "required": False},
                    {"id": "nose_decongestant_overuse", "type": "toggle", "label": "Overuse Topical Decongestants? (>5-7 days - rhinitis medicamentosa)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Topical decongestant overuse causes rebound congestion (rhinitis medicamentosa). Must stop. Short steroid course can bridge withdrawal.", "red_flag_negative": ""},
                    {"id": "nose_meds", "type": "multi_select", "label": "Medications That Worsen Rhinitis", "required": False, "options": ["Beta-blockers", "ACE inhibitors", "NSAIDs / Aspirin", "Alpha-blockers", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "nose_rhinoscopy", "type": "single_select", "label": "Anterior Rhinoscopy", "required": True, "options": ["Normal", "Septal deviation", "Septal perforation", "Turbinate hypertrophy", "Nasal polyps", "Mass/lesion", "Blood/mucopus", "Foreign body", "Not visualised"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral mass/polyp/lesion = needs ENT referral for biopsy. Septal perforation in cocaine user = refer.", "red_flag_negative": ""},
                    {"id": "nose_external", "type": "single_select", "label": "External Nose", "required": False, "options": ["Normal", "Saddle deformity", "Deviated", "Swelling"]},
                    {"id": "nose_sinus_tenderness", "type": "toggle", "label": "Sinus Tenderness on Palpation?", "required": False},
                    {"id": "nose_oropharynx", "type": "toggle", "label": "Post-Nasal Drip / Cobblestone Appearance?", "required": False},
                    {"id": "nose_neck_exam", "type": "toggle", "label": "Neck Lymphadenopathy?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cervical lymphadenopathy + nasal obstruction = 2WW ENT.", "red_flag_negative": ""},
                    {"id": "nose_otoscopy", "type": "toggle", "label": "Otoscopy Abnormal? (Eustachian tube dysfunction)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Allergic Rhinitis (seasonal/perennial)",
                    "Non-Allergic Rhinitis (vasomotor)",
                    "Acute Rhinosinusitis (viral/bacterial)",
                    "Chronic Rhinosinusitis (with/without polyps)",
                    "Nasal Polyps",
                    "Deviated Nasal Septum",
                    "Rhinitis Medicamentosa (decongestant overuse)",
                    "Adenoidal Hypertrophy (children)",
                    "Foreign Body (children - unilateral + offensive discharge)",
                    "Sinonasal / Nasopharyngeal Tumour (red flag features)",
                    "Granulomatous Disease (GPA, Sarcoidosis - crusting, epistaxis, systemic)",
                    "Cocaine-Induced Septal Perforation"
                ],
                "questions": [
                    {"id": "nose_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Allergic rhinitis", "Non-allergic/vasomotor rhinitis", "Acute rhinosinusitis", "Chronic rhinosinusitis", "Nasal polyps", "Rhinitis medicamentosa", "Deviated septum", "Suspected sinonasal tumour", "Foreign body", "Uncertain"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "nose_allergy_test", "type": "toggle", "label": "Allergy Testing? (Skin prick / specific IgE if allergic cause suspected)", "required": False},
                    {"id": "nose_nasal_endoscopy", "type": "toggle", "label": "Nasal Endoscopy? (Red flags or refractory to treatment)", "required": False},
                    {"id": "nose_ct_sinuses", "type": "toggle", "label": "CT Sinuses? (Chronic sinusitis, red flags, pre-surgical)", "required": False},
                    {"id": "nose_bloods", "type": "multi_select", "label": "Bloods (if vasculitis suspected)", "required": False, "options": ["FBC", "ESR/CRP", "ANCA", "None indicated"]},
                    {"id": "nose_ent_referral", "type": "single_select", "label": "ENT Referral", "required": True, "options": ["Not needed", "Routine (refractory to treatment)", "Urgent (red flags, unilateral mass, suspected tumour)", "2WW (suspected malignancy)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral symptoms + red flags = 2WW ENT. Unilateral polyp/mass = refer for biopsy.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Allergic rhinitis: intranasal corticosteroid spray (e.g., Fluticasone/Mometasone) OD + oral antihistamine if needed. For moderate-severe: start nasal spray 2-4 weeks before pollen season. Rhinitis medicamentosa: STOP decongestant spray immediately. Short course oral prednisolone (30mg OD 5-7 days) or intranasal steroid to bridge withdrawal. Chronic rhinosinusitis: intranasal steroid + nasal saline irrigation (e.g., NeilMed sinus rinse) BD for ≥3 months before ENT referral. Avoid triggers. Return immediately if: unilateral bleeding develops, facial swelling, visual disturbance, severe headache, or new neck lump. If no improvement after 3 months of adequate treatment - refer ENT. Nasal polyps not responding to steroids - refer ENT for consideration of surgery.",
                "questions": [
                    {"id": "nose_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Intranasal corticosteroid ± antihistamine", "Nasal saline irrigation + steroid", "Stop topical decongestant + bridge with steroids", "Antibiotics (acute bacterial sinusitis)", "Allergy testing + avoidance", "Routine ENT referral", "Urgent/2WW ENT referral", "Reassurance + safety-net"]},
                    {"id": "nose_intranasal_steroid", "type": "toggle", "label": "Intranasal Corticosteroid Prescribed? (Fluticasone/Mometasone OD)", "required": False},
                    {"id": "nose_antihistamine", "type": "toggle", "label": "Oral Antihistamine Added? (Cetirizine/Loratadine/Fexofenadine)", "required": False},
                    {"id": "nose_saline_irrigation", "type": "toggle", "label": "Nasal Saline Irrigation Advised? (NeilMed BD, especially chronic sinusitis)", "required": False},
                    {"id": "nose_stop_decongestant", "type": "toggle", "label": "Stop Topical Decongestant? (Rhinitis medicamentosa)", "required": False},
                    {"id": "nose_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4 weeks to assess response, sooner if red flags"}
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
    seed_nasal_obstruction()