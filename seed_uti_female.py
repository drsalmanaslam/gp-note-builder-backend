from app.database import SessionLocal
from app.models import User, Template

def seed_uti_female():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "UTI / Cystitis (Female)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of uncomplicated UTI in women covering dipstick interpretation, antibiotic choice per NICE NG109, red flags for pyelonephritis, and recurrent UTI management.", category="Urology", content={"sections": [
        {"title": "Symptoms", "section_type": "history", "questions": [
            {"id": "uti_dysuria", "type": "toggle", "label": "Dysuria (Burning/Pain on Passing Urine)?", "required": True},
            {"id": "uti_frequency", "type": "toggle", "label": "Frequency / Urgency?", "required": True},
            {"id": "uti_nocturia", "type": "toggle", "label": "Nocturia?", "required": False},
            {"id": "uti_suprapubic", "type": "toggle", "label": "Suprapubic Pain/Discomfort?", "required": True},
            {"id": "uti_haematuria", "type": "toggle", "label": "Haematuria (Visible Blood)?", "required": True},
            {"id": "uti_odour", "type": "toggle", "label": "Offensive Smell / Cloudy Urine?", "required": False},
            {"id": "uti_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 days"},
            {"id": "uti_loin_pain", "type": "toggle", "label": "Loin Pain / Flank Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Loin pain + fever = ?pyelonephritis. Needs systemic antibiotics + consider admission.", "red_flag_negative": ""},
            {"id": "uti_fever", "type": "toggle", "label": "Fever / Rigors?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever = ?pyelonephritis/sepsis. Urgent assessment. Admit if systemically unwell.", "red_flag_negative": ""},
            {"id": "uti_nausea", "type": "toggle", "label": "Nausea / Vomiting?", "required": False}
        ]},
        {"title": "Risk Factors & History", "section_type": "history", "questions": [
            {"id": "uti_pregnancy", "type": "toggle", "label": "Pregnant?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: UTI in pregnancy = treat with nitrofurantoin (avoid T1)/cefalexin. Send MSU. Refer if pyelonephritis.", "red_flag_negative": ""},
            {"id": "uti_recurrent", "type": "toggle", "label": "Recurrent UTIs? (≥3/year or ≥2/6 months)", "required": True},
            {"id": "uti_previous_uti", "type": "text", "label": "Most Recent UTI", "required": False, "placeholder": "e.g., 2 months ago"},
            {"id": "uti_catheter", "type": "toggle", "label": "Catheter?", "required": True},
            {"id": "uti_diabetes", "type": "toggle", "label": "Diabetes?", "required": False},
            {"id": "uti_immunocompromised", "type": "toggle", "label": "Immunocompromised?", "required": False},
            {"id": "uti_menopause", "type": "toggle", "label": "Postmenopausal? (Atrophic vaginitis risk)", "required": False},
            {"id": "uti_antibiotics_recent", "type": "toggle", "label": "Recent Antibiotics? (Resistance risk)", "required": False}
        ]},
        {"title": "Dipstick & Examination", "section_type": "examination", "questions": [
            {"id": "uti_dip_leuk", "type": "single_select", "label": "Leukocytes", "required": False, "options": ["Negative", "Trace", "+", "++", "+++"]},
            {"id": "uti_dip_nitrite", "type": "single_select", "label": "Nitrites", "required": False, "options": ["Negative", "Positive"]},
            {"id": "uti_dip_blood", "type": "single_select", "label": "Blood", "required": False, "options": ["Negative", "Trace", "+", "++", "+++"]},
            {"id": "uti_dip_protein", "type": "toggle", "label": "Protein Present?", "required": False},
            {"id": "uti_dip_glucose", "type": "toggle", "label": "Glucose Present?", "required": False},
            {"id": "uti_temp", "type": "text", "label": "Temperature", "required": False, "placeholder": "e.g., 37.2"},
            {"id": "uti_renal_tenderness", "type": "toggle", "label": "Renal Angle Tenderness?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Renal tenderness = ?pyelonephritis. Treat as upper UTI.", "red_flag_negative": ""},
            {"id": "uti_msu", "type": "toggle", "label": "MSU Sent?", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Uncomplicated lower UTI / Cystitis", "Pyelonephritis (upper UTI)", "Vaginitis / STI", "Interstitial cystitis / Painful bladder syndrome", "Atrophic vaginitis (postmenopausal)"], "questions": [
            {"id": "uti_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Uncomplicated UTI (≥2 symptoms + positive dipstick)", "Probable UTI (symptoms, dipstick negative - treat empirically)", "Pyelonephritis (fever + loin pain)", "Recurrent UTI", "Not UTI - consider alternative diagnosis"]},
            {"id": "uti_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - oral antibiotics at home", "Moderate - oral antibiotics + safety net", "Severe - consider admission (pyelonephritis/sepsis)"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately or attend A&E if: fever >38°C, rigors, loin pain, vomiting, confusion, or symptoms worsen despite antibiotics. First-line: Nitrofurantoin 100mg MR BD for 3 days (eGFR ≥45). Alternative: Trimethoprim 200mg BD 3 days. Second-line: Cefalexin 500mg BD 7 days. Always check local antibiotic guidelines. Recurrent UTI (>3/year): consider prophylactic antibiotics, post-coital antibiotics, or vaginal oestrogen (postmenopausal). Cranberry products - limited evidence. Increase fluid intake, void after sex, wipe front to back.", "questions": [
            {"id": "uti_antibiotic", "type": "single_select", "label": "Antibiotic Choice", "required": True, "options": ["Nitrofurantoin 100mg MR BD 3 days", "Trimethoprim 200mg BD 3 days", "Cefalexin 500mg BD 7 days", "Nitrofurantoin 50mg QDS 3 days", "Refer hospital (pyelonephritis/sepsis)"]},
            {"id": "uti_analgesia", "type": "toggle", "label": "Analgesia Advised? (Paracetamol/Ibuprofen)", "required": False},
            {"id": "uti_advice", "type": "multi_select", "label": "Advice Given", "required": True, "options": ["Increase fluids", "Void after intercourse", "Wipe front to back", "Cranberry products discussed", "Vaginal oestrogen discussed (postmenopausal)", "Prophylactic antibiotics discussed"]},
            {"id": "uti_safety", "type": "toggle", "label": "Red Flags Explained?", "required": True},
            {"id": "uti_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Return if not improved in 48h, MSU result in 1 week, routine if recurrent"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_uti_female()