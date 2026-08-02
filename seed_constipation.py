from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_constipation():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Constipation",
        "description": "Focused assessment for constipation covering Bristol Stool Chart classification, medication review, red flags, laxative therapy, and faecal disimpaction protocol.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Bowel History",
                "section_type": "history",
                "questions": [
                    {"id": "con_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Not opening bowels regularly for 1 week"},
                    {"id": "con_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 1 week"},
                    {"id": "con_current_frequency", "type": "text", "label": "Current Bowel Frequency", "required": True, "placeholder": "e.g., 1 stool every 3 days"},
                    {"id": "con_baseline", "type": "text", "label": "Baseline (Normal) Bowel Habit", "required": True, "placeholder": "e.g., 1 stool daily"},
                    {"id": "con_fibre", "type": "text", "label": "Dietary Fibre Intake", "required": True, "placeholder": "e.g., 1-2 pieces fruit/veg per week"},
                    {"id": "con_bristol", "type": "single_select", "label": "Stool Consistency (Bristol Stool Chart)", "required": True, "options": ["Type 1 - Separate hard lumps (severe constipation)", "Type 2 - Sausage-shaped but lumpy", "Type 3 - Sausage-shaped with cracks (normal)", "Type 4 - Smooth/snake-like (normal)", "Type 5 - Soft blobs (low fibre)", "Type 6 - Mushy/fluffy (inflammation)", "Type 7 - Liquid (diarrhoea)"]},
                    {"id": "con_flatus", "type": "toggle", "label": "Passing Flatus?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: NOT passing flatus + constipation + distension = ?obstruction. Urgent surgical assessment.", "red_flag_negative": ""},
                    {"id": "con_recent_surgery", "type": "toggle", "label": "Recent Abdominal Surgery?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent surgery + constipation = ?ileus/obstruction. Urgent assessment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms & Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "con_associated", "type": "multi_select", "label": "Associated Symptoms", "required": True, "options": ["Abdominal distension", "Vomiting", "Difficulty passing urine", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Vomiting + constipation = ?obstruction. Urgent surgical assessment.", "red_flag_negative": ""},
                    {"id": "con_red_flags", "type": "multi_select", "label": "Red Flag Screen", "required": True, "options": ["Weight loss", "PR bleeding", "Vomiting", "None - apart from change in bowel habit"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + PR bleeding + change in bowel habit = ?colorectal cancer. Urgent 2WW referral.", "red_flag_negative": ""},
                    {"id": "con_family_bowel_ca", "type": "toggle", "label": "Family History of Bowel Cancer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx bowel cancer + change in bowel habit = lower threshold for investigation.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Medication Review",
                "section_type": "history",
                "questions": [
                    {"id": "con_meds", "type": "multi_select", "label": "Constipating Medications", "required": True, "options": ["Antimuscarinics / Oxybutynin", "Tricyclic Antidepressants (Amitriptyline)", "Anti-epileptics", "Antihistamines", "Antipsychotics", "Antispasmodics", "Calcium supplements", "Diuretics", "Iron supplements", "Verapamil", "Opioids", "None of the above"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "con_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 72"},
                    {"id": "con_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Generalised tenderness on deep palpation, no guarding/rigidity, no distension, BS present", "Localised tenderness", "Guarding / rigidity present - RED FLAG", "Distension present", "Abnormal bowel sounds"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Guarding/rigidity = ?acute abdomen/obstruction. Urgent surgical assessment.", "red_flag_negative": ""},
                    {"id": "con_lymph", "type": "multi_select", "label": "Lymphadenopathy", "required": False, "options": ["Axillary", "Inguinal", "None palpable"]},
                    {"id": "con_pr", "type": "single_select", "label": "PR Examination", "required": False, "options": ["No rectal wall irregularities", "Irregularity / mass palpated - RED FLAG", "Impacted stool palpated", "PR exam not performed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Rectal mass = ?colorectal cancer. Urgent 2WW.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Functional Constipation (low fibre, dehydration, sedentary)",
                    "Drug-Induced Constipation",
                    "Irritable Bowel Syndrome (IBS-C)",
                    "Faecal Impaction",
                    "Colorectal Cancer (RED FLAG - weight loss, PR bleeding, mass)",
                    "Intestinal Obstruction (RED FLAG - vomiting, no flatus, distension)",
                    "Hypothyroidism",
                    "Hypercalcaemia"
                ],
                "questions": [
                    {"id": "con_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Constipation - no red flags", "Constipation with red flag features - investigate", "Faecal impaction", "Alternative diagnosis"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: no improvement after 1-2 weeks of treatment, red flags develop (weight loss, PR bleeding, vomiting, severe pain), or inability to pass flatus. First-line: Movicol (macrogol) or Ispaghula husk. If stool soft but difficult to pass: Senna PO for 5 days or Dulcolax suppositories for 5 days. Faecal impaction protocol: Day 1 = 2 sachets BD, Day 2 = 2 sachets TDS, Day 3 = 2 sachets QDS, then maintenance 1 sachet BD for 7 days. Lifestyle: increase fruit/veg (5/day), porridge/fibre, water 2L/day, regular exercise. If no improvement: check FBC, LFTs, ESR/CRP, coeliac screen. If red flags: refer gastroenterology or 2WW colorectal.",
                "questions": [
                    {"id": "con_laxative", "type": "single_select", "label": "First-Line Laxative", "required": False, "options": ["Movicol (Macrogol) 1-2 sachets daily", "Ispaghula Husk (Fybogel)", "Lactulose", "None"]},
                    {"id": "con_stool_soft", "type": "single_select", "label": "If Stool Soft But Difficult to Pass", "required": False, "options": ["Senna PO for 5 days", "Dulcolax suppositories for 5 days", "Not required"]},
                    {"id": "con_disimpaction", "type": "single_select", "label": "Faecal Disimpaction Protocol", "required": False, "options": ["Day 1: 2 sachets BD → Day 2: 2 sachets TDS → Day 3: 2 sachets QDS → Maintenance: 1 sachet BD x7d", "Not indicated"]},
                    {"id": "con_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Increase fruit/vegetable intake (5/day)", "Porridge / fibre", "Increase water intake (2L/day)", "Regular exercise"]},
                    {"id": "con_investigations", "type": "multi_select", "label": "Investigations (If Red Flags or No Improvement)", "required": False, "options": ["FBC", "Bone/Liver profile (LFTs)", "ESR / CRP", "Coeliac screen (IgA TTG)", "None"]},
                    {"id": "con_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 1-2 weeks, sooner if red flags"}
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
    seed_constipation()