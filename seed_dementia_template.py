from app.database import SessionLocal
from app.models import User, Template, Category

def seed_dementia_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Elderly Care").first()
    if not category: category = Category(name="Elderly Care"); db.add(category); db.commit()

    template_data = {
        "title": "Dementia Screening",
        "description": "Cognitive assessment including 6-CIT, MMSE, reversible causes, and care planning.",
        "category": "Elderly Care",
        "content": {"sections": [
            {"title": "History & Informant Report", "questions": [
                {"id": "dem_age", "type": "number", "label": "Age", "required": True},
                {"id": "dem_symptoms", "type": "multi_select", "label": "Reported Symptoms", "required": True, "options": ["Memory Loss", "Word-finding Difficulty", "Disorientation", "Poor Judgement", "Mood Changes", "Difficulty with Daily Tasks", "Getting Lost"]},
                {"id": "dem_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Gradual (months-years)", "Stepwise", "Sudden (days-weeks)"]},
                {"id": "dem_duration", "type": "duration", "label": "Duration", "required": True, "units": ["months", "years"]},
                {"id": "dem_informant", "type": "toggle", "label": "Informant/Collateral History Available?", "required": True},
                {"id": "dem_functional", "type": "single_select", "label": "Impact on Daily Function", "required": True, "options": ["Independent", "Needs Prompts", "Needs Assistance", "Fully Dependent"]}
            ]},
            {"title": "Cognitive Assessment", "questions": [
                {"id": "dem_6cit", "type": "number", "label": "6-CIT Score (0-28)", "required": False, "placeholder": "Higher = more impaired"},
                {"id": "dem_mmse", "type": "number", "label": "MMSE Score (0-30)", "required": False},
                {"id": "dem_clock", "type": "toggle", "label": "Clock Drawing Test Abnormal?", "required": False},
                {"id": "dem_mood", "type": "single_select", "label": "Mood Assessment", "required": True, "options": ["Normal", "Low/Depressed", "Anxious", "Irritable", "Apathetic"]},
                {"id": "dem_depression", "type": "toggle", "label": "Consider Depression as Cause? (Pseudodementia)", "required": True}
            ]},
            {"title": "Reversible Causes & Investigations", "red_flag_threshold": 1, "questions": [
                {"id": "dem_bloods", "type": "toggle", "label": "Bloods Done? (FBC, U&E, LFT, TFT, B12, Folate, Glucose)", "required": True},
                {"id": "dem_b12", "type": "toggle", "label": "B12/Folate Deficiency?", "required": False},
                {"id": "dem_thyroid", "type": "toggle", "label": "Thyroid Dysfunction?", "required": False},
                {"id": "dem_infection", "type": "toggle", "label": "Exclude UTI/Chest Infection?", "required": True},
                {"id": "dem_imaging", "type": "toggle", "label": "CT/MRI Head Performed?", "required": False},
                {"id": "dem_rapid", "type": "toggle", "label": "🔴 Rapid Decline (<6 months)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Rapid cognitive decline. Consider CJD, paraneoplastic, autoimmune encephalitis. Urgent neurology referral.", "red_flag_negative": "Gradual decline consistent with neurodegenerative cause."}
            ]},
            {"title": "Diagnosis & Care Planning", "safety_netting": "If sudden worsening, confusion, or aggressive behaviour develops, seek urgent medical assessment. For safeguarding concerns, contact social services.", "questions": [
                {"id": "dem_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Alzheimer's Disease", "Vascular Dementia", "Mixed Dementia", "Lewy Body Dementia", "Frontotemporal Dementia", "Mild Cognitive Impairment", "Delirium Superimposed", "Other"]},
                {"id": "dem_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["GP Management", "Memory Clinic", "Neurology", "Psychiatry (Older Adults)"]},
                {"id": "dem_medication", "type": "textarea", "label": "Medication (e.g., Donepezil, Memantine)", "required": False},
                {"id": "dem_capacity", "type": "toggle", "label": "Capacity Assessment Done?", "required": False},
                {"id": "dem_lpa", "type": "toggle", "label": "LPA/Advance Care Planning Discussed?", "required": False},
                {"id": "dem_carer", "type": "toggle", "label": "Carer Support Discussed?", "required": True},
                {"id": "dem_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["months"]}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_dementia_template()