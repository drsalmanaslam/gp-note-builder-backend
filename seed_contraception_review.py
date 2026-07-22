from app.database import SessionLocal
from app.models import User, Template, Category

def seed_contraception_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Contraception Review",
        "description": "Structured contraception review covering UKMEC eligibility, method satisfaction, red flags, LARC discussion, and safe prescribing.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "con_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 28"},
                    {"id": "con_review_reason", "type": "single_select", "label": "Reason for Review", "required": True, "options": ["Routine review", "Method issues/side effects", "New patient - method check", "Post-partum", "Peri-menopausal", "Considering switch", "Other"]}
                ]
            },
            {
                "title": "Current Method & Satisfaction",
                "section_type": "history",
                "questions": [
                    {"id": "con_current_method", "type": "single_select", "label": "Current Contraception Method", "required": True, "options": ["COCP (Combined Pill)", "POP (Progestogen-Only Pill)", "Implant (Nexplanon)", "IUS (Mirena/Jaydess/Levosert)", "Copper Coil (Cu-IUD)", "Depo-Provera Injection", "Patch (Evra)", "Vaginal Ring (NuvaRing)", "Barrier Methods (Condoms)", "Natural/Fertility Awareness", "None"]},
                    {"id": "con_duration", "type": "text", "label": "Duration on Current Method", "required": True, "placeholder": "e.g., 2 years"},
                    {"id": "con_satisfaction", "type": "single_select", "label": "Satisfaction with Method", "required": True, "options": ["Very satisfied", "Satisfied", "Neutral", "Unsatisfied - considering change", "Very unsatisfied - wants to stop/switch"]},
                    {"id": "con_compliance", "type": "single_select", "label": "Compliance (if pill/patch/ring)", "required": False, "options": ["Excellent - never misses", "Good - rarely misses (<1/month)", "Fair - occasionally misses (1-2/month)", "Poor - frequently misses", "Not applicable"]},
                    {"id": "con_side_effects", "type": "multi_select", "label": "Side Effects", "required": True, "options": ["Breast tenderness", "Nausea", "Headaches", "Mood changes/depression", "Weight gain", "Acne", "Reduced libido", "Irregular bleeding", "Heavy bleeding", "Amenorrhoea (no periods)", "Pelvic pain", "None"]},
                    {"id": "con_bleeding_pattern", "type": "single_select", "label": "Bleeding Pattern", "required": True, "options": ["Regular withdrawal bleeds", "Irregular/erratic", "Heavy bleeding", "No bleeding (amenorrhoea)", "Painful bleeding", "Unscheduled/new onset bleeding"], "is_red_flag": True, "red_flag_positive": "RED FLAG: New onset unscheduled bleeding - rule out pregnancy, infection, missed pills. If persistent, consider pelvic pathology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "UKMEC - Safety Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "con_bp_systolic", "type": "number", "label": "BP Systolic (mmHg) - MUST RECORD TODAY", "required": True, "placeholder": "e.g., 118", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP ≥140/90 - UKMEC 3 for CHC (relative contraindication). If ≥160/100 - UKMEC 4 (absolute contraindication to oestrogen).", "red_flag_negative": ""},
                    {"id": "con_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg) - MUST RECORD TODAY", "required": True, "placeholder": "e.g., 76", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP ≥140/90 - UKMEC 3 for CHC. If ≥160/100 - UKMEC 4. Do not prescribe oestrogen-containing methods.", "red_flag_negative": ""},
                    {"id": "con_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 26", "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI ≥35 - UKMEC 3 for CHC (risks generally outweigh benefits). BMI ≥40 - UKMEC 4 for CHC.", "red_flag_negative": ""},
                    {"id": "con_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Never smoked", "Ex-smoker", "Current smoker - <15 cigarettes/day", "Current smoker - ≥15 cigarettes/day"]},
                    {"id": "con_smoking_age_chc", "type": "toggle", "label": "Age ≥35 AND Current Smoker? (CHC contraindicated)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Age ≥35 + smoker = UKMEC 4 for oestrogen-containing contraception. Do not prescribe CHC. Offer progestogen-only methods.", "red_flag_negative": ""},
                    {"id": "con_migraine", "type": "single_select", "label": "Migraine History", "required": True, "options": ["No migraines", "Migraine WITHOUT aura", "Migraine WITH aura"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Migraine WITH aura = UKMEC 4 (absolute contraindication) for oestrogen-containing contraception. Increased stroke risk. Offer progestogen-only methods.", "red_flag_negative": ""},
                    {"id": "con_vte_personal", "type": "toggle", "label": "Personal History of DVT/PE?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Personal VTE = UKMEC 4 for CHC. Absolute contraindication to oestrogen.", "red_flag_negative": ""},
                    {"id": "con_vte_family", "type": "toggle", "label": "Family History VTE (1st Degree Relative <45)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx VTE <45 = UKMEC 3 for CHC. Consider thrombophilia screen before prescribing oestrogen.", "red_flag_negative": ""},
                    {"id": "con_breast_cancer", "type": "toggle", "label": "Personal History of Breast Cancer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Current breast cancer = UKMEC 4 for all hormonal contraception. Past breast cancer (≥5 years) = UKMEC 3.", "red_flag_negative": ""},
                    {"id": "con_diabetes", "type": "toggle", "label": "Diabetes with Complications? (Nephropathy, retinopathy, neuropathy)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Diabetes with complications = UKMEC 3/4 for CHC.", "red_flag_negative": ""},
                    {"id": "con_liver_disease", "type": "toggle", "label": "Active Liver Disease / Cirrhosis?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe liver disease = UKMEC 4 for CHC.", "red_flag_negative": ""},
                    {"id": "con_sle", "type": "toggle", "label": "SLE (Systemic Lupus Erythematosus)?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: SLE with positive antiphospholipid antibodies = UKMEC 4 for CHC.", "red_flag_negative": ""},
                    {"id": "con_hypertension_history", "type": "toggle", "label": "History of Hypertension?", "required": False}
                ]
            },
            {
                "title": "Sexual Health",
                "section_type": "history",
                "questions": [
                    {"id": "con_new_partner", "type": "toggle", "label": "New or Multiple Partners Since Last Review?", "required": True},
                    {"id": "con_sti_risk", "type": "toggle", "label": "STI Risk Assessment Needed?", "required": False},
                    {"id": "con_chlamydia_screen", "type": "toggle", "label": "Chlamydia Screening Offered? (<25 years or high risk)", "required": False},
                    {"id": "con_smear", "type": "single_select", "label": "Cervical Screening Status", "required": True, "options": ["Up to date", "Overdue - advised", "Not applicable", "Declined"]}
                ]
            },
            {
                "title": "Reproductive Plans",
                "section_type": "history",
                "questions": [
                    {"id": "con_pregnancy_wish", "type": "single_select", "label": "Pregnancy Plans", "required": True, "options": ["No pregnancy planned", "Considering pregnancy within 1 year", "Actively trying to conceive", "Unsure"]},
                    {"id": "con_breastfeeding", "type": "toggle", "label": "Currently Breastfeeding?", "required": False},
                    {"id": "con_postpartum", "type": "toggle", "label": "Postpartum (<6 weeks)?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: <6 weeks postpartum = UKMEC 4 for CHC (VTE risk). Progestogen-only methods safe from birth.", "red_flag_negative": ""},
                    {"id": "con_postpartum_chc", "type": "toggle", "label": "Postpartum 6 Weeks to 6 Months? (CHC UKMEC 2-3)", "required": False}
                ]
            },
            {
                "title": "LARC Discussion",
                "section_type": "history",
                "questions": [
                    {"id": "con_larc_discussed", "type": "toggle", "label": "LARC Discussed? (Coil, implant - best practice to mention at every review)", "required": True},
                    {"id": "con_larc_interest", "type": "single_select", "label": "Interest in LARC", "required": False, "options": ["Interested - wants referral/fitting", "Considering - wants more information", "Not interested currently", "Already using LARC"]},
                    {"id": "con_larc_type", "type": "multi_select", "label": "LARC Options Discussed", "required": False, "options": ["Copper Coil (10 years, non-hormonal)", "Mirena IUS (5-8 years, reduces bleeding)", "Jaydess IUS (3 years)", "Implant (3 years)", "Depo-Provera (3-monthly injection)"]}
                ]
            },
            {
                "title": "Red Flags - Must Ask",
                "section_type": "history",
                "questions": [
                    {"id": "con_unscheduled_bleeding", "type": "toggle", "label": "Unscheduled/Unexpected Vaginal Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unscheduled bleeding - exclude pregnancy, infection, missed pills, drug interactions. If persistent >3-6 months on CHC or new on POP, investigate pelvic pathology.", "red_flag_negative": ""},
                    {"id": "con_leg_pain_swelling", "type": "toggle", "label": "Leg Pain/Swelling? (DVT)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Possible DVT - unilateral leg swelling, pain, warmth, erythema. Stop CHC immediately. Refer for same-day assessment.", "red_flag_negative": ""},
                    {"id": "con_chest_pain_sob", "type": "toggle", "label": "Chest Pain / Breathlessness? (PE)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Possible PE - pleuritic chest pain, sudden breathlessness, haemoptysis. Stop CHC immediately. Emergency assessment.", "red_flag_negative": ""},
                    {"id": "con_severe_headache", "type": "toggle", "label": "Severe Headache / Visual Disturbance?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe headache with visual disturbance - possible cerebral vein thrombosis or stroke. Stop CHC immediately. Emergency assessment.", "red_flag_negative": ""},
                    {"id": "con_breast_lumps", "type": "toggle", "label": "New Breast Lumps / Changes?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: New breast lump - examine and refer breast clinic if indicated.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment & UKMEC Classification",
                "section_type": "assessment",
                "differentials": [
                    "UKMEC 1 - No restriction on method",
                    "UKMEC 2 - Benefits generally outweigh risks",
                    "UKMEC 3 - Risks generally outweigh benefits (requires expert judgement)",
                    "UKMEC 4 - Unacceptable health risk (DO NOT USE)"
                ],
                "questions": [
                    {"id": "con_ukmec_chc", "type": "single_select", "label": "UKMEC Classification for CHC (Combined Hormonal Contraception)", "required": True, "options": ["UKMEC 1 - Safe to prescribe", "UKMEC 2 - Safe, benefits outweigh risks", "UKMEC 3 - Caution, risks outweigh benefits", "UKMEC 4 - DO NOT USE", "Not applicable (not using CHC)"]},
                    {"id": "con_ukmec_pop", "type": "single_select", "label": "UKMEC for Progestogen-Only Methods", "required": False, "options": ["UKMEC 1 - Safe to prescribe", "UKMEC 2 - Safe", "UKMEC 3 - Caution", "UKMEC 4 - DO NOT USE", "Not applicable"]},
                    {"id": "con_ukmec_detail", "type": "textarea", "label": "UKMEC Justification", "required": True, "placeholder": "e.g., UKMEC 1 for COCP - age 28, BP 118/76, BMI 26, non-smoker, no migraines, no VTE history."}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Switching methods: Follow 7-day rule - if switching from POP to CHC, use additional contraception for 7 days. If switching from CHC to POP, start immediately with no break and use additional contraception for 2 days (traditional POP) or no additional if desogestrel POP. Missed pill rules: 1 pill missed (<24h late) - take immediately, no extra precautions. 2+ pills missed (≥48h) - take most recent pill, use condoms for 7 days, consider emergency contraception if UPSI in pill-free interval. When to seek urgent help: leg pain/swelling, chest pain/breathlessness, severe headache/visual disturbance, new breast lump. Return if: unscheduled bleeding persists >3 months, new side effects, considering pregnancy, or method change desired.",
                "questions": [
                    {"id": "con_plan_decision", "type": "single_select", "label": "Plan", "required": True, "options": ["Continue same method", "Switch method", "Stop method (planning pregnancy)", "Stop method (other reason)", "New prescription - first time", "Add additional method"]},
                    {"id": "con_new_method", "type": "single_select", "label": "New Method (if switching/starting)", "required": False, "options": ["None - continuing same", "COCP (specify in notes)", "POP (specify in notes)", "Implant", "IUS", "Copper Coil", "Depo-Provera", "Patch", "Ring", "Barrier methods only"]},
                    {"id": "con_prescription", "type": "text", "label": "Prescription Issued + Duration", "required": True, "placeholder": "e.g., Microgynon 30 ED, 6-month supply"},
                    {"id": "con_safety_advice", "type": "toggle", "label": "Safety-Net Advice Given? (7-day rule, missed pill rules, red flags, when to seek help)", "required": True},
                    {"id": "con_larc_referral", "type": "toggle", "label": "LARC Fitting Referral Made?", "required": False},
                    {"id": "con_followup_value", "type": "number", "label": "Next Review in (months)", "required": True, "placeholder": "e.g., 6"},
                    {"id": "con_followup_note", "type": "textarea", "label": "Follow-up Notes", "required": False, "placeholder": "e.g., Routine review in 6 months. Earlier if side effects, bleeding concerns, or considering pregnancy."}
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
    seed_contraception_review()