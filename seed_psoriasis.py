from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_psoriasis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: 
        category = Category(name="Dermatology")
        db.add(category)
        db.commit()

    t = {
        "title": "Psoriasis Assessment & Management",
        "description": "Comprehensive assessment and treatment guide for psoriasis with Irish-specific treatment options and site-based management.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "psoriasis_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Scaly red patches on elbows for 6 months",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "psoriasis_duration",
                        "type": "text",
                        "label": "Duration of Symptoms",
                        "required": True,
                        "placeholder": "e.g., 6 months",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "psoriasis_age_onset",
                        "type": "number",
                        "label": "Age at Onset",
                        "required": False,
                        "placeholder": "e.g., 25",
                        "output_phrase": "Age onset: {value}"
                    },
                    {
                        "id": "psoriasis_family_history",
                        "type": "toggle",
                        "label": "Family History of Psoriasis?",
                        "required": False,
                        "output_phrase": "Family history: {value}"
                    },
                    {
                        "id": "psoriasis_sites",
                        "type": "multi_select",
                        "label": "Affected Sites",
                        "required": True,
                        "options": ["Scalp", "Face", "Trunk", "Limbs", "Flexures", "Genital", "Nails", "Ears", "Hairline", "Palms/Soles"],
                        "output_phrase": "Sites: {value}"
                    },
                    {
                        "id": "psoriasis_symptoms",
                        "type": "multi_select",
                        "label": "Symptoms",
                        "required": True,
                        "options": ["Itching", "Pain", "Bleeding", "Scale/flaking", "Cosmetic concern", "Joint pain - ?Psoriatic arthritis", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Joint pain - consider psoriatic arthritis. Screen with CASPAR criteria.",
                        "red_flag_negative": "",
                        "output_phrase": "Symptoms: {value}"
                    },
                    {
                        "id": "psoriasis_triggers",
                        "type": "multi_select",
                        "label": "Identified Triggers",
                        "required": False,
                        "options": ["Stress", "Infection (e.g., Strep)", "Trauma (Koebner)", "Medications (e.g., lithium, beta-blockers)", "Alcohol", "Smoking", "None"],
                        "output_phrase": "Triggers: {value}"
                    },
                    {
                        "id": "psoriasis_previous_treatments",
                        "type": "textarea",
                        "label": "Previous Treatments",
                        "required": False,
                        "placeholder": "e.g., Enstilar, Betnovate, UVB phototherapy",
                        "output_phrase": "Previous tx: {value}"
                    },
                    {
                        "id": "psoriasis_smoking",
                        "type": "single_select",
                        "label": "Smoking Status",
                        "required": True,
                        "options": ["Non-smoker", "Ex-smoker", "Current smoker"],
                        "output_phrase": "Smoking: {value}"
                    },
                    {
                        "id": "psoriasis_alcohol",
                        "type": "single_select",
                        "label": "Alcohol Intake",
                        "required": False,
                        "options": ["None", "Within guidelines (<14 units/week)", "Excess (>14 units/week)"],
                        "output_phrase": "Alcohol: {value}"
                    },
                    {
                        "id": "psoriasis_bmi",
                        "type": "number",
                        "label": "BMI",
                        "required": False,
                        "placeholder": "e.g., 28",
                        "output_phrase": "BMI: {value}"
                    },
                    {
                        "id": "psoriasis_medications",
                        "type": "textarea",
                        "label": "Current Medications",
                        "required": False,
                        "placeholder": "e.g., Lithium, beta-blockers, NSAIDs",
                        "output_phrase": "Medications: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "psoriasis_exam_description",
                        "type": "textarea",
                        "label": "Description of Lesions",
                        "required": True,
                        "placeholder": "e.g., Well-demarcated erythematous plaques with silvery scale",
                        "output_phrase": "Lesions: {value}"
                    },
                    {
                        "id": "psoriasis_bsa",
                        "type": "single_select",
                        "label": "Body Surface Area (BSA) Affected",
                        "required": True,
                        "options": ["<3% (Mild)", "3-10% (Moderate)", ">10% (Severe) - consider dermatology referral"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: BSA >10% - consider dermatology referral for systemic therapy.",
                        "red_flag_negative": "",
                        "output_phrase": "BSA: {value}"
                    },
                    {
                        "id": "psoriasis_pasi",
                        "type": "text",
                        "label": "PASI Score (if available)",
                        "required": False,
                        "placeholder": "e.g., 8.4",
                        "output_phrase": "PASI: {value}"
                    },
                    {
                        "id": "psoriasis_nails",
                        "type": "textarea",
                        "label": "Nail Examination",
                        "required": False,
                        "placeholder": "e.g., Pitting, onycholysis, subungual hyperkeratosis",
                        "output_phrase": "Nails: {value}"
                    },
                    {
                        "id": "psoriasis_joints",
                        "type": "single_select",
                        "label": "Joint Examination",
                        "required": True,
                        "options": ["Normal", "Tender/swollen joints - consider psoriatic arthritis", "Signs of osteoarthritis", "Normal"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Tender/swollen joints - refer to rheumatology for psoriatic arthritis assessment.",
                        "red_flag_negative": "",
                        "output_phrase": "Joints: {value}"
                    },
                    {
                        "id": "psoriasis_enthesis",
                        "type": "toggle",
                        "label": "Enthesitis (pain at tendon insertion)?",
                        "required": False,
                        "output_phrase": "Enthesitis: {value}"
                    },
                    {
                        "id": "psoriasis_dactylitis",
                        "type": "toggle",
                        "label": "Dactylitis (sausage digit)?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Dactylitis - strongly suggestive of psoriatic arthritis.",
                        "red_flag_negative": "",
                        "output_phrase": "Dactylitis: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Plaque Psoriasis (most common)",
                    "Guttate Psoriasis (post-streptococcal)",
                    "Flexural Psoriasis (inverse)",
                    "Scalp Psoriasis",
                    "Nail Psoriasis",
                    "Psoriatic Arthritis",
                    "Eczema (may mimic flexural psoriasis)",
                    "Seborrhoeic Dermatitis (scalp/face)",
                    "Fungal Infection (tinea)",
                    "Lichen Planus",
                    "Pityriasis Rosea"
                ],
                "questions": [
                    {
                        "id": "psoriasis_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Diagnosis",
                        "required": True,
                        "options": ["Plaque psoriasis", "Guttate psoriasis", "Flexural/inverse psoriasis", "Scalp psoriasis", "Nail psoriasis", "Palmar/plantar psoriasis", "Combined", "Uncertain - consider referral"],
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "psoriasis_severity",
                        "type": "single_select",
                        "label": "Overall Severity",
                        "required": True,
                        "options": ["Mild (BSA <3%, QoL minimal impact)", "Moderate (BSA 3-10%)", "Severe (BSA >10% or significant QoL impact) - refer dermatology"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Severe psoriasis - consider dermatology referral for systemic therapy.",
                        "red_flag_negative": "",
                        "output_phrase": "Severity: {value}"
                    },
                    {
                        "id": "psoriasis_caspar",
                        "type": "single_select",
                        "label": "CASPAR Criteria for Psoriatic Arthritis",
                        "required": False,
                        "options": ["Satisfies CASPAR (≥3 points) - refer rheumatology", "Does not satisfy CASPAR", "Not assessed"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: CASPAR positive - urgent rheumatology referral.",
                        "red_flag_negative": "",
                        "output_phrase": "CASPAR: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: Worsening or extensive psoriasis despite treatment, significant joint pain/swelling (psoriatic arthritis), signs of infection (erythroderma, pustules), or severe psychological impact. Psoriasis is a chronic condition - treatment aims to control symptoms and improve quality of life. All patients should receive lifestyle advice: smoking cessation, moderation of alcohol, healthy weight (BMI <25), and regular exercise. Use liberal emollients regularly to reduce dryness, scale and itch. Explain that psoriasis is NOT infectious or contagious.",
                "questions": [
                    {
                        "id": "psoriasis_general_advice",
                        "type": "multi_select",
                        "label": "General Advice Given",
                        "required": True,
                        "options": [
                            "Education - chronic condition, not infectious",
                            "Smoking cessation advised",
                            "Alcohol moderation advised",
                            "Weight management/BMI reduction advised",
                            "Regular exercise advised",
                            "Emollients prescribed/recommended",
                            "Trigger identification advised"
                        ],
                        "output_phrase": "General advice: {value}"
                    },
                    {
                        "id": "psoriasis_emollient",
                        "type": "multi_select",
                        "label": "Emollient Recommended",
                        "required": False,
                        "options": ["Emulsifying Ointment BP", "White Soft Paraffin / Liquid Paraffin", "Epaderm", "Cetraben", "Dermol", "Doublebase", "La Roche-Posay Lipikar Baume AP+M", "Other", "None"],
                        "output_phrase": "Emollient: {value}"
                    },
                    {
                        "id": "psoriasis_site_trunk_limbs",
                        "type": "single_select",
                        "label": "Trunk/Limbs Treatment (Plaque Psoriasis)",
                        "required": False,
                        "options": ["Enstilar (calcipotriol + betamethasone foam) - once daily x 4 weeks", "Silkis (calcitriol) + Betnovate (potent steroid) short course", "Topical steroid only (Betnovate) - short course", "Coal tar preparation (if available)", "None required"],
                        "output_phrase": "Trunk/limbs: {value}"
                    },
                    {
                        "id": "psoriasis_site_thick_plaques",
                        "type": "single_select",
                        "label": "Thick Plaque Treatment",
                        "required": False,
                        "options": ["Salicylic acid 5-10% preparation", "Diprosalic (salicylic acid + steroid)", "Coal tar preparation", "Enstilar", "None"],
                        "output_phrase": "Thick plaques: {value}"
                    },
                    {
                        "id": "psoriasis_site_face",
                        "type": "single_select",
                        "label": "Face Treatment",
                        "required": False,
                        "options": ["Eumovate (clobetasone butyrate) - short course", "Protopic (tacrolimus) - steroid-sparing", "Emollient only", "None"],
                        "output_phrase": "Face: {value}"
                    },
                    {
                        "id": "psoriasis_site_flexures",
                        "type": "single_select",
                        "label": "Flexure Treatment",
                        "required": False,
                        "options": ["Eumovate (clobetasone butyrate) - short course", "Protopic (tacrolimus) - steroid-sparing", "Emollient only", "None"],
                        "output_phrase": "Flexures: {value}"
                    },
                    {
                        "id": "psoriasis_site_scalp",
                        "type": "multi_select",
                        "label": "Scalp Treatment",
                        "required": False,
                        "options": ["Keratolytic - salicylic acid 5-10% overnight", "Capasal shampoo (tar/keratolytic)", "Cocois / Sebco (if available)", "Dovobet gel (calcipotriol + betamethasone)", "Enstilar", "Betnovate Scalp Application", "Dermovate Scalp Application (very potent)", "Diprosalic (betamethasone + salicylic acid)", "None"],
                        "output_phrase": "Scalp: {value}"
                    },
                    {
                        "id": "psoriasis_site_hairline",
                        "type": "single_select",
                        "label": "Hairline Treatment",
                        "required": False,
                        "options": ["Eumovate - short course", "Emollient regularly", "Protopic (tacrolimus) - steroid-sparing", "None"],
                        "output_phrase": "Hairline: {value}"
                    },
                    {
                        "id": "psoriasis_site_ear",
                        "type": "single_select",
                        "label": "Ear Treatment",
                        "required": False,
                        "options": ["Betnesol drops (for ear canal) - if TM intact", "Topical steroid for external ear", "Emollient only", "None"],
                        "output_phrase": "Ear: {value}"
                    },
                    {
                        "id": "psoriasis_site_genital",
                        "type": "single_select",
                        "label": "Genital Treatment",
                        "required": False,
                        "options": ["Eumovate - short course", "Protopic (tacrolimus) - steroid-sparing", "Regular emollient", "None"],
                        "output_phrase": "Genital: {value}"
                    },
                    {
                        "id": "psoriasis_site_nails",
                        "type": "single_select",
                        "label": "Nail Treatment",
                        "required": False,
                        "options": ["Betnovate (limited nail disease)", "Dermovate Scalp Application (potent)", "Consider dermatology referral", "Fungal screen if needed", "None"],
                        "output_phrase": "Nails: {value}"
                    },
                    {
                        "id": "psoriasis_steroid_taper",
                        "type": "toggle",
                        "label": "Steroid tapering plan explained?",
                        "required": False,
                        "output_phrase": "Steroid taper: {value}"
                    },
                    {
                        "id": "psoriasis_referral",
                        "type": "multi_select",
                        "label": "Referrals",
                        "required": False,
                        "options": ["Dermatology (routine)", "Dermatology (urgent - erythroderma/pustular)", "Rheumatology (psoriatic arthritis suspected)", "None required"],
                        "output_phrase": "Referrals: {value}"
                    },
                    {
                        "id": "psoriasis_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": ["Review in 4-6 weeks (treatment response)", "Review in 3 months", "Review in 6 months (stable)", "As needed - stable", "Dermatology follow-up"],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "psoriasis_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, counselling, special considerations",
                        "output_phrase": "Notes: {value}"
                    }
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(
            title=t["title"], 
            description=t["description"], 
            category=t["category"], 
            content=t["content"], 
            is_public=True, 
            created_by=admin.id, 
            version=1
        )
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    
    db.close()

if __name__ == "__main__":
    seed_psoriasis()