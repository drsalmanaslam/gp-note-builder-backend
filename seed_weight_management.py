from app.database import SessionLocal
from app.models import User, Template, Category

def seed_weight_management():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin found!")
        db.close()
        return

    title = "Weight Management & Obesity"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return

    template = Template(
        title=title,
        description="Obesity assessment and weight management per NICE CG189, covering cardiovascular risk, dietary advice, physical activity, pharmacotherapy (orlistat, GLP-1 agonists), and bariatric surgery referral criteria.",
        category="General Practice",
        content={"sections": [
            {
                "title": "Anthropometric Measurements",
                "section_type": "examination",
                "questions": [
                    {"id": "wt_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 95"},
                    {"id": "wt_height", "type": "number", "label": "Height (cm)", "required": True, "placeholder": "e.g., 165"},
                    {"id": "wt_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 34.9"},
                    {"id": "wt_waist", "type": "number", "label": "Waist Circumference (cm)", "required": False, "placeholder": "e.g., 102"},
                    {"id": "wt_bmi_category", "type": "single_select", "label": "BMI Category", "required": True, "options": ["Overweight (25-29.9)", "Obese Class I (30-34.9)", "Obese Class II (35-39.9)", "Obese Class III (≥40)"]},
                    {"id": "wt_previous_weight", "type": "text", "label": "Previous Weight & Date", "required": False, "placeholder": "e.g., 88kg (6 months ago)"}
                ]
            },
            {
                "title": "Dietary Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "wt_meals", "type": "single_select", "label": "Meal Pattern", "required": True, "options": ["3 regular meals", "Skips breakfast", "Skips lunch", "Grazes all day", "One large meal/day"]},
                    {"id": "wt_fruit_veg", "type": "single_select", "label": "Fruit & Vegetables (portions/day)", "required": True, "options": ["0-1", "2-3", "4-5", "≥5"]},
                    {"id": "wt_sugary_drinks", "type": "single_select", "label": "Sugary Drinks / Fizzy Drinks", "required": True, "options": ["None", "1-2/week", "Daily", "Multiple/day"]},
                    {"id": "wt_takeaways", "type": "single_select", "label": "Takeaways / Fast Food", "required": True, "options": ["Rarely/Never", "1-2/month", "Weekly", "Multiple/week"]},
                    {"id": "wt_snacking", "type": "single_select", "label": "Snacking Between Meals", "required": True, "options": ["Rarely", "Occasionally", "Frequently", "Constantly"]},
                    {"id": "wt_alcohol", "type": "single_select", "label": "Alcohol (units/week)", "required": True, "options": ["0", "1-7", "8-14", "15-21", ">21"]},
                    {"id": "wt_emotional_eating", "type": "toggle", "label": "Emotional / Stress Eating?", "required": True},
                    {"id": "wt_portion_sizes", "type": "single_select", "label": "Portion Sizes", "required": True, "options": ["Small", "Average", "Large", "Very large"]}
                ]
            },
            {
                "title": "Physical Activity",
                "section_type": "history",
                "questions": [
                    {"id": "wt_exercise_type", "type": "multi_select", "label": "Current Activity", "required": True, "options": ["Walking", "Running/Jogging", "Swimming", "Cycling", "Gym/Resistance", "Team Sports", "None"]},
                    {"id": "wt_exercise_frequency", "type": "single_select", "label": "Exercise Frequency", "required": True, "options": ["None - sedentary", "1-2 sessions/week", "3-4 sessions/week", "Daily"]},
                    {"id": "wt_exercise_minutes", "type": "single_select", "label": "Minutes per Session", "required": True, "options": ["<15 min", "15-30 min", "30-60 min", ">60 min"]},
                    {"id": "wt_barriers", "type": "multi_select", "label": "Barriers to Exercise", "required": False, "options": ["Time", "Motivation", "Joint pain", "Breathlessness", "Cost", "Childcare", "None"]}
                ]
            },
            {
                "title": "Metabolic & Cardiovascular Risk",
                "section_type": "assessment",
                "questions": [
                    {"id": "wt_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 142/88"},
                    {"id": "wt_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
                    {"id": "wt_family_cvd", "type": "toggle", "label": "Family History Premature CVD? (<55 male, <65 female)", "required": True},
                    {"id": "wt_diabetes", "type": "toggle", "label": "Known Diabetes / Prediabetes?", "required": True},
                    {"id": "wt_qrisk", "type": "number", "label": "QRISK3 Score (%)", "required": False, "placeholder": "e.g., 12"},
                    {"id": "wt_osa", "type": "multi_select", "label": "Obstructive Sleep Apnoea Screen", "required": True, "options": ["Loud snoring", "Witnessed apnoeas", "Daytime sleepiness", "Morning headaches", "None"]},
                    {"id": "wt_pcos", "type": "toggle", "label": "PCOS? (Female patients)", "required": False},
                    {"id": "wt_oa", "type": "toggle", "label": "Osteoarthritis (Weight-bearing joints)?", "required": True}
                ]
            },
            {
                "title": "Previous Weight Loss Attempts",
                "section_type": "history",
                "questions": [
                    {"id": "wt_previous_attempts", "type": "toggle", "label": "Previous Weight Loss Attempts?", "required": True},
                    {"id": "wt_methods_tried", "type": "multi_select", "label": "Methods Tried", "required": False, "options": ["Diet alone", "Exercise alone", "Commercial programme (Slimming World, WW)", "Orlistat (Xenical)", "GLP-1 agonist (Ozempic, Mounjaro)", "Referral to weight management", "Bariatric surgery"]},
                    {"id": "wt_max_loss", "type": "text", "label": "Maximum Weight Loss Achieved", "required": False, "placeholder": "e.g., Lost 12kg on WW in 2024, regained 8kg"},
                    {"id": "wt_regain", "type": "toggle", "label": "Weight Regained After Previous Loss?", "required": False},
                    {"id": "wt_readiness", "type": "single_select", "label": "Readiness to Change (0-10)", "required": True, "options": ["0-3: Not ready", "4-6: Considering", "7-8: Ready", "9-10: Taking action"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "wt_bloods", "type": "multi_select", "label": "Blood Tests", "required": False, "options": ["Fasting glucose / HbA1c", "Fasting lipids", "TFTs", "LFTs", "U&E", "FBC", "None", "Awaiting results"]},
                    {"id": "wt_ecg", "type": "toggle", "label": "ECG Indicated? (Before exercise programme if high risk)", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Weight loss requires sustained lifestyle change. Aim for 0.5-1kg/week. 5-10% weight loss significantly reduces cardiovascular risk. Dietary advice: 600kcal deficit/day, Mediterranean diet, reduce processed foods/sugar, increase protein and fibre, 5 portions fruit/veg, use smaller plates, mindful eating. Exercise: 150 min moderate or 75 min vigorous activity/week + strength training 2x/week. Return if: chest pain on exertion, severe breathlessness, or if considering medication/surgery options.",
                "questions": [
                    {"id": "wt_plan", "type": "multi_select", "label": "Management Options", "required": True, "options": ["Lifestyle advice + diet sheet provided", "Physical activity prescription", "Refer to dietitian", "Refer to NHS Weight Management Programme", "Consider Orlistat (BMI ≥30, or ≥28 + comorbidities)", "Consider GLP-1 agonist (per local guidelines)", "Refer for bariatric surgery (BMI ≥40, or ≥35 + comorbidities)", "Commercial programme signposted", "Sick note if indicated"]},
                    {"id": "wt_diet_advice", "type": "toggle", "label": "Dietary Advice Leaflet Provided?", "required": True},
                    {"id": "wt_weight_target", "type": "text", "label": "Target Weight / Goal", "required": True, "placeholder": "e.g., 5% weight loss in 12 weeks (4.7kg)"},
                    {"id": "wt_medication", "type": "text", "label": "Medication Started (if any)", "required": False, "placeholder": "e.g., Orlistat 120mg TDS with meals"},
                    {"id": "wt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 4 weeks, check weight and BP, reinforce lifestyle changes"}
                ]
            }
        ]},
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_weight_management()