from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_vitamin_d_deficiency():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Vitamin D Deficiency",
        "description": "Comprehensive vitamin D assessment covering deficiency vs insufficiency, Irish-specific treatment regimens (Altavita, Thorens, Desunin, Dnord), and HSE population guidance.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & Indication",
                "section_type": "history",
                "questions": [
                    {"id": "vitd_level", "type": "number", "label": "Vitamin D Level (nmol/L)", "required": True, "placeholder": "e.g., 18 (<25 Deficient | 25-50 Insufficient | 50-75 Adequate | >75 Optimal)"},
                    {"id": "vitd_category", "type": "single_select", "label": "Category", "required": True, "options": ["Deficient: <25 nmol/L → TREAT", "Insufficient: 25-50 nmol/L → Supplement", "Adequate: 50-75 nmol/L → Maintain", "Optimal: >75 nmol/L → No Action"]},
                    {"id": "vitd_indication", "type": "single_select", "label": "HSE Testing Indication", "required": True, "options": ["Bone Disease / Osteoporosis", "Musculoskeletal Pain", "Malabsorption", "High Risk Screen", "Incidental"]},
                    {"id": "vitd_symptoms", "type": "multi_select", "label": "Symptom Screen", "required": True, "options": ["Asymptomatic", "Bone / Joint Pain", "Muscle Weakness", "Fatigue"]}
                ]
            },
            {
                "title": "Red Flags & Safety Screen",
                "section_type": "history",
                "questions": [
                    {"id": "vitd_hypercalcaemia", "type": "toggle", "label": "Hypercalcaemia Symptoms? (Nausea, Vomiting, Confusion, Thirst/Polyuria)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Hypercalcaemia. Check adjusted calcium before supplementing Vitamin D.", "red_flag_negative": ""},
                    {"id": "vitd_renal", "type": "toggle", "label": "Renal Impairment / CKD?", "required": True},
                    {"id": "vitd_sarcoidosis", "type": "toggle", "label": "Known Sarcoidosis / Granulomatous Disease? (Risk of Hypercalcaemia with Vit D)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sarcoidosis/granulomatous disease = risk of hypercalcaemia with Vitamin D. Seek specialist advice.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Baseline Bloods",
                "section_type": "examination",
                "questions": [
                    {"id": "vitd_calcium", "type": "number", "label": "Adjusted Calcium (mmol/L) - NR: 2.2-2.6", "required": False, "placeholder": "e.g., 2.35"},
                    {"id": "vitd_phosphate", "type": "number", "label": "Phosphate (mmol/L)", "required": False, "placeholder": "e.g., 1.1"},
                    {"id": "vitd_alp", "type": "number", "label": "ALP (U/L)", "required": False, "placeholder": "e.g., 85"},
                    {"id": "vitd_egfr", "type": "number", "label": "eGFR (mL/min/1.73m²)", "required": False, "placeholder": "e.g., 72"},
                    {"id": "vitd_exam", "type": "single_select", "label": "Targeted Examination", "required": False, "options": ["Proximal Muscle Strength: Normal", "Proximal Muscle Strength: Reduced", "Bony Tenderness: None", "Bony Tenderness: Present"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Vitamin D Deficiency (Dietary / Lack of Sun Exposure - Most Common)",
                    "Vitamin D Insufficiency (Winter / High-Risk Groups)",
                    "Malabsorption (Coeliac, IBD, Gastric Bypass)",
                    "Primary Hyperparathyroidism (Raised Ca, Low PO4, Raised PTH)",
                    "Osteomalacia (Bone Pain, Muscle Weakness, Low Vit D, Raised ALP)",
                    "Renal Impairment (Reduced 1-Alpha Hydroxylation)"
                ],
                "questions": [
                    {"id": "vitd_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Vitamin D Deficiency (<25 nmol/L) - Treat", "Vitamin D Insufficiency (25-50 nmol/L) - Supplement", "Vitamin D Adequate - No Action", "?Malabsorption - Investigate Further"]}
                ]
            },
            {
                "title": "Management Plan - Deficiency (<25 nmol/L)",
                "section_type": "plan",
                "safety_netting": "Repeat serum adjusted Calcium + Vitamin D in 3-6 months to ensure normalization and exclude hypercalcaemia. Report symptoms of hypercalcaemia: nausea, vomiting, confusion, severe thirst/polyuria. Dietary advice: vitamin D-rich foods (oily fish, eggs, red meat, fortified foods) and safe sun exposure (15-30 min/day on arms/face, avoid burning). Altavita D3 is GMS reimbursable. Children (5-11y): 400 IU (10mcg) daily Oct-Mar (fair-skinned) or year-round (dark-skinned). Teens & Adults (12-65y) + Pregnancy: 600 IU (15mcg) daily Oct-Mar (fair-skinned) or year-round (dark-skinned/pregnant).",
                "questions": [
                    {"id": "vitd_preparation", "type": "single_select", "label": "Treatment Regimen (Deficiency <25 nmol/L)", "required": False, "options": ["Altavita D3: 50,000 IU/Week (2 Caps) x6-8 Weeks → 25,000 IU Twice Monthly Maintenance (GMS)", "Thorens 25,000 IU: 2 Bottles/Week x4 Weeks → 1 Bottle Monthly Maintenance", "Desunin 4,000 IU Tablets: 4,000 IU Daily x10 Weeks → 800 IU Daily Maintenance", "Dnord 255mcg Capsule: 1 Capsule Once Monthly", "Not Indicated (Level >25)"]},
                    {"id": "vitd_otc", "type": "single_select", "label": "OTC Maintenance / Prophylaxis (Insufficient 25-50 or Winter)", "required": False, "options": ["Children 5-11y: 400 IU (10mcg) Daily", "Teens/Adults 12-65y: 600 IU (15mcg) Daily", "Pregnancy: 600 IU (15mcg) Daily", "Not indicated"]},
                    {"id": "vitd_dietary", "type": "toggle", "label": "Dietary + Safe Sun Exposure Advised?", "required": False},
                    {"id": "vitd_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat Ca + Vit D in 3-6 months, annual if high risk"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_vitamin_d_deficiency()