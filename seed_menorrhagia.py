from app.database import SessionLocal
from app.models import User, Template, Category

def seed_menorrhagia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Menorrhagia / Heavy Menstrual Bleeding",
        "description": "Focused assessment for heavy menstrual bleeding including key history, examination, investigations, and management options.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                   
                    {"id": "men_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 35"},
                    {"id": "men_age_menarche", "type": "number", "label": "Age at Menarche", "required": False, "placeholder": "e.g., 14"}
                ]
            },
            {
                "title": "Bleeding Pattern",
                "section_type": "history",
                "questions": [
                    {"id": "men_cycle_length", "type": "number", "label": "Cycle Length (days)", "required": True, "placeholder": "e.g., 28"},
                    {"id": "men_cycle_regularity", "type": "single_select", "label": "Cycle Regularity", "required": True, "options": ["Regular", "Irregular", "Variable"]},
                    {"id": "men_bleeding_days", "type": "number", "label": "Duration of Bleeding (days)", "required": True, "placeholder": "e.g., 8"},
                    {"id": "men_pad_use", "type": "text", "label": "Sanitary Protection Use", "required": True, "placeholder": "e.g., 2 pads at a time, 8 pads/day, soaked through"},
                    {"id": "men_flooding", "type": "toggle", "label": "Flooding?", "required": True},
                    {"id": "men_clots", "type": "toggle", "label": "Passing Clots?", "required": False},
                    {"id": "men_clot_size", "type": "text", "label": "Clot Size", "required": False, "placeholder": "e.g., Size of 2 euro coin"},
                    {"id": "men_change_recent", "type": "toggle", "label": "Change from Usual Pattern Recently?", "required": True},
                    {"id": "men_change_duration", "type": "text", "label": "Duration of Change", "required": False, "placeholder": "e.g., Last 6 months - progressively heavier"}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "men_pelvic_pain", "type": "toggle", "label": "Pelvic Pain / Pressure?", "required": False},
                    {"id": "men_dysmenorrhoea", "type": "toggle", "label": "Pain During Periods (Dysmenorrhoea)?", "required": False},
                    {"id": "men_dyspareunia", "type": "toggle", "label": "Deep Dyspareunia (Pain During Intercourse)?", "required": False},
                    {"id": "men_pcb", "type": "toggle", "label": "Postcoital Bleeding (PCB)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postcoital bleeding requires speculum examination and cervical assessment. Consider 2WW referral.", "red_flag_negative": "No PCB."},
                    {"id": "men_imb", "type": "toggle", "label": "Intermenstrual Bleeding (IMB)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: IMB requires investigation for endometrial pathology. Consider pelvic USS and endometrial biopsy if >45.", "red_flag_negative": "No IMB."},
                    {"id": "men_pv_discharge", "type": "toggle", "label": "Abnormal PV Discharge?", "required": False},
                    {"id": "men_sob_fatigue", "type": "toggle", "label": "SOB / Fatigue? (Anaemia symptoms)", "required": True},
                    {"id": "men_thyroid_symptoms", "type": "toggle", "label": "Weight Change / Temperature Intolerance? (Thyroid)", "required": False},
                    {"id": "men_hot_flushes", "type": "toggle", "label": "Hot Flushes / Night Sweats? (Perimenopause)", "required": False},
                    {"id": "men_social_impact", "type": "toggle", "label": "Impacting on Social Activity / Work?", "required": True}
                ]
            },
            {
                "title": "Red Flags - Bleeding Disorders & Malignancy",
                "section_type": "history",
                "questions": [
                    {"id": "men_bleeding_disorder", "type": "multi_select", "label": "Personal/Family History of Bleeding?", "required": True, "options": ["Postpartum haemorrhage", "Easy bruising", "Epistaxis", "Gum bleeding", "Prolonged bleeding after dental extraction", "Family history bleeding disorder", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Positive bleeding history may indicate coagulopathy (e.g., vWD). Check coagulation screen.", "red_flag_negative": ""},
                    {"id": "men_age_redflag", "type": "toggle", "label": "Age >45 with New Heavy Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >45 with new menorrhagia - consider endometrial hyperplasia/cancer. Needs pelvic USS and endometrial biopsy.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Key History",
                "section_type": "history",
                "questions": [
                    {"id": "men_pregnancy_test", "type": "single_select", "label": "Pregnancy Test (β-hCG)", "required": True, "options": ["Negative", "Positive", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Always exclude pregnancy first. May indicate miscarriage or ectopic.", "red_flag_negative": ""},
                    {"id": "men_contraception", "type": "single_select", "label": "Current Contraception", "required": True, "options": ["None", "COCP", "POP", "Implant", "IUS (Mirena/Jaydess)", "Depo-Provera", "Copper coil (can worsen bleeding)"]},
                    {"id": "men_obstetric_history", "type": "text", "label": "Obstetric History (Gravida/Para)", "required": True, "placeholder": "e.g., G0P0 or G2P2"},
                    {"id": "men_smears", "type": "single_select", "label": "Cervical Smear Status", "required": True, "options": ["Up to date", "Overdue", "Never had", "Not applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: If smear overdue, arrange. Abnormal smears require colposcopy.", "red_flag_negative": ""},
                    {"id": "men_meds_anticoag", "type": "toggle", "label": "On Aspirin / Anticoagulants / Antiplatelets?", "required": True},
                    {"id": "men_pmh_relevant", "type": "multi_select", "label": "Relevant PMHx", "required": False, "options": ["PCOS", "Thyroid disease", "Fibroids known", "Endometriosis known", "PID history", "Bleeding disorder", "Obesity", "Diabetes", "DVT/PE (contraindication to TXA)", "None"]},
                    {"id": "men_family_history", "type": "multi_select", "label": "Family History", "required": False, "options": ["Bleeding disorder", "Endometrial cancer", "Ovarian cancer", "Breast cancer", "Colorectal cancer (Lynch syndrome)", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "men_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 28", "is_red_flag": True, "red_flag_positive": "RED FLAG: Raised BMI increases risk of anovulatory cycles, endometrial hyperplasia, and malignancy.", "red_flag_negative": ""},
                    {"id": "men_conjunctival_pallor", "type": "toggle", "label": "Conjunctival Pallor? (Anaemia)", "required": False},
                    {"id": "men_abdominal_exam", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Soft, non-tender, no masses", "Mass palpable (fibroids)", "Tenderness", "Distension"]},
                    {"id": "men_pelvic_exam", "type": "toggle", "label": "Pelvic/Speculum Examination Planned?", "required": True},
                    {"id": "men_pelvic_plan", "type": "textarea", "label": "Pelvic Examination Plan", "required": False, "placeholder": "e.g., Book with practice nurse for speculum exam: assess cervix, uterine size/shape, adnexal masses. Swabs for chlamydia and gonorrhoea."}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Dysfunctional Uterine Bleeding / Anovulatory Cycles",
                    "Uterine Fibroids (Leiomyomas)",
                    "Endometriosis / Adenomyosis",
                    "PCOS",
                    "Hypothyroidism",
                    "Coagulation Disorder (e.g., von Willebrand Disease)",
                    "Endometrial Hyperplasia",
                    "Endometrial Cancer (especially if >45 or red flags)",
                    "Pelvic Inflammatory Disease (PID)",
                    "Contraceptive-Related (Copper coil)",
                    "Ovarian Pathology",
                    "Perimenopause"
                ],
                "questions": [
                    {"id": "men_fbc", "type": "number", "label": "Hb (g/dL)", "required": False, "placeholder": "e.g., 10.2 (NR: 11.5-16.0)"},
                    {"id": "men_ferritin", "type": "number", "label": "Ferritin (µg/L)", "required": False, "placeholder": "e.g., 8 (NR: 30-400)"},
                    {"id": "men_tsh", "type": "number", "label": "TSH (mIU/L)", "required": False, "placeholder": "e.g., 2.1 (NR: 0.4-4.0)"},
                    {"id": "men_prolactin", "type": "number", "label": "Prolactin (mIU/L)", "required": False, "placeholder": "e.g., 320 (NR: 100-500)"},
                    {"id": "men_bloods_ordered", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "Ferritin/Iron Studies", "TFTs", "Prolactin", "Renal + Liver Function", "Coagulation Screen", "ESR/CRP (if PID suspected)", "FSH (if perimenopausal)", "CA125 (if ovarian mass suspected)", "None yet"]},
                    {"id": "men_swabs", "type": "toggle", "label": "Swabs for Chlamydia/Gonorrhoea?", "required": False},
                    {"id": "men_imaging", "type": "single_select", "label": "Pelvic Ultrasound", "required": False, "options": ["Requested", "Not required", "Pending", "Result: Normal", "Result: Fibroids", "Result: Ovarian cyst/mass", "Result: Thickened endometrium"]},
                    {"id": "men_endometrial_biopsy", "type": "toggle", "label": "Endometrial Biopsy Indicated? (>45, IMB, PCB, risk factors)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Endometrial biopsy indicated if >45 with persistent menorrhagia, IMB, PCB, or risk factors for endometrial cancer (obesity, diabetes, PCOS, Lynch syndrome).", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: bleeding becomes heavier with large clots, dizziness/chest pain/SOB (severe anaemia), new PCB or IMB, severe pelvic pain. If tranexamic acid prescribed - STOP immediately if any signs of DVT (calf pain/swelling, breathlessness, chest pain). If IUS (Mirena) fitted - irregular bleeding common for first 3-6 months, reassure. Complete menstrual diary for review. Ensure iron supplementation if anaemic - Galfer 1 tablet OD on empty stomach, avoid tea/coffee around dose. If bleeding not improving within 3 months of treatment - review and consider referral.",
                "questions": [
                    {"id": "men_tranexamic_acid", "type": "toggle", "label": "Tranexamic Acid (Cyklokapron) 1g TDS?", "required": False},
                    {"id": "men_txa_contraindication", "type": "toggle", "label": "Personal/Family History of DVT/PE? (Contraindication to TXA)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: DVT/PE history contraindicates tranexamic acid. Use alternative treatment.", "red_flag_negative": "No DVT/PE history - TXA safe to prescribe."},
                    {"id": "men_mefenamic_acid", "type": "toggle", "label": "Mefenamic Acid 500mg TDS? (NSAID - reduces bleeding + pain)", "required": False},
                    {"id": "men_mirena", "type": "toggle", "label": "Consider Mirena IUS? (First-line for menorrhagia)", "required": False},
                    {"id": "men_cocp", "type": "toggle", "label": "Continuous COCP? (Break every 4-6 months, cover bleed with TXA + mefenamic acid)", "required": False},
                    {"id": "men_norethisterone", "type": "toggle", "label": "Norethisterone 15mg Day 5-26? (Luteal phase progestogen)", "required": False},
                    {"id": "men_iron", "type": "single_select", "label": "Iron Replacement", "required": False, "options": ["None", "Galfer 1 tablet OD", "Galfer FA 1 tablet OD", "Ferrograd 1 tablet OD"]},
                    {"id": "men_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None required", "Gynaecology - routine", "Gynaecology - urgent (suspected cancer)", "Haematology (coagulopathy)", "Endocrinology"]},
                    {"id": "men_menstrual_diary", "type": "toggle", "label": "Menstrual Diary Advised?", "required": False}
                ]
            },
            {
                "title": "Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "men_followup_value", "type": "number", "label": "Follow-up in (Number)", "required": True, "placeholder": "e.g., 3"},
                    {"id": "men_followup_unit", "type": "single_select", "label": "Follow-up Unit", "required": True, "options": ["weeks", "months"]}
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
    seed_menorrhagia()