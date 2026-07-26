from app.database import SessionLocal
from app.models import User, Template, Category

def seed_raised_alt():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised ALT Assessment",
        "description": "Structured assessment for raised ALT covering NAFLD risk stratification, AST:ALT ratio interpretation, stepwise investigation, and lifestyle management.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "alt_level", "type": "number", "label": "ALT Level (U/L)", "required": True, "placeholder": "e.g., 92 (Note lab reference range)"},
                    {"id": "alt_ast", "type": "number", "label": "AST Level (If Available)", "required": False, "placeholder": "e.g., 45"},
                    {"id": "alt_ast_alt_ratio", "type": "number", "label": "AST:ALT Ratio", "required": False, "placeholder": "e.g., 0.5 (<0.8 = Lower Risk, >0.8 = Higher Risk, >1.5 = ?Alcoholic)"},
                    {"id": "alt_diabetes", "type": "toggle", "label": "Diabetes? (NAFLD Risk Factor)", "required": True},
                    {"id": "alt_bbv_risk", "type": "multi_select", "label": "Blood-Borne Virus Risk Screen", "required": True, "options": ["Tattoos", "Blood Transfusion (Before 1991)", "Piercings", "Intravenous Drug Use", "None"]},
                    {"id": "alt_dental_ireland", "type": "toggle", "label": "Dental Fillings Performed in Ireland? (Confirm Location)", "required": False},
                    {"id": "alt_meds", "type": "multi_select", "label": "Hepatotoxic Medications", "required": True, "options": ["Methotrexate", "Azathioprine", "Nitrofurantoin", "Statins", "Terbinafine", "Carbamazepine", "Paracetamol (Excess)", "None of the above"]},
                    {"id": "alt_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within Limits (<14 Units/Week)", "Excess (14-21 Units/Week)", "Heavy (>21 Units/Week / Binge Drinking)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol excess = most common cause of raised ALT. Stop alcohol + repeat LFTs in 4-6 weeks.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "alt_bmi", "type": "number", "label": "BMI (kg/m²) - MUST Document", "required": True, "placeholder": "e.g., 32", "is_red_flag": True, "red_flag_positive": "RED FLAG: Raised BMI + raised ALT = ?NAFLD. Weight loss 7-10% = key intervention.", "red_flag_negative": ""},
                    {"id": "alt_liver_exam", "type": "multi_select", "label": "Abdominal / Liver Examination", "required": True, "options": ["Hepatomegaly", "Ascites", "Normal - No Hepatomegaly/Ascites"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Hepatomegaly/ascites = chronic liver disease. Urgent gastroenterology.", "red_flag_negative": ""},
                    {"id": "alt_cld_signs", "type": "multi_select", "label": "Signs of Chronic Liver Disease", "required": True, "options": ["Palmar Erythema", "Clubbing", "Spider Naevi", "Dupuytren's Contracture", "Gynaecomastia", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: CLD stigmata = advanced liver disease. Urgent gastroenterology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Step 1 - Initial Management",
                "section_type": "plan",
                "questions": [
                    {"id": "alt_stop_alcohol", "type": "toggle", "label": "Stop Alcohol Advised? (If Appropriate)", "required": True},
                    {"id": "alt_repeat_lfts", "type": "toggle", "label": "Repeat LFTs (ALT, AST, GGT) in 4-6 Weeks?", "required": True},
                    {"id": "alt_hba1c", "type": "toggle", "label": "HbA1c Ordered? (At Same Time as Repeat LFTs)", "required": False}
                ]
            },
            {
                "title": "Step 2 - If LFTs Remain Raised at Repeat",
                "section_type": "assessment",
                "questions": [
                    {"id": "alt_hepatitis_serology", "type": "toggle", "label": "Hepatitis B + C Serology Ordered?", "required": False},
                    {"id": "alt_hiv", "type": "toggle", "label": "HIV Screen Ordered?", "required": False},
                    {"id": "alt_ferritin_iron", "type": "toggle", "label": "Ferritin + Iron Studies Ordered?", "required": False},
                    {"id": "alt_inr", "type": "toggle", "label": "INR Ordered?", "required": False},
                    {"id": "alt_uss", "type": "toggle", "label": "Ultrasound Liver? (Assess for Hepatic Steatosis / Fatty Liver)", "required": False}
                ]
            },
            {
                "title": "Interpretation",
                "section_type": "assessment",
                "differentials": [
                    "Non-Alcoholic Fatty Liver Disease (NAFLD) - Most Common Cause of Mildly Raised ALT",
                    "Alcoholic Liver Disease (AST:ALT >1.5, GGT Raised, MCV Raised)",
                    "Viral Hepatitis (A/B/C/EBV/CMV)",
                    "Drug-Induced Liver Injury (Statins, Methotrexate, Azathioprine, etc.)",
                    "Haemochromatosis (Ferritin Raised, Transferrin Saturation >45%)",
                    "Autoimmune Hepatitis (ANA, SMA, IgG Raised)",
                    "Wilson's Disease (Young, Copper Studies)",
                    "Alpha-1 Antitrypsin Deficiency"
                ],
                "questions": [
                    {"id": "alt_ratio_interpret", "type": "single_select", "label": "AST:ALT Ratio Interpretation", "required": False, "options": ["<0.8: Lower Risk NAFLD", ">0.8: Higher Risk NAFLD - Consider Referral", ">1.5: Strongly Suggestive of Alcoholic Liver Disease", "ALT > AST: ?Acute Hepatitis / Obstructive Jaundice", "Not applicable"]},
                    {"id": "alt_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?NAFLD (Most Likely - Raised BMI)", "?Alcoholic Liver Disease", "?Drug-Induced", "?Viral Hepatitis", "?Haemochromatosis", "Raised ALT - Investigating"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "First step: stop alcohol (if appropriate) + repeat LFTs in 4-6 weeks. Check HbA1c at same time. If LFTs remain raised: Hepatitis B+C serology, HIV, ferritin/iron studies, INR, consider US liver for hepatic steatosis. AST:ALT ratio: <0.8 = lower risk NAFLD, >0.8 = higher risk (consider referral), >1.5 = strongly suggestive of alcoholic liver disease. ALT higher than AST = suggests acute hepatitis (viral, drug-induced, autoimmune) or obstructive jaundice. NAFLD management: weight loss 7-10%, Mediterranean diet, exercise, optimise diabetes/HTN/lipids. If AST:ALT >0.8 or persistent raised ALT despite lifestyle: refer gastroenterology/hepatology.",
                "questions": [
                    {"id": "alt_weight_loss", "type": "toggle", "label": "Weight Loss 7-10% Advised? (NAFLD - Key Intervention)", "required": False},
                    {"id": "alt_diet_exercise", "type": "toggle", "label": "Mediterranean Diet + Exercise Advised?", "required": False},
                    {"id": "alt_drug_review", "type": "toggle", "label": "Hepatotoxic Medication Reviewed? (Stop/Reduce If Drug-Induced)", "required": False},
                    {"id": "alt_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Lifestyle + Repeat LFTs)", "Gastroenterology / Hepatology (AST:ALT >0.8 / Persistent / CLD Signs)", "Urgent Gastroenterology (Hepatomegaly / Ascites / CLD Stigmata)"]},
                    {"id": "alt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat LFTs + HbA1c in 4-6 weeks, refer if persistent"}
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
    seed_raised_alt()