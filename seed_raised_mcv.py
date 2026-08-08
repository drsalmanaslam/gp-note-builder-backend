from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_mcv():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised MCV (Macrocytosis)",
        "description": "Assessment of macrocytosis (MCV >100 fL). Covers B12/folate deficiency, alcohol, liver disease, hypothyroidism, and drugs.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & History",
                "section_type": "history",
                "questions": [
                    {"id": "mcv_level", "type": "text", "label": "MCV (fL)", "required": True, "placeholder": "e.g., 106", "output_phrase": "MCV: {value} fL"},
                    {"id": "mcv_hb", "type": "text", "label": "Haemoglobin (g/L)", "required": True, "placeholder": "e.g., 128", "output_phrase": "Hb: {value} g/L"},
                    {"id": "mcv_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within limits", "Excess — >14 units/week", "Heavy — >35 units/week"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Excess alcohol = commonest cause of macrocytosis. Check LFTs, GGT. Brief intervention.", "red_flag_negative": "", "output_phrase": "Alcohol: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "mcv_b12", "type": "toggle", "label": "B12 / Folate Deficiency? (check levels, dietary history, metformin, PPI)", "required": True, "output_phrase": "?B12/Folate: {value}"},
                    {"id": "mcv_liver", "type": "toggle", "label": "Liver Disease? (check LFTs, jaundice, ascites)", "required": True, "output_phrase": "Liver: {value}"},
                    {"id": "mcv_hypothyroid", "type": "toggle", "label": "Hypothyroidism? (check TFTs, fatigue, weight gain)", "required": True, "output_phrase": "?Hypothyroid: {value}"},
                    {"id": "mcv_drugs", "type": "multi_select", "label": "Drugs Causing Macrocytosis", "required": False, "options": ["Methotrexate", "Azathioprine", "Zidovudine", "Phenytoin", "None"], "output_phrase": "Drugs: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Alcohol (commonest)", "B12/Folate Deficiency", "Liver Disease", "Hypothyroidism", "Drug-Induced", "Myelodysplasia (if pancytopenia or other cytopenias)", "Reticulocytosis (haemolysis, bleeding)"],
                "questions": [
                    {"id": "mcv_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Alcohol — check LFTs, GGT, brief intervention", "?B12/Folate deficiency — check levels", "?Hypothyroid — check TFTs", "?Drug-induced — review medications", "Isolated — observe"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Check B12, folate, LFTs, GGT, TFTs. Blood film. If alcohol-related: Brief intervention. If B12/folate deficient: Replace. If no cause found + isolated macrocytosis + normal Hb: Reassure, repeat in 3-6 months. Safety-net: Return if fatigue, weight loss, bleeding, or new symptoms.",
                "questions": [
                    {"id": "mcv_action", "type": "single_select", "label": "Action", "required": True, "options": ["Check B12/folate/LFTs/TFTs + review", "Brief alcohol intervention", "Replace B12/folate", "Reassure + repeat in 3 months", "Refer haematology (?MDS)"], "output_phrase": "Action: {value}"},
                    {"id": "mcv_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "mcv_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Check bloods + review in 2 weeks.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]; existing.content = t["content"]; existing.category = t["category"]; existing.is_public = t["is_public"]; existing.updated_at = datetime.now(timezone.utc)
        db.commit(); print(f"Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t); db.commit(); print(f"Created: {t['title']}")
    db.close()

if __name__ == "__main__":
    seed_raised_mcv()