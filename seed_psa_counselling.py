from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_psa_counselling():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "PSA Levels - Shared Decision-Making",
        "description": "Shared decision-making template for PSA testing covering poor specificity/sensitivity counselling, pre-test preparation, age-adjusted thresholds (NICE NG12 2025), and finasteride correction.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "Reason & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "psa_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 58"},
                    {"id": "psa_reason", "type": "single_select", "label": "Reason for Enquiry", "required": True, "options": ["Patient-Initiated Request", "GP-Initiated (LUTS / Risk Factors)", "Follow-Up of Previous Raised PSA", "Family History Concern"]},
                    {"id": "psa_fh_prostate", "type": "toggle", "label": "Family History of Prostate Cancer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx prostate cancer = increased risk. Lower threshold for testing.", "red_flag_negative": ""},
                    {"id": "psa_luts", "type": "multi_select", "label": "LUTS Screen", "required": True, "options": ["Incomplete Bladder Emptying", "Hesitancy", "Urgency", "Frequency", "Nocturia", "None"]}
                ]
            },
            {
                "title": "Shared Decision-Making - PSA Limitations",
                "section_type": "history",
                "questions": [
                    {"id": "psa_poor_specificity", "type": "toggle", "label": "Poor Specificity Explained? (~3/4 Men with PSA >3 ng/mL Do NOT Have Prostate Cancer - False Positives: BPH, UTI, Recent DRE)", "required": True},
                    {"id": "psa_poor_sensitivity", "type": "toggle", "label": "Poor Sensitivity Explained? (~15% Men with Normal PSA Still Have Prostate Cancer)", "required": True},
                    {"id": "psa_no_survival_benefit", "type": "toggle", "label": "No Conclusive Evidence That Early Detection Through Screening Improves Survival Explained?", "required": True},
                    {"id": "psa_patient_leaflet", "type": "toggle", "label": "HSE Patient Information Leaflet Provided? (https://www.hse.ie/eng/services/publications/topics/prostateassessmentleaflet.pdf)", "required": False},
                    {"id": "psa_risk_calculator", "type": "toggle", "label": "Risk Calculator Used? (https://www.prostatecancer-riskcalculator.com)", "required": False},
                    {"id": "psa_decision", "type": "toggle", "label": "Patient Counselled + Wishes to Proceed with Testing? (Document Decision)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Document informed consent discussion. Patient understands limitations of PSA testing.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Pre-Test Preparation - Confirm BEFORE Testing",
                "section_type": "history",
                "questions": [
                    {"id": "psa_no_uti", "type": "toggle", "label": "No UTI Within Last 6 Weeks? (Falsely Raises PSA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent UTI = falsely raised PSA. Delay testing.", "red_flag_negative": ""},
                    {"id": "psa_no_ejaculation", "type": "toggle", "label": "No Ejaculation Within Last 48 Hours? (Falsely Raises PSA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent ejaculation = falsely raised PSA. Delay testing.", "red_flag_negative": ""},
                    {"id": "psa_no_exercise", "type": "toggle", "label": "No Vigorous Exercise (Especially Cycling) Within Last 48 Hours? (Falsely Raises PSA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent vigorous exercise = falsely raised PSA. Delay testing.", "red_flag_negative": ""},
                    {"id": "psa_no_dre", "type": "toggle", "label": "No DRE Within Last Week? (Falsely Raises PSA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent DRE = falsely raised PSA. Perform DRE AFTER blood draw.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "psa_dre_size", "type": "single_select", "label": "DRE: Prostate Size (Perform AFTER Blood Draw)", "required": False, "options": ["Normal", "Enlarged", "Not Examined"]},
                    {"id": "psa_dre_consistency", "type": "single_select", "label": "DRE: Consistency", "required": False, "options": ["Smooth", "Irregular / Nodular - RED FLAG", "Hard - RED FLAG", "Not Examined"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspicious DRE = refer RAPC irrespective of PSA result.", "red_flag_negative": ""},
                    {"id": "psa_dre_symmetry", "type": "single_select", "label": "DRE: Symmetry", "required": False, "options": ["Symmetrical", "Asymmetrical", "Not Examined"]}
                ]
            },
            {
                "title": "PSA Result & Age-Adjusted Thresholds (NICE NG12, May 2025)",
                "section_type": "assessment",
                "questions": [
                    {"id": "psa_result", "type": "number", "label": "PSA Result (ng/mL)", "required": False, "placeholder": "e.g., 4.2"},
                    {"id": "psa_finasteride", "type": "toggle", "label": "Taking Finasteride? (If Yes = DOUBLE Measured PSA Before Comparing to Thresholds)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Finasteride suppresses PSA. DOUBLE the measured value before interpreting.", "red_flag_negative": ""},
                    {"id": "psa_corrected", "type": "number", "label": "Corrected PSA (Doubled if on Finasteride)", "required": False, "placeholder": "e.g., 8.4"},
                    {"id": "psa_threshold", "type": "single_select", "label": "Age-Adjusted Threshold (Based on Patient Age)", "required": False, "options": ["40-49 Years: >2.5 ng/mL", "50-59 Years: >3.5 ng/mL", "60-69 Years: >4.5 ng/mL", "70-79 Years: >6.5 ng/mL", "Not Applicable"]},
                    {"id": "psa_raised", "type": "toggle", "label": "PSA Raised for Age? (After Finasteride Correction if Applicable)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Raised PSA = repeat in 6-12 weeks. If still raised + suspicious DRE = refer RAPC/urology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Plan",
                "section_type": "plan",
                "safety_netting": "PSA limitations: ~3/4 men with PSA >3 do NOT have cancer (false positives: BPH, UTI, recent DRE/exercise/ejaculation). ~15% with normal PSA still have cancer. No conclusive evidence PSA screening improves survival. Pre-test preparation: no UTI <6 weeks, no ejaculation <48h, no vigorous exercise <48h, no DRE <1 week (perform DRE AFTER blood draw). Finasteride doubles the measured PSA - correct before comparing to thresholds. If raised: repeat PSA 6-12 weeks. If still raised + suspicious DRE = refer RAPC. If normal + non-suspicious DRE = reassure, no further action. Reference: RACGP prostate cancer screening guideline. Risk calculator: prostatecancer-riskcalculator.com. HSE leaflet: hse.ie/prostateassessmentleaflet.",
                "questions": [
                    {"id": "psa_action", "type": "single_select", "label": "Action", "required": True, "options": ["PSA Normal for Age - Reassure, No Further Action", "PSA Raised - Repeat in 6-12 Weeks", "PSA Raised + Suspicious DRE - Refer RAPC / Urology", "Awaiting PSA Result", "Declined Testing After Counselling"]},
                    {"id": "psa_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat PSA in 6-12 weeks, refer RAPC if raised, or reassure"}
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
    seed_psa_counselling()