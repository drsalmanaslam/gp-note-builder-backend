from app.database import SessionLocal
from app.models import User, Template, Category

def seed_asthma_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Asthma Review",
        "description": "Structured asthma review covering symptom control, inhaler technique, exacerbations, and stepwise management.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Current Status",
                "section_type": "history",
                "questions": [
                    {"id": "ast_presenting_complaint", "type": "text", "label": "Reason for Review", "required": True, "placeholder": "e.g., Routine annual review / worsening symptoms"},
                    {"id": "ast_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 35"},
                    {"id": "ast_diagnosis_year", "type": "text", "label": "Year Diagnosed", "required": False, "placeholder": "e.g., 2010"},
                    {"id": "ast_current_step", "type": "single_select", "label": "Current BTS/SIGN Step", "required": True, "options": ["Step 1 - SABA only", "Step 2 - Low-dose ICS", "Step 3 - Low-dose ICS + LABA", "Step 4 - Medium-dose ICS + LABA", "Step 5 - High-dose ICS + LABA + specialist"]}
                ]
            },
            {
                "title": "Symptom Control (Based on Last 4 Weeks)",
                "section_type": "history",
                "questions": [
                    {"id": "ast_daytime_symptoms", "type": "single_select", "label": "Daytime Symptoms >2x/week?", "required": True, "options": ["No", "Yes"]},
                    {"id": "ast_night_waking", "type": "single_select", "label": "Night Waking Due to Asthma?", "required": True, "options": ["No", "Yes"]},
                    {"id": "ast_reliever_use", "type": "single_select", "label": "Reliever Use >2x/week?", "required": True, "options": ["No", "Yes"]},
                    {"id": "ast_activity_limitation", "type": "single_select", "label": "Activity Limitation Due to Asthma?", "required": True, "options": ["No", "Yes"]},
                    {"id": "ast_control_level", "type": "single_select", "label": "Overall Control (GINA)", "required": True, "options": ["Well-controlled (0 of above)", "Partially controlled (1-2 of above)", "Uncontrolled (3-4 of above)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Uncontrolled asthma = step up treatment. If already on Step 4-5 = refer respiratory.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Current Medications & Adherence",
                "section_type": "history",
                "questions": [
                    {"id": "ast_preventer", "type": "text", "label": "Preventer Inhaler (ICS/LABA)", "required": True, "placeholder": "e.g., Fostair 100/6 2 puffs BD"},
                    {"id": "ast_reliever", "type": "text", "label": "Reliever Inhaler", "required": True, "placeholder": "e.g., Salbutamol 100mcg PRN"},
                    {"id": "ast_adherence", "type": "single_select", "label": "Adherence to Preventer", "required": True, "options": ["Excellent - takes daily", "Good - misses occasionally", "Poor - frequently misses", "Not taking preventer"]},
                    {"id": "ast_inhaler_technique", "type": "single_select", "label": "Inhaler Technique", "required": True, "options": ["Good", "Needs improvement - re-educated today", "Poor - spacer needed", "Not checked today"]},
                    {"id": "ast_spacer", "type": "toggle", "label": "Using Spacer?", "required": False},
                    {"id": "ast_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never smoked", "Ex-smoker", "Current smoker"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Smoking reduces ICS efficacy and accelerates lung function decline. Smoking cessation referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Exacerbations & Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "ast_exacerbations_12m", "type": "single_select", "label": "Exacerbations in Last 12 Months?", "required": True, "options": ["None", "1 - GP treated", "2 or more - GP treated", "ED attendance (no admission)", "Hospital admission", "ICU admission"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe exacerbations requiring hospital/ICU = refer respiratory. ≥2 courses oral steroids/year = step up.", "red_flag_negative": ""},
                    {"id": "ast_ocs_courses", "type": "number", "label": "Number of Oral Steroid Courses in 12 Months", "required": False, "placeholder": "e.g., 2"},
                    {"id": "ast_trigger_infections", "type": "toggle", "label": "Exacerbations Triggered by Viral Infections?", "required": False},
                    {"id": "ast_trigger_allergy", "type": "toggle", "label": "Exacerbations Triggered by Allergens?", "required": False},
                    {"id": "ast_trigger_exercise", "type": "toggle", "label": "Exercise-Induced Symptoms?", "required": False},
                    {"id": "ast_peak_flow", "type": "number", "label": "Peak Flow Today (L/min)", "required": False, "placeholder": "e.g., 420"},
                    {"id": "ast_best_peak_flow", "type": "number", "label": "Best Ever Peak Flow (L/min)", "required": False, "placeholder": "e.g., 520"}
                ]
            },
            {
                "title": "Comorbidities & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "ast_allergic_rhinitis", "type": "toggle", "label": "Allergic Rhinitis / Hay Fever?", "required": True},
                    {"id": "ast_eczema", "type": "toggle", "label": "Eczema / Atopy?", "required": False},
                    {"id": "ast_gerd", "type": "toggle", "label": "GORD / Acid Reflux?", "required": False},
                    {"id": "ast_obesity", "type": "toggle", "label": "Obesity? (BMI >30)", "required": False},
                    {"id": "ast_anxiety_depression", "type": "toggle", "label": "Anxiety / Depression?", "required": False},
                    {"id": "ast_aspirin_sensitivity", "type": "toggle", "label": "Aspirin / NSAID Sensitivity?", "required": False},
                    {"id": "ast_nasal_polyps", "type": "toggle", "label": "Nasal Polyps?", "required": False},
                    {"id": "ast_occupational", "type": "toggle", "label": "Occupational Exposure? (Dust, chemicals, animals)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ast_general", "type": "single_select", "label": "General Appearance", "required": True, "options": ["Well - no respiratory distress", "Mild SOB at rest", "Using accessory muscles", "Unable to speak in sentences - EMERGENCY"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute severe asthma = emergency. Immediate transfer to hospital.", "red_flag_negative": ""},
                    {"id": "ast_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": False, "placeholder": "e.g., 16"},
                    {"id": "ast_o2", "type": "number", "label": "SpO2 (%)", "required": False, "placeholder": "e.g., 97", "is_red_flag": True, "red_flag_positive": "RED FLAG: SpO2 <92% = severe/life-threatening asthma. Emergency admission.", "red_flag_negative": ""},
                    {"id": "ast_hr", "type": "number", "label": "Heart Rate (bpm)", "required": False, "placeholder": "e.g., 82"},
                    {"id": "ast_chest_auscultation", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear - normal vesicular", "Wheeze - expiratory", "Wheeze - inspiratory + expiratory", "Silent chest (ominous!)", "Crackles"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Silent chest = life-threatening asthma. Emergency. No wheeze = no air entry.", "red_flag_negative": ""},
                    {"id": "ast_pursed_lip", "type": "toggle", "label": "Pursed Lip Breathing / Prolonged Expiration?", "required": False},
                    {"id": "ast_nasal_polyps_exam", "type": "toggle", "label": "Nasal Polyps Visible?", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Asthma - Well Controlled",
                    "Asthma - Partially Controlled (step up)",
                    "Asthma - Uncontrolled (step up + ?refer)",
                    "Acute Severe Asthma (EMERGENCY)",
                    "Life-Threatening Asthma (EMERGENCY)",
                    "COPD (smokers, older onset)",
                    "Vocal Cord Dysfunction",
                    "GORD-Related Cough/Wheeze",
                    "Heart Failure (cardiac wheeze)",
                    "Allergic Bronchopulmonary Aspergillosis (ABPA)",
                    "Eosinophilic Granulomatosis with Polyangiitis (EGPA / Churg-Strauss)"
                ],
                "questions": [
                    {"id": "ast_diagnosis_impression", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Asthma - well controlled", "Asthma - partially controlled", "Asthma - uncontrolled", "Acute severe asthma - EMERGENCY", "Suspected alternative diagnosis"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: reliever needed >every 4 hours, symptoms worsen rapidly, peak flow <50% best, difficulty speaking, or SpO2 <92%. Written asthma action plan provided. Ensure influenza and pneumococcal vaccines up to date. Annual review minimum. If on high-dose ICS: monitor for adrenal suppression. Check inhaler technique at every review. If smoking: refer to cessation service. If occupational asthma suspected: refer respiratory/occupational health. For acute severe asthma: O2, nebulised salbutamol, oral prednisolone 40-50mg, transfer to hospital.",
                "questions": [
                    {"id": "ast_plan", "type": "single_select", "label": "Management Decision", "required": True, "options": ["Continue same treatment", "Step up (increase ICS dose or add LABA)", "Step down (well-controlled for 3+ months)", "Add on therapy (LTRA / LAMA)", "Refer respiratory specialist", "Emergency admission", "Trial of MART regimen"]},
                    {"id": "ast_new_preventer", "type": "text", "label": "New Preventer Prescribed", "required": False, "placeholder": "e.g., Fostair 200/6 2 puffs BD"},
                    {"id": "ast_ocs_prescribed", "type": "toggle", "label": "Oral Steroids Prescribed? (Prednisolone 40-50mg for 5-7 days)", "required": False},
                    {"id": "ast_antibiotics", "type": "toggle", "label": "Antibiotics? (If infective exacerbation)", "required": False},
                    {"id": "ast_action_plan", "type": "toggle", "label": "Written Asthma Action Plan Given?", "required": True},
                    {"id": "ast_inhaler_technique_checked", "type": "toggle", "label": "Inhaler Technique Checked & Corrected?", "required": True},
                    {"id": "ast_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4 weeks if step up, 3 months if stable, annual review"}
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
    seed_asthma_review()