from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_antenatal_routine():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Routine Antenatal Visit",
        "description": "Structured routine antenatal check covering pre-eclampsia red flags, SFH measurement, foetal heart auscultation, vaccination schedule, and Group B Strep guidance.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Pre-Eclampsia / Complications Screen",
                "section_type": "history",
                "questions": [
                    {"id": "anv_headache", "type": "toggle", "label": "Headache?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Headache + HTN/proteinuria = ?pre-eclampsia. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "anv_abdo_pain", "type": "toggle", "label": "Abdominal Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Abdominal pain = ?pre-eclampsia, placental abruption. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "anv_oedema", "type": "toggle", "label": "Ankle/Leg Oedema?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden/severe oedema + HTN = ?pre-eclampsia.", "red_flag_negative": ""},
                    {"id": "anv_reduced_fm", "type": "toggle", "label": "Reduced Foetal Movement?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced foetal movement = urgent CTG + obstetric assessment.", "red_flag_negative": ""},
                    {"id": "anv_proteinuria", "type": "toggle", "label": "Proteinuria?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Proteinuria + HTN = ?pre-eclampsia. Urgent obstetric referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History - Current Visit",
                "section_type": "history",
                "questions": [
                    {"id": "anv_gestation", "type": "text", "label": "Gestational Age at This Visit (Weeks)", "required": True, "placeholder": "e.g., 28 weeks"},
                    {"id": "anv_bloods_reviewed", "type": "single_select", "label": "Bloods Reviewed - Within Normal Limits?", "required": True, "options": ["Yes - Normal", "No - Abnormal (Specify)", "Awaiting Results"]},
                    {"id": "anv_wellbeing", "type": "single_select", "label": "General Wellbeing", "required": True, "options": ["Well, No Concerns", "Minor Concerns", "Significant Concerns - Escalate"]},
                    {"id": "anv_symptoms", "type": "multi_select", "label": "Symptom Screen", "required": True, "options": ["Ankle Oedema", "Headache", "Abdominal Pain", "Nausea/Vomiting", "None"]},
                    {"id": "anv_fm", "type": "single_select", "label": "Foetal Movement", "required": True, "options": ["Good / Normal", "Reduced - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced FM = urgent CTG + obstetric assessment.", "red_flag_negative": ""},
                    {"id": "anv_questions_addressed", "type": "toggle", "label": "Patient Questions Addressed?", "required": False},
                    {"id": "anv_flu_vaccine", "type": "toggle", "label": "Influenza Vaccine Given This Pregnancy?", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "anv_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 118/72", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP ≥140/90 = ?pre-eclampsia. Check urinalysis + escalate if proteinuria.", "red_flag_negative": ""},
                    {"id": "anv_urinalysis", "type": "single_select", "label": "Urinalysis - Proteinuria?", "required": True, "options": ["Negative", "Trace", "+", "++ or More - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Proteinuria ≥1+ + HTN = pre-eclampsia. Urgent obstetric referral.", "red_flag_negative": ""},
                    {"id": "anv_oedema_exam", "type": "toggle", "label": "Ankle Oedema on Examination?", "required": False},
                    {"id": "anv_fm_palpation", "type": "toggle", "label": "Foetal Movement on Palpation?", "required": False},
                    {"id": "anv_sfh", "type": "number", "label": "Symphysis-Fundal Height (cm) - From 24 Weeks", "required": False, "placeholder": "e.g., 28 (Should match gestational age ±2cm)"},
                    {"id": "anv_fhr", "type": "single_select", "label": "Foetal Heart Rate via Doppler (From 20 Weeks)", "required": False, "options": ["Heard - Normal", "Not Heard - RED FLAG", "Not Applicable (<20 Weeks)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: FHR not heard = urgent ultrasound.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Vaccination Schedule (Reference)",
                "section_type": "assessment",
                "questions": [
                    {"id": "anv_pertussis", "type": "single_select", "label": "Pertussis (Whooping Cough) Vaccine - Best 16-36 Weeks", "required": False, "options": ["Given", "Due - Advise Today", "Not Yet Due", "Declined"]},
                    {"id": "anv_rsv", "type": "single_select", "label": "RSV Vaccine (Abrysvo) - CDC 32-36 Weeks During RSV Season", "required": False, "options": ["Given", "Due - Advise", "Not Applicable (Outside RSV Season)", "Declined"]},
                    {"id": "anv_flu_confirm", "type": "toggle", "label": "Influenza Vaccine - Recommended During Pregnancy", "required": False},
                    {"id": "anv_gbs_note", "type": "toggle", "label": "Group B Strep: NOT Treated Antenatally - Only Intrapartum IV Benzylpenicillin", "required": False}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or contact maternity unit if: headache, abdominal pain, sudden swelling, reduced foetal movement, proteinuria, or any concerns. Pre-eclampsia red flags: headache + HTN + proteinuria = urgent obstetric referral. Pertussis vaccine: best 16-36 weeks. RSV (Abrysvo): CDC recommends 32-36 weeks during RSV season. Influenza: recommended during pregnancy. Group B Strep: NOT treated antenatally - only intrapartum IV benzylpenicillin. Continue routine antenatal care per protocol. Next visit as per antenatal schedule.",
                "questions": [
                    {"id": "anv_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Patient Well - Pregnancy Progressing Normally", "Minor Concerns - Monitor", "Red Flags Present - ESCALATE / Urgent Obstetric Referral"]},
                    {"id": "anv_next_visit", "type": "text", "label": "Next Routine Visit", "required": True, "placeholder": "e.g., 31 weeks per antenatal schedule"}
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
    seed_antenatal_routine()