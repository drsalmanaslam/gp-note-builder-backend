from app.database import SessionLocal
from app.models import User, Template, Category

def seed_menstrual_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Gynaecology").first()
    if not category: category = Category(name="Gynaecology"); db.add(category); db.commit()

    template_data = {
        "title": "Heavy Menstrual Bleeding Assessment",
        "description": "Assessment for heavy menstrual bleeding including FIGO classification and management options.",
        "category": "Gynaecology",
        "content": {"sections": [
            {"title": "Bleeding History", "questions": [
                {"id": "hmb_age", "type": "number", "label": "Age", "required": True},
                {"id": "hmb_duration", "type": "duration", "label": "Duration of Heavy Bleeding", "required": True, "units": ["days"]},
                {"id": "hmb_cycle", "type": "single_select", "label": "Cycle", "required": True, "options": ["Regular", "Irregular", "Continuous"]},
                {"id": "hmb_flooding", "type": "toggle", "label": "Flooding/Clots?", "required": True},
                {"id": "hmb_pads", "type": "number", "label": "Sanitary Protection Changed Per Day", "required": False, "placeholder": "e.g., 8"},
                {"id": "hmb_impact", "type": "single_select", "label": "Impact on Quality of Life", "required": True, "options": ["None", "Mild", "Moderate", "Severe - Missing Work/Social"]}
            ]},
            {"title": "Red Flags & Examination", "red_flag_threshold": 1, "questions": [
                {"id": "hmb_postcoital", "type": "toggle", "label": "🔴 Postcoital Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postcoital bleeding. 2WW gynaecology referral for colposcopy.", "red_flag_negative": "No postcoital bleeding."},
                {"id": "hmb_intermenstrual", "type": "toggle", "label": "🔴 Intermenstrual Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Intermenstrual bleeding. Consider 2WW referral if persistent.", "red_flag_negative": "No intermenstrual bleeding."},
                {"id": "hmb_pelvic", "type": "toggle", "label": "Pelvic Pain/Dyspareunia?", "required": False},
                {"id": "hmb_anaemia", "type": "toggle", "label": "🔴 Symptoms of Anaemia? (Fatigue/SOB/Pallor)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Symptomatic anaemia. Check FBC and consider urgent management.", "red_flag_negative": "No anaemia symptoms."},
                {"id": "hmb_smear", "type": "toggle", "label": "Cervical Screening Up to Date?", "required": True}
            ]},
            {"title": "Investigations & Management", "safety_netting": "If bleeding becomes very heavy (soaking through protection hourly) or you feel dizzy/faint, seek urgent medical attention.", "questions": [
                {"id": "hmb_fbc", "type": "toggle", "label": "FBC Checked?", "required": False},
                {"id": "hmb_hb", "type": "number", "label": "Hb (g/L)", "required": False},
                {"id": "hmb_ferritin", "type": "number", "label": "Ferritin", "required": False},
                {"id": "hmb_contraception", "type": "single_select", "label": "Current Contraception", "required": False, "options": ["None", "COCP", "POP", "IUS/Mirena", "Implant", "Depo", "Barrier"]},
                {"id": "hmb_management", "type": "textarea", "label": "Management Plan", "required": True, "placeholder": "e.g., Tranexamic acid, Mirena coil, mefenamic acid..."},
                {"id": "hmb_referral", "type": "single_select", "label": "Referral Needed?", "required": False, "options": ["No", "Routine Gynaecology", "2WW Referral", "Urgent"]},
                {"id": "hmb_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["weeks", "months"]}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_menstrual_template()