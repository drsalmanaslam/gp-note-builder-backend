from app.database import SessionLocal
from app.models import User, Template

def seed_iron_deficiency():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin: print("❌ No admin!"); db.close(); return

    title = "Iron Deficiency Anaemia - Management"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing: db.delete(existing); db.commit()

    t = Template(title=title, description="Management of iron deficiency anaemia covering investigation of cause, oral vs IV iron, monitoring response, and red flags for GI malignancy per NICE NG12.", category="Abnormal Labs/Investigations", content={"sections": [
        {"title": "Blood Results", "section_type": "assessment", "questions": [
            {"id": "ida_hb", "type": "number", "label": "Haemoglobin (g/L)", "required": True, "placeholder": "e.g., 98"},
            {"id": "ida_mcv", "type": "number", "label": "MCV (fL)", "required": True, "placeholder": "e.g., 72"},
            {"id": "ida_mch", "type": "number", "label": "MCH (pg)", "required": False, "placeholder": "e.g., 24"},
            {"id": "ida_ferritin", "type": "number", "label": "Ferritin (µg/L)", "required": True, "placeholder": "e.g., 8"},
            {"id": "ida_tsat", "type": "number", "label": "Transferrin Saturation (%)", "required": False, "placeholder": "e.g., 10"},
            {"id": "ida_crp", "type": "number", "label": "CRP (if ferritin normal/high but ?IDA)", "required": False, "placeholder": "e.g., <5"},
            {"id": "ida_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild (Hb 110-130 F / 110-140 M)", "Moderate (Hb 80-109)", "Severe (Hb <80)"]}
        ]},
        {"title": "Symptoms & History", "section_type": "history", "questions": [
            {"id": "ida_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Fatigue", "SOB on exertion", "Palpitations", "Pallor", "Pica (ice/dirt cravings)", "Restless legs", "Hair loss", "None - incidental finding"]},
            {"id": "ida_gi_blood_loss", "type": "toggle", "label": "GI Blood Loss? (Melaena, PR bleeding, change in bowel habit)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: GI blood loss + IDA = urgent 2WW referral for ?colorectal cancer (NICE NG12).", "red_flag_negative": ""},
            {"id": "ida_menorrhagia", "type": "toggle", "label": "Heavy Menstrual Bleeding? (Female)", "required": False},
            {"id": "ida_diet", "type": "single_select", "label": "Diet", "required": True, "options": ["Omnivore - adequate iron", "Vegetarian", "Vegan", "Poor diet / Elderly"]},
            {"id": "ida_ppis", "type": "toggle", "label": "On PPI? (Reduces iron absorption)", "required": False},
            {"id": "ida_coeliac", "type": "toggle", "label": "Known Coeliac / ?Undiagnosed?", "required": False},
            {"id": "ida_previous_ida", "type": "toggle", "label": "Previous Iron Deficiency?", "required": True},
            {"id": "ida_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: IDA + weight loss = urgent 2WW GI referral.", "red_flag_negative": ""}
        ]},
        {"title": "Examination", "section_type": "examination", "questions": [
            {"id": "ida_pallor", "type": "toggle", "label": "Conjunctival Pallor?", "required": False},
            {"id": "ida_koilonychia", "type": "toggle", "label": "Koilonychia (Spoon Nails)?", "required": False},
            {"id": "ida_angular_stomatitis", "type": "toggle", "label": "Angular Stomatitis?", "required": False},
            {"id": "ida_abdo_exam", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Normal", "Mass palpable - RED FLAG", "Tenderness", "Not examined"]},
            {"id": "ida_pr_exam", "type": "toggle", "label": "PR Examination?", "required": False}
        ]},
        {"title": "Investigations", "section_type": "assessment", "questions": [
            {"id": "ida_coeliac_screen", "type": "toggle", "label": "Coeliac Screen (tTG) Requested?", "required": True},
            {"id": "ida_oga", "type": "toggle", "label": "OGD / Colonoscopy Required?", "required": True},
            {"id": "ida_2ww", "type": "toggle", "label": "2-Week Wait Referral? (NICE NG12 criteria)", "required": True},
            {"id": "ida_fit", "type": "toggle", "label": "FIT Test Done? (If not 2WW criteria met)", "required": False}
        ]},
        {"title": "Assessment", "section_type": "assessment", "differentials": ["Iron Deficiency Anaemia - dietary (vegetarian/vegan, elderly)", "Iron Deficiency Anaemia - menorrhagia", "Iron Deficiency Anaemia - GI blood loss (?colorectal cancer - URGENT)", "Iron Deficiency Anaemia - PPI-induced", "Iron Deficiency Anaemia - Coeliac disease", "Iron Deficiency Anaemia - Post-surgical (gastrectomy, bypass)", "Anaemia of Chronic Disease (normal/high ferritin, low iron)"], "questions": [
            {"id": "ida_cause", "type": "single_select", "label": "Likely Cause", "required": True, "options": ["Dietary insufficiency", "Menorrhagia", "GI blood loss - ?malignancy", "GI blood loss - benign (angiodysplasia, gastritis)", "Malabsorption (Coeliac, PPI, post-surgery)", "Multiple factors", "Unknown - investigate"]},
            {"id": "ida_2ww_indicated", "type": "toggle", "label": "2WW Referral Made?", "required": True}
        ]},
        {"title": "Management", "section_type": "plan", "safety_netting": "Iron supplements: Ferrous sulfate 200mg TDS (or ferrous fumarate 210mg TDS if GI upset). Take on empty stomach with vitamin C (orange juice) for absorption. Avoid tea/coffee within 1 hour. Side effects: constipation (common), black stools (normal). Warn patients this is expected. Hb should rise by 20g/L within 4 weeks. Continue iron for 3 months after Hb normalises to replenish stores. IV iron (Ferinject/Monofer) if: oral iron not tolerated, severe anaemia (<80g/L), malabsorption, or rapid correction needed. Return if: melaena, PR bleeding, weight loss, abdominal mass, or no response to iron after 4 weeks.", "questions": [
            {"id": "ida_treatment", "type": "single_select", "label": "Treatment", "required": True, "options": ["Oral iron - Ferrous sulfate 200mg TDS", "Oral iron - Ferrous fumarate 210mg TDS", "IV iron - refer to hospital/community service", "Dietary advice only (mild, adequate stores)", "Treat underlying cause + iron"]},
            {"id": "ida_blood_transfusion", "type": "toggle", "label": "Blood Transfusion Required? (Hb <70 or symptomatic <80)", "required": False},
            {"id": "ida_advice", "type": "toggle", "label": "Iron Supplement Advice Given? (Side effects, absorption tips)", "required": True},
            {"id": "ida_followup", "type": "text", "label": "Follow-up", "required": True, "placeholder": "e.g., Repeat FBC + ferritin in 4 weeks, check compliance, 2WW referral pending"}
        ]}
    ]}, is_public=True, created_by=admin.id)
    db.add(t); db.commit(); print(f"✅ {title}"); db.close()

if __name__ == "__main__": seed_iron_deficiency()