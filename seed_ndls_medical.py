from app.database import SessionLocal
from app.models import User, Template, Category

def seed_ndls_medical():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "General").first()
    if not category: category = Category(name="General"); db.add(category); db.commit()

    t = {
        "title": "NDLS Medical Form - Driving Fitness",
        "description": "NDLS medical fitness to drive assessment covering Group 1 licence requirements, vision standards, neurological/cardiac screening, and substance-related restrictions.",
        "category": "General",
        "content": {"sections": [
            {
                "title": "Licence & General Fitness",
                "section_type": "history",
                "questions": [
                    {"id": "ndls_licence", "type": "single_select", "label": "Licence Category", "required": True, "options": ["Group 1 (Car/Motorcycle)", "Group 2 (Bus/Truck)"]},
                    {"id": "ndls_fit_well", "type": "toggle", "label": "Patient Feels Fit and Well to Drive?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: If patient does NOT feel fit = do NOT certify. Investigate cause.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Neurological & Cardiac Screen",
                "section_type": "history",
                "questions": [
                    {"id": "ndls_seizures", "type": "toggle", "label": "History of Seizures / Epilepsy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Seizures = must meet NDLS criteria (≥1 year seizure-free, or sleep-only seizures ≥1 year). Refer to NDLS guidelines.", "red_flag_negative": ""},
                    {"id": "ndls_heart", "type": "toggle", "label": "Heart Problems? (Angina, Arrhythmia, Pacemaker, ICD)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cardiac conditions may affect driving fitness. Refer to NDLS cardiovascular guidelines.", "red_flag_negative": ""},
                    {"id": "ndls_tia", "type": "toggle", "label": "History of TIA / Stroke?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: TIA/Stroke = 1 month off driving. Must inform NDLS. Neurology assessment may be required.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Sleep Apnoea & Mobility",
                "section_type": "history",
                "questions": [
                    {"id": "ndls_osa", "type": "toggle", "label": "History of Sleep Apnoea?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: OSA = must be compliant with CPAP + no excessive daytime somnolence. If untreated/severe = unfit.", "red_flag_negative": ""},
                    {"id": "ndls_cpap", "type": "toggle", "label": "Using CPAP? (If OSA)", "required": False},
                    {"id": "ndls_mobility", "type": "multi_select", "label": "Mobility Issues?", "required": True, "options": ["Mobility Issues", "Neck Issues (Limited Range)", "Limb Prostheses", "None"]},
                    {"id": "ndls_adaptations", "type": "toggle", "label": "Vehicle Adaptations Required?", "required": False}
                ]
            },
            {
                "title": "Vision",
                "section_type": "history",
                "questions": [
                    {"id": "ndls_glasses", "type": "toggle", "label": "Wears Glasses / Contact Lenses?", "required": True},
                    {"id": "ndls_last_checked", "type": "text", "label": "Date Vision Last Checked (If Glasses/Contacts)", "required": False, "placeholder": "e.g., 6 months ago"},
                    {"id": "ndls_colour_vision", "type": "toggle", "label": "Colour Vision Issues?", "required": False}
                ]
            },
            {
                "title": "Driving History & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "ndls_accidents", "type": "toggle", "label": "Previous Driving Accidents?", "required": True},
                    {"id": "ndls_meds_impair", "type": "toggle", "label": "Any Medication That Impairs Driving? (Patient's Own Assessment)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: If medication causes drowsiness = advise NOT to drive. Document clearly.", "red_flag_negative": ""},
                    {"id": "ndls_benzos", "type": "toggle", "label": "Taking Benzodiazepines?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: If drug test positive for benzodiazepines = must be clear for 6 months + letter from treatment centre confirming negative urine toxicology.", "red_flag_negative": ""},
                    {"id": "ndls_opiates", "type": "toggle", "label": "Taking Opiates?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: If drug test positive for opiates = must be clear for 6 months + letter from treatment centre.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ndls_visual_fields", "type": "single_select", "label": "Visual Fields", "required": True, "options": ["Normal", "Quadrantanopia", "Other Defect - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual field defect = may affect fitness. Refer to NDLS visual standards.", "red_flag_negative": ""},
                    {"id": "ndls_acuity", "type": "text", "label": "Binocular Vision Acuity (Unaided or Corrected)", "required": True, "placeholder": "e.g., 6/9 (Minimum 6/12 for Group 1)"},
                    {"id": "ndls_acuity_meets", "type": "toggle", "label": "Meets Group 1 Standard? (Binocular ≥6/12)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Does NOT meet 6/12 standard = unfit to drive. Refer optometrist/ophthalmology.", "red_flag_negative": ""},
                    {"id": "ndls_neck", "type": "single_select", "label": "Neck Movement", "required": True, "options": ["Full Range", "Restricted"]},
                    {"id": "ndls_chest", "type": "single_select", "label": "Chest Examination", "required": False, "options": ["Clear", "Abnormal"]},
                    {"id": "ndls_cvs", "type": "single_select", "label": "Cardiovascular Examination", "required": True, "options": ["Normal", "Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal CVS = investigate before certifying fitness.", "red_flag_negative": ""},
                    {"id": "ndls_limb_strength", "type": "single_select", "label": "Limb Strength", "required": True, "options": ["Normal", "Reduced - May Need Adaptations"]}
                ]
            },
            {
                "title": "Assessment & Certification",
                "section_type": "assessment",
                "differentials": [
                    "Fit to Drive - Group 1 (No Restrictions)",
                    "Fit to Drive - Group 1 (With Adaptations)",
                    "Fit to Drive - Requires Further Assessment",
                    "NOT Fit to Drive - Medical Contraindication",
                    "NOT Fit to Drive - Visual Standard Not Met",
                    "NOT Fit to Drive - Substance-Related (6-Month Clearance Required)"
                ],
                "questions": [
                    {"id": "ndls_fit", "type": "single_select", "label": "Fitness to Drive", "required": True, "options": ["FIT - Group 1", "FIT - With Restrictions/Adaptations", "NOT FIT - Medical Reason", "NOT FIT - Visual Standard", "NOT FIT - Substance-Related"]}
                ]
            },
            {
                "title": "Plan & Certification Details",
                "section_type": "plan",
                "safety_netting": "NDLS Medical Form: https://www.ndls.ie/images/Documents/Forms/171315_NDLS_Medical_Form_JAN_2022_WEB_HR.pdf. Group 1 minimum binocular vision: 6/12 (corrected or uncorrected). Advise patient: if ever drowsy after taking medication, do NOT drive. Substance-related restriction: if drug test positive for benzodiazepines or opiates = must be clear for 6 months + provide letter from treatment centre confirming all urine toxicology negative over past 6 months. Seizures: ≥1 year seizure-free (or sleep-only seizures ≥1 year). TIA/Stroke: 1 month off driving, must inform NDLS. Cardiac: refer to NDLS cardiovascular guidelines.",
                "questions": [
                    {"id": "ndls_duration", "type": "single_select", "label": "Certify Fit for", "required": False, "options": ["1 Year", "3 Years", "5 Years", "10 Years", "Not Certified"]},
                    {"id": "ndls_vehicle_type", "type": "single_select", "label": "Vehicle Type", "required": False, "options": ["Manual", "Automatic", "Both"]},
                    {"id": "ndls_adaptations_detail", "type": "text", "label": "Adaptations Required (or None)", "required": False, "placeholder": "e.g., None / Hand controls / Spinner knob"},
                    {"id": "ndls_medication_warning", "type": "toggle", "label": "Advised: If Drowsy After Medication, Do NOT Drive?", "required": True},
                    {"id": "ndls_followup", "type": "text", "label": "Follow-up / Review", "required": False, "placeholder": "e.g., Recertify in 3 years, sooner if condition changes"}
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
    seed_ndls_medical()