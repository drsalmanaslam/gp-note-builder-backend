from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_goitre():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Endocrinology").first()
    if not category: category = Category(name="Endocrinology"); db.add(category); db.commit()

    t = {
        "title": "Goitre / Thyroid Enlargement",
        "description": "Focused assessment for goitre covering hyper/hypothyroid screening, examination, red flags, and investigation pathway.",
        "category": "Endocrinology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "goi_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Neck swelling noticed for 2 months"},
                    {"id": "goi_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 45"},
                    {"id": "goi_presentation", "type": "single_select", "label": "How Presented", "required": True, "options": ["Neck swelling", "Neck pain", "Voice change / Hoarseness", "Incidental finding"]},
                    {"id": "goi_duration", "type": "single_select", "label": "Duration of Swelling", "required": True, "options": ["<1 week", "1-2 weeks", "3 weeks", ">3 months"]},
                    {"id": "goi_preceding_illness", "type": "toggle", "label": "Preceding Illness / Infection?", "required": False},
                    {"id": "goi_breathing", "type": "toggle", "label": "Effect on Breathing?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Breathing difficulty = ?tracheal compression from large goitre. Urgent ENT/surgical assessment.", "red_flag_negative": ""},
                    {"id": "goi_swallowing", "type": "toggle", "label": "Effect on Swallowing (Dysphagia)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dysphagia = ?oesophageal compression. Urgent ENT + imaging.", "red_flag_negative": ""},
                    {"id": "goi_voice_change", "type": "toggle", "label": "Voice Change / Hoarseness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hoarseness = ?recurrent laryngeal nerve involvement. Urgent ENT + ?malignancy.", "red_flag_negative": ""},
                    {"id": "goi_diet", "type": "multi_select", "label": "Relevant Dietary History", "required": False, "options": ["High iodine intake", "Dairy products", "Goitrogenic foods (cruciferous veg, soy)", "None reported"]}
                ]
            },
            {
                "title": "Hyperthyroid Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "goi_hyper_weight_loss", "type": "toggle", "label": "Weight Loss?", "required": False},
                    {"id": "goi_hyper_anxiety", "type": "toggle", "label": "Anxiety / Irritability?", "required": False},
                    {"id": "goi_hyper_tremor", "type": "toggle", "label": "Tremor?", "required": False},
                    {"id": "goi_hyper_palpitations", "type": "toggle", "label": "Palpitations?", "required": False},
                    {"id": "goi_hyper_heat", "type": "toggle", "label": "Heat Intolerance / Sweating?", "required": False},
                    {"id": "goi_hyper_menstrual", "type": "toggle", "label": "Menstrual Disturbance?", "required": False}
                ]
            },
            {
                "title": "Hypothyroid Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "goi_hypo_weight_gain", "type": "toggle", "label": "Weight Gain?", "required": False},
                    {"id": "goi_hypo_lethargy", "type": "toggle", "label": "Lethargy / Fatigue?", "required": False},
                    {"id": "goi_hypo_hoarse", "type": "toggle", "label": "Hoarse Voice?", "required": False},
                    {"id": "goi_hypo_dry_skin", "type": "toggle", "label": "Dry Skin / Hair Loss?", "required": False},
                    {"id": "goi_hypo_constipation", "type": "toggle", "label": "Constipation?", "required": False},
                    {"id": "goi_hypo_menstrual", "type": "toggle", "label": "Menstrual Disturbance?", "required": False},
                    {"id": "goi_family", "type": "multi_select", "label": "Family History", "required": False, "options": ["Thyroid disease", "Diabetes mellitus", "Other autoimmune condition", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "goi_inspection", "type": "single_select", "label": "Neck / Thyroid Inspection", "required": True, "options": ["Midline swelling", "Lateral swelling", "No visible swelling"]},
                    {"id": "goi_swallow_movement", "type": "toggle", "label": "Moves with Swallowing? (Thyroid origin)", "required": True},
                    {"id": "goi_tongue_movement", "type": "toggle", "label": "Moves with Tongue Protrusion? (Thyroglossal cyst)", "required": False},
                    {"id": "goi_bruit", "type": "toggle", "label": "Thyroid Bruit on Auscultation? (Graves')", "required": False},
                    {"id": "goi_hr", "type": "number", "label": "Pulse Rate (bpm)", "required": True, "placeholder": "e.g., 90"},
                    {"id": "goi_tremor", "type": "toggle", "label": "Fine Tremor?", "required": False},
                    {"id": "goi_eye_signs", "type": "multi_select", "label": "Eye Signs", "required": True, "options": ["Proptosis / Exophthalmos", "Lid lag", "Lid retraction", "Normal"]},
                    {"id": "goi_skin_hair", "type": "single_select", "label": "Skin / Hair", "required": False, "options": ["Abnormal (dry/oily)", "Normal"]},
                    {"id": "goi_proximal_myopathy", "type": "toggle", "label": "Proximal Myopathy? (Hyperthyroid)", "required": False},
                    {"id": "goi_reflexes", "type": "single_select", "label": "Reflexes", "required": False, "options": ["Brisk (hyperthyroid)", "Slow-relaxing (hypothyroid)", "Normal"]},
                    {"id": "goi_thyrotoxic_crisis", "type": "multi_select", "label": "Signs of Thyrotoxic Crisis?", "required": True, "options": ["Fever", "Agitation", "Confusion", "Heart failure", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Thyrotoxic crisis = EMERGENCY. Same-day hospital admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Simple / Colloid Goitre",
                    "Graves' Disease (hyperthyroid + eye signs + bruit)",
                    "Hashimoto's Thyroiditis (hypothyroid + firm goitre)",
                    "Multinodular Goitre",
                    "Solitary Thyroid Nodule",
                    "Thyroid Malignancy (RED FLAG - hoarseness, rapid growth, hard/fixed)",
                    "Thyroglossal Cyst (moves with tongue protrusion)",
                    "Subacute (De Quervain's) Thyroiditis (painful, post-viral)"
                ],
                "questions": [
                    {"id": "goi_tfts", "type": "toggle", "label": "TFTs Ordered? (TSH, Free T4)", "required": True},
                    {"id": "goi_antibodies", "type": "toggle", "label": "Thyroid Autoantibodies? (Anti-TPO, Anti-Tg, TSH-R Ab)", "required": False},
                    {"id": "goi_uss", "type": "toggle", "label": "Ultrasound Thyroid Requested?", "required": False},
                    {"id": "goi_fna", "type": "toggle", "label": "Fine Needle Aspiration (FNA) Indicated?", "required": False},
                    {"id": "goi_isotope_scan", "type": "toggle", "label": "Radioisotope Scan Indicated?", "required": False}
                ]
            },
            {
                "title": "Assessment & Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: breathing difficulty, swallowing difficulty, voice change/hoarseness, or signs of thyrotoxic crisis (fever, agitation, confusion, palpitations). 2WW referral if: unexplained hoarseness, rapidly enlarging thyroid mass, hard/fixed nodule, or cervical lymphadenopathy. Ensure TFTs checked before starting Carbimazole/Levothyroxine. Propranolol can be used for symptomatic tremor/palpitations while awaiting results. If Graves' confirmed: refer ophthalmology for eye involvement.",
                "questions": [
                    {"id": "goi_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Simple / Colloid Goitre", "Graves' Disease", "Hashimoto's Thyroiditis", "Multinodular Goitre", "Goitre - cause undetermined, pending investigation", "Suspected malignancy - URGENT 2WW"]},
                    {"id": "goi_2ww", "type": "toggle", "label": "2-Week-Wait Referral Criteria Met?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: 2WW criteria met = urgent ENT referral. Do not delay for bloods.", "red_flag_negative": ""},
                    {"id": "goi_medication", "type": "single_select", "label": "Pharmacotherapy", "required": False, "options": ["None", "Propranolol (tremor/palpitations)", "Carbimazole (hyperthyroid)", "Levothyroxine (hypothyroid)"]},
                    {"id": "goi_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None", "Endocrinology", "Ophthalmology (Graves' eye disease)", "ENT (urgent 2WW)", "ENT (routine)"]},
                    {"id": "goi_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1-2 weeks with TFT results"}
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
    seed_goitre()