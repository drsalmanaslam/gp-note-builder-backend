from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_tsh_eltroxin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Endocrinology").first()
    if not category: category = Category(name="Endocrinology"); db.add(category); db.commit()

    t = {
        "title": "TSH Levels on Eltroxin - Dose Adjustment",
        "description": "Focused assessment for interpreting TSH levels in patients on levothyroxine with evidence-based dose adjustment decisions and malabsorption screening.",
        "category": "Endocrinology",
        "content": {"sections": [
            {
                "title": "Patient Details & Current Dose",
                "section_type": "history",
                "questions": [
                    {"id": "tsh_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 62"},
                    {"id": "tsh_biotin", "type": "single_select", "label": "Taking Biotin? (Multivitamins / Hair Supplements)", "required": True, "options": ["Yes - currently taking biotin", "No - not taking biotin"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Biotin interferes with TFT immunoassay = falsely low TSH + falsely high T4/T3. Stop biotin 3-5 days before repeat testing.", "red_flag_negative": ""},
                    {"id": "tsh_current_dose", "type": "number", "label": "Current Eltroxin (Levothyroxine) Dose (mcg)", "required": True, "placeholder": "e.g., 100"}
                ]
            },
            {
                "title": "TSH Result",
                "section_type": "assessment",
                "questions": [
                    {"id": "tsh_level", "type": "number", "label": "Current TSH Level (mU/L)", "required": True, "placeholder": "e.g., 0.05 (Target: 0.4-2.5)"},
                    {"id": "tsh_category", "type": "single_select", "label": "TSH Result Category", "required": True, "options": ["<0.1 mU/L - AVOID (overtreatment)", "0.1-0.4 mU/L - Low (tolerated in young)", "0.4-2.5 mU/L - TARGET RANGE", "Upper half of reference range - Acceptable if asymptomatic", "Persistently high despite treatment - ?Malabsorption"]}
                ]
            },
            {
                "title": "Dose Adjustment Decision",
                "section_type": "assessment",
                "questions": [
                    {"id": "tsh_action_in_range", "type": "single_select", "label": "TSH 0.4-2.5 (Target Range)", "required": False, "options": ["No dose adjustment needed", "Patient asymptomatic + TSH upper half = No change", "Not applicable"]},
                    {"id": "tsh_action_01_04", "type": "single_select", "label": "TSH 0.1-0.4 (Low)", "required": False, "options": ["Tolerated - young patient needs higher dose for symptom control", "Consider dose reduction", "Not applicable"]},
                    {"id": "tsh_action_under_01", "type": "single_select", "label": "TSH <0.1 (Very Low / Overtreated)", "required": False, "options": ["Dose reduction indicated - AVOID this range", "Not applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: TSH <0.1 = overtreatment. Increased osteoporosis + AF risk. Reduce dose.", "red_flag_negative": ""},
                    {"id": "tsh_action_over60_low", "type": "single_select", "label": "Low TSH + Age >60 Years", "required": False, "options": ["Small dose reduction - 25mcg daily or alternate days", "Not applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Low TSH in >60s = 3-fold increased AF risk + osteoporosis. Prompt 25mcg reduction.", "red_flag_negative": ""},
                    {"id": "tsh_action_persistently_high", "type": "single_select", "label": "TSH Persistently High Despite Treatment", "required": False, "options": ["Investigate for coeliac disease (IgA TTG)", "Investigate for autoimmune gastritis", "Check compliance / absorption (take on empty stomach, avoid calcium/iron within 4h)", "Not applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Persistently high TSH = ?malabsorption (coeliac, autoimmune gastritis) or non-compliance.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Target TSH on Eltroxin: 0.4-2.5 mU/L. No dose change needed if asymptomatic with TSH in upper half of reference range. TSH <0.1 = AVOID (increased osteoporosis + AF risk). TSH 0.1-0.4 = tolerated in younger patients requiring higher dose for symptom control. Low TSH in >60 years = prompt 25mcg reduction (3-fold AF risk). Persistently high TSH despite adequate dosing = check for coeliac disease (IgA TTG), autoimmune gastritis, or malabsorption. Biotin supplements interfere with TFT immunoassay - stop 3-5 days before testing. Take Eltroxin on empty stomach, 30-60 min before food, and separate from calcium/iron by at least 4 hours.",
                "questions": [
                    {"id": "tsh_action_taken", "type": "multi_select", "label": "Action Taken", "required": True, "options": ["No change to dose", "Dose increased", "Dose reduced", "Investigate for malabsorption (coeliac screen)", "Stop biotin + repeat TFTs", "Compliance counselling"]},
                    {"id": "tsh_new_dose", "type": "text", "label": "New Dose (if adjusted)", "required": False, "placeholder": "e.g., 75mcg daily / 100mcg alternate days"},
                    {"id": "tsh_repeat_tft", "type": "single_select", "label": "Repeat TFT Interval", "required": True, "options": ["6 weeks", "8 weeks", "3 months", "6 months", "No repeat needed - stable"]},
                    {"id": "tsh_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat TFTs in 6 weeks after dose change, annual once stable"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_tsh_eltroxin()