from app.database import SessionLocal
from app.models import User, Template, Category

def seed_tiredness():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "General").first()
    if not category: category = Category(name="General"); db.add(category); db.commit()

    t = {
        "title": "Tiredness / Fatigue Assessment",
        "description": "Systematic assessment for tiredness and fatigue including red flags, common causes, and investigations.",
        "category": "General",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "tire_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Feeling tired all the time for 3 months"},
                    {"id": "tire_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 42"},
                    {"id": "tire_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3 months", "is_red_flag": True, "red_flag_positive": "RED FLAG: Fatigue >2 weeks with unexplained weight loss, fever, or night sweats = ?malignancy. Urgent investigation.", "red_flag_negative": ""},
                    {"id": "tire_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (days-weeks)", "Gradual (weeks-months)", "Long-standing (>6 months)"]},
                    {"id": "tire_severity", "type": "single_select", "label": "Impact on Daily Life", "required": True, "options": ["Mild - functioning normally", "Moderate - reduced activities", "Severe - unable to work/function", "Bed-bound"]},
                    {"id": "tire_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Worst in morning", "Worst in afternoon/evening", "Constant throughout day", "Fluctuating", "After exertion (post-exertional malaise)"]},
                    {"id": "tire_sleep_quality", "type": "single_select", "label": "Sleep Quality", "required": True, "options": ["Good - refreshed on waking", "Poor - unrefreshed despite adequate sleep", "Insomnia", "Excessive sleep (>10 hours)", "Shift work"]}
                ]
            },
            {
                "title": "RED FLAGS - Malignancy & Serious Causes",
                "section_type": "history",
                "questions": [
                    {"id": "tire_weight_loss", "type": "toggle", "label": "Unexplained Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + fatigue = ?malignancy, TB, hyperthyroidism. Urgent CXR, bloods, ?2WW.", "red_flag_negative": ""},
                    {"id": "tire_night_sweats", "type": "toggle", "label": "Drenching Night Sweats?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Night sweats + fatigue = ?lymphoma, TB, infection. Urgent CXR + bloods.", "red_flag_negative": ""},
                    {"id": "tire_fever", "type": "toggle", "label": "Fever?", "required": False},
                    {"id": "tire_lymph_nodes", "type": "toggle", "label": "Lumps / Swollen Glands?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy + fatigue = ?lymphoma, leukaemia, infection. Examine + FBC urgently.", "red_flag_negative": ""},
                    {"id": "tire_bleeding", "type": "toggle", "label": "Easy Bruising / Bleeding?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bleeding + fatigue = ?leukaemia, bone marrow failure. Urgent FBC.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "tire_sob", "type": "toggle", "label": "Shortness of Breath? (Anaemia/Heart failure)", "required": False},
                    {"id": "tire_palpitations", "type": "toggle", "label": "Palpitations? (Anaemia/Thyroid)", "required": False},
                    {"id": "tire_dizziness", "type": "toggle", "label": "Dizziness / Lightheadedness? (Anaemia)", "required": False},
                    {"id": "tire_pallor", "type": "toggle", "label": "Looking Pale? (Anaemia)", "required": False},
                    {"id": "tire_weight_gain", "type": "toggle", "label": "Weight Gain? (Hypothyroidism)", "required": False},
                    {"id": "tire_cold_intolerance", "type": "toggle", "label": "Cold Intolerance? (Hypothyroidism)", "required": False},
                    {"id": "tire_constipation", "type": "toggle", "label": "Constipation? (Hypothyroidism)", "required": False},
                    {"id": "tire_dry_skin_hair", "type": "toggle", "label": "Dry Skin / Hair Loss? (Hypothyroidism)", "required": False},
                    {"id": "tire_heat_intolerance", "type": "toggle", "label": "Heat Intolerance / Tremor? (Hyperthyroidism)", "required": False},
                    {"id": "tire_polyuria_thirst", "type": "toggle", "label": "Increased Thirst / Urination? (Diabetes)", "required": False},
                    {"id": "tire_low_mood", "type": "toggle", "label": "Low Mood / Anhedonia? (Depression)", "required": True},
                    {"id": "tire_stress", "type": "toggle", "label": "Significant Stress / Burnout?", "required": True},
                    {"id": "tire_snoring", "type": "toggle", "label": "Snoring / Apnoeas? (Sleep apnoea)", "required": False}
                ]
            },
            {
                "title": "Lifestyle & Diet",
                "section_type": "history",
                "questions": [
                    {"id": "tire_diet", "type": "single_select", "label": "Diet", "required": False, "options": ["Balanced", "Poor / irregular meals", "Vegetarian/Vegan", "Restrictive dieting", "Skipping meals"]},
                    {"id": "tire_caffeine", "type": "single_select", "label": "Caffeine Intake", "required": False, "options": ["None", "1-2/day", "3-5/day", ">5/day"]},
                    {"id": "tire_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess (>14 units/week)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol excess can cause fatigue through liver disease, nutritional deficiency, sleep disruption.", "red_flag_negative": ""},
                    {"id": "tire_exercise", "type": "single_select", "label": "Exercise", "required": False, "options": ["Regular", "Occasional", "None - sedentary"]},
                    {"id": "tire_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]}
                ]
            },
            {
                "title": "Past History & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "tire_pmh", "type": "multi_select", "label": "Relevant PMHx", "required": False, "options": ["Diabetes", "Hypothyroidism", "Anaemia", "Coeliac disease", "CKD", "Liver disease", "Heart failure", "Autoimmune disease", "Depression/Anxiety", "Cancer history", "None"]},
                    {"id": "tire_meds", "type": "multi_select", "label": "Medications That Cause Fatigue", "required": False, "options": ["Beta-blockers", "Antihistamines", "Benzodiazepines", "Antidepressants", "Antipsychotics", "Opioids", "Steroids", "Chemotherapy", "None"]},
                    {"id": "tire_pregnancy", "type": "toggle", "label": "Possible Pregnancy?", "required": False},
                    {"id": "tire_postviral", "type": "toggle", "label": "Recent Viral Illness / COVID?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "tire_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well-appearing", "Pale", "Tired/fatigued appearance", "Obese", "Cachectic", "Depressed affect"]},
                    {"id": "tire_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 28", "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI >30 = consider sleep apnoea. BMI <18.5 = consider malnutrition/malignancy.", "red_flag_negative": ""},
                    {"id": "tire_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": False, "placeholder": "e.g., 118/76"},
                    {"id": "tire_hr", "type": "number", "label": "Heart Rate (bpm)", "required": False, "placeholder": "e.g., 72"},
                    {"id": "tire_conjunctival_pallor", "type": "toggle", "label": "Conjunctival Pallor? (Anaemia)", "required": False},
                    {"id": "tire_lymph_exam", "type": "toggle", "label": "Lymphadenopathy?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy = ?lymphoma, leukaemia, infection. Urgent FBC.", "red_flag_negative": ""},
                    {"id": "tire_thyroid_exam", "type": "toggle", "label": "Goitre / Thyroid Nodule?", "required": False},
                    {"id": "tire_other_exam", "type": "textarea", "label": "Other Examination Findings", "required": False, "placeholder": "Describe any other findings..."}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Iron Deficiency Anaemia",
                    "Vitamin B12 / Folate Deficiency",
                    "Hypothyroidism",
                    "Hyperthyroidism",
                    "Diabetes Mellitus",
                    "Chronic Kidney Disease",
                    "Coeliac Disease",
                    "Obstructive Sleep Apnoea",
                    "Depression / Anxiety",
                    "Burnout / Stress",
                    "Post-viral Fatigue / Long COVID",
                    "Chronic Fatigue Syndrome / ME",
                    "Malignancy (lymphoma, leukaemia, solid tumours)",
                    "Liver Disease",
                    "Heart Failure",
                    "Autoimmune Disease (SLE, RA)",
                    "Medication Side Effect",
                    "Alcohol Excess",
                    "Poor Diet / Nutritional Deficiency",
                    "Pregnancy"
                ],
                "questions": [
                    {"id": "tire_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "Ferritin / Iron Studies", "B12 / Folate", "TSH / Free T4", "HbA1c / Fasting Glucose", "U&E / Creatinine / eGFR", "LFTs", "Coeliac Screen (tTG-IgA)", "CRP / ESR", "EBV / CMV Serology", "Cortisol (if Addison's suspected)"]},
                    {"id": "tire_other_tests", "type": "multi_select", "label": "Other Tests", "required": False, "options": ["Urinalysis", "Pregnancy test", "Chest X-Ray", "Sleep study (if OSA suspected)", "PHQ-9 (depression screen)", "GAD-7 (anxiety screen)", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: new weight loss, night sweats, fevers, lumps/swollen glands, bruising/bleeding, or symptoms significantly worsen. If investigations normal: reassure, lifestyle advice (sleep hygiene, regular exercise, balanced diet, reduce caffeine/alcohol, stress management). Consider CBT if low mood/anxiety. If OSA suspected - refer respiratory/sleep clinic. If post-viral - advise gradual return to activity, energy management. Review with blood results in 2-4 weeks. If no improvement and all tests normal - consider CFS/ME diagnosis if symptoms >6 months with post-exertional malaise.",
                "questions": [
                    {"id": "tire_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Anaemia", "?Hypothyroidism", "?Diabetes", "?Depression/Burnout", "?Sleep apnoea", "?Post-viral fatigue", "?CFS/ME", "?Malignancy - urgent", "Lifestyle-related", "Uncertain - awaiting results"]},
                    {"id": "tire_plan", "type": "multi_select", "label": "Management", "required": False, "options": ["Reassurance + lifestyle advice", "Treat underlying cause", "Iron replacement", "B12 replacement", "Levothyroxine", "Antidepressants", "Sleep hygiene advice", "Exercise program", "Stress management", "Referral"]},
                    {"id": "tire_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None", "Haematology (urgent)", "Haematology (routine)", "Endocrinology", "Respiratory (sleep study)", "Psychiatry/Psychology", "Dietitian", "Infectious diseases"]},
                    {"id": "tire_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2-4 weeks with blood results"}
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
    seed_tiredness()