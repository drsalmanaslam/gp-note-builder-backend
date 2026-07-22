from app.database import SessionLocal
from app.models import User, Template, Category

def seed_obesity_template():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return
    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    template_data = {
        "title": "Obesity & Weight Management",
        "description": "Weight management assessment including metabolic risk, lifestyle intervention, and medical/surgical options.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {"title": "Anthropometric Measurements", "questions": [
                {"id": "ob_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 95"},
                {"id": "ob_height", "type": "number", "label": "Height (cm)", "required": True, "placeholder": "e.g., 170"},
                {"id": "ob_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 32.9"},
                {"id": "ob_waist", "type": "number", "label": "Waist Circumference (cm)", "required": False},
                {"id": "ob_class", "type": "single_select", "label": "BMI Classification", "required": True, "options": ["Overweight (25-29.9)", "Obese Class I (30-34.9)", "Obese Class II (35-39.9)", "Obese Class III (≥40)"]}
            ]},
            {"title": "Metabolic Risk Assessment", "red_flag_threshold": 1, "questions": [
                {"id": "ob_bp", "type": "number", "label": "Blood Pressure (Systolic)", "required": True, "placeholder": "e.g., 140"},
                {"id": "ob_hba1c", "type": "number", "label": "HbA1c (mmol/mol)", "required": False},
                {"id": "ob_cholesterol", "type": "number", "label": "Total Cholesterol (mmol/L)", "required": False},
                {"id": "ob_sleep_apnoea", "type": "toggle", "label": "🔴 Symptoms of Sleep Apnoea? (Snoring/Daytime Sleepiness)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Possible obstructive sleep apnoea. Refer for sleep studies. May affect driving - inform DVLA if indicated.", "red_flag_negative": "No sleep apnoea symptoms."},
                {"id": "ob_comorbidities", "type": "multi_select", "label": "Obesity-related Comorbidities", "required": True, "options": ["Type 2 Diabetes", "Hypertension", "Dyslipidaemia", "Osteoarthritis", "NAFLD", "PCOS", "GERD", "Depression", "None"]}
            ]},
            {"title": "Lifestyle Assessment", "questions": [
                {"id": "ob_diet", "type": "textarea", "label": "Typical Daily Diet", "required": True, "placeholder": "e.g., Breakfast: cereal, Lunch: sandwich, Dinner: pasta..."},
                {"id": "ob_meals", "type": "single_select", "label": "Meal Pattern", "required": True, "options": ["3 Regular Meals", "Skipping Meals", "Grazing/Snacking", "Binge Eating Pattern"]},
                {"id": "ob_exercise", "type": "single_select", "label": "Physical Activity", "required": True, "options": ["Regular (≥150 min/week)", "Some Activity", "Sedentary"]},
                {"id": "ob_alcohol", "type": "number", "label": "Alcohol Units/Week", "required": False},
                {"id": "ob_emotional", "type": "toggle", "label": "Emotional Eating/Comfort Eating?", "required": False},
                {"id": "ob_motivation", "type": "single_select", "label": "Motivation to Change", "required": True, "options": ["Ready to Change", "Considering", "Not Ready/Pre-contemplative"]}
            ]},
            {"title": "Management Plan", "safety_netting": "If you develop severe shortness of breath, chest pain, or palpitations with activity, seek urgent medical attention.", "questions": [
                {"id": "ob_target", "type": "number", "label": "Target Weight Loss (5-10% = clinically significant)", "required": True, "placeholder": "e.g., 5"},
                {"id": "ob_intervention", "type": "multi_select", "label": "Interventions", "required": True, "options": ["Dietary Advice", "Exercise Prescription", "Weight Management Programme Referral", "Psychological Support", "Pharmacotherapy (e.g., Orlistat, Semaglutide)", "Bariatric Surgery Referral"]},
                {"id": "ob_medication", "type": "textarea", "label": "Weight Loss Medication", "required": False, "placeholder": "e.g., Semaglutide 0.25mg weekly..."},
                {"id": "ob_review_frequency", "type": "single_select", "label": "Review Frequency", "required": True, "options": ["Monthly", "3-Monthly", "6-Monthly", "Annual"]},
                {"id": "ob_notes", "type": "textarea", "label": "Additional Notes", "required": False}
            ]}
        ]}, "is_public": True
    }

    existing = db.query(Template).filter(Template.title == template_data["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_template = Template(title=template_data["title"], description=template_data["description"], category=template_data["category"], content=template_data["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_template); db.commit()
    print(f"Template '{template_data['title']}' created!"); db.close()

if __name__ == "__main__":
    seed_obesity_template()