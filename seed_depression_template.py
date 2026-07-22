from app.database import SessionLocal
from app.models import User, Template, Category

def seed_depression_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Mental Health").first()
    if not category: category = Category(name="Mental Health"); db.add(category); db.commit()

    template_data = {
        "title": "Depression Assessment (PHQ-9)",
        "description": "Depression screening using PHQ-9 with suicide risk assessment and management plan.",
        "category": "Mental Health",
        "content": {"sections": [
            {"title": "PHQ-9 Screening (Over Last 2 Weeks)", "questions": [
                {"id": "dep_interest", "type": "slider", "label": "Little interest/pleasure in doing things (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_mood", "type": "slider", "label": "Feeling down/depressed/hopeless (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_sleep", "type": "slider", "label": "Sleep disturbance (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_energy", "type": "slider", "label": "Feeling tired/low energy (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_appetite", "type": "slider", "label": "Appetite change (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_selfworth", "type": "slider", "label": "Feeling bad about self/failure (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_concentration", "type": "slider", "label": "Trouble concentrating (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_psychomotor", "type": "slider", "label": "Moving/speaking slowly or restlessly (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_suicidal_q9", "type": "slider", "label": "Thoughts of self-harm/suicide (0-3)", "required": True, "min": 0, "max": 3},
                {"id": "dep_total", "type": "number", "label": "Total PHQ-9 Score", "required": True, "placeholder": "0-27"},
                {"id": "dep_duration", "type": "duration", "label": "Duration of Symptoms", "required": True, "units": ["weeks", "months"]}
            ]},
            {"title": "Risk Assessment", "red_flag_threshold": 1, "questions": [
                {"id": "dep_suicidal_active", "type": "toggle", "label": "🔴 Active Suicidal Ideation/Plan?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Active suicidal ideation. Urgent mental health assessment. Safety plan agreed. Crisis team referral if indicated.", "red_flag_negative": "No active suicidal ideation."},
                {"id": "dep_selfharm", "type": "toggle", "label": "🔴 Recent Self-harm?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent self-harm. Urgent mental health assessment required.", "red_flag_negative": "No self-harm."},
                {"id": "dep_psychosis", "type": "toggle", "label": "🔴 Psychotic Symptoms? (Hallucinations/Delusions)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Psychotic symptoms. Urgent psychiatry assessment.", "red_flag_negative": "No psychotic symptoms."},
                {"id": "dep_bipolar", "type": "toggle", "label": "History of Mania/Bipolar?", "required": True},
                {"id": "dep_substance", "type": "single_select", "label": "Alcohol/Substance Use", "required": True, "options": ["None", "Mild", "Moderate", "Heavy/Dependent"]}
            ]},
            {"title": "Management Plan", "safety_netting": "If you feel unable to keep yourself safe, go to A&E or call 999. Samaritans: 116 123 (24/7). Crisis team: contact if urgent.", "questions": [
                {"id": "dep_severity", "type": "single_select", "label": "Depression Severity", "required": True, "options": ["Mild (PHQ-9 5-9)", "Moderate (PHQ-9 10-14)", "Moderately Severe (PHQ-9 15-19)", "Severe (PHQ-9 20-27)"]},
                {"id": "dep_medication", "type": "textarea", "label": "Current/Prescribed Medication", "required": False, "placeholder": "e.g., Sertraline 50mg OD started..."},
                {"id": "dep_therapy", "type": "toggle", "label": "Psychological Therapy Referral (IAPT)?", "required": False},
                {"id": "dep_crisis", "type": "toggle", "label": "Crisis Number Given?", "required": True},
                {"id": "dep_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["weeks"]},
                {"id": "dep_notes", "type": "textarea", "label": "Additional Notes", "required": False}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_depression_template()