from app.database import SessionLocal
from app.models import User, Template, Category

def seed_subconjunctival_haemorrhage():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Ophthalmology").first()
    if not category: category = Category(name="Ophthalmology"); db.add(category); db.commit()

    t = {
        "title": "Subconjunctival Haemorrhage",
        "description": "Focused assessment for subconjunctival haemorrhage covering red flags for trauma/bleeding disorders, BP check, and reassurance.",
        "category": "Ophthalmology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "sch_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Sudden bright red patch in right eye after coughing"},
                    {"id": "sch_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 48"},
                    {"id": "sch_side", "type": "single_select", "label": "Affected Eye", "required": True, "options": ["Right", "Left", "Both"]},
                    {"id": "sch_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (seconds)", "Noticed on waking", "Incidental finding"]},
                    {"id": "sch_trigger", "type": "single_select", "label": "Trigger / Valsalva", "required": True, "options": ["Coughing", "Sneezing", "Straining/lifting", "Vomiting", "Rubbing eye", "No trigger identified"]},
                    {"id": "sch_pain", "type": "toggle", "label": "Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pain = NOT simple subconjunctival haemorrhage. ?Trauma, keratitis, foreign body. Examine + fluorescein.", "red_flag_negative": ""},
                    {"id": "sch_previous", "type": "toggle", "label": "Previous Episodes?", "required": False}
                ]
            },
            {
                "title": "RED FLAGS & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "sch_trauma", "type": "toggle", "label": "Recent Ocular / Head Trauma?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Trauma + subconjunctival haemorrhage = ?penetrating injury, orbital fracture, intracranial bleed. If posterior border not visible = intracranial haemorrhage tracking into orbit. Urgent CT/ophthalmology.", "red_flag_negative": ""},
                    {"id": "sch_photophobia", "type": "toggle", "label": "Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Photophobia = ?uveitis/keratitis. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "sch_discharge", "type": "toggle", "label": "Discharge?", "required": True},
                    {"id": "sch_visual_loss", "type": "toggle", "label": "Visual Loss / Blurring?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual loss = ?intraocular involvement. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "sch_anticoagulants", "type": "toggle", "label": "On Anticoagulants? (Warfarin, DOAC)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Anticoagulants + SCH = check INR (if warfarin) or coag screen. May indicate over-anticoagulation.", "red_flag_negative": ""},
                    {"id": "sch_antiplatelets", "type": "toggle", "label": "On Antiplatelets? (Aspirin, Clopidogrel)", "required": True},
                    {"id": "sch_bleeding_disorder", "type": "toggle", "label": "Bleeding Disorder / Easy Bruising?", "required": False},
                    {"id": "sch_hypertension", "type": "toggle", "label": "Known Hypertension?", "required": False},
                    {"id": "sch_recurrent_unprovoked", "type": "toggle", "label": "Recurrent / Unprovoked Episodes?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent unprovoked = screen for HTN, bleeding disorder, check FBC + coag.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "sch_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 110/80", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP >180/120 = acute hypertensive crisis. Urgent management.", "red_flag_negative": ""},
                    {"id": "sch_appearance", "type": "single_select", "label": "Haemorrhage Appearance", "required": True, "options": ["Well-circumscribed, flat, deep red, clear posterior border", "Posterior border NOT visible - RED FLAG", "Raised/irregular - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Posterior border NOT visible = ?intracranial haemorrhage tracking into orbit. Urgent CT. Raised = ?penetrating injury.", "red_flag_negative": ""},
                    {"id": "sch_sclera", "type": "toggle", "label": "Scleral Laceration?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Scleral laceration = penetrating injury. Emergency ophthalmology.", "red_flag_negative": ""},
                    {"id": "sch_cornea", "type": "toggle", "label": "Corneal Abrasion / Limbal Flush?", "required": False},
                    {"id": "sch_va_right", "type": "text", "label": "Visual Acuity - Right", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "sch_va_left", "type": "text", "label": "Visual Acuity - Left", "required": True, "placeholder": "e.g., 6/6"},
                    {"id": "sch_eomi", "type": "toggle", "label": "Eye Movements Normal? (CN III, IV, VI)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Subconjunctival Haemorrhage - Benign (Valsalva/cough/sneeze)",
                    "Subconjunctival Haemorrhage - Traumatic",
                    "Subconjunctival Haemorrhage - Anticoagulant-Related",
                    "Subconjunctival Haemorrhage - Hypertensive",
                    "Subconjunctival Haemorrhage - Bleeding Disorder",
                    "Penetrating Ocular Injury (RED FLAG)",
                    "Intracranial Haemorrhage Tracking into Orbit (RED FLAG - no posterior border visible)",
                    "Conjunctivitis (if associated discharge/injection)"
                ],
                "questions": [
                    {"id": "sch_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Benign subconjunctival haemorrhage", "Subconjunctival haemorrhage - on anticoagulants", "Subconjunctival haemorrhage - recurrent", "Traumatic - needs assessment", "Suspected penetrating injury - REFER EMERGENCY"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: eye pain develops, vision changes/decreases, discharge or photophobia occurs, or another bleed occurs. Benign subconjunctival haemorrhage resolves spontaneously over 1-2 weeks, changing colour like a skin bruise (red → yellow → clear). No treatment required. Artificial tears if mild irritation. If on warfarin: check INR. If recurrent/unprovoked: screen for hypertension, check FBC + coagulation screen, review antiplatelet/anticoagulant compliance. If traumatic with inability to see posterior border: urgent CT to exclude intracranial haemorrhage.",
                "questions": [
                    {"id": "sch_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassurance + observation", "Check INR (on warfarin)", "Check FBC + coag (recurrent)", "Artificial tears for comfort", "Refer ophthalmology", "Urgent CT (trauma + no posterior border)"]},
                    {"id": "sch_reassurance", "type": "toggle", "label": "Benign Self-Limiting Nature Explained? (Resolves 1-2 weeks like bruise)", "required": True},
                    {"id": "sch_inr", "type": "toggle", "label": "INR / Coagulation Check Ordered?", "required": False},
                    {"id": "sch_tears", "type": "toggle", "label": "Lubricating Artificial Tears?", "required": False},
                    {"id": "sch_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if resolves, 1-2 weeks if not clearing"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_subconjunctival_haemorrhage()