from app.database import SessionLocal
from app.models import User, Template, Category

def seed_lung_cancer():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Respiratory").first()
    if not category: category = Category(name="Respiratory"); db.add(category); db.commit()

    t = {
        "title": "Suspected Lung Cancer - NCCP Rapid Access Service GP Referral Guideline",
        "description": "National NCCP guideline-based lung cancer referral pathway covering urgent CXR criteria, Rapid Access Service triggers, emergency symptoms, and expected service timelines.",
        "category": "Respiratory",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "lc_symptoms", "type": "multi_select", "label": "Presenting Symptoms (>90% Symptomatic at Presentation, >1/3 Have Distant Metastases)", "required": True, "options": ["Haemoptysis", "New onset unexplained or persistent cough (>3 weeks)", "Alteration in character/severity of chronic cough", "Unexplained chest pain", "Unexplained dyspnoea", "Unexplained weight loss / cachexia", "Unexplained bone pain", "Unexplained neurological symptoms", "None of the above"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any of these symptoms = urgent CXR indicated. Haemoptysis + weight loss = high suspicion.", "red_flag_negative": ""},
                    {"id": "lc_emergency", "type": "multi_select", "label": "Emergency / Life-Threatening Symptoms (DO NOT Route via Rapid Access)", "required": True, "options": ["Stridor", "SVC Obstruction (facial swelling, distended neck veins)", "Respiratory distress", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Stridor/SVC obstruction/respiratory distress = EMERGENCY. Do NOT use Rapid Access - refer directly to ED.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Risk Factors (NCRI)",
                "section_type": "history",
                "questions": [
                    {"id": "lc_risk_factors", "type": "multi_select", "label": "Risk Factors (>90% Attributable to Smoking. ~1,800 Cases/Year in Ireland: ~1,100 Male, ~700 Female. Incidence ↓ Male, ↑ Female. <1% Before Age 40)", "required": True, "options": ["Smoking (including passive smoking)", "Marijuana smoking", "Radon exposure", "Heavy metal exposure (e.g., arsenic)", "Radiation exposure", "Asbestos dust exposure", "Previous history of cancer (e.g., head & neck cancer)", "None identified"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lung cancer CAN occur without risk factors. Suspicious symptoms = investigate regardless.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination Signs",
                "section_type": "examination",
                "questions": [
                    {"id": "lc_signs", "type": "multi_select", "label": "Clinical Signs", "required": True, "options": ["Clubbing", "Lymphadenopathy (cervical/supraclavicular)", "Focal chest signs (reduced AE, dullness)", "Hepatomegaly", "None present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any of these signs + symptoms = high suspicion. Urgent CXR + consider direct Rapid Access referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "lc_cxr", "type": "single_select", "label": "Urgent CXR (Indicated for Any Symptoms/Signs Above. Report Within 1 Week)", "required": True, "options": ["Requested - urgent CXR", "Not requested - direct Rapid Access referral (high suspicion)", "Not indicated - no concerning symptoms/signs"]},
                    {"id": "lc_cxr_result", "type": "single_select", "label": "CXR Result", "required": False, "options": ["Normal", "Suspicious for lung cancer - RED FLAG", "Awaiting result"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspicious CXR = refer Rapid Access Service immediately.", "red_flag_negative": ""},
                    {"id": "lc_ct", "type": "single_select", "label": "CT Scan (Do NOT Delay Referral for Outpatient CT - Rapid Access Arranges Directly)", "required": False, "options": ["Not ordered - refer directly to Rapid Access Service", "Ordered (deviation from standard pathway)", "Not indicated"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT delay referral by ordering outpatient CT. Rapid Access Service arranges CT + bronchoscopy directly.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Referral Pathway",
                "section_type": "assessment",
                "differentials": [
                    "Lung Cancer (NSCLC / SCLC)",
                    "Metastatic Disease to Lung",
                    "Carcinoid Tumour",
                    "Lymphoma",
                    "TB",
                    "Pneumonia",
                    "COPD Exacerbation"
                ],
                "questions": [
                    {"id": "lc_referral_trigger", "type": "single_select", "label": "Referral Trigger", "required": True, "options": ["CXR suspicious for lung cancer → Refer to Rapid Access Service", "CXR normal, but haemoptysis or concerning/persistent symptoms → Refer to Rapid Access", "CXR normal, no concerning symptoms → No referral required", "Emergency symptoms (stridor/SVC/resp distress) → EMERGENCY referral"]},
                    {"id": "lc_referral_method", "type": "single_select", "label": "Referral Method", "required": False, "options": ["Electronic referral - Healthlink (www.healthlink.ie)", "National Lung Cancer Rapid Access Service Referral Form (postal)", "Emergency Department referral", "Not applicable"]},
                    {"id": "lc_film_details", "type": "toggle", "label": "If CXR at Different Hospital: Copy of Result Sent to Receiving Clinic + Film Copy for Patient?", "required": False},
                    {"id": "lc_patient_informed", "type": "toggle", "label": "Patient Informed of Referral by GP?", "required": True}
                ]
            },
            {
                "title": "Impression & Timeline",
                "section_type": "plan",
                "safety_netting": "Expected service timeline: patients should be assessed by respiratory physician within 2 weeks of receipt of request. Rapid Access Services typically complete initial investigations (CT, bronchoscopy) within one or two hospital visits. >90% of lung cancer patients are symptomatic at presentation. >1/3 have distant metastases at diagnosis. ~1,800 new cases annually in Ireland. Lung cancer CAN occur without risk factors. If CXR normal but haemoptysis or concerning symptoms persist: STILL refer to Rapid Access Service. If CXR at different hospital: send copy to receiving clinic + give film copy to patient. NCCP contact: (01) 8287100 or www.cancercontrol.hse.ie.",
                "questions": [
                    {"id": "lc_impression", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Suspected Lung Cancer - urgent CXR indicated", "High Likelihood of Lung Cancer - direct Rapid Access referral", "Emergency Presentation (stridor/SVC/resp distress) - EMERGENCY", "Symptoms not currently meeting referral threshold"]},
                    {"id": "lc_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Referral sent - awaiting Rapid Access appointment, CXR normal safety-net, or emergency referral made"}
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
    seed_lung_cancer()