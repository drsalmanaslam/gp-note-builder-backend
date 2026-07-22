from app.database import SessionLocal
from app.models import User, Template, Category

def seed_backpain_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    template_data = {
        "title": "Back Pain Assessment",
        "description": "Assessment for low back pain including red flags for cauda equina and spinal pathology.",
        "category": "Musculoskeletal",
        "content": {
            "sections": [
                {
                    "title": "Pain History",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "bp_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (injury)", "Gradual", "Chronic"]},
                        {"id": "bp_location", "type": "single_select", "label": "Location", "required": True, "options": ["Lumbar", "Thoracic", "Cervical", "Sacral"]},
                        {"id": "bp_radiation", "type": "toggle", "label": "Radiation to Leg(s)?", "required": False},
                        {"id": "bp_severity", "type": "slider", "label": "Severity (1-10)", "required": True, "min": 1, "max": 10},
                        {"id": "bp_cauda_equina", "type": "toggle", "label": "🔴 Saddle Anaesthesia/Incontinence? (Cauda Equina)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspected cauda equina syndrome. Emergency MRI and neurosurgical referral required.", "red_flag_negative": "No cauda equina symptoms."},
                        {"id": "bp_fever", "type": "toggle", "label": "🔴 Fever/Weight Loss/Night Pain? (Infection/Malignancy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Constitutional symptoms with back pain. Consider infection or malignancy. Urgent investigation required.", "red_flag_negative": "No constitutional symptoms."}
                    ]
                },
                {
                    "title": "Examination & Plan",
                    "examination": "Spinal examination, neurological exam of lower limbs (power, sensation, reflexes), straight leg raise test",
                    "safety_netting": "If you develop numbness in the saddle area, incontinence, or severe leg weakness, go to A&E immediately.",
                    "questions": [
                        {"id": "bp_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Mechanical Back Pain", "Sciatica", "Disc Prolapse", "Spinal Stenosis", "Spondylosis"]},
                        {"id": "bp_management", "type": "textarea", "label": "Management Plan", "required": True, "placeholder": "e.g., Analgesia, physiotherapy, lifestyle advice..."},
                        {"id": "bp_followup", "type": "duration", "label": "Follow-up", "required": False, "units": ["weeks"]}
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
    seed_backpain_template()