from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_abnormal_tfts():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Abnormal TFTs — General Approach",
        "description": "Systematic approach to abnormal thyroid function tests. Covers subclinical/overt hypothyroidism and hyperthyroidism, sick euthyroid, and when to refer.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "TFT Results",
                "section_type": "history",
                "questions": [
                    {"id": "tft_tsh", "type": "text", "label": "TSH (mIU/L)", "required": True, "placeholder": "e.g., 8.5", "output_phrase": "TSH: {value}"},
                    {"id": "tft_ft4", "type": "text", "label": "Free T4 (pmol/L)", "required": False, "placeholder": "e.g., 10", "output_phrase": "FT4: {value}"},
                    {"id": "tft_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["TSH raised + FT4 low (overt hypothyroid)", "TSH raised + FT4 normal (subclinical hypothyroid)", "TSH low + FT4 raised (overt hyperthyroid)", "TSH low + FT4 normal (subclinical hyperthyroid)", "TSH low + FT4 low (sick euthyroid / pituitary)"], "output_phrase": "Pattern: {value}"}
                ]
            },
            {
                "title": "Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "tft_hypo_symptoms", "type": "multi_select", "label": "Hypothyroid Symptoms", "required": False, "options": ["Fatigue", "Weight gain", "Cold intolerance", "Constipation", "Dry skin / hair loss", "Bradycardia", "None"], "output_phrase": "Hypo Sx: {value}"},
                    {"id": "tft_hyper_symptoms", "type": "multi_select", "label": "Hyperthyroid Symptoms", "required": False, "options": ["Palpitations / tachycardia", "Weight loss", "Heat intolerance / sweating", "Tremor", "Diarrhoea", "Anxiety / irritability", "None"], "output_phrase": "Hyper Sx: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Primary Hypothyroidism (Hashimoto's)", "Subclinical Hypothyroidism", "Graves' Disease", "Subclinical Hyperthyroidism", "Sick Euthyroid Syndrome", "Central Hypothyroidism (pituitary)", "Drug-Induced (Amiodarone, Lithium)"],
                "questions": [
                    {"id": "tft_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Overt Hypothyroid — start Levothyroxine", "Subclinical Hypothyroid — repeat + monitor", "Overt Hyperthyroid — refer endocrinology", "Subclinical Hyperthyroid — repeat + monitor", "Sick euthyroid — treat underlying illness"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Overt hypothyroid (TSH >10 + FT4 low): Levothyroxine 50-100mcg OD. Repeat TFTs in 6-8 weeks. Subclinical (TSH 4-10, FT4 normal): Repeat in 3 months. Treat if symptomatic, pregnant, or goitre. Overt hyperthyroid: Urgent endocrinology referral. Start Propranolol for symptoms. Subclinical hyperthyroid (TSH <0.4, FT4 normal): Repeat in 2-3 months. Refer if persistent. Sick euthyroid: Treat underlying illness. Repeat TFTs when well. Safety-net: Return if palpitations, chest pain, or severe symptoms.",
                "questions": [
                    {"id": "tft_action", "type": "single_select", "label": "Action", "required": True, "options": ["Start Levothyroxine + repeat TFTs", "Repeat TFTs + monitor (subclinical)", "Refer endocrinology (hyperthyroid)", "Treat underlying illness + repeat (sick euthyroid)", "Reassure (normal)"], "output_phrase": "Action: {value}"},
                    {"id": "tft_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "tft_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Start Levothyroxine 50mcg. Repeat TFTs in 8 weeks.", "output_phrase": "Follow-up: {value}"}
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
    seed_abnormal_tfts()