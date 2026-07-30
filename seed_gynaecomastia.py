from app.database import SessionLocal
from app.models import User, Template, Category

def seed_gynaecomastia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Gynaecomastia",
        "description": "Focused assessment for gynaecomastia covering physiological vs pathological causes, medication review, red flags for malignancy, and investigation triggers.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "gyn_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Bilateral breast enlargement for 6 months"},
                    {"id": "gyn_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 55"},
                    {"id": "gyn_presentation", "type": "single_select", "label": "How Presented", "required": True, "options": ["Breast enlargement", "Breast pain / tenderness", "Nipple discharge", "Incidental finding"]},
                    {"id": "gyn_duration", "type": "single_select", "label": "Duration", "required": True, "options": ["<1 month", "3 months", "6-12 months", ">12 months"]},
                    {"id": "gyn_laterality", "type": "single_select", "label": "Laterality", "required": True, "options": ["Unilateral", "Bilateral / symmetrical"]},
                    {"id": "gyn_onset_rate", "type": "single_select", "label": "Rate of Onset", "required": True, "options": ["Rapid", "Slow / gradual"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Rapid enlargement = investigate (testicular tumour, malignancy). Check AFP, B-HCG, testicular exam.", "red_flag_negative": ""},
                    {"id": "gyn_tenderness", "type": "toggle", "label": "Tenderness / Pain?", "required": True},
                    {"id": "gyn_nipple_discharge", "type": "toggle", "label": "Nipple Discharge?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Nipple discharge + breast enlargement = urgent breast clinic referral.", "red_flag_negative": ""},
                    {"id": "gyn_ed", "type": "toggle", "label": "Erectile Dysfunction?", "required": False}
                ]
            },
            {
                "title": "Systemic & Endocrine Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "gyn_weight_change", "type": "toggle", "label": "Weight Change?", "required": False},
                    {"id": "gyn_visual_field", "type": "toggle", "label": "Visual Field Loss? (Bitemporal hemianopia / bumping into things)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual field defect = ?pituitary mass. Urgent MRI + endocrinology.", "red_flag_negative": ""},
                    {"id": "gyn_heat_intolerance", "type": "toggle", "label": "Heat Intolerance / Thyroid Symptoms?", "required": False},
                    {"id": "gyn_family_breast_ca", "type": "toggle", "label": "Family History of Breast Cancer?", "required": True}
                ]
            },
            {
                "title": "Medications & Substances",
                "section_type": "history",
                "questions": [
                    {"id": "gyn_meds", "type": "multi_select", "label": "Causative Medications", "required": True, "options": ["Digoxin", "Spironolactone", "Antipsychotics (Risperidone, Haloperidol)", "Cimetidine", "Finasteride / Dutasteride", "Calcium Channel Blockers", "Proton Pump Inhibitors (PPIs)", "None of the above"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Drug-induced gynaecomastia common. Review medication - consider alternative if appropriate.", "red_flag_negative": ""},
                    {"id": "gyn_substances", "type": "multi_select", "label": "Substance Use", "required": True, "options": ["Alcohol excess", "Heroin / Opioids", "Cannabis", "Anabolic steroids", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Anabolic steroids = common cause. Alcohol = liver disease + hormonal disruption.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "gyn_breast_exam", "type": "single_select", "label": "Breast Examination", "required": True, "options": ["Symmetrical glandular tissue around areola (gynaecomastia)", "Asymmetrical / suspicious lump - RED FLAG", "Skin changes (peau d'orange, ulceration) - RED FLAG", "Normal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Asymmetrical hard/fixed lump or skin changes = ?male breast cancer. 2WW breast clinic.", "red_flag_negative": ""},
                    {"id": "gyn_tissue_size", "type": "number", "label": "Palpable Tissue Size (cm)", "required": False, "placeholder": "e.g., 2"},
                    {"id": "gyn_tissue_character", "type": "single_select", "label": "Tissue Character", "required": False, "options": ["Firm (gynaecomastia)", "Hard / craggy (malignancy) - RED FLAG", "Soft / fluctuant", "Fatty (pseudogynaecomastia)"]},
                    {"id": "gyn_testes", "type": "single_select", "label": "Testicular Examination", "required": True, "options": ["Normal size, no mass", "Atrophic", "Mass palpated - RED FLAG", "Asymmetry"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Testicular mass = ?testicular tumour. 3% of gynaecomastia have underlying testicular tumour. Urgent USS + urology.", "red_flag_negative": ""},
                    {"id": "gyn_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 32"},
                    {"id": "gyn_liver_signs", "type": "toggle", "label": "Signs of Liver Disease?", "required": False},
                    {"id": "gyn_cushingoid", "type": "toggle", "label": "Signs of Cushing's Syndrome?", "required": False},
                    {"id": "gyn_hyperthyroid", "type": "toggle", "label": "Signs of Hyperthyroidism?", "required": False},
                    {"id": "gyn_hair_pattern", "type": "single_select", "label": "Hair Pattern / Distribution", "required": False, "options": ["Abnormal / reduced", "Normal"]},
                    {"id": "gyn_klinefelter", "type": "multi_select", "label": "Signs of Klinefelter Syndrome?", "required": False, "options": ["Small testes", "Reduced body hair", "Gynaecoid habitus", "Tall stature", "None - no signs of hypogonadism"]}
                ]
            },
            {
                "title": "Investigation Triggers & Workup",
                "section_type": "assessment",
                "differentials": [
                    "Physiological / Idiopathic Gynaecomastia (most common)",
                    "Drug-Induced Gynaecomastia",
                    "Pseudogynaecomastia (Lipomastia - obesity)",
                    "Hypogonadism (primary / secondary)",
                    "Hyperprolactinaemia / Prolactinoma",
                    "Liver Cirrhosis",
                    "Chronic Kidney Disease",
                    "Testicular Tumour (3% of gynaecomastia cases)",
                    "Male Breast Cancer (RED FLAG - unilateral, hard, fixed, skin changes)",
                    "Klinefelter Syndrome (XXY)",
                    "Hyperthyroidism"
                ],
                "questions": [
                    {"id": "gyn_trigger_criteria", "type": "multi_select", "label": "Investigation Trigger Criteria Met?", "required": True, "options": ["Rapid enlargement", "Recent onset, lean male >20y", "Persistent and painful", "Massive or persistent (18-24m) in adolescent", "None - routine reassurance appropriate"]},
                    {"id": "gyn_first_line", "type": "multi_select", "label": "First-Line Investigations", "required": False, "options": ["Renal function (U&E, eGFR)", "Liver function tests (LFTs)", "TFTs (TSH, Free T4)", "Testosterone (9am - total)", "AFP", "Beta-HCG"]},
                    {"id": "gyn_second_line", "type": "multi_select", "label": "Second-Line (if Testosterone Low)", "required": False, "options": ["LH", "FSH", "Sex Hormone Binding Globulin (SHBG)", "Prolactin"]},
                    {"id": "gyn_imaging", "type": "multi_select", "label": "Further Imaging", "required": False, "options": ["Ultrasound testes (if AFP/B-HCG raised or mass)", "Mammogram / USS breast (if suspicious lump)", "MRI pituitary (if prolactin raised / visual symptoms)", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: rapid enlargement, breast lump becomes hard/fixed, skin changes (dimpling, ulceration), nipple discharge, or testicular mass/lump develops. Clinical Reference Notes: 3% of gynaecomastia cases have underlying testicular tumour. 7-11% of testicular tumour cases present with gynaecomastia as the ONLY presenting feature - testicular exam is MANDATORY. Pathological causes: hypogonadism, hyperprolactinaemia, liver cirrhosis, renal failure, testicular tumours, obesity. Indications to investigate: rapid enlargement, recent onset in lean men >20y, persistent and painful, massive or persistent (18-24m) in adolescents. Weight loss advised - obesity exacerbates all causes. Most common age of presentation: 50-69 years.",
                "questions": [
                    {"id": "gyn_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Physiological / Idiopathic Gynaecomastia", "Drug-Induced Gynaecomastia", "Pseudogynaecomastia (Lipomastia)", "Pathological Cause Suspected - Investigating", "Breast Malignancy Suspected - URGENT 2WW", "Testicular Mass - URGENT Urology"]},
                    {"id": "gyn_education", "type": "multi_select", "label": "Patient Education", "required": False, "options": ["Explained common age of presentation (50-69 years)", "Weight loss advised - obesity exacerbates all causes", "Reassurance re benign nature", "Advised to stop causative substance/medication if identified"]},
                    {"id": "gyn_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None at this stage", "Endocrinology", "Breast Clinic (2WW)", "Urology (testicular abnormality)", "Routine breast clinic"]},
                    {"id": "gyn_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4-6 weeks if investigations triggered, 3 months if physiological"}
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
    seed_gynaecomastia()