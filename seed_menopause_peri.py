from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_menopause_peri():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Menopausal Symptoms - Perimenopausal (Still Having Periods)",
        "description": "Initial perimenopausal consultation covering clinical diagnosis, HRT safety screening, sequential HRT options, urogenital atrophy treatment, and alternatives to HRT.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Diagnostic Criteria (Clinical - No Routine Bloods)",
                "section_type": "history",
                "questions": [
                    {"id": "menop_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 48"},
                    {"id": "menop_diagnostic", "type": "single_select", "label": "Diagnostic Criteria (Clinical Diagnosis - Bloods Not Required)", "required": True, "options": ["Age <50 + Period Within Last 2 Years = Perimenopausal", "Age ≥50 + Period Within Last Year", "Uncertain - Consider TSH, FBC"]},
                    {"id": "menop_symptoms", "type": "multi_select", "label": "Symptom Screen (Modified Greene Climacteric Scale Available)", "required": True, "options": ["Vasomotor Flushes/Sweats", "Poor Sleep", "Anxiety", "Low Mood", "Cognitive Impairment / Brain Fog", "Muscle/Joint Pain", "Exacerbation of Urinary Incontinence", "Hair/Skin Changes", "Low Libido", "Vaginal Dryness"]},
                    {"id": "menop_severity", "type": "single_select", "label": "Symptom Severity (~10% Severe, ~10% None, Most In Between)", "required": True, "options": ["Mild - Coping Well", "Moderate - Affecting Quality of Life", "Severe - Significant Impact"]}
                ]
            },
            {
                "title": "HRT Safety Screen - Check Before Prescribing",
                "section_type": "history",
                "questions": [
                    {"id": "menop_breast_ca", "type": "toggle", "label": "Personal History Breast Cancer? (Refer Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Personal breast cancer = REFER menopause clinic. Do NOT prescribe HRT in primary care.", "red_flag_negative": ""},
                    {"id": "menop_endometrial_ca", "type": "toggle", "label": "Personal History Endometrial/Ovarian Cancer? (Refer Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Refer menopause clinic.", "red_flag_negative": ""},
                    {"id": "menop_vte_history", "type": "toggle", "label": "Personal History VTE/Angina/CVA/TIA? (Transdermal HRT with Caution - Consider Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: VTE/CVA history = transdermal preferred. Consider menopause clinic.", "red_flag_negative": ""},
                    {"id": "menop_porphyria", "type": "toggle", "label": "Personal History Porphyria? (Refer Menopause Clinic)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Porphyria = refer menopause clinic.", "red_flag_negative": ""},
                    {"id": "menop_endometriosis", "type": "toggle", "label": "Personal History Severe Endometriosis? (Consider Menopause Clinic)", "required": False},
                    {"id": "menop_family_history", "type": "multi_select", "label": "Family History (Less Significant but Consider Menopause Clinic)", "required": True, "options": ["Breast Cancer", "Ovarian Cancer", "Hormone-Provoked VTE", "None"]},
                    {"id": "menop_smoking", "type": "single_select", "label": "Smoking (Transdermal Preferred Over Oral if Smoker)", "required": True, "options": ["Non-Smoker", "Current Smoker - Transdermal Preferred"]},
                    {"id": "menop_liver_enzyme", "type": "toggle", "label": "On Liver Enzyme-Inducing Medication?", "required": False},
                    {"id": "menop_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": False, "options": ["None", "Within Limits", "Excess"]}
                ]
            },
            {
                "title": "Preventative Care & Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "menop_screening", "type": "multi_select", "label": "Cervical Screening + Mammography Up to Date?", "required": True, "options": ["Cervical Screening UTD", "Mammography UTD", "Overdue - Advise", "Not Applicable"]},
                    {"id": "menop_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 124/80"},
                    {"id": "menop_bmi", "type": "number", "label": "BMI (kg/m²) - Not Essential if Transdermal Planned", "required": False, "placeholder": "e.g., 28"},
                    {"id": "menop_breast_exam", "type": "single_select", "label": "Breast Examination (Not Routine - Offer if Symptoms/Reassurance)", "required": False, "options": ["Normal - No Concerns", "Abnormal - Refer Breast Clinic", "Not Performed (No Symptoms)"]}
                ]
            },
            {
                "title": "Patient Education",
                "section_type": "plan",
                "questions": [
                    {"id": "menop_edu_natural", "type": "toggle", "label": "Menopause = Natural Process Where Ovaries Gradually Stop Producing Oestrogen?", "required": False},
                    {"id": "menop_edu_severity", "type": "toggle", "label": "Symptom Severity Varies: ~10% Severe, ~10% None, Most In Between?", "required": False},
                    {"id": "menop_edu_contraception", "type": "toggle", "label": "Contraception: Continue Until Age 55? (If >50 + Amenorrhoeic: FSH x2 >30 = 1 More Year)", "required": True},
                    {"id": "menop_edu_resources", "type": "multi_select", "label": "Patient Resources Given", "required": False, "options": ["HSE South Menopause Leaflet", "www.menopausematters.co.uk", "CBT for Menopausal Symptoms (WHC Factsheet)"]},
                    {"id": "menop_edu_lifestyle", "type": "multi_select", "label": "Lifestyle Advice", "required": False, "options": ["Smoking Cessation", "Reduced Alcohol", "Exercise", "Healthy Diet", "Wear Layers/Loose Clothing", "CBT Proven for Flushes/Sweats"]},
                    {"id": "menop_edu_supplements", "type": "toggle", "label": "Evening Primrose Oil/Vitamins/Supplements - NOT Proven (No Better Than Placebo)?", "required": False}
                ]
            },
            {
                "title": "HRT - Three Main Risks to Explain",
                "section_type": "plan",
                "questions": [
                    {"id": "menop_risk_breast", "type": "toggle", "label": "Breast Cancer: No Increased Risk First 5 Years. Slight Increase Thereafter (Still Less Than Obesity/Moderate Alcohol)?", "required": True},
                    {"id": "menop_risk_vte", "type": "toggle", "label": "Thrombosis: Associated with ORAL Oestrogen. Transdermal NOT Associated with Increased VTE Risk?", "required": True},
                    {"id": "menop_risk_side_effects", "type": "toggle", "label": "Initial Side Effects: Bloating, Breast Tenderness, Headache, Bleeding - Usually Self-Limiting?", "required": True}
                ]
            },
            {
                "title": "Sequential HRT Options (Bleed-Producing - For Perimenopausal)",
                "section_type": "plan",
                "safety_netting": "Review at 3 months after starting, then 6-12 monthly for BP, BMI, symptom review. Expect irregular bleeding initially - should settle. Book review if excessive or persistent. Can stop HRT at any time + return if side effects severe. Sequential regimen for up to 5 years, then transition to continuous HRT. Evidence: https://gpevidence.org/conditions/menopause/. Risk tools: FRAX (Irish-adapted), QRISK3 (qrisk.org/three/). Breast cancer risk pictogram: WHC. Risk tool: bcrisktool.cancer.gov.",
                "questions": [
                    {"id": "menop_hrt_route", "type": "single_select", "label": "HRT Route", "required": False, "options": ["Oral: Femoston 2/10 or 1/10, Novofem, Trisequens (If No VTE Risk Factors)", "Transdermal: Evorel Conti 2 Weeks → Evorel 2 Weeks", "Transdermal: Patch (Evorel/Estradot 50mcg) Twice Weekly + Progesterone", "Transdermal: Oestrogel 2 Pumps / Divigel 1 Sachet / Lenzetto 3 Sprays Daily + Progesterone", "Mirena IUS + Daily Oestrogen", "None - HRT Declined/Contraindicated"]},
                    {"id": "menop_progesterone", "type": "single_select", "label": "Progesterone (If Uterus Present)", "required": False, "options": ["Utrogestan 200mg Nightly 2 Weeks/Month (Oestrogen ≤50mcg)", "Utrogestan 300mg Nightly 2 Weeks/Month (Oestrogen 75-100mcg)", "Duphaston 10-20mg Daily 2 Weeks/Month", "Mirena IUS (5 Years Endometrial Protection)", "Not Required (No Uterus / HRT Not Prescribed)"]},
                    {"id": "menop_urogenital", "type": "single_select", "label": "Urogenital Atrophy Treatment (If Symptoms)", "required": False, "options": ["Vagifem 10mcg Nightly 2 Weeks → Twice Weekly", "Imvaggis Pessary Nightly 2 Weeks → Twice Weekly", "Blissel 50mcg/g Gel Nightly 3 Weeks → Twice Weekly", "Ovestin Cream Daily 4 Weeks → Twice Weekly", "Vaginal Lubricants/Moisturisers (Replens, YES, KY)", "Not Required"]},
                    {"id": "menop_alternatives", "type": "single_select", "label": "Alternatives to HRT (If HRT Declined/Contraindicated)", "required": False, "options": ["Citalopram / Escitalopram", "Fluoxetine", "Venlafaxine", "Fezolinetant", "None - HRT Prescribed"]},
                    {"id": "menop_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Perimenopausal - Starting Sequential HRT", "Perimenopausal - HRT Contraindicated (Alternatives)", "Perimenopausal - Lifestyle + Monitoring Only", "Refer Menopause Clinic"]},
                    {"id": "menop_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 3 months review, then 6-12 monthly. Return if excessive bleeding."}
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
    seed_menopause_peri()