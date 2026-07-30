from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hyponatraemia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low Sodium / Hyponatraemia",
        "description": "Comprehensive hyponatraemia assessment covering NICE severity triage, fluid status interpretation, SIADH diagnostic criteria, and medication review.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "SEVERITY - Determine First (NICE CKS)",
                "section_type": "assessment",
                "questions": [
                    {"id": "hypona_level", "type": "number", "label": "Sodium Level (mmol/L) - NR: 135-145", "required": True, "placeholder": "e.g., 128", "is_red_flag": True, "red_flag_positive": "RED FLAG: Na <125 = SEVERE - Refer to A&E. Na 125-129 = MODERATE - Secondary care advice. Na 130-135 = MILD - Primary care management.", "red_flag_negative": ""},
                    {"id": "hypona_onset", "type": "single_select", "label": "Onset (Correction Rate Risk)", "required": True, "options": ["Acute (<48 Hours) - Higher Risk of Osmotic Demyelination", "Chronic (>48 Hours)", "Uncertain"]},
                    {"id": "hypona_severity", "type": "single_select", "label": "Severity Category", "required": True, "options": ["Mild: Na 130-135 → Primary Care Management", "Moderate: Na 125-129 → Secondary Care Review/Advice", "Severe: Na <125 → REFER TO A&E"]}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "hypona_symptoms", "type": "multi_select", "label": "Symptom Screen at Time of Bloods", "required": True, "options": ["Confusion", "Headache", "Cramps", "Nausea", "Ataxia", "Dizziness", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Confusion/ataxia + severe hyponatraemia = risk of cerebral oedema. Urgent A&E.", "red_flag_negative": ""},
                    {"id": "hypona_meds_siadh", "type": "multi_select", "label": "Medications Causing SIADH / Hyponatraemia", "required": True, "options": ["SSRI (Citalopram = Highest Risk)", "Carbamazepine (Most Common Antiepileptic Cause)", "Other Antiepileptic", "Diuretics (Thiazide > Loop)", "PPI", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: SSRIs (esp. Citalopram) = highest SIADH risk. Consider switch to TCA/Mirtazapine. Carbamazepine = most common antiepileptic cause.", "red_flag_negative": ""},
                    {"id": "hypona_gi_losses", "type": "toggle", "label": "Recent Vomiting, Diarrhoea, or Excessive Sweating?", "required": True},
                    {"id": "hypona_pmh", "type": "multi_select", "label": "Relevant Past History", "required": True, "options": ["Liver Disease / Cirrhosis", "Congestive Cardiac Failure", "Renal Failure / CKD", "Steroid Use", "Recent Diuretic Use", "None"]}
                ]
            },
            {
                "title": "Examination - Fluid Status Assessment",
                "section_type": "examination",
                "questions": [
                    {"id": "hypona_lying_bp", "type": "text", "label": "Lying BP (mmHg)", "required": False, "placeholder": "e.g., 110/70"},
                    {"id": "hypona_standing_bp", "type": "text", "label": "Standing BP (mmHg) - Orthostatic Hypotension?", "required": False, "placeholder": "e.g., 95/65"},
                    {"id": "hypona_hr", "type": "number", "label": "Pulse (bpm) - Tachycardia?", "required": False, "placeholder": "e.g., 98"},
                    {"id": "hypona_mucosa", "type": "single_select", "label": "Buccal Mucosa", "required": False, "options": ["Moist", "Dry - ?Hypovolaemia"]},
                    {"id": "hypona_jvp", "type": "single_select", "label": "JVP", "required": False, "options": ["Not Visible - ?Hypovolaemia", "Visible - Normal", "Raised - ?Hypervolaemia"]},
                    {"id": "hypona_oedema", "type": "single_select", "label": "Peripheral / Sacral / Pulmonary Oedema", "required": False, "options": ["Absent", "Present - ?Hypervolaemia"]},
                    {"id": "hypona_fluid_status", "type": "single_select", "label": "Fluid Status Interpretation", "required": True, "options": ["HYPOVOLAEMIC (Low BP, JVP Not Visible, Dry Mucosa): GI Loss / Diuretics / Addison's", "HYPERVOLAEMIC (Raised JVP, Oedema): Heart Failure / Liver Failure / Renal Failure", "EUVOLAEMIC (Normal): SIADH / Tea & Toast Diet / Psychogenic Polydipsia"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "hypona_renal", "type": "toggle", "label": "Repeat Renal Profile Ordered?", "required": False},
                    {"id": "hypona_lipids_glucose", "type": "toggle", "label": "Fasting Lipids + Fasting Glucose / HbA1c Ordered?", "required": False},
                    {"id": "hypona_uric_acid", "type": "toggle", "label": "Uric Acid Level Ordered?", "required": False},
                    {"id": "hypona_tfts", "type": "toggle", "label": "TFTs Ordered? (Screen for Hypothyroidism)", "required": False},
                    {"id": "hypona_uacr", "type": "toggle", "label": "Urinary ACR + Urine Dipstick Ordered?", "required": False},
                    {"id": "hypona_urine_na", "type": "number", "label": "Urinary Sodium (mmol/L)", "required": False, "placeholder": "e.g., 45"},
                    {"id": "hypona_urine_na_interpret", "type": "single_select", "label": "Urinary Na Interpretation", "required": False, "options": ["<20mmol/L: ?Diarrhoea / Sweating / Vomiting (Extrarenal Loss)", ">20mmol/L: ?SIADH (Euvolaemic) / Addison's (Hypovolaemic)", "Awaiting Result"]},
                    {"id": "hypona_serum_osmo", "type": "number", "label": "Serum Osmolality (mOsmol/L) - NR: 275-295", "required": False, "placeholder": "e.g., 260 (Use MDCalc)"},
                    {"id": "hypona_urine_osmo", "type": "number", "label": "Urine Osmolality (mOsmol/L)", "required": False, "placeholder": "e.g., 350"},
                    {"id": "hypona_osmo_interpret", "type": "single_select", "label": "Osmolality Interpretation", "required": False, "options": ["Urine Osmo < Serum Osmo: ?Tea & Toast Diet / Psychogenic Polydipsia", "Urine Osmo > Serum Osmo: ?SIADH", "Awaiting Result"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "SIADH (Euvolaemic + Low Serum Osmo + High Urine Osmo + High Urine Na >30)",
                    "Medication-Induced (SSRI, Carbamazepine, Diuretics, PPI)",
                    "GI Losses (Vomiting, Diarrhoea - Hypovolaemic, Urine Na <20)",
                    "Heart Failure (Hypervolaemic, Raised JVP, Oedema)",
                    "Liver Cirrhosis (Hypervolaemic)",
                    "Renal Failure (Hypervolaemic)",
                    "Addison's Disease (Hypovolaemic + High Urine Na)",
                    "Tea & Toast Diet (Elderly, Euvolaemic, Low Urine Osmo)",
                    "Psychogenic Polydipsia (Euvolaemic, Low Urine Osmo)",
                    "Hypothyroidism"
                ],
                "questions": [
                    {"id": "hypona_siadh_criteria", "type": "toggle", "label": "SIADH Criteria Met? (Euvolaemic + Serum Osmo <275 + Urine Osmo >100 + Urine Na >30)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: SIADH confirmed = investigate cause: medications, respiratory disease, CNS disease, or malignancy.", "red_flag_negative": ""},
                    {"id": "hypona_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Mild Hyponatraemia - ?Cause (Primary Care Workup)", "Moderate Hyponatraemia - Requires Secondary Care Advice", "Severe Hyponatraemia - REFER A&E", "?SIADH", "?Medication-Induced", "?GI Losses / Dehydration"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Mild (Na 130-135): Primary care management - investigate cause. Moderate (Na 125-129): Secondary care review/advice recommended. Severe (Na <125): REFER TO A&E. Acute hyponatraemia (<48h) = higher risk of osmotic demyelination if corrected too rapidly. Chronic hyponatraemia (>48h) = correct slowly (max 8-10 mmol/L per 24 hours). Hyponatraemia is typically driven more by water retention (vasopressin/ADH) than sodium loss. SIADH: euvolaemic + low serum osmo + high urine osmo + high urine Na. Causes: medications, respiratory disease, CNS disease, malignancy. SSRIs (esp. Citalopram) = highest risk. Consider switching to TCA/Mirtazapine. Carbamazepine = most common antiepileptic cause.",
                "questions": [
                    {"id": "hypona_plan", "type": "single_select", "label": "Management by Severity", "required": True, "options": ["Primary Care Management (Mild: Na 130-135)", "Secondary Care Advice (Moderate: Na 125-129)", "Refer A&E (Severe: Na <125)", "Fluid Restriction (SIADH - 800-1000ml/Day)", "Stop Causative Medication"]},
                    {"id": "hypona_med_review", "type": "toggle", "label": "Causative Medication Reviewed? (SSRI → TCA/Mirtazapine? Stop Carbamazepine/Diuretic?)", "required": False},
                    {"id": "hypona_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Mild)", "Endocrinology / Acute Medicine (Moderate)", "A&E (Severe)", "Respiratory / CNS / Oncology (If SIADH Cause Identified)"]},
                    {"id": "hypona_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat Na in 1-2 weeks, manage underlying cause, A&E if <125"}
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
    seed_hyponatraemia()