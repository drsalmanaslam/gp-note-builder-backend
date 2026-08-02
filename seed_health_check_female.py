from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_health_check_female():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Asymptomatic Health Check (Female)",
        "description": "Comprehensive routine health check for asymptomatic women covering cardiovascular, metabolic, gynaecological, cancer screening, and lifestyle assessment.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Screen First (If Present = NOT Routine Check)",
                "section_type": "history",
                "questions": [
                    {"id": "ahcf_weight_loss", "type": "toggle", "label": "Unexplained Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss = NOT a routine health check. Investigate underlying cause.", "red_flag_negative": ""},
                    {"id": "ahcf_fatigue", "type": "toggle", "label": "Significant Fatigue?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fatigue = investigate cause (anaemia, thyroid, diabetes, malignancy).", "red_flag_negative": ""},
                    {"id": "ahcf_fever", "type": "toggle", "label": "Fever?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever = ?infection, inflammatory, malignancy.", "red_flag_negative": ""},
                    {"id": "ahcf_night_sweats", "type": "toggle", "label": "Night Sweats?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Night sweats = ?lymphoma, TB, infection.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History - General",
                "section_type": "history",
                "questions": [
                    {"id": "ahcf_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 42"},
                    {"id": "ahcf_concerns", "type": "textarea", "label": "Any Concerns Today?", "required": True, "placeholder": "e.g., No specific concerns - routine check-up"},
                    {"id": "ahcf_pmh", "type": "textarea", "label": "Past Medical & Surgical History", "required": True, "placeholder": "e.g., Nil significant / C-section 2018"},
                    {"id": "ahcf_meds_allergies", "type": "textarea", "label": "Medications & Allergies", "required": True, "placeholder": "e.g., Microgynon 30 ED. No known drug allergies."}
                ]
            },
            {
                "title": "Family History",
                "section_type": "history",
                "questions": [
                    {"id": "ahcf_fh_cvd", "type": "toggle", "label": "Family History: Cardiovascular Disease? (IHD, Stroke <65)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx premature CVD = increased risk. Calculate QRISK.", "red_flag_negative": ""},
                    {"id": "ahcf_fh_diabetes", "type": "toggle", "label": "Family History: Diabetes?", "required": True},
                    {"id": "ahcf_fh_cancer", "type": "multi_select", "label": "Family History: Cancer", "required": True, "options": ["Breast Cancer", "Ovarian Cancer", "Bowel Cancer", "Endometrial Cancer", "Other", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx breast/ovarian cancer = ?BRCA. Genetic counselling. FHx bowel = earlier screening.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Lifestyle",
                "section_type": "history",
                "questions": [
                    {"id": "ahcf_smoking", "type": "single_select", "label": "Smoking / Vaping", "required": True, "options": ["Never Smoked", "Ex-Smoker", "Current Smoker", "Vaping"]},
                    {"id": "ahcf_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within Limits (<14 Units/Week)", "Excess (≥14 Units/Week)"]},
                    {"id": "ahcf_diet", "type": "single_select", "label": "Diet", "required": True, "options": ["Balanced / Mediterranean", "Fair", "Poor"]},
                    {"id": "ahcf_exercise", "type": "single_select", "label": "Exercise", "required": True, "options": ["Regular (≥150 Min/Week)", "Occasional", "Sedentary"]}
                ]
            },
            {
                "title": "Sleep, Mood & Stress",
                "section_type": "history",
                "questions": [
                    {"id": "ahcf_sleep", "type": "single_select", "label": "Sleep Quality", "required": True, "options": ["Good", "Fair", "Poor / Insomnia"]},
                    {"id": "ahcf_mood", "type": "single_select", "label": "Mood / Stress", "required": True, "options": ["Good - No Concerns", "Mild Stress / Low Mood", "Significant Stress / Anxiety", "Low Mood / ?Depression"]}
                ]
            },
            {
                "title": "Gynaecological History",
                "section_type": "history",
                "questions": [
                    {"id": "ahcf_lmp", "type": "text", "label": "Last Menstrual Period (LMP)", "required": False, "placeholder": "e.g., 2 weeks ago / Not applicable (post-menopausal)"},
                    {"id": "ahcf_cycle", "type": "single_select", "label": "Cycle Regularity", "required": False, "options": ["Regular", "Irregular", "Post-Menopausal", "Not Applicable"]},
                    {"id": "ahcf_menorrhagia", "type": "toggle", "label": "Menorrhagia / Heavy Periods?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Heavy menstrual bleeding = check FBC, ferritin. Consider pelvic USS.", "red_flag_negative": ""},
                    {"id": "ahcf_dysmenorrhoea", "type": "toggle", "label": "Dysmenorrhoea / Painful Periods?", "required": False},
                    {"id": "ahcf_contraception", "type": "single_select", "label": "Contraception", "required": False, "options": ["None", "COCP", "POP", "Implant", "IUS / IUD", "Depo-Provera", "Barrier", "Post-Menopausal / Not Needed"]},
                    {"id": "ahcf_sti_risk", "type": "toggle", "label": "STI Risk? (New/Multiple Partners, Unprotected Intercourse)", "required": False},
                    {"id": "ahcf_pregnancy_plans", "type": "toggle", "label": "Pregnancy Plans? (If Relevant)", "required": False},
                    {"id": "ahcf_menopausal", "type": "toggle", "label": "Menopausal Symptoms? (Hot Flushes, Night Sweats, Vaginal Dryness)", "required": False}
                ]
            },
            {
                "title": "Preventative Care",
                "section_type": "history",
                "questions": [
                    {"id": "ahcf_cervical_screening", "type": "single_select", "label": "Cervical Screening (Smear Test)", "required": True, "options": ["Up to Date", "Overdue - Advised Today", "Not Applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Overdue cervical screening = advise + arrange.", "red_flag_negative": ""},
                    {"id": "ahcf_breast_awareness", "type": "toggle", "label": "Breast Awareness Discussed?", "required": True},
                    {"id": "ahcf_vaccinations", "type": "multi_select", "label": "Vaccinations Up to Date?", "required": True, "options": ["Influenza (Annual)", "Pneumococcal", "Tetanus (10-Yearly)", "COVID-19 Booster", "HPV", "Not Up to Date - Advised"]},
                    {"id": "ahcf_screening", "type": "multi_select", "label": "Age-Appropriate Screening Up to Date?", "required": False, "options": ["Breast Screening (Mammogram 50-69)", "Bowel Screen (60-69)", "Not Applicable"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ahcf_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 118/76"},
                    {"id": "ahcf_hr", "type": "number", "label": "Pulse (bpm)", "required": True, "placeholder": "e.g., 72"},
                    {"id": "ahcf_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 24"},
                    {"id": "ahcf_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well, No Distress", "Overweight / Obese", "Pale / Unwell"]},
                    {"id": "ahcf_cvs", "type": "single_select", "label": "Cardiovascular Examination", "required": True, "options": ["HS I+II Audible, No Murmurs", "Murmur Present", "Irregular Pulse"]},
                    {"id": "ahcf_resp", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Clear B/L, Vesicular BS", "Abnormal"]},
                    {"id": "ahcf_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, Non-Tender, No Masses", "Abnormal"]},
                    {"id": "ahcf_skin", "type": "single_select", "label": "Skin Examination (If Indicated)", "required": False, "options": ["Normal", "Abnormal - Refer Dermatology", "Not Examined"]},
                    {"id": "ahcf_breast", "type": "single_select", "label": "Breast Examination (Only if Symptoms/Specific Concerns)", "required": False, "options": ["Normal", "Abnormal - Refer Breast Clinic", "Not Indicated / Not Examined"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Well Asymptomatic Female - Routine Health Check",
                    "?Iron Deficiency Anaemia (Menorrhagia)",
                    "?Hypothyroidism",
                    "?Metabolic Syndrome",
                    "?Perimenopause",
                    "?Vitamin D Deficiency"
                ],
                "questions": [
                    {"id": "ahcf_routine_bloods", "type": "multi_select", "label": "Routine Bloods Ordered", "required": False, "options": ["FBC", "U&E / Renal Profile", "LFTs", "Fasting Lipid Profile", "HbA1c"]},
                    {"id": "ahcf_indicated_bloods", "type": "multi_select", "label": "Additional Bloods (If Indicated by History/Exam)", "required": False, "options": ["Ferritin / Iron Studies (If Menorrhagia)", "TSH", "B12 / Folate", "Vitamin D", "Pregnancy Test", "Hormonal Profile (If Clinically Indicated)", "None"]},
                    {"id": "ahcf_urinalysis", "type": "toggle", "label": "Urinalysis?", "required": False},
                    {"id": "ahcf_sti_screen", "type": "toggle", "label": "STI Screen?", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: new symptoms develop, weight loss, night sweats, fatigue, abnormal bleeding, breast changes, or any concerning changes before next routine check. Lifestyle advice: healthy diet, exercise ≥150 minutes/week, smoking cessation, alcohol moderation. Encourage breast awareness and participation in cervical screening (if applicable). Review vaccinations and age-appropriate screening (mammogram 50-69, bowel screen 60-69). Follow up with blood results in 1-2 weeks. If menorrhagia: check FBC + ferritin, consider pelvic USS. If menopausal symptoms: discuss HRT if appropriate.",
                "questions": [
                    {"id": "ahcf_diagnosis", "type": "single_select", "label": "Assessment", "required": True, "options": ["Well Asymptomatic Female - Routine Health Check", "Abnormal Findings - Requires Further Investigation", "Red Flags Present - NOT Routine Check"]},
                    {"id": "ahcf_lifestyle_advice", "type": "multi_select", "label": "Lifestyle Advice Given", "required": False, "options": ["Healthy Diet", "Exercise ≥150 Min/Week", "Smoking Cessation", "Alcohol Moderation", "Weight Management"]},
                    {"id": "ahcf_breast_awareness", "type": "toggle", "label": "Breast Awareness Encouraged?", "required": False},
                    {"id": "ahcf_cervical_screening_advice", "type": "toggle", "label": "Cervical Screening Participation Encouraged?", "required": False},
                    {"id": "ahcf_vaccination_review", "type": "toggle", "label": "Vaccinations + Screening Reviewed?", "required": False},
                    {"id": "ahcf_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1-2 weeks with blood results, sooner if concerns"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_health_check_female()