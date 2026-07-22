from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hyperprolactinaemia_female():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Hyperprolactinaemia - Female Assessment",
        "description": "Comprehensive assessment for hyperprolactinaemia in females including differential diagnosis, medication review, investigation, and management plan with referral criteria.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "hprl_gender", "type": "single_select", "label": "Gender", "required": True, "options": ["Female", "Trans Man", "Trans Woman"]},
                    {"id": "hprl_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 32"},
                    {"id": "hprl_presentation", "type": "single_select", "label": "Presents For", "required": True, "options": ["New hyperprolactinaemia (incidental)", "New hyperprolactinaemia (symptomatic)", "Known hyperprolactinaemia - follow-up", "Known hyperprolactinaemia - on treatment"]},
                    {"id": "hprl_presentation_detail", "type": "textarea", "label": "Presentation Details", "required": False, "placeholder": "Describe presenting complaint and reason for prolactin check..."}
                ]
            },
            {
                "title": "Blood Results",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_prolactin", "type": "number", "label": "Prolactin (mIU/L)", "required": True, "placeholder": "e.g., 1250 (NR: approx 100-500, lab dependent)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Prolactin >5000 mIU/L is strongly suggestive of prolactinoma. Requires urgent pituitary MRI and endocrinology referral.", "red_flag_negative": ""},
                    {"id": "hprl_elevation", "type": "single_select", "label": "Degree of Elevation", "required": True, "options": ["Normal (<500 mIU/L)", "Mild elevation (500-1000 mIU/L)", "Moderate elevation (1000-5000 mIU/L)", "Marked elevation (>5000 mIU/L) - suspicious for prolactinoma"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Marked elevation >5000 mIU/L strongly suggests prolactinoma. Urgent pituitary MRI and endocrinology referral required.", "red_flag_negative": ""},
                    {"id": "hprl_repeat_prolactin", "type": "number", "label": "Repeat Fasting Morning Prolactin (mIU/L)", "required": False, "placeholder": "e.g., 1180 (repeat fasting, early morning)"},
                    {"id": "hprl_tsh", "type": "number", "label": "TSH (mIU/L)", "required": True, "placeholder": "e.g., 45.2 (NR: 0.4-4.0)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Elevated TSH indicates primary hypothyroidism as cause of hyperprolactinaemia. Treat hypothyroidism first before investigating pituitary.", "red_flag_negative": ""},
                    {"id": "hprl_free_t4", "type": "number", "label": "Free T4 (pmol/L)", "required": False, "placeholder": "e.g., 8.5 (NR: 9-25)"},
                    {"id": "hprl_fsh", "type": "number", "label": "FSH (IU/L)", "required": False, "placeholder": "e.g., 5.2"},
                    {"id": "hprl_lh", "type": "number", "label": "LH (IU/L)", "required": False, "placeholder": "e.g., 8.1"},
                    {"id": "hprl_oestradiol", "type": "number", "label": "Oestradiol (pmol/L)", "required": False, "placeholder": "e.g., 180"},
                    {"id": "hprl_bhcg", "type": "single_select", "label": "β-hCG (Pregnancy Test)", "required": True, "options": ["Negative", "Positive - PREGNANT", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive β-hCG - pregnancy is a common cause of physiological hyperprolactinaemia. No further investigation needed.", "red_flag_negative": ""},
                    {"id": "hprl_ue_creatinine", "type": "textarea", "label": "U&E, Creatinine, eGFR", "required": False, "placeholder": "e.g., Na 139, K 4.2, Creatinine 72, eGFR 88"},
                    {"id": "hprl_lfts", "type": "textarea", "label": "LFTs", "required": False, "placeholder": "e.g., ALT 22, AST 28, ALP 75, GGT 35"},
                    {"id": "hprl_macroprolactin", "type": "single_select", "label": "Macroprolactin Assay", "required": False, "options": ["Not done", "Normal - no macroprolactin", "Macroprolactin present - likely macroprolactinaemia", "Pending"]},
                    {"id": "hprl_other_labs", "type": "textarea", "label": "Other Lab Results", "required": False, "placeholder": "IGF-1, cortisol, other pituitary hormones..."}
                ]
            },
            {
                "title": "Menstrual & Reproductive Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_amenorrhoea", "type": "toggle", "label": "Amenorrhoea (Absent Periods)?", "required": True},
                    {"id": "hprl_amenorrhoea_duration", "type": "text", "label": "Duration of Amenorrhoea", "required": False, "placeholder": "e.g., 6 months"},
                    {"id": "hprl_oligomenorrhoea", "type": "toggle", "label": "Oligomenorrhoea (Infrequent Periods)?", "required": False},
                    {"id": "hprl_irregular_periods", "type": "toggle", "label": "Irregular Periods?", "required": False},
                    {"id": "hprl_infertility", "type": "toggle", "label": "Infertility/Difficulty Conceiving?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Infertility with hyperprolactinaemia requires endocrinology referral for dopamine agonist therapy.", "red_flag_negative": ""},
                    {"id": "hprl_reduced_libido", "type": "toggle", "label": "Reduced Libido?", "required": False},
                    {"id": "hprl_pcos_features", "type": "toggle", "label": "Features of PCOS? (Acne, Hirsutism, Weight Gain)", "required": False}
                ]
            },
            {
                "title": "Breast Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_galactorrhoea", "type": "toggle", "label": "Galactorrhoea (Milky Nipple Discharge)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Galactorrhoea with hyperprolactinaemia is classic for prolactinoma. Requires pituitary MRI and endocrinology referral.", "red_flag_negative": "No galactorrhoea."},
                    {"id": "hprl_galactorrhoea_detail", "type": "textarea", "label": "Galactorrhoea Details", "required": False, "placeholder": "Unilateral or bilateral, spontaneous or expressible, colour (milky/clear/bloody)..."},
                    {"id": "hprl_nipple_discharge", "type": "toggle", "label": "Nipple Discharge (non-milky)?", "required": False},
                    {"id": "hprl_breast_enlargement", "type": "toggle", "label": "Breast Enlargement or Tenderness?", "required": False},
                    {"id": "hprl_breast_pain", "type": "toggle", "label": "Breast Pain (Mastalgia)?", "required": False}
                ]
            },
            {
                "title": "Mass Effect Symptoms - Pituitary",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_headaches", "type": "toggle", "label": "Headaches?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Headaches with hyperprolactinaemia may indicate pituitary macroadenoma. Urgent imaging and endocrinology referral required.", "red_flag_negative": "No headaches."},
                    {"id": "hprl_headache_detail", "type": "textarea", "label": "Headache Details", "required": False, "placeholder": "Location, severity, frequency, associated symptoms..."},
                    {"id": "hprl_visual_disturbance", "type": "toggle", "label": "Visual Disturbance?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual disturbance with hyperprolactinaemia suggests pituitary macroadenoma compressing optic chiasm. URGENT - same-day endocrinology/neurosurgery referral.", "red_flag_negative": "No visual disturbance."},
                    {"id": "hprl_peripheral_vision", "type": "toggle", "label": "Reduced Peripheral Vision?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Peripheral vision loss (bitemporal hemianopia) indicates optic chiasm compression. URGENT neurosurgical referral.", "red_flag_negative": "No peripheral vision loss."},
                    {"id": "hprl_diplopia", "type": "toggle", "label": "Double Vision (Diplopia)?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Diplopia suggests cranial nerve involvement from pituitary mass. Urgent assessment required.", "red_flag_negative": "No diplopia."},
                    {"id": "hprl_bumping_objects", "type": "toggle", "label": "Bumping Into Objects? (Visual Field Defect)", "required": False}
                ]
            },
            {
                "title": "Endocrine & Systemic Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_weight_gain", "type": "toggle", "label": "Weight Gain?", "required": False},
                    {"id": "hprl_fatigue", "type": "toggle", "label": "Fatigue?", "required": False},
                    {"id": "hprl_cold_intolerance", "type": "toggle", "label": "Cold Intolerance? (Hypothyroidism)", "required": False},
                    {"id": "hprl_hypothyroid_features", "type": "multi_select", "label": "Features of Hypothyroidism", "required": False, "options": ["Weight gain", "Fatigue", "Cold intolerance", "Constipation", "Dry skin", "Hair loss", "Hoarse voice", "Bradycardia", "None"]},
                    {"id": "hprl_pcos_features_detailed", "type": "multi_select", "label": "Features of PCOS", "required": False, "options": ["Acne", "Hirsutism", "Weight gain/obesity", "Irregular periods", "Acanthosis nigricans", "None"]}
                ]
            },
            {
                "title": "Pregnancy & Physiological History",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_possible_pregnancy", "type": "toggle", "label": "Possible Pregnancy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Always exclude pregnancy first. Pregnancy is the most common physiological cause of hyperprolactinaemia.", "red_flag_negative": ""},
                    {"id": "hprl_recent_pregnancy", "type": "toggle", "label": "Recent Pregnancy or Postpartum?", "required": False},
                    {"id": "hprl_breastfeeding", "type": "toggle", "label": "Currently Breastfeeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Breastfeeding is a physiological cause of hyperprolactinaemia. No investigation needed. Recheck prolactin after weaning.", "red_flag_negative": "Not breastfeeding."},
                    {"id": "hprl_stress", "type": "toggle", "label": "Significant Stress?", "required": False},
                    {"id": "hprl_excess_exercise", "type": "toggle", "label": "Excessive Exercise?", "required": False},
                    {"id": "hprl_chest_wall_trauma", "type": "toggle", "label": "Recent Chest Wall Trauma or Surgery?", "required": False},
                    {"id": "hprl_recent_surgery", "type": "toggle", "label": "Recent Surgery (Any)?", "required": False},
                    {"id": "hprl_seizures", "type": "toggle", "label": "Seizures or Epilepsy?", "required": False}
                ]
            },
            {
                "title": "Medication History",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_antipsychotics", "type": "toggle", "label": "Taking Antipsychotics? (Risperidone, Haloperidol, Phenothiazines, Olanzapine)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Antipsychotics are a common cause of drug-induced hyperprolactinaemia. Discuss with psychiatrist about dose reduction or switching to prolactin-sparing agent (e.g., Aripiprazole, Quetiapine).", "red_flag_negative": ""},
                    {"id": "hprl_antipsychotic_details", "type": "textarea", "label": "Antipsychotic Details", "required": False, "placeholder": "Drug, dose, duration, prescriber..."},
                    {"id": "hprl_metoclopramide", "type": "toggle", "label": "Taking Metoclopramide (Maxolon)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Metoclopramide is a potent D2 antagonist causing hyperprolactinaemia. Stop if possible and use alternative antiemetic (e.g., Domperidone, Cyclizine).", "red_flag_negative": ""},
                    {"id": "hprl_ssris", "type": "toggle", "label": "Taking SSRIs? (Fluoxetine, Sertraline, Citalopram, Escitalopram, Paroxetine)", "required": True},
                    {"id": "hprl_tcas", "type": "toggle", "label": "Taking Tricyclic Antidepressants? (Amitriptyline, Nortriptyline)", "required": False},
                    {"id": "hprl_oestrogens", "type": "toggle", "label": "Taking Oestrogens or Combined Oral Contraceptive?", "required": True},
                    {"id": "hprl_verapamil", "type": "toggle", "label": "Taking Verapamil?", "required": False},
                    {"id": "hprl_opioids", "type": "toggle", "label": "Taking Opioids? (Codeine, Tramadol, Morphine, Oxycodone)", "required": False},
                    {"id": "hprl_methyldopa", "type": "toggle", "label": "Taking Methyldopa?", "required": False},
                    {"id": "hprl_ppis", "type": "toggle", "label": "Taking Proton Pump Inhibitors? (Omeprazole, Lansoprazole, Pantoprazole)", "required": False},
                    {"id": "hprl_other_meds", "type": "textarea", "label": "Other Current Medications", "required": False, "placeholder": "List all medications including OTC and supplements..."}
                ]
            },
            {
                "title": "Past Medical History",
                "section_type": "history",
                "questions": [
                    {"id": "hprl_pmh_none", "type": "toggle", "label": "No Significant PMHx?", "required": False},
                    {"id": "hprl_ckd", "type": "toggle", "label": "Chronic Kidney Disease?", "required": False},
                    {"id": "hprl_liver_disease", "type": "toggle", "label": "Liver Disease?", "required": False},
                    {"id": "hprl_hypothyroidism", "type": "toggle", "label": "Known Hypothyroidism?", "required": False},
                    {"id": "hprl_pcos", "type": "toggle", "label": "Known PCOS?", "required": False},
                    {"id": "hprl_pituitary_disease", "type": "toggle", "label": "Known Pituitary Disease or Previous Pituitary Surgery?", "required": False},
                    {"id": "hprl_family_pituitary", "type": "toggle", "label": "Family History of Pituitary Disease or MEN1?", "required": False}
                ]
            },
            {
                "title": "Physical Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hprl_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well-appearing", "Anxious", "Obese", "Distressed", "Cushingoid features", "Acromegalic features"]},
                    {"id": "hprl_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 120"},
                    {"id": "hprl_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 78"},
                    {"id": "hprl_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 72"},
                    {"id": "hprl_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 16"},
                    {"id": "hprl_o2", "type": "number", "label": "SpO2 (%)", "required": True, "placeholder": "e.g., 98"},
                    {"id": "hprl_temp", "type": "number", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 36.5"},
                    {"id": "hprl_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 28"},
                    {"id": "hprl_visual_acuity", "type": "single_select", "label": "Visual Acuity", "required": False, "options": ["Normal", "Reduced - Right eye", "Reduced - Left eye", "Reduced - Both eyes", "Not assessed"]},
                    {"id": "hprl_visual_fields", "type": "single_select", "label": "Visual Fields (Confrontation)", "required": True, "options": ["Intact", "Reduced - Bitemporal hemianopia", "Reduced - Other pattern", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bitemporal hemianopia indicates optic chiasm compression from pituitary mass. Urgent neurosurgical referral.", "red_flag_negative": ""},
                    {"id": "hprl_diplopia_exam", "type": "toggle", "label": "Diplopia on Examination?", "required": False},
                    {"id": "hprl_thyroid_exam", "type": "single_select", "label": "Thyroid Examination", "required": False, "options": ["Normal", "Goitre present", "Thyroid nodule(s)", "Clinical hypothyroidism features", "Not examined"]},
                    {"id": "hprl_breast_exam", "type": "single_select", "label": "Breast Examination", "required": False, "options": ["Normal", "Galactorrhoea expressible", "Breast tenderness", "Breast mass", "Not examined"]},
                    {"id": "hprl_galactorrhoea_exam", "type": "toggle", "label": "Galactorrhoea on Examination?", "required": False},
                    {"id": "hprl_cranial_nerves", "type": "single_select", "label": "Cranial Nerve Examination", "required": True, "options": ["Intact (CN I-XII)", "Abnormality detected", "Not examined"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Cranial nerve abnormality with hyperprolactinaemia suggests pituitary mass with cavernous sinus involvement. Urgent imaging and referral.", "red_flag_negative": ""},
                    {"id": "hprl_hirsutism", "type": "toggle", "label": "Hirsutism or Acne? (PCOS)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Prolactinoma - Microadenoma (<10mm)",
                    "Prolactinoma - Macroadenoma (≥10mm)",
                    "Physiological Hyperprolactinaemia (Pregnancy, Lactation, Stress, Exercise)",
                    "Drug-Induced Hyperprolactinaemia (Antipsychotics, Metoclopramide, SSRIs, Oestrogens, Verapamil, Opioids)",
                    "Primary Hypothyroidism (TRH-driven hyperprolactinaemia)",
                    "Polycystic Ovary Syndrome (PCOS)",
                    "Chronic Kidney Disease",
                    "Liver Disease/Cirrhosis",
                    "Pituitary Stalk Compression (Non-functioning pituitary adenoma, Craniopharyngioma)",
                    "Pituitary Macroadenoma (Non-prolactin secreting)",
                    "Acromegaly (Co-secretion or stalk effect)",
                    "Cushing Syndrome/Cushing Disease",
                    "Chest Wall Pathology/Trauma/Herpes Zoster",
                    "Idiopathic Hyperprolactinaemia",
                    "Macroprolactinaemia (Macroprolactin - biologically inactive)"
                ],
                "questions": [
                    {"id": "hprl_diagnosis", "type": "textarea", "label": "Working Diagnosis / Impression", "required": True, "placeholder": "e.g., Drug-induced hyperprolactinaemia secondary to Risperidone. Alternatively: Likely prolactinoma given prolactin >5000 with galactorrhoea and amenorrhoea..."},
                    {"id": "hprl_diagnosis_certainty", "type": "single_select", "label": "Diagnostic Certainty", "required": True, "options": ["Likely drug-induced", "Likely physiological", "Suspected prolactinoma", "Suspected hypothyroidism-related", "Suspected stalk compression", "Uncertain - requires further investigation"]},
                    {"id": "hprl_redflags_assessed", "type": "toggle", "label": "Red Flags Specifically Assessed and Excluded?", "required": True}
                ]
            },
            {
                "title": "Plan - Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "hprl_repeat_prolactin_test", "type": "toggle", "label": "Repeat Fasting Morning Prolactin Ordered?", "required": True},
                    {"id": "hprl_bloods_list", "type": "multi_select", "label": "Blood Tests Ordered", "required": False, "options": ["TSH, Free T4", "β-hCG (Pregnancy Test)", "FSH/LH", "Oestradiol", "U&E, Creatinine, eGFR", "LFTs", "Macroprolactin Assay", "IGF-1 (if pituitary pathology suspected)", "Cortisol (if Cushing's suspected)", "Testosterone (if PCOS features)"]},
                    {"id": "hprl_mri_pituitary", "type": "toggle", "label": "MRI Pituitary with Contrast Requested?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: MRI pituitary indicated if: prolactin >1000 mIU/L persistent, visual symptoms, headaches, galactorrhoea with elevated prolactin, or suspected pituitary pathology. Usually arranged by endocrinology.", "red_flag_negative": ""},
                    {"id": "hprl_visual_fields_formal", "type": "toggle", "label": "Formal Visual Field Assessment (Perimetry) Requested?", "required": False},
                    {"id": "hprl_other_imaging", "type": "textarea", "label": "Other Imaging", "required": False, "placeholder": "e.g., CT pituitary if MRI contraindicated..."}
                ]
            },
            {
                "title": "Plan - Management & Medication Review",
                "section_type": "plan",
                "safety_netting": "Return immediately if you develop: new or worsening headaches, visual disturbance (blurred vision, double vision), loss of peripheral vision (bumping into objects), severe breast discharge, or any new neurological symptoms. If on dopamine agonist therapy (Cabergoline/Bromocriptine) - do not stop suddenly. Always exclude pregnancy and hypothyroidism before investigating for prolactinoma. Review all medications carefully - many common drugs cause hyperprolactinaemia. If medication-induced, discuss with prescribing physician before stopping or changing medications. If prolactinoma confirmed, dopamine agonist therapy is highly effective and usually initiated by endocrinology.",
                "questions": [
                    {"id": "hprl_treat_hypothyroidism", "type": "toggle", "label": "Treat Hypothyroidism? (Levothyroxine if TSH elevated)", "required": False},
                    {"id": "hprl_stop_offending_med", "type": "multi_select", "label": "Medications to Stop/Change (Discuss with Prescriber)", "required": False, "options": ["Antipsychotic - discuss switching to Aripiprazole/Quetiapine", "Metoclopramide - stop, use alternative antiemetic", "SSRI - consider dose reduction or alternative", "Oestrogens/OCP - consider alternative contraception", "Verapamil - change to alternative antihypertensive", "Opioids - reduce/stop if possible", "PPI - consider H2RA alternative"]},
                    {"id": "hprl_dopamine_agonist", "type": "single_select", "label": "Dopamine Agonist Therapy (Usually Initiated by Endocrinology)", "required": False, "options": ["None - not indicated yet", "Cabergoline - initiated by endocrinology", "Bromocriptine - initiated by endocrinology", "Awaiting endocrinology to initiate"]},
                    {"id": "hprl_reassurance", "type": "toggle", "label": "Reassurance Given? (if physiological cause or macroprolactinaemia)", "required": False},
                    {"id": "hprl_other_management", "type": "textarea", "label": "Other Management", "required": False, "placeholder": "Additional advice, lifestyle modifications, stress management..."}
                ]
            },
            {
                "title": "Referral & Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "hprl_endo_referral", "type": "toggle", "label": "Refer to Endocrinology?", "required": True},
                    {"id": "hprl_endo_routine", "type": "toggle", "label": "Routine Endocrinology Referral Criteria Met", "required": False, "placeholder": "Indications:\n- Persistent hyperprolactinaemia\n- Elevated prolactin without obvious cause\n- Menstrual disturbance (amenorrhoea/oligomenorrhoea)\n- Galactorrhoea\n- Infertility\n- Suspected pituitary adenoma"},
                    {"id": "hprl_endo_urgent", "type": "toggle", "label": "Urgent Endocrinology/Neurosurgery Referral Required?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Urgent referral if: visual field defect, visual disturbance, severe headache, cranial nerve abnormalities, suspected pituitary macroadenoma, prolactin >5000 mIU/L.", "red_flag_negative": ""},
                    {"id": "hprl_urgent_reason", "type": "textarea", "label": "Reason for Urgent Referral", "required": False, "placeholder": "Document specific urgent criteria met..."},
                    {"id": "hprl_ophthalmology_referral", "type": "toggle", "label": "Refer to Ophthalmology? (Visual field testing)", "required": False},
                    {"id": "hprl_followup_value", "type": "number", "label": "Follow-up in (Number)", "required": True, "placeholder": "e.g., 4"},
                    {"id": "hprl_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["weeks", "months"]},
                    {"id": "hprl_followup_plan", "type": "textarea", "label": "Follow-up Plan", "required": False, "placeholder": "e.g., Repeat prolactin in 4 weeks after medication change. If still elevated, refer endocrinology for MRI pituitary. If normalized, monitor clinically."},
                    {"id": "hprl_followup_notes", "type": "textarea", "label": "Additional Follow-up Notes", "required": False, "placeholder": "e.g., Patient understands red flag symptoms. Written safety netting provided. Copy of results given..."}
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
    seed_hyperprolactinaemia_female()