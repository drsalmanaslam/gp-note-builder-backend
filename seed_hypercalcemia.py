from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hypercalcemia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Hypercalcemia Assessment",
        "description": "Comprehensive assessment for hypercalcemia in general practice including differential diagnosis, investigation, and management plan with referral criteria.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "hcal_gender", "type": "single_select", "label": "Gender", "required": True, "options": ["Male", "Female", "Trans Man", "Trans Woman"]},
                    {"id": "hcal_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 55"},
                    {"id": "hcal_presentation", "type": "single_select", "label": "Presents For", "required": True, "options": ["New hypercalcemia (incidental finding)", "New hypercalcemia (symptomatic)", "Known hypercalcemia - follow-up", "Known hypercalcemia - worsening"]},
                    {"id": "hcal_presentation_detail", "type": "textarea", "label": "Presentation Details", "required": False, "placeholder": "Describe presenting complaint and circumstances leading to calcium check..."}
                ]
            },
            {
                "title": "Lab Results",
                "section_type": "history",
                "questions": [
                    {"id": "hcal_adj_ca", "type": "number", "label": "Albumin-Adjusted Calcium (mmol/L)", "required": True, "placeholder": "e.g., 2.85", "is_red_flag": True, "red_flag_positive": "RED FLAG: Adjusted calcium >3.00 mmol/L requires urgent assessment. If >3.40 mmol/L, refer to hospital immediately.", "red_flag_negative": ""},
                    {"id": "hcal_severity", "type": "single_select", "label": "Hypercalcemia Severity", "required": True, "options": ["Mild (2.65-3.00 mmol/L)", "Moderate (3.00-3.40 mmol/L)", "Severe (>3.40 mmol/L)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe hypercalcemia >3.40 mmol/L requires emergency hospital admission. Moderate hypercalcemia 3.00-3.40 mmol/L requires urgent endocrinology referral.", "red_flag_negative": ""},
                    {"id": "hcal_phosphate", "type": "number", "label": "Phosphate (mmol/L)", "required": False, "placeholder": "e.g., 0.8 (Normal: 0.8-1.5)"},
                    {"id": "hcal_albumin", "type": "number", "label": "Albumin (g/L)", "required": True, "placeholder": "e.g., 42 (Normal: 35-50)"},
                    {"id": "hcal_creatinine", "type": "number", "label": "Creatinine (µmol/L)", "required": True, "placeholder": "e.g., 88 (Normal: 60-110)"},
                    {"id": "hcal_egfr", "type": "number", "label": "eGFR (ml/min/1.73m²)", "required": True, "placeholder": "e.g., 72", "is_red_flag": True, "red_flag_positive": "RED FLAG: eGFR 30-44 (CKD 3b) with hypercalcemia requires endocrinology referral.", "red_flag_negative": ""},
                    {"id": "hcal_pth", "type": "number", "label": "PTH (pmol/L)", "required": False, "placeholder": "e.g., 12.5 (Normal: 1.6-6.9)"},
                    {"id": "hcal_vit_d", "type": "number", "label": "Vitamin D (nmol/L)", "required": False, "placeholder": "e.g., 85 (Normal: >50)"},
                    {"id": "hcal_tsh", "type": "number", "label": "TSH (mIU/L)", "required": False, "placeholder": "e.g., 2.1 (Normal: 0.4-4.0)"},
                    {"id": "hcal_urinalysis", "type": "single_select", "label": "Urinalysis", "required": False, "options": ["Normal", "Haematuria", "Proteinuria", "Calcium oxalate crystals", "Not done"]},
                    {"id": "hcal_other_labs", "type": "textarea", "label": "Other Lab Results", "required": False, "placeholder": "Cortisol, PRL, β-hCG, serum protein electrophoresis, 24h urine calcium..."}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hcal_bone_pain", "type": "toggle", "label": "Bone Pain?", "required": False},
                    {"id": "hcal_abdo_pain", "type": "toggle", "label": "Abdominal Pain?", "required": False},
                    {"id": "hcal_thirst", "type": "toggle", "label": "Increased Thirst (Polydipsia)?", "required": False},
                    {"id": "hcal_polyuria", "type": "toggle", "label": "Increased Urination (Polyuria)?", "required": False},
                    {"id": "hcal_fatigue", "type": "toggle", "label": "Fatigue?", "required": False},
                    {"id": "hcal_muscle_weakness", "type": "toggle", "label": "Muscle Weakness?", "required": False},
                    {"id": "hcal_nausea_vomiting", "type": "toggle", "label": "Nausea/Vomiting?", "required": False},
                    {"id": "hcal_constipation", "type": "toggle", "label": "Constipation?", "required": False},
                    {"id": "hcal_confusion", "type": "toggle", "label": "Confusion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Confusion with hypercalcemia indicates severe hypercalcemia. Requires urgent hospital assessment.", "red_flag_negative": "No confusion."},
                    {"id": "hcal_depression", "type": "toggle", "label": "Depression/Low Mood?", "required": False},
                    {"id": "hcal_dyspepsia", "type": "toggle", "label": "Dyspepsia?", "required": False},
                    {"id": "hcal_kidney_stones", "type": "toggle", "label": "History of Kidney Stones?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Renal stones with hypercalcemia are a referral criterion for endocrinology.", "red_flag_negative": "No kidney stones."},
                    {"id": "hcal_cardiac", "type": "toggle", "label": "Palpitations or Cardiac Symptoms?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypercalcemia can cause shortened QT interval and arrhythmias. ECG required.", "red_flag_negative": "No cardiac symptoms."}
                ]
            },
            {
                "title": "Risk Factors & Past Medical History",
                "section_type": "history",
                "questions": [
                    {"id": "hcal_pmh_none", "type": "toggle", "label": "No Significant PMHx?", "required": False},
                    {"id": "hcal_hyperparathyroidism", "type": "toggle", "label": "Known Hyperparathyroidism?", "required": False},
                    {"id": "hcal_kidney_disease", "type": "toggle", "label": "Chronic Kidney Disease?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: CKD with hypercalcemia requires nephrology input. eGFR 30-44 with hypercalcemia requires endocrinology referral.", "red_flag_negative": "No kidney disease."},
                    {"id": "hcal_cancer", "type": "toggle", "label": "Known or Suspected Malignancy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Malignancy is the second most common cause of hypercalcemia. Consider lung, breast, multiple myeloma, renal cell carcinoma. Urgent oncology workup required.", "red_flag_negative": "No known malignancy."},
                    {"id": "hcal_cancer_type", "type": "textarea", "label": "Cancer Details (if applicable)", "required": False, "placeholder": "Type, stage, current treatment..."},
                    {"id": "hcal_sarcoidosis", "type": "toggle", "label": "Sarcoidosis?", "required": False},
                    {"id": "hcal_tb", "type": "toggle", "label": "Tuberculosis (History or Exposure)?", "required": False},
                    {"id": "hcal_thyroid", "type": "toggle", "label": "Thyroid Disease?", "required": False},
                    {"id": "hcal_osteoporosis", "type": "toggle", "label": "History of Osteoporosis or Fragility Fracture?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: History of osteoporosis or fracture with hypercalcemia requires endocrinology referral.", "red_flag_negative": "No osteoporosis or fractures."},
                    {"id": "hcal_immobilization", "type": "toggle", "label": "Prolonged Immobilization?", "required": False},
                    {"id": "hcal_diet_calcium", "type": "toggle", "label": "High-Calcium Diet?", "required": False},
                    {"id": "hcal_dehydration", "type": "toggle", "label": "Recent Dehydration?", "required": False},
                    {"id": "hcal_family_history", "type": "toggle", "label": "Family History of Hypercalcemia or MEN Syndrome?", "required": False}
                ]
            },
            {
                "title": "Medications & Supplements",
                "section_type": "history",
                "questions": [
                    {"id": "hcal_vit_d_supp", "type": "toggle", "label": "Taking Vitamin D Supplements?", "required": True},
                    {"id": "hcal_vit_d_dose", "type": "text", "label": "Vitamin D Dose (if taking)", "required": False, "placeholder": "e.g., 2000 IU daily"},
                    {"id": "hcal_calcium_supp", "type": "toggle", "label": "Taking Calcium Supplements?", "required": True},
                    {"id": "hcal_calcium_dose", "type": "text", "label": "Calcium Dose (if taking)", "required": False, "placeholder": "e.g., 500mg BD"},
                    {"id": "hcal_thiazide", "type": "toggle", "label": "Taking Thiazide Diuretics? (e.g., Bendroflumethiazide, Indapamide)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Thiazide diuretics can cause or worsen hypercalcemia. Stop immediately and recheck calcium.", "red_flag_negative": "Not taking thiazides."},
                    {"id": "hcal_lithium", "type": "toggle", "label": "Taking Lithium?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lithium can cause hyperparathyroidism and hypercalcemia. Check lithium levels and PTH.", "red_flag_negative": "Not taking lithium."},
                    {"id": "hcal_vit_a", "type": "toggle", "label": "Taking Vitamin A Supplements?", "required": False},
                    {"id": "hcal_antacids", "type": "toggle", "label": "Taking Calcium-Containing Antacids? (e.g., Rennie, Tums)", "required": False},
                    {"id": "hcal_digoxin", "type": "toggle", "label": "Taking Digoxin?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypercalcemia potentiates digoxin toxicity. Stop digoxin and seek urgent cardiology advice.", "red_flag_negative": "Not taking digoxin."},
                    {"id": "hcal_tamoxifen", "type": "toggle", "label": "Taking Tamoxifen?", "required": False},
                    {"id": "hcal_other_meds", "type": "textarea", "label": "Other Current Medications", "required": False, "placeholder": "List all medications including OTC and supplements..."}
                ]
            },
            {
                "title": "Physical Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hcal_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well-appearing", "Ill-appearing", "In Apparent Distress", "Alert and Oriented", "Comfortable", "In Pain", "Lethargic", "Diaphoretic", "Pale", "Toxic"]},
                    {"id": "hcal_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 130"},
                    {"id": "hcal_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 80"},
                    {"id": "hcal_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 78"},
                    {"id": "hcal_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 16"},
                    {"id": "hcal_o2", "type": "number", "label": "SpO2 (%)", "required": True, "placeholder": "e.g., 98"},
                    {"id": "hcal_temp", "type": "number", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 36.6"},
                    {"id": "hcal_neck", "type": "single_select", "label": "Neck Examination", "required": False, "options": ["Normal", "Thyroid enlargement", "Thyroid nodule", "Lymphadenopathy", "Parotid swelling", "Not examined"]},
                    {"id": "hcal_heart", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["RRR, Normal S1+S2, No Murmur", "Irregular", "Regularly-Irregular", "Murmur Present", "Friction Rub", "Gallop"]},
                    {"id": "hcal_lungs", "type": "single_select", "label": "Lung Examination", "required": True, "options": ["Clear, Vesicular BS, No Added Sounds", "Crackles/Crepitations", "Wheeze", "Rhonchi", "Reduced Air Entry", "Bronchial Breathing"]},
                    {"id": "hcal_abdomen", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, Non-tender, Non-distended", "Tenderness - Epigastric", "Tenderness - RUQ", "Tenderness - LUQ", "Tenderness - Suprapubic", "Tenderness - Generalised", "Distended", "Mass Palpable", "Organomegaly"]},
                    {"id": "hcal_extremities", "type": "single_select", "label": "Extremities", "required": False, "options": ["Normal - Warm, CRT <3 sec, Pulses Normal", "Edema Present", "CRT >3 sec", "Reduced Pulses", "Clubbing", "Bone Tenderness"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Primary Hyperparathyroidism",
                    "Malignancy (Lung Cancer, Breast Cancer, Multiple Myeloma, Renal Cell Carcinoma)",
                    "Granulomatous Disease (Sarcoidosis, Tuberculosis)",
                    "Medication-Induced (Thiazide Diuretics, Lithium, Vitamin A, Vitamin D Intoxication)",
                    "Calcium Supplementation",
                    "Thyrotoxicosis",
                    "Familial Hypocalciuric Hypercalcemia (FHH)",
                    "Adrenal Insufficiency",
                    "Milk-Alkali Syndrome",
                    "Prolonged Immobilization",
                    "Renal Failure (Secondary/Tertiary Hyperparathyroidism)",
                    "Hypothyroidism",
                    "Acromegaly",
                    "Pheochromocytoma",
                    "Adrenal Cortical Carcinoma",
                    "Dehydration",
                    "Parenteral Nutrition",
                    "Idiopathic Hypercalcemia of Infancy"
                ],
                "questions": [
                    {"id": "hcal_diagnosis", "type": "textarea", "label": "Working Diagnosis / Impression", "required": True, "placeholder": "e.g., Likely primary hyperparathyroidism given elevated PTH with hypercalcemia and normal renal function..."},
                    {"id": "hcal_diagnosis_certainty", "type": "single_select", "label": "Diagnostic Certainty", "required": True, "options": ["Likely", "Suspected", "Possible", "Uncertain - requires further investigation"]},
                    {"id": "hcal_redflags_assessed", "type": "toggle", "label": "Red Flags Specifically Assessed and Excluded?", "required": True}
                ]
            },
            {
                "title": "Plan - Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "hcal_bloods_repeat", "type": "toggle", "label": "Repeat Bloods Ordered?", "required": True},
                    {"id": "hcal_bloods_list", "type": "multi_select", "label": "Blood Tests Ordered", "required": False, "options": ["FBC", "U&E, Creatinine, eGFR", "Glucose", "Albumin", "Adjusted Calcium", "Phosphate", "PTH", "Vitamin D (25-OH)", "TSH", "Cortisol", "Prolactin", "β-hCG", "Serum Protein Electrophoresis", "Serum Free Light Chains"]},
                    {"id": "hcal_urine_tests", "type": "multi_select", "label": "Urine Tests Ordered", "required": False, "options": ["Urinalysis", "Urine Calcium", "Urine Creatinine", "24-Hour Urine Calcium", "Urine Protein Electrophoresis"]},
                    {"id": "hcal_ecg", "type": "toggle", "label": "ECG Requested? (Check for Short QT)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ECG essential to check for shortened QT interval which predisposes to arrhythmias.", "red_flag_negative": ""},
                    {"id": "hcal_cxr", "type": "toggle", "label": "Chest X-Ray Requested?", "required": False},
                    {"id": "hcal_abdo_uss", "type": "toggle", "label": "Abdominal Ultrasound Requested?", "required": False},
                    {"id": "hcal_dexa", "type": "toggle", "label": "Bone Mineral Density (DEXA) Scan?", "required": False},
                    {"id": "hcal_other_imaging", "type": "textarea", "label": "Other Imaging", "required": False, "placeholder": "e.g., Renal tract ultrasound, Sestamibi scan, CT CAP..."}
                ]
            },
            {
                "title": "Plan - Management",
                "section_type": "plan",
                "safety_netting": "If calcium >3.00 mmol/L or symptomatic with confusion, severe bone pain, abdominal pain, or cardiac symptoms - attend Emergency Department immediately. Return if symptoms worsen or if new symptoms develop such as bone pain, confusion, abdominal pain, palpitations, or worsening fatigue. Ensure adequate hydration (2-3 litres water daily unless fluid restricted). Avoid high-calcium foods (dairy, fortified products). Stop any calcium or vitamin D supplements immediately.",
                "questions": [
                    {"id": "hcal_hydration", "type": "toggle", "label": "Encourage Hydration Advised? (2-3L daily)", "required": True},
                    {"id": "hcal_dietary_advice", "type": "toggle", "label": "Dietary Counselling Given? (Low calcium, low vitamin D, low phosphate diet)", "required": False},
                    {"id": "hcal_stop_thiazide", "type": "toggle", "label": "Stop Thiazide Diuretics?", "required": False},
                    {"id": "hcal_stop_lithium", "type": "toggle", "label": "Stop Lithium? (Discuss with psychiatrist)", "required": False},
                    {"id": "hcal_stop_vit_a", "type": "toggle", "label": "Stop Vitamin A Supplements?", "required": False},
                    {"id": "hcal_stop_vit_d", "type": "toggle", "label": "Stop Vitamin D Supplements?", "required": False},
                    {"id": "hcal_stop_calcium", "type": "toggle", "label": "Stop Calcium Supplements?", "required": False},
                    {"id": "hcal_stop_digoxin", "type": "toggle", "label": "Stop Digoxin?", "required": False},
                    {"id": "hcal_stop_antacids", "type": "toggle", "label": "Stop Calcium-Containing Antacids?", "required": False},
                    {"id": "hcal_stop_tamoxifen", "type": "toggle", "label": "Stop Tamoxifen? (Discuss with oncology)", "required": False},
                    {"id": "hcal_bisphosphonate", "type": "single_select", "label": "Bisphosphonate Prescribed", "required": False, "options": ["None", "Alendronate 70mg PO weekly (advise about administration)", "Pamidronate IV (hospital only)"]},
                    {"id": "hcal_calcitonin", "type": "toggle", "label": "Calcitonin 200IU SC or IM OD Prescribed?", "required": False},
                    {"id": "hcal_cinacalcet", "type": "single_select", "label": "Cinacalcet Prescribed", "required": False, "options": ["None", "Cinacalcet 30mg OD", "Cinacalcet 60mg OD", "Cinacalcet 90mg OD"]},
                    {"id": "hcal_phosphate_binder", "type": "single_select", "label": "Phosphate Binder Prescribed", "required": False, "options": ["None", "Calcium Carbonate 500mg PO TDS with meals", "Sevelamer 800mg OD", "Lanthanum 500mg PO TDS with meals"]},
                    {"id": "hcal_vit_d_analogue", "type": "single_select", "label": "Vitamin D Analogue Prescribed", "required": False, "options": ["None", "Calcitriol 0.25mcg PO OD", "Paricalcitol 1mcg OD PO"]},
                    {"id": "hcal_furosemide", "type": "single_select", "label": "Furosemide Prescribed", "required": False, "options": ["None", "Furosemide 20mg OD", "Furosemide 40mg OD"]},
                    {"id": "hcal_other_management", "type": "textarea", "label": "Other Management", "required": False, "placeholder": "Additional medications, lifestyle advice..."}
                ]
            },
            {
                "title": "Referral & Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "hcal_hospital_referral", "type": "toggle", "label": "Refer to Hospital? (Calcium >3.00 mmol/L)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Calcium >3.00 mmol/L requires hospital assessment. If >3.40 mmol/L, refer immediately as emergency.", "red_flag_negative": ""},
                    {"id": "hcal_endo_referral", "type": "toggle", "label": "Refer to Endocrinology?", "required": True},
                    {"id": "hcal_endo_criteria", "type": "textarea", "label": "Endocrinology Referral Criteria Met", "required": False, "placeholder": "Document which criteria met:\n- Calcium ≥2.79 mmol/L\n- eGFR 30-44 (CKD 3b)\n- Symptomatic (including renal stones)\n- History of osteoporosis or fracture\n\nIf referral indicated: Arrange urinary calcium excretion index prior to appointment.\nIf referral not indicated: Manage in primary care. Repeat calcium in 3 months. If stable, monitor annually. Every 2-3 years consider 3-site DEXA scan."},
                    {"id": "hcal_nephro_referral", "type": "toggle", "label": "Refer to Nephrologist?", "required": False},
                    {"id": "hcal_oncology_referral", "type": "toggle", "label": "Refer to Oncologist?", "required": False},
                    {"id": "hcal_dietitian_referral", "type": "toggle", "label": "Refer to Dietitian?", "required": False},
                    {"id": "hcal_followup_value", "type": "number", "label": "Repeat Calcium in (Number)", "required": True, "placeholder": "e.g., 4"},
                    {"id": "hcal_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["days", "weeks", "months"]},
                    {"id": "hcal_monitoring_plan", "type": "textarea", "label": "Long-term Monitoring Plan", "required": False, "placeholder": "e.g., If calcium stable on 3-month repeat, monitor annually.\nIf referral criteria met at later review - refer to endocrinology.\nEvery 2-3 years consider 3-site DEXA scan.\nAnnual renal function and calcium."},
                    {"id": "hcal_followup_notes", "type": "textarea", "label": "Additional Follow-up Notes", "required": False, "placeholder": "e.g., Patient advised to return if bone pain, confusion, abdominal pain, palpitations, or worsening fatigue..."}
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
    seed_hypercalcemia()