from app.database import SessionLocal
from app.models import User, Template, Category

def seed_sti_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Sexual Health").first()
    if not category: category = Category(name="Sexual Health"); db.add(category); db.commit()

    template_data = {
        "title": "STI Screening",
        "description": "Sexual health screening including risk assessment, testing, and partner notification.",
        "category": "Sexual Health",
        "content": {"sections": [
            {"title": "Risk Assessment", "questions": [
                {"id": "sti_age", "type": "number", "label": "Age", "required": True},
                {"id": "sti_gender", "type": "single_select", "label": "Gender", "required": True, "options": ["Male", "Female", "Trans Man", "Trans Woman", "Non-binary"]},
                {"id": "sti_orientation", "type": "single_select", "label": "Sexual Orientation", "required": True, "options": ["Heterosexual", "Gay", "Lesbian", "Bisexual", "Other"]},
                {"id": "sti_partners", "type": "number", "label": "New Sexual Partners in Last 3 Months", "required": True, "placeholder": "e.g., 2"},
                {"id": "sti_condoms", "type": "single_select", "label": "Condom Use", "required": True, "options": ["Always", "Sometimes", "Never"]},
                {"id": "sti_previous", "type": "toggle", "label": "Previous STI Diagnosis?", "required": True}
            ]},
            {"title": "Symptoms", "red_flag_threshold": 1, "questions": [
                {"id": "sti_symptoms", "type": "toggle", "label": "Any Symptoms?", "required": True},
                {"id": "sti_discharge", "type": "toggle", "label": "Urethral/Vaginal Discharge?", "required": False},
                {"id": "sti_dysuria", "type": "toggle", "label": "Dysuria?", "required": False},
                {"id": "sti_ulcers", "type": "toggle", "label": "Genital Ulcers/Sores?", "required": False},
                {"id": "sti_pelvic_pain", "type": "toggle", "label": "🔴 Pelvic Pain/Fever? (PID)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Possible pelvic inflammatory disease. Urgent treatment and referral required.", "red_flag_negative": "No pelvic pain or fever."},
                {"id": "sti_testicular", "type": "toggle", "label": "🔴 Testicular Pain/Swelling? (Epididymitis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Testicular pain/swelling. Consider epididymo-orchitis or torsion. Urgent assessment.", "red_flag_negative": "No testicular symptoms."}
            ]},
            {"title": "Testing & Results", "questions": [
                {"id": "sti_chlamydia", "type": "toggle", "label": "Chlamydia Test Done?", "required": False},
                {"id": "sti_gonorrhoea", "type": "toggle", "label": "Gonorrhoea Test Done?", "required": False},
                {"id": "sti_hiv", "type": "toggle", "label": "HIV Test Done?", "required": False},
                {"id": "sti_syphilis", "type": "toggle", "label": "Syphilis Test Done?", "required": False},
                {"id": "sti_hepatitis", "type": "toggle", "label": "Hepatitis B/C Test Done?", "required": False},
                {"id": "sti_sample", "type": "single_select", "label": "Sample Type", "required": False, "options": ["Urine", "Swab (self-taken)", "Swab (clinician)", "Bloods", "Multiple"]}
            ]},
            {"title": "Management & Partner Notification", "safety_netting": "If you develop severe pelvic pain, fever, or testicular pain, seek urgent medical attention. Contact clinic if symptoms persist after treatment.", "questions": [
                {"id": "sti_treatment", "type": "textarea", "label": "Treatment Given", "required": False, "placeholder": "e.g., Doxycycline 100mg BD for 7 days..."},
                {"id": "sti_partner_notify", "type": "toggle", "label": "Partner Notification Discussed?", "required": True},
                {"id": "sti_contraception", "type": "toggle", "label": "Contraception Discussed?", "required": False},
                {"id": "sti_prep", "type": "toggle", "label": "PrEP Discussed? (if high risk)", "required": False},
                {"id": "sti_followup", "type": "duration", "label": "Follow-up / Test of Cure", "required": False, "units": ["weeks"]},
                {"id": "sti_notes", "type": "textarea", "label": "Additional Notes", "required": False}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_sti_template()