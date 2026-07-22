from app.database import SessionLocal
from app.models import User, Template, Category

def seed_childfever_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: category = Category(name="Paediatrics"); db.add(category); db.commit()

    template_data = {
        "title": "Child Fever Assessment",
        "description": "Paediatric fever assessment using NICE traffic light system for identifying serious illness.",
        "category": "Paediatrics",
        "content": {
            "sections": [
                {
                    "title": "Fever History",
                    "questions": [
                        {"id": "cf_age", "type": "single_select", "label": "Age", "required": True, "options": ["<3 months", "3-6 months", "6-12 months", "1-2 years", "2-5 years", "5-12 years", ">12 years"]},
                        {"id": "cf_temp", "type": "number", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 38.5"},
                        {"id": "cf_duration", "type": "duration", "label": "Duration of Fever", "required": True, "units": ["hours", "days"]},
                        {"id": "cf_neonate", "type": "toggle", "label": "🔴 Age <3 Months with Fever?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Infant <3 months with fever. Urgent paediatric assessment and admission for septic screen.", "red_flag_negative": "Child is >3 months old."}
                    ]
                },
                {
                    "title": "NICE Traffic Light - Red Features",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "cf_colour", "type": "single_select", "label": "Colour", "required": True, "options": ["Normal", "Pale", "Mottled/Ashen/Blue"]},
                        {"id": "cf_activity", "type": "single_select", "label": "Activity/Response", "required": True, "options": ["Normal/Playing", "Responds to parents", "No response to social cues", "Does not wake/stay awake"]},
                        {"id": "cf_respiratory", "type": "toggle", "label": "🔴 Grunting/Tachypnoea/Chest Recession?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Respiratory distress. Urgent paediatric assessment required.", "red_flag_negative": "Normal breathing."},
                        {"id": "cf_hydration", "type": "single_select", "label": "Hydration Status", "required": True, "options": ["Normal/Good Intake", "Reduced Intake", "Dry Mucous Membranes", "Reduced Urine Output"]},
                        {"id": "cf_dehydration", "type": "toggle", "label": "🔴 Signs of Dehydration/Shock?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Clinical dehydration or shock. Urgent admission for IV fluids.", "red_flag_negative": "Adequate hydration."},
                        {"id": "cf_seizure", "type": "toggle", "label": "🔴 Seizure/Febrile Convulsion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Seizure with fever. Urgent assessment. Consider admission if first episode or prolonged.", "red_flag_negative": "No seizure activity."},
                        {"id": "cf_rash", "type": "toggle", "label": "🔴 Non-blanching Rash?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Non-blanching rash. Consider meningococcal disease. Emergency admission and antibiotics.", "red_flag_negative": "No rash or blanching rash only."},
                        {"id": "cf_neck", "type": "toggle", "label": "🔴 Neck Stiffness/Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Signs of meningism. Urgent admission for investigation.", "red_flag_negative": "No meningeal signs."}
                    ]
                },
                {
                    "title": "Examination Findings",
                    "questions": [
                        {"id": "cf_source", "type": "multi_select", "label": "Likely Source of Infection", "required": False, "options": ["URTI", "Otitis Media", "Tonsillitis", "Chest Infection", "UTI", "Viral Illness", "No Focus Found"]},
                        {"id": "cf_ears", "type": "single_select", "label": "Ear Examination", "required": False, "options": ["Normal", "Otitis Media", "Otitis Externa", "Not Examined"]},
                        {"id": "cf_throat", "type": "single_select", "label": "Throat Examination", "required": False, "options": ["Normal", "Erythema", "Exudate/Tonsillitis", "Not Examined"]},
                        {"id": "cf_chest", "type": "single_select", "label": "Chest Auscultation", "required": False, "options": ["Clear", "Crackles", "Wheeze", "Not Examined"]}
                    ]
                },
                {
                    "title": "Safety Netting & Plan",
                    "safety_netting": "Return immediately if: child becomes drowsy/unrousable, develops a non-blanching rash, has difficulty breathing, has a seizure, or stops drinking/urinating. Call 999 if seriously unwell.",
                    "questions": [
                        {"id": "cf_diagnosis", "type": "textarea", "label": "Working Diagnosis", "required": True},
                        {"id": "cf_management", "type": "textarea", "label": "Management Plan", "required": True, "placeholder": "e.g., Antipyretics, fluids, safety netting, when to return..."},
                        {"id": "cf_safety_net", "type": "toggle", "label": "Verbal & Written Safety Netting Given?", "required": True},
                        {"id": "cf_followup", "type": "single_select", "label": "Follow-up", "required": False, "options": ["None - Safety Net Only", "PRN if Worsens", "Review in 24-48hrs"]},
                        {"id": "cf_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    seed_childfever_template()