from app.database import SessionLocal
from app.models import User, Template, Category

def seed_acr():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "ACR (Albumin:Creatinine Ratio) Assessment",
        "description": "Focused assessment for interpreting urine ACR results covering diagnostic thresholds, ACE inhibitor indications, BP targets, and nephrology referral criteria.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Testing Context",
                "section_type": "history",
                "questions": [
                    {"id": "acr_reason", "type": "single_select", "label": "Reason for Testing", "required": True, "options": ["Diabetes mellitus annual review", "Hypertension screening", "CKD monitoring", "Incidental finding", "Other"]},
                    {"id": "acr_samples", "type": "number", "label": "Number of Samples Taken", "required": True, "placeholder": "e.g., 2 (need 3 to confirm persistent proteinuria)"},
                    {"id": "acr_positive_count", "type": "single_select", "label": "Number of Positive Results", "required": True, "options": ["0/3", "1/3", "2/3 (CONFIRMED - persistent proteinuria)", "3/3 (CONFIRMED - persistent proteinuria)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: 2/3 positive within 6 months = confirmed persistent proteinuria. Start ACEi, statin, BP control based on eGFR.", "red_flag_negative": ""},
                    {"id": "acr_timeframe", "type": "single_select", "label": "Timeframe of Samples", "required": True, "options": ["Within 6 months", ">6 months apart"]}
                ]
            },
            {
                "title": "ACR Result & Risk Factors",
                "section_type": "assessment",
                "questions": [
                    {"id": "acr_value", "type": "number", "label": "ACR Value (mg/mmol)", "required": True, "placeholder": "e.g., 45"},
                    {"id": "acr_category", "type": "single_select", "label": "ACR Category", "required": True, "options": ["<3 mg/mmol - NORMAL", "3-30 mg/mmol - MODERATELY INCREASED (Microalbuminuria)", ">30 mg/mmol - SEVERELY INCREASED (Proteinuria)", ">70 mg/mmol - SEVERELY INCREASED (≈1g/24h proteinuria)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ACR >70 = equivalent to PCR 100 or ~1g/24h proteinuria. Stricter BP targets + ACEi + nephrology consideration.", "red_flag_negative": ""},
                    {"id": "acr_diabetes", "type": "toggle", "label": "Diabetes Mellitus?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: DM + ACR >3 = ACEi indicated (renoprotection).", "red_flag_negative": ""},
                    {"id": "acr_hypertension", "type": "toggle", "label": "Hypertension?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: HTN + ACR >30 = ACEi indicated.", "red_flag_negative": ""},
                    {"id": "acr_egfr", "type": "number", "label": "eGFR (mL/min/1.73m²)", "required": True, "placeholder": "e.g., 52", "is_red_flag": True, "red_flag_positive": "RED FLAG: eGFR <60 + proteinuria = CKD. eGFR <30 = nephrology referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Impression",
                "section_type": "assessment",
                "differentials": [
                    "Normal ACR - No Action",
                    "Transient Proteinuria (UTI, exercise, fever - repeat)",
                    "Persistent Microalbuminuria (ACR 3-30) - Diabetic Nephropathy",
                    "Persistent Proteinuria (ACR >30) - CKD",
                    "Nephrotic Range Proteinuria (ACR >70) - Nephrology Referral",
                    "Orthostatic Proteinuria (benign, young adults)"
                ],
                "questions": [
                    {"id": "acr_impression", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Normal ACR - no action", "Moderately increased ACR - confirmed x2/3", "Severely increased ACR - confirmed x2/3", "Severely increased ACR >70 - stricter BP target", "Single positive result - repeat testing required", "Suspected transient proteinuria - repeat after UTI/exercise"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "ACR interpretation: single raised ACR should be confirmed with repeat testing (2/3 positive within 6 months = persistent proteinuria). ACEi indications: DM + ACR >3, HTN + ACR >30, or ACR >70 regardless of DM/HTN status. ACR >70 = stricter BP targets in non-diabetic patients. Statin + BP control decisions depend on eGFR. Refer nephrology if: severely increased ACR with declining eGFR, diagnostic uncertainty, or nephrotic range proteinuria. Repeat ACR monitoring: 6-monthly if confirmed proteinuria, annually if normal in at-risk patients.",
                "questions": [
                    {"id": "acr_confirmatory", "type": "single_select", "label": "Confirmatory Testing", "required": True, "options": ["Repeat ACR - confirm with 3 samples within 6 months", "No further testing - result normal", "Diagnosis confirmed (2/3 positive) - proceed to management"]},
                    {"id": "acr_pharmacotherapy", "type": "multi_select", "label": "Pharmacotherapy", "required": False, "options": ["ACE Inhibitor (DM + ACR >3 / HTN + ACR >30 / ACR >70)", "ARB (if ACEi not tolerated)", "Statin (eGFR dependent)", "Neither indicated at this stage"]},
                    {"id": "acr_bp_target", "type": "single_select", "label": "BP Target", "required": False, "options": ["Standard BP target (<140/90)", "Stricter BP target (<130/80 - if ACR >70 non-diabetic)", "Not applicable"]},
                    {"id": "acr_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP managed", "Nephrology - severely increased ACR + declining eGFR", "Nephrology - diagnostic uncertainty", "Diabetes team - DM-related nephropathy"]},
                    {"id": "acr_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat ACR in 6 months, annual review, sooner if eGFR declines"}
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
    seed_acr()