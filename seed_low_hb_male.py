from app.database import SessionLocal
from app.models import User, Template, Category

def seed_low_hb_male():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low Haemoglobin - Male / Anaemia Assessment",
        "description": "Comprehensive assessment for low haemoglobin and anaemia in males including differential diagnosis, investigation, management, and referral criteria.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "lhb_gender", "type": "single_select", "label": "Gender", "required": True, "options": ["Male", "Trans Man"]},
                    {"id": "lhb_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 65", "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >50 with iron deficiency anaemia is potential GI malignancy until proven otherwise. Urgent GI workup required.", "red_flag_negative": ""},
                    {"id": "lhb_presentation", "type": "single_select", "label": "Presents For", "required": True, "options": ["New low Hb (incidental finding)", "New low Hb (symptomatic)", "Known anaemia - follow-up", "Known anaemia - not responding to treatment", "Known anaemia - worsening"]},
                    {"id": "lhb_presentation_detail", "type": "textarea", "label": "Presentation Details", "required": False, "placeholder": "Describe presenting complaint and circumstances leading to Hb check..."}
                ]
            },
            {
                "title": "Blood Results",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_hb", "type": "number", "label": "Haemoglobin (g/dL)", "required": True, "placeholder": "e.g., 10.5 (NR: 13.0-17.0)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Hb <8 g/dL is severe anaemia requiring urgent hospital assessment.", "red_flag_negative": ""},
                    {"id": "lhb_severity", "type": "single_select", "label": "Anaemia Severity", "required": True, "options": ["Normal (≥13.0 g/dL)", "Mild Anaemia (11.0-12.9 g/dL)", "Moderate Anaemia (8.0-10.9 g/dL)", "Severe Anaemia (<8.0 g/dL)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe anaemia (<8 g/dL) requires urgent hospital assessment. Moderate anaemia with symptoms may also require urgent referral.", "red_flag_negative": ""},
                    {"id": "lhb_mcv", "type": "number", "label": "MCV (fL)", "required": True, "placeholder": "e.g., 72 (NR: 80-100)"},
                    {"id": "lhb_mcv_type", "type": "single_select", "label": "MCV Classification", "required": True, "options": ["Microcytic (<80 fL)", "Normocytic (80-100 fL)", "Macrocytic (>100 fL)"]},
                    {"id": "lhb_mch", "type": "number", "label": "MCH (pg)", "required": False, "placeholder": "e.g., 24 (NR: 27-33)"},
                    {"id": "lhb_wcc", "type": "number", "label": "WCC (×10⁹/L)", "required": True, "placeholder": "e.g., 6.5 (NR: 4-11)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal WCC with anaemia may indicate haematological malignancy or bone marrow pathology.", "red_flag_negative": ""},
                    {"id": "lhb_platelets", "type": "number", "label": "Platelets (×10⁹/L)", "required": True, "placeholder": "e.g., 250 (NR: 150-400)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Thrombocytopenia with anaemia requires urgent haematology assessment for possible bone marrow failure or malignancy.", "red_flag_negative": ""},
                    {"id": "lhb_ferritin", "type": "number", "label": "Ferritin (µg/L)", "required": False, "placeholder": "e.g., 12 (NR: 30-400)"},
                    {"id": "lhb_iron", "type": "number", "label": "Iron (µmol/L)", "required": False, "placeholder": "e.g., 8 (NR: 10-30)"},
                    {"id": "lhb_transferrin_sat", "type": "number", "label": "Transferrin Saturation (%)", "required": False, "placeholder": "e.g., 15 (NR: 20-50)"},
                    {"id": "lhb_b12", "type": "number", "label": "Vitamin B12 (pg/mL)", "required": False, "placeholder": "e.g., 350 (NR: 200-900)"},
                    {"id": "lhb_folate", "type": "number", "label": "Folate (ng/mL)", "required": False, "placeholder": "e.g., 6.5 (NR: >4)"},
                    {"id": "lhb_reticulocyte", "type": "number", "label": "Reticulocyte Count", "required": False, "placeholder": "e.g., 0.8%"},
                    {"id": "lhb_creatinine", "type": "number", "label": "Creatinine (µmol/L)", "required": False, "placeholder": "e.g., 95 (NR: 60-110)"},
                    {"id": "lhb_egfr", "type": "number", "label": "eGFR (ml/min/1.73m²)", "required": True, "placeholder": "e.g., 68", "is_red_flag": True, "red_flag_positive": "RED FLAG: CKD is a common cause of anaemia. eGFR <30 may require nephrology referral.", "red_flag_negative": ""},
                    {"id": "lhb_esr", "type": "number", "label": "ESR (mm/hr)", "required": False, "placeholder": "e.g., 45"},
                    {"id": "lhb_crp", "type": "number", "label": "CRP (mg/L)", "required": False, "placeholder": "e.g., 18"},
                    {"id": "lhb_lfts", "type": "textarea", "label": "LFTs", "required": False, "placeholder": "e.g., ALT 42, AST 38, ALP 85, GGT 55, Bilirubin 12"},
                    {"id": "lhb_tfts", "type": "textarea", "label": "TFTs", "required": False, "placeholder": "e.g., TSH 3.2, T4 15.5"},
                    {"id": "lhb_urinalysis", "type": "single_select", "label": "Urinalysis", "required": False, "options": ["Normal", "Blood +", "Blood ++", "Blood +++", "Protein +", "Protein ++", "Glucose +", "Not done"]},
                    {"id": "lhb_other_labs", "type": "textarea", "label": "Other Lab Results", "required": False, "placeholder": "Coeliac screen, Hb electrophoresis, LDH, haptoglobin, bilirubin, SPEP, PSA..."}
                ]
            },
            {
                "title": "Associated Symptoms - General",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_fatigue", "type": "toggle", "label": "Fatigue/Lethargy?", "required": True},
                    {"id": "lhb_sob", "type": "toggle", "label": "Shortness of Breath?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB with anaemia may indicate cardiac compromise or severe anaemia. Assess urgently.", "red_flag_negative": "No shortness of breath."},
                    {"id": "lhb_palpitations", "type": "toggle", "label": "Palpitations?", "required": False},
                    {"id": "lhb_dizziness", "type": "toggle", "label": "Dizziness?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dizziness/syncope with anaemia may indicate haemodynamic compromise. Urgent assessment required.", "red_flag_negative": "No dizziness."},
                    {"id": "lhb_chest_pain", "type": "toggle", "label": "Chest Pain/Angina?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain with anaemia may indicate myocardial ischaemia. Urgent assessment and ECG required.", "red_flag_negative": "No chest pain."},
                    {"id": "lhb_syncope", "type": "toggle", "label": "Syncope/Collapse?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Syncope with anaemia is a medical emergency. Refer to hospital immediately.", "red_flag_negative": "No syncope."},
                    {"id": "lhb_headaches", "type": "toggle", "label": "Headaches?", "required": False},
                    {"id": "lhb_exercise_tolerance", "type": "toggle", "label": "Reduced Exercise Tolerance?", "required": False}
                ]
            },
            {
                "title": "Associated Symptoms - Blood Loss",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_pr_bleeding", "type": "toggle", "label": "PR Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: PR bleeding with iron deficiency anaemia requires urgent GI workup for colorectal cancer.", "red_flag_negative": "No PR bleeding."},
                    {"id": "lhb_pr_bleeding_detail", "type": "textarea", "label": "PR Bleeding Details", "required": False, "placeholder": "Colour (bright red/melaena), amount, frequency, mixed with stool or on paper..."},
                    {"id": "lhb_melaena", "type": "toggle", "label": "Melaena (Black Tarry Stools)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Melaena indicates upper GI bleeding. Urgent hospital assessment required.", "red_flag_negative": "No melaena."},
                    {"id": "lhb_haematemesis", "type": "toggle", "label": "Haematemesis (Vomiting Blood)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haematemesis is a medical emergency. Refer to hospital immediately.", "red_flag_negative": "No haematemesis."},
                    {"id": "lhb_haematuria", "type": "toggle", "label": "Haematuria (Blood in Urine)?", "required": False},
                    {"id": "lhb_haemoptysis", "type": "toggle", "label": "Haemoptysis (Coughing Blood)?", "required": False},
                    {"id": "lhb_epistaxis", "type": "toggle", "label": "Epistaxis (Nosebleeds)?", "required": False},
                    {"id": "lhb_bruising", "type": "toggle", "label": "Easy Bruising?", "required": False}
                ]
            },
            {
                "title": "Associated Symptoms - GI & Constitutional",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_bowel_change", "type": "toggle", "label": "Change in Bowel Habit?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Change in bowel habit with iron deficiency anaemia is a RED FLAG for colorectal cancer. Urgent GI referral.", "red_flag_negative": "No change in bowel habit."},
                    {"id": "lhb_abdo_pain", "type": "toggle", "label": "Abdominal Pain?", "required": False},
                    {"id": "lhb_dyspepsia", "type": "toggle", "label": "Dyspepsia/Indigestion?", "required": False},
                    {"id": "lhb_nausea_vomiting", "type": "toggle", "label": "Nausea/Vomiting?", "required": False},
                    {"id": "lhb_dysphagia", "type": "toggle", "label": "Dysphagia (Difficulty Swallowing)?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysphagia with iron deficiency anaemia may indicate oesophageal cancer or Plummer-Vinson syndrome.", "red_flag_negative": "No dysphagia."},
                    {"id": "lhb_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss with anaemia is a RED FLAG for malignancy. Urgent investigation required.", "red_flag_negative": "No weight loss."},
                    {"id": "lhb_appetite", "type": "toggle", "label": "Reduced Appetite?", "required": False},
                    {"id": "lhb_fever", "type": "toggle", "label": "Fever?", "required": False},
                    {"id": "lhb_night_sweats", "type": "toggle", "label": "Drenching Night Sweats?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Night sweats with anaemia may indicate haematological malignancy (lymphoma).", "red_flag_negative": "No night sweats."}
                ]
            },
            {
                "title": "Dietary & Lifestyle History",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_low_red_meat", "type": "toggle", "label": "Low Red Meat Intake?", "required": False},
                    {"id": "lhb_low_leafy_veg", "type": "toggle", "label": "Low Green Leafy Vegetable Intake?", "required": False},
                    {"id": "lhb_vegetarian", "type": "toggle", "label": "Vegetarian Diet?", "required": False},
                    {"id": "lhb_vegan", "type": "toggle", "label": "Vegan Diet?", "required": False},
                    {"id": "lhb_alcohol", "type": "single_select", "label": "Alcohol Consumption", "required": True, "options": ["None", "Within recommended limits (<17 units/week)", "Excessive (≥17 units/week)", "Heavy/alcohol dependence"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol excess can cause macrocytic anaemia, GI bleeding, liver disease, and nutritional deficiencies.", "red_flag_negative": ""},
                    {"id": "lhb_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never smoked", "Ex-smoker", "Current smoker"]},
                    {"id": "lhb_occupational", "type": "toggle", "label": "Occupational Exposure to Toxins/Chemicals?", "required": False}
                ]
            },
            {
                "title": "Past Medical History",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_pmh_none", "type": "toggle", "label": "No Significant PMHx?", "required": False},
                    {"id": "lhb_ckd", "type": "toggle", "label": "Chronic Kidney Disease?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: CKD is a common cause of anaemia of chronic disease. May require nephrology input and erythropoietin.", "red_flag_negative": "No CKD."},
                    {"id": "lhb_ra", "type": "toggle", "label": "Rheumatoid Arthritis?", "required": False},
                    {"id": "lhb_ibd", "type": "toggle", "label": "Inflammatory Bowel Disease?", "required": False},
                    {"id": "lhb_coeliac", "type": "toggle", "label": "Coeliac Disease?", "required": False},
                    {"id": "lhb_malignancy", "type": "toggle", "label": "Known Malignancy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Known malignancy with new anaemia requires urgent oncology review for possible disease progression or treatment-related anaemia.", "red_flag_negative": "No known malignancy."},
                    {"id": "lhb_previous_anaemia", "type": "toggle", "label": "Previous Anaemia?", "required": False},
                    {"id": "lhb_gi_surgery", "type": "toggle", "label": "Gastrointestinal Surgery? (e.g., gastrectomy, bowel resection)", "required": False},
                    {"id": "lhb_peptic_ulcer", "type": "toggle", "label": "History of Peptic Ulcer Disease?", "required": False},
                    {"id": "lhb_family_history", "type": "toggle", "label": "Family History of Anaemia/Haematological Disorders?", "required": False}
                ]
            },
            {
                "title": "Medication History",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_nsaids", "type": "toggle", "label": "Taking NSAIDs? (e.g., Ibuprofen, Naproxen, Diclofenac)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: NSAIDs can cause GI bleeding and iron deficiency anaemia. Review need for PPI cover and consider stopping.", "red_flag_negative": "Not taking NSAIDs."},
                    {"id": "lhb_aspirin", "type": "toggle", "label": "Taking Aspirin?", "required": True},
                    {"id": "lhb_anticoagulants", "type": "toggle", "label": "Taking Anticoagulants? (e.g., Warfarin, Rivaroxaban, Apixaban)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Anticoagulants increase risk of GI bleeding and iron deficiency. Check coagulation and assess for occult blood loss.", "red_flag_negative": "Not taking anticoagulants."},
                    {"id": "lhb_antiplatelets", "type": "toggle", "label": "Taking Antiplatelets? (e.g., Clopidogrel, Ticagrelor)", "required": False},
                    {"id": "lhb_ppis", "type": "toggle", "label": "Taking PPIs? (e.g., Omeprazole, Lansoprazole)", "required": False},
                    {"id": "lhb_methotrexate", "type": "toggle", "label": "Taking Methotrexate?", "required": False},
                    {"id": "lhb_chemo", "type": "toggle", "label": "Receiving Chemotherapy?", "required": False},
                    {"id": "lhb_other_meds", "type": "textarea", "label": "Other Current Medications", "required": False, "placeholder": "List all medications including OTC and supplements..."}
                ]
            },
            {
                "title": "Physical Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "lhb_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well-appearing", "Pale", "Ill-appearing", "Alert and Oriented", "Comfortable", "Lethargic", "Cachectic", "Jaundiced"]},
                    {"id": "lhb_conjunctival_pallor", "type": "toggle", "label": "Conjunctival Pallor?", "required": False},
                    {"id": "lhb_koilonychia", "type": "toggle", "label": "Koilonychia (Spoon Nails)?", "required": False},
                    {"id": "lhb_glossitis", "type": "toggle", "label": "Glossitis?", "required": False},
                    {"id": "lhb_angular_cheilitis", "type": "toggle", "label": "Angular Cheilitis?", "required": False},
                    {"id": "lhb_lymphadenopathy", "type": "toggle", "label": "Lymphadenopathy?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy with anaemia may indicate haematological malignancy.", "red_flag_negative": "No lymphadenopathy."},
                    {"id": "lhb_jaundice", "type": "toggle", "label": "Jaundice?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Jaundice with anaemia suggests haemolysis or liver disease.", "red_flag_negative": "No jaundice."},
                    {"id": "lhb_petechiae", "type": "toggle", "label": "Petechiae/Ecchymoses?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Petechiae with anaemia suggests thrombocytopenia or bone marrow failure. Urgent haematology assessment.", "red_flag_negative": "No petechiae."},
                    {"id": "lhb_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 120"},
                    {"id": "lhb_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 75"},
                    {"id": "lhb_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 92", "is_red_flag": True, "red_flag_positive": "RED FLAG: Tachycardia with anaemia may indicate haemodynamic compensation. Assess for cardiac compromise.", "red_flag_negative": ""},
                    {"id": "lhb_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 18"},
                    {"id": "lhb_o2", "type": "number", "label": "SpO2 (%)", "required": True, "placeholder": "e.g., 96"},
                    {"id": "lhb_temp", "type": "number", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 36.5"},
                    {"id": "lhb_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 26"},
                    {"id": "lhb_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["S1+S2 Audible, No Murmur", "Murmur Present (possible flow murmur)", "Signs of Heart Failure", "Peripheral Oedema"]},
                    {"id": "lhb_lungs", "type": "single_select", "label": "Lung Examination", "required": True, "options": ["Clear, Equal Air Entry Bilaterally, Vesicular BS", "Crackles (possible heart failure)", "Wheeze", "Reduced Air Entry"]},
                    {"id": "lhb_abdomen", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, Non-tender, Non-distended", "Tenderness Present", "Organomegaly", "Abdominal Mass", "Ascites"]},
                    {"id": "lhb_pr_exam", "type": "toggle", "label": "PR Examination Performed?", "required": False},
                    {"id": "lhb_pr_findings", "type": "textarea", "label": "PR Examination Findings", "required": False, "placeholder": "Describe any masses, blood, melaena, prostate..."},
                    {"id": "lhb_urinalysis_exam", "type": "single_select", "label": "Urinalysis Performed", "required": False, "options": ["Normal", "Blood +", "Blood ++", "Blood +++", "Protein +", "Glucose +", "Not done"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Iron Deficiency Anaemia",
                    "Anaemia of Chronic Disease",
                    "Vitamin B12 Deficiency",
                    "Folate Deficiency",
                    "Chronic Kidney Disease",
                    "Gastrointestinal Blood Loss",
                    "Colorectal Cancer",
                    "Gastric Cancer",
                    "Peptic Ulcer Disease",
                    "Coeliac Disease",
                    "Inflammatory Bowel Disease",
                    "Haematological Malignancy (Leukaemia, Lymphoma)",
                    "Multiple Myeloma",
                    "Myelodysplastic Syndrome",
                    "Haemolytic Anaemia",
                    "Bone Marrow Failure",
                    "Hypothyroidism",
                    "Liver Disease",
                    "Alcohol-Related Anaemia",
                    "Aplastic Anaemia",
                    "Sickle Cell Disease/Thalassaemia",
                    "Medication-Induced Anaemia"
                ],
                "questions": [
                    {"id": "lhb_diagnosis", "type": "textarea", "label": "Working Diagnosis / Impression", "required": True, "placeholder": "e.g., Iron deficiency anaemia likely secondary to GI blood loss. Microcytic anaemia with low ferritin..."},
                    {"id": "lhb_diagnosis_certainty", "type": "single_select", "label": "Diagnostic Certainty", "required": True, "options": ["Likely", "Suspected", "Possible", "Uncertain - requires further investigation"]},
                    {"id": "lhb_redflags_assessed", "type": "toggle", "label": "Red Flags Specifically Assessed and Excluded?", "required": True}
                ]
            },
            {
                "title": "Plan - Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "lhb_bloods_repeat", "type": "toggle", "label": "Repeat Bloods Ordered?", "required": True},
                    {"id": "lhb_bloods_list", "type": "multi_select", "label": "Blood Tests Ordered", "required": False, "options": ["FBC + Blood Film", "Reticulocyte Count", "Iron Studies (Ferritin, Iron, Transferrin Saturation)", "B12 and Folate", "U&E, Creatinine, eGFR", "LFTs", "TFTs", "ESR/CRP", "Coeliac Screen (tTG-IgA)", "Hb Electrophoresis", "LDH, Haptoglobin, Bilirubin (haemolysis screen)", "Serum Protein Electrophoresis (SPEP)", "PSA"]},
                    {"id": "lhb_urine_tests", "type": "multi_select", "label": "Urine Tests Ordered", "required": False, "options": ["Urinalysis", "Urine Microscopy", "Urine Culture", "Urine Bence Jones Protein"]},
                    {"id": "lhb_fit_test", "type": "toggle", "label": "FIT Test Ordered?", "required": False},
                    {"id": "lhb_ecg", "type": "toggle", "label": "ECG Requested?", "required": False},
                    {"id": "lhb_cxr", "type": "toggle", "label": "Chest X-Ray Requested?", "required": False},
                    {"id": "lhb_gastroscopy", "type": "toggle", "label": "Upper GI Endoscopy Requested?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Upper GI endoscopy indicated for iron deficiency anaemia to exclude gastric cancer and peptic ulcer disease.", "red_flag_negative": ""},
                    {"id": "lhb_colonoscopy", "type": "toggle", "label": "Colonoscopy Requested?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Colonoscopy indicated for iron deficiency anaemia, especially age >50 or with GI symptoms, to exclude colorectal cancer.", "red_flag_negative": ""},
                    {"id": "lhb_ct_imaging", "type": "toggle", "label": "CT Imaging Requested?", "required": False},
                    {"id": "lhb_bone_marrow", "type": "toggle", "label": "Bone Marrow Biopsy Indicated?", "required": False},
                    {"id": "lhb_other_tests", "type": "textarea", "label": "Other Investigations", "required": False, "placeholder": "Additional tests or imaging..."}
                ]
            },
            {
                "title": "Plan - Management",
                "section_type": "plan",
                "safety_netting": "Return immediately if you develop worsening fatigue, shortness of breath, chest pain, dizziness or syncope (collapse). Return if you notice PR bleeding, black tarry stools (melaena), vomiting blood, blood in urine, or coughing up blood. Return if you experience unintentional weight loss, drenching night sweats, or any new concerning symptoms. If iron prescribed - take on empty stomach if tolerated, avoid tea/coffee/calcium around administration, and consider vitamin C (orange juice) to improve absorption. Continue iron treatment for 3 months after Hb normalises to replenish iron stores. Follow-up in specified timeframe for repeat bloods.",
                "questions": [
                    {"id": "lhb_dietary_advice", "type": "toggle", "label": "Dietary Advice Given? (Increase iron-rich foods)", "required": False},
                    {"id": "lhb_dietary_details", "type": "textarea", "label": "Dietary Advice Details", "required": False, "placeholder": "e.g., Increase red meat, green leafy vegetables, pulses, legumes, iron-fortified cereals..."},
                    {"id": "lhb_iron_replacement", "type": "single_select", "label": "Iron Replacement Prescribed", "required": False, "options": [
                        "None",
                        "Galfer® (Ferrous Fumarate 322mg) 1 tablet OD",
                        "Galfer FA® (Ferrous Fumarate + Folic Acid) 1 tablet OD",
                        "Galfer Liquid®",
                        "Ferrograd® (Ferrous Sulphate 325mg) 1 tablet OD"
                    ]},
                    {"id": "lhb_iron_advice", "type": "textarea", "label": "Iron Administration Advice Given", "required": False, "placeholder": "Advice given:\n- Take once daily or alternate days\n- Take on empty stomach if tolerated\n- Avoid tea, coffee and calcium around administration\n- Consider vitamin C to improve absorption\n- GMS reimbursable options: Galfer, Galfer FA, Galfer Liquid, Ferrograd\n- Non-GMS: Ferrograd C, Active Iron"},
                    {"id": "lhb_b12_replacement", "type": "toggle", "label": "Vitamin B12 Replacement Prescribed?", "required": False},
                    {"id": "lhb_b12_details", "type": "textarea", "label": "B12 Replacement Details", "required": False, "placeholder": "e.g., Hydroxocobalamin 1mg IM alternate days for 2 weeks then 3 monthly..."},
                    {"id": "lhb_folate_replacement", "type": "toggle", "label": "Folate Replacement Prescribed?", "required": False},
                    {"id": "lhb_folate_details", "type": "textarea", "label": "Folate Replacement Details", "required": False, "placeholder": "e.g., Folic acid 5mg OD for 4 months..."},
                    {"id": "lhb_stop_nsaids", "type": "toggle", "label": "Stop/Review NSAIDs?", "required": False},
                    {"id": "lhb_stop_anticoagulants", "type": "toggle", "label": "Stop/Review Anticoagulants?", "required": False},
                    {"id": "lhb_ppi_prescribed", "type": "toggle", "label": "PPI Prescribed for GI Protection?", "required": False},
                    {"id": "lhb_other_management", "type": "textarea", "label": "Other Management", "required": False, "placeholder": "Additional medications, lifestyle modifications, treat underlying cause..."}
                ]
            },
            {
                "title": "Referral",
                "section_type": "plan",
                "questions": [
                    {"id": "lhb_urgent_referral", "type": "toggle", "label": "Urgent Hospital Referral Required?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Urgent referral indicated if: Hb <8 g/dL, symptomatic anaemia, suspected GI malignancy, ongoing bleeding, haemodynamic instability, suspected haematological malignancy.", "red_flag_negative": ""},
                    {"id": "lhb_urgent_reason", "type": "textarea", "label": "Reason for Urgent Referral", "required": False, "placeholder": "Document specific criteria for urgent referral..."},
                    {"id": "lhb_gastro_referral", "type": "toggle", "label": "Refer to Gastroenterology?", "required": False},
                    {"id": "lhb_haematology_referral", "type": "toggle", "label": "Refer to Haematology?", "required": False},
                    {"id": "lhb_oncology_referral", "type": "toggle", "label": "Refer to Oncology?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Urgent oncology referral if malignancy suspected. 2-week wait referral for suspected lower GI cancer if: age ≥40 with unexplained weight loss and abdominal pain, or age ≥50 with unexplained rectal bleeding, or age ≥60 with iron deficiency anaemia or change in bowel habit.", "red_flag_negative": ""},
                    {"id": "lhb_nephro_referral", "type": "toggle", "label": "Refer to Nephrology?", "required": False},
                    {"id": "lhb_dietitian_referral", "type": "toggle", "label": "Refer to Dietitian?", "required": False}
                ]
            },
            {
                "title": "Follow-Up & Monitoring",
                "section_type": "plan",
                "questions": [
                    {"id": "lhb_followup_fbc_value", "type": "number", "label": "Repeat FBC in (Number)", "required": True, "placeholder": "e.g., 4"},
                    {"id": "lhb_followup_fbc_unit", "type": "single_select", "label": "FBC Follow-up Unit", "required": True, "options": ["days", "weeks", "months"]},
                    {"id": "lhb_followup_ferritin_value", "type": "number", "label": "Repeat Ferritin in (Number)", "required": False, "placeholder": "e.g., 8"},
                    {"id": "lhb_followup_ferritin_unit", "type": "single_select", "label": "Ferritin Follow-up Unit", "required": False, "options": ["weeks", "months"]},
                    {"id": "lhb_iron_duration", "type": "toggle", "label": "Continue Iron for 3 Months After Hb Normalises?", "required": True},
                    {"id": "lhb_monitoring_plan", "type": "textarea", "label": "Long-term Monitoring Plan", "required": False, "placeholder": "e.g., Monitor FBC and ferritin every 3-6 months once stable. Annual review if chronic anaemia. Repeat iron studies after completing course."},
                    {"id": "lhb_followup_notes", "type": "textarea", "label": "Additional Follow-up Notes", "required": False, "placeholder": "e.g., Safety netting discussed. Patient understands to return if symptoms worsen. Copy of blood results given..."}
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
    seed_low_hb_male()