from app.database import SessionLocal
from app.models import User, Template, Category

def seed_rash_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    template_data = {
        "title": "Rash Assessment",
        "description": "Structured assessment for skin rashes including red flags for serious conditions.",
        "category": "Dermatology",
        "content": {
            "sections": [
                {
                    "title": "Rash History",
                    "questions": [
                        {"id": "rash_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (hours)", "Gradual (days)", "Slow (weeks)"]},
                        {"id": "rash_location", "type": "multi_select", "label": "Location(s)", "required": True, "options": ["Face", "Trunk", "Arms", "Legs", "Hands/Feet", "Scalp", "Generalised"]},
                        {"id": "rash_type", "type": "multi_select", "label": "Lesion Type", "required": True, "options": ["Macular (flat)", "Papular (raised)", "Vesicular (blisters)", "Pustular", "Urticarial (hives)", "Scaly", "Erythematous (red)"]},
                        {"id": "rash_itch", "type": "single_select", "label": "Itch Severity", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "rash_duration", "type": "duration", "label": "Duration", "required": True, "units": ["days", "weeks"]}
                    ]
                },
                {
                    "title": "Red Flags & Systemic Symptoms",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "rash_fever", "type": "toggle", "label": "Fever Present?", "required": True},
                        {"id": "rash_meningococcal", "type": "toggle", "label": "🔴 Non-blanching/Purpuric? (Meningococcal)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Non-blanching rash. Consider meningococcal sepsis. Urgent admission and antibiotics.", "red_flag_negative": "Rash blanches normally."},
                        {"id": "rash_blistering", "type": "toggle", "label": "🔴 Extensive Blistering/Mucosal Involvement? (SJS/TEN)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Extensive blistering or mucosal involvement. Consider SJS/TEN. Urgent dermatology referral.", "red_flag_negative": "No severe blistering."},
                        {"id": "rash_systemic", "type": "toggle", "label": "Joint Pain/Swelling?", "required": False}
                    ]
                },
                {
                    "title": "Diagnosis & Plan",
                    "safety_netting": "If the rash spreads rapidly, develops blisters, or you feel systemically unwell, seek urgent medical attention.",
                    "questions": [
                        {"id": "rash_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Eczema/Dermatitis", "Urticaria", "Psoriasis", "Fungal Infection", "Viral Exanthem", "Drug Eruption", "Other"]},
                        {"id": "rash_treatment", "type": "textarea", "label": "Treatment Plan", "required": True, "placeholder": "e.g., Emollients, topical steroids, antihistamines..."},
                        {"id": "rash_followup", "type": "duration", "label": "Follow-up", "required": False, "units": ["weeks"]}
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
    seed_rash_template()