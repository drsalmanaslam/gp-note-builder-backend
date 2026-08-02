from app.database import SessionLocal
from app.models import User, Template

def seed_alcohol_audit():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Alcohol Brief Intervention (AUDIT-C)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Alcohol use screening using AUDIT-C, brief intervention, assessment of dependence, withdrawal risk, and referral pathways per NICE CG115.", category="General Practice", content={"sections": [
        {"title": "AUDIT-C Screening", "section_type": "history", "questions": [
            {"id": "alc_audit1", "type": "single_select", "label": "How often do you have a drink containing alcohol?", "required": True, "options": ["Never (0)", "Monthly or less (1)", "2-4 times/month (2)", "2-3 times/week (3)", "4+ times/week (4)"]},
            {"id": "alc_audit2", "type": "single_select", "label": "How many drinks on a typical day when drinking?", "required": True, "options": ["1-2 (0)", "3-4 (1)", "5-6 (2)", "7-9 (3)", "10+ (4)"]},
            {"id": "alc_audit3", "type": "single_select", "label": "How often do you have 6+ drinks on one occasion?", "required": True, "options": ["Never (0)", "Less than monthly (1)", "Monthly (2)", "Weekly (3)", "Daily/almost daily (4)"]},
            {"id": "alc_auditc_score", "type": "number", "label": "AUDIT-C Score (/12)", "required": True, "placeholder": "e.g., 7"},
            {"id": "alc_auditc_positive", "type": "toggle", "label": "AUDIT-C ≥5? (Positive screen - needs full AUDIT)", "required": True}
        ]},
        {"title": "Full AUDIT & Dependence", "section_type": "history", "questions": [
            {"id": "alc_units_week", "type": "number", "label": "Estimated Units per Week", "required": True, "placeholder": "e.g., 50"},
            {"id": "alc_morning_drinking", "type": "toggle", "label": "Morning Drinking to Settle Nerves/Withdrawal?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Morning drinking = ?dependence. Assess for withdrawal risk before advising abrupt cessation.", "red_flag_negative": ""},
            {"id": "alc_loss_control", "type": "toggle", "label": "Loss of Control - Drinking More Than Intended?", "required": True},
            {"id": "alc_guilt", "type": "toggle", "label": "Guilt About Drinking?", "required": False},
            {"id": "alc_blackouts", "type": "toggle", "label": "Memory Blackouts?", "required": True},
            {"id": "alc_injury", "type": "toggle", "label": "Alcohol-Related Injury? (Self/Others)", "required": True},
            {"id": "alc_others_concerned", "type": "toggle", "label": "Others Concerned About Your Drinking?", "required": True},
            {"id": "alc_previous_help", "type": "toggle", "label": "Previous Help for Alcohol?", "required": False}
        ]},
        {"title": "Withdrawal Risk & Medical Assessment", "section_type": "assessment", "questions": [
            {"id": "alc_withdrawal_history", "type": "toggle", "label": "History of Withdrawal Seizures / DTs?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: History of DTs/seizures = DO NOT advise abrupt cessation. Planned medically-assisted withdrawal needed.", "red_flag_negative": ""},
            {"id": "alc_lfts", "type": "multi_select", "label": "LFTs / Bloods", "required": False, "options": ["GGT raised", "ALT/AST raised", "MCV raised", "Normal", "Not checked"]},
            {"id": "alc_bp", "type": "text", "label": "Blood Pressure", "required": False, "placeholder": "e.g., 148/92"},
            {"id": "alc_mental_health", "type": "toggle", "label": "Co-existing Mental Health Issue?", "required": True},
            {"id": "alc_suicidal", "type": "toggle", "label": "Suicidal Ideation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suicidal ideation + alcohol = high risk. Urgent mental health assessment.", "red_flag_negative": ""}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Hazardous drinking (AUDIT-C 5+, increasing risk)", "Harmful drinking (causing physical/mental harm)", "Alcohol dependence (withdrawal symptoms, craving, tolerance)", "Alcohol-related liver disease", "Dual diagnosis (mental health + alcohol)"], "questions": [
            {"id": "alc_category", "type": "single_select", "label": "Drinking Category", "required": True, "options": ["Lower risk (<14 units/week)", "Increasing risk (15-35 units/week)", "Higher risk (>35 units/week)", "Possible dependence"]},
            {"id": "alc_readiness", "type": "single_select", "label": "Readiness to Change", "required": True, "options": ["Not ready", "Considering", "Ready to cut down", "Ready to stop completely"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "If dependent drinker: do NOT advise abrupt cessation - risk of withdrawal seizures/DTs. Medically-assisted withdrawal with chlordiazepoxide or carbamazepine. Thiamine 100mg TDS for prevention of Wernicke's encephalopathy. Return immediately if: confusion, hallucinations, severe tremor, seizures, or vomiting. Alcohol services: local drug & alcohol team, AA, SMART Recovery. Drinkaware.co.uk for self-help. Liver ultrasound if LFTs abnormal. Repeat LFTs in 3-6 months.", "questions": [
            {"id": "alc_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Brief advice + leaflet", "Cut down advice (drink-free days)", "Self-help resources (Drinkaware)", "Refer to alcohol service", "Medically-assisted detox (community)", "Inpatient detox referral", "Thiamine 100mg TDS", "Acamprosate/Naltrexone (relapse prevention)", "Liver USS requested"]},
            {"id": "alc_medication", "type": "text", "label": "Medication", "required": False, "placeholder": "e.g., Chlordiazepoxide reducing regime, Thiamine 100mg TDS"},
            {"id": "alc_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 2 weeks, repeat LFTs in 3 months, alcohol service appointment"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_alcohol_audit()