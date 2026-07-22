from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_toggle_template():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("❌ Admin user not found")
        db.close()
        return
    
    # Asthma template with toggle questions
    template_data = {
        "title": "Asthma Review (Toggle Version)",
        "description": "Asthma review with clickable toggle buttons for symptoms.",
        "category": "Chronic Disease Reviews",
        "content": {
            "sections": [
                {
                    "id": "symptoms",
                    "title": "Symptoms",
                    "questions": [
                        {"id": "wheeze", "type": "toggle", "label": "Wheeze", "required": False},
                        {"id": "breathlessness", "type": "toggle", "label": "Breathlessness", "required": False},
                        {"id": "chest_tightness", "type": "toggle", "label": "Chest tightness", "required": False},
                        {"id": "cough", "type": "toggle", "label": "Cough (night/early morning)", "required": False},
                        {"id": "exercise_induced", "type": "toggle", "label": "Exercise induced", "required": False}
                    ]
                },
                {
                    "id": "triggers",
                    "title": "Triggers",
                    "questions": [
                        {"id": "cold_air", "type": "toggle", "label": "Cold air", "required": False},
                        {"id": "allergens", "type": "toggle", "label": "Allergens", "required": False},
                        {"id": "stress", "type": "toggle", "label": "Stress", "required": False},
                        {"id": "smoking", "type": "toggle", "label": "Smoking", "required": False}
                    ]
                },
                {
                    "id": "red_flags",
                    "title": "Red Flags",
                    "questions": [
                        {"id": "red_flag_silent_chest", "type": "toggle", "label": "🔴 Silent chest - URGENT", "required": False, "is_red_flag": True},
                        {"id": "red_flag_cyanosis", "type": "toggle", "label": "🔴 Cyanosis - URGENT", "required": False, "is_red_flag": True},
                        {"id": "red_flag_exhaustion", "type": "toggle", "label": "🔴 Exhaustion - URGENT", "required": False, "is_red_flag": True}
                    ]
                },
                {
                    "id": "examination",
                    "title": "Examination",
                    "questions": [
                        {"id": "exam_findings", "type": "textarea", "label": "Examination Findings", "required": False, "placeholder": "Describe examination findings..."}
                    ]
                },
                {
                    "id": "plan",
                    "title": "Plan",
                    "questions": [
                        {"id": "plan_details", "type": "textarea", "label": "Plan", "required": False, "placeholder": "Describe the plan..."}
                    ]
                }
            ]
        },
        "differentials": ["COPD", "Allergic Rhinitis", "Vocal Cord Dysfunction", "Respiratory Infections"],
        "safetyNetting": [
            "Use reliever inhaler if symptoms worsen",
            "If unable to get relief from medication, call GP",
            "Follow asthma action plan",
            "If symptoms are severe and not responding to medication, call 999",
            "Attend annual asthma reviews"
        ],
        "is_public": True
    }
    
    # Delete existing template if it exists
    existing = db.query(Template).filter(Template.title == template_data["title"]).first()
    if existing:
        db.delete(existing)
        db.commit()
        print(f"🔄 Removed old '{template_data['title']}' template")
    
    # Get or create category
    category = db.query(Category).filter(Category.name == template_data["category"]).first()
    if not category:
        category = Category(name=template_data["category"])
        db.add(category)
        db.commit()
        db.refresh(category)
    
    new_template = Template(
        title=template_data["title"],
        description=template_data["description"],
        category=template_data["category"],
        content=template_data["content"],
        is_public=template_data["is_public"],
        created_by=admin.id,
        version=1
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    
    print(f"✅ Template '{template_data['title']}' created with toggle buttons!")
    db.close()

if __name__ == "__main__":
    seed_toggle_template()