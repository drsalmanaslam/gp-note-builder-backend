from app.database import SessionLocal
from app.models import User, Template

def seed_endometriosis():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Endometriosis"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment of suspected endometriosis covering cyclical pain, dyspareunia, fertility impact, examination findings, and referral per NICE NG73 and BSGE guidelines.", category="Gynaecology", content={"sections": [
        {"title": "Pain History", "section_type": "history", "questions": [
            {"id": "endo_pain_cyclical", "type": "toggle", "label": "Cyclical Pain? (Worse around menstruation)", "required": True},
            {"id": "endo_pain_type", "type": "multi_select", "label": "Pain Type", "required": True, "options": ["Dysmenorrhoea (period pain)", "Chronic pelvic pain", "Dyspareunia (deep, not superficial)", "Dyschezia (painful bowel movements - cyclical)", "Dysuria (painful urination - cyclical)", "Lower back pain"]},
            {"id": "endo_pain_severity", "type": "number", "label": "Pain Score (0-10)", "required": True, "placeholder": "e.g., 8"},
            {"id": "endo_pain_impact", "type": "single_select", "label": "Impact on Life", "required": True, "options": ["None", "Misses 1-2 days work/school per month", "Misses 3-5 days per month", "Severe - bedbound during menses, unable to work"]},
            {"id": "endo_pain_duration", "type": "text", "label": "Duration of Symptoms (years)", "required": True, "placeholder": "e.g., 5 years"},
            {"id": "endo_analgesia_required", "type": "single_select", "label": "Analgesia Required", "required": True, "options": ["Paracetamol/NSAID only", "Codeine/Tramadol", "Strong opioids", "A&E visits for pain"]}
        ]},
        {"title": "Associated Symptoms", "section_type": "history", "questions": [
            {"id": "endo_menstrual", "type": "single_select", "label": "Menstrual Pattern", "required": True, "options": ["Regular cycles", "Heavy menstrual bleeding", "Irregular", "Amenorrhoea"]},
            {"id": "endo_bowel", "type": "toggle", "label": "Bowel Symptoms? (Constipation, diarrhoea, bloating - cyclical)", "required": True},
            {"id": "endo_bladder", "type": "toggle", "label": "Bladder Symptoms? (Frequency, urgency, haematuria - cyclical)", "required": True},
            {"id": "endo_fatigue", "type": "toggle", "label": "Chronic Fatigue?", "required": True},
            {"id": "endo_nausea", "type": "toggle", "label": "Nausea / Bloating?", "required": False},
            {"id": "endo_fertility", "type": "toggle", "label": "Trying to Conceive? (Subfertility affects 30-50%)", "required": True}
        ]},
        {"title": "Risk Factors & History", "section_type": "history", "questions": [
            {"id": "endo_age_menarche", "type": "text", "label": "Age at Menarche", "required": False, "placeholder": "e.g., 11"},
            {"id": "endo_family_history", "type": "toggle", "label": "Family History of Endometriosis?", "required": True},
            {"id": "endo_nulliparous", "type": "toggle", "label": "Nulliparous? (Never given birth)", "required": True},
            {"id": "endo_previous_diagnosis", "type": "toggle", "label": "Previous Diagnosis of Endometriosis?", "required": True},
            {"id": "endo_previous_laparoscopy", "type": "toggle", "label": "Previous Laparoscopy?", "required": False},
            {"id": "endo_previous_treatment", "type": "multi_select", "label": "Previous Treatments", "required": False, "options": ["COCP", "POP", "Mirena IUS", "GnRH agonists", "Pain clinic", "Laparoscopic surgery", "None"]}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "endo_abdo_tenderness", "type": "single_select", "label": "Abdominal Tenderness", "required": False, "options": ["None", "Suprapubic", "Lower quadrant", "Generalised", "Not examined"]},
            {"id": "endo_pelvic_mass", "type": "toggle", "label": "Adnexal Mass? (?Endometrioma)", "required": False},
            {"id": "endo_cul_de_sac", "type": "toggle", "label": "Tender Nodules / Cul-de-sac Thickening? (Examination)", "required": False},
            {"id": "endo_uss", "type": "toggle", "label": "Pelvic USS Done?", "required": False},
            {"id": "endo_uss_findings", "type": "single_select", "label": "USS Findings", "required": False, "options": ["Normal", "Endometrioma (chocolate cyst)", "Adenomyosis", "Deep endometriosis suggested", "Not done"]}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Endometriosis", "Adenomyosis", "Primary Dysmenorrhoea", "Pelvic Inflammatory Disease", "Irritable Bowel Syndrome", "Interstitial Cystitis / Painful Bladder Syndrome", "Ovarian Cyst", "Pelvic Congestion Syndrome", "Musculoskeletal Pain"], "questions": [
            {"id": "endo_diagnosis", "type": "single_select", "label": "Suspected Diagnosis", "required": True, "options": ["High suspicion endometriosis - refer gynaecology", "Possible endometriosis - trial treatment + USS", "Adenomyosis", "Primary dysmenorrhoea", "Other pelvic pathology"]},
            {"id": "endo_referral", "type": "single_select", "label": "Referral Pathway", "required": True, "options": ["Routine gynaecology referral", "Urgent gynaecology (suspected malignancy)", "BSGE endometriosis centre (severe/deep)", "Manage in primary care", "Fertility referral"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Endometriosis diagnosis is confirmed by laparoscopy - USS may be normal. Treatment options: 1) Analgesia (NSAIDs, paracetamol), 2) Hormonal (COCP, POP, Mirena IUS, GnRH agonists), 3) Surgery (laparoscopic excision/ablation). Mirena IUS is effective first-line. COCP can be taken continuously (no break) to suppress menstruation. Refer to gynaecology if: suspected endometriosis not responding to 3-6 months hormonal treatment, USS suggests endometrioma >4cm, fertility concerns, or severe symptoms affecting quality of life. BSGE centres for severe/deep endometriosis. Return if: severe acute pain, fever, or new mass.", "questions": [
            {"id": "endo_plan", "type": "multi_select", "label": "Management", "required": True, "options": ["NSAID (Mefenamic acid / Naproxen)", "Trial of hormonal treatment (COCP/POP/Mirena)", "Pelvic USS requested", "Routine gynaecology referral", "BSGE centre referral (severe)", "Fertility referral", "Pain clinic referral", "Sick note if needed"]},
            {"id": "endo_hormonal", "type": "text", "label": "Hormonal Treatment", "required": False, "placeholder": "e.g., Cerazette 75mcg OD, or Mirena IUS insertion"},
            {"id": "endo_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Review in 3 months, USS result, gynaecology referral progress"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_endometriosis()