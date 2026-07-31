from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_lymphocytosis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Abnormal Labs/Investigations").first()
    if not category: category = Category(name="Abnormal Labs/Investigations"); db.add(category); db.commit()

    t = {
        "title": "Lymphocytosis",
        "description": "Focused assessment for lymphocytosis covering reactive vs clonal causes, B-symptom red flags, haematology referral criteria, and CLL monitoring guidance.",
        "category": "Abnormal Labs/Investigations",
        "content": {"sections": [
            {
                "title": "History & Red Flags",
                "section_type": "history",
                "questions": [
                    {"id": "lymph_reason", "type": "single_select", "label": "Reason for Testing", "required": True, "options": ["Routine", "URTI / Viral Symptoms", "Fatigue", "B-Symptoms Screen", "Incidental"]},
                    {"id": "lymph_recent_illness", "type": "single_select", "label": "Current / Recent Illness", "required": True, "options": ["URTI / Viral Symptoms", "None"]},
                    {"id": "lymph_night_sweats", "type": "toggle", "label": "Night Sweats? (B-Symptom - RED FLAG)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: B-symptoms + lymphocytosis = ?lymphoma/CLL. Urgent haematology referral.", "red_flag_negative": ""},
                    {"id": "lymph_weight_loss", "type": "toggle", "label": "Unexplained Weight Loss? (B-Symptom - RED FLAG)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + lymphocytosis = ?malignancy. Urgent haematology.", "red_flag_negative": ""},
                    {"id": "lymph_fevers", "type": "toggle", "label": "Unexplained Fevers? (B-Symptom - RED FLAG)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fevers + lymphocytosis = ?lymphoma, infection. Urgent investigation.", "red_flag_negative": ""},
                    {"id": "lymph_bruising", "type": "toggle", "label": "Easy Bruising / Bleeding? (RED FLAG)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Bruising/bleeding = ?bone marrow involvement. Urgent haematology.", "red_flag_negative": ""},
                    {"id": "lymph_infections", "type": "toggle", "label": "Recurrent / Severe Infections? (RED FLAG)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Recurrent infections = ?immune dysfunction from haematological disorder.", "red_flag_negative": ""},
                    {"id": "lymph_pruritus", "type": "toggle", "label": "Pruritus? (Lymphoma - RED FLAG)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pruritus + lymphocytosis = ?lymphoma. Urgent haematology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "lymph_ent", "type": "single_select", "label": "ENT", "required": False, "options": ["Coryzal", "Pharyngitis", "Normal"]},
                    {"id": "lymph_resp", "type": "single_select", "label": "Respiratory", "required": False, "options": ["Equal AE B/L, Vesicular BS, No Added Sounds", "Abnormal"]},
                    {"id": "lymph_nodes", "type": "single_select", "label": "Lymphadenopathy", "required": True, "options": ["Not Felt", "Cervical - Present", "Axillary - Present", "Inguinal - Present", "Multiple Sites - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy + lymphocytosis = ?lymphoma/CLL. Urgent haematology.", "red_flag_negative": ""},
                    {"id": "lymph_hepatosplenomegaly", "type": "single_select", "label": "Hepatosplenomegaly", "required": True, "options": ["Not Felt", "Present - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Organomegaly + lymphocytosis = ?CLL/lymphoma. Urgent haematology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Reactive Lymphocytosis (Viral - URTI, EBV, CMV - Most Common)",
                    "Chronic Lymphocytic Leukaemia (CLL - Asymptomatic, Elderly)",
                    "Lymphoma (B-Symptoms, Lymphadenopathy, Organomegaly)",
                    "Acute Lymphoblastic Leukaemia (ALL - Children, Young Adults)",
                    "Pertussis (Whooping Cough - Extreme Lymphocytosis)",
                    "Stress / Trauma / Surgery (Transient Reactive)",
                    "Autoimmune Disease (SLE, RA)"
                ],
                "questions": [
                    {"id": "lymph_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Isolated Reactive Lymphocytosis - ?Viral (URTI)", "Reactive Lymphocytosis - Red Flags PRESENT - Urgent Haematology", "?CLL - Monitoring Required", "Uncertain - Requires Further Investigation"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return sooner if developing: persistent or worsening night sweats, unexplained weight loss, unexplained fevers, new palpable lumps (neck, armpits, groin), progressive fatigue, pallor, or easy bruising/bleeding. Reactive lymphocytosis is common and typically transient following viral illness - usually resolves within 2 months. Repeat FBC + Blood Film in 6-8 weeks. Haematology referral criteria: persistent lymphocytosis >7 x10⁹/L, rapidly rising lymphocyte count, abnormal blood film (blasts/atypical cells), associated cytopenias (anaemia, neutropenia, thrombocytopenia), unexplained B-symptoms or organomegaly. Note: asymptomatic CLL does NOT benefit from early treatment - monitoring is safe.",
                "questions": [
                    {"id": "lymph_reassurance", "type": "toggle", "label": "Reactive/Transient Nature Explained? (Common After Viral Illness, Resolves Within 2 Months)", "required": True},
                    {"id": "lymph_repeat_fbc", "type": "toggle", "label": "Repeat FBC + Blood Film in 6-8 Weeks?", "required": True},
                    {"id": "lymph_referral_criteria", "type": "toggle", "label": "Haematology Referral Criteria Reviewed? (For Follow-Up FBC)", "required": True},
                    {"id": "lymph_cll_note", "type": "toggle", "label": "CLL Monitoring Note: Asymptomatic CLL Does NOT Benefit from Early Treatment", "required": False},
                    {"id": "lymph_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed (Reactive, Repeat FBC)", "Haematology - Urgent (Red Flags Present)", "Haematology - Routine (?CLL Monitoring)"]},
                    {"id": "lymph_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Repeat FBC + blood film in 6-8 weeks, urgent haematology if red flags"}
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
    seed_lymphocytosis()