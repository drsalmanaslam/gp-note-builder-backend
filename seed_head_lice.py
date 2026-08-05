from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_head_lice():
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
        "title": "Head Lice (Pediculosis Capitis)",
        "description": "Assessment and management of head lice infestation. Covers detection, wet combing vs chemical treatments, resistance considerations, and school/daycare advice.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "hl_age", "type": "number", "label": "Age (most common 4-11 years)", "required": True, "placeholder": "e.g., 7", "output_phrase": "Age: {value}"},
                    {"id": "hl_itch", "type": "toggle", "label": "Scalp Itching? (may take 4-6 weeks to develop after first infestation)", "required": True, "output_phrase": "Itch: {value}"},
                    {"id": "hl_contacts", "type": "toggle", "label": "Known Contacts Affected? (school, family, sleepover)", "required": True, "output_phrase": "Contacts: {value}"},
                    {"id": "hl_previous", "type": "single_select", "label": "Previous Treatments?", "required": True, "options": ["None — first episode", "Wet combing — worked", "Chemical treatment — worked", "Chemical treatment — failed (?resistance)", "Multiple failed treatments"], "output_phrase": "Previous: {value}"}
                ]
            },
            {
                "title": "Detection & Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hl_detection", "type": "single_select", "label": "Detection Method", "required": True, "options": ["Live lice seen", "Nits (egg cases) only — ?old infestation", "Both live lice + nits", "No evidence found — reassure", "Not examined"], "output_phrase": "Detection: {value}"},
                    {"id": "hl_secondary", "type": "toggle", "label": "Secondary Infection? (impetigo from scratching)", "required": False, "output_phrase": "Infection: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Head Lice — live lice or viable nits within 1cm of scalp", "Dandruff / Seborrhoeic Dermatitis — diffuse scaling, not attached to hair shaft", "Hair casts — slide easily along hair shaft", "Old/empty nit cases — >1cm from scalp", "Tinea Capitis — scaly patches, hair loss"],
                "questions": [
                    {"id": "hl_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Active Head Lice Infestation", "Old infestation — nits only >1cm from scalp", "No infestation — reassure", "Secondary impetigo — treat"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "WET COMBING (Bug Busting): First-line. Apply conditioner to wet hair, comb through with fine-toothed nit comb every 3-4 days for 2 weeks. Repeat until no live lice for 3 consecutive sessions. CHEMICAL: Dimeticone 4% lotion (Hedrin) — physical action, not insecticide (no resistance). Apply to dry hair, leave 8h/overnight, repeat after 7 days. Avoid traditional insecticides (malathion, permethrin) first-line due to resistance. Treat ALL affected household members simultaneously. No need to wash bedding at high temp — lice die within 24-48h off scalp. Children can attend school after first treatment — no exclusion needed. Notify school/nursery. Safety-net: Return if live lice persist after 2 weeks of treatment.",
                "questions": [
                    {"id": "hl_treatment", "type": "single_select", "label": "Treatment", "required": True, "options": ["Wet combing (Bug Busting) — first-line", "Dimeticone 4% lotion (Hedrin)", "Other chemical treatment", "Combination — wet combing + chemical", "Treat secondary infection + lice"], "output_phrase": "Treatment: {value}"},
                    {"id": "hl_contacts", "type": "toggle", "label": "All Household Members Advised to Check/Treat?", "required": True, "output_phrase": "Household advice: {value}"},
                    {"id": "hl_school", "type": "toggle", "label": "School/Nursery Notification Advised? (no exclusion needed)", "required": True, "output_phrase": "School advice: {value}"},
                    {"id": "hl_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Check after 2 weeks. If persistent, try alternative treatment.", "output_phrase": "Follow-up: {value}"}
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
    seed_head_lice()