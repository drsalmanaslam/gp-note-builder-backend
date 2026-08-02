from app.database import SessionLocal
from app.models import Template, User

def seed_anxiety_management():
    db = SessionLocal()
    
    title = "Anxiety Management (GAD-7)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        db.delete(existing)
        db.commit()
    
    admin = db.query(User).filter(User.role == "admin").first()
    
    template = Template(
        title=title,
        description="Comprehensive anxiety management template covering GAD-7 assessment, panic attacks, medication review, and stepped care approach per NICE guidance.",
        category="Mental Health",
        content={
            "sections": [
                {
                    "title": "Anxiety Assessment",
                    "section_type": "history",
                    "questions": [
                        {"id": "anx_presenting", "type": "text", "label": "Main Concerns", "required": True, "placeholder": "e.g., Constant worry, panic attacks, social anxiety"},
                        {"id": "anx_gad7_score", "type": "number", "label": "GAD-7 Score", "required": True, "placeholder": "e.g., 14"},
                        {"id": "anx_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 6 months"},
                        {"id": "anx_trigger", "type": "text", "label": "Triggers", "required": False, "placeholder": "e.g., Work stress, relationship, financial"},
                        {"id": "anx_symptoms", "type": "multi_select", "label": "Key Symptoms", "required": True, "options": ["Excessive worry", "Restlessness", "Fatigue", "Poor concentration", "Irritability", "Muscle tension", "Sleep disturbance", "Panic attacks"]},
                        {"id": "anx_panic", "type": "toggle", "label": "Panic Attacks?", "required": True},
                        {"id": "anx_panic_frequency", "type": "text", "label": "Panic Attack Frequency", "required": False, "placeholder": "e.g., 3 times per week"},
                        {"id": "anx_avoidance", "type": "toggle", "label": "Avoidance Behaviours?", "required": True},
                        {"id": "anx_impact", "type": "single_select", "label": "Impact on Daily Life", "required": True, "options": ["Mild", "Moderate", "Severe", "Unable to function"]}
                    ]
                },
                {
                    "title": "Physical Health Screen",
                    "section_type": "history",
                    "questions": [
                        {"id": "anx_palpitations", "type": "toggle", "label": "Palpitations / Chest Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cardiac symptoms need ECG. Consider 24h Holter if paroxysmal.", "red_flag_negative": ""},
                        {"id": "anx_thyroid", "type": "toggle", "label": "Thyroid Symptoms? (Heat intolerance, tremor, weight loss)", "required": True},
                        {"id": "anx_caffeine", "type": "single_select", "label": "Caffeine Intake", "required": True, "options": ["None", "1-2 cups/day", "3-5 cups/day", ">5 cups/day or energy drinks"]},
                        {"id": "anx_alcohol", "type": "single_select", "label": "Alcohol Use", "required": True, "options": ["None", "Within limits", "Excess", "Using to manage anxiety"]},
                        {"id": "anx_substances", "type": "toggle", "label": "Recreational Drugs?", "required": False},
                        {"id": "anx_bloods", "type": "toggle", "label": "Bloods Done? (FBC, TFTs, glucose)", "required": False}
                    ]
                },
                {
                    "title": "Current Management",
                    "section_type": "history",
                    "questions": [
                        {"id": "anx_medication", "type": "text", "label": "Current Medication", "required": False, "placeholder": "e.g., Sertraline 50mg, Propranolol 40mg PRN"},
                        {"id": "anx_therapy", "type": "single_select", "label": "Psychological Therapy", "required": True, "options": ["None", "IAPT referral made", "Currently in therapy", "Completed therapy", "Private therapy"]},
                        {"id": "anx_self_help", "type": "multi_select", "label": "Self-Help Strategies", "required": False, "options": ["Exercise", "Meditation/Mindfulness", "Breathing exercises", "Sleep hygiene", "None"]}
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Generalised Anxiety Disorder (GAD)",
                        "Panic Disorder",
                        "Social Anxiety Disorder",
                        "Mixed Anxiety & Depression",
                        "Hyperthyroidism",
                        "Substance-induced anxiety",
                        "Cardiac arrhythmia"
                    ],
                    "questions": [
                        {"id": "anx_severity", "type": "single_select", "label": "Severity (per GAD-7)", "required": True, "options": ["Mild (5-9)", "Moderate (10-14)", "Severe (15-21)"]},
                        {"id": "anx_stepped_care", "type": "single_select", "label": "Stepped Care Level (NICE)", "required": True, "options": ["Step 1: Watchful waiting + psychoeducation", "Step 2: Low-intensity CBT / Guided self-help", "Step 3: High-intensity CBT / Medication", "Step 4: Specialist mental health"]}
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "If you experience worsening anxiety, panic attacks, chest pain, or thoughts of self-harm, seek urgent help. Contact GP, call 111, or attend A&E. Do not stop medication abruptly. Avoid alcohol and limit caffeine. Regular exercise (30 min/day) and mindfulness can significantly reduce anxiety symptoms. Continue treatment for at least 12 months after improvement to prevent relapse.",
                    "questions": [
                        {"id": "anx_plan", "type": "multi_select", "label": "Management Options", "required": True, "options": ["Watchful waiting", "Guided self-help / IAPT referral", "Start SSRI (Sertraline 50mg first-line)", "Increase existing medication", "Propranolol for physical symptoms", "Refer to CMHT", "CBT referral", "Psychoeducation provided"]},
                        {"id": "anx_prescription", "type": "text", "label": "New Prescription", "required": False, "placeholder": "e.g., Sertraline 50mg OD, Propranolol 40mg PRN"},
                        {"id": "anx_sick_note", "type": "toggle", "label": "Sick Note Required?", "required": False},
                        {"id": "anx_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 4 weeks, check GAD-7 response"}
                    ]
                }
            ]
        },
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_anxiety_management()