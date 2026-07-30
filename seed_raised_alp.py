from app.database import SessionLocal
from app.models import User, Template, Category

def seed_raised_alp():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Alkaline Phosphatase",
        "description": "Stepwise investigation of raised ALP covering hepatobiliary vs bone source differentiation, PBC screening, and drug-induced causes.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Results & History",
                "section_type": "history",
                "questions": [
                    {"id": "alp_level", "type": "number", "label": "Alkaline Phosphatase (ALP) Level", "required": True, "placeholder": "e.g., 185 (Note lab reference range)"},
                    {"id": "alp_ggt", "type": "number", "label": "GGT Level (If Available)", "required": False, "placeholder": "e.g., 92 (Raised GGT = Hepatobiliary Source)"},
                    {"id": "alp_pbc_screen", "type": "multi_select", "label": "PBC Screen", "required": True, "options": ["Itch / Pruritus", "Nausea", "Vomiting", "None - Absence Does NOT Exclude PBC"]},
                    {"id": "alp_meds", "type": "multi_select", "label": "Drug-Induced Liver Abnormalities", "required": True, "options": ["Methotrexate", "Azathioprine", "Nitrofurantoin", "Statins", "Terbinafine", "Carbamazepine", "None of the above"]}
                ]
            },
            {
                "title": "Step 1 Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "alp_step1_ggt", "type": "toggle", "label": "GGT Ordered?", "required": True},
                    {"id": "alp_step1_fbc", "type": "toggle", "label": "FBC Ordered?", "required": True},
                    {"id": "alp_ggt_result", "type": "single_select", "label": "GGT Result", "required": False, "options": ["GGT Raised → Hepatobiliary Source (Cholestasis)", "GGT Normal → ?Bone Source", "Awaiting Result"]},
                    {"id": "alp_ggt_mcv", "type": "toggle", "label": "GGT AND MCV Both Raised? → Consider Alcohol as Likely Cause", "required": False},
                    {"id": "alp_alt_raised", "type": "toggle", "label": "ALT Also Raised? → Consider Alcoholic Hepatitis", "required": False},
                    {"id": "alp_fbc_ggt_normal", "type": "toggle", "label": "FBC AND GGT Both Normal? → Check Vitamin D (Note Raised ALP on Request Form)", "required": False}
                ]
            },
            {
                "title": "Step 2 - If GGT Raised (Hepatobiliary Source)",
                "section_type": "assessment",
                "questions": [
                    {"id": "alp_fractionated", "type": "toggle", "label": "Fractionated Alkaline Phosphatase Ordered?", "required": False},
                    {"id": "alp_igm", "type": "toggle", "label": "IgM Ordered?", "required": False},
                    {"id": "alp_ama", "type": "toggle", "label": "Antimitochondrial Antibody (AMA) Ordered? (PBC Screen)", "required": False},
                    {"id": "alp_pbc_diagnosis", "type": "toggle", "label": "PBC Diagnostic Features? (Raised ALP + Raised GGT + AMA Positive = 2 of 3 Criteria)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: PBC confirmed (2 of 3 criteria met). Start Ursofalk (Ursodeoxycholic Acid). Refer gastroenterology/hepatology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Hepatobiliary Source (Raised GGT): PBC, Cholestasis, Malignancy",
                    "Primary Biliary Cholangitis (PBC): AMA Positive, IgM Raised, ALP + GGT Raised",
                    "Alcohol-Related (GGT + MCV Both Raised)",
                    "Alcoholic Hepatitis (GGT + ALT Raised)",
                    "Bone Source (Normal GGT): Paget's Disease, Osteomalacia (Vit D Deficiency), Metastases",
                    "Drug-Induced (Methotrexate, Azathioprine, Statins, etc.)",
                    "Inflammatory (Rheumatoid Arthritis - if hepatobiliary + bone excluded)",
                    "Pregnancy (Physiological - 3rd Trimester)",
                    "Benign Transient Hyperphosphatasaemia (Children)"
                ],
                "questions": [
                    {"id": "alp_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Hepatobiliary Source - Investigating", "?Bone Source - Investigating", "?PBC (AMA Positive)", "?Alcohol-Related", "?Drug-Induced", "Uncertain - Stepwise Investigation Ongoing"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Stepwise approach: Step 1 = GGT + FBC. If GGT raised = hepatobiliary source (cholestasis). Send fractionated ALP, IgM, AMA (PBC screen). If AMA positive + raised ALP + raised GGT = 2 of 3 diagnostic features consistent with PBC. PBC treatment: Ursofalk (Ursodeoxycholic Acid). Refer gastroenterology/hepatology. If GGT + MCV both raised = consider alcohol. If ALT also raised = consider alcoholic hepatitis. If FBC + GGT both normal = check Vitamin D (note raised ALP on request form to aid interpretation). ALP can also be raised due to inflammatory conditions (e.g., RA) if hepatobiliary and bone causes excluded. Drug-induced causes: methotrexate, azathioprine, nitrofurantoin, statins, terbinafine, carbamazepine.",
                "questions": [
                    {"id": "alp_pbc_rx", "type": "toggle", "label": "Ursofalk (Ursodeoxycholic Acid) Started? (If PBC Confirmed)", "required": False},
                    {"id": "alp_vit_d", "type": "toggle", "label": "Vitamin D Level Ordered? (If FBC + GGT Normal = ?Bone Source)", "required": False},
                    {"id": "alp_alcohol_advice", "type": "toggle", "label": "Alcohol Reduction Advised? (If GGT + MCV Raised)", "required": False},
                    {"id": "alp_drug_review", "type": "toggle", "label": "Causative Medication Reviewed? (Stop/Reduce if Drug-Induced)", "required": False},
                    {"id": "alp_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Stepwise Investigation)", "Gastroenterology / Hepatology (?PBC)", "Rheumatology (?Inflammatory Cause)"]},
                    {"id": "alp_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review with stepwise results, refer if PBC confirmed"}
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
    seed_raised_alp()