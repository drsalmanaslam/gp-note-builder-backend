from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_complete_sob_template():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("❌ Admin user not found")
        db.close()
        return
    
    template_data = {
        "title": "Shortness of Breath (SOB) - Complete Assessment",
        "description": "Complete SOB assessment with all symptoms, signs, red flags, and management.",
        "category": "Respiratory",
        "content": {
            "sections": [
                {
                    "id": "situation",
                    "title": "Situation & Patient Details",
                    "questions": [
                        {"id": "consultation_type", "type": "select", "label": "Consultation Type", "required": True, "options": ["F2F consultation: ID confirmed", "Telephone consultation, ID confirmed", "Seen alone", "Seen with family/carer"]},
                        {"id": "gender", "type": "select", "label": "Gender", "required": True, "options": ["Male", "Female", "Trans Man", "Trans Woman"]},
                        {"id": "age", "type": "number", "label": "Age (years)", "required": True, "placeholder": "e.g., 45"}
                    ]
                },
                {
                    "id": "chief_complaint",
                    "title": "Chief Complaint",
                    "questions": [
                        {"id": "sob_type", "type": "select", "label": "SOB Type", "required": True, "options": ["on exertion", "at rest"]},
                        {"id": "onset", "type": "select", "label": "Onset", "required": True, "options": ["sudden", "gradual"]},
                        {"id": "pattern", "type": "select", "label": "Pattern", "required": False, "options": ["constant", "intermittent", "occasional", "worsening", "variable in intensity"]},
                        {"id": "duration", "type": "text", "label": "Duration", "required": False, "placeholder": "e.g., 3 days"}
                    ]
                },
                {
                    "id": "symptoms",
                    "title": "Symptoms (Toggle to add)",
                    "questions": [
                        {"id": "wheeze", "type": "toggle", "label": "Wheeze", "required": False},
                        {"id": "cough", "type": "toggle", "label": "Cough", "required": False},
                        {"id": "sputum", "type": "toggle", "label": "Sputum production", "required": False},
                        {"id": "chest_pain", "type": "toggle", "label": "Chest pain", "required": False},
                        {"id": "palpitations", "type": "toggle", "label": "Palpitations", "required": False},
                        {"id": "dizziness", "type": "toggle", "label": "Dizziness / lightheadedness", "required": False},
                        {"id": "syncope", "type": "toggle", "label": "Syncope (fainting)", "required": False}
                    ]
                },
                {
                    "id": "symptoms_details",
                    "title": "Symptom Details",
                    "questions": [
                        {
                            "id": "wheeze_details",
                            "type": "textarea",
                            "label": "Wheeze details",
                            "required": False,
                            "placeholder": "Describe the wheeze (onset, triggers, associated symptoms)...",
                            "condition": {"questionId": "wheeze", "value": True}
                        },
                        {
                            "id": "cough_details",
                            "type": "textarea",
                            "label": "Cough details",
                            "required": False,
                            "placeholder": "Describe the cough (dry/wet, productive, worse at night)...",
                            "condition": {"questionId": "cough", "value": True}
                        },
                        {
                            "id": "sputum_details",
                            "type": "textarea",
                            "label": "Sputum details",
                            "required": False,
                            "placeholder": "Colour, consistency, amount...",
                            "condition": {"questionId": "sputum", "value": True}
                        },
                        {
                            "id": "chest_pain_details",
                            "type": "textarea",
                            "label": "Chest pain details",
                            "required": False,
                            "placeholder": "Nature, location, radiation, severity...",
                            "condition": {"questionId": "chest_pain", "value": True}
                        },
                        {
                            "id": "palpitations_details",
                            "type": "textarea",
                            "label": "Palpitations details",
                            "required": False,
                            "placeholder": "Rate, rhythm, triggers...",
                            "condition": {"questionId": "palpitations", "value": True}
                        }
                    ]
                },
                {
                    "id": "examination",
                    "title": "Examination Findings",
                    "questions": [
                        {"id": "respiratory_rate", "type": "number", "label": "Respiratory rate (breaths/min)", "required": False, "placeholder": "e.g., 18"},
                        {"id": "oxygen_saturation", "type": "number", "label": "Oxygen saturation (%)", "required": False, "placeholder": "e.g., 96"},
                        {"id": "heart_rate", "type": "number", "label": "Heart rate (bpm)", "required": False, "placeholder": "e.g., 80"},
                        {"id": "temperature", "type": "number", "label": "Temperature (°C)", "required": False, "placeholder": "e.g., 37.2"},
                        {"id": "chest_auscultation", "type": "textarea", "label": "Chest auscultation", "required": False, "placeholder": "Describe breath sounds, added sounds..."},
                        {"id": "accessory_muscles", "type": "select", "label": "Use of accessory muscles", "required": False, "options": ["Yes", "No"]},
                        {"id": "cyanosis", "type": "select", "label": "Cyanosis (blue lips/fingers)", "required": False, "options": ["Yes", "No"]},
                        {"id": "peripheral_oedema", "type": "select", "label": "Peripheral oedema", "required": False, "options": ["Yes", "No"]}
                    ]
                },
                {
    "id": "red_flags",
    "title": "⚠️ Red Flags",
    "questions": [
        {"id": "red_flag_severe_sob", "type": "toggle", "label": "Severe SOB at rest", "required": False, "is_red_flag": True},
        {"id": "red_flag_cyanosis", "type": "toggle", "label": "Cyanosis", "required": False, "is_red_flag": True},
        {"id": "red_flag_silent_chest", "type": "toggle", "label": "Silent chest", "required": False, "is_red_flag": True},
        {"id": "red_flag_confusion", "type": "toggle", "label": "Confusion / decreased consciousness", "required": False, "is_red_flag": True},
        {"id": "red_flag_haemodynamic", "type": "toggle", "label": "Haemodynamic instability", "required": False, "is_red_flag": True}
    ]
},
                {
                    "id": "assessment",
                    "title": "Assessment & Impression",
                    "questions": [
                        {"id": "clinical_impression", "type": "textarea", "label": "Clinical Impression", "required": False, "placeholder": "What is your clinical impression?"},
                        {"id": "differential_diagnosis", "type": "textarea", "label": "Differential Diagnoses", "required": False, "placeholder": "List differential diagnoses..."}
                    ]
                },
                {
                    "id": "plan",
                    "title": "Plan & Management",
                    "questions": [
                        {"id": "investigations", "type": "textarea", "label": "Investigations", "required": False, "placeholder": "List investigations ordered..."},
                        {"id": "treatment", "type": "textarea", "label": "Treatment", "required": False, "placeholder": "Describe treatment plan..."},
                        {"id": "follow_up", "type": "textarea", "label": "Follow up", "required": False, "placeholder": "Follow up plan..."}
                    ]
                }
            ]
        },
        "differentials": [
            "Asthma",
            "COPD (Chronic Obstructive Pulmonary Disease)",
            "Pulmonary Embolism (PE)",
            "Heart Failure",
            "Pneumonia",
            "Pulmonary Fibrosis",
            "Anaemia",
            "Anxiety / Panic Attack",
            "Upper Airway Obstruction",
            "Pleural Effusion",
            "Pneumothorax"
        ],
        "safetyNetting": [
            "🔴 Seek immediate medical attention (call 999) if:",
            "   - Breathing gets worse and is not improving",
            "   - Unable to speak in full sentences",
            "   - Develops chest pain, confusion, or cyanosis",
            "   - Has a severe asthma attack (if known asthmatic)",
            "Follow up with GP within 48 hours",
            "Contact GP if symptoms are not improving",
            "If unable to contact GP, call 111 for advice"
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
    
    print(f"✅ Template '{template_data['title']}' created with all sections!")
    db.close()

if __name__ == "__main__":
    seed_complete_sob_template()