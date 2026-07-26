from app.database import SessionLocal
from app.models import User, Template, Category

def seed_raised_creatinine():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Creatinine Assessment",
        "description": "Structured assessment for raised creatinine covering spurious causes (cimetidine/trimethoprim), CKD staging, and stepwise renal investigation.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirmation & Medication Review",
                "section_type": "history",
                "questions": [
                    {"id": "rcr_creatinine", "type": "number", "label": "Serum Creatinine (µmol/L) - NR: 60-110", "required": True, "placeholder": "e.g., 145"},
                    {"id": "rcr_egfr", "type": "number", "label": "eGFR (mL/min/1.73m²)", "required": False, "placeholder": "e.g., 42"},
                    {"id": "rcr_repeat_confirmed", "type": "toggle", "label": "Raised Creatinine Confirmed on Repeat Testing? (Not One-Off / Lab Error)", "required": True},
                    {"id": "rcr_cimetidine", "type": "toggle", "label": "Recent Cimetidine Use?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cimetidine can raise creatinine by up to 15% by blocking tubular secretion = SPURIOUS rise, not true GFR fall. Also blocks K+ secretion = caution with ACEi/ARB/Spironolactone.", "red_flag_negative": ""},
                    {"id": "rcr_trimethoprim", "type": "toggle", "label": "Recent Trimethoprim Use?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Trimethoprim can raise creatinine by up to 15% = spurious rise. Also blocks K+ secretion = hyperkalaemia risk with ACEi/ARB/Spironolactone.", "red_flag_negative": ""},
                    {"id": "rcr_spurious", "type": "toggle", "label": "Spurious Rise Due to Cimetidine/Trimethoprim? (Not True GFR Fall)", "required": True}
                ]
            },
            {
                "title": "Examination & Risk Factors",
                "section_type": "examination",
                "questions": [
                    {"id": "rcr_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 148/88"},
                    {"id": "rcr_meds_nephrotoxic", "type": "multi_select", "label": "Nephrotoxic / Contributing Medications", "required": True, "options": ["ACE Inhibitor (Ramipril/Lisinopril)", "ARB (Losartan/Candesartan)", "Diuretics", "NSAIDs", "PPI", "Spironolactone", "None"]},
                    {"id": "rcr_pmh", "type": "multi_select", "label": "Relevant PMHx", "required": True, "options": ["Diabetes", "Hypertension", "Heart Failure", "Liver Disease", "Known CKD", "None"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "rcr_urine_dip", "type": "multi_select", "label": "Urine Dipstick Findings", "required": False, "options": ["Haematuria", "Proteinuria", "Glucose", "Leucocytes", "Normal", "Not yet performed"]},
                    {"id": "rcr_renal_profile", "type": "toggle", "label": "Renal Profile (U&Es) Ordered?", "required": False},
                    {"id": "rcr_uacr", "type": "toggle", "label": "Urinary ACR Ordered?", "required": False},
                    {"id": "rcr_bone_profile", "type": "toggle", "label": "Bone / Renal Profile (Calcium, Phosphate, ALP) Ordered?", "required": False},
                    {"id": "rcr_pth", "type": "toggle", "label": "PTH Ordered? (Screen for Hyperparathyroidism)", "required": False},
                    {"id": "rcr_pcr", "type": "toggle", "label": "Protein:Creatinine Ratio? (Non-Diabetic - Detect Free Light Chains / ?Myeloma)", "required": False}
                ]
            },
            {
                "title": "CKD Staging",
                "section_type": "assessment",
                "differentials": [
                    "Drug-Induced (Cimetidine/Trimethoprim = Spurious Rise)",
                    "Pre-Renal (Dehydration, Heart Failure, NSAIDs, ACEi/ARB)",
                    "Renal: Acute Kidney Injury (AKI)",
                    "Renal: Chronic Kidney Disease (CKD - Diabetic, Hypertensive, Glomerulonephritis)",
                    "Renal: Tubulointerstitial Nephritis (PPI, NSAIDs)",
                    "Post-Renal: Obstruction (BPH, Stone, Mass)",
                    "Myeloma (Free Light Chains - PCR in Non-Diabetic)"
                ],
                "questions": [
                    {"id": "rcr_ckd_stage", "type": "single_select", "label": "CKD Stage (Based on eGFR)", "required": False, "options": ["Stage 1: eGFR ≥90 + Proteinuria/Haematuria", "Stage 2: eGFR 60-89 + Proteinuria/Haematuria", "Stage 3a: eGFR 45-59", "Stage 3b: eGFR 30-44", "Stage 4: eGFR 15-29", "Stage 5: eGFR <15", "Not CKD - Spurious / AKI"]},
                    {"id": "rcr_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Spurious Rise (Cimetidine/Trimethoprim) - No Further Action", "?Pre-Renal Cause (Dehydration/Drugs)", "?CKD - Staging Required", "?AKI - Urgent Assessment", "?Post-Renal Obstruction", "?Myeloma (Check PCR)"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Cimetidine and trimethoprim can raise serum creatinine by up to 15% by blocking tubular secretion = SPURIOUS rise, not true fall in GFR. Both also block potassium secretion = CAUTION if used concurrently with ACE inhibitors, ARBs, or spironolactone (increased risk of sudden death via hyperkalaemia). Repeat creatinine to confirm persistent elevation. Check urine dipstick (haematuria, proteinuria, glucose, leucocytes). Renal profile, eGFR, urinary ACR, bone/renal profile (calcium), PTH. In non-diabetic patients: protein:creatinine ratio can detect free light chains (?myeloma). CKD staging based on eGFR + ACR. Refer nephrology if: eGFR <30, rapidly declining eGFR, proteinuria, or diagnostic uncertainty.",
                "questions": [
                    {"id": "rcr_hyperkalaemia_warning", "type": "toggle", "label": "Hyperkalaemia Risk Discussed? (Cimetidine/Trimethoprim + ACEi/ARB/Spironolactone = Sudden Death Risk)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cimetidine/Trimethoprim + ACEi/ARB/Spironolactone = increased risk of sudden death via hyperkalaemia.", "red_flag_negative": ""},
                    {"id": "rcr_med_review", "type": "toggle", "label": "Nephrotoxic Medications Reviewed? (NSAIDs, ACEi/ARB Hold if AKI)", "required": False},
                    {"id": "rcr_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Mild CKD / Spurious)", "Nephrology (eGFR <30 / Rapid Decline / Proteinuria)", "Urology (?Post-Renal Obstruction)", "Haematology (?Myeloma)"]},
                    {"id": "rcr_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat U&Es + ACR, stage CKD, refer if indicated"}
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
    seed_raised_creatinine()