from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_triglycerides():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Triglycerides",
        "description": "Assessment of hypertriglyceridaemia. Covers primary and secondary causes, pancreatitis risk, and management from lifestyle to fibrates.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Level",
                "section_type": "history",
                "questions": [
                    {"id": "tg_level", "type": "text", "label": "Triglyceride Level (mmol/L)", "required": True, "placeholder": "e.g., 8.5", "is_red_flag": True, "red_flag_positive": "RED FLAG: TG >10 mmol/L = risk of acute pancreatitis. Urgent lipid clinic referral + fibrate.", "red_flag_negative": "", "output_phrase": "TG: {value} mmol/L"},
                    {"id": "tg_fasting", "type": "toggle", "label": "Fasting Sample? (non-fasting gives higher readings)", "required": True, "output_phrase": "Fasting: {value}"}
                ]
            },
            {
                "title": "Secondary Causes",
                "section_type": "history",
                "questions": [
                    {"id": "tg_diabetes", "type": "toggle", "label": "Diabetes / Poor Glycaemic Control?", "required": True, "output_phrase": "Diabetes: {value}"},
                    {"id": "tg_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Moderate", "Excess"], "output_phrase": "Alcohol: {value}"},
                    {"id": "tg_obesity", "type": "toggle", "label": "Obesity / Metabolic Syndrome?", "required": True, "output_phrase": "Obesity: {value}"},
                    {"id": "tg_hypothyroid", "type": "toggle", "label": "Hypothyroidism?", "required": True, "output_phrase": "Hypothyroid: {value}"},
                    {"id": "tg_drugs", "type": "multi_select", "label": "Contributing Drugs", "required": False, "options": ["Thiazides", "Beta-blockers", "Steroids", "Oestrogens / OCP", "Retinoids", "None"], "output_phrase": "Drugs: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Secondary — diabetes, obesity, alcohol, hypothyroidism", "Familial Hypertriglyceridaemia", "Familial Combined Hyperlipidaemia", "Drug-Induced"],
                "questions": [
                    {"id": "tg_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Secondary — lifestyle + treat cause", "?Familial — family history + lipid clinic", "Mild-moderate — CV risk management", "Severe (>10) — urgent fibrate + lipid clinic"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Lifestyle: Weight loss, exercise, reduce alcohol, low glycaemic index diet. Optimise diabetes control. Check HbA1c, TFTs, LFTs. If TG >10: Urgent fibrate (Fenofibrate 200mg OD) + lipid clinic referral. If CV risk: Statin first-line (Atorvastatin 20mg). If TG remains >4 on statin: Add fibrate. Safety-net: Return if severe abdominal pain (pancreatitis).",
                "questions": [
                    {"id": "tg_action", "type": "single_select", "label": "Action", "required": True, "options": ["Lifestyle + repeat", "Statin (CV risk)", "Fibrate (TG >4-10)", "Urgent fibrate + lipid clinic (TG >10)", "Treat secondary cause"], "output_phrase": "Action: {value}"},
                    {"id": "tg_safety_net", "type": "toggle", "label": "Pancreatitis Risk Discussed?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "tg_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat fasting lipids in 3 months. Lifestyle advice given.", "output_phrase": "Follow-up: {value}"}
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
    seed_raised_triglycerides()