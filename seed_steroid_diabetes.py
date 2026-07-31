from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_steroid_diabetes():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "Steroid-Induced Diabetes Management",
        "description": "Focused template for managing steroid-induced hyperglycaemia covering CBG monitoring, Gliclazide initiation/titration, and dose adjustment with steroid tapering.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Presentation & Risk",
                "section_type": "history",
                "questions": [
                    {"id": "sid_presentation", "type": "single_select", "label": "Presentation", "required": True, "options": ["New onset hyperglycaemia on regular oral steroids", "Pre-existing diabetes (not this pathway)"]},
                    {"id": "sid_steroid", "type": "text", "label": "Current Steroid Therapy (Drug, Dose, Frequency)", "required": True, "placeholder": "e.g., Prednisolone 30mg OD"},
                    {"id": "sid_risk", "type": "single_select", "label": "Risk Stratification", "required": True, "options": ["High risk - daily CBG monitoring indicated", "Standard risk"]}
                ]
            },
            {
                "title": "CBG Monitoring",
                "section_type": "assessment",
                "questions": [
                    {"id": "sid_monitoring_frequency", "type": "single_select", "label": "Current Monitoring Frequency", "required": True, "options": ["Daily (high risk)", "QDS (4x daily)", "Reduced / stopped"]},
                    {"id": "sid_cbg_trend", "type": "single_select", "label": "CBG Trend", "required": True, "options": ["Consistently <10 mmol/L → Consider stopping monitoring", ">12 mmol/L → Increase to QDS monitoring", "Consistently >12 mmol/L (≥2 occasions in 24h) → START TREATMENT"], "is_red_flag": True, "red_flag_positive": "RED FLAG: CBG >12 on ≥2 occasions in 24h = treatment threshold met. Start Gliclazide.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Treatment Initiation & Titration",
                "section_type": "plan",
                "questions": [
                    {"id": "sid_treatment_threshold", "type": "toggle", "label": "Treatment Threshold Met? (CBG >12 on ≥2 occasions in 24h)", "required": True},
                    {"id": "sid_treatment", "type": "single_select", "label": "Treatment of Choice", "required": False, "options": ["Gliclazide 40mg mane", "Gliclazide 80mg mane", "Gliclazide 160mg mane", "Gliclazide 240mg mane (max dose)", "Not started yet - continue monitoring"]},
                    {"id": "sid_titration", "type": "single_select", "label": "Titration Status", "required": False, "options": ["Started at initial dose", "Titrating up", "Maximum dose reached - 240mg mane", "Not applicable"]},
                    {"id": "sid_referral_trigger", "type": "single_select", "label": "Specialist Referral", "required": False, "options": ["No improvement on 160mg Gliclazide → SEEK SPECIALIST HELP", "Adequate control on current dose - no referral", "Not applicable"]}
                ]
            },
            {
                "title": "Steroid Dose Changes & Gliclazide Adjustment",
                "section_type": "plan",
                "questions": [
                    {"id": "sid_steroid_change", "type": "single_select", "label": "Steroid Dose Status", "required": False, "options": ["Unchanged", "Reduced", "Discontinued"]},
                    {"id": "sid_gliclazide_adjustment", "type": "single_select", "label": "Gliclazide Dose Adjustment", "required": False, "options": ["Consider dose reduction (steroid reduced/discontinued)", "No change - continue current dose", "Not applicable"]},
                    {"id": "sid_continued_monitoring", "type": "single_select", "label": "Continued Monitoring", "required": False, "options": ["Continue CBG if >12 mmol/L", "CBG can be relaxed - consistently <10", "Not applicable"]}
                ]
            },
            {
                "title": "Plan Summary",
                "section_type": "plan",
                "safety_netting": "Gliclazide works by stimulating insulin secretion - risk of hypoglycaemia especially if steroid dose is reduced without adjusting Gliclazide. Always review Gliclazide dose when steroid dose changes. CBG >12 on ≥2 occasions in 24h = treatment threshold. If no improvement on 160mg Gliclazide: seek specialist help. If CBG consistently <10: consider reducing/stopping monitoring. Steroid-induced diabetes may resolve when steroids are discontinued - ensure CBG monitoring continues during steroid taper.",
                "questions": [
                    {"id": "sid_actions", "type": "multi_select", "label": "Actions Today", "required": True, "options": ["Gliclazide started", "Gliclazide dose increased", "Gliclazide dose reduced", "Specialist referral made", "CBG monitoring frequency adjusted", "Continue current management"]},
                    {"id": "sid_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 1 week, in line with steroid course, or sooner if CBG >12"}
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
    seed_steroid_diabetes()