from app.database import SessionLocal
from app.models import User, Template, Category

def seed_headache_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Neurology").first()
    if not category:
        category = Category(name="Neurology")
        db.add(category)
        db.commit()

    template_data = {
        "title": "Headache Assessment",
        "description": "Structured assessment for patients presenting with headache. Includes red flags for serious pathology.",
        "category": "Neurology",
        "content": {
            "sections": [
                {
                    "title": "Headache History",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "ha_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (thunderclap)", "Gradual (hours)", "Gradual (days)"]},
                        {"id": "ha_thunderclap", "type": "toggle", "label": "🔴 Thunderclap Onset? (SAH Red Flag)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Thunderclap headache. Urgent CT/MRI and neurosurgical referral required.", "red_flag_negative": "No thunderclap onset."},
                        {"id": "ha_location", "type": "single_select", "label": "Location", "required": True, "options": ["Unilateral", "Bilateral", "Frontal", "Occipital", "Generalised"]},
                        {"id": "ha_character", "type": "single_select", "label": "Character", "required": True, "options": ["Throbbing/Pulsating", "Pressing/Tightening", "Sharp/Stabbing", "Dull"]},
                        {"id": "ha_severity", "type": "slider", "label": "Pain Severity (1-10)", "required": True, "min": 1, "max": 10},
                        {"id": "ha_duration", "type": "single_select", "label": "Duration", "required": True, "options": ["<1 hour", "1-4 hours", "4-72 hours", ">72 hours", "Continuous"]},
                        {"id": "ha_frequency", "type": "single_select", "label": "Frequency", "required": True, "options": ["Daily", "Weekly", "Monthly", "Occasional"]}
                    ]
                },
                {
                    "title": "Associated Symptoms",
                    "questions": [
                        {"id": "ha_aura", "type": "toggle", "label": "Aura Present?", "required": False},
                        {"id": "ha_nausea", "type": "toggle", "label": "Nausea/Vomiting?", "required": False},
                        {"id": "ha_photophobia", "type": "toggle", "label": "Photophobia?", "required": False},
                        {"id": "ha_phonophobia", "type": "toggle", "label": "Phonophobia?", "required": False},
                        {"id": "ha_neurological", "type": "toggle", "label": "🔴 Neurological Symptoms? (Weakness/Numbness/Vision)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Focal neurological symptoms. Urgent neuroimaging required.", "red_flag_negative": "No focal neurological symptoms."},
                        {"id": "ha_systemic", "type": "toggle", "label": "🔴 Systemic Symptoms? (Fever/Weight Loss/Stiff Neck)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Systemic symptoms with headache. Consider meningitis, temporal arteritis, or malignancy.", "red_flag_negative": "No systemic symptoms."}
                    ]
                },
                {
                    "title": "Examination & Assessment",
                    "examination": "Neurological examination including cranial nerves, fundoscopy, BP, neck stiffness assessment",
                    "safety_netting": "If headache becomes sudden and severe, or you develop weakness, vision changes, or confusion, seek urgent medical attention or call 999.",
                    "questions": [
                        {"id": "ha_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Tension-type Headache", "Migraine", "Cluster Headache", "Medication Overuse", "Sinus Headache", "Other"]},
                        {"id": "ha_management", "type": "textarea", "label": "Management Plan", "required": True, "placeholder": "e.g., Lifestyle advice, acute treatment, prophylaxis..."},
                        {"id": "ha_followup", "type": "duration", "label": "Follow-up", "required": False, "units": ["weeks", "months"]}
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
    seed_headache_template()