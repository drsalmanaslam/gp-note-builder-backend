from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_clinical_template():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("❌ Admin user not found")
        db.close()
        return
    
    template_data = {
        "title": "Clinical Assessment - Chest Pain",
        "description": "Complete chest pain assessment with all question types.",
        "category": "Cardiovascular",
        "content": {
            "sections": [
                {
                    "id": "demographics",
                    "title": "Patient Demographics",
                    "questions": [
                        {"id": "gender", "type": "single_select", "label": "Gender", "required": True, "options": ["Male", "Female", "Trans Man", "Trans Woman"]},
                        {"id": "age", "type": "number", "label": "Age (years)", "required": True, "placeholder": "e.g., 45"}
                    ]
                },
                {
                    "id": "symptoms",
                    "title": "Symptoms",
                    "questions": [
                        {"id": "chest_pain_type", "type": "single_select", "label": "Chest pain type", "required": True, "options": ["Crushing", "Sharp", "Dull", "Burning", "Tearing"]},
                        {"id": "pain_severity", "type": "slider", "label": "Pain severity", "min": 0, "max": 10, "step": 1, "unit": "/10"},
                        {"id": "pain_location", "type": "multi_select", "label": "Pain location (select all that apply)", "required": False, "options": ["Central chest", "Left side", "Right side", "Radiates to arm", "Radiates to jaw", "Radiates to back"]},
                        {"id": "symptom_onset", "type": "date", "label": "Date of symptom onset", "required": False},
                        {"id": "symptom_duration", "type": "duration", "label": "Duration of symptoms", "required": False, "units": ["hours", "days", "weeks"]}
                    ]
                },
                {
                    "id": "risk_factors",
                    "title": "Risk Factors",
                    "questions": [
                        {"id": "smoking_status", "type": "single_select", "label": "Smoking status", "required": False, "options": ["Never", "Ex-smoker", "Current"]},
                        {"id": "diabetes", "type": "toggle", "label": "Diabetes", "required": False},
                        {"id": "hypertension", "type": "toggle", "label": "Hypertension", "required": False},
                        {"id": "family_history", "type": "toggle", "label": "Family history of IHD", "required": False}
                    ]
                },
                {
                    "id": "examination",
                    "title": "Examination Findings",
                    "questions": [
                        {"id": "ecg_findings", "type": "single_select", "label": "ECG findings", "required": True, "options": ["Normal", "ST elevation", "ST depression", "T wave inversion", "Pathological Q waves"]},
                        {"id": "troponin", "type": "single_select", "label": "Troponin result", "required": True, "options": ["Normal (<14 ng/L)", "Elevated (14-50 ng/L)", "High (>50 ng/L)"]},
                        {"id": "heart_rate", "type": "number", "label": "Heart rate (bpm)", "required": False, "placeholder": "e.g., 80"}
                    ]
                },
                {
                    "id": "red_flags",
                    "title": "⚠️ Red Flags",
                    "questions": [
                        {"id": "red_flag_mi", "type": "toggle", "label": "🔴 Myocardial Infarction - Cardiac sounding pain with haemodynamic instability", "required": False, "is_red_flag": True},
                        {"id": "red_flag_aortic", "type": "toggle", "label": "🔴 Aortic Dissection - Tearing pain with BP differential", "required": False, "is_red_flag": True},
                        {"id": "red_flag_pe", "type": "toggle", "label": "🔴 Pulmonary Embolism - Sudden pleuritic pain with hypoxia", "required": False, "is_red_flag": True}
                    ]
                },
                {
                    "id": "plan",
                    "title": "Management Plan",
                    "questions": [
                        {"id": "plan_details", "type": "textarea", "label": "Management plan", "required": False, "placeholder": "Describe the management plan..."}
                    ]
                }
            ]
        },
        "differentials": [
            "Myocardial Infarction",
            "Unstable Angina",
            "Aortic Dissection",
            "Pulmonary Embolism",
            "Pericarditis",
            "Costochondritis"
        ],
        "safetyNetting": [
            "Call 999 immediately if chest pain worsens",
            "Take GTN as prescribed (if applicable)",
            "Attend A&E if new symptoms develop",
            "Follow up with GP within 48 hours"
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
    
    print(f"✅ Template '{template_data['title']}' created with all question types!")
    db.close()

if __name__ == "__main__":
    seed_clinical_template()