from app.database import SessionLocal
from app.models import User, Template, Category

def seed_raised_ast():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised AST",
        "description": "Focused assessment for raised AST covering NAFLD vs alcoholic liver disease differentiation, AST:ALT ratio interpretation, and stepwise investigation.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & History",
                "section_type": "history",
                "questions": [
                    {"id": "ast_level", "type": "number", "label": "AST Level (U/L)", "required": True, "placeholder": "e.g., 78 (Note lab reference range)"},
                    {"id": "ast_alt", "type": "number", "label": "ALT Level (If Available)", "required": False, "placeholder": "e.g., 42"},
                    {"id": "ast_ast_alt_ratio", "type": "number", "label": "AST:ALT Ratio", "required": False, "placeholder": "e.g., 1.8 (>1.5 = Strongly Suggestive Alcoholic Liver Disease)"},
                    {"id": "ast_meds", "type": "multi_select", "label": "Hepatotoxic Medications", "required": True, "options": ["Methotrexate", "Azathioprine", "Nitrofurantoin", "Statins", "Terbinafine", "Carbamazepine", "None of the above"]},
                    {"id": "ast_alcohol", "type": "single_select", "label": "Alcohol Intake (Most Common Cause of Raised AST)", "required": True, "options": ["None", "Within Limits", "Excess / Binge Drinking"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Alcohol excess = most common cause of raised AST. Stop alcohol + repeat LFTs in 4-6 weeks.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ast_liver_exam", "type": "multi_select", "label": "Abdominal / Liver Examination", "required": True, "options": ["Hepatomegaly", "Ascites", "Normal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Hepatomegaly/ascites = chronic liver disease. Urgent gastroenterology.", "red_flag_negative": ""},
                    {"id": "ast_cld_signs", "type": "multi_select", "label": "Signs of Chronic Liver Disease", "required": True, "options": ["Palmar Erythema", "Clubbing", "Spider Naevi", "Dupuytren's Contracture", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: CLD stigmata = advanced liver disease. Urgent gastroenterology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Step 1 - Initial Management",
                "section_type": "plan",
                "questions": [
                    {"id": "ast_stop_alcohol", "type": "toggle", "label": "Stop Alcohol Advised?", "required": True},
                    {"id": "ast_repeat_lfts", "type": "toggle", "label": "Repeat LFTs (AST, ALT, GGT) in 4-6 Weeks?", "required": True}
                ]
            },
            {
                "title": "Step 2 - If LFTs Remain Raised",
                "section_type": "assessment",
                "questions": [
                    {"id": "ast_hepatitis", "type": "toggle", "label": "Hepatitis B + C Serology Ordered?", "required": False},
                    {"id": "ast_ferritin", "type": "toggle", "label": "Ferritin + Iron Studies Ordered?", "required": False},
                    {"id": "ast_inr", "type": "toggle", "label": "INR Ordered?", "required": False},
                    {"id": "ast_uss", "type": "toggle", "label": "Ultrasound Liver? (Assess for Fatty Liver)", "required": False}
                ]
            },
            {
                "title": "Interpretation",
                "section_type": "assessment",
                "differentials": [
                    "Alcoholic Liver Disease (AST:ALT >1.5, GGT Raised, MCV Raised) - Most Common",
                    "Non-Alcoholic Fatty Liver Disease (NAFLD)",
                    "Drug-Induced Liver Injury (Statins, Methotrexate, etc.)",
                    "Viral Hepatitis (B/C/EBV/CMV)",
                    "Haemochromatosis (Ferritin Raised)",
                    "Autoimmune Hepatitis",
                    "Muscle Source (AST also from muscle - check CK if ALT normal)",
                    "Wilson's Disease (Young Patients)"
                ],
                "questions": [
                    {"id": "ast_ratio_interpret", "type": "single_select", "label": "AST:ALT Ratio Interpretation", "required": False, "options": ["<0.8: Lower Risk NAFLD", ">0.8: Higher Risk - Consider Referral", ">1.5: STRONGLY Suggestive of Alcoholic Liver Disease", "Not applicable (ALT Not Available)"]},
                    {"id": "ast_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Alcoholic Liver Disease", "?NAFLD", "?Drug-Induced", "?Viral Hepatitis", "Raised AST - Investigating"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Most commonly due to fatty liver or alcohol. First step: stop alcohol + repeat LFTs in 4-6 weeks. If LFTs remain raised: Hepatitis B+C serology, ferritin/iron studies, INR, consider US liver for fatty liver. AST:ALT ratio: <0.8 = lower risk NAFLD, >0.8 = higher risk (consider referral), >1.5 = strongly suggestive of alcoholic liver disease. AST also found in muscle - if ALT normal, consider checking CK (muscle source). Confirm no medication cause and no signs of CLD before proceeding. If AST:ALT >0.8 or persistent despite lifestyle: refer gastroenterology/hepatology.",
                "questions": [
                    {"id": "ast_drug_review", "type": "toggle", "label": "Hepatotoxic Medication Reviewed?", "required": False},
                    {"id": "ast_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Lifestyle + Repeat LFTs)", "Gastroenterology / Hepatology (AST:ALT >0.8 / Persistent / CLD Signs)", "Urgent Gastroenterology (Hepatomegaly / Ascites / CLD Stigmata)"]},
                    {"id": "ast_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat LFTs in 4-6 weeks, refer if persistent or CLD signs"}
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
    seed_raised_ast()