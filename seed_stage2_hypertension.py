from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_stage2_hypertension():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Stage 2 Hypertension",
        "description": "Structured assessment for Stage 2 hypertension covering immediate pharmacotherapy initiation, drug selection by age/ethnicity, fixed-dose combinations, and monitoring.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Diagnosis & BP Profile",
                "section_type": "history",
                "questions": [
                    {"id": "htn2_presenting_complaint", "type": "text", "label": "Reason for Assessment", "required": True, "placeholder": "e.g., Raised BP on routine check / ABPM result"},
                    {"id": "htn2_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 58"},
                    {"id": "htn2_ethnicity", "type": "single_select", "label": "Ethnicity (guides drug choice)", "required": True, "options": ["White / Caucasian", "Afro-Caribbean / Black", "Asian", "Other"]},
                    {"id": "htn2_clinic_bp", "type": "text", "label": "Clinic BP (mmHg)", "required": True, "placeholder": "e.g., 160/100"},
                    {"id": "htn2_abpm_day", "type": "text", "label": "ABPM / HBPM Daytime Average (mmHg)", "required": True, "placeholder": "e.g., 150/95"},
                    {"id": "htn2_stage2", "type": "toggle", "label": "Stage 2 Confirmed? (Clinic ≥160/100 or ABPM ≥150/95)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Stage 2 HTN = TREAT ALL patients with pharmacotherapy regardless of age, QRISK, or TOD.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Target Organ Damage (TOD) & Secondary Causes",
                "section_type": "history",
                "questions": [
                    {"id": "htn2_headaches", "type": "toggle", "label": "Headaches / Visual Disturbance?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe headache + visual symptoms = ?malignant HTN. Urgent fundoscopy + same-day assessment.", "red_flag_negative": ""},
                    {"id": "htn2_phaeo", "type": "multi_select", "label": "Phaeochromocytoma Triad?", "required": True, "options": ["Episodic sweating", "Palpitations", "Severe paroxysmal headache", "None"]},
                    {"id": "htn2_conns", "type": "toggle", "label": "Muscle Weakness / Cramps? (Hypokalaemia - ?Conn's)", "required": False},
                    {"id": "htn2_nsaids", "type": "toggle", "label": "Regular NSAIDs / Steroids / Decongestants?", "required": True},
                    {"id": "htn2_ckd", "type": "toggle", "label": "Known CKD?", "required": True},
                    {"id": "htn2_diabetes", "type": "toggle", "label": "Type 2 Diabetes?", "required": True},
                    {"id": "htn2_cvd", "type": "toggle", "label": "Established CVD? (IHD, Stroke, PAD)", "required": True},
                    {"id": "htn2_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
                    {"id": "htn2_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "htn2_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 30"},
                    {"id": "htn2_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal", "Murmur / S4", "Not assessed"]},
                    {"id": "htn2_pulses", "type": "single_select", "label": "Peripheral Pulses", "required": True, "options": ["B/L present + normal", "Radio-femoral delay - RED FLAG", "Weak femoral - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal pulses = ?coarctation. Urgent vascular imaging.", "red_flag_negative": ""},
                    {"id": "htn2_renal_bruit", "type": "toggle", "label": "Renal Artery Bruit?", "required": False},
                    {"id": "htn2_cushingoid", "type": "toggle", "label": "Cushingoid Features?", "required": False},
                    {"id": "htn2_fundoscopy", "type": "single_select", "label": "Fundoscopy", "required": False, "options": ["Normal", "AV nipping", "Haemorrhages/exudates - RED FLAG", "Papilloedema - RED FLAG", "Not yet done"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "htn2_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["U&E / eGFR", "HbA1c / Fasting Glucose", "TFTs", "LFTs + Fasting Lipids", "None"]},
                    {"id": "htn2_uacr", "type": "toggle", "label": "Urine ACR + Dipstick Ordered?", "required": True},
                    {"id": "htn2_ecg", "type": "single_select", "label": "ECG - LVH?", "required": True, "options": ["No LVH", "LVH present - RED FLAG", "ST-T strain - RED FLAG", "Not done"]}
                ]
            },
            {
                "title": "Pharmacotherapy Selection",
                "section_type": "plan",
                "questions": [
                    {"id": "htn2_first_line", "type": "single_select", "label": "First-Line Agent (by Age + Ethnicity)", "required": True, "options": ["ACEi / ARB (Age <55 or T2DM)", "CCB - Amlodipine (Age ≥55 or Afro-Caribbean)", "Dual combination (if non-frail Stage 2)"]},
                    {"id": "htn2_acei_arb", "type": "single_select", "label": "ACEi / ARB Choice", "required": False, "options": ["Ramipril 2.5mg nocte (titrate to 5-10mg)", "Ramipril 1.25mg (if on diuretic/DM/CKD/HF)", "Lisinopril 5mg OD", "Losartan 50mg OD", "Perindopril 4mg OD", "Not applicable"]},
                    {"id": "htn2_ccb", "type": "single_select", "label": "CCB Choice", "required": False, "options": ["Amlodipine 5mg OD (titrate to 10mg)", "Lercanidipine 10mg OD", "Not applicable"]},
                    {"id": "htn2_combination", "type": "single_select", "label": "Fixed-Dose Combination (if indicated)", "required": False, "options": ["Acerycal/Coveram (Perindopril/Amlodipine)", "Lercaril (Enalapril/Lercanidipine)", "Twynsta (Telmisartan/Amlodipine)", "Coversyl Plus (Perindopril/Indapamide)", "Coverdine (Perindopril/Indapamide/Amlodipine - triple)", "None - monotherapy sufficient"]}
                ]
            },
            {
                "title": "Monitoring & Targets",
                "section_type": "plan",
                "safety_netting": "Nurse review in 1 week: check BP response + U&E (1-2 weeks post ACEi/ARB start). Acceptable: ≤30% rise Cr or ≤25% drop eGFR. Dry cough with ACEi = switch to ARB. Avoid grapefruit juice with CCBs. BP targets: Age <80 = clinic <140/90 (ABPM <135/85). Age ≥80 = clinic <150/90 (ABPM <145/85). Achieve within 3 months. Annual renal profile + uACR + BP review once stable. Lifestyle: DASH diet, sodium <6g/day, exercise, weight management. Refer secondary care if uncontrolled on optimal triple therapy (including diuretic) or if secondary HTN suspected.",
                "questions": [
                    {"id": "htn2_target_under80", "type": "toggle", "label": "Target <140/90 (Age <80)?", "required": False},
                    {"id": "htn2_target_over80", "type": "toggle", "label": "Target <150/90 (Age ≥80)?", "required": False},
                    {"id": "htn2_nurse_review", "type": "toggle", "label": "Nurse Review in 1 Week Booked? (BP + U&E)", "required": True},
                    {"id": "htn2_lifestyle", "type": "toggle", "label": "Lifestyle Advice Given?", "required": True},
                    {"id": "htn2_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1 week nurse, 4 weeks GP, titrate to target within 3 months"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_stage2_hypertension()