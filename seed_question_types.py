from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_question_types():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("❌ Admin user not found")
        db.close()
        return
    
    template_data = {
        "title": "All Question Types Demo",
        "description": "Template demonstrating all question types.",
        "category": "General",
        "content": {
            "sections": [
                {
                    "id": "question_types",
                    "title": "Question Types Demo",
                    "questions": [
                        {
                            "id": "single_select_demo",
                            "type": "single_select",
                            "label": "Single Select (choose one)",
                            "required": True,
                            "options": ["Option A", "Option B", "Option C", "Option D"]
                        },
                        {
                            "id": "multi_select_demo",
                            "type": "multi_select",
                            "label": "Multi Select (choose all that apply)",
                            "required": False,
                            "options": ["Red", "Blue", "Green", "Yellow"]
                        },
                        {
                            "id": "date_demo",
                            "type": "date",
                            "label": "Date of symptom onset",
                            "required": False
                        },
                        {
                            "id": "pain_slider_demo",
                            "type": "slider",
                            "label": "Pain score",
                            "min": 0,
                            "max": 10,
                            "step": 1,
                            "unit": "/10"
                        },
                        {
                            "id": "duration_demo",
                            "type": "duration",
                            "label": "Duration of symptoms",
                            "required": False,
                            "units": ["hours", "days", "weeks", "months"]
                        }
                    ]
                }
            ]
        },
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
    
    print(f"✅ Template '{template_data['title']}' created with all question types!")
    db.close()

if __name__ == "__main__":
    seed_question_types()