from app.database import SessionLocal
from app.models import User, Template, Category

def seed_health_check_male():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Asymptomatic Health Check (Male)",
        "description": "Comprehensive routine health check for asymptomatic men covering cardiovascular, metabolic, cancer screening, sexual health, and lifestyle assessment.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Screen First (If Present = NOT Routine Check)",
                "section_type": "history",
                "questions": [
                    {"id": "ahcm_weight_loss", "type": "toggle", "label": "Unexplained Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss = NOT a routine health check. Investigate underlying cause.", "red_flag_negative": ""},
                    {"id": "ahcm_fatigue", "type": "toggle", "label": "Significant Fatigue?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fatigue = investigate cause (anaemia, thyroid, diabetes, malignancy).", "red_flag_negative": ""},
                    {"id": "ahcm_fever", "type": "toggle", "label": "Fever?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever = ?infection, inflammatory, malignancy.", "red_flag_negative": ""},
                    {"id": "ahcm_night_sweats", "type": "toggle", "label": "Night Sweats?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Night sweats = ?lymphoma, TB, infection.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History - General",
                "section_type": "history",
                "questions": [
                    {"id": "ahcm_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 45"},
                    {"id": "ahcm_concerns", "type": "textarea", "label": "Any Concerns Today?", "required": True, "placeholder": "e.g., No specific concerns - routine check-up"},
                    {"id": "ahcm_pmh", "type": "textarea", "label": "Past Medical & Surgical History", "required": True, "placeholder": "e.g., Nil significant / Appendicectomy 2010"},
                    {"id": "ahcm_meds_allergies", "type": "textarea", "label": "Medications & Allergies", "required": True, "placeholder": "e.g., No regular medications. No known drug allergies."}
                ]
            },
            {
                "title": "Family History",
                "section_type": "history",
                "questions": [
                    {"id": "ahcm_fh_cvd", "type": "toggle", "label": "Family History: Cardiovascular Disease? (IHD, Stroke <65)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx premature CVD = increased risk. Calculate QRISK.", "red_flag_negative": ""},
                    {"id": "ahcm_fh_diabetes", "type": "toggle", "label": "Family History: Diabetes?", "required": True},
                    {"id": "ahcm_fh_cancer", "type": "multi_select", "label": "Family History: Cancer", "required": True, "options": ["Prostate Cancer", "Bowel Cancer", "Breast Cancer (BRCA)", "Other", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx prostate/bowel cancer = earlier screening. FHx breast/BRCA = genetic counselling.", "red_flag_negative": ""},
                    {"id": "ahcm_fh_scd", "type": "toggle", "label": "Family History: Sudden Cardiac Death (<40)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx SCD = ?Brugada, LQTS, HOCM. Cardiology referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Lifestyle",
                "section_type": "history",
                "questions": [
                    {"id": "ahcm_smoking", "type": "single_select", "label": "Smoking / Vaping", "required": True, "options": ["Never Smoked", "Ex-Smoker", "Current Smoker", "Vaping"]},
                    {"id": "ahcm_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within Limits (<17 Units/Week)", "Excess (≥17 Units/Week)"]},
                    {"id": "ahcm_drugs", "type": "toggle", "label": "Recreational Drug Use?", "required": False},
                    {"id": "ahcm_diet", "type": "single_select", "label": "Diet", "required": True, "options": ["Balanced / Mediterranean", "Fair - Some Unhealthy Choices", "Poor - High Fat/Sugar/Processed"]},
                    {"id": "ahcm_exercise", "type": "single_select", "label": "Exercise", "required": True, "options": ["Regular (≥150 Min/Week)", "Occasional", "Sedentary"]}
                ]
            },
            {
                "title": "Sleep, Mood & Stress",
                "section_type": "history",
                "questions": [
                    {"id": "ahcm_snoring", "type": "toggle", "label": "Snoring?", "required": False},
                    {"id": "ahcm_daytime_somnolence", "type": "toggle", "label": "Daytime Somnolence / Fatigue?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Snoring + daytime somnolence = ?OSA. Epworth score + sleep study.", "red_flag_negative": ""},
                    {"id": "ahcm_mood", "type": "single_select", "label": "Mood / Stress", "required": True, "options": ["Good - No Concerns", "Mild Stress / Low Mood", "Significant Stress / Anxiety", "Low Mood / ?Depression"]}
                ]
            },
            {
                "title": "Sexual & Urological Health",
                "section_type": "history",
                "questions": [
                    {"id": "ahcm_libido", "type": "toggle", "label": "Reduced Libido?", "required": False},
                    {"id": "ahcm_ed", "type": "toggle", "label": "Erectile Dysfunction?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: ED = ?cardiovascular risk marker. Check QRISK, glucose, lipids, testosterone.", "red_flag_negative": ""},
                    {"id": "ahcm_sti_risk", "type": "toggle", "label": "STI Risk? (New/Multiple Partners, Unprotected Intercourse)", "required": False},
                    {"id": "ahcm_luts", "type": "multi_select", "label": "Lower Urinary Tract Symptoms (If Older)", "required": False, "options": ["Frequency", "Nocturia", "Hesitancy", "Poor Stream", "Urgency", "None"]}
                ]
            },
            {
                "title": "Vaccinations & Screening",
                "section_type": "history",
                "questions": [
                    {"id": "ahcm_vaccinations", "type": "multi_select", "label": "Vaccinations Up to Date?", "required": True, "options": ["Influenza (Annual)", "Pneumococcal", "Tetanus (10-Yearly)", "COVID-19 Booster", "Not Up to Date - Advised"]},
                    {"id": "ahcm_screening", "type": "multi_select", "label": "Age-Appropriate Screening Up to Date?", "required": False, "options": ["Bowel Screen (Age 60-69)", "PSA Discussed (If Appropriate)", "Not Applicable"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ahcm_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 128/82"},
                    {"id": "ahcm_hr", "type": "number", "label": "Pulse (bpm)", "required": True, "placeholder": "e.g., 72"},
                    {"id": "ahcm_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 26"},
                    {"id": "ahcm_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well, No Distress", "Overweight / Obese", "Pale / Unwell"]},
                    {"id": "ahcm_cvs", "type": "single_select", "label": "Cardiovascular Examination", "required": True, "options": ["HS I+II Audible, No Murmurs", "Murmur Present", "Irregular Pulse"]},
                    {"id": "ahcm_resp", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Clear B/L, Vesicular BS", "Abnormal"]},
                    {"id": "ahcm_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, Non-Tender, No Masses", "Abnormal"]},
                    {"id": "ahcm_skin", "type": "single_select", "label": "Skin Examination (If Indicated)", "required": False, "options": ["Normal", "Abnormal - Refer Dermatology", "Not Examined"]},
                    {"id": "ahcm_testicular", "type": "single_select", "label": "Testicular Examination (Only if Symptoms/Specific Concerns)", "required": False, "options": ["Normal", "Abnormal - Refer Urology", "Not Indicated / Not Examined"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Well Asymptomatic Male - Routine Health Check",
                    "?Metabolic Syndrome (Central Obesity, Raised BP, Dyslipidaemia)",
                    "?Hypogonadism (Low Libido, ED, Fatigue)",
                    "?OSA (Snoring, Daytime Somnolence, Obesity)",
                    "?Cardiovascular Risk (FHx, Smoking, Raised BP)"
                ],
                "questions": [
                    {"id": "ahcm_routine_bloods", "type": "multi_select", "label": "Routine Bloods Ordered", "required": False, "options": ["FBC", "U&E / Renal Profile", "LFTs", "Fasting Lipid Profile", "HbA1c"]},
                    {"id": "ahcm_indicated_bloods", "type": "multi_select", "label": "Additional Bloods (If Indicated by History/Exam)", "required": False, "options": ["TSH", "Ferritin / Iron Studies", "B12 / Folate", "Vitamin D", "Testosterone (9am - If Hypogonadal Symptoms)", "PSA (Shared Decision-Making - Appropriate Age/Risk Only)", "None"]},
                    {"id": "ahcm_urinalysis", "type": "toggle", "label": "Urinalysis?", "required": False},
                    {"id": "ahcm_sti_screen", "type": "toggle", "label": "STI Screen?", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: new symptoms develop, weight loss, night sweats, fatigue, or any concerning changes before next routine check. Lifestyle advice: Mediterranean diet, 150 min exercise/week, smoking cessation, alcohol reduction, weight management. Advise monthly testicular self-awareness. Review vaccinations and age-appropriate screening. Follow up with blood results in 1-2 weeks. If PSA testing: counsel on risks/benefits (false positives, unnecessary biopsies, overdiagnosis). Not routine in young asymptomatic men.",
                "questions": [
                    {"id": "ahcm_diagnosis", "type": "single_select", "label": "Assessment", "required": True, "options": ["Well Asymptomatic Male - Routine Health Check", "Abnormal Findings - Requires Further Investigation", "Red Flags Present - NOT Routine Check"]},
                    {"id": "ahcm_lifestyle_advice", "type": "multi_select", "label": "Lifestyle Advice Given", "required": False, "options": ["Mediterranean Diet", "Exercise - 150 Min/Week", "Smoking Cessation", "Alcohol Reduction", "Weight Management"]},
                    {"id": "ahcm_testicular_awareness", "type": "toggle", "label": "Monthly Testicular Self-Awareness Advised?", "required": False},
                    {"id": "ahcm_vaccination_review", "type": "toggle", "label": "Vaccinations + Screening Reviewed?", "required": False},
                    {"id": "ahcm_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1-2 weeks with blood results, sooner if concerns"}
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
    seed_health_check_male()