from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_varicose_veins():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Varicose Veins",
        "description": "Focused assessment for varicose veins covering chronic venous insufficiency complications, compression therapy (GMS Class 2), and vascular surgery referral with ABPI.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "vv_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Aching, heavy legs with visible veins, worse at end of day"},
                    {"id": "vv_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Aching", "Heaviness", "Pressure / throbbing", "Itching", "Restless legs"]},
                    {"id": "vv_aggravating", "type": "multi_select", "label": "Aggravating Factors", "required": True, "options": ["Prolonged standing", "Worse at end of day", "Heat / warm weather"]},
                    {"id": "vv_relieving", "type": "multi_select", "label": "Relieving Factors", "required": True, "options": ["Leg elevation", "Sitting", "Walking", "Compression stockings"]},
                    {"id": "vv_complications", "type": "multi_select", "label": "Chronic Venous Insufficiency / Complications", "required": True, "options": ["Leg swelling / oedema", "Itch", "Skin changes (discolouration)", "Venous eczema", "Ulceration", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Active ulceration / skin changes = refer vascular. Venous eczema = treat + compression.", "red_flag_negative": ""},
                    {"id": "vv_pregnancies", "type": "toggle", "label": "Previous Pregnancies? (Risk Factor)", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "vv_pelvic_mass", "type": "toggle", "label": "Pelvic / Abdominal Masses? (Secondary Venous Obstruction)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pelvic/abdominal mass = ?secondary cause of varicose veins (tumour compression). Urgent imaging.", "red_flag_negative": ""},
                    {"id": "vv_gaiter_eczema", "type": "toggle", "label": "Gaiter Area: Venous Eczema?", "required": True},
                    {"id": "vv_gaiter_ulcer", "type": "toggle", "label": "Gaiter Area: Ulceration?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Active ulceration = vascular referral + compression therapy + wound care.", "red_flag_negative": ""},
                    {"id": "vv_gaiter_oedema", "type": "toggle", "label": "Gaiter Area: Oedema?", "required": True},
                    {"id": "vv_haemosiderin", "type": "toggle", "label": "Haemosiderin Deposition? (Brown Discolouration)", "required": False},
                    {"id": "vv_lipodermatosclerosis", "type": "toggle", "label": "Lipodermatosclerosis? (Hardened, Fibrotic Skin)", "required": False},
                    {"id": "vv_lsv", "type": "single_select", "label": "Long Saphenous Vein", "required": False, "options": ["Normal", "Varicose / Dilated", "Not assessed"]},
                    {"id": "vv_ssv", "type": "single_select", "label": "Short Saphenous Vein (Popliteal to Lateral Malleolus)", "required": False, "options": ["Normal", "Varicose / Dilated", "Not assessed"]},
                    {"id": "vv_phlebitis", "type": "toggle", "label": "Phlebitis or Thrombosis Along Saphenous Veins?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Superficial thrombophlebitis = NSAIDs + compression. If extending near SFJ = urgent vascular (risk of DVT).", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Primary Varicose Veins (Valvular Incompetence - Most Common)",
                    "Secondary Varicose Veins (Pelvic Mass, Previous DVT)",
                    "Chronic Venous Insufficiency (Skin Changes, Ulceration)",
                    "Superficial Thrombophlebitis",
                    "Deep Vein Thrombosis (Unilateral Swelling, Pain, Redness)",
                    "Lymphoedema (Non-Pitting, Dorsal Foot Involvement)",
                    "Peripheral Arterial Disease (Claudication, Absent Pulses)"
                ],
                "questions": [
                    {"id": "vv_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Varicose Veins - Uncomplicated", "Varicose Veins with Chronic Venous Insufficiency", "Varicose Veins with Venous Eczema", "Varicose Veins with Ulceration - Urgent Referral", "Superficial Thrombophlebitis", "Suspected Secondary Cause - Investigate"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: skin breaks down/ulceration develops, sudden increase in swelling/pain (DVT), or signs of infection (cellulitis). Lifestyle: exercise as tolerated, avoid prolonged uninterrupted standing, elevate legs when resting. Emulsifying ointment BD for venous eczema. Compression: support stockings applied before getting out of bed. Class 2 (CCL2) Mediven compression stockings if significant oedema present - available on GMS. Refer vascular surgery: ABPI (ankle-brachial pressure index) required prior to/as part of assessment. Do NOT use compression if ABPI <0.8 (arterial disease).",
                "questions": [
                    {"id": "vv_emulsifying", "type": "toggle", "label": "Emulsifying Ointment BD Advised? (Venous Eczema)", "required": False},
                    {"id": "vv_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Exercise as Tolerated", "Avoid Prolonged Standing", "Elevate Legs When Resting"]},
                    {"id": "vv_compression", "type": "single_select", "label": "Compression Therapy", "required": False, "options": ["Support Stockings (Apply Before Getting Out of Bed)", "Class 2 CCL2 Mediven Stockings (Significant Oedema - GMS Available)", "Not indicated / Contraindicated (ABPI <0.8)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT compress if ABPI <0.8 (arterial disease). Check pulses before prescribing.", "red_flag_negative": ""},
                    {"id": "vv_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Conservative)", "Vascular Surgery (Symptomatic / Complications - ABPI Required)", "Urgent Vascular (Ulceration / Phlebitis Near SFJ)"]},
                    {"id": "vv_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await vascular OPD, review if skin changes, or routine follow-up"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_varicose_veins()