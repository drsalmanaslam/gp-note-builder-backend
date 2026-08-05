from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_hidradenitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category:
        category = Category(name="Dermatology")
        db.add(category)
        db.commit()

    t = {
        "title": "Hidradenitis Suppurativa",
        "description": "Assessment of hidradenitis suppurativa including Hurley staging, severity assessment, management from lifestyle to biologics, and referral criteria.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "hs_sites", "type": "multi_select", "label": "Affected Areas", "required": True, "options": ["Axillae", "Groin / perineum", "Inframammary", "Buttocks", "Perianal", "Other"], "output_phrase": "Sites: {value}"},
                    {"id": "hs_lesions", "type": "multi_select", "label": "Type of Lesions", "required": True, "options": ["Painful nodules / boils", "Abscesses", "Sinus tracts / tunnelling", "Scarring", "Double comedones", "Chronic draining wounds"], "output_phrase": "Lesions: {value}"},
                    {"id": "hs_duration", "type": "text", "label": "Duration & Frequency of Flares", "required": True, "placeholder": "e.g., Monthly flares for 5 years", "output_phrase": "Duration: {value}"}
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "hs_risk", "type": "multi_select", "label": "Risk Factors", "required": True, "options": ["Smoking", "Obesity / overweight", "Family history", "Hormonal — worse pre-menstrually", "Diabetes / metabolic syndrome", "Crohn's disease", "None"], "output_phrase": "Risk factors: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Hidradenitis Suppurativa", "Recurrent furunculosis", "Crohn's disease (fistulating)", "Pilonidal sinus", "Actinomycosis", "Lymphogranuloma venereum"],
                "questions": [
                    {"id": "hs_hurley", "type": "single_select", "label": "Hurley Stage", "required": True, "options": ["I — Single/multiple nodules, no sinus tracts or scarring", "II — Recurrent nodules + sinus tracts + scarring (single region)", "III — Diffuse involvement with interconnected sinus tracts and abscesses"], "output_phrase": "Hurley: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "General: Smoking cessation, weight loss (even 10% improves outcomes), avoid tight clothing, antiseptic washes (chlorhexidine/Hibiscrub). Hurley I: Topical Clindamycin 1% BD. If fails, oral Tetracycline (Lymecycline 300mg OD) for 12 weeks. Hurley II-III: Oral Tetracycline + Rifampicin (300mg BD each) for 12 weeks. Consider Metformin if BMI >25. If failed oral therapy: Refer dermatology for Adalimumab (biologic, anti-TNF). Acute abscess: Incision & drainage if fluctuant — but avoid wide excision (promotes sinus formation). Refer urgently if: extensive sinus tracts, severe pain, systemic symptoms. Safety-net: Return if spreading infection, systemic illness, or no improvement.",
                "questions": [
                    {"id": "hs_treatment", "type": "single_select", "label": "Treatment", "required": True, "options": ["General measures + topical Clindamycin", "Oral Tetracycline ± Rifampicin", "Refer dermatology — biologic consideration", "Refer dermatology — surgical (Hurley III)", "Acute abscess — I&D + antibiotics"], "output_phrase": "Treatment: {value}"},
                    {"id": "hs_lifestyle", "type": "toggle", "label": "Smoking Cessation / Weight Loss Advised?", "required": True, "output_phrase": "Lifestyle advice: {value}"},
                    {"id": "hs_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 12 weeks. If no response to antibiotics, refer dermatology.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created!")
    db.close()

if __name__ == "__main__":
    seed_hidradenitis()