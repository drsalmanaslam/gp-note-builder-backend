from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_hypothyroidism():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Endocrinology").first()
    if not category: category = Category(name="Endocrinology"); db.add(category); db.commit()

    t = {
        "title": "Hypothyroidism",
        "description": "Focused assessment for hypothyroidism covering symptom screening, TFT interpretation, treatment thresholds, Eltroxin dosing, and subclinical monitoring pathways.",
        "category": "Endocrinology",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hypo_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Feeling cold, tired, and gaining weight for 6 months"},
                    {"id": "hypo_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 48"},
                    {"id": "hypo_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Cold intolerance (cold when others hot)", "Weight gain", "Fatigue / exhaustion", "Hoarse / husky voice", "Muscle aches", "Dry skin", "Dry hair / hair loss", "Constipation", "Menstrual disturbance", "None"]},
                    {"id": "hypo_duration", "type": "text", "label": "Symptom Duration", "required": True, "placeholder": "e.g., 6 months"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hypo_skin_hair", "type": "multi_select", "label": "Skin / Hair Findings", "required": True, "options": ["Dry skin", "Thinning temporal hair / eyebrows (lateral third)", "None present"]},
                    {"id": "hypo_neck", "type": "single_select", "label": "Neck Examination", "required": True, "options": ["Goitre present", "No goitre"]},
                    {"id": "hypo_reflexes", "type": "single_select", "label": "Reflexes", "required": True, "options": ["Slow-relaxing (hypothyroid)", "Normal"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "hypo_tsh", "type": "number", "label": "TSH (mU/L)", "required": False, "placeholder": "e.g., 12.5 (NR: 0.4-4.0)"},
                    {"id": "hypo_ft4", "type": "number", "label": "Free T4 (pmol/L)", "required": False, "placeholder": "e.g., 8 (NR: 9-25)"},
                    {"id": "hypo_tft_pattern", "type": "single_select", "label": "TFT Pattern", "required": False, "options": ["TSH high + T4 low = Overt Hypothyroidism", "TSH high + T4 normal = Subclinical Hypothyroidism", "Awaiting results"]},
                    {"id": "hypo_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["TSH", "Free T4", "Coeliac screen (IgA TTG)", "Immunoglobulin levels (IgA)", "Anti-TPO antibodies", "None"]}
                ]
            },
            {
                "title": "Treatment Decision",
                "section_type": "assessment",
                "differentials": [
                    "Overt Hypothyroidism (TSH high + T4 low)",
                    "Subclinical Hypothyroidism (TSH high + T4 normal)",
                    "Hashimoto's Thyroiditis (anti-TPO positive + goitre)",
                    "Post-Radioiodine / Post-Thyroidectomy Hypothyroidism",
                    "Drug-Induced (Amiodarone, Lithium, Immunotherapy)",
                    "Iodine Deficiency / Excess"
                ],
                "questions": [
                    {"id": "hypo_tsh_level", "type": "single_select", "label": "TSH Level Category", "required": False, "options": ["TSH >10 → TREAT (regardless of symptoms)", "TSH 5-10 + symptomatic / infertility / pregnant / goitre / anti-TPO+ → TREAT", "TSH 5-10, asymptomatic, no risk factors → Do NOT treat", "TSH normal = Euthyroid"]},
                    {"id": "hypo_subclinical_decision", "type": "single_select", "label": "Subclinical Hypothyroidism Management (BMJ 2019)", "required": False, "options": ["Do NOT offer thyroxine - strong recommendation (BMJ 2019;365:l2006)", "Trial of treatment justified - exception criteria met"], "is_red_flag": True, "red_flag_positive": "RED FLAG: BMJ 2019 strong recommendation = do NOT routinely treat subclinical hypothyroidism. Exceptions: pregnancy, planning pregnancy, already on treatment, TSH>20, age<30.", "red_flag_negative": ""},
                    {"id": "hypo_exception_criteria", "type": "multi_select", "label": "Exception Criteria (for trial of treatment)", "required": False, "options": ["Pregnancy", "Planning pregnancy", "Risk of unplanned pregnancy", "Already established on treatment", "Very severe symptoms", "TSH >20", "Age <30 years", "None - routine recommendation applies"]}
                ]
            },
            {
                "title": "Pharmacotherapy",
                "section_type": "plan",
                "questions": [
                    {"id": "hypo_eltroxin_dose", "type": "single_select", "label": "Eltroxin (Levothyroxine) Initiation", "required": False, "options": ["Start 75mcg OD (standard)", "Start 50mcg OD (elderly/cardiac history)", "Start 25mcg OD (frail/ischaemic heart disease)", "Start 100mcg OD (young/fit)", "Alternative starting dose", "Not started - subclinical, criteria not met"]},
                    {"id": "hypo_alt_dose", "type": "text", "label": "Alternative Starting Dose (mcg)", "required": False, "placeholder": "e.g., 50"},
                    {"id": "hypo_repeat_tft", "type": "single_select", "label": "Repeat TFTs After Initiation", "required": False, "options": ["3 months (standard)", "6 weeks (pregnancy/urgent)", "6 months (stable elderly)", "Not applicable"]}
                ]
            },
            {
                "title": "Subclinical Monitoring Pathway (NICE 2018)",
                "section_type": "plan",
                "questions": [
                    {"id": "hypo_tsh_normalised", "type": "single_select", "label": "If Untreated + TSH Normalises on Repeat", "required": False, "options": ["No further testing (asymptomatic, anti-TPO negative, no goitre)", "Continue monitoring - risk factors present"]},
                    {"id": "hypo_tsh_high", "type": "single_select", "label": "If TSH Remains High", "required": False, "options": ["Repeat TFTs 6-monthly for 2 years, then annually", "Not applicable"]},
                    {"id": "hypo_anti_tpo", "type": "single_select", "label": "If Anti-TPO Positive or Goitre Present", "required": False, "options": ["Annual TFTs", "Not applicable"]},
                    {"id": "hypo_age_over65", "type": "single_select", "label": "If Age >65, Healthy, Asymptomatic", "required": False, "options": ["Repeat TFTs not required", "Repeat TFTs indicated - symptoms developed"]}
                ]
            },
            {
                "title": "Impression & Plan",
                "section_type": "plan",
                "safety_netting": "Eltroxin monitoring targets: TSH 0.4-2.5 mU/L. No dose change if asymptomatic with TSH in upper half of reference range. TSH <0.1 = AVOID (risk osteoporosis/AF). TSH 0.1-0.4 = tolerated in younger patients. Low TSH in >60 years = prompt 25mcg reduction (3-fold increased AF risk + osteoporosis). Persistently high TSH despite Eltroxin = consider coeliac disease or autoimmune gastritis. Subclinical hypothyroidism: BMJ 2019 strong recommendation NOT to treat. Exceptions: pregnancy/planning pregnancy, already on treatment, TSH>20, age<30 with severe symptoms. Follow NICE monitoring pathway based on risk factors.",
                "questions": [
                    {"id": "hypo_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Overt Hypothyroidism - Treat", "Subclinical Hypothyroidism - Do NOT Treat", "Subclinical Hypothyroidism - Trial Treatment (exception)", "Euthyroid - No action", "Biochemical confirmation pending"]},
                    {"id": "hypo_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP managed", "Endocrinology - treatment-resistant", "Endocrinology - pregnancy-related", "Endocrinology - diagnostic uncertainty"]},
                    {"id": "hypo_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3 months repeat TFTs if treated, 6-monthly monitoring if subclinical"}
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
    seed_hypothyroidism()