from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_pressure_sores():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Geriatrics").first()
    if not category:
        category = Category(name="Geriatrics")
        db.add(category)
        db.commit()

    t = {
        "title": "Pressure Sores & Leg Ulcers",
        "description": "Assessment of pressure ulcers and leg ulcers. Covers grading, risk assessment, infection detection, wound care, dressings, and MDT referral pathways.",
        "category": "Geriatrics",
        "content": {"sections": [
            {
                "title": "History & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "pu_type", "type": "single_select", "label": "Type of Ulcer", "required": True, "options": ["Pressure ulcer — sacrum/heel/hip", "Venous leg ulcer — gaiter area, shallow, wet", "Arterial leg ulcer — toes/foot, punched-out, painful", "Diabetic foot ulcer — plantar, neuropathic", "Mixed aetiology"], "output_phrase": "Type: {value}"},
                    {"id": "pu_risk", "type": "multi_select", "label": "Risk Factors", "required": True, "options": ["Immobility / bedbound", "Incontinence", "Poor nutrition / weight loss", "Diabetes", "Peripheral vascular disease", "Venous insufficiency", "Smoking", "Advanced age"], "output_phrase": "Risk factors: {value}"},
                    {"id": "pu_duration", "type": "text", "label": "Duration of Ulcer", "required": True, "placeholder": "e.g., 3 weeks", "output_phrase": "Duration: {value}"}
                ]
            },
            {
                "title": "Assessment & Grading",
                "section_type": "examination",
                "questions": [
                    {"id": "pu_grade", "type": "single_select", "label": "Pressure Ulcer Grade (EPUAP)", "required": True, "options": ["I — Non-blanchable erythema, intact skin", "II — Partial thickness loss, blister/shallow ulcer", "III — Full thickness, subcutaneous fat visible", "IV — Full thickness, bone/tendon/muscle visible", "Unstageable — eschar/slough covering"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Grade III-IV = deep tissue damage. Urgent wound care referral. Risk of osteomyelitis.", "red_flag_negative": "", "output_phrase": "Grade: {value}"},
                    {"id": "pu_size", "type": "text", "label": "Size (length x width x depth in cm)", "required": True, "placeholder": "e.g., 3 x 2 x 0.5 cm", "output_phrase": "Size: {value}"},
                    {"id": "pu_infection", "type": "toggle", "label": "Signs of Infection? (erythema, warmth, purulent discharge, odour, fever)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Infected ulcer = wound swab + antibiotics. If systemic: admit for IV antibiotics. Risk of sepsis/osteomyelitis.", "red_flag_negative": "", "output_phrase": "Infection: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Pressure Ulcer", "Venous Leg Ulcer", "Arterial Ulcer", "Diabetic Neuropathic Ulcer", "Malignant Ulcer (Marjolin's — SCC in chronic wound)", "Pyoderma Gangrenosum", "Cellulitis"],
                "questions": [
                    {"id": "pu_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Pressure Ulcer — Grade I-II", "Pressure Ulcer — Grade III-IV (urgent)", "Venous Leg Ulcer", "Arterial Ulcer", "Diabetic Foot Ulcer", "Infected — needs antibiotics", "Mixed / Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "PRESSURE RELIEF: Regular repositioning (every 2h), pressure-relieving mattress/cushion, heel protectors. WOUND CARE: Clean with saline. Debridement if slough (district nurse/tissue viability). Dressings: Hydrocolloid (Grade I-II), Foam/Alginate (Grade II-III, exudating), Hydrogel (dry/necrotic), Antimicrobial (silver/iodine if infected). VENOUS ULCER: Compression bandaging (ABPI must be >0.8 first — do NOT compress if arterial). Elevation. ARTERIAL ULCER: Urgent vascular referral. Do NOT compress. MDT: District nurse, tissue viability nurse, podiatry (diabetic), dietitian (if MUST ≥2). Safety-net: Return if spreading infection, fever, worsening pain, or no improvement in 2 weeks.",
                "questions": [
                    {"id": "pu_treatment", "type": "single_select", "label": "Treatment Plan", "required": True, "options": ["Pressure relief + wound care + district nurse referral", "Compression bandaging (venous — after ABPI)", "Antibiotics + wound care (infected)", "Urgent vascular referral (arterial)", "Tissue viability / wound clinic referral"], "output_phrase": "Treatment: {value}"},
                    {"id": "pu_dn_referral", "type": "toggle", "label": "District Nurse / Tissue Viability Referral Made?", "required": True, "output_phrase": "DN referral: {value}"},
                    {"id": "pu_abpi", "type": "toggle", "label": "ABPI Checked Before Compression? (must be >0.8 for safe compression)", "required": False, "output_phrase": "ABPI checked: {value}"},
                    {"id": "pu_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if spreading infection / fever / worsening)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "pu_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., District nurse visiting 3x/week. GP review in 2 weeks. If not healing, tissue viability referral.", "output_phrase": "Follow-up: {value}"}
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
    seed_pressure_sores()