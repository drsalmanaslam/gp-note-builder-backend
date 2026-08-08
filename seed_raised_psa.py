from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_psa():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised PSA",
        "description": "Assessment of elevated PSA. Covers age-specific ranges, benign vs malignant causes, and rapid access prostate clinic referral criteria.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Context",
                "section_type": "history",
                "questions": [
                    {"id": "psa_level", "type": "text", "label": "PSA Level (ng/mL)", "required": True, "placeholder": "e.g., 8.5", "output_phrase": "PSA: {value} ng/mL"},
                    {"id": "psa_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 68", "output_phrase": "Age: {value}"},
                    {"id": "psa_previous", "type": "text", "label": "Previous PSA + Date (if known)", "required": False, "placeholder": "e.g., 4.2 — 1 year ago", "is_red_flag": True, "red_flag_positive": "RED FLAG: PSA velocity >0.75/year or doubling time <3 years = ?prostate cancer. Refer RAPC.", "red_flag_negative": "", "output_phrase": "Previous: {value}"}
                ]
            },
            {
                "title": "Benign Causes",
                "section_type": "history",
                "questions": [
                    {"id": "psa_uti", "type": "toggle", "label": "UTI / Prostatitis Symptoms? (dysuria, frequency, perineal pain)", "required": True, "output_phrase": "UTI/Prostatitis: {value}"},
                    {"id": "psa_instrumentation", "type": "toggle", "label": "Recent Catheter / Instrumentation / Ejaculation (<48h)?", "required": True, "output_phrase": "Instrumentation: {value}"},
                    {"id": "psa_bph", "type": "toggle", "label": "LUTS / BPH Symptoms? (hesitancy, poor stream, nocturia)", "required": True, "output_phrase": "BPH: {value}"}
                ]
            },
            {
                "title": "Red Flags — ?Prostate Cancer",
                "section_type": "history",
                "questions": [
                    {"id": "psa_weight_loss", "type": "toggle", "label": "Weight Loss / Bone Pain / Back Pain? (?metastatic disease)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bone pain/weight loss + raised PSA = ?metastatic prostate cancer. Urgent RAPC referral.", "red_flag_negative": "", "output_phrase": "Metastatic: {value}"},
                    {"id": "psa_dre", "type": "single_select", "label": "DRE Findings", "required": True, "options": ["Normal — smooth, symmetrical", "Enlarged — BPH pattern", "Hard / nodular / asymmetrical — ?malignancy", "Not examined"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Hard/nodular prostate = ?cancer. Urgent RAPC referral regardless of PSA.", "red_flag_negative": "", "output_phrase": "DRE: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Benign Prostatic Hyperplasia", "Prostatitis / UTI", "Prostate Cancer", "Recent Ejaculation / Instrumentation", "Age-related PSA rise"],
                "questions": [
                    {"id": "psa_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?BPH — monitor + repeat", "?Prostatitis — treat + repeat PSA in 6 weeks", "?Prostate cancer — RAPC referral", "Incidental — repeat after 6 weeks (no recent triggers)", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If UTI/prostatitis: Treat, repeat PSA in 6 weeks. If BPH + PSA mildly raised: Repeat in 3-6 months. Refer RAPC (Rapid Access Prostate Clinic) if: PSA > age-specific range, hard/nodular DRE, PSA velocity >0.75/year, bone pain/weight loss. Age-specific PSA upper limits: Age 50-59: 3.0, 60-69: 4.0, 70-79: 5.0, >80: 6.0. Safety-net: Return if bone pain, weight loss, urinary retention, or haematuria.",
                "questions": [
                    {"id": "psa_action", "type": "single_select", "label": "Action", "required": True, "options": ["Repeat PSA (post-infection/instrumentation)", "RAPC referral (cancer suspected)", "Monitor + repeat (BPH)", "Reassure (normal for age)"], "output_phrase": "Action: {value}"},
                    {"id": "psa_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "psa_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat PSA in 6 weeks. RAPC referral if persistent elevation.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]; existing.content = t["content"]; existing.category = t["category"]; existing.is_public = t["is_public"]; existing.updated_at = datetime.now(timezone.utc)
        db.commit(); print(f"Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t); db.commit(); print(f"Created: {t['title']}")
    db.close()

if __name__ == "__main__":
    seed_raised_psa()