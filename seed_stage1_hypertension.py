from app.database import SessionLocal
from app.models import User, Template, Category

def seed_stage1_hypertension():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Stage 1 Hypertension Assessment",
        "description": "Structured assessment for Stage 1 hypertension covering ABPM/HBPM interpretation, target organ damage screening, QRISK stratification, and treatment thresholds.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Diagnosis & BP Profile",
                "section_type": "history",
                "questions": [
                    {"id": "htn_presenting_complaint", "type": "text", "label": "Reason for Assessment", "required": True, "placeholder": "e.g., Raised BP on routine check / ABPM result"},
                    {"id": "htn_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 48"},
                    {"id": "htn_clinic_bp", "type": "text", "label": "Clinic BP (mmHg)", "required": True, "placeholder": "e.g., 140/90"},
                    {"id": "htn_abpm_day", "type": "text", "label": "ABPM / HBPM Daytime Average (mmHg)", "required": True, "placeholder": "e.g., 135/85"},
                    {"id": "htn_stage", "type": "single_select", "label": "Hypertension Stage", "required": True, "options": ["Stage 1 (ABPM ≥135/85)", "Stage 2 (ABPM ≥150/95)", "Severe (Clinic ≥180/120) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe HTN (≥180/120) = urgent assessment. If papilloedema or AKI = same-day admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Target Organ Damage (TOD) Screening",
                "section_type": "history",
                "questions": [
                    {"id": "htn_headaches", "type": "toggle", "label": "Headaches?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe headache + HTN = ?malignant hypertension, intracranial bleed. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "htn_visual_disturbance", "type": "toggle", "label": "Visual Disturbance?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms = ?hypertensive retinopathy, papilloedema. Urgent fundoscopy.", "red_flag_negative": ""},
                    {"id": "htn_nausea_vomiting", "type": "toggle", "label": "Nausea / Vomiting? (Raised ICP)", "required": False},
                    {"id": "htn_phaeochromocytoma", "type": "multi_select", "label": "Phaeochromocytoma Symptoms?", "required": True, "options": ["Episodic sweating", "Palpitations", "Severe headache (paroxysmal)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Paroxysmal triad = ?phaeochromocytoma. Urgent endocrine referral.", "red_flag_negative": ""},
                    {"id": "htn_conns", "type": "toggle", "label": "Persistent Muscle Weakness / Cramps? (Conn's - hypokalaemia)", "required": False},
                    {"id": "htn_ckd_history", "type": "toggle", "label": "Known CKD / Renal Disease?", "required": True},
                    {"id": "htn_family_htn", "type": "toggle", "label": "Family History Early-Onset HTN / CVD?", "required": True}
                ]
            },
            {
                "title": "Exogenous Factors & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "htn_nsaids", "type": "toggle", "label": "Regular NSAID Use?", "required": True},
                    {"id": "htn_steroids", "type": "toggle", "label": "Oral Corticosteroids?", "required": True},
                    {"id": "htn_decongestants", "type": "toggle", "label": "Sympathomimetic Decongestants?", "required": False},
                    {"id": "htn_liquorice", "type": "toggle", "label": "Excessive Liquorice Consumption?", "required": False},
                    {"id": "htn_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
                    {"id": "htn_alcohol", "type": "single_select", "label": "Alcohol", "required": True, "options": ["None", "Within limits", "Excess"]},
                    {"id": "htn_diet_exercise", "type": "single_select", "label": "Diet & Exercise", "required": True, "options": ["Balanced + Regular exercise", "Fair", "Poor - high salt/sedentary"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "htn_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 28"},
                    {"id": "htn_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal", "Murmur (coarctation/valve)", "S4 (LVH)", "Not assessed"]},
                    {"id": "htn_pulses", "type": "single_select", "label": "Peripheral Pulses", "required": True, "options": ["B/L present + normal", "Radio-femoral delay - RED FLAG", "Weak femoral - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Radio-femoral delay / weak femoral = ?coarctation. Urgent vascular imaging.", "red_flag_negative": ""},
                    {"id": "htn_cushingoid", "type": "toggle", "label": "Cushingoid Features? (Striae, buffalo hump, central obesity)", "required": False},
                    {"id": "htn_renal_bruit", "type": "toggle", "label": "Renal Artery Bruit?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Renal bruit = ?renal artery stenosis. Renal USS + referral.", "red_flag_negative": ""},
                    {"id": "htn_fundoscopy", "type": "single_select", "label": "Fundoscopy / Optometrist Report", "required": False, "options": ["Normal", "Hypertensive retinopathy (AV nipping)", "Haemorrhages / exudates - RED FLAG", "Papilloedema - RED FLAG", "Not yet done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Haemorrhages/exudates/papilloedema = malignant HTN. Same-day admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations & TOD Workup",
                "section_type": "assessment",
                "differentials": [
                    "Primary / Essential Hypertension",
                    "White Coat Hypertension (excluded by ABPM)",
                    "Secondary Hypertension (renal, endocrine, coarctation)",
                    "Renal Artery Stenosis",
                    "Phaeochromocytoma",
                    "Conn's Syndrome / Primary Aldosteronism",
                    "Cushing's Syndrome",
                    "Coarctation of Aorta",
                    "Thyroid Disease"
                ],
                "questions": [
                    {"id": "htn_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["U&E / eGFR (baseline renal, K+)", "HbA1c / Fasting Glucose", "TFTs", "Fasting Lipids", "None"]},
                    {"id": "htn_uacr", "type": "toggle", "label": "Urine ACR + Dipstick Ordered?", "required": True},
                    {"id": "htn_ecg", "type": "single_select", "label": "ECG - LVH Criteria", "required": True, "options": ["No LVH", "LVH by Cornell/Sokolow - RED FLAG", "ST-T changes (strain) - RED FLAG", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: LVH = target organ damage. Antihypertensive therapy indicated regardless of QRISK.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "QRISK3 & Treatment Threshold",
                "section_type": "assessment",
                "questions": [
                    {"id": "htn_cvd", "type": "toggle", "label": "Established CVD? (IHD, Stroke, PAD)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Established CVD = treat regardless of BP stage. Antiplatelet + statin + BP control.", "red_flag_negative": ""},
                    {"id": "htn_tod_present", "type": "toggle", "label": "Target Organ Damage Present? (LVH, CKD, retinopathy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: TOD present = treat regardless of QRISK. Urgent BP control.", "red_flag_negative": ""},
                    {"id": "htn_diabetes", "type": "toggle", "label": "Type 2 Diabetes?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: DM + HTN = treat. Target BP <130/80. Start ACEi/ARB.", "red_flag_negative": ""},
                    {"id": "htn_qrisk", "type": "number", "label": "QRISK3 Score (%)", "required": True, "placeholder": "e.g., 8"},
                    {"id": "htn_treat_now", "type": "toggle", "label": "Pharmacotherapy Indicated? (CVD / TOD / DM / QRISK ≥10%)", "required": True}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: severe headache, visual disturbance, chest pain, SOB, or neurological symptoms. Attend ED if BP ≥180/120 with symptoms. Lifestyle: DASH/Mediterranean diet, sodium <6g/day, regular exercise (150 min/week), smoking cessation, alcohol reduction. NICE Patient Decision Aid provided. If pharmacotherapy indicated (CVD/TOD/DM/QRISK ≥10%): ACEi/ARB first-line (<55 years) or CCB (≥55 years or Black). Target BP <140/90 (<130/80 if DM or CKD). Recheck U&E 1-2 weeks after starting ACEi/ARB. If all investigations clear + QRISK <10%: annual ABPM/HBPM review. If BP uncontrolled on triple therapy: refer secondary care for investigation of secondary HTN.",
                "questions": [
                    {"id": "htn_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Lifestyle only (no current indication for drugs)", "Start ACEi / ARB (first-line <55)", "Start CCB (first-line ≥55 or Black)", "Start combination therapy", "Refer secondary care (?secondary HTN)", "Awaiting investigation results"]},
                    {"id": "htn_lifestyle", "type": "toggle", "label": "Lifestyle Advice Given? (DASH diet, salt <6g, exercise)", "required": True},
                    {"id": "htn_decision_aid", "type": "toggle", "label": "NICE Patient Decision Aid Provided?", "required": False},
                    {"id": "htn_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review with results, start treatment if indicated. Annual ABPM if lifestyle only."}
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
    seed_stage1_hypertension()