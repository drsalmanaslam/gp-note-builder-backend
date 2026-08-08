from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_insect_bites():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "OOH").first()
    if not category:
        category = Category(name="OOH"); db.add(category); db.commit()

    t = {
        "title": "OOH - Insect Bites & Stings",
        "description": "Rapid out-of-hours assessment of insect bites and bee/wasp stings. Rule out anaphylaxis, assess for secondary infection, and guide management.",
        "category": "OOH",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_ib_agent", "type": "single_select", "label": "Agent", "required": True, "options": ["Bee sting", "Wasp sting", "Mosquito bite", "Tick bite", "Spider bite", "Horsefly", "Unknown"], "output_phrase": "Agent: {value}"},
                    {"id": "ooh_ib_time", "type": "text", "label": "Time Since Bite/Sting", "required": True, "placeholder": "e.g., 30 minutes", "output_phrase": "Time: {value}"},
                    {"id": "ooh_ib_location", "type": "single_select", "label": "Location", "required": True, "options": ["Face / lip / tongue — risk of airway oedema", "Neck", "Limb", "Trunk", "Multiple sites"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Face/lip/tongue = risk of airway compromise. Urgent assessment.", "red_flag_negative": "", "output_phrase": "Location: {value}"}
                ]
            },
            {
                "title": "Red Flags — Anaphylaxis",
                "section_type": "history",
                "questions": [
                    {"id": "ooh_ib_anaphylaxis", "type": "multi_select", "label": "Anaphylaxis Features", "required": True, "options": ["Urticaria / widespread rash", "Angioedema — lip/tongue/eyelid swelling", "Stridor / difficulty breathing", "Wheeze", "Dizziness / hypotension / collapse", "Nausea / vomiting", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any airway/breathing/circulatory symptoms = ANAPHYLAXIS. IM Adrenaline 0.5mg STAT. Call 999.", "red_flag_negative": "", "output_phrase": "Anaphylaxis: {value}"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ooh_ib_reaction", "type": "single_select", "label": "Local Reaction", "required": True, "options": ["Mild — localised swelling <5cm", "Moderate — swelling 5-10cm", "Large local reaction — >10cm", "Spreading cellulitis — hot, tender, expanding"], "output_phrase": "Reaction: {value}"},
                    {"id": "ooh_ib_stinger", "type": "toggle", "label": "Stinger Retained? (bee — scrape out, don't squeeze)", "required": False, "output_phrase": "Stinger: {value}"},
                    {"id": "ooh_ib_tick", "type": "toggle", "label": "If Tick — Fully Removed? (save for identification, watch for Lyme)", "required": False, "output_phrase": "Tick: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Anaphylaxis", "Large Local Reaction", "Secondary Cellulitis", "Lyme Disease (tick, erythema migrans)", "Imported Infection (malaria, dengue if travel)"],
                "questions": [
                    {"id": "ooh_ib_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Anaphylaxis — emergency 999", "Large local reaction — antihistamines + steroids", "?Cellulitis — antibiotics", "?Lyme — doxycycline prophylaxis", "Mild reaction — symptomatic treatment"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Anaphylaxis: IM Adrenaline 0.5mg. Call 999. Large local reaction: Chlorphenamine 4mg PO + Prednisolone 40mg OD 3-5 days. Remove stinger (scrape sideways, don't squeeze). Tick: Remove with fine tweezers. If endemic area + engorged tick >24h: Doxycycline 200mg stat (prophylaxis). Cellulitis: Flucloxacillin 500mg QDS. Safety-net: Return immediately if SOB, stridor, facial swelling, collapse, or spreading infection.",
                "questions": [
                    {"id": "ooh_ib_action", "type": "single_select", "label": "Disposition", "required": True, "options": ["999 — anaphylaxis", "Home with antihistamines + steroids", "Home with antibiotics", "Tick prophylaxis", "Observe + discharge"], "output_phrase": "Disposition: {value}"},
                    {"id": "ooh_ib_antihistamine", "type": "toggle", "label": "Antihistamine Given?", "required": False, "output_phrase": "Antihistamine: {value}"},
                    {"id": "ooh_ib_steroids", "type": "toggle", "label": "Oral Steroids Given? (large local reaction)", "required": False, "output_phrase": "Steroids: {value}"},
                    {"id": "ooh_ib_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if SOB/angioedema/spreading)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "ooh_ib_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., No follow-up needed. Return if concerns.", "output_phrase": "Follow-up: {value}"}
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
    seed_insect_bites()