from app.database import SessionLocal
from app.models import User, Template, Category

def seed_sorethroat_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    template_data = {
        "title": "Sore Throat Assessment",
        "description": "Assessment for sore throat including Centor criteria and red flags.",
        "category": "ENT",
        "content": {
            "sections": [
                {
                    "title": "Centor Criteria",
                    "questions": [
                        {"id": "st_fever", "type": "toggle", "label": "Fever >38°C? (+1)", "required": True},
                        {"id": "st_exudate", "type": "toggle", "label": "Tonsillar Exudate? (+1)", "required": True},
                        {"id": "st_lymph", "type": "toggle", "label": "Tender Anterior Cervical Lymphadenopathy? (+1)", "required": True},
                        {"id": "st_cough", "type": "toggle", "label": "Absence of Cough? (+1)", "required": True},
                        {"id": "st_duration", "type": "duration", "label": "Duration", "required": True, "units": ["days"]},
                        {"id": "st_quinsy", "type": "toggle", "label": "🔴 Trismus/Drooling/Stridor? (Quinsy/Airway)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Possible quinsy or airway compromise. Urgent ENT assessment required.", "red_flag_negative": "No airway concerns."}
                    ]
                },
                {
                    "title": "Plan",
                    "safety_netting": "If you develop difficulty breathing, cannot swallow saliva, or have trismus, seek urgent medical attention.",
                    "questions": [
                        {"id": "st_antibiotics", "type": "toggle", "label": "Antibiotics Prescribed?", "required": False},
                        {"id": "st_advice", "type": "textarea", "label": "Advice Given", "required": True, "placeholder": "e.g., Fluids, analgesia, safety netting..."},
                        {"id": "st_followup", "type": "single_select", "label": "Follow-up Needed?", "required": False, "options": ["No", "PRN", "1 week"]}
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
    seed_sorethroat_template()