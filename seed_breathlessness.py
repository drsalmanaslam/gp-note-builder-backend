from app.database import SessionLocal
from app.models import User, Template, Category

def seed_breathlessness():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Breathlessness / SOB - Comprehensive",
        "description": "Comprehensive breathlessness assessment covering mMRC grading, cardiac vs respiratory differentiation, spirometry interpretation, NT-proBNP pathway, and multifactorial approach.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Symptom Profile",
                "section_type": "history",
                "questions": [
                    {"id": "sob2_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Progressive breathlessness over 3 weeks"},
                    {"id": "sob2_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 3 weeks"},
                    {"id": "sob2_trajectory", "type": "single_select", "label": "Trajectory", "required": True, "options": ["Progressive", "Stable", "Improving"]},
                    {"id": "sob2_mmrc", "type": "single_select", "label": "mMRC Dyspnoea Scale", "required": True, "options": ["Grade 0 - SOB only on strenuous exercise", "Grade 1 - SOB hurrying or walking uphill", "Grade 2 - Walks slower or stops for breath", "Grade 3 - Stops after ~100m", "Grade 4 - Too breathless to leave house"], "is_red_flag": True, "red_flag_positive": "RED FLAG: mMRC 3-4 = severe breathlessness. Urgent investigation for cardiac/respiratory cause.", "red_flag_negative": ""},
                    {"id": "sob2_baseline", "type": "text", "label": "Baseline (12 Months Ago)", "required": False, "placeholder": "e.g., mMRC Grade 0"}
                ]
            },
            {
                "title": "Cardiac vs Respiratory Differentiation",
                "section_type": "history",
                "questions": [
                    {"id": "sob2_cardiac_screen", "type": "multi_select", "label": "Cardiac / Heart Failure Screen", "required": True, "options": ["Worse lying down (orthopnoea)", "Requires multiple pillows (3-4)", "Paroxysmal nocturnal dyspnoea (PND)", "Nocturnal wheeze", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Orthopnoea + PND = HEART FAILURE until proven otherwise. Urgent echo + NT-proBNP.", "red_flag_negative": ""},
                    {"id": "sob2_cardiac_symptoms", "type": "multi_select", "label": "Cardiac Symptoms", "required": True, "options": ["Chest pain", "Palpitations", "Neither present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain + SOB = ?ACS. Urgent ECG + troponin.", "red_flag_negative": ""},
                    {"id": "sob2_oedema", "type": "toggle", "label": "Peripheral / Ankle Oedema?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ankle swelling + SOB = ?right heart failure. Urgent echo.", "red_flag_negative": ""},
                    {"id": "sob2_respiratory_screen", "type": "multi_select", "label": "Infective / Respiratory Screen", "required": True, "options": ["Fever", "Cough", "Sputum", "Wheeze", "Hoarseness", "None present"]},
                    {"id": "sob2_anxiety", "type": "toggle", "label": "Patient Feels Breathlessness Related to Anxiety?", "required": False}
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "sob2_risk_factors", "type": "multi_select", "label": "Risk Factor History", "required": True, "options": ["Smoking", "Alcohol excess", "History of anxiety / depression", "Asbestos exposure", "Occupational dust/chemicals", "None of the above"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "sob2_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["No increased WOB / respiratory distress", "Increased work of breathing noted - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Increased WOB = ?acute respiratory failure. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "sob2_vitals", "type": "text", "label": "Vital Signs", "required": True, "placeholder": "e.g., RR 18, HR 90, SpO2 99%, BP 128/88"},
                    {"id": "sob2_resp", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Equal air entry B/L, vesicular BS, no added sounds", "Reduced air entry", "Crackles (heart failure/fibrosis) - RED FLAG", "Wheeze (asthma/COPD)", "Clubbing present - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Crackles = ?heart failure/pulmonary oedema. Clubbing = ?lung cancer, fibrosis.", "red_flag_negative": ""},
                    {"id": "sob2_cvs", "type": "single_select", "label": "Cardiovascular Examination", "required": True, "options": ["HS I+II audible, no murmurs, regular pulse", "Murmur present (AS/MR) - RED FLAG", "Irregular pulse (AF)", "Added sounds (S3 gallop) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Murmur + SOB = ?valve disease. S3 gallop = heart failure. Urgent echo.", "red_flag_negative": ""},
                    {"id": "sob2_oedema_exam", "type": "single_select", "label": "Peripheral Oedema", "required": True, "options": ["None", "Present - ankle", "Present - to knee", "Sacral / anasarca"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Cardiac: Heart Failure, IHD, AF, Valve Disease, Pulmonary Hypertension",
                    "Respiratory: COPD, Asthma, ILD/Fibrosis, Bronchiectasis, Lung Cancer",
                    "Metabolic: Anaemia, CKD, Thyroid Disease, Obesity",
                    "Neuromuscular: Motor Neuron Disease, Myasthenia",
                    "Other: Deconditioning, Frailty, Anxiety"
                ],
                "questions": [
                    {"id": "sob2_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC (anaemia)", "TFTs", "Renal function (U&Es)", "LFTs", "HbA1c", "Fasting Lipids", "NT-proBNP (if available)"]},
                    {"id": "sob2_cxr", "type": "toggle", "label": "Chest X-Ray Requested?", "required": True},
                    {"id": "sob2_ecg", "type": "toggle", "label": "ECG Requested?", "required": True},
                    {"id": "sob2_echo", "type": "toggle", "label": "Echocardiogram? (If NT-proBNP >400 or murmur/S3)", "required": False},
                    {"id": "sob2_spirometry", "type": "toggle", "label": "Spirometry Referral?", "required": False},
                    {"id": "sob2_peak_flow", "type": "toggle", "label": "Peak Flow Meter + Diary?", "required": False}
                ]
            },
            {
                "title": "Spirometry Interpretation (Reference)",
                "section_type": "assessment",
                "questions": [
                    {"id": "sob2_spirometry_result", "type": "single_select", "label": "Spirometry Findings", "required": False, "options": ["FEV1/FVC <0.7, no reversibility → ?COPD", "FEV1/FVC <0.7, reversibility >12% → ?Asthma", "FEV1/FVC normal, FEV1/FVC reduced → ?Restrictive / poor effort", "Not yet performed"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: rapid deterioration, chest pain, haemoptysis, severe breathlessness at rest, or syncope. Breathlessness is frequently multifactorial - consider cardiac, respiratory, metabolic, neuromuscular, and other causes together. NT-proBNP >400 = echo indicated (?heart failure). Spirometry: FEV1/FVC <0.7 = obstruction (COPD vs asthma based on reversibility). Normal spirometry + symptoms = ?asthma (diurnal variation). Lifestyle: smoking cessation, alcohol reduction, weight management, increase physical activity (pulmonary rehabilitation if COPD).",
                "questions": [
                    {"id": "sob2_diagnosis", "type": "single_select", "label": "Working Impression", "required": True, "options": ["Likely multifactorial", "Predominantly cardiac", "Predominantly respiratory", "Predominantly metabolic (anaemia/thyroid)", "Predominantly anxiety / deconditioning"]},
                    {"id": "sob2_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Smoking cessation", "Alcohol reduction", "Weight management", "Increase physical activity"]},
                    {"id": "sob2_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - awaiting results", "Respiratory", "Cardiology", "Both respiratory + cardiology"]},
                    {"id": "sob2_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review with results, sooner if red flags"}
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
    seed_breathlessness()