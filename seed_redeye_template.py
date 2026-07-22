from app.database import SessionLocal
from app.models import User, Template, Category

def seed_redeye_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    template_data = {
        "title": "Red Eye Assessment",
        "description": "Assessment for red eye including red flags for serious ophthalmology conditions.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {"title": "Symptoms", "red_flag_threshold": 1, "questions": [
                {"id": "re_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
                {"id": "re_eye", "type": "single_select", "label": "Affected Eye", "required": True, "options": ["Right", "Left", "Both"]},
                {"id": "re_pain", "type": "single_select", "label": "Pain Severity", "required": True, "options": ["None", "Mild Discomfort/Gritty", "Moderate", "Severe"]},
                {"id": "re_severe_pain", "type": "toggle", "label": "🔴 Severe Pain/Vomiting? (Acute Glaucoma)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe eye pain with nausea. Consider acute angle closure glaucoma. Urgent ophthalmology referral.", "red_flag_negative": "No severe pain."},
                {"id": "re_vision", "type": "toggle", "label": "🔴 Reduced Visual Acuity?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced vision with red eye. Urgent ophthalmology assessment required.", "red_flag_negative": "Vision unaffected."},
                {"id": "re_photophobia", "type": "toggle", "label": "Photophobia?", "required": False},
                {"id": "re_discharge", "type": "single_select", "label": "Discharge", "required": True, "options": ["None", "Watery", "Purulent/Sticky", "Mucoid"]},
                {"id": "re_trauma", "type": "toggle", "label": "History of Trauma/Foreign Body?", "required": True}
            ]},
            {"title": "Examination", "questions": [
                {"id": "re_pattern", "type": "single_select", "label": "Redness Pattern", "required": True, "options": ["Conjunctival (diffuse)", "Ciliary Flush (around cornea)", "Localised/Sectoral"]},
                {"id": "re_cornea", "type": "single_select", "label": "Cornea", "required": False, "options": ["Clear", "Hazy/Cloudy", "Fluorescein Staining Positive", "Not Examined"]},
                {"id": "re_pupil", "type": "single_select", "label": "Pupil", "required": False, "options": ["Normal/Reactive", "Dilated/Fixed", "Mid-dilated/Oval", "Not Examined"]}
            ]},
            {"title": "Diagnosis & Plan", "safety_netting": "If vision deteriorates, pain becomes severe, or you develop nausea/vomiting, seek urgent eye casualty review.", "differentials": ["Conjunctivitis (viral/bacterial/allergic)", "Subconjunctival Haemorrhage", "Corneal Abrasion/Foreign Body", "Anterior Uveitis/Iritis", "Acute Angle Closure Glaucoma", "Scleritis/Episcleritis", "Herpes Keratitis"], "questions": [
                {"id": "re_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Bacterial Conjunctivitis", "Viral Conjunctivitis", "Allergic Conjunctivitis", "Subconjunctival Haemorrhage", "Corneal Abrasion", "Iritis/Uveitis", "Other"]},
                {"id": "re_treatment", "type": "textarea", "label": "Treatment", "required": True, "placeholder": "e.g., Chloramphenicol eye drops QDS for 5 days..."},
                {"id": "re_followup", "type": "single_select", "label": "Follow-up", "required": False, "options": ["None", "PRN", "Review 48hrs", "Eye Casualty"]}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_redeye_template()