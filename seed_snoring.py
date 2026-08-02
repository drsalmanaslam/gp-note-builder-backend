from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_snoring():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Snoring",
        "description": "Focused assessment for snoring covering OSA screening (witnessed apnoeas, daytime sleepiness), lifestyle management, and sleep study referral criteria.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "snor_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Loud snoring every night, reported by partner"},
                    {"id": "snor_frequency", "type": "single_select", "label": "Frequency (Nights Per Week)", "required": True, "options": ["1-2 nights", "3-4 nights", "5-6 nights", "Every night"]},
                    {"id": "snor_reported_by", "type": "single_select", "label": "Reported By", "required": True, "options": ["Patient", "Partner / witness", "Both"]},
                    {"id": "snor_sleep_disturbance", "type": "toggle", "label": "Sleep Disturbance? (Own or partner's)", "required": True},
                    {"id": "snor_apnoeas", "type": "toggle", "label": "Witnessed Apnoeas? (OSA Screen)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Witnessed apnoeas = ?OSA. Epworth Sleepiness Scale + consider sleep study referral.", "red_flag_negative": ""},
                    {"id": "snor_daytime_sleepiness", "type": "toggle", "label": "Excessive Daytime Sleepiness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Daytime sleepiness + snoring = ?OSA. Sleep study referral indicated.", "red_flag_negative": ""},
                    {"id": "snor_irritability", "type": "toggle", "label": "Irritability / Poor Concentration?", "required": False},
                    {"id": "snor_alcohol", "type": "single_select", "label": "Alcohol Use (OSA Risk Factor)", "required": True, "options": ["None", "Within limits", "Excess / Evening drinking"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "snor_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 32"},
                    {"id": "snor_neck", "type": "number", "label": "Collar / Neck Circumference (inches)", "required": False, "placeholder": "e.g., 17.5 (>17 = OSA Risk Factor)"},
                    {"id": "snor_ent_pharynx", "type": "single_select", "label": "Pharynx", "required": False, "options": ["Normal", "Abnormal"]},
                    {"id": "snor_tonsils", "type": "single_select", "label": "Tonsillar Enlargement?", "required": False, "options": ["Present", "Absent"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Simple Snoring (No OSA Features)",
                    "Obstructive Sleep Apnoea (OSA) - RED FLAG",
                    "Hypothyroidism (Contributing Factor)",
                    "Nasal Obstruction (Septal Deviation, Polyps, Rhinitis)",
                    "Obesity-Related",
                    "Alcohol / Sedative-Related"
                ],
                "questions": [
                    {"id": "snor_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Simple Snoring - Unlikely OSA", "Suspected OSA - Sleep Study Referral Indicated", "Snoring + Nasal Obstruction", "Snoring + Obesity / Lifestyle Factors"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: daytime sleepiness worsens, partner witnesses apnoeas, or symptoms impact daily functioning. Snoring occurs when airflow causes vibration of soft tissues - obstruction can occur anywhere from nose to base of tongue. Lifestyle: weight loss (most effective), regular exercise, smoking cessation, reduce/stop alcohol (especially evening), sleep on side rather than back (tennis ball technique or positional pillow). TFTs to exclude hypothyroidism. If OSA suspected (witnessed apnoeas + daytime sleepiness): Epworth Sleepiness Scale + refer for sleep studies (respiratory/ENT). If simple snoring without OSA features: reassurance + lifestyle management.",
                "questions": [
                    {"id": "snor_explanation", "type": "toggle", "label": "Explained Airway Obstruction Mechanism? (Nose to Tongue Base)", "required": False},
                    {"id": "snor_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Weight loss", "Regular exercise", "Smoking cessation", "Reduce / stop alcohol (especially evening)", "Sleep on side rather than back"]},
                    {"id": "snor_tfts", "type": "toggle", "label": "TFTs Ordered? (Exclude Hypothyroidism)", "required": False},
                    {"id": "snor_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "Sleep Study (Respiratory / ENT)", "ENT (Nasal Obstruction)"]},
                    {"id": "snor_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review after lifestyle trial, sleep study referral if OSA suspected"}
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
    seed_snoring()