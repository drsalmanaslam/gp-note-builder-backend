from app.database import SessionLocal
from app.models import User, Template, Category

def seed_b12_deficiency():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Low Vitamin B12",
        "description": "Comprehensive B12 deficiency assessment covering neurological red flags, pernicious anaemia diagnosis, IM vs oral treatment pathways, and concurrent folate safety.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Neurological & Haematological",
                "section_type": "history",
                "questions": [
                    {"id": "b12_ataxia", "type": "toggle", "label": "Ataxia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neurological symptoms = IM B12 every 2 MONTHS for life (not 3-monthly).", "red_flag_negative": ""},
                    {"id": "b12_confusion", "type": "toggle", "label": "Confusion / Memory Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cognitive symptoms = neurological involvement. IM B12 every 2 months.", "red_flag_negative": ""},
                    {"id": "b12_paraesthesia", "type": "toggle", "label": "Paraesthesia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Paraesthesia = neurological involvement (can occur with normal MCV). IM B12 every 2 months.", "red_flag_negative": ""},
                    {"id": "b12_vision_problems", "type": "toggle", "label": "Vision Problems?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Optic neuropathy = neurological involvement. IM B12 every 2 months.", "red_flag_negative": ""},
                    {"id": "b12_peripheral_neuropathy", "type": "toggle", "label": "Peripheral Neuropathy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Peripheral neuropathy = neurological involvement. IM B12 every 2 months.", "red_flag_negative": ""},
                    {"id": "b12_pancytopenia", "type": "toggle", "label": "Low Hb + Low Reticulocytes + NRBCs / Low Platelets / Low Neutrophils?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pancytopenia features = CONTACT HAEMATOLOGY urgently.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Results & History",
                "section_type": "history",
                "questions": [
                    {"id": "b12_level", "type": "number", "label": "B12 Level (ng/L) - NR: 120-650", "required": True, "placeholder": "e.g., 85 (100-120 = Indeterminate, <100 = Low)"},
                    {"id": "b12_folate", "type": "single_select", "label": "Folic Acid Level", "required": False, "options": ["Normal", "Low - DO NOT Start Folate Until B12 Normalised (Risk SACD)"]},
                    {"id": "b12_if_antibody", "type": "single_select", "label": "Intrinsic Factor Antibody (Highly Specific, ~50% Sensitive)", "required": False, "options": ["Positive - Pernicious Anaemia Confirmed", "Negative - Does NOT Exclude PA"]},
                    {"id": "b12_diet", "type": "single_select", "label": "Dietary History", "required": True, "options": ["Vegetarian", "Vegan", "Omnivore - Adequate B12 Intake"]},
                    {"id": "b12_meds", "type": "multi_select", "label": "Medications Reducing B12 Absorption", "required": True, "options": ["PPI (Omeprazole, Lansoprazole)", "Metformin", "Anticonvulsant", "Colchicine", "None of the above"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "b12_neuro", "type": "single_select", "label": "Neurological Examination", "required": True, "options": ["Normal", "Abnormal - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal neuro exam = IM B12 every 2 months. Neuro exam findings dictate treatment urgency.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Dietary B12 Deficiency (Vegetarian/Vegan)",
                    "Pernicious Anaemia (Intrinsic Factor Antibody Positive)",
                    "Non-Dietary / Malabsorptive B12 Deficiency (PPI, Metformin, GI Surgery)",
                    "B12 Deficiency with Neurological Involvement (RED FLAG)",
                    "B12 Deficiency with Anaemia (Hb Low, MCV Raised)",
                    "Concurrent Folate Deficiency (Treat B12 FIRST)"
                ],
                "questions": [
                    {"id": "b12_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Dietary B12 Deficiency - No Neurological Symptoms", "Non-Dietary / Malabsorptive B12 Deficiency - No Neurological Symptoms", "Pernicious Anaemia (IF Antibody Positive)", "B12 Deficiency WITH Neurological Symptoms - Urgent Treatment", "B12 Deficiency with Anaemia (B12 <150) - Treat While Awaiting IF Antibody"]}
                ]
            },
            {
                "title": "Treatment Pathway",
                "section_type": "plan",
                "safety_netting": "IMPORTANT: If folate deficiency is also present, do NOT start folate replacement until B12 levels have normalised. Starting folate first can precipitate subacute combined degeneration of the cord (SACD). Once B12 normalised: Folic acid 5mg OD for minimum 4 months (prescription required for 5mg strength). Neocytamen is the ONLY GMS-reimbursable B12 injection. Cyanocobalamin (Cytamen) is unlicensed and not GMS reimbursable. Routine monitoring of B12 levels is NOT normally required or recommended. Follow up with coeliac screen and repeat B12 at 6 months (dietary/malabsorptive cause). If IF antibody positive = Pernicious Anaemia = refer gastroenterology (increased gastric cancer risk with autoimmune gastritis).",
                "questions": [
                    {"id": "b12_pathway", "type": "single_select", "label": "Treatment Pathway", "required": True, "options": ["Dietary, No Neuro: Oral Methylcobalamin 1000mcg OD (Sona Brand OTC) OR 6-Monthly IM", "Non-Dietary, No Neuro: Neocytamen 1000mcg IM Alternate Days x2 Weeks → Every 3 Months for Life", "NEUROLOGICAL Symptoms: Neocytamen 1000mcg IM Alternate Days x2 Weeks → Every 2 MONTHS for Life", "Anaemia + B12 <150: IM Hydroxocobalamin 1000mcg Alternate Days x2 Weeks → Maintenance Per Cause", "Pernicious Anaemia: IM B12 for Life + Refer Gastroenterology"]},
                    {"id": "b12_oral_rx", "type": "toggle", "label": "Oral B12 Methylcobalamin 1000mcg OD Advised? (OTC - Sona Brand)", "required": False},
                    {"id": "b12_im_rx", "type": "toggle", "label": "Neocytamen (Hydroxocobalamin) 1000mcg IM Prescribed?", "required": False},
                    {"id": "b12_folate_warning", "type": "toggle", "label": "Folate Safety: Do NOT Start Folate Until B12 Normalised (SACD Risk)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Starting folate before B12 normalised can precipitate subacute combined degeneration of the cord.", "red_flag_negative": ""},
                    {"id": "b12_folic_acid", "type": "toggle", "label": "Folic Acid 5mg OD for 4 Months? (Once B12 Normalised - If Folate Deficient)", "required": False},
                    {"id": "b12_gastro_referral", "type": "toggle", "label": "Refer Gastroenterology? (IF Antibody Positive = Pernicious Anaemia = Gastric Cancer Risk)", "required": False},
                    {"id": "b12_coeliac", "type": "toggle", "label": "Coeliac Screen + Repeat B12 at 6 Months?", "required": False},
                    {"id": "b12_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat B12 at 6 months, coeliac screen, gastro referral if PA"}
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
    seed_b12_deficiency()