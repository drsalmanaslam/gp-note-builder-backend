from app.database import SessionLocal
from app.models import User, Template, Category

def seed_copd_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "COPD Review",
        "description": "Structured COPD review covering symptom burden, exacerbations, inhaler technique, MRC dyspnoea scale, and management optimisation.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Current Status",
                "section_type": "history",
                "questions": [
                    {"id": "copd_presenting_complaint", "type": "text", "label": "Reason for Review", "required": True, "placeholder": "e.g., Routine annual review / worsening SOB / post-exacerbation"},
                    {"id": "copd_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 68"},
                    {"id": "copd_diagnosis_year", "type": "text", "label": "Year Diagnosed", "required": False, "placeholder": "e.g., 2015"},
                    {"id": "copd_severity", "type": "single_select", "label": "GOLD Stage (based on spirometry)", "required": True, "options": ["GOLD 1 - Mild (FEV1 ≥80%)", "GOLD 2 - Moderate (FEV1 50-79%)", "GOLD 3 - Severe (FEV1 30-49%)", "GOLD 4 - Very Severe (FEV1 <30%)", "Unknown - spirometry needed"]}
                ]
            },
            {
                "title": "Symptom Burden",
                "section_type": "history",
                "questions": [
                    {"id": "copd_mrc", "type": "single_select", "label": "MRC Dyspnoea Scale", "required": True, "options": ["Grade 1 - SOB on strenuous exercise", "Grade 2 - SOB hurrying or walking uphill", "Grade 3 - Walks slower / stops for breath", "Grade 4 - SOB on walking 100m", "Grade 5 - Too breathless to leave house"], "is_red_flag": True, "red_flag_positive": "RED FLAG: MRC 4-5 = very severe breathlessness. Consider palliative care, oxygen assessment, respiratory referral.", "red_flag_negative": ""},
                    {"id": "copd_cat_score", "type": "number", "label": "CAT Score (0-40)", "required": False, "placeholder": "e.g., 18 (≥10 = high symptom burden)"},
                    {"id": "copd_cough", "type": "single_select", "label": "Cough", "required": True, "options": ["None", "Mild - occasional", "Moderate - daily", "Severe - constant"]},
                    {"id": "copd_sputum", "type": "single_select", "label": "Sputum", "required": True, "options": ["None", "White/clear", "Yellow/green (stable)", "Increased volume/purulence (exacerbation?)"]},
                    {"id": "copd_sputum_volume", "type": "single_select", "label": "Sputum Volume Change?", "required": False, "options": ["No change", "Increased recently"]},
                    {"id": "copd_haemoptysis", "type": "toggle", "label": "Haemoptysis?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemoptysis = ?lung cancer. CXR urgently. 2WW if persistent.", "red_flag_negative": ""},
                    {"id": "copd_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + COPD = ?lung cancer, severe disease. CXR + consider nutritional support.", "red_flag_negative": ""},
                    {"id": "copd_ankle_swelling", "type": "toggle", "label": "Ankle Swelling? (Cor pulmonale)", "required": False}
                ]
            },
            {
                "title": "Exacerbations",
                "section_type": "history",
                "questions": [
                    {"id": "copd_exacerbations_12m", "type": "single_select", "label": "Exacerbations in Last 12 Months", "required": True, "options": ["None", "1 - GP treated (antibiotics/steroids)", "2 - GP treated", "≥3 or hospital admission", "ICU admission"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ≥2 moderate or ≥1 hospitalised exacerbation/year = frequent exacerbator phenotype. Optimise therapy, consider respiratory referral.", "red_flag_negative": ""},
                    {"id": "copd_ocs_courses", "type": "number", "label": "Number of Oral Steroid Courses in 12 Months", "required": False, "placeholder": "e.g., 3"},
                    {"id": "copd_antibiotics_courses", "type": "number", "label": "Number of Antibiotic Courses in 12 Months", "required": False, "placeholder": "e.g., 2"},
                    {"id": "copd_hospital_admissions", "type": "number", "label": "Hospital Admissions for COPD in 12 Months", "required": False, "placeholder": "e.g., 1"}
                ]
            },
            {
                "title": "Current Treatment & Adherence",
                "section_type": "history",
                "questions": [
                    {"id": "copd_current_inhalers", "type": "textarea", "label": "Current Inhalers", "required": True, "placeholder": "e.g., LAMA: Spiriva 18mcg OD\nLABA/ICS: Fostair 100/6 2 puffs BD\nSABA: Salbutamol 100mcg PRN"},
                    {"id": "copd_inhaler_technique", "type": "single_select", "label": "Inhaler Technique", "required": True, "options": ["Good", "Needs correction", "Poor - needs spacer/alternative device", "Not checked today"]},
                    {"id": "copd_adherence", "type": "single_select", "label": "Adherence", "required": True, "options": ["Good", "Fair", "Poor"]},
                    {"id": "copd_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never smoked", "Ex-smoker", "Current smoker"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Continued smoking = ongoing lung damage. Smoking cessation is the MOST effective intervention. Refer cessation service.", "red_flag_negative": ""},
                    {"id": "copd_pack_years", "type": "text", "label": "Pack Years", "required": False, "placeholder": "e.g., 40 pack years"},
                    {"id": "copd_oxygen", "type": "toggle", "label": "On Long-Term Oxygen Therapy (LTOT)?", "required": False},
                    {"id": "copd_nebulisers", "type": "toggle", "label": "Using Nebulisers?", "required": False},
                    {"id": "copd_vaccination", "type": "single_select", "label": "Vaccinations", "required": True, "options": ["Influenza + Pneumococcal up to date", "Influenza only", "Pneumococcal only", "Neither - advised today"]}
                ]
            },
            {
                "title": "Comorbidities",
                "section_type": "history",
                "questions": [
                    {"id": "copd_comorbidities", "type": "multi_select", "label": "Comorbidities", "required": False, "options": ["Ischaemic heart disease", "Heart failure", "Hypertension", "Diabetes", "Osteoporosis (steroid risk)", "Anxiety/Depression", "Obstructive sleep apnoea", "Bronchiectasis", "Lung cancer", "None"]},
                    {"id": "copd_anxiety_depression", "type": "toggle", "label": "Anxiety / Depression Screening Needed?", "required": False},
                    {"id": "copd_osteoporosis_risk", "type": "toggle", "label": "Osteoporosis Risk? (Multiple OCS courses, low BMI, smoker)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "copd_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well", "SOB at rest", "Cyanosed", "Pursed-lip breathing", "Cachectic", "Cushingoid (steroids)"]},
                    {"id": "copd_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": False, "placeholder": "e.g., 20"},
                    {"id": "copd_o2", "type": "number", "label": "SpO2 (%)", "required": False, "placeholder": "e.g., 92", "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 ≤92% on air = consider LTOT assessment. SpO2 <88% = urgent.", "red_flag_negative": ""},
                    {"id": "copd_hr", "type": "number", "label": "Heart Rate (bpm)", "required": False, "placeholder": "e.g., 88"},
                    {"id": "copd_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 24", "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI <21 = poor prognostic factor in COPD. Nutritional support needed.", "red_flag_negative": ""},
                    {"id": "copd_chest", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear", "Wheeze", "Coarse crackles", "Prolonged expiration", "Reduced air entry", "Silent chest - EMERGENCY"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Silent chest = life-threatening. Emergency admission.", "red_flag_negative": ""},
                    {"id": "copd_hyperinflation", "type": "toggle", "label": "Hyperinflation? (Barrel chest, hyperresonance)", "required": False},
                    {"id": "copd_ankle_oedema", "type": "toggle", "label": "Ankle Oedema? (Cor pulmonale)", "required": False},
                    {"id": "copd_jvp", "type": "toggle", "label": "Raised JVP? (Right heart failure)", "required": False}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "COPD - Stable",
                    "COPD - Exacerbation (infective)",
                    "COPD - Disease progression",
                    "COPD with Cor Pulmonale",
                    "COPD with Chronic Respiratory Failure (consider LTOT)",
                    "COPD + Lung Cancer (red flags)",
                    "Asthma-COPD Overlap (ACO)",
                    "Bronchiectasis",
                    "Heart Failure",
                    "Anaemia (worsening SOB)"
                ],
                "questions": [
                    {"id": "copd_spirometry", "type": "text", "label": "Latest Spirometry (FEV1, FVC, FEV1/FVC)", "required": False, "placeholder": "e.g., FEV1 55%, FVC 72%, FEV1/FVC 0.58"},
                    {"id": "copd_sats_walk", "type": "toggle", "label": "Ambulatory O2 Desaturation? (Walk test)", "required": False},
                    {"id": "copd_cxr", "type": "single_select", "label": "Chest X-Ray", "required": False, "options": ["Up to date - normal", "Up to date - hyperinflation", "Overdue - request today", "Not indicated"]},
                    {"id": "copd_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC (polycythaemia/anaemia)", "U&E", "Alpha-1 antitrypsin (if early onset/non-smoker)", "CRP", "None"]},
                    {"id": "copd_ecg", "type": "toggle", "label": "ECG? (Cor pulmonale, cardiac comorbidity)", "required": False},
                    {"id": "copd_echo", "type": "toggle", "label": "Echocardiogram Indicated? (?Cor pulmonale)", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: sudden worsening of breathlessness, change in sputum colour/volume, haemoptysis, chest pain, fever, confusion, or SpO2 <88%. Written COPD action plan provided. Influenza vaccine annually. Pneumococcal vaccine (once + booster per guidelines). Smoking cessation is the single most effective intervention. Pulmonary rehabilitation referral if MRC ≥3 or deconditioned. Consider palliative care input if MRC 4-5, frequent admissions, or weight loss. For exacerbation: Prednisolone 30mg OD for 5 days + antibiotics (Amoxicillin/Doxycycline) if purulent sputum. If on frequent OCS: consider osteoporosis prophylaxis.",
                "questions": [
                    {"id": "copd_plan", "type": "single_select", "label": "Management Decision", "required": True, "options": ["Continue same treatment", "Step up bronchodilator (add LAMA/LABA)", "Add ICS (if frequent exacerbator)", "Trial of triple therapy (LAMA/LABA/ICS)", "Refer pulmonary rehabilitation", "Refer respiratory specialist", "LTOT assessment", "Palliative care referral", "Treat exacerbation"]},
                    {"id": "copd_new_inhaler", "type": "text", "label": "New Inhaler(s) Prescribed", "required": False, "placeholder": "e.g., Trelegy Ellipta 1 puff OD"},
                    {"id": "copd_ocs", "type": "toggle", "label": "Oral Steroids Prescribed?", "required": False},
                    {"id": "copd_antibiotics_rx", "type": "toggle", "label": "Antibiotics Prescribed?", "required": False},
                    {"id": "copd_action_plan", "type": "toggle", "label": "Written COPD Action Plan Given?", "required": True},
                    {"id": "copd_inhaler_check", "type": "toggle", "label": "Inhaler Technique Checked?", "required": True},
                    {"id": "copd_smoking_cessation", "type": "toggle", "label": "Smoking Cessation Referred?", "required": False},
                    {"id": "copd_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4 weeks if step up, 3-6 months if stable, annual review"}
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
    seed_copd_review()