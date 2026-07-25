from app.database import SessionLocal
from app.models import User, Template, Category

def seed_haemorrhoids():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Haemorrhoids Assessment",
        "description": "Focused assessment for haemorrhoids covering grading, differentiation from anal fissure, conservative management, and escalation to surgical options.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hae_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Bright red blood on toilet paper and dragging sensation"},
                    {"id": "hae_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Sensation of a haemorrhoid / lump", "Dragging sensation throughout the day (HAEMORRHOIDS)", "Bright red blood on toilet paper / dripping into bowl", "Itch", "Discomfort", "Pain (sharp on defaecation = ?FISSURE)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Sharp pain confined to defaecation = ?anal fissure, not haemorrhoids. Painless bleeding + dragging = haemorrhoids.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hae_location", "type": "text", "label": "Haemorrhoid Location (Clock Position)", "required": False, "placeholder": "e.g., 5 o'clock"},
                    {"id": "hae_dre", "type": "single_select", "label": "DRE Findings", "required": False, "options": ["No internal rectal wall irregularities", "Irregularity / mass palpated - RED FLAG", "DRE not performed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Rectal mass = ?colorectal cancer. Urgent 2WW referral.", "red_flag_negative": ""},
                    {"id": "hae_grade", "type": "single_select", "label": "Grade of Haemorrhoid", "required": True, "options": ["Grade 1 - No prolapse", "Grade 2 - Prolapses with bowel motion, self-reduces", "Grade 3 - Prolapses, requires manual reduction", "Grade 4 - Permanently prolapsed, irreducible"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Internal Haemorrhoids (painless bleeding, dragging)",
                    "External Haemorrhoids / Perianal Haematoma (painful lump)",
                    "Anal Fissure (sharp pain on defaecation, sentinel tag)",
                    "Perianal Abscess",
                    "Fistula-in-Ano",
                    "Rectal Prolapse",
                    "Colorectal Cancer (RED FLAG - weight loss, change in bowel habit, mass)",
                    "Pruritus Ani"
                ],
                "questions": [
                    {"id": "hae_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Haemorrhoids - Grade 1", "Haemorrhoids - Grade 2", "Haemorrhoids - Grade 3", "Haemorrhoids - Grade 4", "Suspected malignancy - URGENT 2WW"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if no improvement in 4-6 weeks of conservative treatment, or if red flags develop (weight loss, change in bowel habit, PR bleeding persists). Haemorrhoids are normal anatomical structures - three vascular cushions forming a seal at the top of the anal canal. Symptoms arise when venous plexus becomes engorged (obesity, constipation, pregnancy). First-line: Proctosedyl/Scheriproct suppository at night + ointment during day + Movicol for soft stool. Lifestyle: regular meals (emphasise breakfast), exercise, fibre, adequate fluids - effective in ~50%. If not improving: refer gastroenterology/colorectal for injection sclerotherapy, infrared coagulation, rubber band ligation, or open haemorrhoidectomy if recurrent.",
                "questions": [
                    {"id": "hae_mechanism_explained", "type": "toggle", "label": "Normal Anatomy + Venous Engorgement Mechanism Explained?", "required": True},
                    {"id": "hae_topical", "type": "multi_select", "label": "Topical Treatment", "required": False, "options": ["Proctosedyl / Scheriproct suppository at night", "Scheriproct ointment during the day", "Perianal spray (alternative)", "None"]},
                    {"id": "hae_stool_softener", "type": "single_select", "label": "Stool Softener", "required": False, "options": ["Movicol (Macrogol) once daily", "Lactulose", "None"]},
                    {"id": "hae_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Regular meals - emphasise breakfast", "Exercise", "Increase fibre intake", "Adequate fluid intake"]},
                    {"id": "hae_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP managed, first-line trial", "Referred to gastroenterology/colorectal surgery"]},
                    {"id": "hae_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return in 4-6 weeks if no improvement"}
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
    seed_haemorrhoids()