from app.database import SessionLocal
from app.models import User, Template, Category

def seed_noac_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "NOAC / CDM Review",
        "description": "Structured NOAC monitoring review covering dose appropriateness, renal function (CrCl via Cockcroft-Gault), compliance, drug interactions, and patient safety.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Patient Profile & Indication",
                "section_type": "history",
                "questions": [
                    {"id": "noacr_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 76"},
                    {"id": "noacr_indication", "type": "single_select", "label": "Indication for NOAC", "required": True, "options": ["Non-Valvular Atrial Fibrillation (NVAF)", "DVT/PE Treatment", "DVT/PE Prophylaxis"]},
                    {"id": "noacr_drug", "type": "single_select", "label": "Current NOAC", "required": True, "options": ["Apixaban (Eliquis)", "Rivaroxaban (Xarelto)", "Edoxaban (Lixiana)", "Dabigatran (Pradaxa)"]},
                    {"id": "noacr_dose", "type": "text", "label": "Current Dose (mg) + Frequency", "required": True, "placeholder": "e.g., Apixaban 5mg BD"}
                ]
            },
            {
                "title": "Adherence & Missed Dose Rules",
                "section_type": "history",
                "questions": [
                    {"id": "noacr_missed_doses", "type": "single_select", "label": "Missed Doses in Past Month", "required": True, "options": ["None", "1-2 doses", "Frequent (>2)", "Uncertain"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Frequent missed doses = significant stroke risk. NOAC half-life ~12h. Discontinuation increases stroke risk 2-3 fold. Re-educate.", "red_flag_negative": ""},
                    {"id": "noacr_od_rule", "type": "toggle", "label": "Once Daily Rule Understood? (Take up to 12h late; if >12h skip + take next)", "required": False},
                    {"id": "noacr_bd_rule", "type": "toggle", "label": "Twice Daily Rule Understood? (Take up to 6h late; if >6h skip + take next)", "required": False},
                    {"id": "noacr_compliance_counselling", "type": "toggle", "label": "Short Half-Life + Stroke Risk Counselling Given?", "required": True}
                ]
            },
            {
                "title": "Bleeding & Side Effect Screening",
                "section_type": "history",
                "questions": [
                    {"id": "noacr_bleeding", "type": "multi_select", "label": "Bleeding Symptoms", "required": True, "options": ["Epistaxis", "Gingival bleeding", "Haematuria", "Melaena", "Easy bruising", "Heavy menses", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Active bleeding = urgent assessment. Check Hb, review NOAC dose, consider GI referral if melaena.", "red_flag_negative": ""},
                    {"id": "noacr_antiplatelets", "type": "toggle", "label": "On Antiplatelets? (Aspirin, Clopidogrel)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Antiplatelet + NOAC = increased bleeding risk. Review indication for antiplatelet.", "red_flag_negative": ""},
                    {"id": "noacr_nsaids", "type": "toggle", "label": "On NSAIDs?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: NSAIDs + NOAC = significantly increased GI bleeding risk. Stop NSAIDs or add PPI.", "red_flag_negative": ""},
                    {"id": "noacr_ssri_snri", "type": "toggle", "label": "On SSRI / SNRI?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: SSRIs/SNRIs increase bleeding risk with NOAC. Review indication.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Drug Interactions - CYP3A4 / P-gp",
                "section_type": "history",
                "questions": [
                    {"id": "noacr_pgp_inhibitors", "type": "multi_select", "label": "P-gp / CYP3A4 Inhibitors", "required": True, "options": ["Ketoconazole / Itraconazole (CONTRAINDICATED)", "HIV Protease Inhibitors (CONTRAINDICATED)", "Amiodarone (caution)", "Clarithromycin (caution)", "Verapamil (Dabigatran dose reduction)", "Ticagrelor (caution)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Strong CYP3A4/P-gp inhibitors = contraindicated or need dose adjustment.", "red_flag_negative": ""},
                    {"id": "noacr_pgp_inducers", "type": "multi_select", "label": "P-gp / CYP3A4 Inducers", "required": True, "options": ["Carbamazepine (avoid)", "Rifampicin (avoid)", "Phenytoin (avoid)", "St John's Wort (avoid)", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Strong inducers reduce NOAC levels = reduced efficacy. Avoid or choose alternative.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Renal Function & Weight (CrCl via Cockcroft-Gault)",
                "section_type": "examination",
                "questions": [
                    {"id": "noacr_weight", "type": "number", "label": "Weight (kg) - MANDATORY", "required": True, "placeholder": "e.g., 72", "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight MUST be recorded at every review. Required for Cockcroft-Gault + Apixaban/Edoxaban dose criteria.", "red_flag_negative": ""},
                    {"id": "noacr_creatinine", "type": "number", "label": "Serum Creatinine (µmol/L)", "required": True, "placeholder": "e.g., 105"},
                    {"id": "noacr_crcl", "type": "number", "label": "Calculated CrCl - Cockcroft-Gault (mL/min)", "required": True, "placeholder": "e.g., 52", "is_red_flag": True, "red_flag_positive": "RED FLAG: CrCl MUST be used for NOAC dosing - eGFR CANNOT be used. CrCl <50 = dose adjustment needed.", "red_flag_negative": ""},
                    {"id": "noacr_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 132/80"}
                ]
            },
            {
                "title": "Dose Appropriateness Matrix",
                "section_type": "assessment",
                "questions": [
                    {"id": "noacr_apixaban_criteria", "type": "multi_select", "label": "Apixaban Reduction Criteria (need ≥2)", "required": False, "options": ["Age ≥80", "Weight ≤60kg", "Creatinine ≥133 µmol/L", "None - standard dose 5mg BD", "Not on Apixaban"]},
                    {"id": "noacr_rivaroxaban_criteria", "type": "toggle", "label": "Rivaroxaban: CrCl 15-49? → Reduce to 15mg OD", "required": False},
                    {"id": "noacr_edoxaban_criteria", "type": "multi_select", "label": "Edoxaban Reduction Criteria (need ANY 1)", "required": False, "options": ["CrCl 15-49", "Weight ≤60kg", "Concomitant potent P-gp inhibitor", "None - standard dose 60mg OD", "Not on Edoxaban"]},
                    {"id": "noacr_dabigatran_criteria", "type": "multi_select", "label": "Dabigatran Reduction Criteria", "required": False, "options": ["Age ≥80", "Concomitant Verapamil", "None - standard dose 150mg BD", "Not on Dabigatran"]},
                    {"id": "noacr_dosing_status", "type": "single_select", "label": "Current Dosing Status", "required": True, "options": ["Appropriately Dosed", "Underdosed - ADJUST UP", "Overdosed - ADJUST DOWN"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Incorrect dosing = adjust immediately. Underdosing = stroke risk. Overdosing = bleeding risk.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Monitoring Schedule (EHRA Rule)",
                "section_type": "assessment",
                "questions": [
                    {"id": "noacr_crcl_ge_60", "type": "single_select", "label": "If CrCl ≥60: Monitoring Frequency", "required": False, "options": ["Annual (6-monthly if ≥75 or frail)", "Not applicable"]},
                    {"id": "noacr_crcl_lt_60", "type": "text", "label": "If CrCl <60: Frequency = CrCl ÷ 10 months", "required": False, "placeholder": "e.g., CrCl 40 = every 4 months"},
                    {"id": "noacr_next_bloods", "type": "text", "label": "Next Blood Test Due (FBC, U&E, LFTs)", "required": True, "placeholder": "e.g., 4 months"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: signs of major bleeding (haematuria, dark stools/melaena, spontaneous bruising, severe headache), initiating new interacting medications (especially OTC NSAIDs, St John's Wort, or secondary care antibiotics). Rivaroxaban: MUST take 15mg/20mg with main meal (essential for absorption). Dabigatran: keep capsules in original blister pack (moisture-sensitive). Do NOT use dosette box. Swallow whole with 2 glasses of water upright. Do NOT crush/open/NG tube (bioavailability increases up to 75%). NOAC Patient Alert Card issued/checked. Switching from Warfarin: Rivaroxaban/Apixaban/Edoxaban = start when INR <2.5. Dabigatran = start when INR <2.0. Missed dose: OD = up to 12h late, BD = up to 6h late. Never double dose.",
                "questions": [
                    {"id": "noacr_impression", "type": "single_select", "label": "Impression", "required": True, "options": ["Stable on current regimen", "Dose adjusted (renal/weight)", "Dose adjusted (drug interaction)", "Bleeding concern - needs workup", "Non-adherent - re-educated"]},
                    {"id": "noacr_action", "type": "single_select", "label": "Action", "required": True, "options": ["Continue current dose", "Adjust dose (document new dose)", "Switch NOAC", "Refer GI (bleeding)", "Refer cardiology"]},
                    {"id": "noacr_alert_card", "type": "toggle", "label": "NOAC Alert Card Issued / Checked?", "required": True},
                    {"id": "noacr_rivaroxaban_food", "type": "toggle", "label": "Rivaroxaban: Take With Food Advised?", "required": False},
                    {"id": "noacr_dabigatran_blister", "type": "toggle", "label": "Dabigatran: Keep in Blister + No Crushing Advised?", "required": False},
                    {"id": "noacr_followup", "type": "text", "label": "Next Review", "required": True, "placeholder": "e.g., Annual or per CrCl schedule. Next bloods: date"}
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
    seed_noac_review()