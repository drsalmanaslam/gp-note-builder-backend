from app.database import SessionLocal
from app.models import User, Template, Category

def seed_ibs():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Irritable Bowel Syndrome (IBS)",
        "description": "Focused assessment for IBS covering Rome IV diagnostic criteria, IBD red flags, dietary/lifestyle management, and pharmacotherapy by subtype.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Symptom Profile",
                "section_type": "history",
                "questions": [
                    {"id": "ibs_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Abdominal pain, bloating, and alternating bowel habit for 6 months"},
                    {"id": "ibs_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Abdominal pain", "Bloating", "Change in bowel habit", "Abdominal distension"]},
                    {"id": "ibs_subtype", "type": "single_select", "label": "Predominant Bowel Habit", "required": True, "options": ["IBS-D (Diarrhoea predominant)", "IBS-C (Constipation predominant)", "IBS-M (Mixed)", "IBS-U (Unclassified)"]}
                ]
            },
            {
                "title": "Rome IV Diagnostic Criteria",
                "section_type": "history",
                "questions": [
                    {"id": "ibs_rome", "type": "multi_select", "label": "Rome IV Features (≥2 of the following)", "required": True, "options": ["Pain relieved by defaecation", "Altered stool frequency", "Altered stool form (Bristol scale)", "Straining", "Urgency", "Incomplete evacuation", "PR mucus", "Symptoms worse after eating"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Rome IV = recurrent abdominal pain ≥1 day/week for 3 months + ≥2 features. Onset ≥6 months ago.", "red_flag_negative": ""},
                    {"id": "ibs_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 6 months (Rome IV requires onset ≥6 months ago)"}
                ]
            },
            {
                "title": "Psychological & Red Flag Screening",
                "section_type": "history",
                "questions": [
                    {"id": "ibs_psych", "type": "single_select", "label": "Psychological Screen", "required": True, "options": ["Positive - low mood / anhedonia / anxiety", "Negative - no anhedonia / anxiety"]},
                    {"id": "ibs_stressors", "type": "toggle", "label": "Psychosocial Stressors? (Home / work / relationship)", "required": False},
                    {"id": "ibs_red_flags", "type": "multi_select", "label": "IBD / Red Flag Screen", "required": True, "options": ["Family history of IBD", "PR blood / melaena", "Weight loss", "Mouth ulcers", "Joint pain", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: IBD red flags present = ?Crohn's/UC. Faecal calprotectin + gastroenterology referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ibs_general", "type": "single_select", "label": "General Examination", "required": True, "options": ["Normal - no anaemia, no jaundice", "Pallor present (anaemia - RED FLAG)", "Jaundice present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Anaemia + GI symptoms = ?IBD, coeliac, malignancy. Investigate.", "red_flag_negative": ""},
                    {"id": "ibs_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, non-tender, no masses/organomegaly", "Tenderness present", "Mass palpated", "Organomegaly"]},
                    {"id": "ibs_pelvic", "type": "single_select", "label": "Pelvic Examination (Females)", "required": False, "options": ["No ovarian masses", "Mass palpated - RED FLAG", "Not performed"]},
                    {"id": "ibs_pr", "type": "single_select", "label": "PR Examination", "required": False, "options": ["No rectal wall irregularities", "Irregularity / mass palpated - RED FLAG", "Not performed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Irritable Bowel Syndrome (IBS)",
                    "Inflammatory Bowel Disease (Crohn's / UC)",
                    "Coeliac Disease",
                    "Colorectal Cancer (RED FLAG)",
                    "Ovarian Cancer (females - Ca-125 + pelvic exam)",
                    "Lactose Intolerance",
                    "Small Intestinal Bacterial Overgrowth (SIBO)",
                    "Diverticular Disease"
                ],
                "questions": [
                    {"id": "ibs_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["IBS - Rome IV criteria met", "IBS - Rome IV criteria met, psychological component", "Red flag features present - investigate further", "Alternative diagnosis suspected"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: red flags develop (weight loss, PR bleeding, nocturnal symptoms), symptoms worsen significantly, or no improvement after 4-6 weeks of first-line management. IBS is a clinical diagnosis based on Rome IV criteria - no diagnostic test exists. First-line: dietary + lifestyle advice. Regular meals, oats/linseed for bloating, 8 cups fluid/day, limit fruit to <3 portions/day, take time to eat, regular exercise, relaxation. Symptom diary. IBS-D: Loperamide. IBS-C: Ispaghula husk or Movicol. Antispasmodic: Colofac. Probiotic: Alflorex OD. Second-line: Amitriptyline 10mg nocte (visceral hypersensitivity). If diagnostic uncertainty or red flags: FBC, coeliac screen, LFTs, U&Es, ESR/CRP, CEA, Ca-125 (females).",
                "questions": [
                    {"id": "ibs_diet", "type": "multi_select", "label": "Dietary & Lifestyle Advice", "required": False, "options": ["Regular meals - don't skip meals", "Oats / linseed for bloating", "8 cups of fluid daily", "Limit fresh fruit to <3 portions/day", "Take time to eat", "Regular exercise", "Relaxation and leisure time", "Symptom diary"]},
                    {"id": "ibs_diarrhoea_rx", "type": "toggle", "label": "Loperamide? (IBS-D - diarrhoea predominant)", "required": False},
                    {"id": "ibs_constipation_rx", "type": "single_select", "label": "Constipation Treatment (IBS-C)", "required": False, "options": ["Ispaghula Husk (Fybogel)", "Movicol (Macrogol) - aim for soft stool", "None"]},
                    {"id": "ibs_antispasmodic", "type": "toggle", "label": "Colofac (Mebeverine) 135mg TDS?", "required": False},
                    {"id": "ibs_probiotic", "type": "toggle", "label": "Alflorex (Bifidobacterium) Once Daily?", "required": False},
                    {"id": "ibs_amitriptyline", "type": "toggle", "label": "Amitriptyline 10mg Nocte? (Second-line - visceral hypersensitivity)", "required": False},
                    {"id": "ibs_investigations", "type": "multi_select", "label": "Investigations (If Red Flags or Diagnostic Uncertainty)", "required": False, "options": ["FBC", "Coeliac screen (IgA TTG)", "LFTs", "Renal function (U&Es)", "ESR / CRP", "CEA", "Ca-125 (females)", "None"]},
                    {"id": "ibs_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review after 4-6 weeks dietary/lifestyle trial, sooner if red flags"}
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
    seed_ibs()