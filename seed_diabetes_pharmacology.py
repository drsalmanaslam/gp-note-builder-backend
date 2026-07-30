from app.database import SessionLocal
from app.models import User, Template, Category

def seed_diabetes_pharmacology():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "Pharmacological Management of Type 2 Diabetes",
        "description": "Stepwise treatment escalation template for T2DM covering drug class selection by comorbidity, renal safety, adverse effects, and guideline-directed targets.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Patient Factors & Current Status",
                "section_type": "history",
                "questions": [
                    {"id": "dmrx_cvd", "type": "toggle", "label": "Established Cardiovascular Disease?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: CVD present = Gliflozin or Glutide preferred agents.", "red_flag_negative": ""},
                    {"id": "dmrx_bmi", "type": "single_select", "label": "BMI Status", "required": True, "options": ["Raised BMI (Glutide preferred for weight loss)", "Normal BMI"]},
                    {"id": "dmrx_egfr", "type": "number", "label": "eGFR (mL/min/1.73m²)", "required": True, "placeholder": "e.g., 55 (Drives agent choice + dose limits)"},
                    {"id": "dmrx_hf", "type": "single_select", "label": "Heart Failure Status", "required": True, "options": ["HFrEF (EF <40%) - SGLT2i indicated", "At risk of heart failure", "Known heart failure", "None"]},
                    {"id": "dmrx_frailty", "type": "single_select", "label": "Frailty Status", "required": True, "options": ["None", "Moderate (target HbA1c 64)", "Severe (target HbA1c 69-75)"]},
                    {"id": "dmrx_pad_foot", "type": "toggle", "label": "Peripheral Arterial Disease / Diabetic Foot?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: PAD/foot disease = caution with SGLT2i (amputation risk). Avoid Canagliflozin.", "red_flag_negative": ""},
                    {"id": "dmrx_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 62"},
                    {"id": "dmrx_hba1c_current", "type": "number", "label": "Current HbA1c (mmol/mol)", "required": True, "placeholder": "e.g., 72"},
                    {"id": "dmrx_hba1c_target", "type": "single_select", "label": "HbA1c Target", "required": True, "options": ["53 mmol/mol (standard - life expectancy >10y)", "58 mmol/mol (individualised)", "64 mmol/mol (elderly/comorbidities)", "75 mmol/mol (moderate/severe frailty)"]}
                ]
            },
            {
                "title": "Stepwise Treatment Escalation",
                "section_type": "plan",
                "questions": [
                    {"id": "dmrx_step1", "type": "single_select", "label": "Step 1: Lifestyle ± First Agent", "required": True, "options": ["HbA1c >48 despite lifestyle → Start Metformin", "Target achieved on lifestyle alone"]},
                    {"id": "dmrx_step2", "type": "single_select", "label": "Step 2: HbA1c ≥58 on Metformin → Add Second Agent", "required": False, "options": ["Add Gliflozin (SGLT2i)", "Add Gliptin (DPP-4i)", "Add Glutide (GLP-1)", "Gliclazide (selected cases)", "Not yet at step 2"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT combine Gliptin with Glutide - therapeutic duplication.", "red_flag_negative": ""},
                    {"id": "dmrx_step3", "type": "single_select", "label": "Step 3: HbA1c ≥58 on Two Agents → Add Third Agent", "required": False, "options": ["Add Gliflozin", "Add Gliptin", "Add Glutide", "Not yet at step 3"]},
                    {"id": "dmrx_step4", "type": "single_select", "label": "Step 4: Injectable Escalation", "required": False, "options": ["Add Glutide - stop Gliptin, reduce Gliclazide", "Add basal insulin - stop Gliclazide", "Not yet at step 4"]}
                ]
            },
            {
                "title": "Agent Selection by Comorbidity (EASD/ADA/SIGN)",
                "section_type": "plan",
                "questions": [
                    {"id": "dmrx_cvd_choice", "type": "single_select", "label": "Pre-existing CVD → Preferred Agent", "required": False, "options": ["Canagliflozin / Empagliflozin (SGLT2i)", "Liraglutide (GLP-1)", "Not applicable"]},
                    {"id": "dmrx_hf_choice", "type": "single_select", "label": "CVD + Heart Failure (or at risk) → Preferred", "required": False, "options": ["Dapagliflozin 10mg (HFrEF licensed) - if eGFR >60", "GLP-1 if not at target", "Not applicable"]},
                    {"id": "dmrx_ckd_choice", "type": "single_select", "label": "Known CKD (eGFR <60) → Consider", "required": False, "options": ["Canagliflozin - renal benefit (licensed US/Canada eGFR >30)", "GLP-1 (usable down to eGFR 15)", "Linagliptin (no dose adjustment)", "Not applicable"]}
                ]
            },
            {
                "title": "Gliflozins (SGLT2 Inhibitors) - Safety",
                "section_type": "plan",
                "questions": [
                    {"id": "dmrx_gliflozin_drug", "type": "single_select", "label": "Gliflozin Agent", "required": False, "options": ["Canagliflozin (Invokana) 100-300mg OD", "Dapagliflozin (Forxiga) 10mg OD", "Empagliflozin (Jardiance) 10-25mg OD", "Ertugliflozin (Steglatro) 5-15mg OD", "Not starting Gliflozin"]},
                    {"id": "dmrx_gliflozin_renal", "type": "single_select", "label": "Renal Criteria", "required": False, "options": ["eGFR >59 - safe to start for glucose lowering", "eGFR ≤59 - do NOT start (diminished glycaemic efficacy)", "eGFR ≤44 - STOP (loss of efficacy)", "Not applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT start as glucose-lowering if eGFR ≤59. Stop if eGFR ≤44.", "red_flag_negative": ""},
                    {"id": "dmrx_gliflozin_contraindications", "type": "multi_select", "label": "Contraindications / Cautions", "required": False, "options": ["Peripheral arterial disease (avoid Canagliflozin)", "Diabetic foot disease", "Combination with Pioglitazone (avoid)", "None present"]},
                    {"id": "dmrx_gliflozin_counselling", "type": "multi_select", "label": "Adverse Effects Counselled", "required": False, "options": ["UTIs / genital thrush", "DKA risk (euglycaemic DKA possible - normal glucose doesn't exclude)", "Amputation risk (Canagliflozin - MHRA 2016)", "Fournier's gangrene risk (class-wide - MHRA 2019)", "Sick-day rule: STOP during dehydrating illness", "Not applicable"]}
                ]
            },
            {
                "title": "Gliptins (DPP-4 Inhibitors)",
                "section_type": "plan",
                "questions": [
                    {"id": "dmrx_gliptin_drug", "type": "single_select", "label": "Gliptin Agent", "required": False, "options": ["Sitagliptin (Januvia) 100mg OD", "Vildagliptin (Galvus) 50mg BD", "Linagliptin (Trajenta) 5mg OD (no renal adjustment)", "Saxagliptin (Onglyza) 5mg OD", "Not starting Gliptin"]},
                    {"id": "dmrx_gliptin_note", "type": "toggle", "label": "Least effective HbA1c reduction, no CV benefit, weight neutral. Well tolerated. Reduce dose in renal impairment except Linagliptin.", "required": False}
                ]
            },
            {
                "title": "Glutides (GLP-1 Receptor Agonists)",
                "section_type": "plan",
                "questions": [
                    {"id": "dmrx_glutide_drug", "type": "single_select", "label": "Glutide Agent", "required": False, "options": ["Semaglutide (Ozempic) weekly SC", "Dulaglutide (Trulicity) weekly SC", "Liraglutide (Victoza) daily SC", "Exenatide BD (Byetta)", "Exenatide weekly (Bydureon)", "Not starting Glutide"]},
                    {"id": "dmrx_glutide_note", "type": "toggle", "label": "Weight loss ~5kg at 2 years. Usable down to eGFR 15. Stop Gliptin before starting (duplication). GI side effects common. Pancreatitis risk 1:100-1,000.", "required": False}
                ]
            },
            {
                "title": "Other Agents",
                "section_type": "plan",
                "questions": [
                    {"id": "dmrx_gliclazide", "type": "toggle", "label": "Gliclazide? (Hypo risk, weight gain, no CV benefit. May be useful for steroid-induced hyperglycaemia)", "required": False},
                    {"id": "dmrx_pioglitazone", "type": "toggle", "label": "Pioglitazone? (CI: heart failure. Caution: bladder cancer, fractures. Weight gain. Check urine dip before starting)", "required": False}
                ]
            },
            {
                "title": "Plan Summary",
                "section_type": "plan",
                "safety_netting": "DKA warning (SGLT2i): nausea, vomiting, abdominal pain, tachypnoea, thirst, rapid weight loss. Can occur with normal glucose (euglycaemic DKA). Check blood ketones if suspected. STOP SGLT2i during dehydrating illness. Amputation risk: stop Canagliflozin if ulcers/osteomyelitis/gangrene develop. Check feet regularly. Pancreatitis risk (Glutides/Gliptins): abdominal pain + nausea + vomiting = stop + check amylase/lipase. Fournier's gangrene (SGLT2i): perineal pain/erythema = emergency. BP target: <140/90 (age <80), <150/90 (≥80), <130/80 (eGFR <60 + DM). HbA1c step-up trigger: 48 on lifestyle, 58 on medication. Target ≥40% reduction in non-HDL cholesterol.",
                "questions": [
                    {"id": "dmrx_agents_selected", "type": "multi_select", "label": "Agent(s) Selected Today", "required": True, "options": ["Metformin", "Gliflozin (SGLT2i)", "Gliptin (DPP-4i)", "Glutide (GLP-1)", "Gliclazide", "Pioglitazone", "Basal insulin"]},
                    {"id": "dmrx_agents_discontinued", "type": "multi_select", "label": "Agent(s) Discontinued Today", "required": False, "options": ["Gliptin (duplication with Glutide)", "Gliclazide (insulin/Glutide initiation)", "None"]},
                    {"id": "dmrx_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat HbA1c in 3 months, routine diabetic review"}
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
    seed_diabetes_pharmacology()