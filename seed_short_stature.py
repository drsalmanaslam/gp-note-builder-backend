from app.database import SessionLocal
from app.models import User, Template, Category

def seed_short_stature():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: category = Category(name="Paediatrics"); db.add(category); db.commit()

    t = {
        "title": "Short Stature",
        "description": "Focused assessment for short stature in children covering mid-parental height, red flags, investigations, and referral criteria.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "History & Growth Concern",
                "section_type": "history",
                "questions": [
                    {"id": "ss_sex", "type": "single_select", "label": "Sex", "required": True, "options": ["Male", "Female"]},
                    {"id": "ss_age", "type": "number", "label": "Age (years)", "required": True, "placeholder": "e.g., 8"},
                    {"id": "ss_concern", "type": "text", "label": "Reason for Referral / Concern", "required": True, "placeholder": "e.g., Parental concern re short stature compared to peers"},
                    {"id": "ss_birth_gestation", "type": "single_select", "label": "Gestation at Birth", "required": True, "options": ["Term (≥37 weeks)", "Preterm (34-36 weeks)", "Preterm (32-33 weeks)", "Preterm (<32 weeks)"]},
                    {"id": "ss_birth_weight", "type": "number", "label": "Birth Weight (kg)", "required": False, "placeholder": "e.g., 3.2"},
                    {"id": "ss_birth_length", "type": "number", "label": "Birth Length (cm)", "required": False, "placeholder": "e.g., 50"},
                    {"id": "ss_nnu", "type": "toggle", "label": "NICU / SCBU Admission?", "required": True},
                    {"id": "ss_diet", "type": "single_select", "label": "Diet / Appetite", "required": True, "options": ["Good appetite, balanced diet", "Poor appetite", "Restricted diet (voluntary)", "Normal"]},
                    {"id": "ss_development", "type": "single_select", "label": "Developmental Milestones", "required": True, "options": ["Normal - all met", "Delayed gross motor", "Delayed speech/language", "Global delay - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Developmental delay + short stature = ?syndromic, genetic, or chronic disease. Urgent paediatric referral.", "red_flag_negative": ""},
                    {"id": "ss_puberty", "type": "single_select", "label": "Pubertal Status", "required": False, "options": ["Pre-pubertal", "Early puberty (<8F/<9M)", "Normal puberty for age", "Delayed puberty (>13F/>14M)", "Not applicable (young child)"]}
                ]
            },
            {
                "title": "Mid-Parental Target Height",
                "section_type": "history",
                "questions": [
                    {"id": "ss_mother_height", "type": "number", "label": "Mother's Height (cm)", "required": True, "placeholder": "e.g., 160"},
                    {"id": "ss_father_height", "type": "number", "label": "Father's Height (cm)", "required": True, "placeholder": "e.g., 175"},
                    {"id": "ss_target_height", "type": "number", "label": "Calculated Target Height (cm)", "required": True, "placeholder": "Boy = (Father+Mother+13)/2 | Girl = (Father-13+Mother)/2"},
                    {"id": "ss_below_target", "type": "toggle", "label": ">2 SD Below Mid-Parental Target?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: >2 SD below target height = pathological short stature. Needs full workup + paediatric referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Systemic & Endocrine",
                "section_type": "history",
                "questions": [
                    {"id": "ss_diarrhoea", "type": "toggle", "label": "Chronic Diarrhoea / Steatorrhoea? (Coeliac/IBD)", "required": True},
                    {"id": "ss_recurrent_infections", "type": "toggle", "label": "Recurrent Chest Infections / LRTIs? (CF/Immunodeficiency)", "required": False},
                    {"id": "ss_headaches", "type": "toggle", "label": "Headaches?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Headaches + short stature = ?pituitary/craniopharyngioma. Visual fields + fundoscopy. Urgent paediatric endocrinology.", "red_flag_negative": ""},
                    {"id": "ss_visual_disturbance", "type": "toggle", "label": "Visual Disturbance?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms = ?pituitary mass. Urgent MRI + paediatric endocrinology.", "red_flag_negative": ""},
                    {"id": "ss_morning_vomiting", "type": "toggle", "label": "Morning Vomiting? (Raised ICP)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Morning vomiting + headaches = ?raised ICP from intracranial mass. Urgent CT/MRI.", "red_flag_negative": ""},
                    {"id": "ss_polyuria_polydipsia", "type": "toggle", "label": "Polyuria / Polydipsia? (Diabetes insipidus)", "required": False},
                    {"id": "ss_cold_intolerance", "type": "toggle", "label": "Cold Intolerance / Constipation / Fatigue? (Hypothyroidism)", "required": False},
                    {"id": "ss_steroids", "type": "toggle", "label": "Prolonged Steroid Use? (Iatrogenic Cushing's)", "required": False},
                    {"id": "ss_family_short_stature", "type": "toggle", "label": "Family History of Short Stature / Delayed Puberty?", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ss_height", "type": "number", "label": "Height (cm)", "required": True, "placeholder": "e.g., 115"},
                    {"id": "ss_height_centile", "type": "text", "label": "Height Centile", "required": True, "placeholder": "e.g., <3rd centile"},
                    {"id": "ss_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 20"},
                    {"id": "ss_weight_centile", "type": "text", "label": "Weight Centile", "required": False, "placeholder": "e.g., 5th centile"},
                    {"id": "ss_sitting_height", "type": "number", "label": "Sitting Height (cm) - Body Proportions", "required": False, "placeholder": "e.g., 60"},
                    {"id": "ss_visual_fields", "type": "single_select", "label": "Visual Fields", "required": True, "options": ["Normal", "Abnormal - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual field defect = ?craniopharyngioma. Urgent MRI.", "red_flag_negative": ""},
                    {"id": "ss_papilloedema", "type": "toggle", "label": "Papilloedema? (Fundoscopy)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Papilloedema = raised ICP. Urgent CT/MRI.", "red_flag_negative": ""},
                    {"id": "ss_turner", "type": "multi_select", "label": "Turner Syndrome Features (Girls)", "required": False, "options": ["Webbed neck", "Wide-spaced nipples", "Cubitus valgus", "Low hairline", "None", "Not applicable (male)"]},
                    {"id": "ss_cafe_au_lait", "type": "toggle", "label": "Café-au-Lait Spots? (≥6 = NF1)", "required": False},
                    {"id": "ss_cushingoid", "type": "toggle", "label": "Cushingoid Features? (Central obesity, striae, buffalo hump)", "required": False},
                    {"id": "ss_hypothyroid", "type": "toggle", "label": "Hypothyroid Features? (Goitre, dry skin, bradycardia)", "required": False}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Familial Short Stature (within mid-parental target)",
                    "Constitutional Delay of Growth & Puberty (CDGP)",
                    "Coeliac Disease",
                    "Inflammatory Bowel Disease (Crohn's/UC)",
                    "Hypothyroidism",
                    "Growth Hormone Deficiency",
                    "Turner Syndrome (girls)",
                    "Cushing Syndrome (iatrogenic/endogenous)",
                    "Skeletal Dysplasia (disproportionate short stature)",
                    "Chronic Kidney Disease",
                    "Cystic Fibrosis",
                    "Psychosocial Deprivation",
                    "Craniopharyngioma / Pituitary Mass (RED FLAG)",
                    "Noonan Syndrome / Other Genetic Syndromes"
                ],
                "questions": [
                    {"id": "ss_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC + Ferritin", "U&E / Creatinine", "LFTs", "Bone Profile (Ca, PO4, ALP)", "Vitamin D", "ESR / CRP", "TFTs (TSH, Free T4)", "Coeliac Screen (IgA tTG + total IgA)", "IGF-1 / IGFBP-3", "Karyotype (girls if Turner suspected)"]},
                    {"id": "ss_urinalysis", "type": "toggle", "label": "Urinalysis? (Renal tubular acidosis, chronic disease)", "required": False},
                    {"id": "ss_bone_age", "type": "toggle", "label": "Left Hand/Wrist X-Ray for Bone Age?", "required": True}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return sooner if: headaches, visual disturbances, morning vomiting, severe fatigue, or polyuria/polydipsia develop. Growth velocity <4 cm/year in childhood is ABNORMAL and requires paediatric endocrine referral regardless of absolute centile. Bone age X-ray essential to differentiate familial short stature from constitutional delay. If Turner syndrome suspected in girls: urgent karyotype + paediatric endocrine referral. Plot growth on UK-WHO 2-18 chart. Provide patient information leaflet on short stature.",
                "questions": [
                    {"id": "ss_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["?Familial short stature", "?Constitutional delay of growth & puberty", "?Pathological short stature - investigating", "?Coeliac disease", "?Hypothyroidism", "?Growth hormone deficiency", "?Turner syndrome", "Suspected intracranial mass - REFER URGENTLY"]},
                    {"id": "ss_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["None - monitor in primary care", "General Paediatrics", "Paediatric Endocrinology", "Paediatric Gastroenterology (?Coeliac/IBD)", "Urgent Paediatric Endocrinology (?mass)", "Dietitian"]},
                    {"id": "ss_growth_chart", "type": "toggle", "label": "Growth Plotted on UK-WHO 2-18 Chart?", "required": True},
                    {"id": "ss_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3-6 months with repeat growth measurements + blood results"}
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
    seed_short_stature()