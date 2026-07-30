from app.database import SessionLocal
from app.models import User, Template, Category

def seed_chondrodermatitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Chondrodermatitis Nodularis Helicis",
        "description": "Focused assessment for chondrodermatitis nodularis helicis covering conservative pressure-relief management and referral criteria for wedge biopsy.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "cnh_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Painful tender nodule on ear for 2 months"},
                    {"id": "cnh_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 months"},
                    {"id": "cnh_sleep_side", "type": "single_select", "label": "Which Side Does Patient Habitually Sleep On? (Pressure = Causative Factor)", "required": True, "options": ["Same side as affected ear", "Opposite side to affected ear", "Both sides / varies"]},
                    {"id": "cnh_side_affected", "type": "single_select", "label": "Affected Ear", "required": True, "options": ["Right", "Left", "Both"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "cnh_findings", "type": "single_select", "label": "Examination Findings", "required": True, "options": ["Tender nodule on helix (consistent with CNH)", "Tender nodule on antihelix (consistent with CNH)", "Other finding - reconsider diagnosis"]},
                    {"id": "cnh_ulceration", "type": "toggle", "label": "Ulceration / Crusting Present?", "required": False},
                    {"id": "cnh_size", "type": "text", "label": "Nodule Size (mm)", "required": False, "placeholder": "e.g., 4mm"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Chondrodermatitis Nodularis Helicis (CNH) - Pressure-Induced",
                    "Actinic Keratosis",
                    "Squamous Cell Carcinoma (SCC) - Biopsy if Uncertain",
                    "Basal Cell Carcinoma (BCC)",
                    "Gouty Tophus",
                    "Relapsing Polychondritis"
                ],
                "questions": [
                    {"id": "cnh_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Chondrodermatitis Nodularis Helicis - Typical", "Suspicious Lesion - Refer for Biopsy", "Uncertain - Needs Dermatology/ENT Review"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if no improvement within 6 weeks of conservative measures, or if nodule grows/changes/ulcerates. CNH is caused by pressure on the ear cartilage, typically from sleeping on that side. First-line: sleep on opposite side + use pressure-relieving pillow (foam pillow with centre cut out / doughnut pillow / purpose-made CNH pillow). If no improvement at 6 weeks: refer ENT/dermatology for wedge biopsy (note: cartilage removal is required as part of this procedure). Do NOT attempt excision in primary care.",
                "questions": [
                    {"id": "cnh_sleep_advice", "type": "toggle", "label": "Advise Sleeping on Opposite Side to Affected Ear?", "required": True},
                    {"id": "cnh_pillow", "type": "toggle", "label": "Pressure-Relieving Pillow Advised? (Foam with Centre Cut Out / Doughnut Pillow)", "required": True},
                    {"id": "cnh_referral", "type": "single_select", "label": "Referral (If No Improvement at 6 Weeks)", "required": False, "options": ["Refer ENT / Dermatology for Wedge Biopsy (Cartilage Removal Required)", "Not indicated - conservative trial ongoing"]},
                    {"id": "cnh_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 6 weeks if no improvement"}
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
    seed_chondrodermatitis()