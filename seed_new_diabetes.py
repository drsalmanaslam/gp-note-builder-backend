from app.database import SessionLocal
from app.models import User, Template, Category

def seed_new_diabetes():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "New Type 2 Diabetes Diagnosis",
        "description": "Comprehensive template for newly diagnosed Type 2 diabetes covering diagnostic confirmation, metformin initiation, cardiovascular risk management, vaccinations, screening setup, and lifestyle advice.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Diagnostic Confirmation",
                "section_type": "history",
                "questions": [
                    {"id": "dm2_diagnosis_method", "type": "single_select", "label": "Diagnostic Confirmation (2 abnormal results on separate occasions)", "required": True, "options": ["Confirmed on two occasions - HbA1c ≥48", "Confirmed on two occasions - Fasting glucose ≥7", "Confirmed on two occasions - OGTT ≥11.1", "Confirmed on two occasions - Random glucose ≥11.1", "Confirmed via mixed criteria"]},
                    {"id": "dm2_hba1c", "type": "number", "label": "HbA1c (mmol/mol)", "required": True, "placeholder": "e.g., 62 (Pre-DM: 39-47, DM: ≥48)"},
                    {"id": "dm2_initial_preference", "type": "single_select", "label": "Initial Management Preference", "required": True, "options": ["Trial of lifestyle modification first (if HbA1c 48-58)", "Start metformin today", "Patient undecided"]},
                    {"id": "dm2_ed", "type": "toggle", "label": "Erectile Dysfunction? (Male patients)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "dm2_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 128/78"},
                    {"id": "dm2_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 31"}
                ]
            },
            {
                "title": "Metformin Initiation",
                "section_type": "plan",
                "questions": [
                    {"id": "dm2_metformin_titration", "type": "multi_select", "label": "Titration Schedule (Target: 1g BD over 4-6 weeks)", "required": False, "options": ["Week 1: 500mg once daily, post-meal", "Week 2: 500mg twice daily", "Week 3: 1000mg morning + 500mg evening", "Week 4 onward: 1000mg twice daily", "Not starting metformin yet"]},
                    {"id": "dm2_gi_counselling", "type": "toggle", "label": "GI Side Effects Counselled? (Especially at start)", "required": False},
                    {"id": "dm2_escalation_trigger", "type": "single_select", "label": "Dose Escalation Trigger", "required": False, "options": ["HbA1c ≥58 on metformin → Add second agent", "Target 64 (elderly/comorbidities)", "Target 69 (frail/nursing home)", "Not applicable"]}
                ]
            },
            {
                "title": "Cardiovascular Risk Management",
                "section_type": "plan",
                "questions": [
                    {"id": "dm2_bp_management", "type": "single_select", "label": "Blood Pressure (Treat if ≥140/80)", "required": True, "options": ["Ramipril 5mg OD", "Losartan 100mg OD (if ACEi CI)", "Not indicated - BP within target"]},
                    {"id": "dm2_statin", "type": "single_select", "label": "Statin (Indicated >45 years)", "required": True, "options": ["Atorvastatin 40mg OD", "Atorvastatin 20mg OD", "Not indicated (age <45)", "Contraindicated / declined"]},
                    {"id": "dm2_aspirin", "type": "single_select", "label": "Aspirin", "required": True, "options": ["Indicated - established CVD (secondary prevention)", "Not indicated - primary prevention only"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Aspirin NOT indicated for primary prevention in diabetes. Only for established CVD.", "red_flag_negative": ""},
                    {"id": "dm2_folic_acid", "type": "single_select", "label": "Folic Acid", "required": False, "options": ["5mg - chance of pregnancy (females)", "Not applicable"]}
                ]
            },
            {
                "title": "Vaccinations",
                "section_type": "plan",
                "questions": [
                    {"id": "dm2_pneumococcal", "type": "single_select", "label": "Pneumococcal Vaccine", "required": True, "options": ["First dose given today", "Second dose due (first given <65y)", "Not yet given - advise", "Fully up to date"]},
                    {"id": "dm2_influenza", "type": "single_select", "label": "Influenza Vaccine", "required": True, "options": ["Given this year", "Due - advise yearly vaccination"]}
                ]
            },
            {
                "title": "Monitoring & Screening Setup",
                "section_type": "plan",
                "questions": [
                    {"id": "dm2_register", "type": "multi_select", "label": "Actions Arranged", "required": True, "options": ["Added to diabetic register", "Retinal screening booked (practice nurse)", "Added to medical history on file"]},
                    {"id": "dm2_6monthly", "type": "multi_select", "label": "6-Monthly Bloods/Monitoring Required", "required": False, "options": ["HbA1c", "U&Es / eGFR", "Fasting Lipids", "Urine ACR"]},
                    {"id": "dm2_complication_counselling", "type": "toggle", "label": "Macrovascular + Microvascular Risk Counselled? (Heart, stroke, kidneys, eyes, feet)", "required": True}
                ]
            },
            {
                "title": "Test Strip Entitlement (PCRS)",
                "section_type": "plan",
                "questions": [
                    {"id": "dm2_strips", "type": "single_select", "label": "Test Strip Entitlement", "required": False, "options": ["Insulin-treated → No limit", "Sulphonylurea/meglitinide → 2 boxes/month (1,200/yr)", "Other oral hypoglycaemic → 1 box/month (600/yr)", "Diet alone → 2 boxes/annum (100/yr)", "Not applicable yet"]}
                ]
            },
            {
                "title": "Lifestyle & Dietary Advice",
                "section_type": "plan",
                "questions": [
                    {"id": "dm2_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Weight loss (5-10% target)", "Smoking cessation", "Regular exercise (150 min/week)"]},
                    {"id": "dm2_diet", "type": "multi_select", "label": "Dietary Advice - High Fibre / Low GI", "required": False, "options": ["Cut out table sugar + fizzy drinks; reduce alcohol + starchy carbs", "Substitute mash/chips/pasta/rice with green vegetables", "Homemade soups - green veg, mushroom, tomato, onion", "Fruits - raspberries, strawberries, blueberries", "Eggs, salmon, tuna, unprocessed meats", "Plain full-fat yoghurt with berries", "Cheese in moderation", "Snacks - almonds/walnuts; >70% dark chocolate"]}
                ]
            },
            {
                "title": "Patient Resources & Follow-Up",
                "section_type": "plan",
                "safety_netting": "LTI (Long-Term Illness) form provided. DISCOVER Diabetes Programme - self-registration advised. Type 2 DM booklet: Living Well with Type 2 Diabetes. Diabetes Ireland: 01 842 8118. Return if: symptoms of hyperglycaemia (thirst, polyuria, weight loss), signs of infection (especially foot), visual disturbance, or any concerns. 3-month nurse review: feet check, BP, cholesterol, BMI, smoking status, HbA1c.",
                "questions": [
                    {"id": "dm2_resources", "type": "multi_select", "label": "Patient Resources & Support", "required": False, "options": ["LTI (Long-Term Illness) form provided", "DISCOVER Diabetes Programme - self-registration advised", "Type 2 DM booklet given - Living Well with Type 2 Diabetes", "Advised to contact Diabetes Ireland - 01 842 8118"]},
                    {"id": "dm2_followup", "type": "text", "label": "Next Review", "required": True, "placeholder": "e.g., 3 months - Nurse review (feet, BP, cholesterol, BMI, HbA1c)"}
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
    seed_new_diabetes()