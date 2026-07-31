from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_influenza():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Influenza",
        "description": "Focused assessment for influenza covering Tamiflu (oseltamivir) indication criteria per HSE guidance, symptomatic management, and infection control advice.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "flu_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Sudden onset fever, severe malaise, and cough for 24 hours"},
                    {"id": "flu_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 24 hours (Sudden onset = typical)"},
                    {"id": "flu_symptoms", "type": "multi_select", "label": "Core Symptoms", "required": True, "options": ["Cough", "Pyrexia / feverish", "Severe malaise (hit by train sensation)", "Headache", "Tiredness", "Muscle pain / myalgia", "Limb / joint pain", "Sore throat", "Nasal congestion", "Sneezing", "Loss of appetite"]},
                    {"id": "flu_diarrhoea", "type": "toggle", "label": "Diarrhoea?", "required": False},
                    {"id": "flu_diarrhoea_episodes", "type": "number", "label": "Number of Diarrhoea Episodes", "required": False, "placeholder": "e.g., 3"},
                    {"id": "flu_resp_red_flags", "type": "multi_select", "label": "Respiratory Red Flags", "required": True, "options": ["Shortness of breath", "Wheeze", "Chest pain", "Chest tightness", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB/chest pain = ?pneumonia, ARDS. Examine + consider CXR/admission.", "red_flag_negative": ""},
                    {"id": "flu_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Current smoker", "Ex-smoker", "Never smoked"]},
                    {"id": "flu_asthma", "type": "toggle", "label": "Asthma History?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Asthmatic + influenza = risk of exacerbation. Ensure using preventer. Consider Tamiflu.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "flu_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Looks clinically well", "Looks clinically unwell / toxic - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Toxic appearance = ?severe influenza, sepsis. Consider admission.", "red_flag_negative": ""},
                    {"id": "flu_ent_tm", "type": "single_select", "label": "Tympanic Membranes", "required": False, "options": ["Normal B/L", "Abnormal"]},
                    {"id": "flu_ent_pharynx", "type": "single_select", "label": "Pharynx", "required": False, "options": ["Normal", "Erythematous"]},
                    {"id": "flu_ent_lymph", "type": "toggle", "label": "Lymphadenopathy?", "required": False},
                    {"id": "flu_ent_coryzal", "type": "toggle", "label": "Coryzal?", "required": False},
                    {"id": "flu_ent_turbinates", "type": "single_select", "label": "Nasal Turbinates", "required": False, "options": ["Normal", "Abnormal / swollen"]},
                    {"id": "flu_sinus_tenderness", "type": "toggle", "label": "Maxillary / Frontal Sinus Tenderness?", "required": False},
                    {"id": "flu_resp", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Air entry equal B/L, vesicular BS, no added sounds", "Reduced air entry", "Added sounds (crackles/wheeze) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Crackles = ?pneumonia. Wheeze = ?exacerbation. CXR + consider admission.", "red_flag_negative": ""},
                    {"id": "flu_hydration", "type": "single_select", "label": "Hydration", "required": True, "options": ["Mucous membranes moist - well hydrated", "Mucous membranes dry - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Dehydrated = ?need IV fluids. Especially elderly/children.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Tamiflu (Oseltamivir) - Indication Check (HSE Guidance)",
                "section_type": "assessment",
                "questions": [
                    {"id": "flu_particularly_unwell", "type": "toggle", "label": "Patient PARTICULARLY UNWELL? (Required for Tamiflu Consideration)", "required": True},
                    {"id": "flu_risk_factors", "type": "multi_select", "label": "Risk Factors for Tamiflu (Need ≥1 + Particularly Unwell)", "required": True, "options": ["Chronic respiratory condition (incl. asthma)", "Chronic heart disease", "Chronic kidney disease", "Chronic liver disease", "Chronic neurological disease", "Immunosuppression", "Diabetes", "Age >65 years", "Age <2 years", "BMI ≥40", "Pregnancy (incl. up to 2 weeks post-partum)", "Down syndrome", "Moderate cerebral palsy or intellectual disability", "None of the above"]},
                    {"id": "flu_tamiflu_indicated", "type": "toggle", "label": "Tamiflu Indicated? (Particularly Unwell + ≥1 Risk Factor)", "required": True}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Influenza (Seasonal)",
                    "COVID-19",
                    "Viral URTI / Common Cold",
                    "Bacterial Pneumonia (RED FLAG - crackles, hypoxia)",
                    "Sepsis (RED FLAG - toxic, hypotensive)"
                ],
                "questions": [
                    {"id": "flu_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Influenza - Mild/Moderate (No Tamiflu Indicated)", "Influenza - With Risk Factors (Tamiflu Indicated)", "Influenza - Severe (?Admission)", "Suspected Pneumonia - RED FLAG"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: shortness of breath, chest pain, confusion, or symptoms worsen significantly. Red flags discussed: SOB, chest pain, signs of deterioration. Expected course: symptoms typically peak at 2-3 days, most people feel better within 5-8 days. Cough and general tiredness may persist for 2-3 weeks. Symptomatic treatment: Bisolvon (cough), Otrivine nasal spray (congestion), Paracetamol/Ibuprofen (fever/pain). Infection control: stay at home while unwell. Avoid contact with vulnerable individuals. Tamiflu (oseltamivir): only if particularly unwell AND ≥1 risk factor. Must be started within 48 hours of symptom onset for maximum benefit. Reference: HSE seasonal influenza guidance.",
                "questions": [
                    {"id": "flu_symptomatic", "type": "multi_select", "label": "Symptomatic Treatment", "required": False, "options": ["Bisolvon (Cough Preparation)", "Otrivine Nasal Spray", "Paracetamol PRN", "Ibuprofen PRN", "None"]},
                    {"id": "flu_tamiflu_prescribed", "type": "toggle", "label": "Tamiflu (Oseltamivir) 75mg BD for 5 Days Prescribed?", "required": False},
                    {"id": "flu_infection_control", "type": "toggle", "label": "Infection Control: Stay at Home While Unwell Advised?", "required": True},
                    {"id": "flu_red_flags_discussed", "type": "toggle", "label": "Red Flags Discussed? (SOB, Chest Pain, Deterioration)", "required": True},
                    {"id": "flu_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., No follow-up required - self-limiting, return if red flags, or review if not improving in 5-8 days"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_influenza()