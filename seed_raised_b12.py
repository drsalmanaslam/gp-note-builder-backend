from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_b12():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category:
        category = Category(name="Abnormal Labs/Investigations")
        db.add(category)
        db.commit()

    t = {
        "title": "Raised Vitamin B12",
        "description": "Assessment of elevated serum B12 levels. Covers common benign causes, systematic workup for haematological/hepatic/malignant causes, and red flags for urgent referral.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Confirm & Exclude Benign Causes",
                "section_type": "history",
                "questions": [
                    {"id": "b12_level", "type": "text", "label": "B12 Level (pmol/L or ng/L)", "required": True, "placeholder": "e.g., 1200 pmol/L", "output_phrase": "B12: {value}"},
                    {"id": "b12_supplements", "type": "toggle", "label": "Taking B12 Supplements? (oral/IM/multivitamin/energy drinks)", "required": True, "output_phrase": "Supplements: {value}"},
                    {"id": "b12_recent_injection", "type": "toggle", "label": "Recent B12 Injection? (within 3 months)", "required": True, "output_phrase": "Recent injection: {value}"},
                    {"id": "b12_haemolysed", "type": "toggle", "label": "Sample Haemolysed? (can falsely elevate)", "required": False, "output_phrase": "Haemolysed: {value}"}
                ]
            },
            {
                "title": "Systematic Enquiry",
                "section_type": "history",
                "questions": [
                    {"id": "b12_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within recommended limits", "Excess / harmful"], "output_phrase": "Alcohol: {value}"},
                    {"id": "b12_liver_symptoms", "type": "multi_select", "label": "Liver Disease Symptoms", "required": False, "options": ["Jaundice", "Ascites / abdominal distension", "Known liver disease", "None"], "output_phrase": "Liver symptoms: {value}"},
                    {"id": "b12_red_flags", "type": "multi_select", "label": "Red Flag Symptoms (?malignancy)", "required": True, "options": ["Unintentional weight loss", "Night sweats", "Unexplained fatigue", "Abdominal pain / mass", "Early satiety", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss/night sweats/fatigue + raised B12 = ?malignancy (haematological or solid organ). Urgent workup.", "red_flag_negative": "", "output_phrase": "Red flag symptoms: {value}"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "b12_lymph", "type": "toggle", "label": "Lymphadenopathy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy + raised B12 = ?haematological malignancy. Urgent haematology referral.", "red_flag_negative": "", "output_phrase": "Lymphadenopathy: {value}"},
                    {"id": "b12_hepatosplenomegaly", "type": "toggle", "label": "Hepatosplenomegaly?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hepatosplenomegaly + raised B12 = ?myeloproliferative or hepatic malignancy. Urgent referral.", "red_flag_negative": "", "output_phrase": "Hepatosplenomegaly: {value}"},
                    {"id": "b12_jaundice", "type": "toggle", "label": "Jaundice / Stigmata of Chronic Liver Disease?", "required": False, "output_phrase": "Jaundice: {value}"}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "history",
                "questions": [
                    {"id": "b12_fbc", "type": "single_select", "label": "FBC & Blood Film", "required": True, "options": ["Normal", "Leucocytosis / abnormal cells — ?CML/MPN", "Polycythaemia", "Thrombocytosis", "Pending"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal FBC/film + raised B12 = ?myeloproliferative disorder. Urgent haematology referral.", "red_flag_negative": "", "output_phrase": "FBC/Film: {value}"},
                    {"id": "b12_lfts", "type": "single_select", "label": "Liver Function Tests", "required": True, "options": ["Normal", "Mildly deranged", "Significantly deranged — ?hepatic cause", "Pending"], "output_phrase": "LFTs: {value}"},
                    {"id": "b12_renal", "type": "single_select", "label": "Renal Function (U&E/eGFR)", "required": True, "options": ["Normal", "CKD Stage 3 (eGFR 30-59)", "CKD Stage 4-5 (eGFR <30)", "Pending"], "output_phrase": "Renal: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Benign — supplementation (oral/IM B12, multivitamins)",
                    "Recent transfusion",
                    "Liver disease — hepatocellular damage releasing stored B12",
                    "Myeloproliferative disorder — CML, PV, myelofibrosis (raised transcobalamin)",
                    "Chronic kidney disease — reduced clearance",
                    "Solid organ malignancy — liver, colorectal with hepatic metastases",
                    "Haematological malignancy",
                    "Haemolysed sample — artefactual"
                ],
                "questions": [
                    {"id": "b12_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Benign — supplementation / reassure", "Liver-related — investigate LFTs", "?Myeloproliferative — refer haematology", "?Malignancy — 2-week wait referral", "Isolated finding — observe + repeat", "Renal impairment — monitor"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If benign cause confirmed (supplementation, transfusion): Reassure — no treatment needed. Repeat B12 in 3-6 months if trend monitoring desired. If no cause identified + normal FBC, LFTs, U&E + asymptomatic: Isolated raised B12 is usually not clinically significant. Consider repeat in 3 months. If abnormal FBC/film or red flags: Urgent haematology referral (?MPN/CML). If deranged LFTs without clear cause: Investigate liver pathology — ultrasound, hepatitis screen. If red flag symptoms + raised B12 + normal FBC: Consider 2-week wait referral for suspected malignancy (solid organ). Safety-net: Return if develops weight loss, night sweats, abdominal symptoms, or fatigue.",
                "questions": [
                    {"id": "b12_action", "type": "single_select", "label": "Action", "required": True, "options": ["Reassure + discharge (benign cause)", "Repeat B12 in 3-6 months", "Investigate — LFTs, ultrasound, hepatitis screen", "Urgent haematology referral", "2-week wait cancer referral", "Routine haematology referral"], "output_phrase": "Action: {value}"},
                    {"id": "b12_investigations", "type": "text", "label": "Further Investigations Ordered", "required": False, "placeholder": "e.g., Liver ultrasound, hepatitis serology, repeat FBC", "output_phrase": "Investigations: {value}"},
                    {"id": "b12_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if weight loss/night sweats/new symptoms)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "b12_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat B12 + FBC in 3 months. Refer if rising trend or new symptoms.", "output_phrase": "Follow-up: {value}"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    db.close()

if __name__ == "__main__":
    seed_raised_b12()