from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_ndls_group2():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "GP-Related Topics").first()
    if not category: category = Category(name="GP-Related Topics"); db.add(category); db.commit()

    t = {
        "title": "Medical for Driving Licence - Group 2 (Bus/Truck)",
        "description": "NDLS Group 2 driving medical covering higher vision standards (optician-assessed), neurological/cardiac screening, and substance-related restrictions for commercial drivers.",
        "category": "GP-Related Topics",
        "content": {"sections": [
            {
                "title": "Licence & General Fitness",
                "section_type": "history",
                "questions": [
                    {"id": "g2_licence", "type": "single_select", "label": "Licence Category", "required": True, "options": ["Group 2 (Bus/Truck)", "Group 2 + Group 1"]},
                    {"id": "g2_fit_well", "type": "toggle", "label": "Patient Feels Fit and Well to Drive?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: If patient does NOT feel fit = do NOT certify. Investigate cause.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Neurological & Cardiac Screen",
                "section_type": "history",
                "questions": [
                    {"id": "g2_seizures", "type": "toggle", "label": "History of Seizures / Epilepsy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Group 2 = no unprovoked seizures since age 8, or ≥10 years seizure-free off meds. Stricter than Group 1.", "red_flag_negative": ""},
                    {"id": "g2_tia", "type": "toggle", "label": "History of TIA / Stroke?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Group 2 post-TIA/Stroke = may be permanently unfit. Requires specialist assessment + NDLS notification.", "red_flag_negative": ""},
                    {"id": "g2_heart", "type": "toggle", "label": "Heart Problems? (Angina, MI, Arrhythmia, Pacemaker, ICD)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Group 2 cardiac standards are stricter. MI = 6 weeks off. ICD = permanently unfit. Refer NDLS cardiovascular guidelines.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Sleep Apnoea & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "g2_osa", "type": "toggle", "label": "History of Sleep Apnoea?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Group 2 OSA = must be compliant with CPAP with objective evidence of control. Stricter than Group 1.", "red_flag_negative": ""},
                    {"id": "g2_cpap", "type": "toggle", "label": "Using CPAP? (If OSA)", "required": False},
                    {"id": "g2_meds_impair", "type": "toggle", "label": "Any Medication That Impairs Driving? (Patient's Own Assessment)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: If medication causes drowsiness = advise NOT to drive. Document clearly.", "red_flag_negative": ""},
                    {"id": "g2_benzos", "type": "toggle", "label": "Taking Benzodiazepines?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Drug test positive for benzodiazepines = must be clear for 6 months + letter from treatment centre confirming negative urine toxicology.", "red_flag_negative": ""},
                    {"id": "g2_opiates", "type": "toggle", "label": "Taking Opiates?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Drug test positive for opiates = must be clear for 6 months + letter from treatment centre.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "g2_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 128/82", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP ≥180/100 = unfit for Group 2. Treat and reassess.", "red_flag_negative": ""},
                    {"id": "g2_hr", "type": "number", "label": "Pulse (bpm)", "required": True, "placeholder": "e.g., 72"},
                    {"id": "g2_neck", "type": "single_select", "label": "Neck Movement", "required": True, "options": ["Full Range", "Restricted"]},
                    {"id": "g2_chest", "type": "single_select", "label": "Chest Examination", "required": False, "options": ["Clear", "Abnormal"]},
                    {"id": "g2_cvs", "type": "single_select", "label": "Cardiovascular Examination", "required": True, "options": ["Normal", "Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal CVS = investigate before certifying. Group 2 standards are stricter.", "red_flag_negative": ""},
                    {"id": "g2_limb_strength", "type": "single_select", "label": "Limb Strength", "required": True, "options": ["Normal", "Reduced - May Affect Fitness"]},
                    {"id": "g2_contraindications", "type": "toggle", "label": "Contraindications Identified?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Contraindications present = do NOT certify. Document reason clearly.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Vision - Group 2 Standard (Optician-Assessed)",
                "section_type": "assessment",
                "questions": [
                    {"id": "g2_vision_note", "type": "toggle", "label": "GP Note: Vision MUST be Formally Assessed by Optician for Group 2 (NOT by GP)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Vision for Group 2 must be signed off by optician. GP does NOT complete this section.", "red_flag_negative": ""},
                    {"id": "g2_vision_standard", "type": "single_select", "label": "Group 2 Vision Standard (Reference Only)", "required": False, "options": ["Minimum: 6/7.5 Better Eye + 6/60 Other Eye (Higher Than Group 1 6/12 Binocular)", "Optician Report Pending", "Meets Standard (Per Optician)", "Does NOT Meet Standard"]}
                ]
            },
            {
                "title": "Assessment & Certification",
                "section_type": "assessment",
                "differentials": [
                    "Medically Fit - Group 2 (Awaiting Optician Vision Report)",
                    "Medically Fit - Group 2 (Optician Report Confirmed)",
                    "NOT Fit - Medical Contraindication",
                    "NOT Fit - Visual Standard Not Met",
                    "NOT Fit - Substance-Related (6-Month Clearance Required)",
                    "Requires Further Specialist Assessment"
                ],
                "questions": [
                    {"id": "g2_fit", "type": "single_select", "label": "Fitness to Drive", "required": True, "options": ["FIT - Group 2 (Awaiting Optician)", "FIT - Group 2 (Optician Confirmed)", "NOT FIT - Medical Reason", "NOT FIT - Visual Standard", "NOT FIT - Substance-Related", "Requires Further Assessment"]}
                ]
            },
            {
                "title": "Plan & Certification Details",
                "section_type": "plan",
                "safety_netting": "NDLS Medical Form: https://www.ndls.ie/images/Documents/Forms/171315_NDLS_Medical_Form_JAN_2022_WEB_HR.pdf. RCSI Guide: https://www.ndls.ie/images/GuideToCompletingD501MedicalReport.pdf. Group 2 vision: minimum 6/7.5 better eye + 6/60 other eye (higher than Group 1). Vision MUST be formally assessed and signed off by optician, NOT GP. Patient to attend optician for Group 2 section. Once optician report returned + meets standard = form ready for collection. Scan optician report to patient file. Advise: if ever drowsy after medication, do NOT drive. Substance restriction: benzodiazepines/opiates positive = 6 months clear + treatment centre letter. Group 2 standards are stricter than Group 1 for seizures, cardiac, OSA, and vision.",
                "questions": [
                    {"id": "g2_optician", "type": "toggle", "label": "Patient Advised to Attend Optician for Group 2 Vision Section?", "required": True},
                    {"id": "g2_scan_report", "type": "toggle", "label": "Optician Report to be Scanned to File When Returned?", "required": False},
                    {"id": "g2_medication_warning", "type": "toggle", "label": "Advised: If Drowsy After Medication, Do NOT Drive?", "required": True},
                    {"id": "g2_followup", "type": "text", "label": "Follow-up / Review", "required": False, "placeholder": "e.g., Collect form once optician report returned, recertify per NDLS schedule"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_ndls_group2()