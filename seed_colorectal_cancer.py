from app.database import SessionLocal
from app.models import User, Template, Category

def seed_colorectal_cancer():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Suspected Colorectal Cancer - NCCP GP Referral Pathway",
        "description": "National NCCP guideline-based colorectal cancer referral pathway covering direct endoscopy criteria, colorectal OPD indications, emergency referral, and required pre-referral investigations.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "crc_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Rectal bleeding", "Change in bowel habit", "Unexplained weight loss", "Abdominal pain", "Iron deficiency anaemia", "Palpable abdominal mass", "Palpable rectal mass", "Anal mass", "Anal ulceration", "Diarrhoea", "Constipation (single symptom)", "Anal symptoms (piles, prolapse, fissure)"]},
                    {"id": "crc_bleeding_duration", "type": "single_select", "label": "Rectal Bleeding Duration", "required": False, "options": [">6 weeks - persistent (RED FLAG)", "<6 weeks"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Persistent rectal bleeding >6 weeks = urgent referral criterion.", "red_flag_negative": ""},
                    {"id": "crc_bowel_change_duration", "type": "single_select", "label": "Change in Bowel Habit Duration", "required": False, "options": [">6 weeks", "<6 weeks"]},
                    {"id": "crc_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 62"},
                    {"id": "crc_family_history", "type": "single_select", "label": "Significant Family History", "required": True, "options": ["Yes - 1st degree relative CRC <50, or ≥2 relatives with CRC/endometrial, or Lynch/polyposis syndrome", "No significant family history"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Significant FHx = urgent referral if age <40 with rectal bleeding/change in bowel habit.", "red_flag_negative": ""},
                    {"id": "crc_previous_colonoscopy", "type": "toggle", "label": "Previous Colonoscopy?", "required": False},
                    {"id": "crc_pmh", "type": "multi_select", "label": "Relevant PMHx", "required": True, "options": ["Ulcerative Colitis", "Crohn's Disease", "Neither"]},
                    {"id": "crc_lifestyle", "type": "multi_select", "label": "Lifestyle Risk Factors", "required": False, "options": ["Obesity", "Alcohol excess", "Diet high in fat, red/processed meat, low fibre", "Sedentary lifestyle", "Smoking", "None identified"]},
                    {"id": "crc_bowel_screen", "type": "single_select", "label": "Bowel Screen Participation", "required": False, "options": ["Participating", "Not yet registered - advise participation", "Not applicable (age)"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "crc_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Palpable abdominal mass - RED FLAG", "No mass palpated"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Palpable abdominal mass = refer colorectal OPD (not direct endoscopy).", "red_flag_negative": ""},
                    {"id": "crc_dre", "type": "single_select", "label": "Digital Rectal Examination (DRE)", "required": False, "options": ["Palpable rectal mass - RED FLAG", "Anal mass", "Anal ulceration", "Normal - no mass or ulceration", "Not performed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Palpable rectal mass = refer colorectal OPD. Negative DRE does NOT rule out need to refer.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Pre-Referral Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "crc_fbc", "type": "toggle", "label": "FBC Performed? (MANDATORY before referral)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FBC is MANDATORY prior to referral. Tumour markers of NO diagnostic benefit. Imaging NOT required prior to referral.", "red_flag_negative": ""},
                    {"id": "crc_hb", "type": "number", "label": "Haemoglobin (g/100ml)", "required": False, "placeholder": "e.g., 10.2"},
                    {"id": "crc_ferritin", "type": "number", "label": "Ferritin (IDA sole indication → include ferritin)", "required": False, "placeholder": "e.g., 8 (Coeliac screen if <55 + IDA)"}
                ]
            },
            {
                "title": "Pathway A - Direct to Endoscopy Criteria",
                "section_type": "assessment",
                "questions": [
                    {"id": "crc_criterion1", "type": "toggle", "label": "Criterion 1: Age ≥60 + (PR bleeding >6wk OR bowel change >6wk OR unexplained weight loss + CRC symptoms)?", "required": True},
                    {"id": "crc_criterion2", "type": "toggle", "label": "Criterion 2: Age ≥40 + PR bleeding AND bowel change >6wk?", "required": True},
                    {"id": "crc_criterion3", "type": "toggle", "label": "Criterion 3: Unexplained IDA? (Male Hb ≤11 / Non-menstruating Female Hb ≤10)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: IDA in patients <55 = consider coeliac disease as main cause. Check coeliac screen.", "red_flag_negative": ""},
                    {"id": "crc_criterion4", "type": "toggle", "label": "Criterion 4: Age <40 + PR bleeding/bowel change + significant FHx CRC or IBD?", "required": True},
                    {"id": "crc_direct_endo", "type": "toggle", "label": "Suitable for Direct Referral to Endoscopy? (Any criterion met)", "required": True}
                ]
            },
            {
                "title": "Pathway B - Colorectal OPD (NOT Direct Endoscopy)",
                "section_type": "assessment",
                "questions": [
                    {"id": "crc_opd_criteria", "type": "multi_select", "label": "Refer Direct to Colorectal OPD (Not Endoscopy)", "required": False, "options": ["Palpable abdominal mass", "Palpable rectal mass", "Anal mass", "Anal ulceration", "Suspected CRC on imaging (incidental - needs MDT)", "Suspicion of CRC not fitting direct-referral criteria", "None of these"]}
                ]
            },
            {
                "title": "Pathway C - NOT for Direct Endoscopy",
                "section_type": "assessment",
                "questions": [
                    {"id": "crc_not_endo", "type": "multi_select", "label": "NOT Suitable for Direct Endoscopy", "required": False, "options": ["Diarrhoea <6 weeks", "Constipation as single symptom", "Abdominal pain without altered bowel habit", "Anal symptoms alone (piles, prolapse, fissure)", "Low ferritin, age >50, normal Hb (still consider endoscopy in males)", "Young person + bloody diarrhoea → refer GI (?IBD) URGENTLY"]}
                ]
            },
            {
                "title": "Pathway D - Emergency",
                "section_type": "assessment",
                "questions": [
                    {"id": "crc_emergency", "type": "toggle", "label": "Suspected Bowel Obstruction or Perforation? → EMERGENCY ED", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Obstruction/perforation = EMERGENCY. Refer immediately to Emergency Department.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Referral Decision",
                "section_type": "plan",
                "safety_netting": "All patients require FBC prior to referral. Tumour markers are of NO diagnostic benefit. Imaging is NOT required prior to referral. Negative DRE does NOT rule out the need to refer. IDA in <55 years: coeliac disease is main cause - check coeliac screen. Patient must be informed they are being referred for colonoscopy. Direct endoscopy patients should be considered fit to tolerate the procedure. Urgent referrals: appointment within 4 weeks where possible. Routine: seen within ~13 weeks. Referral MUST include: previous endoscopy details, relevant PMHx, recent FBC.",
                "questions": [
                    {"id": "crc_impression", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Suspected CRC - meets direct endoscopy criteria", "Suspected CRC - requires colorectal OPD (not direct endoscopy)", "Emergency presentation - refer to ED", "Does not meet referral criteria at this time", "Suspected IBD - urgent gastroenterology referral"]},
                    {"id": "crc_referral_type", "type": "single_select", "label": "Referral Type", "required": True, "options": ["Direct to Endoscopy", "Direct to Colorectal OPD", "Urgent Gastroenterology (suspected IBD)", "Emergency Department", "No referral indicated"]},
                    {"id": "crc_priority", "type": "single_select", "label": "Referral Priority", "required": False, "options": ["Urgent (appointment within 4 weeks)", "Routine (seen within ~13 weeks)"]},
                    {"id": "crc_checklist", "type": "multi_select", "label": "Referral Includes", "required": False, "options": ["Previous endoscopy details", "Relevant past medical history", "Recent FBC result"]},
                    {"id": "crc_patient_informed", "type": "toggle", "label": "Patient Informed of Referral Reason? (Colonoscopy)", "required": True},
                    {"id": "crc_fitness", "type": "toggle", "label": "Patient Fit for Endoscopy?", "required": False},
                    {"id": "crc_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Referral sent, safety-net given, or await coeliac screen if IDA <55"}
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
    seed_colorectal_cancer()