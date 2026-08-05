from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_cold_sores():
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
        "title": "Cold Sores (Herpes Simplex Virus)",
        "description": "Assessment and management of HSV-1 cold sores. Covers triggers, stages, treatment (topical/oral antivirals), red flags for complications, and immunocompromised considerations.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "cs_stage", "type": "single_select", "label": "Current Stage", "required": True, "options": ["Prodrome — tingling/burning (best time to treat)", "Vesicles — fluid-filled blisters", "Ulceration — crusting", "Healing — scabbed", "Recurrent — frequent episodes"], "output_phrase": "Stage: {value}"},
                    {"id": "cs_frequency", "type": "single_select", "label": "Frequency", "required": True, "options": ["First episode", "Rare — <2 per year", "Frequent — 3-6 per year", "Very frequent — >6 per year"], "output_phrase": "Frequency: {value}"},
                    {"id": "cs_triggers", "type": "multi_select", "label": "Triggers", "required": False, "options": ["Sunlight / UV exposure", "Stress / fatigue", "Febrile illness", "Menstruation", "Trauma / dental procedures", "Unknown"], "output_phrase": "Triggers: {value}"}
                ]
            },
            {
                "title": "Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "cs_eye", "type": "toggle", "label": "Eye Involvement? (pain, redness, vision change — ?herpes keratitis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Herpes keratitis = ophthalmology emergency. Same-day ophthalmology referral. Do not use topical steroids.", "red_flag_negative": "", "output_phrase": "Eye: {value}"},
                    {"id": "cs_extensive", "type": "toggle", "label": "Extensive / Disseminated? (large area, multiple sites)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Disseminated HSV = ?immunocompromised. Consider HIV test. Oral Aciclovir 400mg 5x/day. Refer if severe.", "red_flag_negative": "", "output_phrase": "Extensive: {value}"},
                    {"id": "cs_immunocompromised", "type": "toggle", "label": "Immunocompromised? (chemo, transplant, HIV, high-dose steroids)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunocompromised + HSV = risk of disseminated infection. Treat aggressively with oral Aciclovir. Low threshold for admission.", "red_flag_negative": "", "output_phrase": "Immunocompromised: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Herpes Simplex Virus (HSV-1) — cold sores", "Herpes Zoster (Shingles) — dermatomal, unilateral, pain precedes rash", "Impetigo — honey-coloured crusts", "Aphthous Ulcer — inside mouth, not vermillion border", "Angular Cheilitis — corners of mouth", "Erythema Multiforme — target lesions, may be HSV-triggered"],
                "questions": [
                    {"id": "cs_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["HSV-1 Cold Sore — typical", "First episode — treat", "Recurrent — suppressive therapy consideration", "?Complicated — ophthalmology/referral", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Prodrome (best treatment window): Topical Aciclovir 5% cream 5x/day for 5 days. Oral Aciclovir 400mg TDS for 5 days if severe or frequent. If >6 episodes/year: Suppressive therapy — Aciclovir 400mg BD for 6-12 months. Avoid triggers: Lip balm with SPF 30+, stress management. Avoid kissing/sharing utensils while active. If immunocompromised or extensive: Oral Aciclovir 400mg 5x/day for 5-10 days. Safety-net: Return if eye pain/redness, lesions spreading despite treatment, not healed in 10 days, or signs of secondary bacterial infection.",
                "questions": [
                    {"id": "cs_treatment", "type": "single_select", "label": "Treatment", "required": True, "options": ["Topical Aciclovir cream", "Oral Aciclovir", "Suppressive therapy (prophylaxis)", "Reassurance — self-limiting, no treatment", "Refer ophthalmology / urgent"], "output_phrase": "Treatment: {value}"},
                    {"id": "cs_prophylaxis", "type": "toggle", "label": "Suppressive Therapy Started? (Aciclovir 400mg BD)", "required": False, "output_phrase": "Suppressive: {value}"},
                    {"id": "cs_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if eye symptoms / spreading / not healed)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "cs_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., No routine follow-up. Return if frequent recurrences for suppressive therapy.", "output_phrase": "Follow-up: {value}"}
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
    seed_cold_sores()