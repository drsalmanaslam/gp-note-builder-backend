from app.database import SessionLocal
from app.models import User, Template, Category

def seed_falls_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Elderly Care").first()
    if not category: category = Category(name="Elderly Care"); db.add(category); db.commit()

    template_data = {
        "title": "Falls Assessment",
        "description": "Comprehensive falls assessment for elderly patients including multifactorial risk evaluation.",
        "category": "Elderly Care",
        "content": {
            "sections": [
                {
                    "title": "Fall History",
                    "questions": [
                        {"id": "falls_number", "type": "number", "label": "Number of Falls in Past 12 Months", "required": True, "placeholder": "e.g., 3"},
                        {"id": "falls_circumstances", "type": "textarea", "label": "Circumstances of Fall(s)", "required": True, "placeholder": "e.g., Tripped on rug, felt dizzy, lost balance..."},
                        {"id": "falls_injury", "type": "toggle", "label": "Injury Sustained?", "required": True},
                        {"id": "falls_loc", "type": "toggle", "label": "🔴 Loss of Consciousness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fall with LOC. Consider cardiac/neurological cause. Urgent investigation required.", "red_flag_negative": "No LOC with falls."},
                        {"id": "falls_fracture", "type": "toggle", "label": "🔴 Suspected Fracture?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspected fracture. Urgent X-ray and orthopaedic assessment.", "red_flag_negative": "No fracture suspected."}
                    ]
                },
                {
                    "title": "Risk Assessment",
                    "questions": [
                        {"id": "falls_medications", "type": "textarea", "label": "Medication Review (especially sedatives/antihypertensives)", "required": True},
                        {"id": "falls_vision", "type": "toggle", "label": "Vision Assessment Needed?", "required": False},
                        {"id": "falls_bp", "type": "toggle", "label": "Postural BP Checked?", "required": True},
                        {"id": "falls_home", "type": "toggle", "label": "Home Safety Assessment Needed?", "required": False},
                        {"id": "falls_mobility", "type": "single_select", "label": "Mobility Status", "required": True, "options": ["Independent", "Uses Stick", "Uses Frame", "Requires Assistance"]}
                    ]
                },
                {
                    "title": "Plan",
                    "safety_netting": "If further falls occur with head injury or loss of consciousness, attend A&E immediately.",
                    "questions": [
                        {"id": "falls_plan", "type": "textarea", "label": "Management Plan", "required": True, "placeholder": "e.g., Physio referral, OT home assessment, medication review..."},
                        {"id": "falls_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["weeks", "months"]}
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
    seed_falls_template()