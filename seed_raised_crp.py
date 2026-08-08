from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_crp():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised CRP",
        "description": "Assessment of elevated CRP. Covers infection, inflammation, autoimmune disease, malignancy, and when a very high CRP indicates serious pathology.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Context",
                "section_type": "history",
                "questions": [
                    {"id": "crp_level", "type": "text", "label": "CRP Level (mg/L)", "required": True, "placeholder": "e.g., 85", "is_red_flag": True, "red_flag_positive": "RED FLAG: CRP >100 = significant pathology likely. Infection, severe inflammation, or malignancy.", "red_flag_negative": "", "output_phrase": "CRP: {value} mg/L"},
                    {"id": "crp_symptoms", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Fever / rigors", "Cough / SOB", "Dysuria / urinary symptoms", "Abdominal pain", "Joint pain / swelling", "Weight loss / fatigue", "None — incidental finding"], "output_phrase": "Symptoms: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "crp_infection", "type": "toggle", "label": "Infection Suspected? (respiratory, urinary, skin, dental)", "required": True, "output_phrase": "Infection: {value}"},
                    {"id": "crp_autoimmune", "type": "toggle", "label": "Known Autoimmune Disease? (RA, SLE, IBD, PMR)", "required": True, "output_phrase": "Autoimmune: {value}"},
                    {"id": "crp_malignancy", "type": "toggle", "label": "Constitutional Symptoms? (weight loss, night sweats, fatigue)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Constitutional symptoms + raised CRP = ?malignancy. Urgent workup.", "red_flag_negative": "", "output_phrase": "?Malignancy: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Acute Infection (bacterial > viral)", "Chronic Inflammation / Autoimmune", "Malignancy", "Tissue Injury / Surgery", "Obesity (low-grade elevation)", "Smoking (low-grade elevation)"],
                "questions": [
                    {"id": "crp_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Infection — treat + repeat", "?Autoimmune — check ESR, autoantibodies", "?Malignancy — urgent workup", "Mild elevation — likely benign", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If infection: Treat. Repeat CRP if not settling. If ?autoimmune: Check ESR, rheumatoid factor, anti-CCP, ANA. If ?malignancy: Urgent workup (CXR, bloods, imaging). If mild elevation (<20) + well: Likely obesity/smoking/benign. Repeat in 3-6 months. Safety-net: Return if fever, weight loss, night sweats, or new symptoms.",
                "questions": [
                    {"id": "crp_action", "type": "single_select", "label": "Action", "required": True, "options": ["Treat infection + repeat CRP", "Autoimmune workup", "Urgent workup (malignancy)", "Reassure + repeat (mild, well)", "Routine investigation"], "output_phrase": "Action: {value}"},
                    {"id": "crp_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "crp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat CRP in 4 weeks. Investigate if persistent.", "output_phrase": "Follow-up: {value}"}
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
    seed_raised_crp()