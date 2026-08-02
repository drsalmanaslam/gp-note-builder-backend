from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_emergency_contraception():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Emergency (Post-Coital) Contraception",
        "description": "Timing-based emergency contraception consultation covering LNG-EC, Ulipristal, and Cu-IUD options, weight/BMI thresholds, safeguarding for minors, and ongoing contraception planning.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Timing Gate - Confirm FIRST",
                "section_type": "history",
                "questions": [
                    {"id": "ec_hours_since", "type": "number", "label": "Hours Since UPSI (Unprotected Sexual Intercourse)", "required": True, "placeholder": "e.g., 36 hours"},
                    {"id": "ec_option_gate", "type": "single_select", "label": "Eligible Options by Timing", "required": True, "options": ["<72h: LNG-EC + UPA-EC + Cu-IUD All Options", "72-96h: UPA-EC + Cu-IUD (LNG Off-Label Only)", "96-120h: UPA-EC + Cu-IUD", ">120h: Cu-IUD Only (Up to 5 Days After Earliest Ovulation)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: All options time-limited. Confirm timing before selecting. Decision app: https://ecapp.myclinic365.com/", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ec_episodes", "type": "number", "label": "Number of UPSI Episodes Since LMP", "required": True, "placeholder": "e.g., 1"},
                    {"id": "ec_partner", "type": "single_select", "label": "Regular or New Partner?", "required": True, "options": ["Regular Partner", "New Partner"]},
                    {"id": "ec_consensual", "type": "toggle", "label": "Consensual? (If NO = Safeguarding Referral)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Non-consensual = safeguarding referral + sexual assault services.", "red_flag_negative": ""},
                    {"id": "ec_usual_method", "type": "single_select", "label": "Usual Contraception Method", "required": True, "options": ["None", "COCP", "POP", "Implant", "IUS/IUD", "Depo-Provera", "Barrier (Condoms)"]},
                    {"id": "ec_previous_ec", "type": "toggle", "label": "Previous Emergency Contraception This Cycle?", "required": False},
                    {"id": "ec_lmp", "type": "text", "label": "LMP / Cycle Regularity & Length", "required": True, "placeholder": "e.g., 14 days ago, regular 28-day cycle, 5 days"},
                    {"id": "ec_missed_period", "type": "toggle", "label": "Missed Period? (Rule Out Existing Pregnancy)", "required": True},
                    {"id": "ec_previous_pregnancy", "type": "toggle", "label": "Previous Pregnancy?", "required": False},
                    {"id": "ec_past_history", "type": "multi_select", "label": "Relevant Past History", "required": True, "options": ["Ectopic Pregnancy", "Pelvic Infection", "STIs", "Valvular Heart Disease (IUCD Contraindication)", "None"]},
                    {"id": "ec_current_symptoms", "type": "multi_select", "label": "Current Symptoms Since LMP", "required": True, "options": ["PV Discharge", "PV Bleeding", "Pelvic Pain", "Itch", "Abdominal Pain - RED FLAG (?Ectopic)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abdominal pain + missed period = ?ectopic. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "ec_breastfeeding", "type": "toggle", "label": "Breastfeeding? (Avoid UPA - 7 Days)", "required": True},
                    {"id": "ec_oral_steroids", "type": "toggle", "label": "Current Oral Steroid Use? (Ulipristal Not Suitable)", "required": True},
                    {"id": "ec_hormonal_7d", "type": "toggle", "label": "Hormonal Contraception Taken in Previous 7 Days? (Reduces UPA Efficacy)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: UPA less effective if hormonal contraception taken in last 7 days.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Safeguarding (If Under 18)",
                "section_type": "history",
                "questions": [
                    {"id": "ec_under18_age", "type": "number", "label": "Patient's Age (If Under 18)", "required": False, "placeholder": "e.g., 16"},
                    {"id": "ec_partner_age_sg", "type": "number", "label": "Partner's Age - Assess for Significant Age Gap", "required": False, "placeholder": "e.g., 25"},
                    {"id": "ec_gillick_needed", "type": "toggle", "label": "Patient Under 16? (Complete Gillick Competence / Fraser Guidelines)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ec_hcg", "type": "single_select", "label": "Pregnancy Test (hCG) - MUST Be Negative Before Proceeding", "required": True, "options": ["Negative", "Positive - CANNOT PROCEED WITH EC"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive hCG = already pregnant. EC not indicated. Refer antenatal services.", "red_flag_negative": ""},
                    {"id": "ec_bmi", "type": "number", "label": "BMI (kg/m²) - LNG Less Effective if >26", "required": False, "placeholder": "e.g., 28"},
                    {"id": "ec_weight", "type": "number", "label": "Weight (kg) - LNG Less Effective if >70kg", "required": False, "placeholder": "e.g., 75"},
                    {"id": "ec_weight_flag", "type": "single_select", "label": "Weight/BMI Action", "required": False, "options": ["Weight <70kg / BMI <26: Standard LNG 1.5mg", "Weight >70kg / BMI >26: Double LNG to 3mg OR UPA OR Cu-IUD", "Not Applicable - Not Using LNG"]}
                ]
            },
            {
                "title": "Option Selection",
                "section_type": "plan",
                "questions": [
                    {"id": "ec_option_chosen", "type": "single_select", "label": "Emergency Contraception Option", "required": True, "options": ["Levonorgestrel (LNG-EC) 1.5mg Stat (Up to 96h FSRH, Licensed 72h)", "Levonorgestrel 3mg (Double Dose - Weight >70kg/BMI >26)", "Ulipristal Acetate (UPA-EC) 30mg Stat (Up to 120h, Age >18)", "Copper IUCD (Most Effective - Up to 5 Days After Earliest Ovulation)"]}
                ]
            },
            {
                "title": "Patient Education & Safety Netting",
                "section_type": "plan",
                "safety_netting": "If vomiting occurs within 2 hours of taking tablet: contact practice for replacement dose. May cause nausea - advise anti-emetic if needed. Mechanism: delays ovulation ONLY - does NOT work retrospectively. Does NOT protect against pregnancy from further acts in same cycle - barrier contraception needed until next period. Home high-sensitivity pregnancy test in 2-3 weeks. Return for pregnancy test if period delayed or lighter than usual. Slight increased risk of ectopic pregnancy - return promptly if abdominal pain develops. UPA: avoid breastfeeding for 7 days. Do NOT start/restart hormonal contraception for 5 days after UPA. Use additional barrier contraception for 7 days after. LNG: can start ongoing hormonal contraception same day. Discuss long-term contraception options. STI risk - offer STI screen. Confirm cervical screening up to date.",
                "questions": [
                    {"id": "ec_vomiting_warning", "type": "toggle", "label": "If Vomiting Within 2h = Contact for Replacement Dose?", "required": True},
                    {"id": "ec_pregnancy_test", "type": "toggle", "label": "Home Pregnancy Test in 2-3 Weeks Advised?", "required": True},
                    {"id": "ec_ectopic_warning", "type": "toggle", "label": "Return if Abdominal Pain? (Ectopic Risk)", "required": True},
                    {"id": "ec_barrier_advice", "type": "toggle", "label": "Barrier Contraception Until Next Period Advised?", "required": True},
                    {"id": "ec_upa_instructions", "type": "toggle", "label": "UPA-Specific: No Hormonal Contraception x5 Days, Barrier x7 Days, No Breastfeeding x7 Days?", "required": False},
                    {"id": "ec_sti_offer", "type": "toggle", "label": "STI Screen Offered?", "required": False},
                    {"id": "ec_longterm", "type": "toggle", "label": "Long-Term Contraception Discussed?", "required": True},
                    {"id": "ec_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Emergency Contraception Indicated - Within Timeframe", "Cu-IUD Recommended (Most Effective)", "Not Indicated - Outside Timeframe / Already Pregnant", "Safeguarding Concern - Refer"]},
                    {"id": "ec_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Pregnancy test in 2-3 weeks, contraception review"}
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
    seed_emergency_contraception()