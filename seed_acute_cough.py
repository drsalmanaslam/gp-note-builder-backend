from app.database import SessionLocal
from app.models import User, Template

def seed_acute_cough():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Acute Cough / Bronchitis"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of acute cough (<3 weeks) covering viral vs bacterial bronchitis, pneumonia red flags, CRB65 score, and antibiotic stewardship.", category="Respiratory", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "ac_duration", "type": "text", "label": "Duration (days)", "required": True, "placeholder": "e.g., 5 days"},
            {"id": "ac_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
            {"id": "ac_sputum", "type": "single_select", "label": "Sputum", "required": True, "options": ["Dry/non-productive", "White/clear", "Yellow/green", "Blood-stained - RED FLAG", "Rust-coloured (?pneumococcal)"]},
            {"id": "ac_sob", "type": "toggle", "label": "Shortness of Breath?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB + cough = ?pneumonia/PE/LRTI. Examine + consider CXR.", "red_flag_negative": ""},
            {"id": "ac_chest_pain", "type": "toggle", "label": "Pleuritic Chest Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pleuritic pain = ?pneumonia/PE. Examine + investigate.", "red_flag_negative": ""},
            {"id": "ac_fever", "type": "toggle", "label": "Fever / Rigors?", "required": True},
            {"id": "ac_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
            {"id": "ac_asthma_copd", "type": "toggle", "label": "Known Asthma / COPD?", "required": True},
            {"id": "ac_immunocompromised", "type": "toggle", "label": "Immunocompromised?", "required": False}
        ]},
        {"title": "Examination & CRB65", "section_type": "examination", "questions": [
            {"id": "ac_confusion", "type": "toggle", "label": "New Confusion? (C in CRB65)", "required": True},
            {"id": "ac_rr", "type": "number", "label": "Respiratory Rate (R in CRB65 - ≥30 = 1 point)", "required": True, "placeholder": "e.g., 18"},
            {"id": "ac_bp_systolic", "type": "number", "label": "Systolic BP (B in CRB65 - <90 = 1 point)", "required": True, "placeholder": "e.g., 125"},
            {"id": "ac_age_crb", "type": "toggle", "label": "Age ≥65? (65 in CRB65)", "required": True},
            {"id": "ac_crb65", "type": "number", "label": "CRB65 Score (0-4)", "required": True, "placeholder": "e.g., 0"},
            {"id": "ac_o2", "type": "text", "label": "O2 Saturations (%)", "required": False, "placeholder": "e.g., 97%"},
            {"id": "ac_chest_exam", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear - normal breath sounds", "Focal crackles (consolidation)", "Wheeze", "Bronchial breathing", "Reduced air entry"]},
            {"id": "ac_temp", "type": "text", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 37.8"}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Acute Bronchitis (viral - most common)", "Community-Acquired Pneumonia", "Acute Exacerbation of Asthma", "Acute Exacerbation of COPD", "COVID-19", "Influenza", "PE (if acute SOB + pleuritic pain)", "Post-nasal drip / URTI"], "questions": [
            {"id": "ac_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Acute Bronchitis (viral) - no antibiotics", "Community-Acquired Pneumonia - antibiotics", "Acute Exacerbation Asthma/COPD", "URTI with cough", "Suspected PE - urgent referral"]},
            {"id": "ac_crb_action", "type": "single_select", "label": "CRB65 Action", "required": True, "options": ["CRB65 0: Home treatment", "CRB65 1-2: Consider hospital referral", "CRB65 3-4: Urgent hospital admission"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately or attend A&E if: increasing breathlessness, chest pain, coughing up blood, high fever >39°C, confusion, or symptoms worsening despite treatment. Viral bronchitis: self-limiting 2-3 weeks. Antibiotics NOT indicated for acute bronchitis (green sputum does NOT equal bacterial infection). Symptomatic: paracetamol/ibuprofen, honey & lemon, steam inhalation. If pneumonia: Amoxicillin 500mg TDS 5 days (or Doxycycline 200mg stat then 100mg OD 4 days if penicillin allergic). Smoking cessation advice if current smoker.", "questions": [
            {"id": "ac_antibiotics", "type": "toggle", "label": "Antibiotics Prescribed?", "required": True},
            {"id": "ac_antibiotic_type", "type": "text", "label": "Antibiotic & Dose", "required": False, "placeholder": "e.g., Amoxicillin 500mg TDS 5 days"},
            {"id": "ac_cxr", "type": "toggle", "label": "CXR Requested?", "required": False},
            {"id": "ac_smoking_cessation", "type": "toggle", "label": "Smoking Cessation Advised?", "required": False},
            {"id": "ac_safety_net", "type": "toggle", "label": "Red Flags Explained?", "required": True},
            {"id": "ac_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Return if not improved in 2 weeks, CXR if persistent cough >3 weeks"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_acute_cough()