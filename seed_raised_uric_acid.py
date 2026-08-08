from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_uric_acid():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Uric Acid",
        "description": "Assessment of hyperuricaemia. Covers gout, CKD, metabolic syndrome, and when to initiate urate-lowering therapy.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Level",
                "section_type": "history",
                "questions": [
                    {"id": "ua_level", "type": "text", "label": "Uric Acid Level (umol/L)", "required": True, "placeholder": "e.g., 520", "output_phrase": "Uric acid: {value} umol/L"},
                    {"id": "ua_symptoms", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Acute gout — red, hot, swollen joint", "Chronic tophi", "Renal stones / colic", "Asymptomatic — incidental finding", "None"], "output_phrase": "Symptoms: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "ua_ckd", "type": "toggle", "label": "CKD / Renal Impairment?", "required": True, "output_phrase": "CKD: {value}"},
                    {"id": "ua_diuretics", "type": "toggle", "label": "On Thiazide / Loop Diuretics?", "required": True, "output_phrase": "Diuretics: {value}"},
                    {"id": "ua_metabolic", "type": "multi_select", "label": "Metabolic Features", "required": False, "options": ["Obesity", "Hypertension", "Diabetes", "Dyslipidaemia", "High purine diet (red meat, seafood, alcohol)", "None"], "output_phrase": "Metabolic: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Gout (acute or chronic)", "Asymptomatic Hyperuricaemia", "CKD", "Metabolic Syndrome", "Diuretic-Induced", "Tumour Lysis Syndrome (chemotherapy)", "Lead Toxicity (rare)"],
                "questions": [
                    {"id": "ua_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Acute gout — treat flare", "Recurrent gout — start allopurinol", "Asymptomatic — no treatment needed", "CKD-related — monitor", "Metabolic — lifestyle + CV risk"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Acute gout: NSAIDs or Colchicine or Prednisolone. Do NOT start allopurinol during acute flare. Asymptomatic hyperuricaemia: No treatment needed. Lifestyle: Weight loss, reduce alcohol, reduce purine-rich foods. Recurrent gout (≥2 flares/year) or tophi or CKD: Start Allopurinol 100mg OD, titrate to target <360 (or <300 if tophi). Check U&E before starting. Safety-net: Return if acute joint pain, renal colic, or new tophi.",
                "questions": [
                    {"id": "ua_action", "type": "single_select", "label": "Action", "required": True, "options": ["Treat acute gout (NSAIDs/Colchicine)", "Start Allopurinol (recurrent/chronic)", "Lifestyle advice (asymptomatic)", "Monitor (CKD-related)", "No treatment needed"], "output_phrase": "Action: {value}"},
                    {"id": "ua_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ua_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Start Allopurinol 100mg. Check U&E + uric acid in 4 weeks.", "output_phrase": "Follow-up: {value}"}
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
    seed_raised_uric_acid()