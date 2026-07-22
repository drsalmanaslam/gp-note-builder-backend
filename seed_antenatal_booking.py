from app.database import SessionLocal
from app.models import User, Template, Category

def seed_antenatal_booking():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Antenatal Booking Assessment",
        "description": "Comprehensive antenatal booking appointment covering risk assessment, screening, and early pregnancy planning.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "anc_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 32"},
                    {"id": "anc_lmp", "type": "text", "label": "First Day of Last Menstrual Period (LMP)", "required": True, "placeholder": "e.g., 15/03/2026"},
                    {"id": "anc_gestation", "type": "text", "label": "Estimated Gestation (weeks+days)", "required": True, "placeholder": "e.g., 10+3 weeks"},
                    {"id": "anc_edd", "type": "text", "label": "Estimated Date of Delivery (EDD)", "required": True, "placeholder": "e.g., 20/12/2026"},
                    {"id": "anc_scan_done", "type": "single_select", "label": "Dating/Viability Scan Status", "required": False, "options": ["Yes - confirms dates", "Yes - dates adjusted", "Not yet performed", "Booked but not yet done"]}
                ]
            },
            {
                "title": "Obstetric History",
                "section_type": "history",
                "questions": [
                    {"id": "anc_gravida", "type": "number", "label": "Gravida (Total Pregnancies Including Current)", "required": True, "placeholder": "e.g., 2"},
                    {"id": "anc_para", "type": "number", "label": "Para (Births After 24 Weeks)", "required": True, "placeholder": "e.g., 1"},
                    {"id": "anc_previous_preg", "type": "textarea", "label": "Details of Previous Pregnancies", "required": True, "placeholder": "Year, gestation, mode of delivery, birth weight, complications:\ne.g., 2019: FTND 3.4kg, uneventful\n2021: EMCS at 38w for breech, 3.1kg\n2022: Miscarriage at 8 weeks"},
                    {"id": "anc_recurrent_miscarriage", "type": "toggle", "label": "3 or More Consecutive Miscarriages?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent miscarriage requires referral to recurrent miscarriage clinic and consultant-led care.", "red_flag_negative": "No recurrent miscarriage."},
                    {"id": "anc_prev_preterm", "type": "toggle", "label": "Previous Preterm Birth (<37 weeks)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous preterm birth requires preterm birth clinic referral. Consider cervical cerclage or progesterone.", "red_flag_negative": "No previous preterm birth."},
                    {"id": "anc_prev_pet", "type": "toggle", "label": "Previous Pre-eclampsia or Pregnancy-Induced Hypertension?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: High risk for recurrent pre-eclampsia. Requires aspirin 150mg from 12 weeks, consultant-led care, serial growth scans.", "red_flag_negative": "No previous pre-eclampsia."},
                    {"id": "anc_prev_pph", "type": "toggle", "label": "Previous Postpartum Haemorrhage?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous PPH requires active management of third stage and delivery in consultant unit.", "red_flag_negative": "No previous PPH."},
                    {"id": "anc_prev_cs", "type": "toggle", "label": "Previous Caesarean Section?", "required": True},
                    {"id": "anc_prev_cs_details", "type": "textarea", "label": "Caesarean Section Details", "required": False, "placeholder": "Year, indication, type of incision, complications..."}
                ]
            },
            {
                "title": "Medical & Surgical History",
                "section_type": "history",
                "questions": [
                    {"id": "anc_pmh_none", "type": "toggle", "label": "No Significant Medical History?", "required": False},
                    {"id": "anc_diabetes", "type": "toggle", "label": "Diabetes (Type 1 or Type 2)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Diabetes in pregnancy requires joint diabetes-antenatal clinic, high dose folic acid 5mg, and consultant-led care.", "red_flag_negative": "No diabetes."},
                    {"id": "anc_hypertension", "type": "toggle", "label": "Chronic Hypertension?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Chronic hypertension requires consultant-led care. Review medications - switch ACEi/ARBs to labetalol/nifedipine/methyldopa.", "red_flag_negative": "No hypertension."},
                    {"id": "anc_thyroid", "type": "toggle", "label": "Thyroid Disease?", "required": True},
                    {"id": "anc_epilepsy", "type": "toggle", "label": "Epilepsy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Epilepsy requires consultant-led care. High dose folic acid 5mg. Medication review - avoid sodium valproate.", "red_flag_negative": "No epilepsy."},
                    {"id": "anc_cardiac", "type": "toggle", "label": "Cardiac Disease?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cardiac disease requires cardiology and obstetric consultant joint care.", "red_flag_negative": "No cardiac disease."},
                    {"id": "anc_autoimmune", "type": "toggle", "label": "Autoimmune Condition? (e.g., SLE, APS)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Autoimmune conditions require consultant-led care and may need aspirin/heparin. Check anti-Ro/La antibodies.", "red_flag_negative": "No autoimmune condition."},
                    {"id": "anc_vte_history", "type": "toggle", "label": "Personal History of VTE (DVT/PE)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: History of VTE requires consultant haematology opinion on antenatal thromboprophylaxis.", "red_flag_negative": "No VTE history."},
                    {"id": "anc_surgical_history", "type": "textarea", "label": "Past Surgical History", "required": False, "placeholder": "Including caesareans, myomectomy, cervical surgery..."},
                    {"id": "anc_mental_health", "type": "single_select", "label": "Mental Health History", "required": True, "options": ["No significant mental health history", "Previous depression - recovered", "Previous anxiety - recovered", "Previous postnatal depression", "Previous postpartum psychosis", "Current depression/anxiety", "Bipolar disorder", "Other serious mental illness"], "is_red_flag": True, "red_flag_positive": "RED FLAG: History of serious mental illness or postpartum psychosis requires perinatal mental health team referral.", "red_flag_negative": ""},
                    {"id": "anc_mh_details", "type": "textarea", "label": "Mental Health Details", "required": False, "placeholder": "Current/past medications, hospital admissions, current status..."}
                ]
            },
            {
                "title": "Medications & Allergies",
                "section_type": "history",
                "questions": [
                    {"id": "anc_allergies", "type": "textarea", "label": "Drug Allergies and Adverse Reactions", "required": True, "placeholder": "Drug, reaction, severity:\ne.g., Penicillin - anaphylaxis\nCodeine - nausea\nNo known drug allergies"},
                    {"id": "anc_current_meds", "type": "textarea", "label": "Current Medications", "required": True, "placeholder": "Prescribed, OTC, herbal, supplements:\ne.g., Levothyroxine 75mcg OD\nPregnacare Original 1 daily\nNo OTC/herbal medications"},
                    {"id": "anc_folic_acid", "type": "single_select", "label": "Folic Acid Supplementation", "required": True, "options": ["Taking 400mcg daily", "Taking 5mg daily (high dose indicated)", "Not taking any folic acid", "Taking pregnancy multivitamin containing folic acid"], "is_red_flag": True, "red_flag_positive": "RED FLAG: High dose folic acid 5mg indicated if BMI>30, diabetes, epilepsy, previous NTD, family history NTD, coeliac disease, sickle cell, thalassaemia. If not taking any, prescribe 400mcg immediately.", "red_flag_negative": ""},
                    {"id": "anc_vitamin_d", "type": "toggle", "label": "Taking Vitamin D 10mcg Daily?", "required": True}
                ]
            },
            {
                "title": "Lifestyle Factors",
                "section_type": "history",
                "questions": [
                    {"id": "anc_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never smoked", "Ex-smoker (quit before pregnancy)", "Stopped since pregnancy", "Current smoker"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Smoking in pregnancy increases risk of miscarriage, IUGR, preterm birth, SIDS. Refer to smoking cessation service immediately.", "red_flag_negative": ""},
                    {"id": "anc_smoking_amount", "type": "number", "label": "Cigarettes Per Day (if current smoker)", "required": False, "placeholder": "e.g., 10"},
                    {"id": "anc_alcohol", "type": "single_select", "label": "Alcohol Consumption", "required": True, "options": ["None", "Stopped since pregnancy", "Occasional (1-2 units/week)", "Regular (≥3 units/week)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol in pregnancy can cause fetal alcohol spectrum disorder. Advise complete abstinence. Refer to support services if needed.", "red_flag_negative": ""},
                    {"id": "anc_drug_use", "type": "single_select", "label": "Recreational Drug Use", "required": True, "options": ["None", "Previous use - stopped before pregnancy", "Current use"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Drug use in pregnancy requires specialist substance misuse team referral and enhanced antenatal care.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Family History & Genetic Risk",
                "section_type": "history",
                "questions": [
                    {"id": "anc_fh_genetic", "type": "textarea", "label": "Family History of Genetic/Congenital Conditions", "required": True, "placeholder": "Condition, relation, details:\ne.g., Cystic fibrosis - maternal cousin\nSpina bifida - mother's sister\nNo significant family history"},
                    {"id": "anc_fh_diabetes", "type": "toggle", "label": "First-Degree Relative with Diabetes?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Higher risk for gestational diabetes. Ensure OGTT at 24-28 weeks.", "red_flag_negative": "No family history of diabetes."},
                    {"id": "anc_fh_pet", "type": "toggle", "label": "Family History of Pre-eclampsia (Mother or Sister)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Moderate risk factor for pre-eclampsia. Consider aspirin 150mg from 12 weeks.", "red_flag_negative": "No family history of pre-eclampsia."},
                    {"id": "anc_fh_vte", "type": "toggle", "label": "Family History of VTE (First-Degree <50 years)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Family history of VTE requires thrombophilia screen and consultant haematology opinion on thromboprophylaxis.", "red_flag_negative": "No family history of VTE."},
                    {"id": "anc_consanguinity", "type": "toggle", "label": "Consanguineous Relationship (Partners are Blood Relatives)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Higher risk of autosomal recessive conditions. Offer genetic counselling.", "red_flag_negative": "No consanguinity."}
                ]
            },
            {
                "title": "Physical Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "anc_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 68"},
                    {"id": "anc_height", "type": "number", "label": "Height (cm)", "required": True, "placeholder": "e.g., 165"},
                    {"id": "anc_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 24.9"},
                    {"id": "anc_bmi_flag", "type": "single_select", "label": "BMI Risk Assessment", "required": True, "options": ["BMI <25 - Normal", "BMI 25-29.9 - Overweight", "BMI 30-34.9 - Obese (high risk)", "BMI 35-39.9 - Severely obese (high risk)", "BMI ≥40 - Morbidly obese (consultant-led care)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI >30 requires high dose folic acid 5mg, GTT at 24-28 weeks, anaesthetic review, thromboprophylaxis risk assessment. BMI >40 requires consultant-led care throughout.", "red_flag_negative": ""},
                    {"id": "anc_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 118"},
                    {"id": "anc_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 72"},
                    {"id": "anc_bp_flag", "type": "toggle", "label": "BP ≥140/90?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: BP ≥140/90 requires urgent assessment for pre-existing hypertension or early pre-eclampsia. If ≥160/110, refer same day.", "red_flag_negative": "BP within normal range."},
                    {"id": "anc_urinalysis", "type": "single_select", "label": "Urinalysis Result", "required": True, "options": ["Normal", "Protein +", "Protein ++ or more", "Glucose +", "Leucocytes/Nitrites positive", "Blood positive", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Proteinuria ≥1+ requires quantification with PCR/ACR and pre-eclampsia assessment. Glycosuria may indicate diabetes - arrange HbA1c or OGTT.", "red_flag_negative": ""},
                    {"id": "anc_general_exam", "type": "textarea", "label": "Other Examination Findings", "required": False, "placeholder": "Abdominal palpation, heart sounds, thyroid, respiratory..."}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Normal pregnancy - low risk", "Normal pregnancy - moderate risk factors", "High risk pregnancy requiring consultant care", "Multiple pregnancy", "Pre-existing medical conditions complicating pregnancy", "Mental health concerns in pregnancy", "Substance misuse in pregnancy"],
                "questions": [
                    {"id": "anc_bloods", "type": "single_select", "label": "Booking Bloods Status", "required": True, "options": ["All booking bloods taken today", "Bloods booked for next appointment", "Bloods already done at hospital", "Bloods declined by patient"]},
                    {"id": "anc_blood_group", "type": "single_select", "label": "Blood Group and Rh Status", "required": False, "options": ["Not yet known", "A Positive", "A Negative", "B Positive", "B Negative", "O Positive", "O Negative", "AB Positive", "AB Negative"]},
                    {"id": "anc_screening_discussed", "type": "textarea", "label": "Screening Tests Discussed and Decisions", "required": True, "placeholder": "Document screening offered and patient decisions:\n- Combined screening (Down's, Edwards', Patau's)\n- 20-week anomaly scan\n- Haemoglobinopathy screening\n- Infectious disease screening (HIV, Hep B, syphilis)\n- Rubella immunity status"},
                    {"id": "anc_risk_level", "type": "single_select", "label": "Overall Risk Assessment and Care Pathway", "required": True, "options": ["Low risk - Suitable for midwife-led care", "Moderate risk - Shared care with consultant review", "High risk - Consultant-led care throughout", "Requires MDT discussion"]},
                    {"id": "anc_redflags_assessed", "type": "toggle", "label": "Red Flags Specifically Assessed and Excluded?", "required": True}
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Provide emergency contact numbers for Early Pregnancy Unit and Maternity Triage. RED FLAGS - attend A&E or call Maternity Triage immediately if: vaginal bleeding (any amount), severe abdominal pain or cramping, reduced fetal movements (from 16-20 weeks onwards), rupture of membranes (waters breaking) - note time and colour, severe headache with visual disturbance or epigastric pain (pre-eclampsia warning), signs of VTE (unilateral leg swelling/pain/redness, sudden breathlessness, chest pain). Ensure patient knows to contact maternity services directly, not GP, for urgent pregnancy concerns. If Rh negative - discuss Anti-D prophylaxis requirements. If nausea/vomiting - advise small frequent meals, ginger, antihistamines if needed.",
                "questions": [
                    {"id": "anc_referrals", "type": "textarea", "label": "Referrals Required", "required": False, "placeholder": "e.g., Anaesthetic review (BMI 38)\nPerinatal mental health team\nDietetics (BMI >30)\nPhysiotherapy (back pain)\nConsultant obstetrician\nSmoking cessation service"},
                    {"id": "anc_medications_plan", "type": "textarea", "label": "Medications Prescribed/Adjusted", "required": False, "placeholder": "e.g., Folic acid 400mcg OD prescribed\nVitamin D 10mcg OD advised\nAspirin 150mg OD from 12 weeks\nACE inhibitor stopped - switched to labetalol"},
                    {"id": "anc_plan_summary", "type": "textarea", "label": "Summary of Plan", "required": True, "placeholder": "1. Dating scan booked for [date]\n2. Combined screening at 12 weeks\n3. OGTT at 24-28 weeks (if indicated)\n4. Aspirin 150mg OD from 12 weeks (if indicated)\n5. Routine midwife appointments\n6. Anomaly scan at 20 weeks"},
                    {"id": "anc_next_appointment", "type": "text", "label": "Next Antenatal Appointment", "required": True, "placeholder": "e.g., 4 weeks - 15/04/2026 with community midwife"}
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
    seed_antenatal_booking()