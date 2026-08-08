from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_positive_fit():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Positive FIT (Faecal Immunochemical Test)",
        "description": "Assessment of positive FIT. Covers risk stratification, differentials beyond cancer, and urgent colorectal referral criteria.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Level",
                "section_type": "history",
                "questions": [
                    {"id": "fit_level", "type": "text", "label": "FIT Result (ug Hb/g faeces)", "required": True, "placeholder": "e.g., 45", "is_red_flag": True, "red_flag_positive": "RED FLAG: FIT ≥10 = positive. ≥100 = higher risk. Urgent 2-week wait colorectal referral.", "red_flag_negative": "", "output_phrase": "FIT: {value} ug/g"},
                    {"id": "fit_symptoms", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Change in bowel habit", "Rectal bleeding", "Abdominal pain", "Weight loss", "Anaemia", "Abdominal mass", "None — screening"], "output_phrase": "Symptoms: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "fit_red_flags", "type": "multi_select", "label": "Red Flag Features (?colorectal cancer)", "required": True, "options": ["Age >40 with change in bowel habit + blood", "Persistent rectal bleeding without anal symptoms", "Iron deficiency anaemia (male or postmenopausal female)", "Palpable abdominal or rectal mass", "Weight loss", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Red flag symptoms + positive FIT = urgent 2-week wait colorectal referral.", "red_flag_negative": "", "output_phrase": "Red flags: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Colorectal Cancer", "Colorectal Polyps", "Inflammatory Bowel Disease", "Haemorrhoids", "Diverticular Disease", "Anal Fissure", "Angiodysplasia"],
                "questions": [
                    {"id": "fit_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Colorectal cancer — 2-week wait referral", "?IBD — refer gastroenterology", "?Benign anorectal — examine + treat", "Positive FIT only — no symptoms — refer colorectal"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "FIT ≥10: Refer colorectal clinic (2-week wait if red flags). FIT <10 + symptoms: Clinical judgement — consider routine referral. Examine abdomen + DRE. Check FBC, iron studies. Do NOT repeat FIT — once positive, needs investigation regardless. Safety-net: Return if worsening symptoms, weight loss, or obstruction symptoms.",
                "questions": [
                    {"id": "fit_action", "type": "single_select", "label": "Action", "required": True, "options": ["2-week wait colorectal referral", "Routine colorectal referral", "Examine + treat benign cause + safety-net", "Gastroenterology referral (?IBD)"], "output_phrase": "Action: {value}"},
                    {"id": "fit_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "fit_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., 2-week wait referral sent. GP to follow up post-colonoscopy.", "output_phrase": "Follow-up: {value}"}
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
    seed_positive_fit()