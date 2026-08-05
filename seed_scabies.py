from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_scabies():
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
        "title": "Scabies",
        "description": "Assessment and management of scabies infestation. Covers classic symptoms, examination findings, treatment with permethrin/malathion, and household management.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "sc_itch", "type": "single_select", "label": "Itch Pattern", "required": True, "options": ["Generalised — worse at night (classic)", "Localised only", "Worse during day", "No itch"], "output_phrase": "Itch: {value}"},
                    {"id": "sc_contacts", "type": "toggle", "label": "Household Contacts / Partner Also Itching?", "required": True, "output_phrase": "Contacts itching: {value}"},
                    {"id": "sc_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 3 weeks", "output_phrase": "Duration: {value}"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "sc_sites", "type": "multi_select", "label": "Affected Sites", "required": True, "options": ["Finger webs / sides of fingers", "Wrist flexures", "Axillae", "Buttocks / groin", "Genitalia (males)", "Nipples (females)", "Palms/soles (children)", "Head/neck (infants)"], "output_phrase": "Sites: {value}"},
                    {"id": "sc_burrows", "type": "toggle", "label": "Burrows Visible? (fine wavy grey/white lines — pathognomonic)", "required": True, "output_phrase": "Burrows: {value}"},
                    {"id": "sc_secondary", "type": "toggle", "label": "Secondary Infection? (excoriations, impetiginisation, crusted areas)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Crusted/hyperkeratotic = ?Norwegian/crusted scabies (immunocompromised/elderly). Highly contagious. Needs dermatology referral + aggressive treatment.", "red_flag_negative": "", "output_phrase": "Secondary infection: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Scabies — classic, household contacts affected", "Crusted (Norwegian) Scabies — immunocompromised/elderly", "Eczema / Atopic Dermatitis", "Urticaria", "Insect Bites", "Prurigo Nodularis"],
                "questions": [
                    {"id": "sc_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Classic Scabies", "?Crusted Scabies — dermatology referral", "?Scabies — treat empirically", "Other dermatosis"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "First-line: Permethrin 5% cream (Lyclear) applied to WHOLE BODY (neck to toes, including soles, under nails). Leave on 8-12 hours then wash off. Repeat after 7 days. Alternative: Malathion 0.5% liquid (Derbac-M) — same application. ALL household contacts + close physical contacts must treat simultaneously — even if asymptomatic. Wash bedding, towels, clothes at 60°C on day of treatment. Items that can't be washed: seal in plastic bag for 72 hours. Itch may persist 2-4 weeks after successful treatment — not treatment failure. Antihistamine (Chlorphenamine) and crotamiton cream for post-scabetic itch. Safety-net: Return if new burrows after 2 weeks, persistent itch >4 weeks, or signs of secondary infection.",
                "questions": [
                    {"id": "sc_treatment", "type": "single_select", "label": "Treatment Prescribed", "required": True, "options": ["Permethrin 5% cream (2 applications, 7 days apart)", "Malathion 0.5% liquid (2 applications)", "Permethrin + antihistamine for itch", "Oral Ivermectin (crusted/derm referral)", "Refer dermatology (crusted/complicated)"], "output_phrase": "Treatment: {value}"},
                    {"id": "sc_contacts_treated", "type": "toggle", "label": "All Household/Close Contacts Advised to Treat Simultaneously?", "required": True, "output_phrase": "Contacts treated: {value}"},
                    {"id": "sc_hygiene", "type": "toggle", "label": "Bedding/Clothing Wash at 60°C Advised?", "required": True, "output_phrase": "Hygiene advice: {value}"},
                    {"id": "sc_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 2 weeks if persistent symptoms. Itch may last 4 weeks post-treatment.", "output_phrase": "Follow-up: {value}"}
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
    seed_scabies()