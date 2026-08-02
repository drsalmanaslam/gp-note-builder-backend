from app.database import SessionLocal
from app.models import User, Template

def seed_smoking_cessation():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Smoking Cessation"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Smoking cessation consultation covering pack-year history, Fagerstrom dependence score, CO monitoring, NRT/varenicline/bupropion options per NICE PH48, and behavioural support.", category="General Practice", content={"sections": [
        {"title": "Smoking History", "section_type": "history", "questions": [
            {"id": "smoke_current", "type": "number", "label": "Cigarettes per Day", "required": True, "placeholder": "e.g., 20"},
            {"id": "smoke_years", "type": "number", "label": "Years Smoked", "required": True, "placeholder": "e.g., 25"},
            {"id": "smoke_pack_years", "type": "number", "label": "Pack-Years", "required": False, "placeholder": "e.g., 25"},
            {"id": "smoke_type", "type": "multi_select", "label": "Type", "required": True, "options": ["Manufactured cigarettes", "Roll-ups", "Cigars/pipe", "Vaping", "Cannabis mixed"]},
            {"id": "smoke_first", "type": "single_select", "label": "Time to First Cigarette After Waking", "required": True, "options": ["<5 minutes (Score 3)", "5-30 minutes (Score 2)", "31-60 minutes (Score 1)", ">60 minutes (Score 0)"]},
            {"id": "smoke_previous_attempts", "type": "toggle", "label": "Previous Quit Attempts?", "required": True},
            {"id": "smoke_methods_tried", "type": "multi_select", "label": "Methods Tried", "required": False, "options": ["Cold turkey", "NRT", "Varenicline (Champix)", "Bupropion (Zyban)", "E-cigarettes", "Behavioural support"]},
            {"id": "smoke_longest_quit", "type": "text", "label": "Longest Period Quit", "required": False, "placeholder": "e.g., 6 months in 2023"},
            {"id": "smoke_motivation", "type": "single_select", "label": "Motivation to Quit (0-10)", "required": True, "options": ["0-3: Not ready", "4-6: Considering", "7-8: Ready", "9-10: Determined"]},
            {"id": "smoke_co_level", "type": "number", "label": "Exhaled CO Level (ppm)", "required": False, "placeholder": "e.g., 18"},
            {"id": "smoke_triggers", "type": "multi_select", "label": "Triggers", "required": False, "options": ["Stress", "Alcohol", "After meals", "Social situations", "Boredom", "Driving", "Coffee/tea"]}
        ]},
        {"title": "Medical History", "section_type": "history", "questions": [
            {"id": "smoke_pregnancy", "type": "toggle", "label": "Pregnant / Planning?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pregnancy = offer NRT (not varenicline/bupropion). Behavioural support first-line.", "red_flag_negative": ""},
            {"id": "smoke_cvd", "type": "toggle", "label": "Cardiovascular Disease?", "required": True},
            {"id": "smoke_respiratory", "type": "toggle", "label": "COPD / Asthma?", "required": True},
            {"id": "smoke_mental_health", "type": "toggle", "label": "Mental Health Condition?", "required": True},
            {"id": "smoke_medications", "type": "text", "label": "Current Medications", "required": False, "placeholder": "e.g., Ramipril, Sertraline"}
        ]},
        {"title": "Treatment Plan", "section_type": "plan", "safety_netting": "Set a quit date. Remove all cigarettes/lighters/ashtrays from home. Identify triggers and plan alternatives. Warn about withdrawal: irritability, craving, anxiety, increased appetite (peak 2-4 weeks). Weight gain average 4-5kg - can be managed. Varenicline: monitor for neuropsychiatric symptoms (mood changes, suicidal ideation). Return if: severe depression, suicidal thoughts, or rash (bupropion). Combination NRT (patch + PRN) more effective than single product.", "questions": [
            {"id": "smoke_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Brief advice + leaflet", "Refer to stop smoking service", "NRT - Patch (16h/24h)", "NRT - Gum/Lozenge/Inhalator PRN", "Combination NRT (patch + PRN)", "Varenicline (Champix)", "Bupropion (Zyban)", "E-cigarettes discussed", "Behavioural support/counselling"]},
            {"id": "smoke_quit_date", "type": "text", "label": "Quit Date Set", "required": False, "placeholder": "e.g., 15/08/2026"},
            {"id": "smoke_prescription", "type": "text", "label": "Prescription", "required": False, "placeholder": "e.g., NRT 21mg/24h patch + 2mg gum PRN"},
            {"id": "smoke_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 2 weeks - check CO, adherence, side effects"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_smoking_cessation()