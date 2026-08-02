from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ogtt():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "Oral Glucose Tolerance Test (OGTT) - Type 2 Diabetes",
        "description": "Structured template for performing and interpreting OGTT covering diagnostic criteria, impaired fasting glucose/glucose tolerance, and HbA1c reference scale.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Indication & Preparation",
                "section_type": "history",
                "questions": [
                    {"id": "ogtt_indication", "type": "single_select", "label": "Indication for OGTT", "required": True, "options": ["Fasting glucose ≥5.6 mmol/L", "Impaired glucose tolerance suspected", "Other"]},
                    {"id": "ogtt_fasting_glucose", "type": "number", "label": "Fasting Glucose Result (mmol/L) - if known", "required": False, "placeholder": "e.g., 6.2"},
                    {"id": "ogtt_fasting_confirmed", "type": "single_select", "label": "Fasting Status Confirmed", "required": True, "options": ["Fasted from midnight", "Fasting duration unclear / inadequate"]}
                ]
            },
            {
                "title": "Test Procedure",
                "section_type": "examination",
                "questions": [
                    {"id": "ogtt_time0", "type": "toggle", "label": "Time 0 Sample Taken? (Bottle marked 'Time 0 minutes')", "required": True},
                    {"id": "ogtt_glucose_load", "type": "single_select", "label": "Glucose Load Administered (75g)", "required": True, "options": ["Rapilose OGTT", "113ml Polycal neutral", "Other 75g glucose load"]},
                    {"id": "ogtt_time120", "type": "toggle", "label": "Time 120 Sample Taken? (Bottle marked '120 minutes')", "required": True},
                    {"id": "ogtt_samples_sent", "type": "toggle", "label": "Both Samples Sent to Lab Together?", "required": True},
                    {"id": "ogtt_pil", "type": "toggle", "label": "Patient Information Leaflet Given? (Glucose Tolerance Test PIL)", "required": False}
                ]
            },
            {
                "title": "Results",
                "section_type": "assessment",
                "questions": [
                    {"id": "ogtt_fbg", "type": "number", "label": "Fasting Blood Glucose (mmol/L)", "required": False, "placeholder": "e.g., 6.5 (NR: <5.6)"},
                    {"id": "ogtt_2hr", "type": "number", "label": "2-Hour Post-Load Glucose (mmol/L)", "required": False, "placeholder": "e.g., 12.1 (NR: <7.8)"},
                    {"id": "ogtt_hba1c", "type": "number", "label": "HbA1c (mmol/mol) - if performed", "required": False, "placeholder": "e.g., 50 (Pre-DM: 39-47, DM: ≥48)"},
                    {"id": "ogtt_rbg", "type": "number", "label": "Random Blood Glucose (mmol/L) - if applicable", "required": False, "placeholder": "e.g., 11.5 (DM: ≥11.1 + symptoms)"}
                ]
            },
            {
                "title": "Interpretation",
                "section_type": "assessment",
                "differentials": [
                    "Type 2 Diabetes Mellitus (confirmed)",
                    "Impaired Fasting Glucose (IFG: 5.6-6.9 mmol/L)",
                    "Impaired Glucose Tolerance (IGT: 2h glucose 7.8-11 mmol/L)",
                    "Normal Glucose Tolerance",
                    "Pre-Diabetes (HbA1c 42-47 mmol/mol)"
                ],
                "questions": [
                    {"id": "ogtt_diagnosis", "type": "single_select", "label": "Diagnostic Category (T2DM = 2 criteria met)", "required": False, "options": ["Type 2 Diabetes Confirmed - two diagnostic criteria met", "Impaired Fasting Glucose - fasting 5.6-6.9", "Impaired Glucose Tolerance - 2h glucose 7.8-11 or HbA1c 39-47", "Normal - no criteria met"], "is_red_flag": True, "red_flag_positive": "RED FLAG: T2DM confirmed = proceed to New Type 2 Diabetic pathway.", "red_flag_negative": ""},
                    {"id": "ogtt_symptoms", "type": "single_select", "label": "Symptom Status", "required": False, "options": ["Symptomatic - RBG ≥11.1 diagnostic with symptoms", "Asymptomatic - repeat test in 2 weeks to confirm"], "is_red_flag": True, "red_flag_positive": "RED FLAG: If asymptomatic, diagnosis MUST be confirmed by repeating test after 2 weeks before formalising.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "HbA1c Reference Scale (WHO 2011)",
                "section_type": "assessment",
                "questions": [
                    {"id": "ogtt_hba1c_ref", "type": "single_select", "label": "HbA1c Interpretation", "required": False, "options": ["42 mmol/mol (6.0%) = Onset of pre-diabetes", "48 mmol/mol (6.5%) = WHO diagnostic threshold for T2DM", "53 mmol/mol (7.0%) = NICE target on dual therapy+", "58 mmol/mol (7.5%) = QOF target", "Not performed"]}
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "If asymptomatic: diagnosis must be confirmed by repeating test after 2 weeks before formalising. Impaired fasting glucose (5.6-6.9): lifestyle advice + annual monitoring. Impaired glucose tolerance (2h glucose 7.8-11 or HbA1c 39-47): lifestyle advice + annual monitoring. Pre-diabetes: weight loss 5-10%, 150 min exercise/week, Mediterranean diet. Normal result: no further action. T2DM confirmed: proceed to New Type 2 Diabetic pathway.",
                "questions": [
                    {"id": "ogtt_outcome", "type": "multi_select", "label": "Outcome", "required": True, "options": ["Diagnosis confirmed - proceed to New T2DM pathway", "Repeat test in 2 weeks - asymptomatic, confirmation required", "IFG - lifestyle advice + monitor annually", "IGT - lifestyle advice + monitor annually", "Normal - no further action"]},
                    {"id": "ogtt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat OGTT in 2 weeks, routine annual monitoring, or no follow-up required"}
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
    seed_ogtt()