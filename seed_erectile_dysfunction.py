from app.database import SessionLocal
from app.models import User, Template, Category

def seed_erectile_dysfunction():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Erectile Dysfunction",
        "description": "Focused assessment for erectile dysfunction covering organic vs psychogenic causes, cardiovascular risk, and PDE5 inhibitor prescribing.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "ed_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Gradual difficulty maintaining erections for 6 months"},
                    {"id": "ed_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 52"},
                    {"id": "ed_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 6 months"},
                    {"id": "ed_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Gradual (months)", "Sudden (days/weeks)", "Situational"]},
                    {"id": "ed_initiation", "type": "single_select", "label": "Difficulty With", "required": True, "options": ["Initiation only", "Maintenance only", "Both initiation + maintenance"]},
                    {"id": "ed_morning_erections", "type": "single_select", "label": "Morning Erections", "required": True, "options": ["Present (suggests psychogenic)", "Absent (suggests organic)", "Reduced"]},
                    {"id": "ed_partner_absent", "type": "toggle", "label": "No Difficulty When Partner Absent? (Psychogenic)", "required": False},
                    {"id": "ed_relationship", "type": "single_select", "label": "Relationship Context", "required": False, "options": ["Stable relationship", "New relationship", "Relationship difficulties", "No current partner", "Declined to discuss"]}
                ]
            },
            {
                "title": "RED FLAGS - Cardiovascular",
                "section_type": "history",
                "questions": [
                    {"id": "ed_chest_pain", "type": "toggle", "label": "Exertional Chest Pain / Angina?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ED + exertional chest pain = ?significant CAD. Cardiac assessment before PDE5i. NO nitrates with PDE5i.", "red_flag_negative": ""},
                    {"id": "ed_claudication", "type": "toggle", "label": "Claudication / Leg Pain on Walking?", "required": False},
                    {"id": "ed_dyslipidaemia", "type": "toggle", "label": "Known Dyslipidaemia / High Cholesterol?", "required": True},
                    {"id": "ed_hypertension", "type": "toggle", "label": "Known Hypertension?", "required": True},
                    {"id": "ed_diabetes", "type": "toggle", "label": "Known Diabetes?", "required": True},
                    {"id": "ed_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Smoking = significant cardiovascular risk. Assess QRISK + lifestyle advice.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Endocrine & Neurological",
                "section_type": "history",
                "questions": [
                    {"id": "ed_libido_loss", "type": "toggle", "label": "Loss of Libido?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Loss of libido + ED = ?hypogonadism/prolactinoma. Check testosterone, prolactin.", "red_flag_negative": ""},
                    {"id": "ed_body_hair_loss", "type": "toggle", "label": "Loss of Body Hair?", "required": False},
                    {"id": "ed_gynaecomastia", "type": "toggle", "label": "Gynaecomastia?", "required": False},
                    {"id": "ed_galactorrhoea", "type": "toggle", "label": "Galactorrhoea?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Galactorrhoea + ED = ?prolactinoma. Check prolactin + consider pituitary MRI.", "red_flag_negative": ""},
                    {"id": "ed_headache", "type": "toggle", "label": "Headaches?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Headaches + ED = ?pituitary mass. Visual fields + MRI if indicated.", "red_flag_negative": ""},
                    {"id": "ed_visual_field", "type": "toggle", "label": "Bitemporal Visual Field Loss?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual field defect = ?pituitary macroadenoma. Urgent MRI + endocrinology.", "red_flag_negative": ""},
                    {"id": "ed_back_pain", "type": "toggle", "label": "Back Pain / Sciatica?", "required": False},
                    {"id": "ed_neuro_deficit", "type": "toggle", "label": "Lower Limb Neurological Deficit?", "required": False}
                ]
            },
            {
                "title": "Medications & Lifestyle",
                "section_type": "history",
                "questions": [
                    {"id": "ed_meds_cause", "type": "multi_select", "label": "Medications That Cause ED", "required": True, "options": ["Beta-blockers", "Thiazide diuretics", "SSRIs", "5-Alpha Reductase Inhibitors (Finasteride/Dutasteride)", "Opioids", "Antipsychotics", "Entresto (Sacubitril/Valsartan)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Multiple medications can cause ED. Review and consider alternatives.", "red_flag_negative": ""},
                    {"id": "ed_nitrates", "type": "toggle", "label": "Taking Nitrates / Nicorandil? (Absolute contraindication to PDE5i)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Nitrates + PDE5i = SEVERE/FATAL HYPOTENSION. NEVER co-prescribe. Document clearly.", "red_flag_negative": ""},
                    {"id": "ed_cycling", "type": "toggle", "label": "Cycling >3 Hours/Week? (Perineal nerve compression)", "required": False},
                    {"id": "ed_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess (>14 units/week)"]},
                    {"id": "ed_peyronies", "type": "toggle", "label": "Penile Deviation / Pain? (Peyronie's Disease)", "required": False},
                    {"id": "ed_hypospadias", "type": "toggle", "label": "Hypospadias?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ed_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 122/84"},
                    {"id": "ed_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 90"},
                    {"id": "ed_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 28"},
                    {"id": "ed_waist", "type": "number", "label": "Waist Circumference (cm)", "required": False, "placeholder": "e.g., 98"},
                    {"id": "ed_gynaecomastia_exam", "type": "toggle", "label": "Gynaecomastia on Exam?", "required": False},
                    {"id": "ed_hair_distribution", "type": "toggle", "label": "Normal Male Hair Distribution?", "required": False},
                    {"id": "ed_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal, No Murmurs", "Murmur Present", "Not examined"]},
                    {"id": "ed_pulses", "type": "single_select", "label": "Pedal Pulses (PT + DP)", "required": False, "options": ["B/L Present + Normal", "Reduced/Absent", "Not examined"]},
                    {"id": "ed_spine", "type": "single_select", "label": "Lumbar Spine", "required": False, "options": ["Non-tender, Normal ROM", "Tender", "Not examined"]},
                    {"id": "ed_neuro_exam", "type": "single_select", "label": "Lower Limb Neuro (SLR, Reflexes, Sensation)", "required": False, "options": ["Normal", "Abnormal", "Not examined"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Psychogenic ED (performance anxiety, depression, relationship)",
                    "Vasculogenic ED (atherosclerosis, hypertension, diabetes, smoking)",
                    "Endocrine ED (hypogonadism, prolactinoma, thyroid disease)",
                    "Neurogenic ED (spinal cord, pelvic surgery, MS, Parkinson's)",
                    "Drug-Induced ED (beta-blockers, SSRIs, 5-ARIs, antiandrogens)",
                    "Peyronie's Disease",
                    "Venous Leak",
                    "Pelvic / Perineal Trauma",
                    "Chronic Kidney Disease"
                ],
                "questions": [
                    {"id": "ed_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Likely psychogenic ED", "Likely organic ED", "Mixed psychogenic + organic", "Likely medication-induced", "Suspected hypogonadism", "Suspected prolactinoma", "Uncertain"]},
                    {"id": "ed_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["Fasting lipids", "Fasting glucose / HbA1c", "Fasted early-morning total testosterone", "LH / FSH (if testosterone low)", "Prolactin", "PSA (if urinary symptoms or indicated)", "TFTs (if thyroid symptoms)", "U&E / Creatinine", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: chest pain during sexual activity, priapism (erection lasting >4 hours - EMERGENCY), sudden visual loss (NAION risk with PDE5i), or medication not effective. PDE5i absolute contraindication: NEVER take with nitrates/nicorandil (risk of severe fatal hypotension). PDE5i side effects: facial flushing, headache, nasal congestion, dyspepsia (common, usually mild). Sildenafil max 4 tablets/month on DPS/GMS. Take 1 hour before sexual activity. Requires sexual stimulation to work - not an aphrodisiac. If PDE5i ineffective: consider Tadalafil (longer duration), Vardenafil, or refer Urology for Alprostadil (Vitaros/MUSE), vacuum device, or intracavernosal injections.",
                "questions": [
                    {"id": "ed_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Sildenafil 50mg PRN (1 hour before)", "Sildenafil 100mg PRN", "Tadalafil 10mg PRN", "Tadalafil 5mg daily", "Lifestyle modification + review", "Refer Urology", "Refer Endocrinology", "Refer Psychosexual counselling"]},
                    {"id": "ed_nitrate_warning", "type": "toggle", "label": "Nitrate Contraindication Warning Given? (NEVER with PDE5i)", "required": True},
                    {"id": "ed_priapism_warning", "type": "toggle", "label": "Priapism Warning Given? (>4 hours = EMERGENCY)", "required": True},
                    {"id": "ed_lifestyle", "type": "toggle", "label": "Lifestyle Advice? (Weight loss, exercise, smoking cessation, alcohol reduction)", "required": False},
                    {"id": "ed_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4 weeks with blood results + QRISK assessment"}
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
    seed_erectile_dysfunction()