from app.database import SessionLocal
from app.models import User, Template, Category

def seed_atrial_fibrillation():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Atrial Fibrillation Assessment",
        "description": "Focused assessment for AF covering CHA2DS2-VASc scoring, rate vs rhythm control, DOAC prescribing, and stroke prevention.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "af_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Incidental AF on ECG / palpitations / SOB"},
                    {"id": "af_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 74"},
                    {"id": "af_how_detected", "type": "single_select", "label": "How Detected", "required": True, "options": ["Incidental ECG finding", "Palpitations", "SOB", "Pulse check", "Stroke/TIA workup", "Pre-operative"]},
                    {"id": "af_onset", "type": "single_select", "label": "Onset / Duration", "required": True, "options": ["<48 hours (acute) - RED FLAG", ">48 hours / unknown", "Paroxysmal (comes and goes)", "Persistent", "Permanent"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute onset <48h with symptoms = ?cardioversion candidate. Urgent cardiology/A&E.", "red_flag_negative": ""},
                    {"id": "af_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["None - asymptomatic", "Palpitations", "SOB", "Chest pain", "Dizziness / Pre-syncope", "Syncope", "Fatigue", "Reduced exercise tolerance"]},
                    {"id": "af_valvular", "type": "toggle", "label": "Rheumatic Heart Disease / Mitral Stenosis? (Valvular AF)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Valvular AF (mitral stenosis/mechanical valve) = WARFARIN only. DOACs contraindicated.", "red_flag_negative": ""},
                    {"id": "af_stroke_tia_history", "type": "toggle", "label": "Previous Stroke / TIA / Thromboembolism?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous stroke/TIA = CHA2DS2-VASc 2 points. Strong indication for anticoagulation.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination & ECG",
                "section_type": "examination",
                "questions": [
                    {"id": "af_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 128/80"},
                    {"id": "af_hr", "type": "number", "label": "Ventricular Rate (bpm)", "required": True, "placeholder": "e.g., 115", "is_red_flag": True, "red_flag_positive": "RED FLAG: HR >150 = ?rapid AF. Urgent rate control. HR <50 = ?sick sinus/block.", "red_flag_negative": ""},
                    {"id": "af_rhythm", "type": "single_select", "label": "Pulse Rhythm", "required": True, "options": ["Irregularly irregular (AF)", "Regular (flutter/tachycardia)", "Irregularly irregular + apex-pulse deficit"]},
                    {"id": "af_jvp", "type": "toggle", "label": "JVP Elevated?", "required": False},
                    {"id": "af_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal, No Murmurs", "Murmur (mitral valve disease?)", "Added sounds"]},
                    {"id": "af_oedema", "type": "toggle", "label": "Pedal Oedema?", "required": True},
                    {"id": "af_chest", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear B/L", "Crackles - ?heart failure RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Crackles = ?heart failure. Urgent CXR + diuretics.", "red_flag_negative": ""},
                    {"id": "af_ecg", "type": "single_select", "label": "ECG Confirmation", "required": True, "options": ["AF confirmed (absent P waves, irregular QRS)", "Atrial flutter", "Sinus rhythm with ectopics", "Other"]}
                ]
            },
            {
                "title": "CHA2DS2-VASc Score",
                "section_type": "assessment",
                "questions": [
                    {"id": "af_chf", "type": "toggle", "label": "CHF / LV Dysfunction? (1 point)", "required": True},
                    {"id": "af_hypertension", "type": "toggle", "label": "Hypertension? (1 point)", "required": True},
                    {"id": "af_age_75", "type": "toggle", "label": "Age ≥75? (2 points)", "required": True},
                    {"id": "af_diabetes", "type": "toggle", "label": "Diabetes? (1 point)", "required": True},
                    {"id": "af_stroke_tia", "type": "toggle", "label": "Previous Stroke/TIA/Thromboembolism? (2 points)", "required": True},
                    {"id": "af_vascular_disease", "type": "toggle", "label": "Vascular Disease? (IHD, PAD, aortic plaque) (1 point)", "required": True},
                    {"id": "af_age_65_74", "type": "toggle", "label": "Age 65-74? (1 point)", "required": True},
                    {"id": "af_sex_female", "type": "toggle", "label": "Female Sex? (1 point - only if other risk factors)", "required": True},
                    {"id": "af_chads_score", "type": "number", "label": "CHA2DS2-VASc Score (0-9)", "required": True, "placeholder": "e.g., 3"},
                    {"id": "af_anticoagulation_indicated", "type": "toggle", "label": "Anticoagulation Indicated? (Score ≥2 men / ≥3 women = YES. Score 1 men = consider)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: CHA2DS2-VASc ≥2 = anticoagulation strongly recommended. Score 1 = consider DOAC.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Bleeding Risk - ORBIT Score",
                "section_type": "assessment",
                "questions": [
                    {"id": "af_orbit_age", "type": "toggle", "label": "Age ≥75? (1 point)", "required": True},
                    {"id": "af_orbit_hb", "type": "toggle", "label": "Low Hb / Anaemia? (2 points)", "required": False},
                    {"id": "af_orbit_bleed", "type": "toggle", "label": "History of Bleeding? (2 points)", "required": True},
                    {"id": "af_orbit_gfr", "type": "toggle", "label": "eGFR <60? (1 point)", "required": False},
                    {"id": "af_orbit_antiplatelet", "type": "toggle", "label": "On Antiplatelet? (1 point)", "required": True},
                    {"id": "af_orbit_score", "type": "number", "label": "ORBIT Score (0-7)", "required": False, "placeholder": "e.g., 2"},
                    {"id": "af_bleeding_modifiable", "type": "multi_select", "label": "Modifiable Bleeding Risks", "required": False, "options": ["Uncontrolled HTN", "Alcohol excess", "NSAIDs", "Labile INR (if warfarin)", "None"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Non-Valvular Atrial Fibrillation (most common)",
                    "Valvular AF (mitral stenosis, mechanical valve - WARFARIN only)",
                    "Atrial Flutter",
                    "Paroxysmal AF",
                    "AF with Rapid Ventricular Response",
                    "AF with Heart Failure",
                    "Sick Sinus Syndrome / Tachy-Brady Syndrome"
                ],
                "questions": [
                    {"id": "af_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC + Ferritin", "U&E / eGFR (calculate CrCl Cockcroft-Gault)", "LFTs", "TFTs", "Fasting Glucose / HbA1c", "None"]},
                    {"id": "af_echo", "type": "toggle", "label": "TTE Referral? (Assess structure, LA size, LV function)", "required": True}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "URGENT ED/A&E if: new onset chest pain, severe shortness of breath, pre-syncope/syncope, or signs of stroke/TIA (FAST - Face, Arm, Speech, Time). Rate control target: resting HR <110 bpm (lenient strategy). DOAC counselling: issued patient alert card + information booklet. DOACs contraindicated in valvular AF (mitral stenosis/mechanical valve) - warfarin only. If cardiology considers elective cardioversion: anticoagulation must be continuous for at least 3-4 weeks prior and 4 weeks post. Routine review: every 12 months (6-monthly if age >75 or frail). At each review: calculate CrCl (Cockcroft-Gault), weight, compliance, concomitant medications, bleeding risks. High bleeding risk should prompt modification of risk factors, NOT withholding anticoagulation.",
                "questions": [
                    {"id": "af_plan", "type": "single_select", "label": "Management Strategy", "required": True, "options": ["Rate control (beta-blocker/CCB)", "DOAC commenced", "Warfarin (valvular AF or DOAC unsuitable)", "Refer cardiology (rhythm control)", "No anticoagulation (low CHA2DS2-VASc)"]},
                    {"id": "af_rate_control", "type": "single_select", "label": "Rate Control Agent", "required": False, "options": ["Bisoprolol 1.25-5mg OD", "Atenolol 25-100mg OD", "Verapamil (if beta-blocker CI)", "Digoxin (sedentary/elderly)", "None"]},
                    {"id": "af_doac", "type": "single_select", "label": "DOAC Prescribed", "required": False, "options": ["Apixaban 5mg BD (reduce to 2.5mg BD if ≥2: age≥80, wt≤60, Cr≥133)", "Edoxaban 60mg OD (reduce to 30mg if CrCl 15-50)", "Rivaroxaban 20mg OD with food (reduce to 15mg if CrCl 15-49)", "Dabigatran 150mg BD (reduce to 110mg if age≥80 or on Verapamil)", "None - warfarin indicated"]},
                    {"id": "af_alert_card", "type": "toggle", "label": "DOAC Patient Alert Card + Booklet Issued?", "required": False},
                    {"id": "af_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4 weeks for rate check, then 6-12 monthly. Annual bloods + CrCl."}
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
    seed_atrial_fibrillation()