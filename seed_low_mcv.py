from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_low_mcv():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low MCV (Microcytosis)",
        "description": "Assessment of microcytosis (MCV <80 fL). Covers iron deficiency, thalassaemia, and anaemia of chronic disease.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & History",
                "section_type": "history",
                "questions": [
                    {"id": "lmcv_level", "type": "text", "label": "MCV (fL)", "required": True, "placeholder": "e.g., 72", "output_phrase": "MCV: {value} fL"},
                    {"id": "lmcv_hb", "type": "text", "label": "Haemoglobin (g/L)", "required": True, "placeholder": "e.g., 105", "output_phrase": "Hb: {value} g/L"},
                    {"id": "lmcv_ferritin", "type": "text", "label": "Ferritin (if checked)", "required": False, "placeholder": "e.g., 8", "output_phrase": "Ferritin: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "lmcv_iron_def", "type": "multi_select", "label": "Iron Deficiency Causes", "required": True, "options": ["Heavy menstrual bleeding", "GI bleeding — ?NSAID, ulcer, cancer", "Poor diet / vegan", "Malabsorption — coeliac, gastrectomy", "Pregnancy", "None"], "output_phrase": "Iron def: {value}"},
                    {"id": "lmcv_thalassaemia", "type": "toggle", "label": "Ethnicity at Risk for Thalassaemia? (Mediterranean, Middle East, South Asian, African)", "required": True, "output_phrase": "?Thalassaemia: {value}"},
                    {"id": "lmcv_chronic", "type": "toggle", "label": "Chronic Disease? (CKD, inflammatory, malignancy, heart failure)", "required": True, "output_phrase": "Chronic disease: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Iron Deficiency Anaemia", "Thalassaemia Trait (alpha or beta)", "Anaemia of Chronic Disease", "Sideroblastic Anaemia (rare)", "Lead Poisoning (rare)"],
                "questions": [
                    {"id": "lmcv_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Iron deficiency — investigate cause + replace", "?Thalassaemia — check ferritin + haemoglobinopathy screen", "?Chronic disease — manage underlying", "Isolated — observe"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Check ferritin, iron studies. If iron deficient: Investigate cause (GI bleeding, menorrhagia, coeliac). Iron replacement. If ferritin normal + microcytosis: ?Thalassaemia trait — haemoglobinopathy screen. If chronic disease: Manage underlying condition. Safety-net: Return if fatigue, weight loss, bleeding, or GI symptoms.",
                "questions": [
                    {"id": "lmcv_action", "type": "single_select", "label": "Action", "required": True, "options": ["Iron studies + investigate cause", "Iron replacement", "Haemoglobinopathy screen", "Reassure + repeat"], "output_phrase": "Action: {value}"},
                    {"id": "lmcv_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "lmcv_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Iron studies + coeliac screen. Review in 2 weeks.", "output_phrase": "Follow-up: {value}"}
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
    seed_low_mcv()