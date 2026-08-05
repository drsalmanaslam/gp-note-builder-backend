from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_urti():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: 
        category = Category(name="Respiratory")
        db.add(category)
        db.commit()

    title = "Viral URTI"
    
    t = {
        "title": "Viral URTI",
        "description": "Focused assessment for viral upper respiratory tract infection covering red flags for LRTI, asthma considerations, and symptomatic management.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "urti_presenting_complaint", "type": "text", "label": "Presentation", "required": True, "placeholder": "e.g., Cough and runny nose for 2 days", "output_phrase": "c/o: {value}", "clinical_note": "Ask about sick contacts and whether anyone else at home/work is unwell."},
                    {"id": "urti_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 days", "output_phrase": "Duration: {value}"},
                    {"id": "urti_main_symptom", "type": "single_select", "label": "Associations", "required": True, "options": ["Cough", "Sore throat", "Wheeze", "Nasal congestion / coryza", "Fever", "Malaise / fatigue"], "output_phrase": "Associated symptoms: {value}"},
                    {"id": "urti_red_flags", "type": "multi_select", "label": "Red Flags", "required": True, "options": ["Shortness of breath", "Chest pain", "Haemoptysis", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB/wheeze/chest pain/haemoptysis = ?LRTI, pneumonia, PE.", "red_flag_negative": "", "output_phrase": "Red flags: {value}"},
                    {"id": "urti_asthma", "type": "single_select", "label": "Asthma History", "required": True, "options": ["Asthmatic - on preventer", "Asthmatic - no preventer", "Non-asthmatic"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Asthmatic + URTI = risk of exacerbation.", "red_flag_negative": "", "output_phrase": "Asthma: {value}"},
                    {"id": "urti_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Current smoker", "Ex-smoker", "Non-smoker"], "output_phrase": "Smoking: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(
            title=t["title"], 
            description=t["description"], 
            category=t["category"], 
            content=t["content"], 
            is_public=True, 
            created_by=admin.id, 
            version=1
        )
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created!")
    
    db.close()

if __name__ == "__main__":
    seed_urti()