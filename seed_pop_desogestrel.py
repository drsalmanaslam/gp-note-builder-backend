from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_pop_desogestrel():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Progesterone-Only Pill (Desogestrel) - UKMEC",
        "description": "Desogestrel POP consultation covering UKMEC 3 threshold (≥2 risk factors), starting rules, missed pill guidance, expected bleeding patterns, and age-related stopping criteria.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "UKMEC 3 Screening - Count Risk Factors (MEC 3 if ≥2)",
                "section_type": "history",
                "questions": [
                    {"id": "pop_risk_count", "type": "number", "label": "Number of UKMEC Risk Factors Present (MEC 3 if ≥2)", "required": True, "placeholder": "e.g., 1"},
                    {"id": "pop_risk_factors", "type": "multi_select", "label": "UKMEC Risk Factors (MEC 3 if ≥2 Present)", "required": True, "options": ["Multiple CV Risk Factors (Smoking, HTN, Diabetes)", "Ischaemic Heart Disease", "Stroke", "Cardiomyopathy", "Cirrhosis / Liver Cancer", "SLE / RA / Antiphospholipid", "IBD", "Cholestasis / Gallbladder Disease", "Diabetes", "Breast Cancer (Personal/Family)", "Unexplained / Irregular PV Bleeding", "Migraine (With or Without Aura)", "Clotting Disorder / DVT", "Dyslipidaemia", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ≥2 risk factors = MEC 3. Reassess suitability.", "red_flag_negative": ""},
                    {"id": "pop_reason", "type": "single_select", "label": "Reason for Choosing POP Over Other Methods", "required": True, "options": ["COCP Contraindicated (Migraine Aura, VTE, Smoking >35)", "Breastfeeding", "Patient Preference", "Side Effects from COCP", "Other"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "pop_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 118/76"},
                    {"id": "pop_bmi", "type": "number", "label": "BMI (kg/m²) - Same Dose Regardless of Weight/BMI (No Adjustment Needed)", "required": False, "placeholder": "e.g., 28"},
                    {"id": "pop_hcg", "type": "single_select", "label": "Pregnancy Test (hCG) - If Clinically Appropriate", "required": False, "options": ["Negative", "Positive - CANNOT PRESCRIBE", "Not Performed"]}
                ]
            },
            {
                "title": "Starting the Pill & Missed Pill Rules",
                "section_type": "plan",
                "questions": [
                    {"id": "pop_start_timing", "type": "single_select", "label": "Starting Point in Cycle", "required": True, "options": ["Started Before Day 5: No Additional Precautions Needed", "Started After Day 5: Barrier Contraception for 48 Hours Required"]},
                    {"id": "pop_vomiting_rule", "type": "toggle", "label": "Vomiting Within 2h = Take Another Pill ASAP?", "required": True},
                    {"id": "pop_missed_window", "type": "toggle", "label": "Missed Pill Window: 12 Hours (vs 24h for COCP)?", "required": True},
                    {"id": "pop_missed_action", "type": "toggle", "label": "If >1 Pill Missed: Take Only 1 Pill, Continue at Usual Time (May Mean 2 Pills in 1 Day)?", "required": True},
                    {"id": "pop_barrier_after_missed", "type": "toggle", "label": "Additional Contraception for 2 Days After Restarting Following Missed Pill?", "required": True}
                ]
            },
            {
                "title": "Patient Education - Efficacy & Side Effects",
                "section_type": "plan",
                "questions": [
                    {"id": "pop_efficacy", "type": "toggle", "label": "Inhibits Ovulation in 97% Cycles. Typical Use: ~9 Pregnancies/100 Women-Years (vs ~1/1000 LARC)?", "required": True},
                    {"id": "pop_ectopic", "type": "toggle", "label": "If Pregnancy Occurs: ~1 in 10 May Be Ectopic?", "required": False},
                    {"id": "pop_side_effects", "type": "multi_select", "label": "Side Effects Discussed", "required": True, "options": ["Bleeding Pattern Changes", "Mood Changes", "Breast Tenderness", "Nausea", "Headaches"]},
                    {"id": "pop_no_sti", "type": "toggle", "label": "Does NOT Protect Against STIs?", "required": True},
                    {"id": "pop_no_association", "type": "toggle", "label": "No Evidence for Association with CVD, Breast Cancer, Depression, or Weight Change?", "required": False}
                ]
            },
            {
                "title": "Expected Bleeding Pattern (After 12 Months, Over 3-Month Period)",
                "section_type": "plan",
                "questions": [
                    {"id": "pop_bleeding_pattern", "type": "single_select", "label": "Bleeding Pattern Counselling", "required": True, "options": ["Amenorrhoeic or Infrequent Bleeding (~5/10 Women)", "3-5 Bleeding/Spotting Episodes - Regular (~4/10 Women)", ">6 Bleeding/Spotting Episodes - Frequent (~1/10 Women)", "Prolonged Bleeding >14 Days (~2/10 Women - In Addition to Above)", "All Patterns Explained"]}
                ]
            },
            {
                "title": "Age Limit / Stopping Criteria",
                "section_type": "plan",
                "questions": [
                    {"id": "pop_age_limit", "type": "toggle", "label": "Can Be Used Up to Age 55 (Natural Loss of Fertility Assumed)?", "required": False},
                    {"id": "pop_fsh_pathway", "type": "toggle", "label": "If Age >50 + Amenorrhoeic: Check FSH x2, 6 Weeks Apart. If Both >30 IU/L = Ovarian Failure → Continue POP/Barrier 1 More Year → Consider Stopping?", "required": False}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return if: new unexplained PV bleeding, suspected pregnancy, severe abdominal pain (?ectopic), or any concerns. Take at consistent time each day. Desogestrel is safe for overwhelming majority of women. UKMEC 3 only if ≥2 risk factors present. Same dose regardless of weight/BMI. Can be started at any point in cycle. Missed pill window is 12 hours (shorter than COCP). Desogestrel inhibits ovulation in 97% of cycles.",
                "questions": [
                    {"id": "pop_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Suitable for Desogestrel POP - UKMEC Criteria Met", "MEC 3 Threshold Met (≥2 Risk Factors) - Discuss Risks/Benefits", "Not Suitable - Offer Alternative"]},
                    {"id": "pop_prescribing", "type": "single_select", "label": "Prescribing", "required": False, "options": ["Desogestrel 75mcg OD (Azalia/Cerazette) - 6 Month Script", "Desogestrel 75mcg OD - 3 Month Trial", "Not Prescribed"]},
                    {"id": "pop_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Routine review in 6 months, sooner if bleeding concerns"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_pop_desogestrel()