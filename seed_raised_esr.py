from app.database import SessionLocal
from app.models import User, Template, Category

def seed_raised_esr():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised ESR Assessment",
        "description": "Systematic assessment for raised ESR including targeted history to exclude serious pathology, investigation, and management plan with age-appropriate reference ranges.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "esr_gender", "type": "single_select", "label": "Gender", "required": True, "options": ["Male", "Female", "Trans Man", "Trans Woman"]},
                    {"id": "esr_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 55"},
                    {"id": "esr_presentation", "type": "single_select", "label": "Presents For", "required": True, "options": ["New raised ESR (incidental)", "New raised ESR (symptomatic)", "Known raised ESR - follow-up", "Known raised ESR - worsening"]}
                ]
            },
            {
                "title": "Lab Results",
                "section_type": "history",
                "questions": [
                    {"id": "esr_value", "type": "number", "label": "ESR (mm/hr)", "required": True, "placeholder": "e.g., 45"},
                    {"id": "esr_max_normal", "type": "text", "label": "Expected Maximum Normal ESR for Age/Gender", "required": False, "placeholder": "Male: Age÷2 = XX mm/hr\nFemale: (Age+10)÷2 = XX mm/hr"},
                    {"id": "esr_elevation", "type": "single_select", "label": "Degree of Elevation", "required": True, "options": ["Within normal range for age/gender", "Mildly elevated (<2x upper limit)", "Moderately elevated (2-4x upper limit)", "Markedly elevated (>4x upper limit)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Markedly elevated ESR >4x upper limit requires urgent investigation for malignancy, giant cell arteritis, infection, or autoimmune disease.", "red_flag_negative": ""},
                    {"id": "esr_crp", "type": "number", "label": "CRP (mg/L) - if available", "required": False, "placeholder": "e.g., 12 (NR: <5)"},
                    {"id": "esr_fbc", "type": "number", "label": "Haemoglobin (g/dL)", "required": False, "placeholder": "e.g., 13.5 (NR: 13.0-17.0 male / 11.5-16.0 female)"},
                    {"id": "esr_platelets", "type": "number", "label": "Platelets (×10⁹/L)", "required": False, "placeholder": "e.g., 350 (NR: 150-400)"},
                    {"id": "esr_wcc", "type": "number", "label": "WCC (×10⁹/L)", "required": False, "placeholder": "e.g., 7.2 (NR: 4-11)"},
                    {"id": "esr_creatinine", "type": "number", "label": "Creatinine (µmol/L)", "required": False, "placeholder": "e.g., 78 (NR: 60-110)"},
                    {"id": "esr_egfr", "type": "number", "label": "eGFR (ml/min/1.73m²)", "required": False, "placeholder": "e.g., 82", "is_red_flag": True, "red_flag_positive": "RED FLAG: Renal disease increases ESR. CKD requires nephrology assessment if eGFR <30.", "red_flag_negative": ""},
                    {"id": "esr_lfts", "type": "textarea", "label": "LFTs", "required": False, "placeholder": "e.g., ALT 28, AST 32, ALP 90, GGT 45, Bilirubin 10"},
                    {"id": "esr_other_labs", "type": "textarea", "label": "Other Lab Results", "required": False, "placeholder": "e.g., Ferritin, B12, Folate, TFTs, Serum Protein Electrophoresis..."}
                ]
            },
            {
                "title": "Constitutional Symptoms - Malignancy Screen",
                "section_type": "history",
                "questions": [
                    {"id": "esr_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss with raised ESR is a RED FLAG for malignancy. Urgent investigation required.", "red_flag_negative": "No weight loss - reassuring."},
                    {"id": "esr_night_sweats", "type": "toggle", "label": "Drenching Night Sweats?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Night sweats with raised ESR may indicate lymphoma, TB, or other malignancy.", "red_flag_negative": "No night sweats - reassuring."},
                    {"id": "esr_fever", "type": "toggle", "label": "Fever or Recurrent Fevers?", "required": False},
                    {"id": "esr_fatigue", "type": "toggle", "label": "Significant Fatigue/Malaise?", "required": False},
                    {"id": "esr_appetite", "type": "toggle", "label": "Reduced Appetite/Anorexia?", "required": False}
                ]
            },
            {
                "title": "Giant Cell Arteritis / Polymyalgia Rheumatica Screen",
                "section_type": "history",
                "questions": [
                    {"id": "esr_temporal_headache", "type": "toggle", "label": "Temporal Headache or Scalp Tenderness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Temporal headache with raised ESR is a RED FLAG for giant cell arteritis (GCA). Urgent ophthalmology/rheumatology referral and consider immediate steroids to prevent blindness.", "red_flag_negative": "No temporal headache - reassuring."},
                    {"id": "esr_jaw_claudication", "type": "toggle", "label": "Pain in Jaw When Chewing (Jaw Claudication)?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Jaw claudication is highly specific for giant cell arteritis. Urgent referral required.", "red_flag_negative": ""},
                    {"id": "esr_visual_disturbance", "type": "toggle", "label": "Visual Disturbance or Vision Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms with raised ESR suggest GCA with risk of permanent blindness. EMERGENCY - same-day ophthalmology assessment and high-dose steroids.", "red_flag_negative": "No visual disturbance - reassuring."},
                    {"id": "esr_pmr_shoulder", "type": "toggle", "label": "Bilateral Shoulder Pain/Stiffness? (PMR)", "required": False},
                    {"id": "esr_pmr_pelvic", "type": "toggle", "label": "Bilateral Pelvic/Hip Girdle Pain/Stiffness? (PMR)", "required": False},
                    {"id": "esr_pmr_morning", "type": "toggle", "label": "Prolonged Morning Stiffness >45 minutes?", "required": False},
                    {"id": "esr_pmr_age", "type": "toggle", "label": "Age >50 Years? (PMR/GCA typically >50)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >50 with raised ESR and bilateral shoulder/pelvic girdle pain is highly suggestive of PMR or GCA.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Infection Screen",
                "section_type": "history",
                "questions": [
                    {"id": "esr_cough", "type": "toggle", "label": "Persistent Cough? (TB/Sarcoidosis/Chest infection)", "required": False},
                    {"id": "esr_haemoptysis", "type": "toggle", "label": "Haemoptysis?", "required": False},
                    {"id": "esr_sinusitis", "type": "toggle", "label": "Chronic Sinusitis or Nasal Symptoms?", "required": False},
                    {"id": "esr_dental", "type": "toggle", "label": "Recent Dental Infection or Abscess?", "required": False},
                    {"id": "esr_urinary", "type": "toggle", "label": "Urinary Symptoms or Recurrent UTIs?", "required": False},
                    {"id": "esr_skin_infection", "type": "toggle", "label": "Skin Infections or Wounds?", "required": False},
                    {"id": "esr_tb_exposure", "type": "toggle", "label": "TB Exposure or Risk Factors?", "required": False},
                    {"id": "esr_recent_travel", "type": "textarea", "label": "Recent Travel History", "required": False, "placeholder": "Destination, duration, unwell during/after travel..."}
                ]
            },
            {
                "title": "Autoimmune / Inflammatory Screen",
                "section_type": "history",
                "questions": [
                    {"id": "esr_joint_pain", "type": "toggle", "label": "Joint Pain, Swelling, or Stiffness? (Rheumatoid Arthritis/SLE)", "required": False},
                    {"id": "esr_joint_details", "type": "textarea", "label": "Joint Symptoms Details", "required": False, "placeholder": "Which joints, symmetry, duration, morning stiffness..."},
                    {"id": "esr_malar_rash", "type": "toggle", "label": "Malar (Butterfly) Rash on Face? (SLE/Lupus)", "required": False},
                    {"id": "esr_photosensitivity", "type": "toggle", "label": "Photosensitivity or Other Rashes?", "required": False},
                    {"id": "esr_raynauds", "type": "toggle", "label": "Raynaud's Phenomenon?", "required": False},
                    {"id": "esr_dry_eyes_mouth", "type": "toggle", "label": "Dry Eyes or Dry Mouth? (Sjögren's Syndrome)", "required": False},
                    {"id": "esr_ibd_symptoms", "type": "toggle", "label": "Diarrhoea, Abdominal Pain, or Blood in Stool? (IBD)", "required": False}
                ]
            },
            {
                "title": "Other Systems Review",
                "section_type": "history",
                "questions": [
                    {"id": "esr_bowel_change", "type": "toggle", "label": "Change in Bowel Habit?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Change in bowel habit with raised ESR requires GI investigation for colorectal cancer or IBD.", "red_flag_negative": "No change in bowel habit - reassuring."},
                    {"id": "esr_breast_symptoms", "type": "toggle", "label": "Breast Lump or Breast Symptoms?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Breast symptoms with raised ESR require breast examination and consideration of breast cancer.", "red_flag_negative": "No breast symptoms - reassuring."},
                    {"id": "esr_bone_pain", "type": "toggle", "label": "Bone Pain? (Multiple Myeloma/Metastases)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bone pain with raised ESR may indicate multiple myeloma or bony metastases. Check SPEP and imaging.", "red_flag_negative": ""},
                    {"id": "esr_lymph_nodes", "type": "toggle", "label": "Lumps or Swollen Glands? (Lymphoma)", "required": False},
                    {"id": "esr_alcohol", "type": "single_select", "label": "Alcohol Consumption", "required": True, "options": ["None", "Within recommended limits", "Excessive consumption"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol excess can elevate ESR through liver disease. Check LFTs and consider liver ultrasound.", "red_flag_negative": ""},
                    {"id": "esr_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never smoked", "Ex-smoker", "Current smoker"]}
                ]
            },
            {
                "title": "Past Medical History & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "esr_pmh_none", "type": "toggle", "label": "No Significant PMHx?", "required": False},
                    {"id": "esr_known_autoimmune", "type": "toggle", "label": "Known Autoimmune Disease? (RA, SLE, IBD, Vasculitis)", "required": False},
                    {"id": "esr_ckd", "type": "toggle", "label": "Chronic Kidney Disease?", "required": False},
                    {"id": "esr_liver_disease", "type": "toggle", "label": "Known Liver Disease?", "required": False},
                    {"id": "esr_malignancy", "type": "toggle", "label": "Known or Previous Malignancy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Known malignancy with raised ESR requires urgent oncology review for recurrence or progression.", "red_flag_negative": "No known malignancy."},
                    {"id": "esr_thyroid_disease", "type": "toggle", "label": "Thyroid Disease?", "required": False},
                    {"id": "esr_obesity", "type": "toggle", "label": "Obesity? (ESR can be mildly elevated)", "required": False},
                    {"id": "esr_pregnancy", "type": "toggle", "label": "Pregnant or Postpartum?", "required": False},
                    {"id": "esr_medications", "type": "textarea", "label": "Current Medications (including OTC)", "required": False, "placeholder": "List all medications..."},
                    {"id": "esr_other_pmh", "type": "textarea", "label": "Other Relevant PMHx", "required": False, "placeholder": "Any other chronic conditions..."}
                ]
            },
            {
                "title": "Physical Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "esr_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well-appearing", "Ill-appearing", "Cachectic", "Obese", "Pale", "In Apparent Distress"]},
                    {"id": "esr_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 130"},
                    {"id": "esr_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 80"},
                    {"id": "esr_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 78"},
                    {"id": "esr_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 16"},
                    {"id": "esr_o2", "type": "number", "label": "SpO2 (%)", "required": True, "placeholder": "e.g., 98"},
                    {"id": "esr_temp", "type": "number", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 36.6"},
                    {"id": "esr_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 28"},
                    {"id": "esr_lymphadenopathy", "type": "toggle", "label": "Lymphadenopathy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy with raised ESR may indicate lymphoma, infection, or autoimmune disease.", "red_flag_negative": "No lymphadenopathy."},
                    {"id": "esr_temporal_artery", "type": "toggle", "label": "Temporal Artery Tenderness/Thickening?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal temporal artery with raised ESR is highly suggestive of GCA. Urgent steroids and rheumatology/ophthalmology referral.", "red_flag_negative": ""},
                    {"id": "esr_malar_rash_exam", "type": "toggle", "label": "Malar (Butterfly) Rash?", "required": False},
                    {"id": "esr_other_rash", "type": "toggle", "label": "Other Skin Rashes or Lesions?", "required": False},
                    {"id": "esr_joint_exam", "type": "single_select", "label": "Joint Examination", "required": False, "options": ["Normal - No synovitis", "Synovitis present", "Deformity", "Limited range of motion", "Not examined"]},
                    {"id": "esr_chest", "type": "single_select", "label": "Chest Examination", "required": True, "options": ["Clear, Vesicular BS, No Added Sounds", "Crackles", "Wheeze", "Reduced Air Entry", "Pleural Rub"]},
                    {"id": "esr_heart", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["RRR, Normal S1+S2, No Murmur", "Murmur Present", "Pericardial Rub", "Irregular"]},
                    {"id": "esr_abdomen", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, Non-tender, Non-distended", "Tenderness Present", "Organomegaly", "Mass Palpable", "Ascites"]},
                    {"id": "esr_neuro", "type": "single_select", "label": "Brief Neurological Examination", "required": False, "options": ["Normal", "Cranial nerve abnormality", "Visual field defect", "Peripheral neuropathy", "Not examined"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Infection (Acute or Chronic - TB, Endocarditis, Osteomyelitis, Abscess)",
                    "Malignancy (Lymphoma, Multiple Myeloma, Renal Cell Carcinoma, Solid Tumours)",
                    "Giant Cell Arteritis (GCA)",
                    "Polymyalgia Rheumatica (PMR)",
                    "Rheumatoid Arthritis",
                    "Systemic Lupus Erythematosus (SLE)",
                    "Inflammatory Bowel Disease (Crohn's, Ulcerative Colitis)",
                    "Sarcoidosis",
                    "Chronic Kidney Disease",
                    "Liver Disease",
                    "Thyroid Disease (Hypo/Hyperthyroidism)",
                    "Pregnancy",
                    "Obesity",
                    "Age-Related Elevation (Normal Variant)",
                    "Medication-Induced",
                    "Vasculitis (ANCA-associated, etc.)",
                    "Osteomyelitis",
                    "Tuberculosis",
                    "Non-Specific/Idiopathic"
                ],
                "questions": [
                    {"id": "esr_diagnosis", "type": "textarea", "label": "Working Diagnosis / Impression", "required": True, "placeholder": "e.g., Mildly elevated ESR likely age-related. No red flag symptoms identified. Alternatively: Raised ESR with bilateral shoulder stiffness - likely Polymyalgia Rheumatica..."},
                    {"id": "esr_diagnosis_certainty", "type": "single_select", "label": "Diagnostic Certainty", "required": True, "options": ["Likely benign/age-related", "Suspected specific diagnosis", "Possible - requires further investigation", "Uncertain - broad workup needed"]},
                    {"id": "esr_redflags_assessed", "type": "toggle", "label": "Red Flags Specifically Assessed and Excluded?", "required": True}
                ]
            },
            {
                "title": "Plan - Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "esr_repeat_esr", "type": "toggle", "label": "Repeat ESR (and CRP) in 4-6 Weeks?", "required": True},
                    {"id": "esr_bloods_list", "type": "multi_select", "label": "Blood Tests Ordered", "required": False, "options": ["FBC with differential", "U&E, Creatinine, eGFR", "LFTs", "CRP", "TFTs", "Ferritin/Iron Studies", "B12/Folate", "Serum Protein Electrophoresis (SPEP)", "Autoimmune screen (ANA, RF, anti-CCP)", "ANCA", "LDH", "Blood cultures (if fever)"]},
                    {"id": "esr_cxr", "type": "toggle", "label": "Chest X-Ray Requested? (TB/Sarcoidosis/Malignancy/Infection)", "required": False},
                    {"id": "esr_imaging_other", "type": "textarea", "label": "Other Imaging", "required": False, "placeholder": "e.g., Ultrasound abdomen, CT CAP, temporal artery ultrasound, MRI..."},
                    {"id": "esr_urinalysis", "type": "toggle", "label": "Urinalysis Performed?", "required": False},
                    {"id": "esr_urine_tests", "type": "multi_select", "label": "Urine Tests Ordered", "required": False, "options": ["Urinalysis", "Urine MSU for culture", "Urine Bence Jones Protein", "Urine Protein:Creatinine Ratio"]},
                    {"id": "esr_fit_test", "type": "toggle", "label": "FIT Test Ordered? (if bowel symptoms)", "required": False},
                    {"id": "esr_temporal_biopsy", "type": "toggle", "label": "Temporal Artery Biopsy Arranged? (if GCA suspected)", "required": False}
                ]
            },
            {
                "title": "Plan - Management",
                "section_type": "plan",
                "safety_netting": "If ESR is markedly elevated or red flags present - escalate investigation urgently. Return immediately if you develop: new severe headache, jaw pain when chewing, visual disturbance or vision loss (GCA red flags - medical emergency), unintentional weight loss, drenching night sweats, new lumps or swollen glands, bone pain, change in bowel habit, or any new breast symptoms. If ESR is only mildly elevated with no red flags, repeat ESR/CRP in 4-6 weeks. If still elevated, proceed with further investigation. If PMR suspected (bilateral shoulder/pelvic girdle stiffness with raised ESR), consider trial of prednisolone 15mg OD and monitor response. Always exclude GCA before treating PMR. Check age-appropriate reference range: Male ESR max = Age÷2; Female ESR max = (Age+10)÷2.",
                "questions": [
                    {"id": "esr_treat_underlying", "type": "textarea", "label": "Treat Underlying Cause Plan", "required": False, "placeholder": "e.g., Treat UTI, Dental infection, Adjust medications..."},
                    {"id": "esr_pmr_trial", "type": "toggle", "label": "Trial of Prednisolone for PMR? (15mg OD)", "required": False},
                    {"id": "esr_gca_steroids", "type": "toggle", "label": "High-Dose Steroids Started for Suspected GCA? (Prednisolone 40-60mg OD - same day)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: If GCA suspected, start high-dose prednisolone 40-60mg immediately (do not wait for biopsy) and refer urgently to ophthalmology/rheumatology to prevent blindness.", "red_flag_negative": ""},
                    {"id": "esr_referral_rheum", "type": "toggle", "label": "Refer to Rheumatology?", "required": False},
                    {"id": "esr_referral_haem", "type": "toggle", "label": "Refer to Haematology?", "required": False},
                    {"id": "esr_referral_ophth", "type": "toggle", "label": "Refer to Ophthalmology? (GCA with visual symptoms)", "required": False},
                    {"id": "esr_referral_other", "type": "textarea", "label": "Other Referrals", "required": False, "placeholder": "e.g., Gastroenterology, Infectious Diseases, Oncology..."},
                    {"id": "esr_reassurance", "type": "toggle", "label": "Reassurance Given? (if likely benign/age-related)", "required": False},
                    {"id": "esr_lifestyle", "type": "textarea", "label": "Lifestyle Advice", "required": False, "placeholder": "e.g., Weight management, smoking cessation, alcohol reduction..."}
                ]
            },
            {
                "title": "Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "esr_followup_value", "type": "number", "label": "Follow-up in (Number)", "required": True, "placeholder": "e.g., 4"},
                    {"id": "esr_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["days", "weeks", "months"]},
                    {"id": "esr_followup_plan", "type": "textarea", "label": "Follow-up Plan", "required": False, "placeholder": "e.g., Repeat ESR, CRP, and FBC in 4 weeks. If ESR remains elevated or rising, proceed with CXR, SPEP, and autoimmune screen. If normalized, reassure and discharge."},
                    {"id": "esr_followup_notes", "type": "textarea", "label": "Additional Follow-up Notes", "required": False, "placeholder": "e.g., Patient understands red flags. Safety netting discussed. Written information provided..."}
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
    seed_raised_esr()