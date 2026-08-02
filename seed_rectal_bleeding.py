from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_rectal_bleeding():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Rectal Bleeding - ?Haemorrhoids",
        "description": "Focused assessment for rectal bleeding covering haemorrhoidal vs colorectal cancer differentiation, blood characteristics, and NICE NG12 2WW referral criteria.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Bleeding History",
                "section_type": "history",
                "questions": [
                    {"id": "rb_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Bright red blood on toilet paper for 4 episodes"},
                    {"id": "rb_episodes", "type": "number", "label": "Number of Episodes", "required": True, "placeholder": "e.g., 4"},
                    {"id": "rb_description", "type": "multi_select", "label": "Bleeding Description", "required": True, "options": ["Bright red blood dripping from back passage", "Turns toilet bowl pink", "Blood on tissue paper only"]},
                    {"id": "rb_blood_stool_relationship", "type": "single_select", "label": "Blood-Stool Relationship", "required": True, "options": ["Blood coats the stool - not mixed in (anal/rectal source)", "Blood mixed with stool - RED FLAG (?colonic/malignancy)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Blood mixed INTO stool = ?colorectal cancer, IBD. Urgent colonoscopy.", "red_flag_negative": ""},
                    {"id": "rb_colour", "type": "single_select", "label": "Blood Colour", "required": True, "options": ["Bright red (anal/rectal)", "Dark red / maroon (colonic)", "Melaena (black tarry - upper GI) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Melaena = upper GI bleed. Urgent A&E. Dark red = ?colonic source.", "red_flag_negative": ""},
                    {"id": "rb_volume", "type": "single_select", "label": "Volume of Bleeding", "required": True, "options": ["Small amount (drips / tissue paper) - haemorrhoids", "Approximately a cupful - consider diverticulosis"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Large volume PR bleed = ?diverticulosis, angiodysplasia. Urgent gastroenterology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms & Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "rb_anal_symptoms", "type": "multi_select", "label": "Associated Anal Symptoms", "required": True, "options": ["Mild anal itching", "Mild anal pain", "Sensation of a 'grape' near anal margin (prolapsing haemorrhoid)", "None"]},
                    {"id": "rb_inflammatory", "type": "multi_select", "label": "Inflammatory / Infective Screen", "required": True, "options": ["Fever", "Mucus", "Joint pain", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever + mucus + blood + joint pain = ?UC/infective colitis. Urgent gastroenterology.", "red_flag_negative": ""},
                    {"id": "rb_abdo_pain", "type": "toggle", "label": "Abdominal Pain?", "required": True},
                    {"id": "rb_bleeding_disorder", "type": "multi_select", "label": "Bleeding Disorder Screen", "required": True, "options": ["Gum bleeding", "Easy bruising", "Neither present"]},
                    {"id": "rb_bowel_habit", "type": "text", "label": "Bowel Habit", "required": True, "placeholder": "e.g., Bowel motion every 2 days"},
                    {"id": "rb_constipation", "type": "toggle", "label": "History of Constipation?", "required": True},
                    {"id": "rb_family", "type": "multi_select", "label": "Personal / Family History", "required": True, "options": ["Bowel cancer", "Bleeding disorder", "Neither"]},
                    {"id": "rb_meds", "type": "single_select", "label": "Medication History", "required": True, "options": ["Currently taking NSAIDs", "Not currently taking NSAIDs"]},
                    {"id": "rb_lifestyle", "type": "multi_select", "label": "Lifestyle", "required": False, "options": ["Alcohol", "Smoking", "Denies both"]}
                ]
            },
            {
                "title": "Colorectal Cancer Red Flags (NICE NG12)",
                "section_type": "history",
                "questions": [
                    {"id": "rb_2ww_criteria", "type": "multi_select", "label": "2WW Referral Criteria", "required": True, "options": ["Weight loss", "Change in bowel habit", "Persistent vomiting", "Age ≥40 years with PR bleeding", "None present, and under 40 years of age"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Age ≥40 + PR bleeding + change in bowel habit/weight loss = URGENT 2WW colorectal. Do NOT assume haemorrhoids.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "rb_general", "type": "single_select", "label": "General Examination", "required": True, "options": ["No anaemia, no jaundice, no lymphadenopathy", "Anaemia present - RED FLAG", "Jaundice present", "Lymphadenopathy present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Anaemia + PR bleeding = ?colorectal cancer. Urgent 2WW.", "red_flag_negative": ""},
                    {"id": "rb_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, non-tender, no organomegaly, BS present", "Abnormal finding"]},
                    {"id": "rb_pr", "type": "single_select", "label": "PR Examination", "required": True, "options": ["External haemorrhoid - no rectal wall irregularities", "Rectal wall irregularity / mass palpated - RED FLAG", "PR not performed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Rectal mass = colorectal cancer until proven otherwise. Urgent 2WW.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Haemorrhoids (bright red, coats stool, itching, grape sensation)",
                    "Anal Fissure (sharp pain on defaecation + blood on paper)",
                    "Diverticulosis (large volume, painless, older)",
                    "Inflammatory Bowel Disease (mucus, fever, joint pain, blood mixed)",
                    "Colorectal Cancer (weight loss, change in bowel habit, age ≥40, mass)",
                    "Upper GI Bleed (melaena, haematemesis)",
                    "Angiodysplasia (intermittent, elderly)"
                ],
                "questions": [
                    {"id": "rb_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Haemorrhoids", "Anal fissure suspected", "Diverticulosis suspected", "IBD suspected", "Colorectal malignancy - RED FLAGS PRESENT", "Upper GI bleed suspected"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: bleeding becomes heavy (cupful), melaena develops, abdominal pain worsens, or red flags develop (weight loss, change in bowel habit). Age ≥40 with PR bleeding + change in bowel habit/weight loss = URGENT 2WW colorectal. Do NOT assume haemorrhoids in patients with red flags. Blood mixed INTO stool = colonoscopy. Blood coating stool + anal symptoms = ?haemorrhoids (PR exam + proctoscopy). Check FBC (anaemia), bone/liver profile, ESR/CRP, coeliac screen, INR. Review in 4 weeks if conservative treatment. If not improving or red flags: refer colorectal for colonoscopy.",
                "questions": [
                    {"id": "rb_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "Bone/Liver profile", "ESR / CRP", "Coeliac screen", "INR", "TFTs", "None"]},
                    {"id": "rb_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["None - GP managed, review in 4 weeks", "May need colonoscopy (pending clinical course)", "Urgent 2WW colorectal (red flags present)", "Urgent A&E (large volume bleed / melaena)"]},
                    {"id": "rb_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 4-week review, sooner if red flags, or urgent referral pathway"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_rectal_bleeding()