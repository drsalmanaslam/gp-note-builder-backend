from app.database import SessionLocal
from app.models import User, Template

def seed_ovarian_cyst():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Ovarian Cyst"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Assessment and management of ovarian cysts covering simple vs complex cysts, CA125 interpretation, RMI scoring, and referral per RCOG Green-top Guideline.", category="Gynaecology", content={"sections": [
        {"title": "History", "section_type": "history", "questions": [
            {"id": "oc_pain", "type": "toggle", "label": "Pelvic Pain?", "required": True},
            {"id": "oc_pain_acute", "type": "toggle", "label": "Acute Severe Pain? (?Torsion/Rupture)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Acute severe pain = ?ovarian torsion / cyst rupture. Emergency gynaecology referral.", "red_flag_negative": ""},
            {"id": "oc_bloating", "type": "toggle", "label": "Abdominal Bloating / Distension?", "required": True},
            {"id": "oc_early_satiety", "type": "toggle", "label": "Early Satiety / Loss of Appetite?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bloating + early satiety = ?ovarian cancer. Check CA125 + TVUSS urgently.", "red_flag_negative": ""},
            {"id": "oc_weight_loss", "type": "toggle", "label": "Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss = ?malignancy. Urgent 2WW.", "red_flag_negative": ""},
            {"id": "oc_menstrual", "type": "single_select", "label": "Menstrual Pattern", "required": True, "options": ["Regular", "Irregular", "Heavy", "Postmenopausal bleeding"]},
            {"id": "oc_urinary", "type": "toggle", "label": "Urinary Frequency / Urgency? (Pressure effect)", "required": False},
            {"id": "oc_constipation", "type": "toggle", "label": "Constipation / Bowel Changes?", "required": False}
        ]},
        {"title": "Risk Assessment", "section_type": "history", "questions": [
            {"id": "oc_menopausal_status", "type": "single_select", "label": "Menopausal Status", "required": True, "options": ["Premenopausal", "Perimenopausal", "Postmenopausal"]},
            {"id": "oc_age", "type": "number", "label": "Age", "required": True},
            {"id": "oc_family_ovarian", "type": "toggle", "label": "Family History Ovarian/Breast Cancer?", "required": True},
            {"id": "oc_previous_cyst", "type": "toggle", "label": "Previous Ovarian Cyst?", "required": True},
            {"id": "oc_ca125", "type": "number", "label": "CA125 Level (U/mL)", "required": False, "placeholder": "e.g., 22"},
            {"id": "oc_uss_findings", "type": "single_select", "label": "USS Findings", "required": False, "options": ["Simple cyst <5cm - likely physiological", "Simple cyst 5-7cm", "Simple cyst >7cm", "Complex cyst (septations, solid areas)", "Endometrioma", "Dermoid cyst", "Not yet done"]},
            {"id": "oc_uss_size", "type": "text", "label": "Cyst Size (cm)", "required": False, "placeholder": "e.g., 4.5cm"}
        ]},
        {"title": "RMI Score (Risk of Malignancy Index)", "section_type": "assessment", "questions": [
            {"id": "oc_rmi_uss", "type": "single_select", "label": "USS Features (Score 0-3)", "required": False, "options": ["0: Simple cyst", "1: One abnormal feature", "3: ≥2 abnormal features (solid, bilat, ascites, mets)"]},
            {"id": "oc_rmi_menopause", "type": "single_select", "label": "Menopausal Status (Score)", "required": False, "options": ["1: Premenopausal", "3: Postmenopausal"]},
            {"id": "oc_rmi_ca125", "type": "toggle", "label": "CA125 Raised? (>35 U/mL)", "required": False},
            {"id": "oc_rmi_total", "type": "number", "label": "RMI Score (≥200 = 75% risk of malignancy)", "required": False, "placeholder": "e.g., 25"}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Functional / Physiological cyst (follicular, corpus luteum)", "Simple ovarian cyst (<5cm premenopausal = likely benign)", "Endometrioma (chocolate cyst)", "Dermoid cyst (mature cystic teratoma)", "Cystadenoma (serous/mucinous)", "Ovarian malignancy (RED FLAG features)", "Polycystic ovaries (PCOS)", "Para-ovarian cyst"], "questions": [
            {"id": "oc_diagnosis", "type": "single_select", "label": "Likely Diagnosis", "required": True, "options": ["Simple cyst - likely benign/physiological", "Complex cyst - requires follow-up", "Endometrioma", "Suspected malignancy - URGENT", "Dermoid cyst"]},
            {"id": "oc_malignancy_risk", "type": "single_select", "label": "Malignancy Risk (RMI)", "required": True, "options": ["Low risk (RMI <25) - discharge or routine follow-up", "Moderate risk (RMI 25-200) - gynaecology referral", "High risk (RMI >200) - urgent 2WW cancer referral"]}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Return immediately if: sudden severe pelvic pain, vomiting, fainting (torsion), or abdominal distension with breathing difficulty. Simple cysts <5cm in premenopausal women: likely physiological, resolve spontaneously - can discharge. Simple cysts 5-7cm: repeat USS in 2-3 months (follow menstrual cycle). Complex cysts or >7cm: refer gynaecology. Postmenopausal: any cyst >1cm with raised CA125 or RMI >200 = urgent 2WW. CA125 can be falsely raised in endometriosis, fibroids, PID, pregnancy, menstruation. Ovarian torsion: sudden severe unilateral pain, nausea/vomiting - surgical emergency.", "questions": [
            {"id": "oc_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassure + discharge (<5cm simple, premenopausal)", "Repeat USS in 2-3 months (5-7cm simple)", "Routine gynaecology referral", "Urgent 2WW cancer referral (RMI >200)", "Emergency gynaecology (torsion/rupture)", "Start COCP to suppress ovulation"]},
            {"id": "oc_2ww", "type": "toggle", "label": "2WW Referral Made?", "required": False},
            {"id": "oc_ca125_repeat", "type": "toggle", "label": "Repeat CA125 + USS Requested?", "required": False},
            {"id": "oc_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat USS in 3 months, gynaecology referral, 2WW outcome"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_ovarian_cyst()