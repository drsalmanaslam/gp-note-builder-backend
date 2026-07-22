from app.database import SessionLocal
from app.models import User, Template, Category
from app.auth import get_password_hash

def seed_all_templates():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("❌ Admin user not found")
        db.close()
        return
    
    templates_data = [
        {
            "title": "Shortness of Breath (SOB)",
            "description": "Complete assessment for patients presenting with shortness of breath.",
            "category": "Respiratory",
            "content": {
                "sections": [
                    {
                        "id": "situation",
                        "title": "Situation",
                        "questions": [
                            {"id": "consultation_type", "type": "select", "label": "Consultation Type", "required": True, "options": ["F2F consultation: ID confirmed", "Telephone consultation, ID confirmed", "Seen alone", "Seen with family/carer"]},
                            {"id": "gender", "type": "select", "label": "Gender", "required": True, "options": ["Male", "Female", "Trans Man", "Trans Woman"]},
                            {"id": "age", "type": "number", "label": "Age (years)", "required": True, "placeholder": "e.g., 45"}
                        ]
                    },
                    {
                        "id": "chief_complaint",
                        "title": "Chief Complaint",
                        "questions": [
                            {"id": "sob_type", "type": "select", "label": "SOB Type", "required": True, "options": ["on exertion", "at rest"]},
                            {"id": "onset", "type": "select", "label": "Onset", "required": True, "options": ["sudden", "gradual"]},
                            {"id": "pattern", "type": "select", "label": "Pattern", "required": False, "options": ["constant", "intermittent", "occasional", "worsening", "variable in intensity"]},
                            {"id": "duration", "type": "text", "label": "Duration", "required": False, "placeholder": "e.g., 3 days"}
                        ]
                    },
                    {"id": "history", "title": "History", "questions": [{"id": "history_details", "type": "textarea", "label": "History Details", "required": False, "placeholder": "Describe the history..."}]},
                    {"id": "examination", "title": "Examination", "questions": [{"id": "exam_findings", "type": "textarea", "label": "Examination Findings", "required": False, "placeholder": "Describe examination findings..."}]},
                    {"id": "assessment", "title": "Impression / Assessment", "questions": [{"id": "impression", "type": "textarea", "label": "Impression", "required": False, "placeholder": "Describe your impression..."}]},
                    {"id": "plan", "title": "Plan", "questions": [{"id": "plan_details", "type": "textarea", "label": "Plan", "required": False, "placeholder": "Describe the plan..."}]}
                ]
            },
            "differentials": ["Asthma", "COPD", "Pulmonary Embolism", "Heart Failure", "Pneumonia", "Anxiety"],
            "safetyNetting": ["Seek immediate medical attention if breathing worsens", "Call 999 if unable to speak in full sentences", "Follow up with GP within 48 hours"],
            "is_public": True
        },
        {
            "title": "Chest Pain Assessment",
            "description": "Complete assessment for patients presenting with chest pain.",
            "category": "Cardiovascular",
            "content": {
                "sections": [
                    {
                        "id": "history",
                        "title": "History of Presenting Complaint",
                        "questions": [
                            {"id": "pain_onset", "type": "text", "label": "Onset of pain", "required": True, "placeholder": "e.g., Sudden onset 2 hours ago"},
                            {"id": "pain_nature", "type": "select", "label": "Nature of pain", "required": True, "options": ["Crushing", "Sharp", "Dull", "Burning", "Tearing"]},
                            {"id": "pain_location", "type": "text", "label": "Location", "required": False, "placeholder": "e.g., Central chest, left side"},
                            {"id": "pain_radiation", "type": "text", "label": "Radiation", "required": False, "placeholder": "e.g., Left arm, jaw, back"},
                            {"id": "pain_severity", "type": "number", "label": "Severity (1-10)", "required": True},
                            {"id": "aggravating_factors", "type": "text", "label": "Aggravating factors", "required": False, "placeholder": "e.g., Exertion, breathing, movement"},
                            {"id": "relieving_factors", "type": "text", "label": "Relieving factors", "required": False, "placeholder": "e.g., Rest, GTN, posture"},
                            {"id": "associated_symptoms", "type": "text", "label": "Associated symptoms", "required": False, "placeholder": "e.g., SOB, nausea, sweating"}
                        ]
                    },
                    {
                        "id": "risk_factors",
                        "title": "Risk Factors",
                        "questions": [
                            {"id": "smoking", "type": "select", "label": "Smoking", "required": False, "options": ["Never", "Ex-smoker", "Current"]},
                            {"id": "hypertension", "type": "select", "label": "Hypertension", "required": False, "options": ["Yes", "No"]},
                            {"id": "diabetes", "type": "select", "label": "Diabetes", "required": False, "options": ["Yes", "No"]},
                            {"id": "family_history", "type": "select", "label": "Family history of IHD", "required": False, "options": ["Yes", "No"]}
                        ]
                    },
                    {"id": "examination", "title": "Examination", "questions": [{"id": "exam_findings", "type": "textarea", "label": "Examination Findings", "required": False, "placeholder": "Describe examination findings..."}]},
                    {"id": "investigations", "title": "Investigations", "questions": [{"id": "investigations", "type": "textarea", "label": "Investigations", "required": False, "placeholder": "List investigations..."}]},
                    {"id": "assessment", "title": "Impression / Assessment", "questions": [{"id": "impression", "type": "textarea", "label": "Impression", "required": False, "placeholder": "Describe your impression..."}]},
                    {"id": "plan", "title": "Plan", "questions": [{"id": "plan_details", "type": "textarea", "label": "Plan", "required": False, "placeholder": "Describe the plan..."}]}
                ]
            },
            "red_flags": [
                {"id": "red_flag_mi", "description": "Myocardial Infarction - Cardiac sounding chest pain with haemodynamic instability", "severity": "high"},
                {"id": "red_flag_aortic", "description": "Aortic Dissection - Tearing chest pain with BP differential", "severity": "high"},
                {"id": "red_flag_pe", "description": "Pulmonary Embolism - Sudden onset pleuritic chest pain with hypoxia", "severity": "high"}
            ],
            "differentials": ["Myocardial Infarction", "Unstable Angina", "Aortic Dissection", "Pulmonary Embolism", "Pericarditis"],
            "safetyNetting": ["Call 999 immediately if chest pain worsens", "Take GTN as prescribed", "Attend A&E if new symptoms develop", "Follow up with GP within 48 hours"],
            "is_public": True
        },
        {
            "title": "Headache Assessment",
            "description": "Complete assessment for patients presenting with headache.",
            "category": "Neurology",
            "content": {
                "sections": [
                    {
                        "id": "history",
                        "title": "History of Presenting Complaint",
                        "questions": [
                            {"id": "headache_onset", "type": "select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
                            {"id": "headache_timing", "type": "text", "label": "Timing", "required": False, "placeholder": "e.g., Morning, evening, nocturnal"},
                            {"id": "headache_frequency", "type": "text", "label": "Frequency", "required": False, "placeholder": "e.g., Daily, weekly, monthly"},
                            {"id": "headache_duration", "type": "text", "label": "Duration", "required": False, "placeholder": "e.g., 30 minutes, 2 hours, 3 days"},
                            {"id": "headache_character", "type": "select", "label": "Character", "required": True, "options": ["Throbbing", "Pressure", "Sharp", "Dull", "Burning"]},
                            {"id": "headache_location", "type": "text", "label": "Location", "required": False, "placeholder": "e.g., Frontal, occipital, unilateral, bilateral"},
                            {"id": "headache_severity", "type": "number", "label": "Severity (1-10)", "required": True},
                            {"id": "associated_symptoms", "type": "text", "label": "Associated symptoms", "required": False, "placeholder": "e.g., Nausea, vomiting, photophobia, aura"}
                        ]
                    },
                    {"id": "examination", "title": "Examination", "questions": [{"id": "exam_findings", "type": "textarea", "label": "Examination Findings", "required": False, "placeholder": "Describe examination findings..."}]},
                    {"id": "investigations", "title": "Investigations", "questions": [{"id": "investigations", "type": "textarea", "label": "Investigations", "required": False, "placeholder": "List investigations..."}]},
                    {"id": "assessment", "title": "Impression / Assessment", "questions": [{"id": "impression", "type": "textarea", "label": "Impression", "required": False, "placeholder": "Describe your impression..."}]},
                    {"id": "plan", "title": "Plan", "questions": [{"id": "plan_details", "type": "textarea", "label": "Plan", "required": False, "placeholder": "Describe the plan..."}]}
                ]
            },
            "red_flags": [
                {"id": "red_flag_sah", "description": "Subarachnoid Haemorrhage - Thunderclap headache", "severity": "high"},
                {"id": "red_flag_meningitis", "description": "Meningitis - Headache with fever and neck stiffness", "severity": "high"},
                {"id": "red_flag_temporal", "description": "Temporal Arteritis - New headache in patient >50 years", "severity": "high"}
            ],
            "differentials": ["Migraine", "Tension-type headache", "Cluster headache", "Subarachnoid Haemorrhage", "Meningitis", "Temporal Arteritis"],
            "safetyNetting": ["Seek immediate medical attention if headache is 'the worst ever'", "Attend A&E if severe headache with vomiting or confusion", "Call 111 for advice if unable to manage symptoms", "Follow up with GP if headache persists >48 hours"],
            "is_public": True
        },
        {
            "title": "UTI Assessment",
            "description": "Complete assessment for urinary tract infections.",
            "category": "Urology",
            "content": {
                "sections": [
                    {
                        "id": "history",
                        "title": "History of Presenting Complaint",
                        "questions": [
                            {"id": "dysuria", "type": "select", "label": "Dysuria (pain on urination)", "required": True, "options": ["Yes", "No"]},
                            {"id": "frequency", "type": "select", "label": "Frequency", "required": True, "options": ["Yes", "No"]},
                            {"id": "urgency", "type": "select", "label": "Urgency", "required": True, "options": ["Yes", "No"]},
                            {"id": "haematuria", "type": "select", "label": "Haematuria (blood in urine)", "required": True, "options": ["Yes", "No"]},
                            {"id": "fever", "type": "select", "label": "Fever", "required": True, "options": ["Yes", "No"]},
                            {"id": "loin_pain", "type": "select", "label": "Loin pain/flank pain", "required": True, "options": ["Yes", "No"]},
                            {"id": "uti_history", "type": "text", "label": "History of UTIs", "required": False, "placeholder": "e.g., Previous UTIs, recurrent infections"}
                        ]
                    },
                    {"id": "examination", "title": "Examination", "questions": [{"id": "exam_findings", "type": "textarea", "label": "Examination Findings", "required": False, "placeholder": "Describe examination findings..."}]},
                    {"id": "investigations", "title": "Investigations", "questions": [{"id": "investigations", "type": "textarea", "label": "Investigations", "required": False, "placeholder": "List investigations..."}]},
                    {"id": "assessment", "title": "Impression / Assessment", "questions": [{"id": "impression", "type": "textarea", "label": "Impression", "required": False, "placeholder": "Describe your impression..."}]},
                    {"id": "plan", "title": "Plan", "questions": [{"id": "plan_details", "type": "textarea", "label": "Plan", "required": False, "placeholder": "Describe the plan..."}]}
                ]
            },
            "red_flags": [
                {"id": "red_flag_pyelonephritis", "description": "Pyelonephritis - Flank pain, high fever, rigors", "severity": "high"},
                {"id": "red_flag_sepsis", "description": "Sepsis - Hypotension, confusion, tachypnoea", "severity": "high"},
                {"id": "red_flag_pregnancy", "description": "Pregnancy with UTI - Requires urgent review", "severity": "high"}
            ],
            "differentials": ["Cystitis", "Pyelonephritis", "Urethritis", "Prostatitis", "Vaginitis"],
            "safetyNetting": ["Complete the full course of antibiotics", "Increase fluid intake (2-3 litres/day)", "Use paracetamol for pain and fever", "Return to GP if symptoms not improving in 48 hours", "Attend A&E if develops high fever, rigors, or confusion"],
            "is_public": True
        },
        {
            "title": "Depression Assessment",
            "description": "Comprehensive assessment for patients presenting with depressive symptoms.",
            "category": "Mental Health",
            "content": {
                "sections": [
                    {
                        "id": "history",
                        "title": "History of Presenting Complaint",
                        "questions": [
                            {"id": "low_mood", "type": "select", "label": "Low mood", "required": True, "options": ["Yes", "No"]},
                            {"id": "anhedonia", "type": "select", "label": "Anhedonia (loss of interest/pleasure)", "required": True, "options": ["Yes", "No"]},
                            {"id": "fatigue", "type": "select", "label": "Fatigue", "required": True, "options": ["Yes", "No"]},
                            {"id": "sleep_disturbance", "type": "select", "label": "Sleep disturbance", "required": False, "options": ["Insomnia", "Hypersomnia", "Normal"]},
                            {"id": "appetite_change", "type": "select", "label": "Appetite change", "required": False, "options": ["Increased", "Decreased", "Normal"]},
                            {"id": "depression_duration", "type": "text", "label": "Duration of symptoms", "required": False, "placeholder": "e.g., 2 weeks, 3 months"},
                            {"id": "suicidal_thoughts", "type": "select", "label": "Suicidal thoughts", "required": True, "options": ["Yes", "No"]}
                        ]
                    },
                    {
                        "id": "risk_factors",
                        "title": "Risk Factors",
                        "questions": [
                            {"id": "previous_depression", "type": "select", "label": "Previous episodes of depression", "required": False, "options": ["Yes", "No"]},
                            {"id": "family_history_depression", "type": "select", "label": "Family history of depression", "required": False, "options": ["Yes", "No"]},
                            {"id": "chronic_illness", "type": "text", "label": "Chronic illness", "required": False, "placeholder": "e.g., Diabetes, heart disease"},
                            {"id": "life_stressors", "type": "text", "label": "Life stressors", "required": False, "placeholder": "e.g., Bereavement, job loss, relationship issues"}
                        ]
                    },
                    {"id": "examination", "title": "Mental State Examination", "questions": [{"id": "mse", "type": "textarea", "label": "Mental State Examination", "required": False, "placeholder": "Describe mental state examination..."}]},
                    {"id": "assessment", "title": "Impression / Assessment", "questions": [{"id": "impression", "type": "textarea", "label": "Impression", "required": False, "placeholder": "Describe your impression..."}]},
                    {"id": "plan", "title": "Plan", "questions": [{"id": "plan_details", "type": "textarea", "label": "Plan", "required": False, "placeholder": "Describe the plan..."}]}
                ]
            },
            "red_flags": [
                {"id": "red_flag_suicide", "description": "Suicidal ideation with intent or plan - URGENT", "severity": "high"},
                {"id": "red_flag_psychosis", "description": "Psychotic symptoms (hallucinations, delusions)", "severity": "high"},
                {"id": "red_flag_self_neglect", "description": "Severe self-neglect - Requires urgent review", "severity": "high"}
            ],
            "differentials": ["Major Depressive Disorder", "Persistent Depressive Disorder", "Bipolar Disorder", "Adjustment Disorder", "Anxiety Disorder"],
            "safetyNetting": ["If experiencing thoughts of self-harm, contact Samaritans (116 123) immediately", "If feeling unable to cope, call 111 or attend A&E", "Take medications as prescribed", "Attend follow-up appointments", "Monitor mood daily", "Contact GP if symptoms worsen"],
            "is_public": True
        },
        {
            "title": "Asthma Review",
            "description": "Comprehensive asthma review including symptoms, control assessment, and management.",
            "category": "Chronic Disease Reviews",
            "content": {
                "sections": [
                    {
                        "id": "history",
                        "title": "History of Presenting Complaint",
                        "questions": [
                            {"id": "wheeze", "type": "select", "label": "Wheeze", "required": True, "options": ["Yes", "No"]},
                            {"id": "breathlessness", "type": "select", "label": "Breathlessness", "required": True, "options": ["Yes", "No"]},
                            {"id": "chest_tightness", "type": "select", "label": "Chest tightness", "required": True, "options": ["Yes", "No"]},
                            {"id": "cough", "type": "select", "label": "Cough (especially at night, early morning)", "required": True, "options": ["Yes", "No"]},
                            {"id": "exercise_induced", "type": "select", "label": "Exercise induced symptoms", "required": False, "options": ["Yes", "No"]},
                            {"id": "trigger_factors", "type": "text", "label": "Trigger factors", "required": False, "placeholder": "e.g., Cold air, allergens, stress, smoking"}
                        ]
                    },
                    {
                        "id": "medication_review",
                        "title": "Medication Review",
                        "questions": [
                            {"id": "saba_use", "type": "text", "label": "SABA use (reliever) - Frequency", "required": False, "placeholder": "e.g., Daily, weekly, monthly"},
                            {"id": "ics_use", "type": "text", "label": "ICS use (preventer) - Dose and compliance", "required": False, "placeholder": "e.g., 100mcg BD, mostly compliant"},
                            {"id": "inhaler_technique", "type": "select", "label": "Inhaler technique", "required": False, "options": ["Good", "Poor", "Needs review"]}
                        ]
                    },
                    {"id": "examination", "title": "Examination", "questions": [{"id": "exam_findings", "type": "textarea", "label": "Examination Findings", "required": False, "placeholder": "Describe examination findings..."}]},
                    {"id": "investigations", "title": "Investigations", "questions": [{"id": "investigations", "type": "textarea", "label": "Investigations", "required": False, "placeholder": "List investigations..."}]},
                    {"id": "assessment", "title": "Impression / Assessment", "questions": [{"id": "impression", "type": "textarea", "label": "Impression", "required": False, "placeholder": "Describe your impression..."}]},
                    {"id": "plan", "title": "Plan", "questions": [{"id": "plan_details", "type": "textarea", "label": "Plan", "required": False, "placeholder": "Describe the plan..."}]}
                ]
            },
            "red_flags": [
                {"id": "red_flag_silent_chest", "description": "Silent chest - Urgent action required", "severity": "high"},
                {"id": "red_flag_cyanosis", "description": "Cyanosis - Immediate A&E referral", "severity": "high"},
                {"id": "red_flag_exhaustion", "description": "Exhaustion - Severe asthma attack", "severity": "high"}
            ],
            "differentials": ["COPD", "Allergic Rhinitis", "Vocal Cord Dysfunction", "Respiratory Infections", "Gastro-oesophageal Reflux Disease"],
            "safetyNetting": ["Use reliever inhaler if symptoms worsen", "If unable to get relief from medication, call GP", "Follow asthma action plan", "Use peak flow meter daily", "If symptoms are severe and not responding to medication, call 999", "Attend annual asthma reviews"],
            "is_public": True
        }
    ]
    
    for template_data in templates_data:
        # Get or create category
        category = db.query(Category).filter(Category.name == template_data["category"]).first()
        if not category:
            category = Category(name=template_data["category"])
            db.add(category)
            db.commit()
            db.refresh(category)
        
        # Check if template exists - if so, delete and recreate
        existing = db.query(Template).filter(
            Template.title == template_data["title"],
            Template.created_by == admin.id
        ).first()
        
        if existing:
            db.delete(existing)
            db.commit()
            print(f"🔄 Removed old '{template_data['title']}' template")
        
        # Create template with proper structure
        new_template = Template(
            title=template_data["title"],
            description=template_data["description"],
            category=template_data["category"],
            content=template_data["content"],
            is_public=template_data["is_public"],
            created_by=admin.id,
            version=1
        )
        db.add(new_template)
        db.commit()
        db.refresh(new_template)
        print(f"✅ Template '{template_data['title']}' created with questions")
    
    print("\n🎉 All templates seeded successfully!")
    
    # Verify
    templates = db.query(Template).all()
    print(f"\n📊 Total templates in database: {len(templates)}")
    for t in templates:
        print(f"  - {t.title} ({t.category})")
    
    db.close()

if __name__ == "__main__":
    seed_all_templates()