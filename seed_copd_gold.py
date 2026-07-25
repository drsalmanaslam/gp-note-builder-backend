from app.database import SessionLocal
from app.models import User, Template, Category

def seed_copd_gold():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Stable COPD Management - GOLD 2023 ABE",
        "description": "GOLD 2023 ABE classification-based COPD management covering Irish brand options, ICS decision support, vaccination, and long-term management priorities.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Current Status & Exacerbation History",
                "section_type": "history",
                "questions": [
                    {"id": "copdg_exacerbations_year", "type": "number", "label": "Number of Exacerbations in Last Year", "required": True, "placeholder": "e.g., 3"},
                    {"id": "copdg_exacerbations_steroids", "type": "number", "label": "Exacerbations Requiring PO Steroids/Antibiotics", "required": True, "placeholder": "e.g., 2"},
                    {"id": "copdg_hospital_admissions", "type": "single_select", "label": "Hospital Admissions for Exacerbation", "required": True, "options": ["None", "1 admission", "≥2 admissions"]},
                    {"id": "copdg_respiratory_followup", "type": "toggle", "label": "Under Respiratory Follow-up?", "required": True},
                    {"id": "copdg_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Current smoker", "Ex-smoker", "Never smoked"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Smoking cessation is the MOST important intervention in COPD - more than inhalers.", "red_flag_negative": ""},
                    {"id": "copdg_symptom_control", "type": "single_select", "label": "Current Symptom Control", "required": True, "options": ["Well at present", "Symptomatic"]},
                    {"id": "copdg_cat", "type": "number", "label": "CAT Score (0-40)", "required": False, "placeholder": "e.g., 18 (≥10 = high symptom burden)"},
                    {"id": "copdg_breathlessness", "type": "single_select", "label": "Breathlessness Pattern", "required": True, "options": ["SOB only when hurrying (mMRC 1)", "Stops for breath walking on flat (mMRC 2)", "Walks slower than peers (mMRC 2)", "Stops after 100m (mMRC 3)", "Too breathless to leave house (mMRC 4)"]}
                ]
            },
            {
                "title": "Vaccination Status",
                "section_type": "history",
                "questions": [
                    {"id": "copdg_flu", "type": "single_select", "label": "Influenza Vaccine", "required": True, "options": ["Received this year", "Due - advise today"]},
                    {"id": "copdg_pneumo", "type": "single_select", "label": "Pneumococcal Vaccine", "required": True, "options": ["Received within last 5 years", "Due - >5 years since last dose", "Never received"]}
                ]
            },
            {
                "title": "GOLD 2023 ABE Classification",
                "section_type": "assessment",
                "questions": [
                    {"id": "copdg_gold_category", "type": "single_select", "label": "GOLD Category (Symptoms + Exacerbations)", "required": True, "options": ["A: CAT <10, mMRC 0-1, ≤1 exacerbation/year (no admission)", "B: CAT ≥10, mMRC ≥2, ≤1 exacerbation/year (no admission)", "E: ≥2 exacerbations/year OR ≥1 exacerbation requiring admission"]}
                ]
            },
            {
                "title": "Inhaler Therapy by GOLD Category",
                "section_type": "plan",
                "questions": [
                    {"id": "copdg_category_a_rx", "type": "single_select", "label": "Category A Treatment", "required": False, "options": ["Salbutamol PRN (Ventolin/Salamol)", "LABA monotherapy", "LAMA monotherapy", "LABA/LAMA combination (if more symptomatic)", "Not applicable"]},
                    {"id": "copdg_category_b_rx", "type": "single_select", "label": "Category B Treatment", "required": False, "options": ["LABA monotherapy", "LAMA monotherapy", "LABA/LAMA combination", "Not applicable"]},
                    {"id": "copdg_category_e_rx", "type": "single_select", "label": "Category E Treatment", "required": False, "options": ["LABA/LAMA combination", "ICS/LABA/LAMA triple (if eosinophils >0.3)", "Relvar (vilanterol/fluticasone) + Incruse (umeclidinium)", "Not applicable"]}
                ]
            },
            {
                "title": "Irish Brand Selection",
                "section_type": "plan",
                "questions": [
                    {"id": "copdg_laba", "type": "single_select", "label": "LABA (Long-Acting Beta Agonist)", "required": False, "options": ["Serevent (Salmeterol)", "Oxis (Formoterol)", "Onbrez (Indacaterol)", "Striverdi (Olodaterol)", "Not indicated"]},
                    {"id": "copdg_lama", "type": "single_select", "label": "LAMA (Long-Acting Muscarinic Antagonist)", "required": False, "options": ["Eklira (Aclidinium) BD", "Seebri (Glycopyrronium) OD", "Incruse (Umeclidinium) OD - HSE Preferred", "Spiriva (Tiotropium) OD", "Not indicated"]},
                    {"id": "copdg_laba_lama", "type": "single_select", "label": "LABA/LAMA Combination", "required": False, "options": ["Brimica (Aclidinium/Formoterol) BD", "Ultibro (Glycopyrronium/Indacaterol) OD", "Anoro (Umeclidinium/Vilanterol) OD - HSE Preferred", "Spiolto (Tiotropium/Olodaterol) OD", "Not indicated"]},
                    {"id": "copdg_triple", "type": "single_select", "label": "ICS/LAMA/LABA Triple Therapy", "required": False, "options": ["Trelegy (Fluticasone/Umeclidinium/Vilanterol) 1 puff OD - HSE Preferred", "Trixeo (Formoterol/Glycopyrronium/Budesonide) 2 puffs BD", "Not indicated"]},
                    {"id": "copdg_saba", "type": "single_select", "label": "SABA Reliever", "required": False, "options": ["Ventolin (Salbutamol) PRN", "Salamol (Salbutamol) PRN", "Not indicated"]}
                ]
            },
            {
                "title": "ICS Decision Support",
                "section_type": "plan",
                "questions": [
                    {"id": "copdg_ics_indications", "type": "multi_select", "label": "Indications to Consider ICS (Trial 3 Months)", "required": False, "options": ["GOLD E + eosinophils >0.3 x10⁹/L", "Previous secure diagnosis of asthma/atopy", "Substantial FEV1 variation (≥400ml)", "Substantial diurnal PEFR variation (≥20%)", "None - ICS not indicated"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ICS increases pneumonia risk in COPD. Only continue if clinical benefit at 3 months. Discontinue if no benefit.", "red_flag_negative": ""},
                    {"id": "copdg_eosinophils", "type": "number", "label": "Eosinophil Count (x10⁹/L)", "required": False, "placeholder": "e.g., 0.4 (ICS if >0.3 + GOLD E)"},
                    {"id": "copdg_ics_trial", "type": "single_select", "label": "ICS Trial Outcome", "required": False, "options": ["Trial ongoing", "Continued - clinical benefit at 3 months", "Discontinued - no benefit at 3 months", "Not applicable"]}
                ]
            },
            {
                "title": "Long-Term Management Priorities (Ranked by Importance)",
                "section_type": "plan",
                "safety_netting": "Smoking cessation is the MOST important intervention - NRT offered. Vaccinations: flu yearly, pneumococcal every 5 years. Dietician review. Chest physiotherapy. Inhalers are the LEAST important of the five interventions. Ellipta device range (Incruse, Anoro, Trelegy) = HSE preferred - most cost-effective. Atrovent (ipratropium) has fallen out of favour - decreases LAMA effectiveness. ICS increases pneumonia risk - trial 3 months and discontinue if no benefit. DEXA scan, fasting lipids, glucose, QRISK for cardiovascular risk. Reference: GP Evidence - COPD treatment evidence.",
                "questions": [
                    {"id": "copdg_priorities", "type": "multi_select", "label": "Management Priorities (Ranked)", "required": False, "options": ["1. Smoking Cessation - NRT offered", "2. Vaccinations - Flu + Pneumococcal", "3. Dietician Review", "4. Chest Physiotherapy", "5. Inhalers (least important)"]},
                    {"id": "copdg_additional_screening", "type": "multi_select", "label": "Additional Screening", "required": False, "options": ["DEXA Scan (osteoporosis risk)", "Fasting Lipids", "Fasting Glucose / HbA1c", "QRISK Cardiovascular Risk"]},
                    {"id": "copdg_actions", "type": "multi_select", "label": "Actions Today", "required": True, "options": ["Inhaler regimen reviewed/changed", "Vaccination given/updated", "Referral for chest physiotherapy", "Dietician referral", "Smoking cessation support offered", "Bloods ordered", "No change to current management"]},
                    {"id": "copdg_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Routine annual review, 3 months if ICS trial, sooner if exacerbation"}
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
    seed_copd_gold()