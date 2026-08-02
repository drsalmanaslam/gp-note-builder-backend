from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_prostate_cancer():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Suspected Prostate Cancer - National Rapid Access Prostate Clinic (RAPC) GP Referral Guideline",
        "description": "National RAPC guideline-based prostate cancer referral pathway covering 5 patient groups, age-related PSA thresholds, shared decision-making, and referral disposition.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "Patient Group Selection",
                "section_type": "history",
                "questions": [
                    {"id": "pca_group", "type": "single_select", "label": "Patient Group (>3,300 Men Diagnosed Annually in Ireland. Lifetime Risk to Age 75: 13.34%. 5-Year Survival: 92%)", "required": True, "options": ["Group 1: Symptoms suspicious of advanced prostate cancer", "Group 2: Age 50-70, no symptoms", "Group 3: Age <50, no symptoms", "Group 4: Age >70, no symptoms", "Group 5: Any age, with Lower Urinary Tract Symptoms (LUTS)"]},
                    {"id": "pca_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 62"}
                ]
            },
            {
                "title": "Group 1 - Symptoms Suspicious of Advanced Prostate Cancer",
                "section_type": "history",
                "questions": [
                    {"id": "pca_g1_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": False, "options": ["New onset bone pain at rest", "Unexplained weight loss", "Symptoms suggestive of Cauda Equina → REFER DIRECTLY TO ED"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Cauda equina symptoms = EMERGENCY. Refer directly to ED - do NOT route via RAPC.", "red_flag_negative": ""},
                    {"id": "pca_g1_action", "type": "single_select", "label": "Action", "required": False, "options": ["Explain need for prostate assessment + patient leaflet → Proceed to PSA + DRE", "Cauda equina suspected → Refer directly to ED"]}
                ]
            },
            {
                "title": "Group 2 - Age 50-70, No Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "pca_g2_discussion", "type": "toggle", "label": "Shared Decision-Making: Benefits (Early Detection) vs Harms (False +/- Results, Side Effects, Anxiety) Discussed?", "required": False},
                    {"id": "pca_g2_high_risk", "type": "multi_select", "label": "Higher-Risk Factors", "required": False, "options": ["African ethnicity", "Family history (number of relatives, early onset <50)", "BRCA1/2 mutation", "None identified"]},
                    {"id": "pca_g2_decision", "type": "single_select", "label": "Decision", "required": False, "options": ["Proceed to prostate assessment (PSA + DRE)", "Decision not to proceed at this time"]},
                    {"id": "pca_g2_normal", "type": "single_select", "label": "If Normal PSA + Non-Suspicious DRE", "required": False, "options": ["No further action - review may be considered in 2 years", "Not applicable"]},
                    {"id": "pca_g2_raised", "type": "single_select", "label": "If Raised PSA + Non-Suspicious DRE", "required": False, "options": ["Repeat PSA 6-12 weeks later, same laboratory", "Not applicable"]},
                    {"id": "pca_g2_repeat_normal", "type": "single_select", "label": "Repeat PSA Normal →", "required": False, "options": ["No referral required - review in 2 years", "Not applicable"]},
                    {"id": "pca_g2_repeat_raised", "type": "single_select", "label": "Repeat PSA Still Raised →", "required": False, "options": ["Referral to Rapid Access Prostate Clinic", "Not applicable"]},
                    {"id": "pca_g2_suspicious_dre", "type": "single_select", "label": "If Suspicious DRE (Irrespective of PSA) →", "required": False, "options": ["Referral to Rapid Access Prostate Clinic", "Not applicable"]}
                ]
            },
            {
                "title": "Group 3 - Age <50, No Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "pca_g3_discussion", "type": "toggle", "label": "Shared Decision-Making Discussed? (Benefits vs Harms, Higher-Risk Groups)", "required": False},
                    {"id": "pca_g3_decision", "type": "single_select", "label": "Decision", "required": False, "options": ["Proceed to prostate assessment (PSA + DRE)", "Decision not to proceed"]},
                    {"id": "pca_g3_psa_threshold", "type": "single_select", "label": "PSA Threshold for <50 Years", "required": False, "options": ["Normal: <2µg/L → No further action, review in 2 years", "Raised: ≥2µg/L → Repeat PSA 6-12 weeks", "Not applicable"]},
                    {"id": "pca_g3_repeat_raised", "type": "single_select", "label": "Repeat PSA ≥2µg/L →", "required": False, "options": ["Referral to Rapid Access Prostate Clinic", "Not applicable"]},
                    {"id": "pca_g3_suspicious_dre", "type": "single_select", "label": "Suspicious DRE (Irrespective of PSA) →", "required": False, "options": ["Referral to Rapid Access Prostate Clinic", "Not applicable"]}
                ]
            },
            {
                "title": "Group 4 - Age >70, No Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "pca_g4_life_expectancy", "type": "single_select", "label": "Comorbidity / Life Expectancy Assessment", "required": False, "options": ["Life expectancy >10 years, healthy and fit", "Life-limiting comorbidities, life expectancy <10 years"]},
                    {"id": "pca_g4_discussion", "type": "toggle", "label": "Shared Decision-Making Discussed? (BPH can raise PSA; Testing unlikely to affect overall survival but may benefit those with >10yr life expectancy)", "required": False},
                    {"id": "pca_g4_decision", "type": "single_select", "label": "Decision", "required": False, "options": ["Proceed to PSA + DRE", "Decision not to proceed - no further investigation"]},
                    {"id": "pca_g4_psa_threshold", "type": "single_select", "label": "PSA Threshold for >70 Years", "required": False, "options": ["Normal: <5µg/L → No further action", "Raised: ≥5µg/L → Repeat PSA 6-12 weeks", "Not applicable"]},
                    {"id": "pca_g4_repeat_raised", "type": "single_select", "label": "Repeat PSA ≥5µg/L →", "required": False, "options": ["Urgent referral to a urologist", "Not applicable"]},
                    {"id": "pca_g4_suspicious_dre", "type": "single_select", "label": "Suspicious DRE (Irrespective of PSA) →", "required": False, "options": ["Urgent referral to a urologist", "Not applicable"]}
                ]
            },
            {
                "title": "Group 5 - Any Age, with LUTS",
                "section_type": "history",
                "questions": [
                    {"id": "pca_g5_urinalysis", "type": "single_select", "label": "Urinalysis", "required": False, "options": ["Positive - manage appropriately, allow 6 weeks for symptom resolution", "Negative - proceed to standard LUTS evaluation"]},
                    {"id": "pca_g5_ipss", "type": "toggle", "label": "IPSS (International Prostate Symptom Score) Completed?", "required": False},
                    {"id": "pca_g5_normal", "type": "single_select", "label": "Normal PSA + Non-Suspicious DRE →", "required": False, "options": ["Treat as BPH", "Not applicable"]},
                    {"id": "pca_g5_raised", "type": "single_select", "label": "Raised PSA + Non-Suspicious DRE →", "required": False, "options": ["Repeat PSA 6-12 weeks later", "Not applicable"]},
                    {"id": "pca_g5_repeat_normal", "type": "single_select", "label": "Repeat PSA Normal →", "required": False, "options": ["Treat symptoms; consider repeat PSA at 6 months for stability", "Not applicable"]},
                    {"id": "pca_g5_repeat_raised", "type": "single_select", "label": "Repeat PSA Still Raised →", "required": False, "options": ["Referral to Rapid Access Prostate Clinic", "Not applicable"]},
                    {"id": "pca_g5_suspicious_dre", "type": "single_select", "label": "Suspicious DRE (Irrespective of PSA) →", "required": False, "options": ["Referral to Rapid Access Prostate Clinic", "Not applicable"]}
                ]
            },
            {
                "title": "PSA Result & Age-Related Thresholds",
                "section_type": "assessment",
                "questions": [
                    {"id": "pca_psa", "type": "number", "label": "PSA Result (µg/L) - Informed Consent Required Before Testing", "required": False, "placeholder": "e.g., 5.2"},
                    {"id": "pca_dre", "type": "single_select", "label": "DRE Finding", "required": False, "options": ["Non-suspicious", "Suspicious - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspicious DRE = refer to RAPC irrespective of PSA result.", "red_flag_negative": ""},
                    {"id": "pca_psa_interpretation", "type": "single_select", "label": "PSA Interpretation (Age-Adjusted)", "required": False, "options": ["<50y: Normal <2 / Raised ≥2", "50-59y: Normal <3 / Raised ≥3", "60-69y: Normal <4 / Raised ≥4", "≥70y: Normal <5 / Raised ≥5"]}
                ]
            },
            {
                "title": "5α-Reductase Inhibitor Consideration",
                "section_type": "assessment",
                "questions": [
                    {"id": "pca_5ari", "type": "toggle", "label": "On 5α-Reductase Inhibitor? (Finasteride/Dutasteride - Reduces PSA)", "required": False},
                    {"id": "pca_5ari_rise", "type": "toggle", "label": "PSA Rise on Treatment? (Irrespective of Absolute Value - May Indicate Cancer)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: PSA rise on 5ARI = may indicate prostate cancer irrespective of absolute PSA value.", "red_flag_negative": ""},
                    {"id": "pca_5ari_action", "type": "single_select", "label": "Action if PSA Rises on 5ARI", "required": False, "options": ["Age ≤70 - consider referral to RAPC", "Age >70 - consider referral to urologist", "Not applicable"]}
                ]
            },
            {
                "title": "Referral Disposition",
                "section_type": "plan",
                "safety_netting": "PSA should NOT be considered a routine test - informed consent must be obtained before testing. Baseline PSA should be performed 6 months after commencing 5α-reductase inhibitor. A rise in PSA while on 5ARI treatment may indicate prostate cancer irrespective of absolute value. Age-related PSA thresholds: <50y: <2 normal; 50-59y: <3 normal; 60-69y: <4 normal; ≥70y: <5 normal. Prostate cancer = leading cause of cancer in Irish men (excluding NMSC): >3,300 annually. Lifetime risk to age 75: 13.34%. 5-year survival improved from 66% to 92%. RAPC = Rapid Access Prostate Clinic.",
                "questions": [
                    {"id": "pca_outcome", "type": "single_select", "label": "Final Outcome", "required": True, "options": ["Referral to Rapid Access Prostate Clinic", "Urgent referral to urologist (>70y suspicious DRE/raised repeat PSA)", "Emergency referral to ED (suspected Cauda Equina)", "No referral - routine review in 2 years", "No further action required", "Treated as BPH"]},
                    {"id": "pca_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Referral sent, routine review 2 years, repeat PSA in 6-12 weeks, or BPH management"}
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
    seed_prostate_cancer()