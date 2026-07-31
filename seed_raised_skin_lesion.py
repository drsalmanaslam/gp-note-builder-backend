from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_raised_skin_lesion():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Raised Skin Lesion",
        "description": "Comprehensive assessment for raised skin lesions covering benign vs malignant differentiation, clinical clues, and urgent referral criteria.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Malignancy Screen",
                "section_type": "history",
                "questions": [
                    {"id": "rsl_non_healing", "type": "toggle", "label": "Non-Healing Lesion (>4-6 Weeks)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Non-healing >4-6 weeks = ?BCC/SCC. Urgent dermatology referral.", "red_flag_negative": ""},
                    {"id": "rsl_persistent_bleeding", "type": "toggle", "label": "Persistent Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Persistent bleeding = ?malignancy. Urgent referral.", "red_flag_negative": ""},
                    {"id": "rsl_rapid_enlargement", "type": "toggle", "label": "Rapid Enlargement?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Rapid growth = ?keratoacanthoma, SCC, amelanotic melanoma. Urgent referral.", "red_flag_negative": ""},
                    {"id": "rsl_colour_change", "type": "toggle", "label": "Colour Change (Black/Brown/Variegated)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Variegated pigmentation = ?melanoma. Urgent 2WW referral.", "red_flag_negative": ""},
                    {"id": "rsl_irregular_borders", "type": "toggle", "label": "Irregular Borders?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Irregular borders = ?malignancy. Urgent referral.", "red_flag_negative": ""},
                    {"id": "rsl_satellite", "type": "toggle", "label": "Satellite Lesions?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Satellite lesions = ?metastatic melanoma. Urgent 2WW.", "red_flag_negative": ""},
                    {"id": "rsl_numbness", "type": "toggle", "label": "Numbness or Altered Sensation?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Altered sensation = ?perineural invasion (SCC). Urgent referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Presenting Complaint",
                "section_type": "history",
                "questions": [
                    {"id": "rsl_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Raised lesion on cheek noticed 2 months ago"},
                    {"id": "rsl_first_noticed", "type": "text", "label": "When First Noticed", "required": True, "placeholder": "e.g., 2 months ago"},
                    {"id": "rsl_change", "type": "multi_select", "label": "Change Noted", "required": True, "options": ["Increase in size", "Change in shape", "Change in colour", "Becoming more raised", "No change - stable"]},
                    {"id": "rsl_number", "type": "single_select", "label": "Single or Multiple", "required": True, "options": ["Single lesion", "Multiple lesions"]},
                    {"id": "rsl_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Gradual", "Sudden"]}
                ]
            },
            {
                "title": "Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "rsl_pain", "type": "toggle", "label": "Pain or Tenderness?", "required": True},
                    {"id": "rsl_itch", "type": "toggle", "label": "Itching?", "required": True},
                    {"id": "rsl_bleeding", "type": "toggle", "label": "Bleeding?", "required": True},
                    {"id": "rsl_ulceration", "type": "toggle", "label": "Ulceration or Crusting?", "required": True},
                    {"id": "rsl_discharge", "type": "toggle", "label": "Discharge?", "required": False},
                    {"id": "rsl_trauma", "type": "toggle", "label": "Recurrent Trauma to the Area?", "required": False},
                    {"id": "rsl_rapid_growth", "type": "toggle", "label": "Rapid Growth?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Rapid growth = ?keratoacanthoma, SCC. Urgent referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "rsl_previous_skin_ca", "type": "toggle", "label": "Previous Skin Cancer?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Previous skin cancer = high risk for second primary.", "red_flag_negative": ""},
                    {"id": "rsl_family_melanoma", "type": "toggle", "label": "Family History of Melanoma?", "required": True},
                    {"id": "rsl_sun_exposure", "type": "toggle", "label": "Excessive Sun Exposure / Sunburns?", "required": True},
                    {"id": "rsl_fitzpatrick", "type": "single_select", "label": "Fitzpatrick Skin Type", "required": False, "options": ["Type I-II (Fair - High Risk)", "Type III-IV", "Type V-VI"]},
                    {"id": "rsl_immunosuppression", "type": "toggle", "label": "Immunosuppression?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunosuppressed = higher skin cancer risk. Lower threshold for referral.", "red_flag_negative": ""},
                    {"id": "rsl_previous_rt", "type": "toggle", "label": "Previous Radiotherapy?", "required": False},
                    {"id": "rsl_outdoor_occupation", "type": "toggle", "label": "Outdoor Occupation?", "required": False}
                ]
            },
            {
                "title": "Systemic Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "rsl_weight_loss", "type": "toggle", "label": "Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + skin lesion = ?metastatic disease.", "red_flag_negative": ""},
                    {"id": "rsl_night_sweats", "type": "toggle", "label": "Night Sweats?", "required": True},
                    {"id": "rsl_fatigue", "type": "toggle", "label": "Fatigue?", "required": False},
                    {"id": "rsl_lymph_nodes", "type": "toggle", "label": "Enlarged Lymph Nodes?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy + skin lesion = ?metastatic spread. Urgent referral.", "red_flag_negative": ""},
                    {"id": "rsl_fever", "type": "toggle", "label": "Fever? (?Infective Cause)", "required": False}
                ]
            },
            {
                "title": "Examination - Clinical Clues",
                "section_type": "examination",
                "questions": [
                    {"id": "rsl_site", "type": "text", "label": "Site of Lesion", "required": True, "placeholder": "e.g., Left cheek"},
                    {"id": "rsl_size", "type": "number", "label": "Size (mm)", "required": False, "placeholder": "e.g., 8"},
                    {"id": "rsl_colour", "type": "single_select", "label": "Colour", "required": True, "options": ["Flesh-coloured", "Pearly / Translucent (BCC)", "Red / Vascular", "Brown / Black / Variegated (Melanoma)", "Waxy / Yellowish (Seborrhoeic Keratosis)", "Scaly / Rough (Actinic Keratosis/SCC)"]},
                    {"id": "rsl_clinical_clues", "type": "multi_select", "label": "Clinical Clues on Examination", "required": True, "options": ["Central punctum (?Epidermoid Cyst)", "Keratin plug (?Keratoacanthoma)", "Hard horn (?Cutaneous Horn)", "Pearly rolled edge (?BCC)", "Stuck-on appearance (?Seborrhoeic Keratosis)", "Dimple sign (?Dermatofibroma)", "Soft + mobile (?Lipoma)", "Bleeds easily (?Pyogenic Granuloma / Malignancy)", "Variegated pigmentation (?Melanoma)", "Warty/verrucous surface (?Viral Wart)", "None of these"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Seborrhoeic Keratosis (Waxy, Stuck-On, Asymptomatic, Older Patient)",
                    "Dermatofibroma (Firm Nodule, Post-Trauma, Dimple Sign)",
                    "Skin Tag / Acrochordon (Soft, Flesh-Coloured, Friction Areas)",
                    "Viral Wart (Rough Surface, Slowly Enlarging, Contagious)",
                    "Epidermoid Cyst (Central Punctum, Intermittent Inflammation)",
                    "Lipoma (Soft, Mobile, Painless, Slowly Enlarging)",
                    "Keratoacanthoma (Rapid Growth, Dome-Shaped, Central Keratin Plug)",
                    "Cutaneous Horn (Hard Keratin Projection, Underlying Lesion May Be Malignant)",
                    "Actinic Keratosis (Rough, Scaly, Sun-Exposed Skin, Pre-Malignant)",
                    "Basal Cell Carcinoma (Pearly, Rolled Edge, Recurrent Bleeding, Non-Healing)",
                    "Squamous Cell Carcinoma (Tender, Enlarging, Keratotic, Ulceration)",
                    "Melanoma (Changing Pigmented Lesion, Irregular Colours, Bleeding/Itching)",
                    "Pyogenic Granuloma (Rapid Red Vascular Lesion, Bleeds Easily)",
                    "Cherry Angioma (Bright Red Papule, Stable, Asymptomatic)",
                    "Kerion / Furuncle / Abscess (Painful, Inflamed, Acute Onset)"
                ],
                "questions": [
                    {"id": "rsl_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Benign Lesion - Reassure (SK / Dermatofibroma / Skin Tag / Lipoma / Cyst)", "Benign Lesion - Diagnostic Uncertainty (Routine Dermatology)", "Pre-Malignant (Actinic Keratosis) - Treat", "Suspected BCC - Urgent Referral", "Suspected SCC - Urgent Referral", "Suspected Melanoma - Urgent 2WW", "Infective / Inflammatory - Treat Accordingly"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: lesion changes (size, shape, colour), becomes symptomatic (pain, itch, bleeding), or new lesions appear nearby. RED FLAGS for urgent referral: non-healing >4-6 weeks, persistent bleeding, rapid enlargement, colour change (black/brown/variegated), irregular borders, satellite lesions, numbness/altered sensation. If benign features: reassure + safety-net. If diagnostic uncertainty: routine dermatology referral. If red flags present: urgent 2WW dermatology per local pathway. Document size, site, colour, and clinical clues. Photograph if available for monitoring.",
                "questions": [
                    {"id": "rsl_referral", "type": "single_select", "label": "Referral", "required": True, "options": ["None - Benign, Reassure + Safety-Net", "Routine Dermatology (Diagnostic Uncertainty)", "Urgent 2WW Dermatology (Suspected Malignancy)", "Cryotherapy / Topical Treatment (Actinic Keratosis / Wart)"]},
                    {"id": "rsl_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if changes, routine review 3-6 months, or urgent referral pathway"}
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
    seed_raised_skin_lesion()