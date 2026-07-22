from app.database import SessionLocal
from app.models import User, Template, Category

def seed_anxiety_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Mental Health").first()
    if not category: category = Category(name="Mental Health"); db.add(category); db.commit()

    template_data = {
        "title": "Anxiety Assessment",
        "description": "Assessment for generalised anxiety disorder including GAD-7 scoring and red flags.",
        "category": "Mental Health",
        "content": {
            "sections": [
                {
                    "title": "GAD-7 Screening",
                    "questions": [
                        {"id": "anx_nervous", "type": "slider", "label": "Feeling nervous/anxious (0-3)", "required": True, "min": 0, "max": 3},
                        {"id": "anx_worry", "type": "slider", "label": "Unable to control worrying (0-3)", "required": True, "min": 0, "max": 3},
                        {"id": "anx_restless", "type": "slider", "label": "Trouble relaxing (0-3)", "required": True, "min": 0, "max": 3},
                        {"id": "anx_irritable", "type": "slider", "label": "Easily annoyed/irritable (0-3)", "required": True, "min": 0, "max": 3},
                        {"id": "anx_duration", "type": "duration", "label": "Duration of Symptoms", "required": True, "units": ["weeks", "months"]},
                        {"id": "anx_suicidal", "type": "toggle", "label": "🔴 Suicidal Ideation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suicidal ideation reported. Urgent mental health assessment required. Safety plan discussed.", "red_flag_negative": "No suicidal ideation."},
                        {"id": "anx_self_harm", "type": "toggle", "label": "🔴 Self-harm Risk?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Self-harm risk identified. Urgent mental health referral.", "red_flag_negative": "No self-harm risk."}
                    ]
                },
                {
                    "title": "Impact & Management",
                    "safety_netting": "If you experience thoughts of harming yourself or others, go to A&E or call 999 immediately. Samaritans: 116 123 (24/7).",
                    "questions": [
                        {"id": "anx_impact", "type": "single_select", "label": "Impact on Daily Life", "required": True, "options": ["Mild", "Moderate", "Severe"]},
                        {"id": "anx_medication", "type": "textarea", "label": "Current Medications", "required": False, "placeholder": "e.g., Sertraline 50mg OD..."},
                        {"id": "anx_therapy", "type": "toggle", "label": "Psychological Therapy Referral?", "required": False},
                        {"id": "anx_plan", "type": "textarea", "label": "Management Plan", "required": True},
                        {"id": "anx_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["weeks"]}
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_anxiety_template()