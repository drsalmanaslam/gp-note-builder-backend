from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_calprotectin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Raised Faecal Calprotectin",
        "description": "Assessment of elevated faecal calprotectin. Differentiates IBD from IBS, guides gastroenterology referral urgency.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Level",
                "section_type": "history",
                "questions": [
                    {"id": "fcal_level", "type": "text", "label": "Calprotectin Level (ug/g)", "required": True, "placeholder": "e.g., 350", "is_red_flag": True, "red_flag_positive": "RED FLAG: Calprotectin >250 = high probability IBD. Urgent gastroenterology referral.", "red_flag_negative": "", "output_phrase": "Calprotectin: {value} ug/g"},
                    {"id": "fcal_symptoms", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Diarrhoea >4 weeks", "Abdominal pain", "Rectal bleeding", "Weight loss", "Nocturnal symptoms", "Extraintestinal (joints, eyes, skin)", "None"], "output_phrase": "Symptoms: {value}"}
                ]
            },
            {
                "title": "Causes",
                "section_type": "history",
                "questions": [
                    {"id": "fcal_nsaids", "type": "toggle", "label": "On NSAIDs / Aspirin? (can raise calprotectin)", "required": True, "output_phrase": "NSAIDs: {value}"},
                    {"id": "fcal_infection", "type": "toggle", "label": "Recent Gastroenteritis? (can transiently raise)", "required": True, "output_phrase": "Infection: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Inflammatory Bowel Disease (Crohn's / UC)", "Acute Infective Gastroenteritis", "NSAID Enteropathy", "Colorectal Cancer (usually normal or mildly elevated)", "Irritable Bowel Syndrome (normal calprotectin)"],
                "questions": [
                    {"id": "fcal_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?IBD — urgent gastroenterology referral (>250)", "?IBD — routine gastroenterology referral (100-250)", "?Infection — repeat after resolution", "?NSAID-related — stop + repeat", "IBS — calprotectin normal/reassuring"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Calprotectin >250: Urgent gastroenterology referral for colonoscopy. 100-250: Refer gastroenterology routinely. 50-100: Borderline — repeat in 4-6 weeks. Treat any infection. Stop NSAIDs. Check FBC, CRP, coeliac screen. Safety-net: Return if worsening diarrhoea, bleeding, weight loss, or nocturnal symptoms.",
                "questions": [
                    {"id": "fcal_action", "type": "single_select", "label": "Action", "required": True, "options": ["Urgent gastro referral (>250)", "Routine gastro referral (100-250)", "Repeat in 4-6 weeks (borderline)", "Stop NSAIDs + repeat", "Reassure (normal)"], "output_phrase": "Action: {value}"},
                    {"id": "fcal_safety_net", "type": "toggle", "label": "Safety-Net Given?", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "fcal_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Urgent gastro referral. GP review in 2 weeks.", "output_phrase": "Follow-up: {value}"}
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
    seed_raised_calprotectin()