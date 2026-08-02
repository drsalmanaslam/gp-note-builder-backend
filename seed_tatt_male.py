from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_tatt_male():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Tired All The Time (TATT) - Male",
        "description": "Comprehensive assessment for fatigue in men covering sleep history, OSA screening, systems review, red flags for malignancy, and VAMPIRE trial evidence-based investigation pathways.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "Fatigue Characteristics",
                "section_type": "history",
                "questions": [
                    {"id": "tattm_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Feeling exhausted all the time for 2 months"},
                    {"id": "tattm_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 45"},
                    {"id": "tattm_duration", "type": "single_select", "label": "Duration", "required": True, "options": ["<1 week", "1-2 weeks", "3 weeks", ">4 weeks"]},
                    {"id": "tattm_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Throughout the day", "Morning only", "Evening only", "Post-exertional only"]},
                    {"id": "tattm_trajectory", "type": "single_select", "label": "Trajectory", "required": True, "options": ["Stable", "Improving", "Worsening"]},
                    {"id": "tattm_functional_impact", "type": "multi_select", "label": "Functional Impact", "required": True, "options": ["Limits household tasks", "Does not limit household tasks", "Limits work", "Limits self-care"]}
                ]
            },
            {
                "title": "Sleep History & OSA Screening",
                "section_type": "history",
                "questions": [
                    {"id": "tattm_sleep_times", "type": "text", "label": "Bedtime / Wake Time", "required": False, "placeholder": "e.g., 12am bed, 6.30am wake"},
                    {"id": "tattm_refreshed", "type": "toggle", "label": "Feels Refreshed After Sleep?", "required": True},
                    {"id": "tattm_screen_time", "type": "single_select", "label": "Screen Use Before Bed", "required": False, "options": ["None prior to bed", "Screen use within 1 hour of bed", "No restriction"]},
                    {"id": "tattm_napping", "type": "toggle", "label": "Daytime Napping?", "required": False},
                    {"id": "tattm_snoring_apnoea", "type": "multi_select", "label": "Snoring / Apnoeic Episodes (Partner-Reported) - OSA Screen", "required": False, "options": ["Snoring", "Choking / gasping", "Cessation of breathing (apnoeas)", "None reported"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Snoring + apnoeas + unrefreshing sleep + daytime fatigue = ?OSA. Refer sleep clinic.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Precipitants & General",
                "section_type": "history",
                "questions": [
                    {"id": "tattm_precipitants", "type": "single_select", "label": "Precipitating Factors", "required": False, "options": ["Recent illness", "Recent stressful event", "Neither"]},
                    {"id": "tattm_mood", "type": "single_select", "label": "Mood / Psychological Screen", "required": True, "options": ["Low mood / stress / anxiety", "None - good interest in life and hobbies maintained"]},
                    {"id": "tattm_substances", "type": "multi_select", "label": "Substance / Lifestyle", "required": False, "options": ["Alcohol excess", "Recreational drugs", "Smoking", "Recent travel", "None"]}
                ]
            },
            {
                "title": "Systems Review - GI & Cardiorespiratory",
                "section_type": "history",
                "questions": [
                    {"id": "tattm_gi", "type": "multi_select", "label": "GI Symptoms (Malabsorption Screen)", "required": False, "options": ["Bloating", "Steatorrhoea (fatty stools - ?coeliac)", "PR bleeding", "None"]},
                    {"id": "tattm_cardioresp", "type": "multi_select", "label": "Cardiorespiratory (Fatigability Screen)", "required": False, "options": ["Tiredness on exertion (fatigability)", "Shortness of breath", "Neither"]},
                    {"id": "tattm_diabetes_screen", "type": "multi_select", "label": "Diabetes Symptoms", "required": False, "options": ["Polyuria", "Polydipsia", "Recent weight change", "None"]},
                    {"id": "tattm_postural", "type": "toggle", "label": "Postural Dizziness? (?Addison's)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postural symptoms + fatigue + hyperpigmentation = ?Addison's. Check cortisol urgently.", "red_flag_negative": ""},
                    {"id": "tattm_temperature", "type": "single_select", "label": "Temperature Intolerance", "required": True, "options": ["Cold intolerance (?hypothyroid)", "Heat intolerance (?hyperthyroid)", "Neither - feels fine relative to others"]}
                ]
            },
            {
                "title": "Red Flags - Malignancy & Inflammatory",
                "section_type": "history",
                "questions": [
                    {"id": "tattm_malignancy", "type": "multi_select", "label": "Malignancy Red Flags", "required": True, "options": ["PR bleeding", "Haematuria", "Haemoptysis", "Night sweats", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Malignancy red flags present = urgent investigation. 2WW if indicated.", "red_flag_negative": ""},
                    {"id": "tattm_msk", "type": "multi_select", "label": "Musculoskeletal (Myositis / PMR)", "required": False, "options": ["Shoulder girdle pain/weakness", "Pelvic girdle pain/weakness", "Muscle tenderness", "None"]},
                    {"id": "tattm_joint", "type": "multi_select", "label": "Joint Symptoms (Inflammatory Arthritis)", "required": False, "options": ["Morning stiffness >30 mins", "Difficulty turning over in bed", "Neither"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "tattm_general", "type": "multi_select", "label": "General Appearance", "required": True, "options": ["Looks clinically well", "Looks unwell", "Pallor (anaemia)", "Jaundice"]},
                    {"id": "tattm_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": False, "placeholder": "e.g., 128/82"},
                    {"id": "tattm_cvs", "type": "single_select", "label": "Cardiovascular", "required": False, "options": ["HS I+II audible, no murmurs, regular", "Murmur present", "Irregular rhythm (AF)", "Added sounds"]},
                    {"id": "tattm_resp", "type": "single_select", "label": "Respiratory", "required": False, "options": ["Clear B/L, vesicular BS, no clubbing", "Reduced air entry", "Added sounds", "Clubbing present"]},
                    {"id": "tattm_abdo", "type": "single_select", "label": "Abdominal", "required": False, "options": ["Soft, non-tender, no masses", "Tenderness", "Organomegaly", "Mass palpated", "Distension"]},
                    {"id": "tattm_lymph", "type": "multi_select", "label": "Lymphadenopathy", "required": False, "options": ["Axillary", "Supraclavicular", "Inguinal", "None palpable"]},
                    {"id": "tattm_msk_exam", "type": "single_select", "label": "Musculoskeletal", "required": False, "options": ["No tenderness, muscles non-tender", "Tenderness present", "Weakness present"]},
                    {"id": "tattm_thyroid", "type": "multi_select", "label": "Thyroid / Endocrine", "required": False, "options": ["Goitre", "Proptosis", "Lymphadenopathy", "None present"]},
                    {"id": "tattm_neuro_peripheral", "type": "multi_select", "label": "Neurological / Peripheral Signs", "required": False, "options": ["Tremor", "Proximal myopathy", "Neither"]},
                    {"id": "tattm_reflexes", "type": "single_select", "label": "Reflexes", "required": False, "options": ["Abnormal (brisk/slow-relaxing)", "Normal"]},
                    {"id": "tattm_skin", "type": "single_select", "label": "Skin / Hair", "required": False, "options": ["Abnormal", "Normal"]},
                    {"id": "tattm_pigmentation", "type": "toggle", "label": "Skin Hyperpigmentation? (?Addison's)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hyperpigmentation + fatigue = ?Addison's disease. Check cortisol urgently.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Obstructive Sleep Apnoea (OSA)",
                    "Iron Deficiency Anaemia",
                    "Hypothyroidism / Hyperthyroidism",
                    "Diabetes Mellitus",
                    "Coeliac Disease",
                    "Depression / Anxiety",
                    "Addison's Disease",
                    "Malignancy (lymphoma, GI, lung)",
                    "Inflammatory Arthritis / PMR / Myositis",
                    "Post-Viral Fatigue / CFS",
                    "Vitamin B12 / Folate Deficiency",
                    "Chronic Kidney Disease",
                    "Alcohol Excess",
                    "Medication Side Effect"
                ],
                "questions": [
                    {"id": "tattm_first_line", "type": "multi_select", "label": "First-Line Investigations (if symptomatic >1 month)", "required": False, "options": ["Urine dip (glucose, protein, blood)", "FBC", "TFTs (TSH, Free T4)", "ESR / CRP", "Monospot (EBV IgM - if <40)", "Haematinics (Ferritin, B12, Folate)", "Bone / Liver profile (Ca, ALP, LFTs)", "Coeliac screen (IgA TTG + IgA)", "Fasting Glucose / HbA1c", "Fasting Lipids", "HIV screen", "Hepatitis B screen"]},
                    {"id": "tattm_second_line", "type": "multi_select", "label": "Second-Line (if no improvement)", "required": False, "options": ["Ultrasound abdomen", "Chest X-Ray", "SPEP (Serum Protein Electrophoresis)", "Serum Free Light Chains", "Urinary Bence Jones Protein", "Sleep study (if OSA suspected)", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: new red flags develop (weight loss, night sweats, bleeding, lumps), symptoms worsen significantly, or no improvement after 1 month of lifestyle measures. VAMPIRE trial (BJGP 2009): in red-flag-negative fatigue, delaying investigation for 1 month caused no harm - 92% had no lab abnormalities, only 17% still symptomatic at 4 weeks. Basic tests (FBC, TSH, ESR, glucose) show similar detection rates to comprehensive panels. Sleep hygiene: bedroom for sleep only, wake at same time daily, avoid daytime napping, no screen time after 9.30pm. Regular exercise. Avoid caffeine after 2pm, avoid alcohol. If snoring/apnoeas + daytime fatigue: refer sleep clinic for OSA assessment. If all tests normal + persistent >6 months: consider CFS/ME.",
                "questions": [
                    {"id": "tattm_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["TATT - no red flags, likely behavioural/sleep", "TATT - red flags present, urgent investigation", "TATT - likely underlying organic cause", "TATT - ?OSA (snoring + apnoeas + fatigue)", "TATT - likely psychological/stress-related"]},
                    {"id": "tattm_plan", "type": "single_select", "label": "Initial Approach (VAMPIRE Trial)", "required": True, "options": ["Watchful wait - investigate if persists at 1 month", "Investigate now - red flags present", "Lifestyle advice + safety-net"]},
                    {"id": "tattm_lifestyle", "type": "multi_select", "label": "Lifestyle / Behavioural Advice", "required": False, "options": ["Sleep hygiene - room for sleep only", "Wake at same time daily", "Avoid daytime napping", "No screen time after 9.30pm", "Regular exercise", "Avoid caffeine after 2pm", "Avoid alcohol"]},
                    {"id": "tattm_osa_referral", "type": "toggle", "label": "Refer Sleep Clinic for OSA Assessment?", "required": False},
                    {"id": "tattm_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 1 month if persists, sooner if red flags"}
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
    seed_tatt_male()