from app.database import SessionLocal
from app.models import User, Template, Category

def seed_dysphagia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Dysphagia",
        "description": "Focused assessment for dysphagia covering malignant vs benign causes, achalasia, globus pharyngis, bulbar palsy, and urgency of OGD referral.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Swallowing History",
                "section_type": "history",
                "questions": [
                    {"id": "dysph_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Difficulty swallowing solids for 3 weeks, now liquids also sticking"},
                    {"id": "dysph_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
                    {"id": "dysph_pattern", "type": "single_select", "label": "Pattern of Difficulty", "required": True, "options": ["Solids only", "Solids progressing to liquids - RED FLAG (?malignancy)", "Both solids and liquids from onset (?achalasia)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Solids progressing to liquids + weight loss = OESOPHAGEAL CANCER until proven otherwise. Urgent 2WW OGD.", "red_flag_negative": ""},
                    {"id": "dysph_course", "type": "single_select", "label": "Course", "required": True, "options": ["Intermittent", "Persistent / progressive - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Persistent progressive dysphagia = ?malignancy. Urgent 2WW OGD.", "red_flag_negative": ""},
                    {"id": "dysph_level", "type": "text", "label": "Level of Obstruction (C6-T11)", "required": False, "placeholder": "e.g., Retrosternal / mid-chest"},
                    {"id": "dysph_globus", "type": "toggle", "label": "Globus Sensation? (Lump in throat WITHOUT true dysphagia)", "required": False},
                    {"id": "dysph_timing", "type": "single_select", "label": "Timing of Difficulty", "required": True, "options": ["Harder at beginning of swallowing (?bulbar palsy)", "Not harder at beginning - food sticks after initiation (?oesophageal)"]}
                ]
            },
            {
                "title": "Associated Symptoms & Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "dysph_associated", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Odynophagia (pain on swallowing)", "Choking sensation", "Cough (aspiration)", "None"]},
                    {"id": "dysph_red_flags", "type": "multi_select", "label": "Alarm Features (2WW Referral)", "required": True, "options": ["Vomiting", "Weight loss", "Neck bulge / lymphadenopathy", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + dysphagia = URGENT 2WW OGD. Do not delay.", "red_flag_negative": ""},
                    {"id": "dysph_scleroderma", "type": "multi_select", "label": "Scleroderma / CREST Screen", "required": False, "options": ["Skin thickening/tightening of hands", "Raynaud's phenomenon (white→blue→red)", "Neither present"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "dysph_hands", "type": "single_select", "label": "Hands", "required": False, "options": ["No calcinosis, no sclerodactyly", "Calcinosis present", "Sclerodactyly present"]},
                    {"id": "dysph_conjunctiva", "type": "single_select", "label": "Conjunctiva", "required": False, "options": ["Normal", "Pale (anaemia - ?malignancy)"]},
                    {"id": "dysph_abdo", "type": "single_select", "label": "Abdominal Examination", "required": False, "options": ["Soft, non-tender, no organomegaly", "Abnormal finding"]},
                    {"id": "dysph_cn", "type": "single_select", "label": "Cerebellar / Cranial Nerve Exam", "required": False, "options": ["Normal", "Abnormal (?bulbar/pseudobulbar palsy)"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Oesophageal Cancer (RED FLAG - progressive, weight loss)",
                    "Achalasia (both solids + liquids from onset, heartburn)",
                    "Benign Oesophageal Stricture (GORD-related)",
                    "Oesophageal Web / Ring (Schatzki ring)",
                    "Globus Pharyngis (lump sensation, no true dysphagia)",
                    "Bulbar / Pseudobulbar Palsy (difficulty initiating swallow, neurological signs)",
                    "Scleroderma-Related Oesophageal Dysmotility",
                    "Eosinophilic Oesophagitis",
                    "Extrinsic Compression (mediastinal mass, goitre)"
                ],
                "questions": [
                    {"id": "dysph_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Dysphagia - cause to be determined on OGD", "Suspected malignancy - URGENT 2WW OGD", "Suspected achalasia", "Suspected globus pharyngis", "Suspected bulbar palsy", "Suspected scleroderma-related dysmotility"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: complete obstruction (cannot swallow saliva), vomiting, weight loss, or neck bulge develops. Solids progressing to liquids + weight loss = oesophageal cancer until proven otherwise - URGENT 2WW OGD. Both solids and liquids from onset with heartburn = ?achalasia - routine OGD. Globus sensation without true dysphagia = likely globus pharyngis (reassure, treat GORD if present). Difficulty at beginning of swallow = ?bulbar palsy - neurological examination + referral. Bloods: FBC (anaemia), ferritin, bone/liver profile. All patients with true dysphagia require OGD for diagnosis.",
                "questions": [
                    {"id": "dysph_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "Ferritin", "Bone/Liver profile", "None"]},
                    {"id": "dysph_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["Urgent 2WW OGD (red flags present)", "Routine OGD (no red flags)", "Neurology (?bulbar palsy)", "None - globus pharyngis"]},
                    {"id": "dysph_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await OGD result, urgent referral if red flags, or routine follow-up"}
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
    seed_dysphagia()