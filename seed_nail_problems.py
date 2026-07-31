from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_nail_problems():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Nail Problems",
        "description": "Focused nail assessment covering fungal infection, psoriasis, trauma, melanoma red flags, and management options.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "nail_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Thickened discoloured toenails for 6 months"},
                    {"id": "nail_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 6 months"},
                    {"id": "nail_site", "type": "single_select", "label": "Which Nails?", "required": True, "options": ["Toenails Only", "Fingernails Only", "Both Fingers + Toes", "Single Nail Only"]},
                    {"id": "nail_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Thickening", "Discolouration (Yellow/Brown)", "Crumbling / Brittle", "Separation from Nail Bed (Onycholysis)", "Pain / Tenderness", "None"]},
                    {"id": "nail_psoriasis", "type": "multi_select", "label": "Psoriasis Features?", "required": True, "options": ["Pitting", "Oil Drop Discolouration", "Subungual Hyperkeratosis", "Known Psoriasis", "None"]},
                    {"id": "nail_trauma", "type": "toggle", "label": "Recent Trauma / Tight Footwear?", "required": False},
                    {"id": "nail_diabetes", "type": "toggle", "label": "Diabetes? (Risk of Onychomycosis + Complications)", "required": True},
                    {"id": "nail_red_flags", "type": "multi_select", "label": "Melanoma Red Flags", "required": True, "options": ["New Pigmented Line in Nail", "Pigmentation Spreading to Nail Fold (Hutchinson's Sign)", "Bleeding / Ulceration", "Single Nail Only + Changing", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Subungual melanoma = Hutchinson's sign, single digit, changing. Urgent 2WW dermatology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "nail_appearance", "type": "multi_select", "label": "Nail Findings", "required": True, "options": ["Thickened / Hypertrophic", "Yellow/Brown Discolouration", "White/Superficial (SOFT)", "Crumbling / Dystrophic", "Pitting (Psoriasis)", "Onycholysis (Lifting)", "Splinter Haemorrhages", "Longitudinal Ridge / Line (Melanonychia)"]},
                    {"id": "nail_hutchinson", "type": "toggle", "label": "Hutchinson's Sign? (Pigment on Nail Fold - RED FLAG Melanoma)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hutchinson's sign = subungual melanoma. Urgent 2WW dermatology.", "red_flag_negative": ""},
                    {"id": "nail_paronychia", "type": "toggle", "label": "Paronychia / Periungual Inflammation?", "required": False},
                    {"id": "nail_foot_check", "type": "toggle", "label": "Diabetic Foot Check? (If Diabetic)", "required": False}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return if: new pigmented line develops, pigment spreads to nail fold (Hutchinson's sign), bleeding/ulceration, or single nail changes rapidly. Fungal (onychomycosis): clinical diagnosis usually sufficient. Nail clippings for fungal culture if diagnostic uncertainty or considering oral treatment. First-line: Amorolfine 5% nail lacquer (Loceryl) weekly for 6-12 months (better for superficial/early disease). Oral Terbinafine 250mg OD for 6-12 weeks (toenails) or 6-8 weeks (fingernails) if topical fails or severe. Check LFTs before + at 4-6 weeks. Cure rate ~50-70%. Psoriasis: treat skin psoriasis + topical vitamin D analogues. Trauma: reassurance + nail care advice. Paronychia: antibiotics (Flucloxacillin) if bacterial, avoid if chronic (candida).",
                "questions": [
                    {"id": "nail_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Onychomycosis (Fungal)", "Nail Psoriasis", "Traumatic Nail Dystrophy", "Paronychia", "Subungual Melanoma - URGENT 2WW", "Longitudinal Melanonychia - Benign"]},
                    {"id": "nail_topical", "type": "toggle", "label": "Amorolfine 5% Nail Lacquer Weekly? (First-Line, 6-12 Months)", "required": False},
                    {"id": "nail_oral", "type": "toggle", "label": "Oral Terbinafine 250mg OD? (If Severe/Topical Failed. Check LFTs Before + at 4-6 Weeks)", "required": False},
                    {"id": "nail_clippings", "type": "toggle", "label": "Nail Clippings for Fungal Culture?", "required": False},
                    {"id": "nail_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None", "Dermatology - Routine (Diagnostic Uncertainty / Severe)", "Dermatology - Urgent 2WW (?Melanoma)", "Podiatry (Diabetic Foot Care)"]},
                    {"id": "nail_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3-6 months if on treatment, sooner if red flags"}
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
    print(f"Template '{t['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_nail_problems()