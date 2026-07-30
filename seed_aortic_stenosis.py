from app.database import SessionLocal
from app.models import User, Template, Category

def seed_aortic_stenosis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Aortic Stenosis",
        "description": "Focused assessment for aortic stenosis covering murmur characteristics, severity indicators, red flags, and echocardiogram referral criteria.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "as_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Incidental systolic murmur found on routine examination"},
                    {"id": "as_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 72"},
                    {"id": "as_how_detected", "type": "single_select", "label": "How Detected", "required": True, "options": ["Incidental finding", "Routine check", "Pre-operative assessment", "Symptom investigation"]},
                    {"id": "as_asymptomatic", "type": "toggle", "label": "Asymptomatic?", "required": True},
                    {"id": "as_pmh_cardiac", "type": "multi_select", "label": "Cardiovascular History", "required": False, "options": ["AF", "IHD / Angina", "Hypertension", "Heart failure", "Previous valve surgery", "Bicuspid aortic valve", "None"]},
                    {"id": "as_family_valve", "type": "toggle", "label": "Family History of Aortic Valve / Aortic Disease?", "required": True}
                ]
            },
            {
                "title": "RED FLAGS - Symptomatic AS",
                "section_type": "history",
                "questions": [
                    {"id": "as_angina", "type": "toggle", "label": "Chest Pain / Angina on Exertion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Exertional angina + AS = SEVERE AS until proven otherwise. Urgent/same-day cardiology. Poor prognosis if symptomatic.", "red_flag_negative": ""},
                    {"id": "as_syncope", "type": "toggle", "label": "Exertional Syncope / Pre-syncope / Blackouts?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Exertional syncope + AS = CRITICAL AS. Same-day emergency cardiology. High risk sudden death.", "red_flag_negative": ""},
                    {"id": "as_sob_exertion", "type": "toggle", "label": "SOB on Exertion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Exertional SOB + AS = ?severe AS with LV dysfunction. Urgent echo + cardiology.", "red_flag_negative": ""},
                    {"id": "as_sob_rest", "type": "toggle", "label": "SOB at Rest?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB at rest = ?heart failure from severe AS. Urgent admission.", "red_flag_negative": ""},
                    {"id": "as_orthopnoea_pnd", "type": "toggle", "label": "Orthopnoea / PND?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Orthopnoea/PND = heart failure. Urgent echo + cardiology.", "red_flag_negative": ""},
                    {"id": "as_pedal_oedema", "type": "toggle", "label": "Pedal Oedema?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Oedema = ?right heart failure from severe AS. Urgent cardiology.", "red_flag_negative": ""},
                    {"id": "as_exercise_tolerance", "type": "single_select", "label": "Exercise Tolerance (if asymptomatic)", "required": True, "options": ["Normal - no limitation", "Mildly reduced (masked)", "Significantly reduced - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced exercise tolerance may indicate masked severe AS. Urgent echo.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "as_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 120/80"},
                    {"id": "as_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 70"},
                    {"id": "as_murmur_type", "type": "single_select", "label": "Murmur Type", "required": True, "options": ["Ejection Systolic Murmur (ESM)", "Pansystolic (MR/TR)", "Early diastolic (AR)", "Mid-diastolic (MS)", "Continuous"]},
                    {"id": "as_murmur_location", "type": "single_select", "label": "Loudest Location", "required": True, "options": ["Aortic area (R 2nd ICS)", "Pulmonary area (L 2nd ICS)", "Mitral area (Apex)", "Tricuspid area (L sternal edge)"]},
                    {"id": "as_s2", "type": "single_select", "label": "Second Heart Sound (S2 / A2)", "required": True, "options": ["Normal - preserved S2", "Soft/absent A2 - RED FLAG (severe AS)", "Paradoxical splitting - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Soft/absent A2 or paradoxical splitting = SEVERE AS. Urgent echo.", "red_flag_negative": ""},
                    {"id": "as_carotid", "type": "single_select", "label": "Carotid Pulse Character", "required": True, "options": ["Normal volume + upstroke", "Slow-rising (pulsus parvus et tardus) - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Slow-rising carotid = severe AS. Urgent echo.", "red_flag_negative": ""},
                    {"id": "as_radiation", "type": "toggle", "label": "Murmur Radiates to Carotids?", "required": False},
                    {"id": "as_lv_heave", "type": "toggle", "label": "LV Heave? (Sustained apex - LVH)", "required": False},
                    {"id": "as_thrill", "type": "toggle", "label": "Thrill Palpable?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Thrill = severe AS (gradient >40mmHg). Urgent echo.", "red_flag_negative": ""},
                    {"id": "as_oedema", "type": "toggle", "label": "Pedal Oedema?", "required": True}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Aortic Stenosis (degenerative calcific - most common in elderly)",
                    "Bicuspid Aortic Valve (younger patients, early AS)",
                    "Aortic Sclerosis (benign, no haemodynamic significance)",
                    "Hypertrophic Cardiomyopathy (HOCM - ESM, carotid upstroke normal/brisk)",
                    "Mitral Regurgitation (pansystolic at apex radiating to axilla)",
                    "Ventricular Septal Defect (pansystolic at L sternal edge)",
                    "Pulmonary Stenosis (ESM at L 2nd ICS)"
                ],
                "questions": [
                    {"id": "as_ecg", "type": "single_select", "label": "ECG Findings", "required": True, "options": ["Normal sinus rhythm, no LVH", "LVH voltage criteria", "ST-T changes (strain pattern) - RED FLAG", "AF", "LBBB", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: LVH with strain pattern = significant AS. Urgent echo.", "red_flag_negative": ""},
                    {"id": "as_cxr", "type": "toggle", "label": "Chest X-Ray? (Cardiomegaly, calcified valve, pulmonary oedema)", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "REPORT IMMEDIATELY or attend Emergency Department if: chest tightness/angina on exertion, shortness of breath (especially on exertion or lying flat), dizziness or syncope/blackouts on exertion. These are RED FLAGS for severe/symptomatic AS which carries high mortality without intervention. Mild AS: surveillance echo every 3-5 years. Moderate AS: echo every 1-2 years. Severe asymptomatic AS: echo every 6-12 months + prompt cardiology review. If symptomatic severe AS develops: urgent valve intervention (TAVI or SAVR). TAVI now widely used alongside SAVR depending on age, surgical risk, and anatomy. Endocarditis prophylaxis: good dental hygiene, no routine antibiotic prophylaxis needed.",
                "questions": [
                    {"id": "as_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Routine cardiology referral for TTE", "Urgent/same-day cardiology (symptomatic/red flags)", "Surveillance echo in 3-5 years (mild)", "Surveillance echo in 1-2 years (moderate)", "No referral (aortic sclerosis only)"]},
                    {"id": "as_symptom_warning", "type": "toggle", "label": "Symptom RED FLAG Warning Given? (Angina, syncope, SOB = urgent)", "required": True},
                    {"id": "as_endocarditis", "type": "toggle", "label": "Dental Hygiene / Endocarditis Advice?", "required": False},
                    {"id": "as_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await TTE, review with result. If mild: repeat echo 3-5 years"}
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
    seed_aortic_stenosis()