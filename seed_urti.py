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

    t = {
        "title": "Viral URTI",
        "description": "Focused assessment for viral upper respiratory tract infection covering red flags for LRTI, asthma considerations, and symptomatic management.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "urti_presenting_complaint", 
                        "type": "text", 
                        "label": "Presenting Complaint", 
                        "required": True, 
                        "placeholder": "e.g., Cough and runny nose for 2 days",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "urti_duration", 
                        "type": "text", 
                        "label": "Duration of Symptoms", 
                        "required": True, 
                        "placeholder": "e.g., 2 days",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "urti_main_symptom", 
                        "type": "single_select", 
                        "label": "Presenting Symptom", 
                        "required": True, 
                        "options": ["Cough", "Sore throat", "Nasal congestion / coryza", "Fever", "Malaise / fatigue"],
                        "output_phrase": "Associated symptoms: {value}"  # 👈 CHANGED THIS
                    },
                    {
                        "id": "urti_red_flags", 
                        "type": "multi_select", 
                        "label": "Respiratory Red Flag Screen", 
                        "required": True, 
                        "options": ["Shortness of breath", "Wheeze", "Chest pain", "Haemoptysis", "None present"], 
                        "is_red_flag": True, 
                        "red_flag_positive": "RED FLAG: SOB/wheeze/chest pain/haemoptysis = ?LRTI, pneumonia, PE. Examine + consider CXR.", 
                        "red_flag_negative": "",
                        "output_phrase": "Red flags: {value}"
                    },
                    {
                        "id": "urti_asthma", 
                        "type": "single_select", 
                        "label": "Asthma History", 
                        "required": True, 
                        "options": ["Asthmatic - on preventer", "Asthmatic - no preventer", "Non-asthmatic"], 
                        "is_red_flag": True, 
                        "red_flag_positive": "RED FLAG: Asthmatic + URTI = risk of exacerbation. Ensure using preventer. Consider oral steroids if wheeze.", 
                        "red_flag_negative": "",
                        "output_phrase": "Asthma: {value}"
                    },
                    {
                        "id": "urti_smoking", 
                        "type": "single_select", 
                        "label": "Smoking Status", 
                        "required": True, 
                        "options": ["Current smoker", "Ex-smoker", "Non-smoker"],
                        "output_phrase": "Smoking: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "urti_vitals", 
                        "type": "text", 
                        "label": "Vital Signs", 
                        "required": True, 
                        "placeholder": "e.g., Temp 36.9°C, HR 75, SpO2 99%",
                        "output_phrase": "Vitals: {value}"
                    },
                    {
                        "id": "urti_resp", 
                        "type": "single_select", 
                        "label": "Respiratory Examination", 
                        "required": True, 
                        "options": [
                            "Equal air entry B/L, vesicular BS, no added sounds, no clubbing", 
                            "Reduced air entry", 
                            "Added sounds (wheeze/crackles) - RED FLAG", 
                            "Clubbing present - RED FLAG"
                        ], 
                        "is_red_flag": True, 
                        "red_flag_positive": "RED FLAG: Crackles = ?pneumonia/LRTI. Wheeze = ?exacerbation. Consider CXR + antibiotics.", 
                        "red_flag_negative": "",
                        "output_phrase": "Respiratory: {value}"
                    },
                    {
                        "id": "urti_ent", 
                        "type": "single_select", 
                        "label": "ENT Examination", 
                        "required": False, 
                        "options": ["Normal", "Pharyngeal erythema", "Tonsillar exudate (?bacterial)", "Cervical lymphadenopathy", "Abnormal"],
                        "output_phrase": "ENT: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Viral URTI (most common - self-limiting 7-10 days)",
                    "Acute Bronchitis",
                    "Community-Acquired Pneumonia (RED FLAG - crackles, fever, SOB)",
                    "Infective Exacerbation of Asthma",
                    "COVID-19",
                    "Influenza",
                    "Allergic Rhinitis",
                    "Sinusitis"
                ],
                "questions": [
                    {
                        "id": "urti_diagnosis", 
                        "type": "single_select", 
                        "label": "Clinical Impression", 
                        "required": True, 
                        "options": ["Viral URTI", "Lower respiratory tract infection suspected", "Acute bronchitis", "Asthma exacerbation", "Alternative diagnosis"],
                        "output_phrase": "Diagnosis: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: increased respiratory rate, chest pain, shortness of breath, haemoptysis, high fever >39°C, confusion, or symptoms worsen significantly. Viral URTI is self-limiting (7-10 days). Antibiotics NOT indicated for viral URTI. Symptomatic treatment: Paracetamol PRN for fever/pain, trial of Exputex/Bisolvon oral solution for cough. Honey and lemon for sore throat. Steam inhalation for congestion. If asthmatic: ensure using preventer regularly, consider stepping up if wheeze develops. If smoker: advise cessation (URTI risk + chronic cough). No routine follow-up required unless red flags develop.",
                "questions": [
                    {
                        "id": "urti_symptomatic", 
                        "type": "multi_select", 
                        "label": "Symptomatic Treatment", 
                        "required": False, 
                        "options": ["Paracetamol PRN", "Trial of Exputex / Bisolvon oral solution (cough)", "Honey + lemon (sore throat)", "Steam inhalation (congestion)", "None"],
                        "output_phrase": "Symptomatic treatment: {value}"
                    },
                    {
                        "id": "urti_antibiotics", 
                        "type": "toggle", 
                        "label": "Antibiotics Prescribed? (Only if bacterial LRTI suspected)", 
                        "required": False, 
                        "is_red_flag": True, 
                        "red_flag_positive": "RED FLAG: Antibiotics NOT indicated for viral URTI. Only consider if crackles, fever, purulent sputum (pneumonia).", 
                        "red_flag_negative": "",
                        "output_phrase": "Antibiotics: {value}"
                    },
                    {
                        "id": "urti_red_flags_discussed", 
                        "type": "toggle", 
                        "label": "Red Flags Discussed? (Increased RR, chest pain, deterioration)", 
                        "required": True,
                        "output_phrase": "Red flags discussed: {value}"
                    },
                    {
                        "id": "urti_followup", 
                        "type": "text", 
                        "label": "Follow-up Plan", 
                        "required": True, 
                        "placeholder": "e.g., No follow-up required - self-limiting, return if red flags, or review in 1 week if not improving",
                        "output_phrase": "Follow-up: {value}"
                    }
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
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
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    
    db.close()

if __name__ == "__main__":
    seed_urti()