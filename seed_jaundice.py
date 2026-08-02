from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_jaundice():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Jaundice",
        "description": "Comprehensive template for jaundice covering pre-hepatic, hepatic, and post-hepatic causes, Courvoisier's sign, PBC screening, and investigation pathways.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "jaun_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Yellow eyes and skin for 1 week"},
                    {"id": "jaun_duration", "type": "text", "label": "Duration of Jaundice", "required": True, "placeholder": "e.g., 1 week"},
                    {"id": "jaun_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (?viral)", "Slow / gradual (?malignancy)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Slow gradual onset + painless jaundice = ?pancreatic/biliary malignancy. Urgent investigation.", "red_flag_negative": ""},
                    {"id": "jaun_location", "type": "single_select", "label": "Location", "required": True, "options": ["Eyes only", "Skin only", "Both"]},
                    {"id": "jaun_associated", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Itching (pruritus)", "Pale stool (obstructive)", "Dark urine (obstructive)", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Pale stool + dark urine = OBSTRUCTIVE JAUNDICE. Urgent US liver + gastroenterology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Differential Screening",
                "section_type": "history",
                "questions": [
                    {"id": "jaun_biliary_colic", "type": "toggle", "label": "RUQ Pain Radiating to Shoulder Tip? (Biliary Colic)", "required": False},
                    {"id": "jaun_constitutional", "type": "multi_select", "label": "Constitutional Symptoms", "required": True, "options": ["Malaise", "Lethargy", "Bleeding (PO/PR) - RED FLAG", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bleeding + jaundice = liver synthetic dysfunction. Check INR urgently.", "red_flag_negative": ""},
                    {"id": "jaun_viral_risk", "type": "multi_select", "label": "Viral Hepatitis Risk Factors", "required": True, "options": ["Recent travel", "Blood transfusion", "Unprotected sexual intercourse (UPSI)", "Tattoos / body piercings", "IV drug use", "None present"]},
                    {"id": "jaun_toxins", "type": "multi_select", "label": "Toxin / Substance History", "required": True, "options": ["OTC medications (paracetamol?)", "Alcohol excess", "Recreational drugs", "None"]},
                    {"id": "jaun_gi_bleed", "type": "multi_select", "label": "GI Bleeding Screen", "required": True, "options": ["Melaena", "Haematemesis", "Neither present"]},
                    {"id": "jaun_acute_hepatitis", "type": "multi_select", "label": "Acute Hepatitis Screen", "required": True, "options": ["Vomiting", "Fever", "Neither present"]},
                    {"id": "jaun_malignancy", "type": "multi_select", "label": "Malignancy Screen", "required": True, "options": ["Weight loss", "Painless jaundice - RED FLAG", "Neither present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Painless jaundice + weight loss = ?pancreatic head cancer. Courvoisier's sign. Urgent CT/US.", "red_flag_negative": ""},
                    {"id": "jaun_pancreatitis", "type": "toggle", "label": "Difficulty Flushing Stools? (Steatorrhoea - ?pancreatic insufficiency)", "required": False},
                    {"id": "jaun_pbc", "type": "multi_select", "label": "Primary Biliary Cholangitis (PBC) Screen", "required": False, "options": ["Dry mouth", "Dry eyes", "Tired all the time", "Itchy skin", "None present - classic in middle-aged women"]},
                    {"id": "jaun_family", "type": "multi_select", "label": "Family History", "required": False, "options": ["Wilson's disease", "Hepatitis", "Haemochromatosis", "Jaundice", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "jaun_vitals", "type": "text", "label": "Vital Signs", "required": True, "placeholder": "e.g., Temp 37°C, BP 130/80"},
                    {"id": "jaun_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 28"},
                    {"id": "jaun_jaundice_exam", "type": "single_select", "label": "Jaundice on Examination", "required": True, "options": ["No visible jaundice", "Jaundice present - skin", "Jaundice present - sclera", "Both skin + sclera"]},
                    {"id": "jaun_abdo", "type": "multi_select", "label": "Abdominal Examination", "required": True, "options": ["No hepatomegaly", "No splenomegaly", "No palpable gallbladder", "Hepatomegaly present", "Splenomegaly present", "Palpable gallbladder (Courvoisier's sign) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Palpable gallbladder + painless jaundice = COURVOISIER'S SIGN (?pancreatic cancer). Urgent CT.", "red_flag_negative": ""},
                    {"id": "jaun_kf_rings", "type": "toggle", "label": "Kayser-Fleischer Rings? (Wilson's disease)", "required": False},
                    {"id": "jaun_cld_stigmata", "type": "multi_select", "label": "Chronic Liver Disease Stigmata", "required": True, "options": ["Tremor (asterixis)", "Clubbing", "Spider naevi", "Dupuytren's contracture", "Palmar erythema", "Gynaecomastia", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: CLD stigmata = chronic liver disease. Check LFTs, INR, albumin. Urgent gastroenterology.", "red_flag_negative": ""},
                    {"id": "jaun_encephalopathy", "type": "toggle", "label": "Encephalopathy? (Confusion, asterixis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Encephalopathy + jaundice = acute liver failure. EMERGENCY admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Pre-Hepatic: Haemolysis (unconjugated bilirubin ↑, LFTs normal)",
                    "Hepatic: Viral Hepatitis (A/B/C/EBV/CMV)",
                    "Hepatic: Alcoholic Hepatitis",
                    "Hepatic: Drug-Induced Liver Injury (DILI)",
                    "Hepatic: Autoimmune Hepatitis",
                    "Hepatic: PBC (AMA positive, IgM ↑)",
                    "Hepatic: Wilson's Disease (young, KF rings, copper studies)",
                    "Hepatic: Haemochromatosis (ferritin ↑, transferrin saturation ↑)",
                    "Post-Hepatic: Choledocholithiasis (RUQ pain, dilated ducts)",
                    "Post-Hepatic: Pancreatic Cancer (painless, Courvoisier's, weight loss)",
                    "Post-Hepatic: Cholangiocarcinoma",
                    "Post-Hepatic: PSC (UC-associated)"
                ],
                "questions": [
                    {"id": "jaun_first_line", "type": "multi_select", "label": "First-Line Bloods", "required": False, "options": ["FBC (haemolysis?)", "Renal profile (U&Es)", "LFTs (conjugated + unconjugated bilirubin)", "Alkaline Phosphatase (ALP)", "ALT / AST", "Total bilirubin with fractionation", "INR / Coagulation screen", "Glucose", "Ferritin (haemochromatosis)", "Hepatitis screen (A/B/C)"]},
                    {"id": "jaun_second_line", "type": "multi_select", "label": "Second-Line Bloods (If Indicated)", "required": False, "options": ["EBV / CMV serology", "Copper studies (Wilson's)", "Autoantibody screen (ANA, SMA, LKM)", "Immunoglobulins (IgG, IgM)", "Alpha-Fetoprotein (AFP)", "Alpha-1 Antitrypsin", "Amylase / Lipase", "None"]},
                    {"id": "jaun_pbc_workup", "type": "multi_select", "label": "PBC-Specific Workup", "required": False, "options": ["Immunoglobulins (IgM)", "AMA (Anti-Mitochondrial Antibody)", "ESR", "Not indicated"]},
                    {"id": "jaun_urine", "type": "multi_select", "label": "Urine Studies", "required": False, "options": ["Bilirubin", "Urobilinogen", "Not indicated"]},
                    {"id": "jaun_imaging", "type": "single_select", "label": "Imaging", "required": True, "options": ["US Liver + Biliary Tree Requested", "CT Abdomen (if malignancy suspected)", "Not required at this stage"]}
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "Attend A&E immediately if: confusion/drowsiness (encephalopathy), vomiting blood (haematemesis), black tarry stools (melaena), severe abdominal pain, or fever with rigors (cholangitis). Pre-hepatic jaundice: unconjugated bilirubin ↑, normal LFTs = haemolysis workup. Hepatic jaundice: AST/ALT ↑, ALP normal/mild ↑ = hepatocellular injury. Post-hepatic jaundice: ALP ↑↑, GGT ↑↑, bile ducts dilated on US = obstruction. Painless jaundice + palpable gallbladder (Courvoisier's sign) = pancreatic cancer until proven otherwise. PBC: middle-aged women, itching, fatigue, AMA positive, IgM ↑.",
                "questions": [
                    {"id": "jaun_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Jaundice - cause to be determined", "Viral hepatitis suspected", "Biliary obstruction suspected", "Haemolytic cause suspected", "PBC suspected", "Malignancy suspected - URGENT", "Haemochromatosis suspected", "Wilson's disease suspected", "Alcoholic hepatitis"]},
                    {"id": "jaun_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - awaiting results", "Gastroenterology / Hepatology", "Urgent referral - red flags present", "Emergency A&E (encephalopathy/bleeding)"]},
                    {"id": "jaun_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review with results, urgent same-day if deteriorating"}
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
    seed_jaundice()