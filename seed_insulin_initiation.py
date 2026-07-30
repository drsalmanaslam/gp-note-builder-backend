from app.database import SessionLocal
from app.models import User, Template, Category

def seed_insulin_initiation():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "Insulin Initiation in Type 2 Diabetes",
        "description": "Structured template for initiating insulin in Type 2 diabetes covering regimen selection, dose titration, hypoglycaemia education, driving safety, and sick-day rules.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Indication & Current Status",
                "section_type": "history",
                "questions": [
                    {"id": "ins_indication", "type": "single_select", "label": "Indication for Insulin Initiation", "required": True, "options": ["Persistently elevated HbA1c despite maximal oral agents / GLP-1", "Acute decompensation / symptomatic hyperglycaemia", "Contraindication to oral agents", "Patient preference"]},
                    {"id": "ins_hba1c", "type": "number", "label": "Current HbA1c (mmol/mol)", "required": True, "placeholder": "e.g., 86"},
                    {"id": "ins_adherence", "type": "single_select", "label": "Adherence to Current Therapy", "required": True, "options": ["Adherent with maximal doses", "Partial adherence", "Non-adherent"]},
                    {"id": "ins_diet", "type": "single_select", "label": "Dietary Management", "required": True, "options": ["Low glycaemic diet - reviewed by dietician", "Diet not yet optimised", "Dietician review not yet arranged"]},
                    {"id": "ins_exercise", "type": "text", "label": "Exercise Frequency", "required": False, "placeholder": "e.g., 3-4 times per week"},
                    {"id": "ins_hyperglycaemia_symptoms", "type": "multi_select", "label": "Symptoms of Hyperglycaemia", "required": False, "options": ["Polyuria", "Polydipsia", "Weight loss", "Blurred vision", "Fatigue", "None reported"]},
                    {"id": "ins_patient_preference", "type": "single_select", "label": "Patient Preference", "required": True, "options": ["Wants to proceed - aim for better control", "Reluctant / declines at this time", "Undecided - needs further discussion"]}
                ]
            },
            {
                "title": "Insulin Regimen",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_endo_referral", "type": "single_select", "label": "Endocrinology Referral", "required": False, "options": ["Referred", "Not referred - GP-managed initiation"]},
                    {"id": "ins_type", "type": "single_select", "label": "Insulin Type", "required": False, "options": ["Levemir (Detemir)", "Lantus (Glargine)", "Toujeo (Glargine U300)", "Abasaglar (Glargine biosimilar)", "Insulatard (NPH)", "Other"]},
                    {"id": "ins_starting_dose", "type": "number", "label": "Starting Dose (units)", "required": False, "placeholder": "e.g., 10"},
                    {"id": "ins_frequency", "type": "single_select", "label": "Frequency / Timing", "required": False, "options": ["Once daily at night (nocte)", "Once daily in morning", "Twice daily", "Other"]},
                    {"id": "ins_concurrent_orals", "type": "multi_select", "label": "Concurrent Oral Therapy", "required": False, "options": ["Continue Metformin", "Discontinue sulfonylurea (hypo risk)", "Discontinue other hypoglycaemic agents", "Continue GLP-1 receptor agonist", "Continue SGLT2 inhibitor"]}
                ]
            },
            {
                "title": "Self-Monitoring Setup",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_smbg_understands", "type": "toggle", "label": "Understands Need for Frequent Self-Monitoring?", "required": True},
                    {"id": "ins_equipment", "type": "multi_select", "label": "Equipment Prescribed", "required": False, "options": ["Lancets", "Test strips", "Glucose meter", "Sharps bin"]},
                    {"id": "ins_proficiency", "type": "toggle", "label": "Proficient at Self-Monitoring?", "required": True},
                    {"id": "ins_not_single_reading", "type": "toggle", "label": "Understands NOT to Adjust Dose on Single Reading?", "required": True},
                    {"id": "ins_testing_schedule", "type": "single_select", "label": "Testing Schedule", "required": False, "options": ["Before breakfast (fasting)", "Before breakfast + before dinner", "Before breakfast + 2h post-meal", "Other timing"]}
                ]
            },
            {
                "title": "Dose Titration Protocol",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_titration", "type": "single_select", "label": "Fasting Glucose → Action (Monitor 72h Before Each Change)", "required": True, "options": ["4-7 mmol/L = OPTIMAL - No change", "<4 mmol/L = REDUCE insulin by 4 units daily", "7.1-14 mmol/L = INCREASE insulin by 2 units daily", ">14 mmol/L = INCREASE insulin by 4 units daily"]}
                ]
            },
            {
                "title": "Hypoglycaemia Education",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_hypo_understands", "type": "toggle", "label": "Understands Hypoglycaemia Management? (15-20g fast CHO, recheck 15 min)", "required": True},
                    {"id": "ins_fast_glucose_access", "type": "toggle", "label": "Always Has Fast-Acting Glucose Access?", "required": True},
                    {"id": "ins_glucagon", "type": "multi_select", "label": "Third-Party Support Arrangements", "required": False, "options": ["Family/friend able to give IM glucagon if needed", "Family/friend able to give oral CHO once safe", "Understands: if IM glucagon not effective in 10 min → call ambulance (IV glucose)", "Not yet arranged"]}
                ]
            },
            {
                "title": "Driving & Occupational Safety",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_driving_informed", "type": "multi_select", "label": "Informed Relevant Parties?", "required": False, "options": ["Insurance company", "NDLS (National Driver Licence Service)", "Employer (if relevant)", "Not applicable"]},
                    {"id": "ins_pre_drive_test", "type": "toggle", "label": "Understands Pre-Driving Glucose Testing Requirement?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Must test glucose before driving + every 2 hours on long journeys. Do NOT drive if <5 mmol/L.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Sick-Day Rules & Adverse Effects",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_ketone_testing", "type": "toggle", "label": "Understands Ketone Testing When Unwell?", "required": True},
                    {"id": "ins_never_stop_insulin", "type": "toggle", "label": "Understands NEVER to Stop Insulin When Unwell? (May need MORE)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Never stop insulin during illness. Risk of DKA. May need increased doses.", "red_flag_negative": ""},
                    {"id": "ins_weight_gain", "type": "toggle", "label": "Counselled on Weight Gain Risk?", "required": False}
                ]
            },
            {
                "title": "Dietary Advice - Low GI for Type 2 Diabetes",
                "section_type": "plan",
                "questions": [
                    {"id": "ins_dietary_advice", "type": "multi_select", "label": "Dietary Advice Given", "required": False, "options": ["Cut out table sugar + fizzy drinks; reduce alcohol + starchy carbs", "Substitute mash/chips/pasta/rice with green vegetables", "Homemade soups - green veg, mushroom, tomato, onion", "Fruits - raspberries, strawberries, blueberries", "Eggs, salmon, tuna, unprocessed meats", "Plain full-fat yoghurt with berries", "Cheese in moderation", "Snacks - almonds/walnuts; >70% dark chocolate"]}
                ]
            },
            {
                "title": "Targets & Follow-Up",
                "section_type": "plan",
                "safety_netting": "Target HbA1c: individualised (usually 53-58 mmol/mol). Balance glycaemic benefits against harms (hypoglycaemia, weight gain). Titrate insulin slowly - monitor fasting glucose for 72 hours before each dose change. Never stop insulin during illness. Test ketones when unwell. Do not drive if glucose <5 mmol/L. Inform NDLS + insurance of insulin initiation. Review in 1-2 weeks for dose adjustment. Ensure family/friend trained in glucagon administration. If recurrent hypos or poor control: refer diabetes specialist team.",
                "questions": [
                    {"id": "ins_target_hba1c", "type": "number", "label": "Target HbA1c (mmol/mol)", "required": False, "placeholder": "e.g., 53"},
                    {"id": "ins_risk_benefit", "type": "toggle", "label": "Risk-Benefit Discussion Completed?", "required": True},
                    {"id": "ins_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1-2 weeks for dose titration, 4-6 weeks HbA1c review"}
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
    seed_insulin_initiation()