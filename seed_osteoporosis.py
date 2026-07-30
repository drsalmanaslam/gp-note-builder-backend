from app.database import SessionLocal
from app.models import User, Template, Category

def seed_osteoporosis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Chronic Disease Reviews").first()
    if not category: category = Category(name="Chronic Disease Reviews"); db.add(category); db.commit()

    t = {
        "title": "Osteoporosis",
        "description": "Comprehensive osteoporosis assessment covering FRAX risk stratification, DEXA interpretation, antiresorptive therapy prescribing, and safety monitoring.",
        "category": "Chronic Disease Reviews",
        "content": {"sections": [
            {
                "title": "Key Risk Factors (FRAX Mandatory if Any Present)",
                "section_type": "history",
                "questions": [
                    {"id": "osteo_fhx", "type": "toggle", "label": "FHx Osteoporosis / Hip Fracture?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: FHx = Calculate FRAX regardless of screening result.", "red_flag_negative": ""},
                    {"id": "osteo_fragility_fx", "type": "toggle", "label": "Previous Fragility Fracture?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fragility fracture = treatment may be indicated regardless of T-score.", "red_flag_negative": ""},
                    {"id": "osteo_steroids", "type": "toggle", "label": "Long-Term Steroids? (≥7.5mg Prednisolone/Day, >3 Months)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Long-term steroids = FRAX mandatory + consider treatment.", "red_flag_negative": ""},
                    {"id": "osteo_height_loss", "type": "toggle", "label": "Height Loss / Stooping?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Height loss = ?vertebral fractures. Calculate FRAX.", "red_flag_negative": ""},
                    {"id": "osteo_age70_hip", "type": "toggle", "label": "Age >70 with Prior Hip Fracture?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Treatment indicated regardless of T-score.", "red_flag_negative": ""},
                    {"id": "osteo_coeliac_ibd", "type": "toggle", "label": "Coeliac Disease / IBD?", "required": True},
                    {"id": "osteo_premature_menopause", "type": "toggle", "label": "Premature Menopause / Orchidectomy-Oophorectomy?", "required": True},
                    {"id": "osteo_endocrine", "type": "toggle", "label": "RA / T1DM / Hyperparathyroid / Hyperthyroid / Cushing's?", "required": True}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "osteo_smoking", "type": "toggle", "label": "Smoking?", "required": True},
                    {"id": "osteo_alcohol", "type": "toggle", "label": "Alcohol Excess?", "required": True},
                    {"id": "osteo_exercise", "type": "toggle", "label": "Weight-Bearing Exercise?", "required": False},
                    {"id": "osteo_falls", "type": "toggle", "label": "Falls / Fracture History?", "required": True},
                    {"id": "osteo_endocrine_symptoms", "type": "toggle", "label": "Heat Intolerance / Weight Loss? (?Hyperthyroid)", "required": False},
                    {"id": "osteo_gi_symptoms", "type": "toggle", "label": "Coeliac / IBD Symptoms?", "required": False},
                    {"id": "osteo_calcium", "type": "single_select", "label": "Calcium Intake (Calcium Calculator: webapps.igc.ed.ac.uk)", "required": False, "options": ["Low", "Adequate"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "osteo_height", "type": "number", "label": "Height (cm)", "required": False, "placeholder": "e.g., 162"},
                    {"id": "osteo_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 58"},
                    {"id": "osteo_height_loss_recorded", "type": "toggle", "label": "Height Loss Recorded?", "required": False}
                ]
            },
            {
                "title": "FRAX Risk Stratification (Irish-Adapted FRAX Tool)",
                "section_type": "assessment",
                "questions": [
                    {"id": "osteo_frax", "type": "single_select", "label": "FRAX Category (No NOGG Graph - Irish Version)", "required": True, "options": ["Low Risk - Reassure", "Intermediate Risk - Order DEXA, Re-Run FRAX with T-Score", "High Risk - Consider Treatment"]}
                ]
            },
            {
                "title": "DEXA T-Score Interpretation",
                "section_type": "assessment",
                "questions": [
                    {"id": "osteo_dexa_performed", "type": "toggle", "label": "DEXA Performed?", "required": False},
                    {"id": "osteo_t_score", "type": "number", "label": "T-Score", "required": False, "placeholder": "e.g., -2.8"},
                    {"id": "osteo_t_score_category", "type": "single_select", "label": "T-Score Category", "required": False, "options": ["Normal (> -1.0) - Correct modifiable risk factors", "Osteopenia (-2.5 to -1.0) - Treat if risk factor present", "Osteoporosis (< -2.5) - TREAT", "Severe Osteoporosis (< -2.5 + fragility fracture) - TREAT"]},
                    {"id": "osteo_additional_triggers", "type": "multi_select", "label": "Additional Treatment Triggers (Treatment Regardless of T-Score)", "required": False, "options": ["Fragility fracture", "Age >70 + prior hip fracture", "≥2 Vertebral fractures", "Long-term glucocorticoids", "Age >75 + fragility fracture"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any selected = treatment indicated regardless of T-score.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "osteo_inv_fbc", "type": "toggle", "label": "FBC", "required": False},
                    {"id": "osteo_inv_esr", "type": "toggle", "label": "ESR (Exclude Myeloma)", "required": False},
                    {"id": "osteo_inv_crp", "type": "toggle", "label": "CRP", "required": False},
                    {"id": "osteo_inv_tfts", "type": "toggle", "label": "TFTs", "required": False},
                    {"id": "osteo_inv_bone", "type": "toggle", "label": "LFT / Bone Profile", "required": False},
                    {"id": "osteo_inv_vit_d", "type": "toggle", "label": "Vitamin D", "required": False}
                ]
            },
            {
                "title": "Plan - Lifestyle",
                "section_type": "plan",
                "questions": [
                    {"id": "osteo_pl_exercise", "type": "toggle", "label": "Weight-Bearing Exercise Advised?", "required": False},
                    {"id": "osteo_pl_smoking", "type": "toggle", "label": "Smoking Cessation Advised?", "required": False},
                    {"id": "osteo_pl_alcohol", "type": "toggle", "label": "Reduce Alcohol Advised?", "required": False},
                    {"id": "osteo_pl_diet", "type": "toggle", "label": "Increase Dietary Calcium Advised?", "required": False}
                ]
            },
            {
                "title": "Plan - Calcium & Vitamin D",
                "section_type": "plan",
                "questions": [
                    {"id": "osteo_calcium_vitd", "type": "single_select", "label": "Calcium + Vitamin D Supplement", "required": False, "options": ["Cadelius 600mg/1000IU OD", "Caltrate 600mg/400IU BD", "Kalcipos 800IU/500mg OD", "Ideos 1 BD", "None"]},
                    {"id": "osteo_vit_d_correction", "type": "toggle", "label": "Correct Vitamin D Insufficiency First? (Before Bisphosphonate/Denosumab)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Must correct Vit D before starting bisphosphonate/denosumab. Options: Altavita, Thorens, Desunin.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Plan - Antiresorptive Therapy",
                "section_type": "plan",
                "safety_netting": "BISPHOSPHONATE SAFETY: Take upright, avoid food 1hr before/2hr after, exclude achalasia/oesophageal stricture first. Counsel: report vague thigh pain (atypical fracture), report unexplained ear pain/discharge (osteonecrosis). DENOSUMAB SAFETY (MHRA Aug 2020): Do NOT stop denosumab without specialist review - risk of multiple vertebral fractures on discontinuation. If stopping, MUST transition to bisphosphonate to prevent rebound bone loss. Calcium + Vit D MUST be checked before first dose (contraindicated if hypocalcaemic) and before subsequent doses. Dental review MUST be booked before starting either therapy. Continue bisphosphonate 5 years (up to 10 years if high fracture risk). No data beyond 10 years for denosumab.",
                "questions": [
                    {"id": "osteo_therapy_line", "type": "single_select", "label": "Therapy Line", "required": False, "options": ["Bisphosphonate (First-Line)", "Denosumab (Second-Line)", "None"]},
                    {"id": "osteo_bisphosphonate", "type": "single_select", "label": "Bisphosphonate Choice", "required": False, "options": ["Alendronate + Vit D (Fosavance) 70mg Once Weekly", "Risedronate", "Binosto (Alendronate 70mg in 120ml Water)", "Not applicable"]},
                    {"id": "osteo_bisphosphonate_qty", "type": "text", "label": "Quantity + Review", "required": False, "placeholder": "e.g., 60 tabs, review 3-5 years"},
                    {"id": "osteo_denosumab_calcium", "type": "toggle", "label": "Calcium + Vit D Checked Before First Dose? (CI if Hypocalcaemic)", "required": False},
                    {"id": "osteo_dental", "type": "toggle", "label": "Dental Review Booked Before Starting Bisphosphonate/Denosumab?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dental review MUST be completed before starting antiresorptive therapy (ONJ risk).", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Duration & Review",
                "section_type": "plan",
                "questions": [
                    {"id": "osteo_holiday", "type": "single_select", "label": "Bisphosphonate Holiday (After 5 Years)", "required": False, "options": ["Risedronate - 6 Month Break", "Alendronate - 12-24 Month Break", "Not applicable"]},
                    {"id": "osteo_extended", "type": "multi_select", "label": "Extended Duration Indications (Continue 6-10 Years)", "required": False, "options": ["Fragility fracture", "Age >70", "Prior hip fracture", "≥2 Vertebral fractures", "On glucocorticoids"]},
                    {"id": "osteo_nice_stop", "type": "toggle", "label": "NICE: Discuss Stopping Bisphosphonate at 3 Years if Multimorbid?", "required": False}
                ]
            },
            {
                "title": "Patient Education & Follow-Up",
                "section_type": "plan",
                "questions": [
                    {"id": "osteo_edu", "type": "toggle", "label": "Explained Painless Bone Thinning / Fracture Risk? (Patient.info Leaflet)", "required": False},
                    {"id": "osteo_gpevidence", "type": "toggle", "label": "GP Evidence Link Provided? (gpevidence.org)", "required": False},
                    {"id": "osteo_fu_dexa", "type": "toggle", "label": "DEXA to Review Ongoing Need (Bisphosphonate)?", "required": False},
                    {"id": "osteo_fu_reassess", "type": "toggle", "label": "Reassess Fracture Risk at 5-10 Years (Denosumab)?", "required": False},
                    {"id": "osteo_fu_routine", "type": "toggle", "label": "Routine Review?", "required": False}
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
    seed_osteoporosis()