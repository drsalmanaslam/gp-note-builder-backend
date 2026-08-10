from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_htn_meds_test():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category:
        category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "HTN Meds Test (Cascading)",
        "description": "Test template for cascading multi-select medication selection.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Medication Selection",
                "section_type": "plan",
                "questions": [
                    {
                        "id": "htn_class",
                        "type": "cascading_multi",
                        "label": "Select Medication Classes",
                        "required": False,
                        "options": ["ACEi", "ARB", "CCB", "Thiazide"],
                        "output_phrase": "Classes: {value}",
                        "children": {
                            "ACEi": [
                                {"id": "acei_drug", "type": "single_select", "label": "ACEi Drug", "options": ["Ramipril", "Lisinopril", "Perindopril"], "output_phrase": "ACEi: {value}"},
                                {"id": "acei_dose", "type": "text", "label": "ACEi Dose", "placeholder": "e.g., 5mg OD", "output_phrase": "ACEi Dose: {value}"}
                            ],
                            "CCB": [
                                {"id": "ccb_drug", "type": "single_select", "label": "CCB Drug", "options": ["Amlodipine", "Nifedipine", "Felodipine"], "output_phrase": "CCB: {value}"},
                                {"id": "ccb_dose", "type": "text", "label": "CCB Dose", "placeholder": "e.g., 5mg OD", "output_phrase": "CCB Dose: {value}"}
                            ],
                            "Thiazide": [
                                {"id": "thia_drug", "type": "single_select", "label": "Thiazide Drug", "options": ["Bendroflumethiazide", "Indapamide"], "output_phrase": "Thiazide: {value}"}
                            ]
                        }
                    }
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]; existing.content = t["content"]; existing.category = t["category"]; existing.is_public = t["is_public"]; existing.updated_at = datetime.now(timezone.utc)
        db.commit(); print(f"Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t); db.commit(); print(f"Created: {t['title']}")
    db.close()

if __name__ == "__main__":
    seed_htn_meds_test()