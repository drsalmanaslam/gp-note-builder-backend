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
    
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return

    template = Template(
        title=title,
        description="Focused assessment for viral upper respiratory tract infection covering red flags for LRTI, asthma considerations, and symptomatic management.",
        category="Respiratory",
        content={"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "urti_presenting_complaint", "type": "text", "label": "Presentation", "required": True, "placeholder": "e.g., Cough and runny nose for 2 days", "output_phrase": "c/o: {value}"},
                    {"id": "urti_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 days", "output_phrase": "Duration: {value}"},
                    {"id": "urti_main_symptom", "type": "single_select", "label": "Associations", "required": True, "options": ["Cough", "Sore throat", "Wheeze", "Nasal congestion / coryza", "Fever", "Malaise / fatigue"], "output_phrase": "Associated symptoms: {value}"},
                    {"id": "urti_red_flags", "type": "multi_select", "label": "Red Flags", "required": True, "options": ["Shortness of breath", "Chest pain", "Haemoptysis", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB/wheeze/chest pain/haemoptysis = ?LRTI, pneumonia, PE.", "red_flag_negative": "", "output_phrase": "Red flags: {value}"},
                    {"id": "urti_asthma", "type": "single_select", "label": "Asthma History", "required": True, "options": ["Asthmatic - on preventer", "Asthmatic - no preventer", "Non-asthmatic"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Asthmatic + URTI = risk of exacerbation.", "red_flag_negative": "", "output_phrase": "Asthma: {value}"},
                    {"id": "urti_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Current smoker", "Ex-smoker", "Non-smoker"], "output_phrase": "Smoking: {value}"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "urti_resp", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Equal air entry B/L, vesicular BS, no added sounds, no clubbing", "Reduced air entry", "Added sounds (wheeze/crackles) - RED FLAG", "Clubbing present - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Crackles = ?pneumonia/LRTI. Wheeze = ?exacerbation.", "red_flag_negative": "", "output_phrase": "Respiratory: {value}"},
                    {"id": "urti_ent", "type": "single_select", "label": "ENT Examination", "required": False, "options": ["Normal", "Pharyngeal erythema", "Tonsillar exudate (?bacterial)", "Cervical lymphadenopathy", "Abnormal"], "output_phrase": "ENT: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Viral URTI (Self limiting upto 10 days)", "Acute Bronchitis", "Community Acquired Pneumonia", "Infective Exacerbation of Asthma", "COVID 19", "Influenza", "Allergic Rhinitis", "Sinusitis"],
                "questions": [
                    {"id": "urti_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Viral URTI", "COVID 19", "Community Acquired Pneumonia", "Acute bronchitis", "Asthma exacerbation", "Influenza", "Allergic Rhinitis", "Sinusitis"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: increased respiratory rate, chest pain, shortness of breath, haemoptysis, high fever >39°C, confusion, or symptoms worsen significantly. Viral URTI is self-limiting (7-10 days). Antibiotics NOT indicated for viral URTI. Symptomatic treatment: Paracetamol PRN, Exputex/Bisolvon for cough. Honey and lemon for sore throat. Steam inhalation for congestion. If asthmatic: ensure using preventer regularly.",
                "questions": [
                    {"id": "urti_symptomatic", "type": "multi_select", "label": "Symptomatic Treatment", "required": False, "options": ["Paracetamol PRN", "Trial of Exputex / Bisolvon oral solution (cough)", "Honey + lemon (sore throat)", "Steam inhalation (congestion)", "None"], "output_phrase": "Symptomatic treatment: {value}"},
                    {"id": "urti_antibiotics", "type": "toggle", "label": "Antibiotics Prescribed?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Antibiotics NOT indicated for viral URTI. Only consider if crackles, fever, purulent sputum.", "red_flag_negative": "", "output_phrase": "Antibiotics: {value}"},
                    {"id": "urti_red_flags_discussed", "type": "toggle", "label": "Red Flags Discussed?", "required": True, "output_phrase": "Red flags discussed: {value}"},
                    {"id": "urti_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., No follow-up required - return if red flags", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        is_public=True,
        created_by=admin.id,
        clinical_references='[{"label": "HSE URTI Guidelines", "url": "https://www.hse.ie/eng/health/az/u/upper-respiratory-tract-infection/"}, {"label": "NICE NG120 - Cough (Acute)", "url": "https://www.nice.org.uk/guidance/ng120"}, {"label": "Heidi Evidence - URTI", "url": "https://app.heidi-app.com/search?q=URTI"}]'
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_urti()