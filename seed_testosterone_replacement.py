from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_testosterone_replacement():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Testosterone Replacement Therapy",
        "description": "Comprehensive testosterone replacement template covering diagnostic criteria (two fasting <8 nmol/L), Testogel prescribing, monitoring protocol, and safety considerations.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "trt_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Erectile Dysfunction", "Low Libido", "Fatigue", "Reduced Muscle Mass", "Low Mood", "Brain Fog"]},
                    {"id": "trt_diabetes", "type": "toggle", "label": "Diabetes? (Associated with Hypogonadism)", "required": True},
                    {"id": "trt_ihd", "type": "toggle", "label": "Ischaemic Heart Disease?", "required": True},
                    {"id": "trt_prostate_ca_personal", "type": "toggle", "label": "Personal History of Prostate Cancer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Prostate cancer = contraindication to testosterone replacement.", "red_flag_negative": ""},
                    {"id": "trt_prostate_ca_family", "type": "toggle", "label": "Family History of Prostate Cancer?", "required": True}
                ]
            },
            {
                "title": "Diagnostic Criteria - Testosterone Deficiency",
                "section_type": "assessment",
                "questions": [
                    {"id": "trt_testosterone_1", "type": "number", "label": "First Fasting Morning Testosterone (Before 11am) - nmol/L", "required": False, "placeholder": "e.g., 6.5"},
                    {"id": "trt_testosterone_2", "type": "number", "label": "Second Fasting Morning Testosterone (Before 11am) - nmol/L", "required": False, "placeholder": "e.g., 7.2"},
                    {"id": "trt_both_low", "type": "toggle", "label": "Both Levels <8 nmol/L? (Diagnostic of Testosterone Deficiency)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Confirmed deficiency = proceed to PSA + DRE before treatment.", "red_flag_negative": ""},
                    {"id": "trt_borderline", "type": "single_select", "label": "If Testosterone 8-12 nmol/L + Clinically Suspicious", "required": False, "options": ["Take Second Sample + SHBG", "Calculate Free Testosterone (If SHBG Low)", "Free Testosterone <0.225 nmol/L = Consistent with Deficiency", "Not Applicable"]},
                    {"id": "trt_severe_low", "type": "toggle", "label": "Testosterone <5.2 nmol/L? (Severe - Refer Endocrinology + Arrange FSH/LH/Prolactin)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe deficiency = refer endocrinology. Arrange FSH, LH, prolactin.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Safety Checks Before Treatment",
                "section_type": "examination",
                "questions": [
                    {"id": "trt_psa", "type": "number", "label": "PSA (ng/mL) - Must Be Normal Before Starting", "required": False, "placeholder": "e.g., 1.2", "is_red_flag": True, "red_flag_positive": "RED FLAG: Raised PSA = investigate before TRT. ?Prostate cancer.", "red_flag_negative": ""},
                    {"id": "trt_dre_size", "type": "single_select", "label": "DRE: Prostate Size", "required": False, "options": ["Normal", "Enlarged", "Not Examined"]},
                    {"id": "trt_dre_consistency", "type": "single_select", "label": "DRE: Consistency", "required": False, "options": ["Smooth - Normal", "Irregular / Hard - RED FLAG", "Not Examined"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspicious DRE = investigate before TRT. Refer urology.", "red_flag_negative": ""},
                    {"id": "trt_dre_symmetry", "type": "single_select", "label": "DRE: Symmetry", "required": False, "options": ["Symmetrical", "Asymmetrical", "Not Examined"]}
                ]
            },
            {
                "title": "Pre-Treatment Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "trt_bloods", "type": "multi_select", "label": "Bloods Ordered Before Starting", "required": False, "options": ["FBC (Baseline Haematocrit)", "PSA", "Testosterone", "Prolactin", "FSH", "LH", "Iron Levels"]}
                ]
            },
            {
                "title": "Patient Counselling",
                "section_type": "plan",
                "questions": [
                    {"id": "trt_counselling_benefits", "type": "toggle", "label": "Benefits Explained? (Improves Energy + ED, Full Effect May Take Up to 6 Months)", "required": True},
                    {"id": "trt_counselling_bp", "type": "toggle", "label": "Can Increase Blood Pressure Explained?", "required": True},
                    {"id": "trt_counselling_polycythaemia", "type": "toggle", "label": "Can Cause Polycythaemia (Raised Haematocrit) Explained?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haematocrit must remain <52%. If >52% = venesection or stop treatment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Treatment: Testogel pump - 2 actuations, one to each upper arm/shoulder, applied 2 hours before showering. Alternative: 1 sachet Testogel/Testim once daily to shoulders/upper arms, 6 hours before showering. Monitoring: repeat PSA, testosterone, lipids, FBC (haematocrit), LFT at 3-6 months, then annually. Haematocrit MUST remain <52%. If no clinical benefit after 3-6 months: discontinue treatment. If treatment stopped: patient's own endogenous testosterone at that point reflects true baseline (not confounded by residual exogenous effect) - useful if reassessing ongoing need. If testosterone <5.2 nmol/L: refer endocrinology + arrange FSH/LH/Prolactin.",
                "questions": [
                    {"id": "trt_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Testosterone Deficiency Confirmed (2 Fasting <8 nmol/L + Normal PSA + Normal DRE)", "Borderline - Needs SHBG/Free Testosterone", "Severe - Refer Endocrinology", "Not Deficient - No Treatment"]},
                    {"id": "trt_treatment", "type": "single_select", "label": "Treatment", "required": False, "options": ["Testogel Pump: 2 Actuations, One to Each Upper Arm/Shoulder, 2h Before Shower", "Testogel/Testim Sachet: 1 Daily to Shoulders/Upper Arms, 6h Before Shower", "Not Started - Awaiting Results / Referred"]},
                    {"id": "trt_monitoring", "type": "multi_select", "label": "Monitoring at 3-6 Months, Then Annually", "required": False, "options": ["PSA", "Testosterone", "Lipids", "FBC (Haematocrit <52%)", "LFTs"]},
                    {"id": "trt_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "Endocrinology (Severe / <5.2 nmol/L)", "Urology (?Prostate Cancer)"]},
                    {"id": "trt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3-6 months with bloods, then annually. Discontinue if no benefit."}
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
    seed_testosterone_replacement()