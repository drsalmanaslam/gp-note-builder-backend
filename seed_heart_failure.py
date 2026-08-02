from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_heart_failure():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Heart Failure",
        "description": "Comprehensive heart failure consultation covering NYHA class, haemodynamic profile, GDMT 4 pillars, and monitoring protocols.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hf_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Progressive SOB on exertion, orthopnoea, ankle swelling"},
                    {"id": "hf_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 72"},
                    {"id": "hf_nyha", "type": "single_select", "label": "NYHA Class", "required": True, "options": ["Class I - No limitation", "Class II - Mild limitation (ordinary activity causes SOB)", "Class III - Marked limitation (less than ordinary activity)", "Class IV - Symptoms at rest"], "is_red_flag": True, "red_flag_positive": "RED FLAG: NYHA III-IV = significant heart failure. Optimise GDMT urgently. NYHA IV = ?hospital admission.", "red_flag_negative": ""},
                    {"id": "hf_orthopnoea", "type": "toggle", "label": "Orthopnoea? (SOB lying flat)", "required": True},
                    {"id": "hf_pillows", "type": "number", "label": "Number of Pillows to Sleep", "required": False, "placeholder": "e.g., 3"},
                    {"id": "hf_pnd", "type": "toggle", "label": "Paroxysmal Nocturnal Dyspnoea? (Waking gasping)", "required": True},
                    {"id": "hf_oedema", "type": "toggle", "label": "Peripheral / Ankle Oedema? (Bilateral)", "required": True},
                    {"id": "hf_fatigue", "type": "toggle", "label": "Fatigue / Reduced Exercise Tolerance?", "required": True},
                    {"id": "hf_palpitations", "type": "toggle", "label": "Palpitations?", "required": False},
                    {"id": "hf_chest_pain", "type": "toggle", "label": "Chest Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain + HF = ?ACS. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "hf_cough_wheeze", "type": "toggle", "label": "Cough / Sputum / Wheeze?", "required": False}
                ]
            },
            {
                "title": "Precipitants & Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "hf_ischaemia", "type": "toggle", "label": "Recent Ischaemia / MI Symptoms?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recent ischaemia = urgent cardiology. May need revascularisation.", "red_flag_negative": ""},
                    {"id": "hf_nsaids", "type": "toggle", "label": "NSAID / Steroid Use?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: NSAIDs/steroids worsen HF. Stop immediately.", "red_flag_negative": ""},
                    {"id": "hf_alcohol_salt", "type": "toggle", "label": "Alcohol Excess / High Salt Intake?", "required": False},
                    {"id": "hf_anaemia", "type": "toggle", "label": "Blood Loss / Anaemia Symptoms?", "required": False},
                    {"id": "hf_infection", "type": "toggle", "label": "Recent Infection / Illness?", "required": False},
                    {"id": "hf_attr_cm", "type": "multi_select", "label": "ATTR-CM Red Flags? (Carpal tunnel, polyneuropathy, GDMT intolerance)", "required": False, "options": ["Bilateral carpal tunnel", "Polyneuropathy", "Intolerance to low-dose beta-blocker/ACEi", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ATTR-CM suspected = urgent cardiology. Transthyretin amyloidosis needs specialist diagnosis.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination - Perfusion & Volume Status",
                "section_type": "examination",
                "questions": [
                    {"id": "hf_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 118/72"},
                    {"id": "hf_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 78"},
                    {"id": "hf_rhythm", "type": "single_select", "label": "Rhythm", "required": True, "options": ["Regular", "Irregular (AF)", "Paced"]},
                    {"id": "hf_weight", "type": "number", "label": "Weight (kg)", "required": True, "placeholder": "e.g., 78"},
                    {"id": "hf_target_weight", "type": "number", "label": "Target / Dry Weight (kg)", "required": False, "placeholder": "e.g., 75"},
                    {"id": "hf_haemodynamic", "type": "single_select", "label": "Haemodynamic Profile", "required": True, "options": ["Warm & Dry (well-perfused, no congestion)", "Warm & Wet (well-perfused, congested)", "Cold & Dry (hypoperfused, no congestion)", "Cold & Wet (hypoperfused + congested) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Cold & Wet = cardiogenic shock. Emergency admission.", "red_flag_negative": ""},
                    {"id": "hf_jvp", "type": "single_select", "label": "JVP", "required": True, "options": ["Normal", "Elevated", "Not assessed"]},
                    {"id": "hf_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal", "S3 Gallop - RED FLAG", "S4", "Murmur present", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: S3 gallop = ventricular dysfunction. Urgent echo.", "red_flag_negative": ""},
                    {"id": "hf_chest", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear B/L", "Bibasal crackles", "Wheeze", "Not assessed"]},
                    {"id": "hf_oedema_extent", "type": "single_select", "label": "Oedema Extent", "required": True, "options": ["None", "Ankle", "Mid-calf", "Knee", "Sacral / Anasarca"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Heart Failure with Reduced Ejection Fraction (HFrEF - LVEF ≤40%)",
                    "Heart Failure with Preserved Ejection Fraction (HFpEF - LVEF ≥50%)",
                    "Heart Failure with Mildly Reduced EF (HFmrEF - LVEF 41-49%)",
                    "Right Heart Failure / Cor Pulmonale",
                    "Acute Decompensated Heart Failure (ADHF)",
                    "ATTR-CM (Transthyretin Amyloidosis)"
                ],
                "questions": [
                    {"id": "hf_ecg", "type": "single_select", "label": "ECG", "required": True, "options": ["Normal sinus rhythm", "AF", "LBBB (QRS ≥130ms - ?CRT candidate)", "LVH", "Pathological Q waves (prior MI)", "Not done"]},
                    {"id": "hf_qrs", "type": "number", "label": "QRS Duration (ms)", "required": False, "placeholder": "e.g., 140", "is_red_flag": True, "red_flag_positive": "RED FLAG: QRS ≥130ms LBBB = ?CRT candidate. Cardiology referral.", "red_flag_negative": ""},
                    {"id": "hf_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC (anaemia)", "U&E / eGFR", "LFTs", "TFTs", "Ferritin / Iron studies", "ESR / CRP", "NT-proBNP / BNP"]},
                    {"id": "hf_cxr", "type": "toggle", "label": "Chest X-Ray Requested?", "required": False},
                    {"id": "hf_echo", "type": "single_select", "label": "Echocardiogram", "required": True, "options": ["Urgent TTE requested", "Routine TTE requested", "Already done - LVEF ___%", "Not yet requested"]}
                ]
            },
            {
                "title": "GDMT - 4 Pillars of Heart Failure Therapy",
                "section_type": "plan",
                "questions": [
                    {"id": "hf_acei_arb_arni", "type": "single_select", "label": "ACEi / ARB / ARNI", "required": False, "options": ["Ramipril 2.5mg OD (titrate to 10mg OD)", "Lisinopril 2.5-5mg OD (titrate to 20-35mg OD)", "Losartan 50mg OD (titrate to 150mg OD)", "Sacubitril/Valsartan (Entresto) - requires 36h ACEi washout", "Not yet started", "Contraindicated"]},
                    {"id": "hf_beta_blocker", "type": "single_select", "label": "Beta-Blocker", "required": False, "options": ["Bisoprolol 1.25mg OD (titrate to 10mg OD)", "Carvedilol 3.125mg BD (titrate to 25-50mg BD)", "Nebivolol 1.25mg OD (titrate to 10mg OD)", "Not yet started (SBP must be >100)", "Contraindicated"]},
                    {"id": "hf_sglt2i", "type": "single_select", "label": "SGLT2 Inhibitor", "required": False, "options": ["Dapagliflozin 10mg OD", "Empagliflozin 10mg OD", "Not yet started", "Contraindicated"]},
                    {"id": "hf_mra", "type": "single_select", "label": "Mineralocorticoid Receptor Antagonist (MRA)", "required": False, "options": ["Spironolactone 25mg OD", "Eplerenone 25mg OD (titrate to 50mg OD)", "Not yet started (K+ must be <5.0)", "Contraindicated"]},
                    {"id": "hf_diuretic", "type": "single_select", "label": "Loop Diuretic (Congestion)", "required": False, "options": ["Furosemide 20mg mane", "Furosemide 40mg mane", "Furosemide 40mg BD", "Bumetanide 1mg mane", "Not needed (no congestion)"]}
                ]
            },
            {
                "title": "Safety Monitoring & Advanced Therapies",
                "section_type": "plan",
                "questions": [
                    {"id": "hf_renal_check", "type": "toggle", "label": "U&E Recheck in 1 Week? (And 1-2 weeks post dose change)", "required": True},
                    {"id": "hf_acceptable_labs", "type": "toggle", "label": "Acceptable Parameters Known? (≤30% rise Cr, K+ ≤5.5)", "required": True},
                    {"id": "hf_avoid_nsaids", "type": "toggle", "label": "NSAIDs / Trimethoprim Avoidance Advised?", "required": True},
                    {"id": "hf_ivabradine", "type": "toggle", "label": "Ivabradine? (LVEF ≤35%, sinus, HR ≥70 despite max BB)", "required": False},
                    {"id": "hf_crt", "type": "toggle", "label": "CRT Candidate? (QRS ≥130ms LBBB, LVEF ≤35%)", "required": False},
                    {"id": "hf_icd", "type": "toggle", "label": "ICD Candidate? (LVEF ≤35% after 3 months optimal GDMT)", "required": False},
                    {"id": "hf_palliative", "type": "single_select", "label": "Surprise Question (12-month mortality)", "required": False, "options": ["Yes - would be surprised if died in 12 months", "No - would NOT be surprised → consider palliative/ACP"]}
                ]
            },
            {
                "title": "Lifestyle & Self-Management",
                "section_type": "plan",
                "safety_netting": "Daily morning weight: log daily. Report weight gain >1.5-2kg over 2-3 days (fluid retention). Home BP monitoring with BIHS-validated monitor. Low salt diet. Moderate fluid intake if hyponatraemic. Smoking cessation offered. Annual influenza + pneumococcal vaccines UTD. Return immediately if: worsening SOB, orthopnoea, PND, rapid weight gain, palpitations, chest pain, or syncope. Avoid NSAIDs, OTC decongestants, excessive salt, and alcohol. U&E must be rechecked 1 week after starting or changing doses of ACEi/ARB/ARNI/MRA.",
                "questions": [
                    {"id": "hf_weight_monitoring", "type": "toggle", "label": "Daily Weight Monitoring Advised? (Report gain >1.5-2kg in 2-3 days)", "required": True},
                    {"id": "hf_home_bp", "type": "toggle", "label": "Home BP Monitoring Advised?", "required": False},
                    {"id": "hf_diet", "type": "toggle", "label": "Low Salt / Fluid Advice Given?", "required": True},
                    {"id": "hf_smoking", "type": "toggle", "label": "Smoking Cessation Offered?", "required": False},
                    {"id": "hf_vaccines", "type": "single_select", "label": "Vaccination Status", "required": True, "options": ["Influenza + Pneumococcal UTD", "Influenza only", "Pneumococcal only", "Neither - advised today"]},
                    {"id": "hf_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1 week U&E, 2-4 weeks clinical review, titrate GDMT every 2-4 weeks"}
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
    seed_heart_failure()