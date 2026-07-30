from app.database import SessionLocal
from app.models import User, Template, Category

def seed_halitosis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Halitosis",
        "description": "Focused assessment for halitosis covering dental, sinus, GORD, and pharyngeal pouch causes with structured lifestyle and hygiene advice.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "hal_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Bad breath for several months, worse in mornings"},
                    {"id": "hal_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 3 months"},
                    {"id": "hal_pattern", "type": "single_select", "label": "Pattern", "required": True, "options": ["Worse in mornings", "Throughout the day", "After eating", "Constant"]},
                    {"id": "hal_improved_mouthwash", "type": "toggle", "label": "Improved by Mouthwash?", "required": False},
                    {"id": "hal_brushing", "type": "toggle", "label": "Brushing Teeth Twice Daily?", "required": True},
                    {"id": "hal_flossing", "type": "toggle", "label": "Flossing Daily?", "required": True},
                    {"id": "hal_bleeding_gums", "type": "toggle", "label": "Bleeding Gums After Brushing? (Gingivitis/Periodontitis)", "required": True},
                    {"id": "hal_sinusitis", "type": "multi_select", "label": "Sinusitis Screen", "required": True, "options": ["Sore throat", "Fever", "Lymphadenopathy", "None"]},
                    {"id": "hal_frontal_headache", "type": "toggle", "label": "Frontal Headache Worse on Leaning Forward? (Sinusitis)", "required": False},
                    {"id": "hal_gord", "type": "toggle", "label": "GORD Symptoms? (Heartburn, Reflux)", "required": True},
                    {"id": "hal_neck_bulge", "type": "toggle", "label": "Neck Bulge?", "required": False},
                    {"id": "hal_regurgitation", "type": "toggle", "label": "Regurgitation of Food? (Pharyngeal Pouch)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Regurgitation of undigested food = ?pharyngeal pouch. ENT referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hal_detectable", "type": "toggle", "label": "Halitosis Detectable on Breath?", "required": True},
                    {"id": "hal_ent_pharynx", "type": "single_select", "label": "Pharynx", "required": False, "options": ["Normal", "Abnormal"]},
                    {"id": "hal_ent_tm", "type": "single_select", "label": "Tympanic Membranes", "required": False, "options": ["Normal B/L", "Abnormal"]},
                    {"id": "hal_tonsilloliths", "type": "toggle", "label": "Tonsilloliths Visible? (Tonsil Stones)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Poor Oral Hygiene / Gingivitis / Periodontitis (most common)",
                    "Tonsilloliths (Tonsil Stones)",
                    "Sinusitis / Post-Nasal Drip",
                    "GORD / Acid Reflux",
                    "Pharyngeal Pouch (Zenker's Diverticulum) - RED FLAG",
                    "Dry Mouth (Xerostomia - medications, Sjögren's)",
                    "H. pylori Infection",
                    "Dietary (onions, garlic, coffee, alcohol)"
                ],
                "questions": [
                    {"id": "hal_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Halitosis - Oral Hygiene Related", "Halitosis - ?Tonsilloliths", "Halitosis - ?Sinusitis", "Halitosis - ?GORD", "Halitosis - ?Pharyngeal Pouch (Refer ENT)", "No Red Flags Identified"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return in 2 weeks if no improvement with lifestyle and hygiene measures. Halitosis is most commonly caused by oral hygiene issues (gingivitis, periodontitis, tongue coating). Avoid onions and garlic. Smoking cessation. Brush teeth twice daily. Floss daily. Clean tongue (tongue scraper or brush). Use alcohol-free mouthwash. If sinusitis suspected: treat appropriately. If GORD suspected: trial PPI. If pharyngeal pouch suspected (regurgitation of undigested food): refer ENT. If no improvement despite good oral hygiene: consider dental review, H. pylori testing, or ENT referral.",
                "questions": [
                    {"id": "hal_lifestyle", "type": "multi_select", "label": "Lifestyle & Hygiene Advice", "required": False, "options": ["Avoid onions and garlic", "Smoking cessation", "Brush teeth twice daily", "Floss daily", "Clean tongue (tongue scraper)", "Use alcohol-free mouthwash"]},
                    {"id": "hal_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - routine primary care", "Dental review", "ENT (pharyngeal pouch / persistent)", "Gastroenterology (?GORD / H. pylori)"]},
                    {"id": "hal_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return in 2 weeks if no improvement"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_halitosis()