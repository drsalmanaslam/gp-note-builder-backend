from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_templates():
    db = SessionLocal()
    
    # Get admin user
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("❌ Admin user not found. Please create admin first.")
        db.close()
        return
    
    templates_data = [
        {
            "title": "Shortness of Breath (SOB)",
            "description": "Complete assessment for patients presenting with shortness of breath.",
            "category": "Respiratory",
            "content": {
                "sections": [
                    {
                        "id": "situation",
                        "title": "Situation",
                        "questions": [
                            {
                                "id": "consultation_type",
                                "type": "select",
                                "label": "Consultation Type",
                                "required": True,
                                "options": [
                                    "F2F consultation: ID confirmed",
                                    "Telephone consultation, ID confirmed",
                                    "Seen alone",
                                    "Seen with family/carer"
                                ]
                            },
                            {
                                "id": "gender",
                                "type": "select",
                                "label": "Gender",
                                "required": True,
                                "options": ["Male", "Female", "Trans Man", "Trans Woman"]
                            },
                            {
                                "id": "age",
                                "type": "number",
                                "label": "Age (years)",
                                "required": True,
                                "placeholder": "e.g., 45"
                            }
                        ]
                    },
                    {
                        "id": "chief_complaint",
                        "title": "Chief Complaint",
                        "questions": [
                            {
                                "id": "sob_type",
                                "type": "select",
                                "label": "SOB Type",
                                "required": True,
                                "options": ["on exertion", "at rest"]
                            },
                            {
                                "id": "onset",
                                "type": "select",
                                "label": "Onset",
                                "required": True,
                                "options": ["sudden", "gradual"]
                            },
                            {
                                "id": "pattern",
                                "type": "select",
                                "label": "Pattern",
                                "required": False,
                                "options": ["constant", "intermittent", "occasional", "worsening", "variable in intensity"]
                            },
                            {
                                "id": "duration",
                                "type": "text",
                                "label": "Duration",
                                "required": False,
                                "placeholder": "e.g., 3 days"
                            }
                        ]
                    },
                    {
                        "id": "history",
                        "title": "History",
                        "questions": [
                            {
                                "id": "history_details",
                                "type": "textarea",
                                "label": "History Details",
                                "required": False,
                                "placeholder": "Describe the history of presenting complaint..."
                            }
                        ]
                    },
                    {
                        "id": "examination",
                        "title": "Examination",
                        "questions": [
                            {
                                "id": "exam_findings",
                                "type": "textarea",
                                "label": "Examination Findings",
                                "required": False,
                                "placeholder": "Describe examination findings..."
                            }
                        ]
                    },
                    {
                        "id": "assessment",
                        "title": "Impression / Assessment",
                        "questions": [
                            {
                                "id": "impression",
                                "type": "textarea",
                                "label": "Impression",
                                "required": False,
                                "placeholder": "Describe your impression..."
                            }
                        ]
                    },
                    {
                        "id": "plan",
                        "title": "Plan",
                        "questions": [
                            {
                                "id": "plan_details",
                                "type": "textarea",
                                "label": "Plan",
                                "required": False,
                                "placeholder": "Describe the plan..."
                            }
                        ]
                    }
                ]
            },
            "differentials": [
                "Asthma",
                "COPD",
                "Pulmonary Embolism",
                "Heart Failure",
                "Pneumonia",
                "Anxiety"
            ],
            "safetyNetting": [
                "Seek immediate medical attention if breathing worsens",
                "Call 999 if unable to speak in full sentences",
                "Follow up with GP within 48 hours"
            ],
            "is_public": True
        }
    ]
    
    for template_data in templates_data:
        category_name = template_data["category"]
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.commit()
            db.refresh(category)
            print(f"✅ Category '{category_name}' created")
        
        # Check if template already exists
        existing_template = db.query(Template).filter(
            Template.title == template_data["title"],
            Template.created_by == admin.id
        ).first()
        
        if existing_template:
            # Delete existing template to replace with new version
            db.delete(existing_template)
            db.commit()
            print(f"🔄 Removing old '{template_data['title']}' template")
        
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
        print(f"✅ Template '{template_data['title']}' created with questions")
    
    print("\n🎉 Templates seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_templates()