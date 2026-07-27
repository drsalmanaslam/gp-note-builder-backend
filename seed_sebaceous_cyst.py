from app.database import SessionLocal
from app.models import User, Template, Category

def seed_sebaceous_cyst():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Sebaceous Cyst (Epidermoid Cyst) Assessment",
        "description": "Focused assessment for sebaceous/epidermoid cysts covering diagnostic features (punctum, mobility), infection red flags, and excision referral.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "sc_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Lump on back for 6 months"},
                    {"id": "sc_location", "type": "text", "label": "Location of Lump (NOT Palms/Soles - No Sebaceous Glands)", "required": True, "placeholder": "e.g., Upper back"},
                    {"id": "sc_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 6 months"},
                    {"id": "sc_pain", "type": "toggle", "label": "Pain / Tenderness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Painful/tender = ?infected cyst. May need antibiotics before excision.", "red_flag_negative": ""},
                    {"id": "sc_size_change", "type": "single_select", "label": "Change in Size", "required": True, "options": ["Increasing", "Stable", "Decreasing"]},
                    {"id": "sc_infection_history", "type": "toggle", "label": "Previous Episodes of Inflammation / Infection?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "sc_circumscribed", "type": "toggle", "label": "Well Circumscribed?", "required": True},
                    {"id": "sc_mobility", "type": "single_select", "label": "Mobility", "required": True, "options": ["Freely Mobile, Fixed to Overlying Skin (NOT Deep Tissue) - Typical", "Fixed to Deep Tissue - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Fixed to deep tissue = ?malignancy. Urgent referral for biopsy.", "red_flag_negative": ""},
                    {"id": "sc_punctum", "type": "toggle", "label": "Central Punctum Present? (Diagnostic of Epidermoid Cyst)", "required": True},
                    {"id": "sc_size", "type": "number", "label": "Size (cm)", "required": False, "placeholder": "e.g., 2"},
                    {"id": "sc_erythema", "type": "toggle", "label": "Erythema / Inflammatory Changes? (?Infected)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Infected cyst = treat with antibiotics first. Do NOT excise while infected.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Epidermoid Cyst / Sebaceous Cyst (Central Punctum, Mobile, Fixed to Skin)",
                    "Pilar Cyst / Trichilemmal Cyst (Scalp, No Punctum)",
                    "Lipoma (Soft, Mobile, No Punctum, Not Fixed to Skin)",
                    "Dermoid Cyst (Congenital, Present Since Birth)",
                    "Abscess / Infected Cyst (Painful, Erythematous, Tender)",
                    "Ganglion (Wrist/Hand, Transilluminates)"
                ],
                "questions": [
                    {"id": "sc_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Sebaceous Cyst - Non-Infected", "Sebaceous Cyst - Infected (Treat Infection First)", "Pilar Cyst", "Diagnostic Uncertainty - Refer"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: cyst becomes painful, red, hot, or inflamed (infection). Sebaceous cysts do NOT occur on palms of hands or soles of feet (no sebaceous glands). If infected: treat with antibiotics first (Flucloxacillin). Do NOT excise while actively infected - higher recurrence and poor wound healing. Excision is cosmetic/patient choice - not medically necessary unless symptomatic. Refer for excision under local anaesthetic per patient request. Warn patient: excision includes removal of the sac to prevent recurrence. If diagnostic uncertainty or fixed to deep tissue: refer for biopsy to exclude malignancy.",
                "questions": [
                    {"id": "sc_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["Routine Surgical Referral - Excision Under LA (Patient Request)", "Treat Infection First - Reassess After (Antibiotics ± I&D)", "Refer Dermatology - Diagnostic Uncertainty", "Reassure - No Intervention Required"]},
                    {"id": "sc_antibiotics", "type": "toggle", "label": "Antibiotics Prescribed? (If Infected - Flucloxacillin)", "required": False},
                    {"id": "sc_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await surgical OPD, return if infected, or PRN"}
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
    seed_sebaceous_cyst()