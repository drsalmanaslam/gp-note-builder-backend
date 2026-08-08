from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_prolactin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Prolactin",
        "description": "Assessment of hyperprolactinaemia. Covers physiological, pharmacological, and pathological causes including prolactinoma.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Level",
                "section_type": "history",
                "questions": [
                    {"id": "prl_level", "type": "text", "label": "Prolactin Level (mIU/L)", "required": True, "placeholder": "e.g., 1200", "is_red_flag": True, "red_flag_positive": "RED FLAG: Prolactin >5000 = ?prolactinoma. Urgent endocrinology referral + MRI pituitary.", "red_flag_negative": "", "output_phrase": "Prolactin: {value} mIU/L"},
                    {"id": "prl_stress", "type": "toggle", "label": "Stressed / Recent Exercise / Venepuncture Difficult? (can transiently raise)", "required": True, "output_phrase": "Stress: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "prl_drugs", "type": "multi_select", "label": "Drugs Raising Prolactin", "required": True, "options": ["Antipsychotics (risperidone, haloperidol)", "Metoclopramide / Domperidone", "SSRIs", "Opiates", "Oestrogens / OCP", "None"], "output_phrase": "Drugs: {value}"},
                    {"id": "prl_pregnancy", "type": "toggle", "label": "Pregnant / Breastfeeding?", "required": True, "output_phrase": "Pregnant/BF: {value}"},
                    {"id": "prl_hypothyroid", "type": "toggle", "label": "Hypothyroidism? (check TSH)", "required": True, "output_phrase": "Hypothyroid: {value}"},
                    {"id": "prl_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Galactorrhoea", "Amenorrhoea / oligomenorrhoea", "Infertility", "Reduced libido", "Headaches / visual disturbance (?macroadenoma)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Headaches + visual disturbance + raised prolactin = ?pituitary macroadenoma. Urgent MRI + endocrinology.", "red_flag_negative": "", "output_phrase": "Symptoms: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Physiological — stress, pregnancy, breastfeeding", "Drug-Induced", "Hypothyroidism", "Prolactinoma (micro <10mm, macro >10mm)", "Pituitary Stalk Compression", "Idiopathic"],
                "questions": [
                    {"id": "prl_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Drug-induced — review medications", "?Hypothyroidism — check TSH + treat", "?Prolactinoma — MRI pituitary + endocrinology", "Physiological — repeat in relaxed state", "Idiopathic — observe"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Check TSH, pregnancy test, U&E. If drug-induced: Consider switching medication. Do not stop antipsychotics without psychiatry consultation. If prolactin >5000 or neurological symptoms: Urgent MRI pituitary + endocrinology referral. If mildly raised + asymptomatic: Repeat in 2-3 weeks (relaxed, fasting). Safety-net: Return if headaches, vision changes, galactorrhoea, or menstrual changes.",
                "questions": [
                    {"id": "prl_action", "type": "single_select", "label": "Action", "required": True, "options": ["Review medications + repeat", "Check TSH + treat hypothyroidism", "MRI pituitary + endocrinology referral", "Reassure + repeat (mild elevation)", "Pregnancy test"], "output_phrase": "Action: {value}"},
                    {"id": "prl_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "prl_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat prolactin in 3 weeks. Endocrine referral if persistent.", "output_phrase": "Follow-up: {value}"}
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
    seed_raised_prolactin()