from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_tatt_female():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Tired All The Time (TATT) - Female",
        "description": "Comprehensive assessment for fatigue in women covering sleep history, systems review, red flags for malignancy, and investigation pathways.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Fatigue Characteristics",
                "section_type": "history",
                "questions": [
                    {"id": "tatt_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Feeling tired all the time for 6 weeks"},
                    {"id": "tatt_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 38"},
                    {"id": "tatt_duration", "type": "single_select", "label": "Duration", "required": True, "options": ["<1 week", "1-2 weeks", "3 weeks", ">4 weeks"]},
                    {"id": "tatt_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Throughout the day", "Morning only", "Evening only", "Post-exertional only"]},
                    {"id": "tatt_trajectory", "type": "single_select", "label": "Trajectory", "required": True, "options": ["Stable", "Improving", "Worsening"]},
                    {"id": "tatt_functional_impact", "type": "multi_select", "label": "Functional Impact", "required": True, "options": ["Limits household tasks", "Does not limit household tasks", "Limits work", "Limits self-care"]}
                ]
            },
            {
                "title": "Sleep History",
                "section_type": "history",
                "questions": [
                    {"id": "tatt_sleep_times", "type": "text", "label": "Bedtime / Wake Time", "required": False, "placeholder": "e.g., 11pm bed, 7am wake"},
                    {"id": "tatt_refreshed", "type": "toggle", "label": "Feels Refreshed After Sleep?", "required": True},
                    {"id": "tatt_screen_time", "type": "single_select", "label": "Screen Use Before Bed", "required": False, "options": ["None after 9.30pm", "Screen use within 1 hour of bed", "No restriction"]},
                    {"id": "tatt_napping", "type": "toggle", "label": "Daytime Napping?", "required": False},
                    {"id": "tatt_snoring_apnoea", "type": "multi_select", "label": "Snoring / Apnoeic Episodes (Partner-Reported)", "required": False, "options": ["Snoring", "Choking / gasping", "Cessation of breathing (apnoeas)", "None reported"]}
                ]
            },
            {
                "title": "Precipitants & General",
                "section_type": "history",
                "questions": [
                    {"id": "tatt_precipitants", "type": "single_select", "label": "Precipitating Factors", "required": False, "options": ["Recent illness", "Recent stressful event", "Neither"]},
                    {"id": "tatt_mood", "type": "single_select", "label": "Mood / Psychological Screen", "required": True, "options": ["Low mood / stress / anxiety", "None - good interest in life and hobbies maintained"]},
                    {"id": "tatt_substances", "type": "multi_select", "label": "Substance / Lifestyle", "required": False, "options": ["Alcohol excess", "Recreational drugs", "Smoking", "Recent travel", "None"]},
                    {"id": "tatt_menstrual", "type": "text", "label": "Menstrual History", "required": False, "placeholder": "e.g., LMP 1 month ago, regular, not heavy"}
                ]
            },
            {
                "title": "Systems Review - GI & Cardiorespiratory",
                "section_type": "history",
                "questions": [
                    {"id": "tatt_gi", "type": "multi_select", "label": "GI Symptoms", "required": False, "options": ["Bloating", "Steatorrhoea (fatty stools)", "PR bleeding", "None"]},
                    {"id": "tatt_cardioresp", "type": "multi_select", "label": "Cardiorespiratory Symptoms", "required": False, "options": ["Tiredness on exertion (fatigability)", "Shortness of breath", "Neither"]},
                    {"id": "tatt_diabetes_screen", "type": "multi_select", "label": "Diabetes Symptoms", "required": False, "options": ["Polyuria", "Polydipsia", "Recent weight change", "None"]},
                    {"id": "tatt_postural", "type": "toggle", "label": "Postural Symptoms? (Dizziness on standing - ?Addison's)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postural symptoms + fatigue + hyperpigmentation = ?Addison's. Check cortisol urgently.", "red_flag_negative": ""},
                    {"id": "tatt_temperature", "type": "single_select", "label": "Temperature Intolerance", "required": True, "options": ["Cold intolerance (?hypothyroid)", "Heat intolerance (?hyperthyroid)", "Neither - feels fine relative to others"]}
                ]
            },
            {
                "title": "Red Flags - Malignancy & Inflammatory",
                "section_type": "history",
                "questions": [
                    {"id": "tatt_malignancy", "type": "multi_select", "label": "Malignancy Red Flags", "required": True, "options": ["PR bleeding", "Haematuria", "Haemoptysis", "Breast lump", "Night sweats", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Malignancy red flags present = urgent investigation. 2WW if indicated.", "red_flag_negative": ""},
                    {"id": "tatt_msk", "type": "multi_select", "label": "Musculoskeletal (Myositis / PMR)", "required": False, "options": ["Shoulder girdle pain/weakness", "Pelvic girdle pain/weakness", "Muscle tenderness", "None"]},
                    {"id": "tatt_joint", "type": "multi_select", "label": "Joint Symptoms (Inflammatory Arthritis)", "required": False, "options": ["Morning stiffness >30 mins", "Difficulty turning over in bed", "Neither"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "tatt_general", "type": "multi_select", "label": "General Appearance", "required": True, "options": ["Looks clinically well", "Looks unwell", "Pallor (anaemia)", "Jaundice"]},
                    {"id": "tatt_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": False, "placeholder": "e.g., 128/82"},
                    {"id": "tatt_cvs", "type": "single_select", "label": "Cardiovascular", "required": False, "options": ["HS I+II audible, no murmurs, regular", "Murmur present", "Irregular rhythm (AF)", "Added sounds"]},
                    {"id": "tatt_resp", "type": "single_select", "label": "Respiratory", "required": False, "options": ["Clear B/L, vesicular BS, no clubbing", "Reduced air entry", "Added sounds", "Clubbing present"]},
                    {"id": "tatt_abdo", "type": "single_select", "label": "Abdominal", "required": False, "options": ["Soft, non-tender, no masses", "Tenderness", "Organomegaly", "Mass palpated", "Distension"]},
                    {"id": "tatt_lymph", "type": "multi_select", "label": "Lymphadenopathy", "required": False, "options": ["Axillary", "Supraclavicular", "Inguinal", "None palpable"]},
                    {"id": "tatt_msk_exam", "type": "single_select", "label": "Musculoskeletal", "required": False, "options": ["No tenderness, muscles non-tender", "Tenderness present", "Weakness present"]},
                    {"id": "tatt_thyroid", "type": "multi_select", "label": "Thyroid / Endocrine", "required": False, "options": ["Goitre", "Proptosis", "Lymphadenopathy", "None present"]},
                    {"id": "tatt_neuro_peripheral", "type": "multi_select", "label": "Neurological / Peripheral Signs", "required": False, "options": ["Tremor", "Proximal myopathy", "Neither"]},
                    {"id": "tatt_reflexes", "type": "single_select", "label": "Reflexes", "required": False, "options": ["Abnormal (brisk/slow-relaxing)", "Normal"]},
                    {"id": "tatt_skin", "type": "single_select", "label": "Skin / Hair", "required": False, "options": ["Abnormal", "Normal"]},
                    {"id": "tatt_pigmentation", "type": "toggle", "label": "Skin Hyperpigmentation? (?Addison's)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hyperpigmentation + fatigue = ?Addison's disease. Check cortisol urgently.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Iron Deficiency Anaemia",
                    "Hypothyroidism / Hyperthyroidism",
                    "Diabetes Mellitus",
                    "Coeliac Disease",
                    "Chronic Fatigue Syndrome / ME",
                    "Sleep Apnoea",
                    "Depression / Anxiety",
                    "Addison's Disease",
                    "Malignancy (lymphoma, GI, breast)",
                    "Inflammatory Arthritis / PMR / Myositis",
                    "Post-Viral Fatigue",
                    "Vitamin B12 / Folate Deficiency",
                    "Chronic Kidney Disease"
                ],
                "questions": [
                    {"id": "tatt_first_line", "type": "multi_select", "label": "First-Line Investigations (if symptomatic >1 month)", "required": False, "options": ["Urine dip (glucose, protein, blood)", "FBC", "TFTs (TSH, Free T4)", "ESR / CRP", "Monospot (EBV IgM - if <40)", "Haematinics (Ferritin, B12, Folate)", "Bone / Liver profile (Ca, ALP, LFTs)", "Coeliac screen (IgA TTG + IgA)", "Fasting Glucose / HbA1c", "Fasting Lipids", "HIV screen", "Hepatitis B screen"]},
                    {"id": "tatt_second_line", "type": "multi_select", "label": "Second-Line (if no improvement)", "required": False, "options": ["Ultrasound abdomen", "Chest X-Ray", "CA-125", "Serum Protein Electrophoresis (SPEP)", "Serum Free Light Chains", "Urinary Bence Jones Protein", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: new red flags develop (weight loss, night sweats, bleeding, lumps), symptoms worsen significantly, or no improvement after 1 month of lifestyle measures. Sleep hygiene: bedroom for sleep only, wake at same time daily, avoid daytime napping, no screen time after 9.30pm. Regular exercise (even when tired - improves energy). Avoid caffeine after 2pm. Avoid alcohol. If red flags present: investigate now. If no red flags + normal exam: watchful wait 1 month with lifestyle measures before investigating. If all tests normal + persistent symptoms >6 months: consider CFS/ME diagnosis.",
                "questions": [
                    {"id": "tatt_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["TATT - no red flags, likely behavioural/sleep", "TATT - red flags present, urgent investigation", "TATT - likely underlying organic cause", "TATT - likely psychological/stress-related"]},
                    {"id": "tatt_plan", "type": "single_select", "label": "Initial Approach", "required": True, "options": ["Watchful wait - investigate if persists at 1 month", "Investigate now - red flags present", "Lifestyle advice + safety-net"]},
                    {"id": "tatt_lifestyle", "type": "multi_select", "label": "Lifestyle / Behavioural Advice", "required": False, "options": ["Sleep hygiene - room for sleep only", "Wake at same time daily", "Avoid daytime napping", "No screen time after 9.30pm", "Regular exercise", "Avoid caffeine after 2pm", "Avoid alcohol"]},
                    {"id": "tatt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 1 month if persists, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_tatt_female()