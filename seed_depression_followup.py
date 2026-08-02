from app.database import SessionLocal
from app.models import Template, User

def seed_depression_followup():
    db = SessionLocal()
    
    title = "Depression Follow-up"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        db.delete(existing)
        db.commit()
    
    admin = db.query(User).filter(User.role == "admin").first()
    
    template = Template(
        title=title,
        description="Structured follow-up assessment for depression covering PHQ-9 monitoring, medication response, suicide risk assessment, and treatment optimisation.",
        category="Mental Health",
        content={
            "sections": [
                {
                    "title": "Clinical Status Review",
                    "section_type": "history",
                    "questions": [
                        {"id": "dep_fu_interval", "type": "text", "label": "Interval Since Last Review", "required": True, "placeholder": "e.g., 4 weeks"},
                        {"id": "dep_fu_phq9_score", "type": "number", "label": "PHQ-9 Score (Current)", "required": True, "placeholder": "e.g., 12"},
                        {"id": "dep_fu_phq9_previous", "type": "number", "label": "PHQ-9 Score (Previous)", "required": False, "placeholder": "e.g., 18"},
                        {"id": "dep_fu_subjective", "type": "single_select", "label": "Patient's Self-Assessment", "required": True, "options": ["Much better", "Slightly better", "No change", "Slightly worse", "Much worse"]},
                        {"id": "dep_fu_sleep", "type": "single_select", "label": "Sleep", "required": True, "options": ["Improved", "No change", "Worsened"]},
                        {"id": "dep_fu_appetite", "type": "single_select", "label": "Appetite", "required": True, "options": ["Improved", "No change", "Worsened", "Weight gain concern"]},
                        {"id": "dep_fu_energy", "type": "single_select", "label": "Energy Levels", "required": True, "options": ["Improved", "No change", "Worsened"]},
                        {"id": "dep_fu_anhedonia", "type": "toggle", "label": "Persistent Anhedonia?", "required": True},
                        {"id": "dep_fu_concentration", "type": "single_select", "label": "Concentration", "required": True, "options": ["Improved", "No change", "Worsened"]}
                    ]
                },
                {
                    "title": "Suicide Risk Assessment",
                    "section_type": "history",
                    "questions": [
                        {"id": "dep_fu_suicidal_ideation", "type": "toggle", "label": "Suicidal Ideation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suicidal ideation requires urgent risk assessment. Ask about plans, means, and intent.", "red_flag_negative": ""},
                        {"id": "dep_fu_self_harm", "type": "toggle", "label": "Self-Harm Since Last Review?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Self-harm requires urgent assessment. Consider Crisis Team referral.", "red_flag_negative": ""},
                        {"id": "dep_fu_hopelessness", "type": "toggle", "label": "Feelings of Hopelessness?", "required": True},
                        {"id": "dep_fu_protective_factors", "type": "text", "label": "Protective Factors", "required": False, "placeholder": "e.g., Family support, children, pets, work"}
                    ]
                },
                {
                    "title": "Medication Review",
                    "section_type": "history",
                    "questions": [
                        {"id": "dep_fu_antidepressant", "type": "text", "label": "Current Antidepressant & Dose", "required": True, "placeholder": "e.g., Sertraline 100mg OD"},
                        {"id": "dep_fu_duration", "type": "text", "label": "Duration on Current Dose", "required": True, "placeholder": "e.g., 6 weeks"},
                        {"id": "dep_fu_adherence", "type": "single_select", "label": "Medication Adherence", "required": True, "options": ["Taking regularly", "Misses occasional doses", "Misses frequently", "Stopped taking"]},
                        {"id": "dep_fu_side_effects", "type": "multi_select", "label": "Side Effects", "required": False, "options": ["Nausea", "Headache", "Sexual dysfunction", "Weight gain", "Insomnia", "Drowsiness", "Anxiety/Agitation", "None"]},
                        {"id": "dep_fu_side_effect_severity", "type": "single_select", "label": "Side Effect Impact", "required": False, "options": ["None", "Mild - tolerable", "Moderate - bothersome", "Severe - considering stopping"]}
                    ]
                },
                {
                    "title": "Biological & Lifestyle",
                    "section_type": "history",
                    "questions": [
                        {"id": "dep_fu_alcohol", "type": "single_select", "label": "Alcohol Use", "required": True, "options": ["None", "Within limits", "Excess", "Using to cope"]},
                        {"id": "dep_fu_substances", "type": "toggle", "label": "Recreational Drug Use?", "required": False},
                        {"id": "dep_fu_exercise", "type": "single_select", "label": "Physical Activity", "required": True, "options": ["Regular exercise", "Some activity", "Sedentary"]},
                        {"id": "dep_fu_bloods", "type": "toggle", "label": "Bloods Checked? (FBC, TFTs, LFTs, B12/Folate)", "required": False}
                    ]
                },
                {
                    "title": "Assessment & Plan",
                    "section_type": "assessment",
                    "differentials": [
                        "Treatment-responsive depression - continue current management",
                        "Partial response - optimise dose or augment",
                        "Treatment-resistant depression - consider switch/augmentation",
                        "Bipolar depression (screen for past mania/hypomania)",
                        "Secondary to physical illness (hypothyroidism, anaemia)"
                    ],
                    "questions": [
                        {"id": "dep_fu_response", "type": "single_select", "label": "Treatment Response (PHQ-9 change)", "required": True, "options": ["Remission (PHQ-9 <5)", "Good response (≥50% reduction)", "Partial response (25-50% reduction)", "Minimal response (<25% reduction)", "Deterioration"]},
                        {"id": "dep_fu_plan", "type": "single_select", "label": "Management Plan", "required": True, "options": ["Continue current treatment", "Increase dose", "Switch antidepressant", "Add augmentation (e.g., Mirtazapine, Quetiapine)", "Refer to Psychiatry", "Refer to Crisis Team", "Psychological therapy referral", "Combined approach"]},
                        {"id": "dep_fu_next_dose", "type": "text", "label": "New Prescription", "required": False, "placeholder": "e.g., Sertraline 150mg OD"},
                        {"id": "dep_fu_psychology", "type": "toggle", "label": "Psychological Therapy Referral?", "required": False},
                        {"id": "dep_fu_sick_note", "type": "toggle", "label": "Sick Note Required?", "required": False}
                    ]
                },
                {
                    "title": "Safety Netting & Follow-up",
                    "section_type": "plan",
                    "safety_netting": "If you experience worsening mood, thoughts of self-harm or suicide, contact your GP immediately, call 111, or attend A&E. Crisis line: 0800 689 5652 (24/7). Do not stop antidepressants abruptly - this can cause discontinuation syndrome. Return if side effects become intolerable. Continue treatment for at least 6 months after remission to prevent relapse.",
                    "questions": [
                        {"id": "dep_fu_next_review", "type": "text", "label": "Next Review", "required": True, "placeholder": "e.g., 4 weeks for dose change, 8-12 weeks if stable"},
                        {"id": "dep_fu_crisis_plan", "type": "toggle", "label": "Crisis Plan Discussed?", "required": True},
                        {"id": "dep_fu_red_flags", "type": "toggle", "label": "Red Flags Explained?", "required": True}
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
    seed_depression_followup()