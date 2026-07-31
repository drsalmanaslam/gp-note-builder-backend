from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_low_hb_female():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low Haemoglobin / Anaemia - Female",
        "description": "Comprehensive anaemia assessment for females covering gynaecological bleeding, iron deficiency treatment, dietary advice, and referral pathways.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_hb", "type": "number", "label": "Haemoglobin (g/dL) - NR: 11.5-16.0", "required": True, "placeholder": "e.g., 9.8", "is_red_flag": True, "red_flag_positive": "RED FLAG: Hb <8 g/dL = severe anaemia. Urgent assessment + consider admission.", "red_flag_negative": ""},
                    {"id": "lhb_symptoms", "type": "multi_select", "label": "Symptom Screen", "required": True, "options": ["Lethargy / fatigue", "Shortness of breath", "Palpitations", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB + palpitations + anaemia = cardiac compromise possible. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "lhb_diet", "type": "single_select", "label": "Dietary Intake", "required": True, "options": ["Adequate red meat + green leafy vegetables", "Reduced intake", "Vegetarian", "Vegan"]}
                ]
            },
            {
                "title": "Bleeding Screen",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_menorrhagia", "type": "toggle", "label": "Menorrhagia / Heavy Periods?", "required": True},
                    {"id": "lhb_imb", "type": "toggle", "label": "Intermenstrual Bleeding (IMB)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: IMB = ?endometrial pathology. Pelvic USS + consider endometrial biopsy if >45.", "red_flag_negative": ""},
                    {"id": "lhb_pcb", "type": "toggle", "label": "Postcoital Bleeding (PCB)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: PCB = ?cervical cancer. Speculum examination + 2WW referral if suspicious.", "red_flag_negative": ""},
                    {"id": "lhb_pr_bleeding", "type": "toggle", "label": "PR Bleeding / Melaena?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: GI bleeding + anaemia = urgent GI workup (OGD/colonoscopy).", "red_flag_negative": ""},
                    {"id": "lhb_haematuria", "type": "toggle", "label": "Haematuria?", "required": False},
                    {"id": "lhb_haemoptysis", "type": "toggle", "label": "Haemoptysis?", "required": False},
                    {"id": "lhb_epistaxis", "type": "toggle", "label": "Epistaxis?", "required": False}
                ]
            },
            {
                "title": "GI & Systemic Screen",
                "section_type": "history",
                "questions": [
                    {"id": "lhb_gi_symptoms", "type": "multi_select", "label": "GI Symptoms", "required": True, "options": ["Change in bowel habit", "Dyspepsia", "Vomiting", "Nausea", "Abdominal pain", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: GI symptoms + anaemia = urgent GI investigation (coeliac, IBD, malignancy).", "red_flag_negative": ""},
                    {"id": "lhb_angina", "type": "toggle", "label": "Angina / Chest Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Angina + anaemia = myocardial ischaemia risk. Urgent ECG + consider admission.", "red_flag_negative": ""},
                    {"id": "lhb_malignancy", "type": "multi_select", "label": "Malignancy Screen", "required": True, "options": ["Drenching night sweats", "Weight loss", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: B symptoms + anaemia = ?lymphoma/malignancy. Urgent investigation.", "red_flag_negative": ""},
                    {"id": "lhb_pmh", "type": "multi_select", "label": "Relevant PMHx", "required": False, "options": ["Renal failure / CKD", "Rheumatoid Arthritis", "IBD (Crohn's / UC)", "Coeliac disease", "None"]},
                    {"id": "lhb_bruising", "type": "toggle", "label": "Easy Bruising / Bleeding Tendency?", "required": False},
                    {"id": "lhb_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Current", "Ex-smoker", "Never"]},
                    {"id": "lhb_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "lhb_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 24"},
                    {"id": "lhb_urine_dip", "type": "single_select", "label": "Urine Dipstick - Blood?", "required": False, "options": ["Present", "Absent", "Not performed"]},
                    {"id": "lhb_conjunctival_pallor", "type": "toggle", "label": "Conjunctival Pallor?", "required": False},
                    {"id": "lhb_koilonychia", "type": "toggle", "label": "Koilonychia (Spoon Nails)?", "required": False},
                    {"id": "lhb_glossitis", "type": "toggle", "label": "Glossitis?", "required": False},
                    {"id": "lhb_cvs", "type": "single_select", "label": "Cardiovascular", "required": False, "options": ["HS I+II Normal, No Murmurs", "Murmur Present (Flow Murmur?)", "Ankle Oedema Present"]},
                    {"id": "lhb_resp", "type": "single_select", "label": "Respiratory", "required": False, "options": ["Clear B/L, Vesicular BS", "Reduced Air Entry", "Added Sounds"]},
                    {"id": "lhb_abdo", "type": "single_select", "label": "Abdominal", "required": False, "options": ["Soft, Non-Tender, No Organomegaly/Masses", "Organomegaly / Mass - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abdominal mass + anaemia = ?GI malignancy. Urgent 2WW.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Iron Deficiency Anaemia (Dietary / Menorrhagia / GI Loss)",
                    "Anaemia of Chronic Disease (CKD, RA, IBD)",
                    "Vitamin B12 / Folate Deficiency",
                    "Coeliac Disease",
                    "Hypothyroidism",
                    "Haematological Malignancy (Leukaemia, Lymphoma, Myeloma)",
                    "Colorectal Cancer (RED FLAG)",
                    "Gynaecological Malignancy (RED FLAG - IMB, PCB)"
                ],
                "questions": [
                    {"id": "lhb_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC + Blood Film", "Haematinics (Ferritin, B12, Folate)", "Iron Studies", "LFTs", "TFTs", "ESR / CRP", "Coeliac Screen (IgA TTG + IgA)", "None"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Do NOT wait for investigation results before starting iron supplementation. First-line: Ferrous sulfate 200mg two to three times daily. If not tolerated: Ferrous fumarate or ferrous gluconate. Continue treatment for 3 months AFTER iron deficiency corrected to replenish stores. GMS reimbursable: Galfer, Galfer FA, Galfer Liquid, Ferrograd - 1 tablet daily or alternate days. Ferrograd C and Active Iron are NOT GMS reimbursable. Take on empty stomach if tolerated, avoid tea/coffee/calcium around administration, consider vitamin C to improve absorption. Dietary advice: increase red meat, green leafy vegetables, pulses, legumes, iron-fortified cereals. NICE CKS: Anaemia - Iron Deficiency. May require referral for endoscopy, SPEP, or other investigation depending on cause.",
                "questions": [
                    {"id": "lhb_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Iron Deficiency Anaemia - ?Dietary", "Iron Deficiency Anaemia - ?Menorrhagia", "Iron Deficiency Anaemia - ?GI Loss", "Anaemia of Chronic Disease", "?Coeliac Disease", "?Haematological Malignancy", "Red Flags Present - Urgent Investigation"]},
                    {"id": "lhb_iron_rx", "type": "single_select", "label": "Iron Replacement (NICE CKS)", "required": False, "options": ["Ferrous Sulfate 200mg 2-3 Times Daily", "Ferrous Fumarate (If Sulfate Not Tolerated)", "Ferrous Gluconate (If Sulfate Not Tolerated)", "Galfer 1 Tablet Daily", "Galfer FA 1 Tablet Daily", "Ferrograd 1 Tablet Daily", "Not yet started"]},
                    {"id": "lhb_gms_note", "type": "toggle", "label": "GMS Options Explained? (Galfer, Galfer FA, Galfer Liquid, Ferrograd - Ferrograd C/Active Iron NOT GMS)", "required": False},
                    {"id": "lhb_iron_advice", "type": "toggle", "label": "Iron Administration Advice Given? (Empty Stomach, Avoid Tea/Coffee/Ca, Vit C Helps)", "required": False},
                    {"id": "lhb_dietary_advice", "type": "toggle", "label": "Dietary Advice Given? (Red Meat, Leafy Greens, Pulses, Fortified Cereals)", "required": False},
                    {"id": "lhb_continue_3months", "type": "toggle", "label": "Continue Iron for 3 Months After Hb Normalises? (Replenish Stores)", "required": True},
                    {"id": "lhb_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "Gynaecology (Menorrhagia / IMB / PCB)", "Gastroenterology (OGD / Colonoscopy)", "Haematology", "Urgent 2WW (Red Flags)"]},
                    {"id": "lhb_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat FBC + ferritin in 4-6 weeks, continue iron 3 months post-normalisation"}
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
    seed_low_hb_female()