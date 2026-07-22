from app.database import SessionLocal
from app.models import User, Template, Category

def seed_chronic_cough():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Chronic Cough Assessment",
        "description": "Comprehensive assessment for chronic cough including differential diagnosis, red flags, and management plan.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "cc_gender", "type": "single_select", "label": "Gender", "required": True, "options": ["Male", "Female", "Trans Man", "Trans Woman"]},
                    {"id": "cc_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 45"}
                ]
            },
            {
                "title": "Chief Complaint",
                "section_type": "history",
                "questions": [
                    {"id": "cc_duration_value", "type": "number", "label": "Cough Duration (Number)", "required": True, "placeholder": "e.g., 3"},
                    {"id": "cc_duration_unit", "type": "single_select", "label": "Duration Unit", "required": True, "options": ["days", "weeks", "months"]},
                    {"id": "cc_type", "type": "single_select", "label": "Cough Type", "required": True, "options": ["Dry", "Productive", "Wet", "Whooping", "Barking"]},
                    {"id": "cc_sputum", "type": "multi_select", "label": "Sputum", "required": False, "options": ["None", "Clear", "Yellow", "Green", "White", "Bloody", "Blood-tinged", "Rust-coloured", "Foul-smelling"]},
                    {"id": "cc_rhinorrhoea", "type": "single_select", "label": "Rhinorrhoea", "required": False, "options": ["None", "Clear", "Coloured", "White", "Yellow", "Green", "Brown", "Blood-tinged"]},
                    {"id": "cc_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild", "Moderate", "Severe"]},
                    {"id": "cc_worsening", "type": "multi_select", "label": "Worsening Factors", "required": False, "options": ["Cold Air", "Lying Down", "Smoke", "Dust", "Stress", "Talking", "Certain Smells"]},
                    {"id": "cc_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
                    {"id": "cc_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Constant", "Intermittent", "Occasional", "Worsening", "Variable in Intensity"]}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "cc_contacts", "type": "toggle", "label": "Similar Symptoms in Close Contacts?", "required": False},
                    {"id": "cc_occupational", "type": "toggle", "label": "Occupational Exposure to Irritants?", "required": False},
                    {"id": "cc_nasal_congestion", "type": "toggle", "label": "Nasal Congestion/Post-nasal Drip?", "required": False},
                    {"id": "cc_sob", "type": "toggle", "label": "Shortness of Breath?", "required": False},
                    {"id": "cc_wheezing", "type": "toggle", "label": "Wheezing?", "required": False},
                    {"id": "cc_chest_tightness", "type": "toggle", "label": "Chest Tightness?", "required": False},
                    {"id": "cc_chest_pain", "type": "toggle", "label": "Chest Pain?", "required": False},
                    {"id": "cc_haemoptysis", "type": "toggle", "label": "Haemoptysis?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemoptysis reported. Urgent CXR and consider 2-week wait referral for lung cancer.", "red_flag_negative": "No haemoptysis."},
                    {"id": "cc_fever", "type": "toggle", "label": "Fever?", "required": False},
                    {"id": "cc_chills", "type": "toggle", "label": "Chills/Rigors?", "required": False},
                    {"id": "cc_fatigue", "type": "toggle", "label": "Fatigue?", "required": False},
                    {"id": "cc_night_sweats", "type": "toggle", "label": "Night Sweats?", "required": False},
                    {"id": "cc_weight_loss", "type": "toggle", "label": "Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unintentional weight loss with cough. Consider TB or malignancy. Urgent CXR and investigation.", "red_flag_negative": "No significant weight loss."},
                    {"id": "cc_hoarseness", "type": "toggle", "label": "Hoarseness?", "required": False}
                ]
            },
            {
                "title": "Past Medical History",
                "section_type": "history",
                "questions": [
                    {"id": "cc_pmh_none", "type": "toggle", "label": "No Significant PMHx?", "required": False},
                    {"id": "cc_covid", "type": "toggle", "label": "Recent COVID-19?", "required": False},
                    {"id": "cc_asthma", "type": "toggle", "label": "Asthma?", "required": False},
                    {"id": "cc_copd", "type": "toggle", "label": "COPD?", "required": False},
                    {"id": "cc_allergic_rhinitis", "type": "toggle", "label": "Allergic Rhinitis?", "required": False},
                    {"id": "cc_pneumonia", "type": "toggle", "label": "Previous Pneumonia?", "required": False},
                    {"id": "cc_gerd", "type": "toggle", "label": "GERD/Acid Reflux?", "required": False},
                    {"id": "cc_lung_cancer", "type": "toggle", "label": "Lung Cancer?", "required": False},
                    {"id": "cc_tb_exposure", "type": "toggle", "label": "TB Exposure/History?", "required": False},
                    {"id": "cc_similar_episodes", "type": "toggle", "label": "History of Similar Episodes?", "required": False}
                ]
            },
            {
                "title": "Medications",
                "section_type": "history",
                "questions": [
                    {"id": "cc_acei", "type": "toggle", "label": "Taking ACE Inhibitor? (e.g., Ramipril, Lisinopril)", "required": True},
                    {"id": "cc_other_meds", "type": "textarea", "label": "Other Current Medications", "required": False, "placeholder": "e.g., Salbutamol PRN, Omeprazole 20mg OD..."}
                ]
            },
            {
                "title": "ICE - Ideas, Concerns, Expectations",
                "section_type": "history",
                "questions": [
                    {"id": "cc_tried_treatment", "type": "multi_select", "label": "Treatments Already Tried", "required": False, "options": ["Cough Suppressants", "Antihistamines", "Antibiotics", "Corticosteroids", "Lozenges", "Steam Inhalation", "Saline Nasal Irrigation"]},
                    {"id": "cc_treatment_effect", "type": "single_select", "label": "Effectiveness of Tried Treatments", "required": False, "options": ["Effective", "Ineffective", "Temporarily Effective", "Not Applicable"]}
                ]
            },
            {
                "title": "Physical Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "cc_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well-appearing", "Ill-appearing", "In Apparent Distress", "Alert and Oriented", "Comfortable", "In Pain", "Lethargic", "Diaphoretic", "Pale", "Toxic"]},
                    {"id": "cc_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 120"},
                    {"id": "cc_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 80"},
                    {"id": "cc_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 80"},
                    {"id": "cc_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 16"},
                    {"id": "cc_o2", "type": "number", "label": "SpO2 (%)", "required": True, "placeholder": "e.g., 97"},
                    {"id": "cc_temp", "type": "number", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 36.8"},
                    {"id": "cc_throat", "type": "single_select", "label": "Throat Examination", "required": False, "options": ["Normal", "Redness", "Exudate Swelling", "Enlarged Tonsils", "Uvula Deviation", "Ulcers", "Postnasal Drip", "Cobblestone Appearance", "Intact Palate"]},
                    {"id": "cc_heart", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["RRR, Normal S1+S2, No Murmur", "Irregular", "Regularly-Irregular", "Murmur Present", "Friction Rub", "Gallop"]},
                    {"id": "cc_lungs", "type": "single_select", "label": "Lung Examination", "required": True, "options": ["Equal Air Entry Bilaterally, Vesicular BS, No Added Sounds", "Wheeze", "Crackles/Crepitations", "Rhonchi", "Reduced Air Entry", "Bronchial Breathing"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Post-nasal Drip", "Chronic Bronchitis", "GERD", "Asthma", "COPD", "Bronchiectasis", "Lung Cancer", "Tuberculosis", "ACEi-induced Cough", "Non-asthmatic Eosinophilic Bronchitis", "Interstitial Lung Disease", "Heart Failure", "Pertussis", "Allergic Rhinitis", "Chronic Sinusitis", "Foreign Body Aspiration", "Occupational Lung Diseases"],
                "questions": [
                    {"id": "cc_diagnosis", "type": "textarea", "label": "Working Diagnosis / Impression", "required": True, "placeholder": "e.g., Likely post-nasal drip secondary to allergic rhinitis..."},
                    {"id": "cc_redflags_assessed", "type": "toggle", "label": "Red Flags Specifically Assessed and Excluded?", "required": True}
                ]
            },
            {
                "title": "Plan - Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "cc_bloods", "type": "multi_select", "label": "Blood Tests Ordered", "required": False, "options": ["FBC", "CRP", "Renal Function", "LFT", "Lipase", "Troponin", "BNP"]},
                    {"id": "cc_sputum_culture", "type": "toggle", "label": "Sputum Culture Sent?", "required": False},
                    {"id": "cc_allergy_test", "type": "toggle", "label": "Allergy Testing (RAST/IgE)?", "required": False},
                    {"id": "cc_ecg", "type": "toggle", "label": "ECG Requested?", "required": False},
                    {"id": "cc_cxr", "type": "toggle", "label": "Chest X-Ray Requested?", "required": False},
                    {"id": "cc_pft", "type": "toggle", "label": "Pulmonary Function Tests?", "required": False},
                    {"id": "cc_ct_sinuses", "type": "toggle", "label": "CT Sinuses?", "required": False}
                ]
            },
            {
                "title": "Plan - Management",
                "section_type": "plan",
                "questions": [
                    {"id": "cc_smoking_cessation", "type": "toggle", "label": "Smoking Cessation Counselling Given?", "required": False},
                    {"id": "cc_avoid_irritants", "type": "toggle", "label": "Advised to Avoid Irritants (Smoke/Dust/Chemicals)?", "required": False},
                    {"id": "cc_stop_acei", "type": "toggle", "label": "Stop ACE Inhibitor?", "required": False},
                    {"id": "cc_saline_nasal", "type": "toggle", "label": "Saline Nasal Irrigation Advised?", "required": False},
                    {"id": "cc_nasal_steroids", "type": "toggle", "label": "Nasal Steroids Prescribed?", "required": False},
                    {"id": "cc_cough_suppressants", "type": "toggle", "label": "Cough Suppressants?", "required": False},
                    {"id": "cc_ppi", "type": "toggle", "label": "PPI Trial? (e.g., Omeprazole)", "required": False},
                    {"id": "cc_expectorants", "type": "toggle", "label": "Expectorants?", "required": False},
                    {"id": "cc_inhalers", "type": "toggle", "label": "Inhalers Prescribed?", "required": False},
                    {"id": "cc_antibiotics", "type": "toggle", "label": "Antibiotics Prescribed?", "required": False},
                    {"id": "cc_antihistamine", "type": "single_select", "label": "Antihistamine Prescribed", "required": False, "options": ["None", "Cetirizine 10mg PO OD", "Fexofenadine 30mg", "Fexofenadine 120mg", "Fexofenadine 180mg OD", "Diphenhydramine 25mg 4-6hrs PRN"]},
                    {"id": "cc_referral_pulm", "type": "toggle", "label": "Referral to Pulmonologist?", "required": False},
                    {"id": "cc_referral_ent", "type": "toggle", "label": "Referral to ENT?", "required": False},
                    {"id": "cc_referral_immuno", "type": "toggle", "label": "Referral to Immunologist?", "required": False}
                ]
            },
            {
                "title": "Follow-Up",
                "section_type": "plan",
                "safety_netting": "If cough worsens, you develop haemoptysis, significant weight loss, night sweats, or shortness of breath at rest, seek urgent medical attention. If symptoms do not improve or new symptoms develop, please return for review.",
                "questions": [
                    {"id": "cc_followup_value", "type": "number", "label": "Follow-up in (Number)", "required": True, "placeholder": "e.g., 2"},
                    {"id": "cc_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["days", "weeks", "months"]},
                    {"id": "cc_followup_notes", "type": "textarea", "label": "Additional Follow-up Notes", "required": False}
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
    seed_chronic_cough()