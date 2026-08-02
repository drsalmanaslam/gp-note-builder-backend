from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_steroid_hyperglycaemia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "Steroid-Induced Hyperglycaemia (Known Diabetes)",
        "description": "Management template for steroid-induced hyperglycaemia in patients with known diabetes covering treatment escalation pathways based on current regimen.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Presentation & Current Treatment",
                "section_type": "history",
                "questions": [
                    {"id": "sih_diabetes_type", "type": "single_select", "label": "Known Diabetes Type", "required": True, "options": ["Type 2 Diabetes", "Type 1 Diabetes (mandatory community diabetes team)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: T1DM = community diabetes team involvement MANDATORY. Titrate insulin ≥2 units every 24-48h.", "red_flag_negative": ""},
                    {"id": "sih_steroid", "type": "text", "label": "Current Steroid Therapy (Drug, Dose, Frequency)", "required": True, "placeholder": "e.g., Prednisolone 40mg OD"},
                    {"id": "sih_current_treatment", "type": "multi_select", "label": "Current Diabetes Treatment (Determines Pathway)", "required": True, "options": ["Diet alone", "Metformin", "Gliflozin (SGLT2i)", "Gliptin (DPP-4i)", "Glutide (GLP-1)", "Sulfonylurea (Gliclazide)", "Once-daily night insulin", "Multiple daily insulin doses", "Type 1 - insulin dependent"]},
                    {"id": "sih_hypo_symptoms", "type": "toggle", "label": "Hypoglycaemia Symptoms?", "required": True}
                ]
            },
            {
                "title": "CBG Monitoring",
                "section_type": "assessment",
                "questions": [
                    {"id": "sih_cbg_trend", "type": "single_select", "label": "CBG Trend (Monitor once daily - pre/post-lunch or evening meal)", "required": True, "options": ["Consistently <10 mmol/L → Consider stopping monitoring", ">12 mmol/L → Increase to QDS monitoring", "Consistently >12 mmol/L (≥2 occasions in 24h) → ESCALATE TREATMENT"], "is_red_flag": True, "red_flag_positive": "RED FLAG: CBG >12 on ≥2 occasions in 24h = escalate treatment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Treatment Pathway Selection",
                "section_type": "plan",
                "questions": [
                    {"id": "sih_pathway", "type": "single_select", "label": "Select Applicable Pathway", "required": True, "options": ["Pathway 1: Not on SU/insulin, no hypo symptoms → Titrate Gliclazide to max 240mg mane", "Pathway 2: Already on max morning SU → Add evening SU (max total 320mg) or morning NPH insulin", "Pathway 3: On once-daily night insulin → Switch to morning dosing + titrate ± add Gliclazide", "Pathway 4: Multiple daily insulin doses → Involve community diabetes team", "Pathway 5: Type 1 Diabetes → Titrate insulin + mandatory community diabetes team"]},
                    {"id": "sih_gliclazide_dose", "type": "single_select", "label": "Gliclazide Dose (Pathway 1 or 2)", "required": False, "options": ["Start 40mg mane", "Titrate to 80mg mane", "Titrate to 160mg mane", "Max 240mg mane reached", "Add evening SU (max total 320mg: 240mg mane + 80mg evening)", "Not applicable"]},
                    {"id": "sih_insulin_action", "type": "single_select", "label": "Insulin Adjustment (Pathway 3/4/5)", "required": False, "options": ["Switch night insulin to morning dosing", "Titrate in 10-20% increments", "Consider BD dosing or basal-bolus", "Titrate ≥2 units every 24-48h (T1DM)", "Involve community diabetes team", "Not applicable"]}
                ]
            },
            {
                "title": "Steroid Dose Changes",
                "section_type": "plan",
                "questions": [
                    {"id": "sih_steroid_change", "type": "single_select", "label": "Steroid Dose Status", "required": False, "options": ["Unchanged", "Reduced", "Discontinued"]},
                    {"id": "sih_treatment_adjustment", "type": "single_select", "label": "Glucose-Lowering Adjustment", "required": False, "options": ["Dose reduction required (steroid reduced/discontinued)", "No change - steroid dose unchanged", "Not applicable"]}
                ]
            },
            {
                "title": "Plan Summary",
                "section_type": "plan",
                "safety_netting": "Steroid-induced hyperglycaemia in known diabetes is almost inevitable - anticipate and monitor. CBG >12 on ≥2 occasions in 24h = escalate treatment. Gliclazide max: 240mg mane or 320mg total daily (240mg mane + 80mg evening). When steroids are reduced/discontinued: reduce glucose-lowering treatment accordingly to avoid hypoglycaemia. T1DM: community diabetes team involvement is MANDATORY. Titrate insulin ≥2 units every 24-48h. If on multiple daily insulin doses or not at target: involve community diabetes team.",
                "questions": [
                    {"id": "sih_actions", "type": "multi_select", "label": "Actions Today", "required": True, "options": ["Gliclazide started/titrated", "Evening SU dose added", "Morning NPH insulin added", "Insulin switched to morning dosing", "Insulin dose titrated", "Community diabetes team referral made", "CBG monitoring frequency adjusted", "Continue current management"]},
                    {"id": "sih_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 1 week, in line with steroid course, or community diabetes team follow-up"}
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
    seed_steroid_hyperglycaemia()