from app.database import SessionLocal
from app.models import User, Template, Category

def seed_galactorrhoea():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Galactorrhoea / Nipple Discharge",
        "description": "Focused assessment for galactorrhoea and nipple discharge including key history, examination, investigations, and management with red flags for breast pathology.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "gal_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 32"}
                ]
            },
            {
                "title": "Discharge Characteristics",
                "section_type": "history",
                "questions": [
                    {"id": "gal_side", "type": "single_select", "label": "Which Breast?", "required": True, "options": ["Right breast", "Left breast", "Both breasts"]},
                    {"id": "gal_colour", "type": "single_select", "label": "Discharge Colour", "required": True, "options": ["Milky/White", "Bloody", "Blood-stained", "Serous (clear/watery)", "Purulent (green/yellow)", "Brown/Green"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bloody or serous discharge requires urgent breast clinic referral (2WW) - possible intraductal papilloma or malignancy. Milky discharge suggests galactorrhoea.", "red_flag_negative": ""},
                    {"id": "gal_blood", "type": "toggle", "label": "Any Blood in Discharge?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bloody discharge - refer breast clinic urgently via Healthmail. Do not delay.", "red_flag_negative": ""},
                    {"id": "gal_pus", "type": "toggle", "label": "Any Pus?", "required": False},
                    {"id": "gal_volume", "type": "text", "label": "Volume of Discharge", "required": False, "placeholder": "e.g., Teaspoonful daily, drops only, stains clothing"},
                    {"id": "gal_spontaneous", "type": "toggle", "label": "Spontaneous or Only on Expression?", "required": True},
                    {"id": "gal_breast_pain", "type": "toggle", "label": "Breast Pain / Tenderness?", "required": False}
                ]
            },
            {
                "title": "Menstrual & Reproductive History",
                "section_type": "history",
                "questions": [
                    {"id": "gal_pregnancy_test", "type": "single_select", "label": "Pregnancy Test (β-hCG)", "required": True, "options": ["Negative", "Positive", "Not done"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Always exclude pregnancy first.", "red_flag_negative": ""},
                    {"id": "gal_lmp", "type": "text", "label": "Last Menstrual Period", "required": True, "placeholder": "e.g., 1 month ago"},
                    {"id": "gal_periods_regular", "type": "toggle", "label": "Regular Periods?", "required": True},
                    {"id": "gal_period_duration", "type": "number", "label": "Duration of Periods (days)", "required": False, "placeholder": "e.g., 5"},
                    {"id": "gal_periods_absent", "type": "toggle", "label": "Amenorrhoea / Oligomenorrhoea?", "required": False},
                    {"id": "gal_breastfeeding", "type": "toggle", "label": "Breastfeeding or Recent Postpartum?", "required": True},
                    {"id": "gal_obstetric", "type": "text", "label": "Obstetric History (Gravida / Para)", "required": True, "placeholder": "e.g., G0P0"}
                ]
            },
            {
                "title": "Key History - Endocrine & Medications",
                "section_type": "history",
                "questions": [
                    {"id": "gal_headaches", "type": "toggle", "label": "Headaches?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Headaches + galactorrhoea = possible pituitary prolactinoma. Check prolactin and visual fields.", "red_flag_negative": "No headaches."},
                    {"id": "gal_visual_disturbance", "type": "toggle", "label": "Visual Disturbance? (Blurring, peripheral vision loss, bumping into things)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms + galactorrhoea = pituitary macroadenoma compressing optic chiasm. Urgent MRI + endocrinology referral.", "red_flag_negative": "No visual disturbance."},
                    {"id": "gal_thyroid_symptoms", "type": "toggle", "label": "Weight Change / Temperature Intolerance / Fatigue? (Thyroid)", "required": True},
                    {"id": "gal_hirsutism_acne", "type": "toggle", "label": "Hirsutism / Acne / Hair Loss? (PCOS)", "required": False},
                    {"id": "gal_meds_antipsychotics", "type": "toggle", "label": "Taking Antipsychotics? (Risperidone, Haloperidol, Olanzapine)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Antipsychotics are a common cause of drug-induced hyperprolactinaemia. Check prolactin. Discuss with psychiatrist about switching to prolactin-sparing agent (Aripiprazole, Quetiapine).", "red_flag_negative": ""},
                    {"id": "gal_meds_other", "type": "multi_select", "label": "Other Relevant Medications", "required": False, "options": ["Metoclopramide (Maxolon)", "SSRIs", "Combined Oral Contraceptive", "Oestrogen therapy", "Verapamil", "Opioids", "PPIs", "None"]},
                    {"id": "gal_meds_recent_change", "type": "toggle", "label": "Recently Started New Medication?", "required": True},
                    {"id": "gal_family_pituitary", "type": "toggle", "label": "Family History of Pituitary Tumours or MEN1?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "gal_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 124"},
                    {"id": "gal_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 80"},
                    {"id": "gal_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 76"},
                    {"id": "gal_goitre", "type": "toggle", "label": "Goitre Present?", "required": False},
                    {"id": "gal_exophthalmos", "type": "toggle", "label": "Exophthalmos / Eye Signs?", "required": False},
                    {"id": "gal_tremor", "type": "toggle", "label": "Tremor?", "required": False},
                    {"id": "gal_hirsutism_exam", "type": "toggle", "label": "Hirsutism / Acne / Hair Loss? (PCOS)", "required": False},
                    {"id": "gal_breast_lumps", "type": "toggle", "label": "Breast Lumps?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Breast lump with discharge requires urgent breast clinic referral (2WW).", "red_flag_negative": "No breast lumps."},
                    {"id": "gal_peau_dorange", "type": "toggle", "label": "Peau d'Orange / Skin Changes?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Skin changes suggest inflammatory breast cancer. Urgent breast clinic referral.", "red_flag_negative": ""},
                    {"id": "gal_discharge_expressible", "type": "toggle", "label": "Discharge Expressible on Examination?", "required": True},
                    {"id": "gal_nipple_exam", "type": "single_select", "label": "Nipple Examination", "required": False, "options": ["Normal", "Inversion/Retraction", "Eczema/Ulceration (Paget's)", "Discharge from single duct", "Discharge from multiple ducts"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Single duct discharge, nipple inversion, or eczematous changes require breast clinic referral.", "red_flag_negative": ""},
                    {"id": "gal_visual_fields", "type": "single_select", "label": "Visual Fields (Confrontation)", "required": True, "options": ["Intact", "Bitemporal Hemianopia", "Other Deficit", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual field defect = pituitary macroadenoma. Urgent MRI + endocrinology/neurosurgery referral.", "red_flag_negative": "Visual fields intact."}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Physiological Galactorrhoea (Pregnancy, Lactation, Postpartum)",
                    "Hyperprolactinaemia / Prolactinoma",
                    "Drug-Induced (Antipsychotics, Metoclopramide, SSRIs, Oestrogens)",
                    "Primary Hypothyroidism (TRH-driven)",
                    "PCOS",
                    "Intraductal Papilloma",
                    "Duct Ectasia",
                    "Breast Cancer (if bloody/serous unilateral discharge)",
                    "Paget's Disease of the Nipple",
                    "Chest Wall Trauma/Herpes Zoster",
                    "Idiopathic Galactorrhoea",
                    "Pituitary Macroadenoma (Stalk Compression)",
                    "Chronic Kidney Disease",
                    "Liver Disease"
                ],
                "questions": [
                    {"id": "gal_prolactin", "type": "number", "label": "Prolactin (mIU/L)", "required": True, "placeholder": "e.g., 1850 (NR: 100-500)", "is_red_flag": True, "red_flag_positive": "RED FLAG: Prolactin >1000 - repeat fasting morning sample. If persistent, needs MRI pituitary. >5000 strongly suggests prolactinoma.", "red_flag_negative": ""},
                    {"id": "gal_tsh", "type": "number", "label": "TSH (mIU/L)", "required": True, "placeholder": "e.g., 2.1 (NR: 0.4-4.0)"},
                    {"id": "gal_bloods_ordered", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["β-hCG", "Prolactin (fasting, morning)", "TFTs (TSH, Free T4)", "Renal Function (U&E, Creatinine)", "Liver Function Tests", "FSH/LH/Oestradiol", "Testosterone (if PCOS features)", "None yet"]},
                    {"id": "gal_discharge_mcs", "type": "toggle", "label": "Discharge for MC+S Sent?", "required": False},
                    {"id": "gal_cytology", "type": "toggle", "label": "Discharge for Cytology Sent?", "required": False},
                    {"id": "gal_mammogram", "type": "toggle", "label": "Mammogram / Breast Imaging Requested?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Breast imaging indicated for unilateral discharge, bloody/serous discharge, or breast lump. Refer breast clinic.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return in 3 weeks for review with blood results, or sooner if any concerning symptoms. RED FLAGS - return immediately if: discharge becomes bloody, new breast lump develops, new nipple changes (inversion, eczema, ulceration), headaches develop or worsen, visual disturbance (blurring, peripheral vision loss, bumping into things), or any new neurological symptoms. If medication-induced - do not stop psychiatric medications without discussing with prescriber. If breastfeeding or postpartum - likely physiological, reassure. If BLOODY or unilateral serous spontaneous discharge - refer breast clinic via Healthmail urgently.",
                "questions": [
                    {"id": "gal_plan_type", "type": "single_select", "label": "Management Approach", "required": True, "options": ["Reassurance + investigate", "Treat underlying cause", "Medication review/change", "Refer breast clinic (bloody/serous unilateral discharge)", "Refer endocrinology", "Awaiting blood results"]},
                    {"id": "gal_refer_breast", "type": "toggle", "label": "Refer Breast Clinic? (Bloody/serous unilateral spontaneous discharge)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral bloody or spontaneous serous discharge = urgent breast clinic referral via Healthmail.", "red_flag_negative": ""},
                    {"id": "gal_refer_endo", "type": "toggle", "label": "Refer Endocrinology? (Elevated prolactin, suspected prolactinoma, visual symptoms)", "required": False},
                    {"id": "gal_stop_medication", "type": "toggle", "label": "Stop/Change Causative Medication? (Discuss with prescriber)", "required": False},
                    {"id": "gal_followup_plan", "type": "text", "label": "Next Review", "required": True, "placeholder": "e.g., 3 weeks with blood results"}
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
    seed_galactorrhoea()