from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_conditional_template():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("❌ Admin user not found")
        db.close()
        return
    
    template_data = {
        "title": "SOB Assessment (Conditional)",
        "description": "SOB assessment with conditional questions based on SOB type.",
        "category": "Respiratory",
        "content": {
            "sections": [
                {
                    "id": "symptoms",
                    "title": "Symptoms",
                    "questions": [
                        {
                            "id": "sob_type",
                            "type": "select",
                            "label": "SOB Type",
                            "required": True,
                            "options": ["on exertion", "at rest"]
                        },
                        {
                            "id": "sob_exertion_details",
                            "type": "textarea",
                            "label": "Details of SOB on exertion",
                            "required": False,
                            "placeholder": "Describe the exertion that triggers SOB...",
                            "condition": {
                                "questionId": "sob_type",
                                "value": "on exertion"
                            }
                        },
                        {
                            "id": "sob_rest_details",
                            "type": "textarea",
                            "label": "Details of SOB at rest",
                            "required": False,
                            "placeholder": "Describe the SOB at rest...",
                            "condition": {
                                "questionId": "sob_type",
                                "value": "at rest"
                            }
                        }
                    ]
                },
                {
                    "id": "additional",
                    "title": "Additional Information",
                    "questions": [
                        {
                            "id": "has_wheeze",
                            "type": "toggle",
                            "label": "Wheeze present",
                            "required": False
                        },
                        {
                            "id": "wheeze_details",
                            "type": "textarea",
                            "label": "Wheeze details",
                            "required": False,
                            "placeholder": "Describe the wheeze...",
                            "condition": {
                                "questionId": "has_wheeze",
                                "value": True
                            }
                        }
                    ]
                }
            ]
        },
        "differentials": ["Asthma", "COPD", "Pulmonary Embolism", "Heart Failure"],
        "safetyNetting": ["Seek immediate medical attention if breathing worsens", "Call 999 if unable to speak in full sentences"],
        "is_public": True
    }
    
    existing = db.query(Template).filter(Template.title == template_data["title"]).first()
    if existing:
        db.delete(existing)
        db.commit()
    
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
    
    print(f"✅ Template '{template_data['title']}' created with conditional questions!")
    db.close()

if __name__ == "__main__":
    seed_conditional_template()