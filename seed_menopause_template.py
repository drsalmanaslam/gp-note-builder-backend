from app.database import SessionLocal
from app.models import User, Template, Category

def seed_menopause_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    template_data = {
        "title": "Menopause Review",
        "description": "Comprehensive menopause assessment including symptom review, HRT discussion, and risk assessment.",
        "category": "Women's Health",
        "content": {
            "sections": [
                {
                    "title": "Menstrual & Symptom History",
                    "questions": [
                        {"id": "meno_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 51"},
                        {"id": "meno_lmp", "type": "date", "label": "Date of Last Menstrual Period", "required": False},
                        {"id": "meno_status", "type": "single_select", "label": "Menopausal Status", "required": True, "options": ["Perimenopausal", "Menopausal (<12 months LMP)", "Postmenopausal (>12 months LMP)", "Surgical Menopause", "Premature Ovarian Insufficiency"]},
                        {"id": "meno_hot_flushes", "type": "single_select", "label": "Hot Flushes/Night Sweats", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "meno_sleep", "type": "single_select", "label": "Sleep Disturbance", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "meno_mood", "type": "single_select", "label": "Mood Changes/Anxiety", "required": True, "options": ["None", "Mild", "Moderate", "Severe"]},
                        {"id": "meno_vaginal", "type": "toggle", "label": "Vaginal Dryness/Discomfort?", "required": False},
                        {"id": "meno_libido", "type": "single_select", "label": "Libido Change", "required": False, "options": ["No Change", "Decreased", "Significantly Decreased"]}
                    ]
                },
                {
                    "title": "HRT Assessment & Risk Factors",
                    "red_flag_threshold": 1,
                    "questions": [
                        {"id": "meno_hrt_current", "type": "toggle", "label": "Currently on HRT?", "required": True},
                        {"id": "meno_hrt_type", "type": "textarea", "label": "Current HRT Regime", "required": False, "placeholder": "e.g., Estradiol 2mg, Utrogestan 200mg..."},
                        {"id": "meno_hrt_duration", "type": "duration", "label": "Duration on HRT", "required": False, "units": ["months", "years"]},
                        {"id": "meno_hrt_benefit", "type": "single_select", "label": "Symptom Relief on HRT?", "required": False, "options": ["Good Relief", "Partial Relief", "No Relief"]},
                        {"id": "meno_brca", "type": "toggle", "label": "🔴 Personal/Family History Breast Cancer? (BRCA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Breast cancer history. HRT may be contraindicated. Discuss with oncology before prescribing.", "red_flag_negative": "No breast cancer history."},
                        {"id": "meno_vte", "type": "toggle", "label": "🔴 History of DVT/PE/VTE?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: VTE history. Transdermal HRT preferred. Haematology discussion if indicated.", "red_flag_negative": "No VTE history."},
                        {"id": "meno_bleeding", "type": "toggle", "label": "🔴 Postmenopausal Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postmenopausal bleeding. Urgent 2WW gynaecology referral required.", "red_flag_negative": "No abnormal bleeding."},
                        {"id": "meno_mammogram", "type": "toggle", "label": "Mammogram Up to Date?", "required": True},
                        {"id": "meno_bp", "type": "number", "label": "BP (systolic)", "required": True, "placeholder": "e.g., 130"}
                    ]
                },
                {
                    "title": "Bone Health & Lifestyle",
                    "questions": [
                        {"id": "meno_osteoporosis", "type": "single_select", "label": "Osteoporosis Risk", "required": True, "options": ["Low", "Moderate", "High"]},
                        {"id": "meno_dexa", "type": "toggle", "label": "DEXA Scan Indicated?", "required": False},
                        {"id": "meno_calcium", "type": "toggle", "label": "Calcium/Vitamin D Supplementation?", "required": False},
                        {"id": "meno_exercise", "type": "single_select", "label": "Exercise Level", "required": True, "options": ["Regular Weight-bearing", "Some Activity", "Sedentary"]},
                        {"id": "meno_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never", "Ex-Smoker", "Current"]},
                        {"id": "meno_alcohol", "type": "number", "label": "Alcohol Units/Week", "required": False}
                    ]
                },
                {
                    "title": "Plan & Follow-up",
                    "safety_netting": "If you experience any abnormal vaginal bleeding, breast lumps, or calf pain/swelling, seek urgent medical attention.",
                    "questions": [
                        {"id": "meno_plan", "type": "textarea", "label": "Management Plan", "required": True, "placeholder": "e.g., Continue HRT, lifestyle advice, bone health..."},
                        {"id": "meno_followup", "type": "duration", "label": "Follow-up", "required": True, "units": ["months"]},
                        {"id": "meno_notes", "type": "textarea", "label": "Additional Notes", "required": False}
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
    seed_menopause_template()