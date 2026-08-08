from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_abnormal_smear():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Positive HPV / Abnormal Cervical Cytology",
        "description": "Assessment and management of positive HPV result and abnormal cervical cytology. Covers CervicalCheck triage, colposcopy referral criteria, and patient counselling.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Result Details",
                "section_type": "history",
                "questions": [
                    {"id": "smr_hpv", "type": "single_select", "label": "HPV Result", "required": True, "options": ["HPV Positive (non-16/18)", "HPV 16/18 Positive", "HPV Negative"], "is_red_flag": True, "red_flag_positive": "RED FLAG: HPV 16/18 positive = highest risk for CIN/cancer. Ensure timely colposcopy referral.", "red_flag_negative": "", "output_phrase": "HPV: {value}"},
                    {"id": "smr_cytology", "type": "single_select", "label": "Cytology Result", "required": True, "options": ["Normal / Inadequate", "Borderline nuclear changes (BNC) / ASC-US", "Low-grade dyskaryosis (LSIL / CIN1)", "High-grade dyskaryosis (moderate — HSIL / CIN2)", "High-grade dyskaryosis (severe — HSIL / CIN3)", "?Glandular abnormality / ?AGC", "?Invasive carcinoma"], "is_red_flag": True, "red_flag_positive": "RED FLAG: High-grade dyskaryosis or ?invasion = urgent colposcopy. Glandular abnormality = urgent colposcopy.", "red_flag_negative": "", "output_phrase": "Cytology: {value}"}
                ]
            },
            {
                "title": "Management Pathway",
                "section_type": "history",
                "questions": [
                    {"id": "smr_previous", "type": "toggle", "label": "Previous Abnormal Smear / Colposcopy / Treatment?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous CIN treatment + new abnormality = higher risk. Ensure colposcopy referral.", "red_flag_negative": "", "output_phrase": "Previous: {value}"},
                    {"id": "smr_symptoms", "type": "multi_select", "label": "Symptoms (?cervical cancer)", "required": True, "options": ["Postcoital bleeding", "Intermenstrual bleeding", "Postmenopausal bleeding", "Vaginal discharge", "Pelvic pain", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Symptoms + abnormal cytology = ?cervical cancer. Urgent colposcopy (2-week wait).", "red_flag_negative": "", "output_phrase": "Symptoms: {value}"}
                ]
            },
            {
                "title": "Assessment & Triage",
                "section_type": "assessment",
                "differentials": ["HPV Positive + Normal Cytology — repeat in 12 months", "HPV Positive + Borderline/Low-Grade — colposcopy", "HPV 16/18 + Any Cytology — colposcopy", "High-Grade Dyskaryosis — urgent colposcopy", "?Glandular Abnormality — urgent colposcopy", "?Invasive — 2-week wait colposcopy"],
                "questions": [
                    {"id": "smr_diagnosis", "type": "single_select", "label": "Triage Outcome", "required": True, "options": ["Routine colposcopy (HPV + borderline/low-grade)", "Urgent colposcopy (high-grade/glandular)", "2-week wait (?invasion/symptoms)", "Repeat smear in 12 months (HPV + normal)", "HPV negative + normal — routine recall"], "output_phrase": "Triage: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Explain: HPV is very common — most clear spontaneously. Abnormal cytology does NOT mean cancer. Colposcopy is a closer look — may need biopsy. If HPV + normal cytology: Repeat smear in 12 months. If borderline/low-grade + HPV positive: Routine colposcopy. If high-grade/glandular: Urgent colposcopy (within 2-4 weeks). If symptoms suggestive of cancer: 2-week wait colposcopy. Advise: Continue screening even if previous normal results. Safety-net: Return if postcoital bleeding, intermenstrual bleeding, pelvic pain, or new discharge.",
                "questions": [
                    {"id": "smr_action", "type": "single_select", "label": "Action", "required": True, "options": ["Routine colposcopy referral", "Urgent colposcopy referral", "2-week wait colposcopy (cancer suspected)", "Repeat smear in 12 months", "Routine recall (3-5 years)"], "output_phrase": "Action: {value}"},
                    {"id": "smr_counselling", "type": "toggle", "label": "Patient Counselled? (HPV common, does not mean cancer, colposcopy process)", "required": True, "output_phrase": "Counselled: {value}"},
                    {"id": "smr_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if bleeding/pain/discharge)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "smr_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Colposcopy referral sent. GP review post-colposcopy. Repeat smear per colposcopy advice.", "output_phrase": "Follow-up: {value}"}
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
    seed_abnormal_smear()