from app.database import SessionLocal
from app.models import User, Template, Category

def seed_chronic_cough_extended():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Chronic Cough (>8 Weeks) - BTS Guideline",
        "description": "BTS guideline-based assessment for chronic cough >8 weeks covering the three most common causes: cough variant asthma, GORD, and upper airway disease, with targeted treatment trials.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Cough History",
                "section_type": "history",
                "questions": [
                    {"id": "cc2_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Persistent dry cough for 10 weeks"},
                    {"id": "cc2_duration", "type": "single_select", "label": "Duration", "required": True, "options": [">8 weeks (chronic cough - investigate)", ">3 weeks (subacute)", "<3 weeks (acute)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Cough >8 weeks = MANDATORY CXR + spirometry. BTS guideline.", "red_flag_negative": ""},
                    {"id": "cc2_character", "type": "single_select", "label": "Cough Character", "required": True, "options": ["Non-productive (dry)", "Productive (sputum)"]},
                    {"id": "cc2_associated", "type": "multi_select", "label": "Associated Respiratory Symptoms", "required": True, "options": ["Minor wheeze", "SOB on exertion", "None"]}
                ]
            },
            {
                "title": "Cough Patterns & Triggers (Asthma Screen)",
                "section_type": "history",
                "questions": [
                    {"id": "cc2_patterns", "type": "multi_select", "label": "Cough Pattern / Triggers (?Cough Variant Asthma)", "required": True, "options": ["Nocturnal cough", "After exercise", "After allergen exposure", "None of these patterns"]},
                    {"id": "cc2_red_flags", "type": "multi_select", "label": "Red Flag Screen", "required": True, "options": ["Chest pain", "Haemoptysis", "Weight loss", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemoptysis + weight loss + cough = ?lung cancer. Urgent CXR + 2WW respiratory.", "red_flag_negative": ""},
                    {"id": "cc2_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Current / ex-smoker", "Non-smoker"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Smoker + cough >3 weeks = ?COPD, lung cancer. CXR mandatory.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Medication & Exposure Review",
                "section_type": "history",
                "questions": [
                    {"id": "cc2_meds", "type": "multi_select", "label": "Causative Medications", "required": True, "options": ["ACE Inhibitor (Ramipril, Lisinopril)", "Sitagliptin (DPP-4 inhibitor)", "Neither"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ACEi-induced cough = class effect. Trial cessation for 4 weeks. Sitagliptin can also cause cough.", "red_flag_negative": ""},
                    {"id": "cc2_exposures", "type": "multi_select", "label": "Exposure History", "required": True, "options": ["Workplace sensitisers", "Dust exposure at home", "Chemical exposure at home", "Pet exposure at home", "None"]}
                ]
            },
            {
                "title": "Upper Airway / GORD Screen",
                "section_type": "history",
                "questions": [
                    {"id": "cc2_upper_airway", "type": "multi_select", "label": "Upper Airway / Rhinitis Screen (?Post-Nasal Drip)", "required": True, "options": ["Nasal congestion", "Sinusitis / facial pain", "Sensation of secretions draining into posterior pharynx", "None present"]},
                    {"id": "cc2_gord", "type": "multi_select", "label": "GORD Screen", "required": True, "options": ["Cough on eating / postprandial", "Heartburn / acid reflux", "Waterbrash / regurgitation", "None present"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "cc2_general", "type": "single_select", "label": "General Examination", "required": True, "options": ["No clubbing", "Clubbing present - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Clubbing + cough = ?lung cancer, pulmonary fibrosis. Urgent CXR.", "red_flag_negative": ""},
                    {"id": "cc2_ent", "type": "multi_select", "label": "ENT Examination", "required": False, "options": ["Turbinates normal", "No nasal polyps", "No post-nasal drip", "Abnormal finding"]},
                    {"id": "cc2_resp", "type": "single_select", "label": "Respiratory Examination", "required": True, "options": ["Equal air entry B/L, vesicular BS, no added sounds", "Reduced air entry", "Added sounds present"]},
                    {"id": "cc2_abdo", "type": "single_select", "label": "Abdominal Examination", "required": False, "options": ["Soft, non-tender", "Tenderness present"]}
                ]
            },
            {
                "title": "Assessment (BTS Guidelines)",
                "section_type": "assessment",
                "differentials": [
                    "Cough Variant Asthma / Eosinophilic Bronchitis (~30% of cough clinic referrals)",
                    "GORD-Related Cough (5-41% of referrals)",
                    "Upper Airway Cough Syndrome (Post-Nasal Drip / Allergic Rhinitis)",
                    "ACE Inhibitor-Induced Cough",
                    "COPD",
                    "Bronchiectasis",
                    "Lung Cancer (RED FLAG)",
                    "Interstitial Lung Disease",
                    "Pertussis (Whooping Cough)"
                ],
                "questions": [
                    {"id": "cc2_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Cough Variant Asthma / Eosinophilic Bronchitis", "GORD-Related Cough Suspected", "Upper Airway Cough Syndrome Suspected", "ACE Inhibitor-Induced Cough", "Further Investigation Required - Cause Unclear", "Red Flags Present - Urgent CXR + 2WW"]}
                ]
            },
            {
                "title": "Investigations (All Patients with Cough >8 Weeks)",
                "section_type": "plan",
                "questions": [
                    {"id": "cc2_cxr", "type": "toggle", "label": "Chest X-Ray (MANDATORY for cough >8 weeks)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: CXR is MANDATORY for all patients with cough >8 weeks. BTS guideline.", "red_flag_negative": ""},
                    {"id": "cc2_spirometry", "type": "toggle", "label": "PFTs / Spirometry Requested?", "required": True},
                    {"id": "cc2_fbc", "type": "toggle", "label": "FBC? (Eosinophilia = ?asthma/eosinophilic bronchitis)", "required": False},
                    {"id": "cc2_referral", "type": "toggle", "label": "Refer Respiratory OPD for PFTs?", "required": False}
                ]
            },
            {
                "title": "Trial of Therapy (Based on Suspected Cause)",
                "section_type": "plan",
                "safety_netting": "Return immediately if: haemoptysis, chest pain, weight loss, or worsening SOB. CXR is MANDATORY for all patients with cough >8 weeks. BTS: three most common causes = cough variant asthma/eosinophilic bronchitis (~30%), GORD (5-41%), upper airway disease (post-nasal drip). If ACEi-induced: trial cessation for 4 weeks. Asthma trial: inhaled beclomethasone for 4-8 weeks. GORD trial: Lansoprazole 15-30mg BD for ≥8 weeks ± Metoclopramide 10mg TDS. Upper airway: topical nasal corticosteroid for 1 month. Review after trial. If no improvement or red flags: respiratory referral.",
                "questions": [
                    {"id": "cc2_asthma_trial", "type": "single_select", "label": "Cough Variant Asthma / Eosinophilic Bronchitis Trial", "required": False, "options": ["Inhaled Beclomethasone (Clenil) 200mcg BD for 4-8 weeks", "Not indicated - no asthma features"]},
                    {"id": "cc2_gord_trial", "type": "single_select", "label": "GORD Trial (≥8 Weeks)", "required": False, "options": ["Lansoprazole 15-30mg BD for ≥8 weeks", "Add Metoclopramide 10mg TDS", "Not indicated - no GORD features"]},
                    {"id": "cc2_upper_airway_trial", "type": "single_select", "label": "Upper Airway Trial (1 Month)", "required": False, "options": ["Topical Nasal Corticosteroid (Fluticasone/Mometasone) for 1 month", "Not indicated - no upper airway features"]},
                    {"id": "cc2_acei_trial", "type": "toggle", "label": "Trial ACEi Cessation? (Stop for 4 weeks + review)", "required": False},
                    {"id": "cc2_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review after 4-8 week trial, await CXR/PFTs, sooner if red flags"}
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
    seed_chronic_cough_extended()