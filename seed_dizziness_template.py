from app.database import SessionLocal
from app.models import User, Template, Category

def seed_dizziness_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Neurology").first()
    if not category: category = Category(name="Neurology"); db.add(category); db.commit()

    template_data = {
        "title": "Dizziness & Vertigo Assessment",
        "description": "Assessment for dizziness/vertigo including HINTS exam, Dix-Hallpike, and red flags for central causes.",
        "category": "Neurology",
        "content": {"sections": [
            {"title": "Symptom Characterisation", "red_flag_threshold": 1, "questions": [
                {"id": "diz_type", "type": "single_select", "label": "Type of Dizziness", "required": True, "options": ["Vertigo (spinning/room moving)", "Pre-syncope (feeling faint)", "Disequilibrium (unsteady)", "Light-headedness"]},
                {"id": "diz_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
                {"id": "diz_duration", "type": "single_select", "label": "Duration of Episodes", "required": True, "options": ["Seconds", "Minutes", "Hours", "Days", "Continuous"]},
                {"id": "diz_triggers", "type": "multi_select", "label": "Triggers", "required": False, "options": ["Head Movement", "Position Change", "Standing Up", "Stress", "None"]},
                {"id": "diz_neuro_sudden", "type": "toggle", "label": "🔴 Sudden Onset with Neurological Symptoms? (Stroke)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute vestibular syndrome with neurological features. Consider posterior circulation stroke. Urgent CT/MRI.", "red_flag_negative": "No acute neurological features."}
            ]},
            {"title": "Associated Symptoms", "questions": [
                {"id": "diz_nausea", "type": "toggle", "label": "Nausea/Vomiting?", "required": False},
                {"id": "diz_hearing", "type": "toggle", "label": "Hearing Loss/Tinnitus?", "required": False},
                {"id": "diz_headache", "type": "toggle", "label": "Headache?", "required": False},
                {"id": "diz_neuro_symptoms", "type": "toggle", "label": "🔴 Diplopia/Dysarthria/Ataxia/Weakness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Focal neurological symptoms with dizziness. Urgent neuroimaging required.", "red_flag_negative": "No focal neurology."},
                {"id": "diz_nystagmus", "type": "single_select", "label": "Nystagmus", "required": False, "options": ["None", "Horizontal (Unidirectional)", "Horizontal (Direction-changing)", "Vertical/Rotatory", "Not Examined"]},
                {"id": "diz_hints", "type": "single_select", "label": "HINTS Exam (if acute vertigo)", "required": False, "options": ["Peripheral Pattern (Reassuring)", "Central Pattern (Concerning)", "Not Performed"]}
            ]},
            {"title": "Diagnosis & Plan", "safety_netting": "If dizziness becomes severe, you develop speech difficulty, facial droop, limb weakness, or severe headache, call 999 immediately.", "differentials": ["BPPV", "Vestibular Neuronitis", "Labyrinthitis", "Meniere's Disease", "Vestibular Migraine", "Posterior Circulation Stroke", "Orthostatic Hypotension"], "questions": [
                {"id": "diz_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["BPPV", "Vestibular Neuronitis", "Labyrinthitis", "Meniere's Disease", "Vestibular Migraine", "Orthostatic Hypotension", "Other"]},
                {"id": "diz_treatment", "type": "textarea", "label": "Treatment", "required": True, "placeholder": "e.g., Epley manoeuvre, prochlorperazine, betahistine..."},
                {"id": "diz_followup", "type": "duration", "label": "Follow-up", "required": False, "units": ["weeks"]}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_dizziness_template()