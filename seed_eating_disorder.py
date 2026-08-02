from app.database import SessionLocal
from app.models import User, Template, Category

def seed_eating_disorder():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin found!")
        db.close()
        return

    title = "Eating Disorder Assessment (SCOFF)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return

    template = Template(
        title=title,
        description="Eating disorder screening and assessment using SCOFF questionnaire, medical risk evaluation, BMI monitoring, and referral criteria per NICE NG69 and MEED guidelines.",
        category="Mental Health",
        content={"sections": [
            {
                "title": "SCOFF Screening (2+ = Likely Eating Disorder)",
                "section_type": "history",
                "questions": [
                    {"id": "ed_scoff_s", "type": "toggle", "label": "S - Do you ever make yourself SICK because you feel uncomfortably full?", "required": True},
                    {"id": "ed_scoff_c", "type": "toggle", "label": "C - Do you worry you have lost CONTROL over how much you eat?", "required": True},
                    {"id": "ed_scoff_o", "type": "toggle", "label": "O - Have you recently lost more than ONE stone (6.3kg) in a 3-month period?", "required": True},
                    {"id": "ed_scoff_f1", "type": "toggle", "label": "F - Do you believe yourself to be FAT when others say you are too thin?", "required": True},
                    {"id": "ed_scoff_f2", "type": "toggle", "label": "F - Would you say that FOOD dominates your life?", "required": True},
                    {"id": "ed_scoff_score", "type": "number", "label": "SCOFF Score (/5)", "required": True, "placeholder": "e.g., 3"}
                ]
            },
            {
                "title": "Weight & Eating Behaviours",
                "section_type": "history",
                "questions": [
                    {"id": "ed_weight_now", "type": "number", "label": "Current Weight (kg)", "required": True, "placeholder": "e.g., 42"},
                    {"id": "ed_height", "type": "number", "label": "Height (cm)", "required": True, "placeholder": "e.g., 162"},
                    {"id": "ed_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 16.0"},
                    {"id": "ed_highest_weight", "type": "text", "label": "Highest Weight & When", "required": False, "placeholder": "e.g., 58kg (2 years ago)"},
                    {"id": "ed_lowest_weight", "type": "text", "label": "Lowest Weight & When", "required": False, "placeholder": "e.g., 40kg (3 months ago)"},
                    {"id": "ed_weight_change_rate", "type": "text", "label": "Rate of Weight Change", "required": True, "placeholder": "e.g., Lost 8kg in 6 weeks"},
                    {"id": "ed_desired_weight", "type": "text", "label": "Patient's Desired Weight", "required": False, "placeholder": "e.g., 38kg - wants to lose more"},
                    {"id": "ed_restriction", "type": "single_select", "label": "Dietary Restriction", "required": True, "options": ["Severe restriction (<500 kcal/day)", "Moderate restriction", "Mild restriction/counting calories", "Normal intake", "Binge eating episodes"]},
                    {"id": "ed_binge", "type": "toggle", "label": "Binge Eating Episodes?", "required": True},
                    {"id": "ed_binge_frequency", "type": "text", "label": "Binge Frequency (if present)", "required": False, "placeholder": "e.g., 3-4 times per week, feels out of control"},
                    {"id": "ed_purge", "type": "multi_select", "label": "Compensatory Behaviours", "required": True, "options": ["Self-induced vomiting", "Laxative misuse", "Diuretic misuse", "Excessive exercise", "Fasting after binges", "Diet pills/slimming aids", "None"]},
                    {"id": "ed_purge_frequency", "type": "text", "label": "Purge Frequency (if present)", "required": False, "placeholder": "e.g., Vomiting after every meal, laxatives 2x daily"},
                    {"id": "ed_exercise", "type": "text", "label": "Exercise Pattern", "required": False, "placeholder": "e.g., Runs 10km daily, cannot skip a day, exercises in secret"},
                    {"id": "ed_body_image", "type": "single_select", "label": "Body Image Distortion", "required": True, "options": ["Severe - sees self as fat despite low weight", "Moderate - overestimates body size", "Mild - some dissatisfaction", "Realistic body image"]},
                    {"id": "ed_fear_weight_gain", "type": "toggle", "label": "Intense Fear of Weight Gain?", "required": True},
                    {"id": "ed_menstruation", "type": "single_select", "label": "Menstrual History (Females)", "required": False, "options": ["Regular periods", "Oligomenorrhoea (infrequent)", "Amenorrhoea (absent >3 months)", "Not applicable (male/pre-pubertal/post-menopausal)", "On hormonal contraception"]}
                ]
            },
            {
                "title": "Medical Risk Assessment (MEED)",
                "section_type": "examination",
                "questions": [
                    {"id": "ed_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 90/60"},
                    {"id": "ed_hr", "type": "text", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 48"},
                    {"id": "ed_temp", "type": "text", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 35.8"},
                    {"id": "ed_sit_stand_bp", "type": "toggle", "label": "Postural Drop? (>10mmHg systolic drop)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postural hypotension = significant medical compromise. Urgent referral/admission.", "red_flag_negative": ""},
                    {"id": "ed_cold_extremities", "type": "toggle", "label": "Cold/Blue Extremities?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Peripheral cyanosis = severe malnutrition/cardiovascular compromise.", "red_flag_negative": ""},
                    {"id": "ed_lanugo", "type": "toggle", "label": "Lanugo Hair?", "required": False},
                    {"id": "ed_parotid", "type": "toggle", "label": "Parotid Gland Swelling? (Purging)", "required": False},
                    {"id": "ed_dental", "type": "toggle", "label": "Dental Erosion / Caries? (Vomiting)", "required": False},
                    {"id": "ed_russells", "type": "toggle", "label": "Russell's Sign? (Calluses on knuckles from vomiting)", "required": False},
                    {"id": "ed_oedema", "type": "toggle", "label": "Peripheral Oedema?", "required": False},
                    {"id": "ed_muscle_wasting", "type": "single_select", "label": "Muscle Wasting", "required": True, "options": ["None", "Mild - visible wasting", "Moderate - proximal myopathy", "Severe - unable to squat/stand from chair"]},
                    {"id": "ed_squat_test", "type": "toggle", "label": "Sit-Up-Squat-Stand (SUSS) Test Abnormal?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cannot SUSS = severe muscle weakness. High medical risk.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "ed_bloods", "type": "multi_select", "label": "Blood Tests Required", "required": False, "options": ["FBC", "U&E (K+, Na+, Mg, PO4)", "LFTs", "Glucose", "TFTs", "CK (if excessive exercise)", "ECG", "Bone density (DEXA) if amenorrhoea >1 year", "None"]},
                    {"id": "ed_ecg", "type": "toggle", "label": "ECG Done?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ECG is ESSENTIAL. Look for bradycardia, prolonged QTc, arrhythmias. QTc >450ms (M) or >460ms (F) = high risk.", "red_flag_negative": ""},
                    {"id": "ed_ecg_findings", "type": "single_select", "label": "ECG Findings", "required": False, "options": ["Normal", "Sinus bradycardia (<50bpm)", "Prolonged QTc", "Arrhythmia", "Not done/awaiting"]},
                    {"id": "ed_hypokalaemia", "type": "toggle", "label": "Hypokalaemia? (K+ <3.5 - risk of arrhythmia)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypokalaemia + purging = high risk of fatal arrhythmia. Urgent medical admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Psychiatric Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "ed_onset", "type": "text", "label": "Onset & Duration of Eating Problems", "required": True, "placeholder": "e.g., Started restricting 18 months ago, purging for 6 months"},
                    {"id": "ed_triggers", "type": "text", "label": "Precipitating Factors", "required": False, "placeholder": "e.g., Bullying about weight, relationship breakdown, exam stress"},
                    {"id": "ed_comorbid_mh", "type": "multi_select", "label": "Comorbid Mental Health", "required": True, "options": ["Depression", "Anxiety", "OCD", "PTSD/Trauma", "Self-harm", "Substance misuse", "Personality disorder traits", "None apparent"]},
                    {"id": "ed_suicidal", "type": "toggle", "label": "Suicidal Ideation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suicidal ideation requires urgent risk assessment. High mortality in eating disorders.", "red_flag_negative": ""},
                    {"id": "ed_self_harm", "type": "toggle", "label": "Self-Harm?", "required": True},
                    {"id": "ed_alcohol_drugs", "type": "toggle", "label": "Alcohol/Drug Use to Control Weight?", "required": False},
                    {"id": "ed_previous_treatment", "type": "toggle", "label": "Previous Treatment for Eating Disorder?", "required": False}
                ]
            },
            {
                "title": "Medical Risk Level (MEED Criteria)",
                "section_type": "assessment",
                "differentials": [
                    "Anorexia Nervosa (Restricting type)",
                    "Anorexia Nervosa (Binge-Purge type)",
                    "Bulimia Nervosa",
                    "Binge Eating Disorder",
                    "OSFED (Other Specified Feeding or Eating Disorder)",
                    "ARFID (Avoidant/Restrictive Food Intake Disorder)"
                ],
                "questions": [
                    {"id": "ed_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Anorexia Nervosa (Restricting)", "Anorexia Nervosa (Binge-Purge)", "Bulimia Nervosa", "Binge Eating Disorder", "OSFED / Atypical", "ARFID"]},
                    {"id": "ed_medical_risk", "type": "single_select", "label": "Medical Risk Level (MEED)", "required": True, "options": ["GREEN - Low risk: Manage in primary care with eating disorder service", "YELLOW - Moderate risk: Urgent eating disorder service referral (<2 weeks)", "RED - High risk: Emergency medical admission or urgent ED assessment", "Immediate risk to life: 999/A&E"]},
                    {"id": "ed_risk_factors", "type": "multi_select", "label": "High-Risk Factors Present?", "required": True, "options": ["BMI <13", "Rapid weight loss (>1kg/week)", "HR <40bpm", "BP <90/60 or postural drop >10mmHg", "Temperature <35.5°C", "Hypokalaemia", "Prolonged QTc", "SUSS test abnormal", "Suicidal ideation", "None - lower risk"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Eating disorders have the HIGHEST mortality of any psychiatric illness (medical complications + suicide). Medical stabilisation takes priority. Refeeding syndrome risk if severely malnourished - needs monitored refeeding with phosphate/electrolyte monitoring. Do NOT simply advise to 'eat more' - this can be fatal in severe anorexia. Family involvement crucial for adolescents. Return immediately or attend A&E if: chest pain, palpitations, fainting, severe weakness, haematemesis, or suicidal thoughts. Crisis line: 0800 689 5652.",
                "questions": [
                    {"id": "ed_plan", "type": "multi_select", "label": "Management Plan", "required": True, "options": ["Medical admission (RED risk)", "Urgent eating disorder service referral", "Routine CAMHS/adult ED service referral", "ECG + bloods arranged", "Meal plan discussed", "Family meeting/psychoeducation", "Physical health monitoring schedule", "Sick note if indicated", "Supplement drinks (Fortisip/Ensure)", "Safety plan agreed"]},
                    {"id": "ed_refeeding_risk", "type": "toggle", "label": "Refeeding Syndrome Risk Assessed?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI <14 or rapid weight loss = high refeeding risk. Start at 10-20kcal/kg/day, monitor PO4, K+, Mg daily. Medical admission required.", "red_flag_negative": ""},
                    {"id": "ed_medication", "type": "toggle", "label": "Medication Started? (Fluoxetine for bulimia; limited evidence in AN)", "required": False},
                    {"id": "ed_followup", "type": "text", "label": "Follow-up & Monitoring Plan", "required": True, "placeholder": "e.g., Weekly weight + BP + HR, ECG in 2 weeks, ED service assessment within 2 weeks"}
                ]
            }
        ]},
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_eating_disorder()