from app.database import SessionLocal
from app.models import User, Template, Category

def seed_cocp():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Combined Oral Contraceptive Pill (COCP) - UKMEC Assessment",
        "description": "UKMEC-based COCP consultation covering contraindications (MEC 3/4), pill-free interval options, missed pill rules, and formulation choices.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "UKMEC Screening - Contraindications & Cautions",
                "section_type": "history",
                "questions": [
                    {"id": "cocp_dvt_pe", "type": "toggle", "label": "Previous DVT/PE? (MEC 4 - ABSOLUTE Contraindication)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: MEC 4 = COCP absolutely contraindicated. Offer progestogen-only or LARC.", "red_flag_negative": ""},
                    {"id": "cocp_breast_ca", "type": "toggle", "label": "Previous Breast Cancer? (MEC 4 - ABSOLUTE Contraindication)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: MEC 4 = COCP contraindicated.", "red_flag_negative": ""},
                    {"id": "cocp_migraine_aura", "type": "toggle", "label": "Migraine WITH Aura? (Any Age - MEC 4 - ABSOLUTE Contraindication)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Migraine with aura = MEC 4. COCP contraindicated. Progestogen-only or LARC.", "red_flag_negative": ""},
                    {"id": "cocp_migraine_no_aura_over35", "type": "toggle", "label": "Migraine WITHOUT Aura + Age ≥35 Continuing COCP? (MEC 3)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: MEC 3 = risks generally outweigh benefits. Discuss alternatives.", "red_flag_negative": ""},
                    {"id": "cocp_fh_vte", "type": "toggle", "label": "Family History VTE - 1st Degree Relative <45 Years? (MEC 3)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: MEC 3 = consider thrombophilia screen before prescribing.", "red_flag_negative": ""},
                    {"id": "cocp_smoking_age", "type": "toggle", "label": "Age >35 + Smoking (Even 1/Day) or Stopped <1 Year? (MEC 3/4)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >35 + smoking = MEC 3/4 depending on amount. COCP may be unsuitable.", "red_flag_negative": ""},
                    {"id": "cocp_other_mec", "type": "multi_select", "label": "Other UKMEC Considerations", "required": True, "options": ["Gallbladder Disease (MEC 3)", "BP ≥140/90 (MEC 3)", "BMI ≥35 (MEC 3)", "Diabetes with Complications", "Liver Disease", "Immobility", "On Antihypertensives", "None"]}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "cocp_preference", "type": "single_select", "label": "Contraceptive Preference", "required": True, "options": ["COCP (Pill)", "Patch (Evra)", "Ring (NuvaRing)", "LARC (Coil/Implant) - Refer", "Undecided"]},
                    {"id": "cocp_compliance", "type": "toggle", "label": "Taking Daily, No Missed Pills? (Current/Previous Method)", "required": True},
                    {"id": "cocp_lmp", "type": "text", "label": "LMP / Cycle Regularity & Duration", "required": True, "placeholder": "e.g., 2 weeks ago, regular 28-day cycle, 5 days"},
                    {"id": "cocp_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Non-Smoker", "Ex-Smoker >1 Year", "Current Smoker / Stopped <1 Year"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "cocp_bp", "type": "text", "label": "Blood Pressure (mmHg) - MEC 3 if ≥140/90", "required": True, "placeholder": "e.g., 118/76", "is_red_flag": True, "red_flag_positive": "RED FLAG: BP ≥140/90 = MEC 3. Treat BP before considering COCP.", "red_flag_negative": ""},
                    {"id": "cocp_bmi", "type": "number", "label": "BMI (kg/m²) - MEC 3 if ≥35", "required": True, "placeholder": "e.g., 24", "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI ≥35 = MEC 3. BMI >30 + additional risk factor = assess individually.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Patient Education",
                "section_type": "plan",
                "questions": [
                    {"id": "cocp_mechanism", "type": "toggle", "label": "Mechanism Explained? (Inhibits Ovulation, Thickens Cervical Mucus, Inhibits Implantation)", "required": False},
                    {"id": "cocp_risks", "type": "toggle", "label": "Risks Explained? (Small Increased Risk: Breast Ca, Cervical Ca, Stroke, DVT)", "required": True},
                    {"id": "cocp_benefits", "type": "toggle", "label": "Benefits Explained? (Decreased Risk: Ovarian + Endometrial Cancer)", "required": False},
                    {"id": "cocp_sti", "type": "toggle", "label": "Does NOT Protect Against STIs Explained?", "required": True},
                    {"id": "cocp_efficacy", "type": "toggle", "label": "Efficacy Explained? (~9 Pregnancies/100 Women-Years Typical Use vs ~1/1000 with LARC)", "required": False},
                    {"id": "cocp_side_effects", "type": "multi_select", "label": "Side Effects Counselled", "required": True, "options": ["Breakthrough Bleeding", "Weight Gain", "Mood Changes", "Skin Changes", "Nausea", "Headaches", "Breast Tenderness"]},
                    {"id": "cocp_missed_pill", "type": "toggle", "label": "Missed Pill Rules Explained?", "required": True},
                    {"id": "cocp_vte_warning", "type": "toggle", "label": "Return Immediately if Chest Pain, SOB, or Calf Swelling? (VTE/PE Red Flags)", "required": True}
                ]
            },
            {
                "title": "Pill-Free Interval & Regimen Options",
                "section_type": "plan",
                "questions": [
                    {"id": "cocp_regimen", "type": "single_select", "label": "Regimen Choice (4-Day Break Recommended Over Traditional 7-Day - Unlicensed but FSRH Supported)", "required": True, "options": ["Standard Monthly: 21 Days COCP → 4-Day Break (Monthly Bleed)", "Tricycling: 63 Days (3 Packs) Continuously → 4-Day Break (Less Frequent Bleeding)", "Continuous/Extended: 365 Days (Start 30mcg → Switch 20mcg to Minimise BTB) - Minimal Bleed", "Licensed Alternative (Yaz/Zoely): 24 Active + 4-Day Break (Monthly Bleed, More Expensive)"]},
                    {"id": "cocp_pill_choice", "type": "single_select", "label": "Pill Formulation", "required": False, "options": ["Ovreena (Same as Ovranette) - 21 Days → 4-Day Break", "Mercilon (20mcg) / Marviol (30mcg)", "Cilique (35mcg) - GMS (Replaced Cilest)", "Yasmin / Elvina (Anti-Androgenic)", "Yasminelle / Elvinette", "Logynon (Triphasic)", "Qlaira (Multiphasic)"]},
                    {"id": "cocp_script_duration", "type": "single_select", "label": "Script Duration", "required": False, "options": ["6-Month Script (Standard Monthly)", "9 Packs / 6 Months (Tricycling)", "Not Applicable - Other Method Chosen"]}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: chest pain, shortness of breath, or calf swelling (VTE/PE red flags). Missed pill rules: 1 pill missed (<24h late) = take immediately, no extra precautions. 2+ pills missed (≥48h) = take most recent pill, use condoms for 7 days, consider emergency contraception if UPSI in pill-free interval. 4-day pill-free interval now recommended (FSRH) over traditional 7-day break (unlicensed use). If migraine with aura develops on COCP = stop immediately + switch to progestogen-only/LARC. COCP does NOT protect against STIs.",
                "questions": [
                    {"id": "cocp_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Suitable for COCP - No MEC 3/4 Contraindications", "MEC 3 Present - Discuss Risks/Benefits", "MEC 4 Present - COCP CONTRAINDICATED - Offer Alternative", "Progestogen-Only / LARC Preferred"]},
                    {"id": "cocp_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Routine review in 6 months, sooner if side effects/concerns"}
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
    seed_cocp()