from app.database import SessionLocal
from app.models import User, Template, Category

def seed_hrt_review():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "HRT Review Appointment",
        "description": "Structured HRT review covering symptom response, side effects, examination, risk-benefit counselling, bleeding assessment, and management adjustments.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Situation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "hrt_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 52"},
                    {"id": "hrt_green_scale", "type": "toggle", "label": "Modified Greene Climacteric Scale Completed?", "required": True}
                ]
            },
            {
                "title": "Current HRT Regimen",
                "section_type": "history",
                "questions": [
                    {"id": "hrt_type", "type": "single_select", "label": "HRT Type", "required": True, "options": ["Sequential combined (cyclical)", "Continuous combined", "Oestrogen only (post-hysterectomy)", "Local oestrogen only (vaginal)", "Tibolone"]},
                    {"id": "hrt_oestrogen", "type": "text", "label": "Oestrogen - Drug, Dose, Route", "required": True, "placeholder": "e.g., Estradiol 50mcg patch twice weekly"},
                    {"id": "hrt_progestogen", "type": "text", "label": "Progestogen - Drug, Dose, Route (if combined)", "required": False, "placeholder": "e.g., Utrogestan 200mg nocte days 15-26, or Levonorgestrel IUS"},
                    {"id": "hrt_duration", "type": "text", "label": "Duration on Current Regimen", "required": True, "placeholder": "e.g., 6 months"},
                    {"id": "hrt_lmp", "type": "text", "label": "Last Menstrual Period", "required": True, "placeholder": "e.g., 18 months ago or still cycling"},
                    {"id": "hrt_menopausal_status", "type": "single_select", "label": "Menopausal Status", "required": True, "options": ["Perimenopausal (LMP <1 year, or still cycling)", "Postmenopausal (LMP >1 year)", "Post-hysterectomy", "Premature (<40 years)"]}
                ]
            },
            {
                "title": "Symptom Response",
                "section_type": "history",
                "questions": [
                    {"id": "hrt_response", "type": "single_select", "label": "Symptom Response to HRT", "required": True, "options": ["Good improvement - symptoms well controlled", "Partial improvement - some ongoing symptoms", "No improvement", "Symptoms worse"]},
                    {"id": "hrt_vasomotor_improved", "type": "toggle", "label": "Hot Flushes / Night Sweats Improved?", "required": True},
                    {"id": "hrt_ongoing_symptoms", "type": "multi_select", "label": "Ongoing Symptoms", "required": False, "options": ["Hot flushes", "Night sweats", "Mood changes", "Sleep disturbance", "Vaginal dryness", "Low libido", "Joint pains", "Brain fog", "None - all controlled"]},
                    {"id": "hrt_urogenital", "type": "toggle", "label": "Urogenital Symptoms? (Dryness, dyspareunia, frequency)", "required": False}
                ]
            },
            {
                "title": "Side Effects & Tolerability",
                "section_type": "history",
                "questions": [
                    {"id": "hrt_side_effects", "type": "multi_select", "label": "Side Effects Experienced", "required": True, "options": ["Breast tenderness/enlargement", "Nausea", "Headaches", "Leg cramps", "Fluid retention/bloating", "Mood swings", "Weight gain concern", "Patch adhesion issues", "None - tolerating well"]},
                    {"id": "hrt_side_effect_duration", "type": "text", "label": "Duration of Side Effects", "required": False, "placeholder": "e.g., 4 weeks - may still settle as advised 12 weeks"},
                    {"id": "hrt_pv_bleeding", "type": "single_select", "label": "PV Bleeding Pattern", "required": True, "options": ["Regular withdrawal bleeds (sequential HRT)", "No bleeding (continuous combined HRT)", "Erratic/irregular bleeding (first 3-6 months)", "Heavy bleeding", "Unscheduled/new onset bleeding", "No bleeding"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unscheduled bleeding after 6 months of continuous combined HRT, or new onset bleeding, requires pelvic USS and endometrial assessment.", "red_flag_negative": ""},
                    {"id": "hrt_bleeding_detail", "type": "textarea", "label": "Bleeding Details (if abnormal)", "required": False, "placeholder": "Heavy, erratic, painful, new onset, postcoital..."},
                    {"id": "hrt_compliance", "type": "toggle", "label": "Compliant with Progestogen Component?", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hrt_bp_systolic", "type": "number", "label": "BP Systolic (mmHg)", "required": True, "placeholder": "e.g., 126"},
                    {"id": "hrt_bp_diastolic", "type": "number", "label": "BP Diastolic (mmHg)", "required": True, "placeholder": "e.g., 84"},
                    {"id": "hrt_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 76"},
                    {"id": "hrt_bmi", "type": "number", "label": "BMI (kg/m²)", "required": True, "placeholder": "e.g., 27", "is_red_flag": True, "red_flag_positive": "RED FLAG: BMI >30 - transdermal preparation preferred (reduced VTE risk). BMI >40 - refer menopause clinic.", "red_flag_negative": ""},
                    {"id": "hrt_breast_exam", "type": "toggle", "label": "Breast Examination Indicated?", "required": False},
                    {"id": "hrt_pelvic_exam", "type": "toggle", "label": "Pelvic Examination Indicated? (if abnormal bleeding)", "required": False}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "hrt_tfts", "type": "text", "label": "TFTs (if ongoing vasomotor symptoms)", "required": False, "placeholder": "e.g., TSH 2.1, normal"},
                    {"id": "hrt_hba1c", "type": "text", "label": "HbA1c (if weight/PCOS/risk factors)", "required": False, "placeholder": "e.g., 34 mmol/mol, normal"},
                    {"id": "hrt_pelvic_uss", "type": "toggle", "label": "Pelvic USS Needed? (New/unscheduled bleeding, >6 months erratic)", "required": False},
                    {"id": "hrt_mammogram", "type": "toggle", "label": "Mammogram Up to Date?", "required": True},
                    {"id": "hrt_smear", "type": "toggle", "label": "Cervical Screening Up to Date?", "required": True}
                ]
            },
            {
                "title": "Risk-Benefit Counselling",
                "section_type": "plan",
                "safety_netting": "Return if: new onset or persistent unscheduled PV bleeding (after 6 months on continuous combined HRT), new breast lump or skin changes, severe headaches not responding to transdermal switch, leg swelling/pain or breathlessness (possible DVT/PE). Continue breast awareness and attend screening mammograms. Attend cervical screening. Weight gain common at menopause - diet and exercise important (no RCT evidence HRT causes weight gain). For urogenital symptoms not controlled with systemic HRT: add vaginal oestrogen (Vagifem 10mcg or Imvaggis). Side effect management: breast tenderness usually settles 4-6 weeks, oestrogen side effects may persist up to 12 weeks. Leg cramps - exercise and calf stretches. Headaches - consider transdermal oestrogen. For bleeding problems: heavy/erratic on sequential - double progestogen dose or extend to 21 days. Painful bleeding - change progestogen. Unscheduled bleeding first 6 months of continuous combined - common, no investigation needed unless persistent beyond 6 months or new onset after established amenorrhoea.",
                "questions": [
                    {"id": "hrt_risk_discussed", "type": "toggle", "label": "Risk:Benefit Ratio Discussed?", "required": True},
                    {"id": "hrt_breast_cancer_risk", "type": "toggle", "label": "Breast Cancer Risk Discussed? (No increased risk first 5 years, small increase thereafter - less than obesity or moderate alcohol)", "required": True},
                    {"id": "hrt_fracture_risk", "type": "toggle", "label": "Fracture Risk Discussed? (FRAX tool)", "required": False},
                    {"id": "hrt_qrisk", "type": "toggle", "label": "QRISK3 Cardiovascular Risk Assessed?", "required": False},
                    {"id": "hrt_breast_awareness", "type": "toggle", "label": "Breast Awareness + Screening Encouraged?", "required": True},
                    {"id": "hrt_lowest_dose", "type": "toggle", "label": "Lowest Effective Dose Advised?", "required": True}
                ]
            },
            {
                "title": "Management Adjustments",
                "section_type": "plan",
                "questions": [
                    {"id": "hrt_continue_same", "type": "toggle", "label": "Continue Same HRT Regimen?", "required": True},
                    {"id": "hrt_dose_change", "type": "single_select", "label": "Oestrogen Dose Adjustment", "required": False, "options": ["No change", "Increase dose (ongoing symptoms)", "Decrease dose (side effects)", "Consider higher dose - age <50", "Consider low/ultra-low dose - age >60 or >10 years from LMP"]},
                    {"id": "hrt_progestogen_change", "type": "single_select", "label": "Progestogen Adjustment", "required": False, "options": ["No change", "Double progestogen dose (heavy/erratic bleeding)", "Extend progestogen to 21 days", "Change progestogen type (side effects/bleeding)", "Consider IUS for endometrial protection", "Switch from oral to transdermal"]},
                    {"id": "hrt_route_change", "type": "toggle", "label": "Switch to Transdermal? (Headaches, BMI>30, VTE risk, enzyme inducers)", "required": False},
                    {"id": "hrt_switch_continuous", "type": "toggle", "label": "Switch from Sequential to Continuous Combined?", "required": False},
                    {"id": "hrt_switch_continuous_criteria", "type": "textarea", "label": "Switch Criteria", "required": False, "placeholder": "Criteria: On sequential HRT ≥1 year, or >1 year since LMP, or age >54, and patient wants to avoid bleeds."},
                    {"id": "hrt_vaginal_oestrogen", "type": "single_select", "label": "Vaginal Oestrogen Added?", "required": False, "options": ["None", "Vagifem 10mcg nocte 2 weeks then twice weekly", "Imvaggis pessary nightly 2 weeks then twice weekly", "Vaginal lubricants advised (Replens, YES, KY Jelly)"]},
                    {"id": "hrt_lifestyle", "type": "toggle", "label": "Diet and Exercise Advised? (Weight gain common at menopause)", "required": False},
                    {"id": "hrt_patient_resources", "type": "toggle", "label": "Patient Resources Given? (www.menopausematters.co.uk, HSE menopause leaflet)", "required": False}
                ]
            },
            {
                "title": "Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "hrt_next_review", "type": "text", "label": "Next Review", "required": True, "placeholder": "e.g., 6 months or 1 year"},
                    {"id": "hrt_referral", "type": "single_select", "label": "Referral Needed?", "required": False, "options": ["None", "Menopause clinic (complex symptoms, BMI>40, premature menopause)", "Gynaecology (abnormal bleeding, pelvic pathology)", "Breast clinic (new lump/skin changes)", "Endocrinology"]}
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
    seed_hrt_review()