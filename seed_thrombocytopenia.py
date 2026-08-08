from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_thrombocytopenia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low Platelets (Thrombocytopenia)",
        "description": "Assessment of thrombocytopenia (platelets <150 x10^9/L). Covers ITP, drugs, liver disease, infection, and bone marrow disorders.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Severity",
                "section_type": "history",
                "questions": [
                    {"id": "ltp_platelets", "type": "text", "label": "Platelet Count (x10^9/L)", "required": True, "placeholder": "e.g., 85", "is_red_flag": True, "red_flag_positive": "RED FLAG: Platelets <50 = significant thrombocytopenia. Risk of bleeding. Urgent haematology referral if <20 or bleeding.", "red_flag_negative": "", "output_phrase": "Platelets: {value}"},
                    {"id": "ltp_bleeding", "type": "multi_select", "label": "Bleeding Symptoms", "required": True, "options": ["Petechiae / purpura", "Epistaxis / gum bleeding", "Easy bruising", "Menorrhagia", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Active bleeding + low platelets = EMERGENCY. Same-day haematology assessment.", "red_flag_negative": "", "output_phrase": "Bleeding: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "ltp_drugs", "type": "multi_select", "label": "Drugs Causing Thrombocytopenia", "required": True, "options": ["Alcohol", "Quinine", "Heparin (HIT)", "Valproate", "Sulfonamides", "None"], "output_phrase": "Drugs: {value}"},
                    {"id": "ltp_infection", "type": "toggle", "label": "Recent Viral Infection? (HIV, EBV, CMV, Hepatitis)", "required": True, "output_phrase": "Infection: {value}"},
                    {"id": "ltp_liver", "type": "toggle", "label": "Liver Disease / Cirrhosis? (hypersplenism)", "required": True, "output_phrase": "Liver: {value}"},
                    {"id": "ltp_autoimmune", "type": "toggle", "label": "Autoimmune Disease? (SLE, ITP)", "required": True, "output_phrase": "Autoimmune: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Immune Thrombocytopenia (ITP)", "Drug-Induced (alcohol, heparin, valproate)", "Liver Disease / Hypersplenism", "Viral Infection (HIV, EBV)", "Bone Marrow Disease / Malignancy", "DIC", "TTP / HUS (if anaemia + renal + neuro)"],
                "questions": [
                    {"id": "ltp_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?ITP — refer haematology if platelets <30 or bleeding", "?Drug-induced — stop agent + repeat", "?Liver disease — manage + monitor", "?Bone marrow — urgent haematology referral", "Isolated mild — repeat + observe"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Platelets >50 + no bleeding: Usually safe. Investigate cause. Platelets <50: Discuss with haematology. Platelets <20 or active bleeding: Emergency haematology referral. Stop causative drugs. Check FBC, blood film, LFTs, HIV/Hep C if risk factors. Safety-net: Return if petechiae, bruising, bleeding gums, epistaxis, or melaena.",
                "questions": [
                    {"id": "ltp_action", "type": "single_select", "label": "Action", "required": True, "options": ["Reassure + repeat (mild, asymptomatic)", "Investigate + stop causative drug", "Urgent haematology referral (<50 or bleeding)", "Emergency haematology (<20 or active bleeding)"], "output_phrase": "Action: {value}"},
                    {"id": "ltp_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ltp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat FBC in 1 week. Haematology referral if persistent.", "output_phrase": "Follow-up: {value}"}
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
    seed_thrombocytopenia()