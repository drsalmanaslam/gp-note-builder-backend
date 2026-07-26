from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hyperkalaemia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Hyperkalaemia Assessment",
        "description": "Emergency-focused hyperkalaemia assessment covering severity stratification, ECG interpretation, pseudohyperkalaemia exclusion, and urgent management pathways.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "Severity Stratification & Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hyperk_k", "type": "number", "label": "Current K+ (mmol/L) - NR: 3.5-5.3", "required": True, "placeholder": "e.g., 6.2", "is_red_flag": True, "red_flag_positive": "RED FLAG: K+ ≥6.5 = SEVERE - URGENT A&E via ambulance. K+ ≥6.0 = MODERATE - urgent ECG. K+ 5.5-5.9 = MILD.", "red_flag_negative": ""},
                    {"id": "hyperk_severity", "type": "single_select", "label": "Severity Category", "required": True, "options": ["Mild: 5.5-5.9 mmol/L", "Moderate: 6.0-6.4 mmol/L (Urgent ECG)", "Severe: ≥6.5 mmol/L (EMERGENCY - URGENT A&E)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: K+ ≥6.5 = EMERGENCY. URGENT A&E via ambulance for Calcium Gluconate/Insulin-Dextrose.", "red_flag_negative": ""},
                    {"id": "hyperk_na", "type": "single_select", "label": "Sodium (Hyponatraemia Exacerbates Cardiac Toxicity)", "required": False, "options": ["Normal", "Hyponatraemia - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Hyponatraemia + hyperkalaemia = increased cardiac toxicity risk.", "red_flag_negative": ""},
                    {"id": "hyperk_ca", "type": "single_select", "label": "Calcium (Hypocalcaemia Exacerbates Cardiac Toxicity)", "required": False, "options": ["Normal", "Hypocalcaemia - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Hypocalcaemia + hyperkalaemia = increased cardiac toxicity risk.", "red_flag_negative": ""},
                    {"id": "hyperk_symptoms", "type": "multi_select", "label": "Symptom Screen", "required": True, "options": ["Asymptomatic", "Muscle weakness / cramps", "Palpitations", "Paraesthesias", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Symptomatic hyperkalaemia = urgent ECG + consider admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Medication & Risk Factor Screen",
                "section_type": "history",
                "questions": [
                    {"id": "hyperk_meds", "type": "multi_select", "label": "Causative Medications", "required": True, "options": ["ACE Inhibitor (Ramipril/Lisinopril)", "ARB (Losartan/Candesartan)", "Spironolactone / Eplerenone", "Amiloride", "NSAIDs", "Trimethoprim", "Potassium Supplements", "Salt Substitutes (High K+)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Multiple K+-raising drugs = withhold ACEi/ARB/Spironolactone/NSAIDs. Repeat K+ urgently.", "red_flag_negative": ""},
                    {"id": "hyperk_ckd", "type": "toggle", "label": "Known CKD?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: CKD + hyperkalaemia = high risk. Urgent ECG + nephrology consideration.", "red_flag_negative": ""},
                    {"id": "hyperk_diabetes", "type": "toggle", "label": "Diabetes? (Type 4 RTA Risk)", "required": True},
                    {"id": "hyperk_dehydration", "type": "toggle", "label": "Dehydration / Vomiting / Diarrhoea?", "required": False},
                    {"id": "hyperk_crush_exercise", "type": "toggle", "label": "Recent Crush Injury / Strenuous Exercise?", "required": False}
                ]
            },
            {
                "title": "Pseudohyperkalaemia Screen",
                "section_type": "history",
                "questions": [
                    {"id": "hyperk_difficult_draw", "type": "toggle", "label": "Difficult Draw / Prolonged Tourniquet?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ?Pseudohyperkalaemia from haemolysis/delayed transport. Repeat sample with direct lab transport.", "red_flag_negative": ""},
                    {"id": "hyperk_delayed_transport", "type": "toggle", "label": "Delayed Transport to Lab? (Haemolysis Risk)", "required": True},
                    {"id": "hyperk_pseudohyperkalaemia", "type": "toggle", "label": "Likely Pseudohyperkalaemia? (Repeat with Direct Transport to Lab)", "required": True}
                ]
            },
            {
                "title": "Examination & ECG",
                "section_type": "examination",
                "questions": [
                    {"id": "hyperk_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": False, "placeholder": "e.g., 118/72"},
                    {"id": "hyperk_hr", "type": "number", "label": "Heart Rate (bpm) + Rhythm", "required": False, "placeholder": "e.g., 68 Regular"},
                    {"id": "hyperk_spo2", "type": "number", "label": "SpO2 (%)", "required": False, "placeholder": "e.g., 98"},
                    {"id": "hyperk_fluid_status", "type": "single_select", "label": "Fluid Status", "required": False, "options": ["Euvolaemic", "Dehydrated", "Overloaded"]},
                    {"id": "hyperk_ecg_done", "type": "single_select", "label": "Urgent 12-Lead ECG (Indicated if K+ ≥6.0 or Symptomatic)", "required": True, "options": ["Performed", "Not Indicated (K+ <6.0 + Asymptomatic)"]},
                    {"id": "hyperk_ecg_peaked_t", "type": "toggle", "label": "Tall/Tented T Waves? (>R Wave in >1 Lead)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Peaked T waves = hyperkalaemic ECG changes. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "hyperk_ecg_flat_p", "type": "toggle", "label": "Flattened / Absent P Waves?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent P waves = severe hyperkalaemia. URGENT A&E via ambulance.", "red_flag_negative": ""},
                    {"id": "hyperk_ecg_pr", "type": "toggle", "label": "PR Prolongation?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: PR prolongation = progressive cardiac toxicity. URGENT A&E.", "red_flag_negative": ""},
                    {"id": "hyperk_ecg_qrs", "type": "toggle", "label": "QRS Widening? (Sine Wave Pattern Imminent)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Wide QRS = pre-arrest rhythm. EMERGENCY 999. Calcium Gluconate STAT.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Pseudohyperkalaemia (Haemolysis, Delayed Transport, Difficult Draw)",
                    "Drug-Induced (ACEi/ARB/Spironolactone/NSAIDs/Trimethoprim)",
                    "CKD-Related (Most Common True Cause)",
                    "Acute Kidney Injury (AKI)",
                    "Type 4 Renal Tubular Acidosis (Diabetes, Hypoaldosteronism)",
                    "Addison's Disease (Hypoaldosteronism - Hyponatraemia + Hyperkalaemia)",
                    "Rhabdomyolysis / Crush Injury",
                    "Excess K+ Intake (Supplements, Salt Substitutes)"
                ],
                "questions": [
                    {"id": "hyperk_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Mild Hyperkalaemia (5.5-5.9) - Primary Care Management", "Moderate Hyperkalaemia (6.0-6.4) - Urgent ECG + Repeat K+", "Severe Hyperkalaemia (≥6.5) - URGENT A&E", "Pseudohyperkalaemia - Repeat Sample", "Drug-Induced - Withhold Medications"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "EMERGENCY - attend A&E via ambulance immediately if: severe muscle weakness, chest pain, shortness of breath, or palpitations. If ECG changes present OR K+ ≥6.5: URGENT same-day admission to ED via ambulance for acute stabilization (Calcium gluconate/insulin-dextrose). If asymptomatic + ECG normal: urgent repeat sample with direct patient/courier transport to lab to ensure minimal processing delay and prevent haemolysis. Withhold ACEi/ARB/Spironolactone/NSAIDs pending repeat. Dietary advice: low-potassium diet pending repeat results. Hyponatraemia and hypocalcaemia exacerbate cardiac toxicity - note if present. Patient verbalised understanding and agreed to repeat blood draw instructions.",
                "questions": [
                    {"id": "hyperk_ecg_red_flag_action", "type": "single_select", "label": "Action if ECG Changes or K+ ≥6.5", "required": True, "options": ["URGENT Same-Day A&E via Ambulance (Calcium Gluconate/Insulin-Dextrose)", "Not Indicated (K+ <6.0 + Normal ECG + Asymptomatic)"]},
                    {"id": "hyperk_repeat_sample", "type": "toggle", "label": "Urgent Repeat K+ Arranged? (Direct Patient/Courier Transport to Lab - Avoid Haemolysis)", "required": False},
                    {"id": "hyperk_meds_held", "type": "multi_select", "label": "Medications Withheld Pending Repeat", "required": False, "options": ["ACEi / ARB", "Spironolactone / Eplerenone", "NSAIDs", "Trimethoprim", "K+ Supplements", "Not applicable"]},
                    {"id": "hyperk_diet", "type": "toggle", "label": "Low-Potassium Diet Advised Pending Repeat?", "required": False},
                    {"id": "hyperk_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Mild / Pseudohyperkalaemia)", "A&E (Severe / ECG Changes / Symptomatic)", "Nephrology (Recurrent / CKD-Related)"]},
                    {"id": "hyperk_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Await repeat K+ result, continue withheld meds if normalized, A&E if ≥6.5"}
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
    seed_hyperkalaemia()