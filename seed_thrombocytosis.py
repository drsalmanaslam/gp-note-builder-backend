from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_thrombocytosis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Thrombocytosis (Raised Platelets)",
        "description": "Comprehensive assessment for thrombocytosis covering reactive vs primary causes, LEGO-C cancer screen, iron deficiency exclusion, and JAK2 referral pathway.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "History & Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "plt_count", "type": "number", "label": "Platelet Count (x10⁹/L) - Persistently Raised on Repeat FBC (>400)", "required": True, "placeholder": "e.g., 520", "is_red_flag": True, "red_flag_positive": "RED FLAG: Persistently raised platelets = needs investigation for reactive cause vs MPN.", "red_flag_negative": ""},
                    {"id": "plt_b_symptoms", "type": "multi_select", "label": "B-Symptoms / Red Flags", "required": True, "options": ["Unexplained weight loss", "Fatigue", "Pruritus", "Night sweats", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: B-symptoms + thrombocytosis = ?MPN/malignancy. Urgent haematology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "LEGO-C Cancer Screen",
                "section_type": "history",
                "questions": [
                    {"id": "plt_respiratory", "type": "multi_select", "label": "Respiratory Screen", "required": True, "options": ["Persistent cough", "Haemoptysis", "Dyspnoea", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Respiratory symptoms + thrombocytosis = ?lung cancer. Urgent CXR.", "red_flag_negative": ""},
                    {"id": "plt_lower_gi", "type": "multi_select", "label": "Lower GI Screen", "required": True, "options": ["Change in bowel habit", "PR bleeding", "Melaena", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: GI symptoms + thrombocytosis = ?colorectal cancer. Urgent colonoscopy/FIT.", "red_flag_negative": ""},
                    {"id": "plt_upper_gi", "type": "multi_select", "label": "Upper GI Screen", "required": True, "options": ["Dyspepsia", "Reflux", "Nausea/Vomiting", "Dysphagia", "Epigastric pain", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Upper GI symptoms + thrombocytosis = ?gastric/oesophageal cancer. Urgent OGD.", "red_flag_negative": ""},
                    {"id": "plt_haematuria", "type": "toggle", "label": "Visible or Non-Visible Haematuria? (Renal/Bladder Cancer)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Haematuria + thrombocytosis = ?renal/bladder cancer. Urgent urology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Reactive Causes Screen",
                "section_type": "history",
                "questions": [
                    {"id": "plt_inflammatory", "type": "toggle", "label": "History of Rheumatological / Inflammatory Condition? (RA, IBD, Vasculitis)", "required": True},
                    {"id": "plt_recent_trigger", "type": "multi_select", "label": "Recent Triggers", "required": True, "options": ["Surgery", "Acute infection", "Trauma", "Severe blood loss", "None"]},
                    {"id": "plt_splenectomy", "type": "toggle", "label": "Prior Splenectomy? (Causes Persistent Thrombocytosis)", "required": True}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "plt_abdo", "type": "multi_select", "label": "Abdominal Examination", "required": True, "options": ["Masses", "Hepatomegaly", "Splenomegaly", "Normal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Splenomegaly + thrombocytosis = ?MPN (ET, CML, PV). Urgent haematology.", "red_flag_negative": ""},
                    {"id": "plt_lymph", "type": "single_select", "label": "Lymphadenopathy", "required": True, "options": ["Not Felt", "Cervical", "Axillary", "Inguinal", "Multiple Sites - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy + thrombocytosis = ?lymphoma/malignancy.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "plt_urinalysis", "type": "single_select", "label": "Urine Dipstick - Haematuria?", "required": False, "options": ["Negative", "Positive - RED FLAG", "Not performed"]},
                    {"id": "plt_iron_studies", "type": "toggle", "label": "Iron Studies Ordered? (Ferritin/Iron/TIBC - Rule Out Iron Deficiency Thrombocytosis)", "required": True},
                    {"id": "plt_crp_esr", "type": "toggle", "label": "CRP / ESR Ordered?", "required": True},
                    {"id": "plt_cxr", "type": "toggle", "label": "Chest X-Ray Ordered? (Rule Out Lung Malignancy)", "required": False},
                    {"id": "plt_ogd", "type": "toggle", "label": "OGD Referral? (If Upper GI Symptoms Present)", "required": False},
                    {"id": "plt_colonoscopy_fit", "type": "toggle", "label": "Colonoscopy / FIT? (If Bowel Habit Change or PR Bleeding)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Reactive Thrombocytosis (Infection, Inflammation, Iron Deficiency - Most Common)",
                    "Iron Deficiency Thrombocytosis (Check Ferritin/Iron Studies)",
                    "Essential Thrombocythaemia (ET - JAK2 V617F Positive)",
                    "Chronic Myeloid Leukaemia (CML - BCR-ABL Positive)",
                    "Polycythaemia Vera (PV - JAK2 Positive)",
                    "Primary Myelofibrosis",
                    "Occult Malignancy (Lung, GI, Renal - LEGO-C Screen)",
                    "Post-Splenectomy Thrombocytosis",
                    "Inflammatory Disease (RA, IBD, Vasculitis)"
                ],
                "questions": [
                    {"id": "plt_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["?Reactive Thrombocytosis - Investigating", "?Iron Deficiency Thrombocytosis", "?Occult Malignancy - Urgent LEGO-C Workup", "?MPN (ET/CML/PV) - Haematology Referral", "Post-Splenectomy / Inflammatory - Monitoring"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if developing: haemoptysis, PR bleeding, dysphagia, visible haematuria, or rapid weight loss. Reactive thrombocytosis is most common cause (infection, inflammation, iron deficiency). Iron deficiency can cause thrombocytosis - check ferritin/iron studies. LEGO-C cancer screen: Lungs (CXR), Esophagus/Stomach (OGD), Gastric/Colon (Colonoscopy/FIT), Others (Renal - urinalysis). If all primary care workup for reactive causes is negative: refer Haematology for myeloproliferative screen (JAK2 mutation / CALR / MPL / BCR-ABL).",
                "questions": [
                    {"id": "plt_red_flags_discussed", "type": "toggle", "label": "Red Flags Discussed? (Haemoptysis, PR Bleeding, Dysphagia, Haematuria, Weight Loss)", "required": True},
                    {"id": "plt_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Reactive Cause Identified)", "Haematology (MPN Screen - JAK2/CALR/MPL/BCR-ABL)", "Urgent 2WW (LEGO-C Red Flags)", "Gastroenterology (OGD / Colonoscopy)"]},
                    {"id": "plt_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review with iron studies + CRP, refer haematology if reactive causes excluded"}
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
    seed_thrombocytosis()