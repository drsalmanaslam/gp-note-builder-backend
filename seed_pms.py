from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_pms():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Premenstrual Syndrome (PMS) - Diagnosis & Management",
        "description": "PMS consultation covering diagnostic criteria (luteal-phase, ≥3 cycles), symptom diary, lifestyle/supplement management, COCP for moderate PMS, and SSRI for severe PMS.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Diagnostic Criteria",
                "section_type": "history",
                "questions": [
                    {"id": "pms_luteal_onset", "type": "toggle", "label": "Symptoms Occur in Luteal Phase (After Ovulation, Before Menses) + Resolve Soon After Period Onset?", "required": True},
                    {"id": "pms_cycles_affected", "type": "number", "label": "Number of Consecutive Cycles Affected (Must Be ≥3 for Diagnosis)", "required": True, "placeholder": "e.g., 4"},
                    {"id": "pms_symptom_diary", "type": "toggle", "label": "Symptom Diary Recommended Before Starting Treatment? (Confirms Cyclical Pattern)", "required": True}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "pms_symptoms", "type": "multi_select", "label": "Symptom Screen (Luteal-Phase Onset, Resolves with Menses)", "required": True, "options": ["Bloating", "Headaches", "Sleep Disturbance", "Breast Pain / Tenderness", "Irritability", "Mood Swings", "Reduced Libido", "Fatigue"]},
                    {"id": "pms_timing", "type": "toggle", "label": "Confirm Luteal-Phase Onset + Resolution with Menses?", "required": True},
                    {"id": "pms_impact", "type": "single_select", "label": "Impact on Quality of Life", "required": True, "options": ["Mild - Coping Well", "Moderate - Affecting Daily Life", "Severe - Significant Distress"]},
                    {"id": "pms_gp", "type": "text", "label": "Gravida / Para", "required": False, "placeholder": "e.g., G1P1"},
                    {"id": "pms_cycle", "type": "single_select", "label": "Cycle Regularity", "required": True, "options": ["Regular", "Irregular"]},
                    {"id": "pms_smear", "type": "toggle", "label": "Cervical Screening Up to Date?", "required": False},
                    {"id": "pms_contraception", "type": "single_select", "label": "Current Contraception", "required": True, "options": ["None", "COCP", "POP", "Implant", "IUS/IUD", "Depo-Provera", "Barrier"]},
                    {"id": "pms_oestrogen", "type": "toggle", "label": "Current Oestrogen Use?", "required": False},
                    {"id": "pms_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Non-Smoker", "Current Smoker"]},
                    {"id": "pms_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within Limits", "Excess"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "pms_abdo", "type": "single_select", "label": "Abdominal Examination", "required": False, "options": ["Soft, Non-Tender, No Organomegaly", "Abnormal"]},
                    {"id": "pms_lymph", "type": "single_select", "label": "Lymph Nodes (Cervical, Supraclavicular, Infraclavicular, Axillary)", "required": False, "options": ["Normal", "Abnormal"]},
                    {"id": "pms_breast", "type": "single_select", "label": "Breast Examination (Only if Prominent Breast Pain)", "required": False, "options": ["Normal", "Abnormal - Refer", "Not Performed"]}
                ]
            },
            {
                "title": "Patient Education",
                "section_type": "plan",
                "questions": [
                    {"id": "pms_edu_prevalence", "type": "toggle", "label": "Affects ~1 in 20 Women Explained?", "required": False},
                    {"id": "pms_edu_diary", "type": "toggle", "label": "Symptom + Menstrual Diary Recommended Before Treatment?", "required": False},
                    {"id": "pms_edu_resources", "type": "multi_select", "label": "Patient Resources Given", "required": False, "options": ["RCOG PMS Leaflet", "www.pms.org.uk"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if symptoms not improving with treatment, or if symptoms worsen. PMS: symptoms occur in luteal phase, resolve with menses, ≥3 consecutive cycles. Affects ~1 in 20 women. Symptom diary recommended before treatment. Lifestyle: small regular meals, increase milk/yoghurt, decrease caffeine/salt/sugar, increase fibre, smoking cessation, relaxation, decrease alcohol, regular sleep. Supplements: Vitamin B6, Calcium, Vitamin D, Magnesium, Vitamin A from day 14 until menses. Evening Primrose Oil 1000mg BD for breast tenderness (2-3 months trial, avoid if epilepsy or TTC). Naproxen 500mg BD PRN for pain. Moderate PMS: Yasmin (COCP) continuously 6 months with 4-day break (unlicensed). Severe PMS: Citalopram/Escitalopram 10mg (daily or luteal-phase only) + CBT for 3 months. Refer gynaecology if not improving. Breast pain leaflet: beaumont.ie/media/Breastpain1.pdf",
                "questions": [
                    {"id": "pms_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["PMS - Mild (Lifestyle + Supplements)", "PMS - Moderate (COCP Indicated)", "PMS - Severe (SSRI + CBT Indicated)", "Not PMS - Pattern Not Consistent"]},
                    {"id": "pms_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Small Regular Meal Portions", "Increase Milk + Yoghurt", "Decrease Caffeine/Salt/Sugar", "Increase Fibre", "Smoking Cessation", "Relaxation Techniques", "Decrease Alcohol", "Regular Sleep"]},
                    {"id": "pms_supplements", "type": "multi_select", "label": "Supplements (Day 14 Until Menses)", "required": False, "options": ["Vitamin B6", "Calcium", "Vitamin D", "Magnesium", "Vitamin A"]},
                    {"id": "pms_evening_primrose", "type": "toggle", "label": "Evening Primrose Oil 1000mg BD? (Breast Tenderness - 2-3 Month Trial. Avoid if Epilepsy/TTC)", "required": False},
                    {"id": "pms_naproxen", "type": "toggle", "label": "Naproxen 500mg BD PRN for Pain?", "required": False},
                    {"id": "pms_cocp", "type": "toggle", "label": "Yasmin (COCP) Continuous 6 Months + 4-Day Break? (Moderate PMS - Unlicensed)", "required": False},
                    {"id": "pms_ssri", "type": "single_select", "label": "SSRI for Severe PMS (Daily or Luteal-Phase Only + CBT x3 Months)", "required": False, "options": ["Citalopram 10mg", "Escitalopram 10mg", "Not Indicated"]},
                    {"id": "pms_referral", "type": "toggle", "label": "Refer Gynaecology? (If Not Improving)", "required": False},
                    {"id": "pms_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3 months review with symptom diary, sooner if concerns"}
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
    seed_pms()