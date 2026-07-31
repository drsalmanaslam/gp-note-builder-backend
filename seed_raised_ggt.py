from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_ggt():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised GGT",
        "description": "Focused assessment for raised GGT covering alcohol vs cholestasis differentiation, PBC screening, and combined GGT/ALP/MCV interpretation.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & History",
                "section_type": "history",
                "questions": [
                    {"id": "ggt_level", "type": "number", "label": "GGT Level (U/L)", "required": True, "placeholder": "e.g., 125"},
                    {"id": "ggt_alp", "type": "number", "label": "ALP Level (If Available)", "required": False, "placeholder": "e.g., 145"},
                    {"id": "ggt_pbc_screen", "type": "multi_select", "label": "PBC Screen", "required": True, "options": ["Itch / Pruritus", "Nausea", "Vomiting", "None"]},
                    {"id": "ggt_alcohol", "type": "single_select", "label": "Alcohol Use (Most Common Cause)", "required": True, "options": ["None", "Within Limits", "Excess"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol excess = most common cause. Stop alcohol + repeat LFTs.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations & Interpretation",
                "section_type": "assessment",
                "questions": [
                    {"id": "ggt_fbc", "type": "toggle", "label": "FBC Ordered? (Check MCV)", "required": True},
                    {"id": "ggt_mcv_raised", "type": "toggle", "label": "Raised GGT + Raised MCV? → Mainly Due to Alcohol", "required": False},
                    {"id": "ggt_alt_raised", "type": "toggle", "label": "Raised GGT + Raised ALT? → Consider Alcoholic Hepatitis", "required": False},
                    {"id": "ggt_cholestasis", "type": "toggle", "label": "Raised GGT + Raised ALP? → Suggests CHOLESTASIS (Send Fractionated ALP + AMA)", "required": False},
                    {"id": "ggt_pbc_criteria", "type": "toggle", "label": "PBC Confirmed? (ALP + GGT Raised + AMA Positive = 2 of 3 Criteria)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: PBC confirmed. Start Ursofalk. Refer gastroenterology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Most common cause = alcohol. Stop alcohol + repeat LFTs. GGT + MCV raised = alcohol. GGT + ALT raised = alcoholic hepatitis. GGT + ALP raised = cholestasis (send AMA for PBC). PBC: Ursofalk + gastroenterology referral.",
                "questions": [
                    {"id": "ggt_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Alcohol-Related", "?PBC (GGT + ALP Raised)", "?Drug-Induced", "Uncertain"]},
                    {"id": "ggt_alcohol_advice", "type": "toggle", "label": "Stop Alcohol + Repeat LFTs in 4-6 Weeks?", "required": False},
                    {"id": "ggt_urso", "type": "toggle", "label": "Ursofalk Started? (If PBC Confirmed)", "required": False},
                    {"id": "ggt_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "Gastroenterology (?PBC)"]},
                    {"id": "ggt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat LFTs in 4-6 weeks"}
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
    seed_raised_ggt()