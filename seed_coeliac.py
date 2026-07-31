from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_coeliac():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Coeliac Disease",
        "description": "Comprehensive template for coeliac disease covering serological testing prerequisites, diagnosis pathway, gluten-free diet counselling, vaccination, and annual monitoring.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "coel_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Abdominal bloating, intermittent diarrhoea, and fatigue for 6 months"},
                    {"id": "coel_gi_symptoms", "type": "multi_select", "label": "GI Symptoms", "required": True, "options": ["Non-specific abdominal pain", "Bloating", "Intermittent diarrhoea", "Nausea", "None"]},
                    {"id": "coel_systemic", "type": "multi_select", "label": "Associated Systemic Symptoms", "required": True, "options": ["Fatigue", "Weight loss", "Tired all the time", "Sore tongue / aphthous ulcers", "Hair thinning", "None present"]},
                    {"id": "coel_gluten_intake", "type": "single_select", "label": "Gluten Intake Before Testing", "required": True, "options": ["Adequate - gluten >1 meal/day for ≥6 weeks", "Inadequate - advise reintroduction before testing", "Not yet established"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Serology only accurate if gluten eaten in >1 meal/day for ≥6 weeks prior to testing. False negatives if gluten-restricted.", "red_flag_negative": ""},
                    {"id": "coel_pmh", "type": "multi_select", "label": "Relevant PMHx (Associated Autoimmune)", "required": False, "options": ["Autoimmune condition", "Irritable Bowel Syndrome", "Type 1 Diabetes Mellitus", "None"]},
                    {"id": "coel_family", "type": "toggle", "label": "Family History of Coeliac Disease? (1st degree = 10% risk)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: 1st degree relatives have 10% risk of coeliac disease. Advise screening.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "coel_bmi", "type": "number", "label": "BMI (kg/m²)", "required": False, "placeholder": "e.g., 18"},
                    {"id": "coel_dermatitis", "type": "toggle", "label": "Dermatitis Herpetiformis?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dermatitis herpetiformis = pathognomonic for coeliac disease. Skin biopsy can confirm.", "red_flag_negative": ""},
                    {"id": "coel_abdo", "type": "single_select", "label": "Abdominal Examination", "required": False, "options": ["No obvious distension", "Distension present", "Other finding"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Coeliac Disease",
                    "Irritable Bowel Syndrome (IBS)",
                    "Inflammatory Bowel Disease (Crohn's/UC)",
                    "Lactose Intolerance",
                    "Small Intestinal Bacterial Overgrowth (SIBO)",
                    "Giardiasis",
                    "Autoimmune Gastritis"
                ],
                "questions": [
                    {"id": "coel_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "LFTs", "ESR / CRP", "Calcium", "IgA TTG (tissue transglutaminase)", "Total IgA (Immunoglobulins)", "None"]},
                    {"id": "coel_ttg_result", "type": "single_select", "label": "IgA TTG Result", "required": False, "options": ["Negative", "Equivocal - IgA endomysial antibody needed", "Mildly raised (weak PPV ~93%)", "Markedly raised (≥10x ULN - strong PPV)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Raised TTG does NOT equal coeliac diagnosis. Histological confirmation via endoscopic biopsy required. Do NOT start gluten-free diet yet.", "red_flag_negative": ""},
                    {"id": "coel_ema", "type": "toggle", "label": "IgA Endomysial Antibody Requested? (If TTG equivocal)", "required": False}
                ]
            },
            {
                "title": "Pre-Diagnosis Counselling",
                "section_type": "plan",
                "questions": [
                    {"id": "coel_no_gf_diet_yet", "type": "toggle", "label": "Advised NOT to Start Gluten-Free Diet Until After Biopsy? (Even if serology positive)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Starting gluten-free diet before biopsy can cause false negative histology. Must wait for gastroenterology.", "red_flag_negative": ""},
                    {"id": "coel_referral", "type": "single_select", "label": "Gastroenterology Referral for Biopsy", "required": False, "options": ["Referred", "Not yet referred - awaiting serology"]}
                ]
            },
            {
                "title": "Management (If Diagnosis Confirmed)",
                "section_type": "plan",
                "safety_netting": "Lifelong gluten-free diet: avoid wheat, barley, and rye. Oats: inherently gluten-free but often cross-contaminated. Avenin may cause symptoms in minority. Most patients report clinical improvement within 2-6 months of starting gluten-free diet. Dietician review arranged. Coeliac Ireland: coeliac.ie. Coeliac UK: Gluten-Free Diet and Lifestyle. Annual monitoring: FBC, haematinics, LFTs, bone profile, Vitamin D, coeliac screen, TFTs (autoimmune thyroid risk), HbA1c (T1DM risk). First-degree relatives: advise screening (10% risk). DEXA scan: post-menopausal women, men >55, fragility fracture. Vaccinations: annual influenza + pneumococcal. Consider additional vaccination if splenic dysfunction suspected (HIB/MenC, MenACWY, MenB) - seek specialist advice.",
                "questions": [
                    {"id": "coel_diet", "type": "multi_select", "label": "Dietary Management", "required": False, "options": ["Lifelong abstinence from wheat, barley, rye", "Dietician review arranged", "Oat counselling given (cross-contamination + avenin)"]},
                    {"id": "coel_resources", "type": "toggle", "label": "Patient Resources Given? (Coeliac Ireland / Coeliac UK)", "required": False},
                    {"id": "coel_supplements", "type": "multi_select", "label": "Nutritional Supplements", "required": False, "options": ["Iron", "Vitamin D", "Folate", "Calcium", "Folic acid 5mg (if chance of pregnancy)"]},
                    {"id": "coel_dexa", "type": "multi_select", "label": "DEXA Scan Indications", "required": False, "options": ["Post-menopausal women", "All patients - baseline scan", "Men >55 years", "Fragility fracture history", "Not indicated"]},
                    {"id": "coel_vaccines", "type": "multi_select", "label": "Vaccinations", "required": False, "options": ["Annual influenza vaccine", "Pneumococcal vaccine", "Additional: HIB/MenC, MenACWY, MenB (splenic dysfunction)", "Not applicable"]},
                    {"id": "coel_annual_monitoring", "type": "multi_select", "label": "Annual Monitoring (Increased Autoimmune Risk)", "required": False, "options": ["Vitamin D", "LFTs", "Bone profile", "Coeliac screen (IgA TTG)", "Haematinics (Ferritin, B12, Folate)", "TFTs (autoimmune thyroid)", "HbA1c (T1DM risk)"]},
                    {"id": "coel_family_screening", "type": "toggle", "label": "First-Degree Relatives Advised to be Tested? (10% risk)", "required": False},
                    {"id": "coel_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review after gastroenterology, 2-6 months post-diagnosis, or annual review"}
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
    seed_coeliac()