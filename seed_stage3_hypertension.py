from app.database import SessionLocal
from app.models import User, Template, Category

def seed_stage3_hypertension():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Stage 3 Severe Hypertension",
        "description": "Emergency-focused assessment for severe hypertension (≥180/120) covering acute TOD screening, hospital vs primary care management, and immediate pharmacotherapy.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Diagnosis & Acute TOD Screening",
                "section_type": "history",
                "questions": [
                    {"id": "htn3_presenting_complaint", "type": "text", "label": "Reason for Assessment", "required": True, "placeholder": "e.g., Incidental BP 180/120 on routine check"},
                    {"id": "htn3_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 55"},
                    {"id": "htn3_clinic_bp", "type": "text", "label": "Clinic BP (mmHg)", "required": True, "placeholder": "e.g., 180/120", "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe HTN ≥180/120 = immediate assessment for acute TOD. Hospital if papilloedema/chest pain/confusion.", "red_flag_negative": ""},
                    {"id": "htn3_headache_visual", "type": "toggle", "label": "Severe Headache / Visual Disturbance / Confusion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypertensive encephalopathy = SAME-DAY HOSPITAL ADMISSION. Do NOT delay.", "red_flag_negative": ""},
                    {"id": "htn3_chest_pain_sob", "type": "toggle", "label": "Chest Pain / Acute SOB / Orthopnoea?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ACS/APO + severe HTN = EMERGENCY ADMISSION. 999/112.", "red_flag_negative": ""},
                    {"id": "htn3_neuro_deficit", "type": "toggle", "label": "Focal Weakness / Numbness / Speech Difficulty?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Stroke/TIA = EMERGENCY ADMISSION. FAST assessment.", "red_flag_negative": ""},
                    {"id": "htn3_phaeo", "type": "multi_select", "label": "Phaeochromocytoma Triad?", "required": True, "options": ["Episodic sweating", "Severe palpitations", "Paroxysmal headache", "Pallor", "None"]},
                    {"id": "htn3_meds", "type": "multi_select", "label": "Contributing Factors", "required": True, "options": ["NSAIDs", "Oral steroids", "Decongestants", "Sudden medication non-adherence", "High caffeine/liquorice", "None"]}
                ]
            },
            {
                "title": "Examination - Acute TOD",
                "section_type": "examination",
                "questions": [
                    {"id": "htn3_fundoscopy", "type": "single_select", "label": "Fundoscopy", "required": True, "options": ["Normal", "AV nipping only", "Haemorrhages / Exudates - HOSPITAL", "Papilloedema - HOSPITAL EMERGENCY", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Papilloedema/haemorrhages = MALIGNANT HTN. Same-day hospital admission.", "red_flag_negative": ""},
                    {"id": "htn3_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal", "S3/S4 / Murmur", "Not assessed"]},
                    {"id": "htn3_jvp", "type": "toggle", "label": "JVP Elevated?", "required": False},
                    {"id": "htn3_chest", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear B/L", "Crackles (APO) - HOSPITAL", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Crackles = acute pulmonary oedema. Emergency admission.", "red_flag_negative": ""},
                    {"id": "htn3_oedema", "type": "toggle", "label": "Peripheral Oedema?", "required": False},
                    {"id": "htn3_pulses", "type": "single_select", "label": "Peripheral Pulses", "required": False, "options": ["B/L present + normal", "Abnormal", "Not assessed"]},
                    {"id": "htn3_renal_bruit", "type": "toggle", "label": "Renal Bruit?", "required": False}
                ]
            },
            {
                "title": "NICE Clinical Pathway Decision",
                "section_type": "assessment",
                "questions": [
                    {"id": "htn3_acute_tod", "type": "single_select", "label": "Acute Target Organ Damage Present?", "required": True, "options": ["NO acute TOD → Manage in Primary Care", "YES - Papilloedema/haemorrhages → HOSPITAL", "YES - ACS/APO → EMERGENCY HOSPITAL", "YES - Encephalopathy → EMERGENCY HOSPITAL", "YES - Stroke/TIA → EMERGENCY HOSPITAL"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute TOD = HOSPITAL. No acute TOD = start treatment in primary care immediately + investigate within 7 days.", "red_flag_negative": ""},
                    {"id": "htn3_no_acute_tod_action", "type": "toggle", "label": "If NO Acute TOD: Start Treatment IMMEDIATELY (no ABPM needed)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe HTN without acute TOD = treat NOW. Do NOT wait for ABPM. Investigate within 7 days.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations (Within 7 Days)",
                "section_type": "assessment",
                "questions": [
                    {"id": "htn3_bloods", "type": "multi_select", "label": "Bloods Ordered (Within 7 Days)", "required": False, "options": ["U&E / eGFR", "HbA1c / Fasting Glucose", "TFTs", "LFTs + Fasting Lipids"]},
                    {"id": "htn3_uacr", "type": "toggle", "label": "Urine ACR + Dipstick Ordered?", "required": True},
                    {"id": "htn3_ecg", "type": "single_select", "label": "ECG - LVH?", "required": True, "options": ["No LVH", "LVH present", "Not done"]},
                    {"id": "htn3_optometry", "type": "toggle", "label": "Optometry Referral for Dilated Fundoscopy?", "required": True}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "EMERGENCY - attend ED/Ambulance IMMEDIATELY if: severe chest pain/tightness, sudden shortness of breath, severe headache with visual blurring/double vision/confusion, weakness/numbness/focal neurological deficits. If NO acute TOD: start antihypertensive TODAY. First-line: Age <55 or T2DM = ACEi/ARB (Ramipril 2.5-5mg). Age ≥55 or Afro-Caribbean = CCB (Amlodipine 5-10mg). If markedly elevated: consider dual combination (ACEi/ARB + CCB). Nurse review in 3-7 days for BP recheck + U&E. Formal optometry for dilated fundoscopy. Once stable: annual monitoring. If BP uncontrolled on triple therapy: refer secondary care.",
                "questions": [
                    {"id": "htn3_first_line", "type": "single_select", "label": "First-Line Agent", "required": True, "options": ["ACEi / ARB (Age <55 or T2DM)", "CCB - Amlodipine (Age ≥55 or Afro-Caribbean)", "Dual combination (ACEi/ARB + CCB)", "HOSPITAL ADMISSION (acute TOD)"]},
                    {"id": "htn3_acei", "type": "single_select", "label": "ACEi / ARB", "required": False, "options": ["Ramipril 2.5mg OD", "Ramipril 5mg OD", "Losartan 50mg OD", "Candesartan 8mg OD", "Not applicable"]},
                    {"id": "htn3_ccb", "type": "single_select", "label": "CCB", "required": False, "options": ["Amlodipine 5mg OD", "Amlodipine 10mg OD", "Not applicable"]},
                    {"id": "htn3_nurse_review", "type": "toggle", "label": "Nurse Review in 3-7 Days Booked? (BP + U&E)", "required": True},
                    {"id": "htn3_lifestyle", "type": "toggle", "label": "Lifestyle Advice Given?", "required": True},
                    {"id": "htn3_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3-7 days nurse, 2 weeks GP, titrate to target <140/90"}
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
    seed_stage3_hypertension()