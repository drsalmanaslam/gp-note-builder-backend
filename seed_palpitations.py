from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_palpitations():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Palpitations",
        "description": "Focused assessment for palpitations covering benign vs arrhythmic causes, red flags, caffeine/anxiety triggers, and investigation pathway.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Symptom Profile",
                "section_type": "history",
                "questions": [
                    {"id": "palp_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Intermittent palpitations for 3 months, at rest"},
                    {"id": "palp_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 34"},
                    {"id": "palp_duration_history", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 3 months"},
                    {"id": "palp_episode_duration", "type": "single_select", "label": "Duration Per Episode", "required": True, "options": ["Seconds", "5-10 minutes", "10-30 minutes", ">30 minutes", "Hours"]},
                    {"id": "palp_frequency", "type": "text", "label": "Frequency (episodes per week)", "required": True, "placeholder": "e.g., 2 times per week"},
                    {"id": "palp_onset", "type": "single_select", "label": "Onset Pattern", "required": True, "options": ["Abrupt (suggestive of arrhythmia)", "Gradual (suggestive of sinus tachycardia/anxiety)", "Variable"]},
                    {"id": "palp_offset", "type": "single_select", "label": "Offset Pattern", "required": True, "options": ["Abrupt (suggestive of arrhythmia)", "Slow/gradual (adrenergic)", "Variable"]},
                    {"id": "palp_character", "type": "single_select", "label": "Character / Rhythm Feel", "required": True, "options": ["Very fast + regular (SVT)", "Fast + irregular (AF)", "Skipping / extra beats (ectopics)", "Pounding / forceful (anxiety/sinus)", "Fluttering in neck"]},
                    {"id": "palp_timing", "type": "single_select", "label": "When Do They Occur?", "required": True, "options": ["At rest (watching TV, lying in bed)", "On exertion", "After exercise", "Random / no pattern"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Exertional palpitations = ?arrhythmia, cardiomyopathy. Urgent cardiology.", "red_flag_negative": ""},
                    {"id": "palp_triggers", "type": "multi_select", "label": "Triggers", "required": True, "options": ["Coffee / Caffeine", "Alcohol", "Stress / Anxiety", "Lying down / at night", "Exercise", "None identified"]}
                ]
            },
            {
                "title": "Associated Symptoms & RED FLAGS",
                "section_type": "history",
                "questions": [
                    {"id": "palp_chest_pain", "type": "toggle", "label": "Chest Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain + palpitations = ?ACS, myocarditis. Urgent A&E.", "red_flag_negative": ""},
                    {"id": "palp_sob", "type": "toggle", "label": "Shortness of Breath?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB + palpitations = ?arrhythmia, heart failure. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "palp_syncope", "type": "toggle", "label": "Syncope / Pre-Syncope / Lightheadedness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Syncope + palpitations = ?VT, complete heart block, Brugada. Urgent cardiology. Do NOT drive.", "red_flag_negative": ""},
                    {"id": "palp_diaphoresis", "type": "toggle", "label": "Diaphoresis (Sweating) During Episodes?", "required": False},
                    {"id": "palp_tingling", "type": "toggle", "label": "Finger / Perioral Tingling? (Hyperventilation)", "required": False},
                    {"id": "palp_anxiety", "type": "toggle", "label": "Anxiety / Panic Symptoms?", "required": True}
                ]
            },
            {
                "title": "Risk Factors & Substances",
                "section_type": "history",
                "questions": [
                    {"id": "palp_caffeine", "type": "single_select", "label": "Caffeine Intake", "required": True, "options": ["None", "1-2 cups/day", "3-5 cups/day", ">5 cups/day or energy drinks"]},
                    {"id": "palp_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess / binge drinking"]},
                    {"id": "palp_smoking", "type": "toggle", "label": "Smoking / Vaping?", "required": True},
                    {"id": "palp_drugs", "type": "toggle", "label": "Illicit Drugs / Amphetamines / Cocaine?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Stimulant drugs = arrhythmia risk. Urgent ECG + cardiac monitoring.", "red_flag_negative": ""},
                    {"id": "palp_decongestants", "type": "toggle", "label": "OTC Decongestants / Pseudoephedrine?", "required": False},
                    {"id": "palp_thyroid", "type": "multi_select", "label": "Thyrotoxicosis Symptoms?", "required": True, "options": ["Weight loss", "Heat intolerance", "Sweating", "Diarrhoea", "Fine tremor", "None"]},
                    {"id": "palp_family_scd", "type": "toggle", "label": "Family History Sudden Cardiac Death (<40)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx SCD = ?Brugada, LQTS, HOCM. Urgent cardiology.", "red_flag_negative": ""},
                    {"id": "palp_family_arrhythmia", "type": "toggle", "label": "Family History Arrhythmia / Cardiomyopathy?", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "palp_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 122/78"},
                    {"id": "palp_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 80"},
                    {"id": "palp_rhythm", "type": "single_select", "label": "Rhythm", "required": True, "options": ["Regular", "Irregular", "Irregularly irregular"]},
                    {"id": "palp_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal, No Murmurs", "Murmur present (HOCM/valve)", "Click", "Not assessed"]},
                    {"id": "palp_radial", "type": "toggle", "label": "Radio-Radial Delay?", "required": False},
                    {"id": "palp_goitre", "type": "toggle", "label": "Goitre / Thyroid Enlargement?", "required": False},
                    {"id": "palp_tremor", "type": "toggle", "label": "Fine Postural Tremor? (Hyperthyroidism)", "required": False},
                    {"id": "palp_exophthalmos", "type": "toggle", "label": "Exophthalmos / Lid Lag?", "required": False},
                    {"id": "palp_anaemia", "type": "toggle", "label": "Conjunctival Pallor? (Anaemia)", "required": False}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Sinus Tachycardia (anxiety, caffeine, hyperventilation)",
                    "Atrial Fibrillation / Atrial Flutter",
                    "Supraventricular Tachycardia (SVT / AVNRT / AVRT)",
                    "Ventricular Ectopic Beats (benign)",
                    "Paroxysmal AF",
                    "Hyperthyroidism",
                    "Anaemia",
                    "Phaeochromocytoma (rare)",
                    "Wolf-Parkinson-White Syndrome (delta waves on ECG)",
                    "Long QT Syndrome",
                    "Brugada Syndrome",
                    "Hypertrophic Cardiomyopathy (HOCM)"
                ],
                "questions": [
                    {"id": "palp_ecg", "type": "single_select", "label": "12-Lead ECG", "required": True, "options": ["Normal sinus rhythm", "Sinus tachycardia", "AF / Flutter", "Delta waves (WPW) - RED FLAG", "Long QTc (>460ms) - RED FLAG", "LVH / ST-T changes", "Ectopic beats", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: WPW/delta waves, long QTc, Brugada pattern = urgent cardiology.", "red_flag_negative": ""},
                    {"id": "palp_pr", "type": "number", "label": "PR Interval (ms)", "required": False, "placeholder": "e.g., 160 (NR: 120-200)"},
                    {"id": "palp_qrs", "type": "number", "label": "QRS Duration (ms)", "required": False, "placeholder": "e.g., 90 (NR: <120)"},
                    {"id": "palp_qtc", "type": "number", "label": "QTc (ms)", "required": False, "placeholder": "e.g., 420 (NR: <440M, <460F)"},
                    {"id": "palp_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC (anaemia)", "TFTs (TSH, Free T4)", "U&E / eGFR", "Fasting Glucose / HbA1c", "Lipids", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Attend ED immediately if: palpitations become sustained (lasting >30 minutes), newly associated with severe chest pain, SOB, or loss of consciousness/syncope. Do NOT drive if experiencing syncope or presyncope with palpitations. Caffeine: stop/reduce strictly (coffee, energy drinks, chocolate). Breathing technique for hyperventilation: slow abdominal/pursed-lip breathing during episodes. Avoid alcohol, OTC decongestants, and stimulants. If episodes increase in frequency/duration: refer for 24-48h Holter monitor / event recorder. If ECG abnormal or structural heart disease suspected: refer cardiology for echocardiogram.",
                "questions": [
                    {"id": "palp_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Likely benign / adrenergic (sinus tachycardia)", "Suspected SVT / arrhythmia", "Suspected AF", "Anxiety-related", "Suspected thyrotoxicosis", "Uncertain - needs Holter"]},
                    {"id": "palp_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassurance + lifestyle (reduce caffeine)", "Holter monitor (24-48h)", "Event recorder", "Refer cardiology (routine)", "Refer cardiology (urgent - red flags)", "Treat underlying cause (thyroid/anaemia)"]},
                    {"id": "palp_caffeine_advice", "type": "toggle", "label": "Caffeine Reduction / Elimination Advised?", "required": False},
                    {"id": "palp_breathing", "type": "toggle", "label": "Slow Breathing Technique Demonstrated?", "required": False},
                    {"id": "palp_driving", "type": "toggle", "label": "Driving Advice Given? (Do not drive if syncope/presyncope)", "required": False},
                    {"id": "palp_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4 weeks if no improvement, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_palpitations()