from app.database import SessionLocal
from app.models import User, Template, Category

def seed_abdominal_pain_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category:
        category = Category(name="Gastroenterology")
        db.add(category); db.commit()

    template_data = {
        "title": "Abdominal Pain Assessment",
        "description": "Structured assessment for abdominal pain including surgical red flags.",
        "category": "Gastroenterology",
        "content": {
            "sections": [
                {
                    "title": "Pain History",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "ap_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
                        {"id": "ap_location", "type": "single_select", "label": "Location", "required": True, "options": ["RUQ", "LUQ", "RLQ", "LLQ", "Epigastric", "Periumbilical", "Suprapubic", "Generalised"]},
                        {"id": "ap_character", "type": "single_select", "label": "Character", "required": True, "options": ["Colicky/Cramping", "Sharp", "Burning", "Dull Ache"]},
                        {"id": "ap_severity", "type": "slider", "label": "Severity (1-10)", "required": True, "min": 1, "max": 10},
                        {"id": "ap_radiation", "type": "single_select", "label": "Radiation", "required": False, "options": ["None", "To Back", "To Shoulder", "To Groin"]},
                        {"id": "ap_severe_sudden", "type": "toggle", "label": "🔴 Severe Sudden Onset? (Acute Abdomen)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute abdomen suspected. Urgent surgical assessment required.", "red_flag_negative": "No acute abdomen features."}
                    ]
                },
                {
                    "title": "Associated Symptoms",
                    "questions": [
                        {"id": "ap_nausea", "type": "toggle", "label": "Nausea/Vomiting?", "required": False},
                        {"id": "ap_bowel_change", "type": "single_select", "label": "Bowel Habit", "required": True, "options": ["Normal", "Diarrhoea", "Constipation", "Alternating"]},
                        {"id": "ap_rectal_bleeding", "type": "toggle", "label": "🔴 Rectal Bleeding/Melaena?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: GI bleeding. Urgent assessment and possible admission required.", "red_flag_negative": "No GI bleeding."},
                        {"id": "ap_fever", "type": "toggle", "label": "Fever?", "required": False},
                        {"id": "ap_weight_loss", "type": "toggle", "label": "🔴 Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss with abdominal pain. Consider malignancy - 2WW referral.", "red_flag_negative": "No significant weight loss."}
                    ]
                },
                {
                    "title": "Examination & Plan",
                    "examination": "Abdominal examination including inspection, palpation, percussion, auscultation. Check for guarding/rigidity/rebound.",
                    "safety_netting": "If pain becomes severe, you develop vomiting, fever, or cannot pass wind/stool, seek urgent medical attention. Call 999 for severe sudden pain.",
                    "differentials": ["Appendicitis", "Cholecystitis", "Pancreatitis", "Diverticulitis", "IBS", "Gastritis", "Bowel Obstruction"],
                    "questions": [
                        {"id": "ap_diagnosis", "type": "textarea", "label": "Assessment & Plan", "required": True, "placeholder": "Working diagnosis and management plan..."},
                        {"id": "ap_followup", "type": "duration", "label": "Follow-up", "required": False, "units": ["days", "weeks"]}
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
    print(f"Template '{template_data['title']}' created!")
    db.close()

if __name__ == "__main__":
    seed_abdominal_pain_template()