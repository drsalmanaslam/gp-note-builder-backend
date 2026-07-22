from app.database import SessionLocal
from app.models import User, Template, Category

def seed_prostate_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    template_data = {
        "title": "Prostate Check",
        "description": "Prostate assessment including LUTS scoring, PSA interpretation, and 2WW referral criteria.",
        "category": "Men's Health",
        "content": {
            "sections": [
                {
                    "title": "Lower Urinary Tract Symptoms (LUTS)",
                    "questions": [
                        {"id": "prost_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 65"},
                        {"id": "prost_frequency", "type": "single_select", "label": "Daytime Urinary Frequency", "required": True, "options": ["Normal (4-6x/day)", "Increased (7-8x/day)", "Very Frequent (>8x/day)"]},
                        {"id": "prost_nocturia", "type": "number", "label": "Nocturia (times per night)", "required": True, "placeholder": "e.g., 2"},
                        {"id": "prost_stream", "type": "single_select", "label": "Urinary Stream", "required": True, "options": ["Normal", "Weak", "Intermittent", "Straining"]},
                        {"id": "prost_urgency", "type": "toggle", "label": "Urgency?", "required": False},
                        {"id": "prost_incomplete", "type": "toggle", "label": "Incomplete Emptying?", "required": False},
                        {"id": "prost_retention", "type": "toggle", "label": "🔴 Acute Retention Episodes?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute urinary retention. Urgent catheterisation and urology assessment.", "red_flag_negative": "No retention episodes."}
                    ]
                },
                {
                    "title": "PSA & Examination",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "prost_psa", "type": "number", "label": "PSA Level (ng/mL)", "required": False, "placeholder": "e.g., 4.5"},
                        {"id": "prost_psa_date", "type": "date", "label": "Date of PSA Test", "required": False},
                        {"id": "prost_dre", "type": "toggle", "label": "DRE Performed?", "required": True},
                        {"id": "prost_dre_findings", "type": "single_select", "label": "DRE Findings", "required": False, "options": ["Normal", "Enlarged - Benign Feeling", "Suspicious - Hard/Irregular"]},
                        {"id": "prost_suspicious", "type": "toggle", "label": "🔴 Suspicious DRE or PSA Above Age-specific Range?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspicious prostate findings. Urgent 2WW urology referral required.", "red_flag_negative": "Prostate examination unremarkable."},
                        {"id": "prost_haematuria", "type": "toggle", "label": "🔴 Haematuria?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haematuria. 2WW urology referral required.", "red_flag_negative": "No haematuria."}
                    ]
                },
                {
                    "title": "Risk Factors & Family History",
                    "questions": [
                        {"id": "prost_family", "type": "toggle", "label": "Family History of Prostate Cancer?", "required": True},
                        {"id": "prost_ethnicity", "type": "single_select", "label": "Ethnicity (Risk Factor)", "required": True, "options": ["White", "Black African/Caribbean (Higher Risk)", "Asian", "Other"]},
                        {"id": "prost_medications", "type": "textarea", "label": "Current Medications", "required": False, "placeholder": "e.g., Tamsulosin 400mcg, Finasteride 5mg..."},
                        {"id": "prost_lifestyle", "type": "textarea", "label": "Lifestyle Advice Given", "required": False, "placeholder": "e.g., Fluid management, caffeine reduction..."}
                    ]
                },
                {
                    "title": "Plan & Follow-up",
                    "safety_netting": "If you develop sudden inability to pass urine, severe pain, or visible blood in urine, seek urgent medical attention.",
                    "questions": [
                        {"id": "prost_plan", "type": "textarea", "label": "Management Plan", "required": True, "placeholder": "e.g., Watchful waiting, alpha-blocker, urology referral..."},
                        {"id": "prost_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["weeks", "months"]},
                        {"id": "prost_notes", "type": "textarea", "label": "Additional Notes", "required": False}
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_prostate_template()