from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_keratosis_pilaris():
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
        "title": "Keratosis Pilaris Assessment & Management",
        "description": "Practical GP assessment and management of keratosis pilaris, including reassurance, emollients, and treatment options.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "kp_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Rough bumps on arms for several years",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "kp_duration",
                        "type": "text",
                        "label": "Duration of Symptoms",
                        "required": True,
                        "placeholder": "e.g., Since childhood",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "kp_age_onset",
                        "type": "text",
                        "label": "Age at Onset",
                        "required": False,
                        "placeholder": "e.g., 5 years old",
                        "output_phrase": "Age onset: {value}"
                    },
                    {
                        "id": "kp_sites",
                        "type": "multi_select",
                        "label": "Affected Sites",
                        "required": True,
                        "options": [
                            "Upper arms (posterior)",
                            "Thighs (anterior)",
                            "Buttocks",
                            "Lower back",
                            "Chest",
                            "Face/eyebrows",
                            "Other"
                        ],
                        "output_phrase": "Sites: {value}"
                    },
                    {
                        "id": "kp_symptoms",
                        "type": "multi_select",
                        "label": "Symptoms",
                        "required": True,
                        "options": ["Rough texture", "Goose bump appearance", "Itching", "Redness around bumps", "Dryness", "Cosmetic concern", "None"],
                        "output_phrase": "Symptoms: {value}"
                    },
                    {
                        "id": "kp_seasonal",
                        "type": "single_select",
                        "label": "Seasonal Variation",
                        "required": False,
                        "options": ["Worse in winter", "Improves in summer", "No variation"],
                        "output_phrase": "Seasonal: {value}"
                    },
                    {
                        "id": "kp_associated_conditions",
                        "type": "multi_select",
                        "label": "Associated Conditions",
                        "required": False,
                        "options": ["Atopic eczema", "Ichthyosis vulgaris", "Asthma", "Hay fever", "None"],
                        "output_phrase": "Associated: {value}"
                    },
                    {
                        "id": "kp_family_history",
                        "type": "toggle",
                        "label": "Family History of Keratosis Pilaris?",
                        "required": False,
                        "output_phrase": "Family history: {value}"
                    },
                    {
                        "id": "kp_previous_treatments",
                        "type": "textarea",
                        "label": "Previous Treatments",
                        "required": False,
                        "placeholder": "e.g., Moisturisers, urea creams, exfoliators",
                        "output_phrase": "Previous tx: {value}"
                    },
                    {
                        "id": "kp_impact",
                        "type": "single_select",
                        "label": "Impact on Quality of Life",
                        "required": False,
                        "options": ["Minimal", "Moderate - some cosmetic concern", "Severe - significant psychological impact"],
                        "output_phrase": "QoL impact: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "kp_description",
                        "type": "textarea",
                        "label": "Lesion Description",
                        "required": True,
                        "placeholder": "e.g., Multiple 1-2mm follicular papules, keratotic plugs, rough texture, erythema around follicles",
                        "output_phrase": "Lesions: {value}"
                    },
                    {
                        "id": "kp_distribution",
                        "type": "textarea",
                        "label": "Distribution/Extent",
                        "required": True,
                        "placeholder": "e.g., Bilateral posterior upper arms, anterior thighs, mild erythema",
                        "output_phrase": "Distribution: {value}"
                    },
                    {
                        "id": "kp_skin_type",
                        "type": "single_select",
                        "label": "Skin Type",
                        "required": False,
                        "options": ["Dry", "Normal", "Oily", "Sensitive"],
                        "output_phrase": "Skin type: {value}"
                    },
                    {
                        "id": "kp_erythema",
                        "type": "single_select",
                        "label": "Erythema/Redness Present?",
                        "required": False,
                        "options": ["None", "Mild", "Moderate", "Significant"],
                        "output_phrase": "Erythema: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Keratosis pilaris (most common)",
                    "Follicular eczema",
                    "Lichen spinulosus",
                    "Folliculitis",
                    "Keratosis pilaris rubra (with erythema)",
                    "Phrynoderma (vitamin A deficiency - rare)",
                    "Milia",
                    "Acne vulgaris"
                ],
                "questions": [
                    {
                        "id": "kp_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Diagnosis",
                        "required": True,
                        "options": [
                            "Keratosis pilaris (typical)",
                            "Keratosis pilaris rubra (with erythema)",
                            "Follicular eczema",
                            "Folliculitis",
                            "Uncertain - consider dermatology referral"
                        ],
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "kp_severity",
                        "type": "single_select",
                        "label": "Severity",
                        "required": True,
                        "options": [
                            "Mild - limited extent, minimal cosmetic concern",
                            "Moderate - widespread, some cosmetic concern",
                            "Severe - extensive, significant erythema, psychological impact"
                        ],
                        "output_phrase": "Severity: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Reassure patient that keratosis pilaris is harmless, not infectious, and considered one end of the normal spectrum of skin changes. It often improves in adulthood. Treatments improve appearance temporarily but do not cure the condition. If significant psychological impact or severe erythema, consider dermatology referral for further options.",
                "questions": [
                    {
                        "id": "kp_reassurance",
                        "type": "multi_select",
                        "label": "Reassurance/Education Given",
                        "required": True,
                        "options": [
                            "Explained - considered normal spectrum of skin changes",
                            "Explained - very common in children/teens",
                            "Explained - not infectious",
                            "Explained - often improves in adulthood",
                            "Explained - may improve in summer",
                            "Leaflet given (BAD or equivalent)",
                            "All above"
                        ],
                        "output_phrase": "Reassurance: {value}"
                    },
                    {
                        "id": "kp_general_measures",
                        "type": "multi_select",
                        "label": "General Measures Advised",
                        "required": True,
                        "options": [
                            "Use mild soaps or soap substitutes",
                            "Apply emollients frequently",
                            "Tepid rather than hot showers/baths",
                            "Gentle exfoliation - may help",
                            "Sun protection (SPF 30+) - Elave 30 SPF or similar",
                            "All above"
                        ],
                        "output_phrase": "General measures: {value}"
                    },
                    {
                        "id": "kp_emollients",
                        "type": "multi_select",
                        "label": "Emollients/Topical Treatments",
                        "required": False,
                        "options": [
                            "Eucerin Urea Repair 5% urea - face",
                            "CeraVe SA Smoothing Cream 10% urea + salicylic acid",
                            "Calmurid 10% urea cream - body",
                            "Neostrata Lotion Plus 15% glycolic acid - body (more expensive)",
                            "CeraVe SA Smoothing Cleanser",
                            "Standard emollient (e.g., Cetraben, Epaderm)",
                            "None"
                        ],
                        "output_phrase": "Emollients: {value}"
                    },
                    {
                        "id": "kp_topical_retinoid",
                        "type": "single_select",
                        "label": "Topical Retinoid Considered?",
                        "required": False,
                        "options": [
                            "Not indicated at this time",
                            "Consider topical retinoid (e.g., tretinoin, adapalene) - specialist/off-label",
                            "Referred for specialist consideration",
                            "Patient declined"
                        ],
                        "output_phrase": "Topical retinoid: {value}"
                    },
                    {
                        "id": "kp_vascular",
                        "type": "single_select",
                        "label": "Intense Pulsed Light (IPL) Referral Considered?",
                        "required": False,
                        "options": [
                            "Not indicated",
                            "Consider IPL for vascular component/erythema - referral to dermatology",
                            "Referred for dermatology assessment",
                            "Patient declined"
                        ],
                        "output_phrase": "IPL referral: {value}"
                    },
                    {
                        "id": "kp_referral",
                        "type": "single_select",
                        "label": "Referral Plan",
                        "required": True,
                        "options": [
                            "No referral needed - reassure and advise",
                            "Dermatology (routine) - if significant erythema/impact",
                            "Dermatology (routine) - if refractory",
                            "None"
                        ],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "kp_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "No follow-up needed - reassured",
                            "Review in 3 months (if treatment trial started)",
                            "Review in 6 months",
                            "As needed",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "kp_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, lifestyle advice, psychological support",
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
    seed_keratosis_pilaris()