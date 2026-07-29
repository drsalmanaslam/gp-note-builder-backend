from app.database import SessionLocal
from app.models import User, Template, Category

def seed_contraception_minor():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Contraception in a Minor (Under 17) - Gillick Competence",
        "description": "Fraser Guidelines-based contraception consultation for minors covering Gillick competence assessment, safeguarding, UKMEC screening, and prescribing without parental consent.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Gillick Competence / Fraser Guidelines (Complete FIRST)",
                "section_type": "history",
                "questions": [
                    {"id": "cm_patient_age", "type": "number", "label": "Patient's Age", "required": True, "placeholder": "e.g., 15"},
                    {"id": "cm_gillick1", "type": "toggle", "label": "Criterion 1: Patient Understands the Advice - Assessed as Competent to Consent?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: All 5 Fraser criteria must be met + documented before proceeding.", "red_flag_negative": ""},
                    {"id": "cm_gillick2", "type": "toggle", "label": "Criterion 2: Cannot Be Persuaded to Inform Parents/Guardians or Allow GP to Inform Them?", "required": True},
                    {"id": "cm_gillick3", "type": "toggle", "label": "Criterion 3: Likely to Begin/Continue Sexual Intercourse With or Without Contraception?", "required": True},
                    {"id": "cm_gillick4", "type": "toggle", "label": "Criterion 4: Without Contraception, Physical/Mental Health Likely to Suffer?", "required": True},
                    {"id": "cm_gillick5", "type": "toggle", "label": "Criterion 5: Best Interests Require Providing Contraception Without Parental Consent?", "required": True},
                    {"id": "cm_all_criteria_met", "type": "toggle", "label": "ALL 5 Fraser Criteria Met + Documented?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Proceed only if ALL criteria confirmed. Document fully.", "red_flag_negative": "STOP: Do NOT proceed without all Fraser criteria met."}
                ]
            },
            {
                "title": "Safeguarding Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "cm_partner_age", "type": "number", "label": "Partner's Age (Assess for Significant Age Gap / Power Imbalance)", "required": True, "placeholder": "e.g., 22 (Note if >2 years difference)"},
                    {"id": "cm_coercion", "type": "toggle", "label": "Any Indication of Coercion, Exploitation, or Non-Consensual Activity?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Safeguarding concern = refer to social work / child protection immediately.", "red_flag_negative": ""},
                    {"id": "cm_safeguarding_referral", "type": "single_select", "label": "Safeguarding Referral Indicated?", "required": True, "options": ["Yes - Refer Now", "No - No Concerns Identified", "Discuss with Safeguarding Lead"]},
                    {"id": "cm_age_15_under", "type": "toggle", "label": "Patient Aged ≤15? (Refer to Local Youth Health Service in Addition)", "required": True}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "cm_preference", "type": "single_select", "label": "Contraceptive Preference", "required": True, "options": ["COCP (Pill)", "Patch (Evra)", "Ring (NuvaRing)", "LARC (Coil/Implant) - Refer", "Progestogen-Only Pill", "Undecided"]},
                    {"id": "cm_compliance", "type": "toggle", "label": "Currently on Method? Taking Daily, No Missed Pills?", "required": False},
                    {"id": "cm_lmp", "type": "text", "label": "LMP / Cycle Regularity & Duration", "required": True, "placeholder": "e.g., 10 days ago, regular 28-day cycle, 5 days"},
                    {"id": "cm_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Non-Smoker", "Current Smoker"]}
                ]
            },
            {
                "title": "UKMEC Screening",
                "section_type": "history",
                "questions": [
                    {"id": "cm_dvt_pe", "type": "toggle", "label": "Previous DVT/PE? (MEC 4)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: MEC 4 = COCP contraindicated.", "red_flag_negative": ""},
                    {"id": "cm_breast_ca", "type": "toggle", "label": "Previous Breast Cancer? (MEC 4)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: MEC 4 = COCP contraindicated.", "red_flag_negative": ""},
                    {"id": "cm_migraine_aura", "type": "toggle", "label": "Migraine WITH Aura? (MEC 4)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: MEC 4 = COCP contraindicated.", "red_flag_negative": ""},
                    {"id": "cm_other_mec", "type": "multi_select", "label": "Other UKMEC Factors", "required": True, "options": ["Migraine Without Aura", "FHx VTE <45 (MEC 3)", "Diabetes", "Hypertension", "Liver Disease", "Immobility", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "cm_bp", "type": "text", "label": "Blood Pressure (mmHg) - MEC 3 if ≥140/90", "required": True, "placeholder": "e.g., 112/70"},
                    {"id": "cm_bmi", "type": "number", "label": "BMI (kg/m²) - MEC 3 if ≥35", "required": True, "placeholder": "e.g., 22"}
                ]
            },
            {
                "title": "Patient Education",
                "section_type": "plan",
                "questions": [
                    {"id": "cm_mechanism", "type": "toggle", "label": "Mechanism Explained? (Inhibits Ovulation, Thickens Cervical Mucus, Inhibits Implantation)", "required": False},
                    {"id": "cm_risks", "type": "toggle", "label": "Risks Explained? (Small Increased: Breast Ca, Cervical Ca, Stroke, DVT)", "required": True},
                    {"id": "cm_benefits", "type": "toggle", "label": "Benefits Explained? (Decreased: Ovarian + Endometrial Cancer)", "required": False},
                    {"id": "cm_sti", "type": "toggle", "label": "Does NOT Protect Against STIs - Condom Use Discussed?", "required": True},
                    {"id": "cm_efficacy", "type": "toggle", "label": "Efficacy Explained? (~9 Pregnancies/100 Women-Years Typical Use)", "required": False},
                    {"id": "cm_side_effects", "type": "multi_select", "label": "Side Effects Counselled", "required": True, "options": ["Breakthrough Bleeding", "Weight Gain", "Mood Changes", "Nausea", "Headaches", "Breast Tenderness"]},
                    {"id": "cm_missed_pill", "type": "toggle", "label": "Missed Pill Rules Explained?", "required": True},
                    {"id": "cm_vte_warning", "type": "toggle", "label": "Return Immediately if Chest Pain, SOB, or Calf Swelling? (VTE/PE)", "required": True}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return if: side effects, change in circumstances raising safeguarding concern, chest pain/SOB/calf swelling (VTE). Encourage patient to reconsider involving a parent/trusted adult in future (without making this a condition of continued care). Routine contraception review. Gillick competence must be reassessed at each visit. Safeguarding: if partner significantly older, coercion suspected, or non-consensual activity = refer safeguarding immediately. Age ≤15: refer to local youth health service in addition.",
                "questions": [
                    {"id": "cm_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Requesting Contraception - Gillick Competent, Proceeding Without Parental Knowledge", "MEC 3/4 Present - Discuss Alternatives", "Safeguarding Concern - REFER", "Fraser Criteria Not Met - Cannot Proceed"]},
                    {"id": "cm_prescribing", "type": "single_select", "label": "Prescribing", "required": False, "options": ["Ovreena (30mcg) - 6 Month Script", "Mercilon (20mcg)", "Cilique (35mcg) - GMS", "Yasmin / Elvina", "Progestogen-Only (Azalia/Cerazette)", "LARC Referral", "Not Prescribed - MEC Contraindication"]},
                    {"id": "cm_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Routine contraception review in 6 months, sooner if concerns"}
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
    seed_contraception_minor()