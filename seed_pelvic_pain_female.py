from app.database import SessionLocal
from app.models import User, Template

def seed_pelvic_pain_female():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Chronic Pelvic Pain (Female)"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of chronic pelvic pain in women covering gynaecological, urological, GI, and musculoskeletal causes, red flags, and multidisciplinary management per RCOG guidelines.", category="Gynaecology", content={"sections": [
        {"title": "Pain Assessment", "section_type": "history", "questions": [
            {"id": "cpp_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 8 months"},
            {"id": "cpp_location", "type": "multi_select", "label": "Pain Location", "required": True, "options": ["Suprapubic", "Right iliac fossa", "Left iliac fossa", "Lower back", "Deep pelvic", "Generalised"]},
            {"id": "cpp_cyclical", "type": "single_select", "label": "Relationship to Menstrual Cycle", "required": True, "options": ["Cyclical (worse during menses) - ?endometriosis", "Non-cyclical - constant", "Intermittent - no pattern", "Related to ovulation (mid-cycle)"]},
            {"id": "cpp_severity", "type": "number", "label": "Pain Score (0-10)", "required": True, "placeholder": "e.g., 7"},
            {"id": "cpp_dyspareunia", "type": "toggle", "label": "Dyspareunia?", "required": True},
            {"id": "cpp_deep_dyspareunia", "type": "toggle", "label": "Deep Dyspareunia? (?Endometriosis/PID)", "required": False},
            {"id": "cpp_bowel", "type": "toggle", "label": "Bowel Symptoms? (Constipation, diarrhoea, bloating)", "required": True},
            {"id": "cpp_bladder", "type": "toggle", "label": "Urinary Symptoms? (Frequency, urgency, dysuria)", "required": True},
            {"id": "cpp_impact", "type": "single_select", "label": "Impact on Daily Life", "required": True, "options": ["Mild", "Moderate - affects work/relationships", "Severe - unable to function"]}
        ]},
        {"title": "Gynaecological History", "section_type": "history", "questions": [
            {"id": "cpp_lmp", "type": "text", "label": "LMP & Cycle", "required": True, "placeholder": "e.g., Regular 28-day, LMP 2 weeks ago"},
            {"id": "cpp_menorrhagia", "type": "toggle", "label": "Heavy Menstrual Bleeding?", "required": True},
            {"id": "cpp_dysmenorrhoea", "type": "toggle", "label": "Severe Period Pain?", "required": True},
            {"id": "cpp_discharge", "type": "toggle", "label": "Abnormal Vaginal Discharge?", "required": True},
            {"id": "cpp_postcoital", "type": "toggle", "label": "Postcoital Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postcoital bleeding = ?cervical cancer. Speculum + swabs + 2WW referral if persistent.", "red_flag_negative": ""},
            {"id": "cpp_contraception", "type": "text", "label": "Current Contraception", "required": False},
            {"id": "cpp_smear", "type": "toggle", "label": "Cervical Screening Up to Date?", "required": True},
            {"id": "cpp_previous_pid", "type": "toggle", "label": "Previous PID / STI?", "required": True},
            {"id": "cpp_previous_surgery", "type": "toggle", "label": "Previous Pelvic/Abdominal Surgery?", "required": True}
        ]},
        {"title": "Red Flags", "section_type": "history", "questions": [
            {"id": "cpp_pregnancy", "type": "toggle", "label": "Possibility of Pregnancy? (?Ectopic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pelvic pain + positive pregnancy test = ?ectopic until proven otherwise. Urgent TVUSS.", "red_flag_negative": ""},
            {"id": "cpp_weight_loss", "type": "toggle", "label": "Weight Loss / Bloating / Early Satiety?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + pelvic pain + bloating = ?ovarian cancer. Urgent CA125 + TVUSS.", "red_flag_negative": ""},
            {"id": "cpp_fever", "type": "toggle", "label": "Fever / Vaginal Discharge? (?PID/TOA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever + pelvic pain + discharge = ?PID/tubo-ovarian abscess. Urgent gynaecology.", "red_flag_negative": ""},
            {"id": "cpp_acute", "type": "toggle", "label": "Sudden Severe Onset? (?Ovarian torsion, cyst rupture)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute severe pelvic pain = ?ovarian torsion, ruptured ectopic, cyst accident. Emergency.", "red_flag_negative": ""},
            {"id": "cpp_pr_bleeding", "type": "toggle", "label": "PR Bleeding / Change in Bowel Habit?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bowel symptoms + pelvic pain = ?colorectal cancer. Urgent colonoscopy.", "red_flag_negative": ""}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "cpp_abdo_tenderness", "type": "single_select", "label": "Abdominal Tenderness", "required": True, "options": ["None", "Suprapubic", "Focal LIF/RIF", "Generalised", "Not examined"]},
            {"id": "cpp_abdo_mass", "type": "toggle", "label": "Palpable Mass?", "required": False},
            {"id": "cpp_speculum", "type": "toggle", "label": "Speculum Examination?", "required": False},
            {"id": "cpp_bimanual", "type": "single_select", "label": "Bimanual Findings", "required": False, "options": ["Normal", "Cervical motion tenderness (PID)", "Adnexal mass/tenderness", "Uterine enlargement (fibroids/adenomyosis)", "Cul-de-sac nodularity (?endometriosis)", "Not examined"]}
        ]},
        {"title": "Investigations", "section_type": "assessment", "questions": [
            {"id": "cpp_preg_test", "type": "toggle", "label": "Pregnancy Test Done?", "required": True},
            {"id": "cpp_sti_screen", "type": "toggle", "label": "STI Screen (Chlamydia/Gonorrhoea)?", "required": False},
            {"id": "cpp_uss", "type": "toggle", "label": "Pelvic USS (Transvaginal)?", "required": False},
            {"id": "cpp_ca125", "type": "toggle", "label": "CA125 Checked? (>35 = urgent 2WW)", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Endometriosis / Adenomyosis", "Pelvic Inflammatory Disease (acute or chronic)", "Irritable Bowel Syndrome", "Interstitial Cystitis / Painful Bladder Syndrome", "Ovarian Cyst / Endometrioma", "Fibroids", "Pelvic Congestion Syndrome", "Adhesions (post-surgical/post-PID)", "Musculoskeletal (pelvic floor myalgia)", "Ovarian Cancer (RED FLAG)"], "questions": [
            {"id": "cpp_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Endometriosis", "PID (acute/chronic)", "IBS", "Ovarian cyst", "Musculoskeletal / Pelvic floor", "Idiopathic chronic pelvic pain", "Suspected malignancy - URGENT"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately if: sudden severe pain, fever >38°C, vomiting, fainting, or heavy vaginal bleeding. Chronic pelvic pain is often multifactorial - consider multidisciplinary approach (gynaecology, pain clinic, physiotherapy, psychology). Trial of NSAIDs, hormonal suppression (COCP/POP/Mirena). Pelvic floor physiotherapy for musculoskeletal component. Refer gynaecology if: diagnostic uncertainty, failed primary care management, USS abnormality, or suspected endometriosis. Pain clinic for chronic pain management. 2WW referral if CA125 >35 or suspicious USS.", "questions": [
            {"id": "cpp_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["Analgesia (NSAID + paracetamol)", "Trial of hormonal suppression", "Pelvic USS (TV)", "STI screen + swabs", "Gynaecology referral", "Pain clinic referral", "Pelvic floor physiotherapy", "2WW referral (if CA125 raised/mass)"]},
            {"id": "cpp_hormonal", "type": "text", "label": "Hormonal Treatment", "required": False, "placeholder": "e.g., Cerelle 75mcg OD, or Mirena IUS"},
            {"id": "cpp_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., USS + CA125 results, gynaecology referral, review 6 weeks"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_pelvic_pain_female()