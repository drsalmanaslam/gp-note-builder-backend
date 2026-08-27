from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_seborrhoeic_dermatitis():
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
        "title": "Seborrhoeic Dermatitis Assessment & Management",
        "description": "Practical GP assessment and treatment guide for seborrhoeic dermatitis, including scalp, face, and flexural involvement.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "sebderm_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Red scaly patches on face for 2 months",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "sebderm_duration",
                        "type": "text",
                        "label": "Duration of Symptoms",
                        "required": True,
                        "placeholder": "e.g., 2 months",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "sebderm_onset",
                        "type": "single_select",
                        "label": "Onset",
                        "required": True,
                        "options": ["Gradual", "Sudden", "Recent", "Recurrent"],
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "sebderm_sites",
                        "type": "multi_select",
                        "label": "Affected Sites",
                        "required": True,
                        "options": [
                            "Scalp",
                            "Face (centre)",
                            "Nasolabial folds",
                            "Glabella",
                            "Eyebrows",
                            "Ears (external/retroauricular)",
                            "Upper trunk (sternum)",
                            "Axillae/armpits",
                            "Groin folds",
                            "Submammary (if female)",
                            "Other"
                        ],
                        "output_phrase": "Sites: {value}"
                    },
                    {
                        "id": "sebderm_symptoms",
                        "type": "multi_select",
                        "label": "Symptoms",
                        "required": True,
                        "options": ["Itching", "Scaling", "Dryness", "Oily skin", "Flaking", "Redness", "Blepharitis (scaly eyelids)", "None"],
                        "output_phrase": "Symptoms: {value}"
                    },
                    {
                        "id": "sebderm_seasonal",
                        "type": "single_select",
                        "label": "Seasonal Variation",
                        "required": False,
                        "options": ["Worse in winter", "Improves in summer", "No variation"],
                        "output_phrase": "Seasonal: {value}"
                    },
                    {
                        "id": "sebderm_triggers",
                        "type": "multi_select",
                        "label": "Triggers",
                        "required": False,
                        "options": ["Stress", "Lack of sleep", "Cold weather", "Hormonal changes", "Medications", "None"],
                        "output_phrase": "Triggers: {value}"
                    },
                    {
                        "id": "sebderm_previous_treatments",
                        "type": "textarea",
                        "label": "Previous Treatments",
                        "required": False,
                        "placeholder": "e.g., Hydrocortisone cream, Nizoral shampoo",
                        "output_phrase": "Previous tx: {value}"
                    },
                    {
                        "id": "sebderm_medical_history",
                        "type": "multi_select",
                        "label": "Associated Conditions",
                        "required": False,
                        "options": [
                            "Parkinson's disease",
                            "Depression/anxiety",
                            "HIV/immunosuppression",
                            "Psoriasis",
                            "Neurological disorder",
                            "Oily skin (seborrhea)",
                            "None"
                        ],
                        "output_phrase": "Associated: {value}"
                    },
                    {
                        "id": "sebderm_medications",
                        "type": "textarea",
                        "label": "Current Medications",
                        "required": False,
                        "placeholder": "e.g., Neuroleptics, steroids, immunosuppressants",
                        "output_phrase": "Medications: {value}"
                    },
                    {
                        "id": "sebderm_eye_symptoms",
                        "type": "multi_select",
                        "label": "Ocular Symptoms",
                        "required": False,
                        "options": ["Dry eyes", "Sore eyes", "Gritty sensation", "Red eyelids", "None", "Not applicable"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Ocular symptoms - consider blepharitis. Clean eyelids and consider lubricating eye drops.",
                        "red_flag_negative": "",
                        "output_phrase": "Ocular: {value}"
                    },
                    {
                        "id": "sebderm_impact",
                        "type": "single_select",
                        "label": "Impact on Quality of Life",
                        "required": False,
                        "options": ["Minimal", "Moderate - some social impact", "Severe - significant psychological impact"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Significant psychological impact - consider dermatology referral / psychological support.",
                        "red_flag_negative": "",
                        "output_phrase": "QoL impact: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "sebderm_face",
                        "type": "textarea",
                        "label": "Facial Examination",
                        "required": True,
                        "placeholder": "e.g., Well-demarcated erythematous patches with greasy yellowish scales on centre of face, nasolabial folds, eyebrows",
                        "output_phrase": "Face: {value}"
                    },
                    {
                        "id": "sebderm_scalp",
                        "type": "textarea",
                        "label": "Scalp Examination",
                        "required": False,
                        "placeholder": "e.g., Diffuse scaly patches, dandruff, erythema",
                        "output_phrase": "Scalp: {value}"
                    },
                    {
                        "id": "sebderm_ears",
                        "type": "textarea",
                        "label": "Ear Examination",
                        "required": False,
                        "placeholder": "e.g., Scaling on external ear, retroauricular involvement",
                        "output_phrase": "Ears: {value}"
                    },
                    {
                        "id": "sebderm_trunk",
                        "type": "textarea",
                        "label": "Trunk / Flexural Examination",
                        "required": False,
                        "placeholder": "e.g., Salmon-pink patches on sternum, axillae, groin",
                        "output_phrase": "Trunk: {value}"
                    },
                    {
                        "id": "sebderm_skin_type",
                        "type": "single_select",
                        "label": "Skin Type (Fitzpatrick)",
                        "required": False,
                        "options": ["I - Very fair", "II - Fair", "III - Medium", "IV - Olive", "V - Brown", "VI - Dark"],
                        "output_phrase": "Skin type: {value}"
                    },
                    {
                        "id": "sebderm_blepharitis",
                        "type": "single_select",
                        "label": "Blepharitis Present?",
                        "required": False,
                        "options": ["None", "Mild - scaly eyelid margins", "Moderate - with erythema", "Severe - with crusting"],
                        "output_phrase": "Blepharitis: {value}"
                    },
                    {
                        "id": "sebderm_other",
                        "type": "textarea",
                        "label": "Other Examination Findings",
                        "required": False,
                        "placeholder": "e.g., Nail changes, joint involvement if psoriasis suspected",
                        "output_phrase": "Other: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Seborrhoeic dermatitis (most common)",
                    "Psoriasis (sebopsoriasis may overlap)",
                    "Atopic dermatitis/eczema",
                    "Contact dermatitis (allergic/irritant)",
                    "Rosacea (may coexist)",
                    "Tinea faciei / dermatophyte infection",
                    "Lupus erythematosus (discoid)",
                    "Pityriasis versicolor (trunk)",
                    "Dermatomyositis",
                    "Pellagra (rare)"
                ],
                "questions": [
                    {
                        "id": "sebderm_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Diagnosis",
                        "required": True,
                        "options": [
                            "Seborrhoeic dermatitis",
                            "Sebopsoriasis (overlap with psoriasis)",
                            "Atopic dermatitis (eczema)",
                            "Rosacea",
                            "Contact dermatitis",
                            "Uncertain - consider dermatology referral"
                        ],
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "sebderm_severity",
                        "type": "single_select",
                        "label": "Severity",
                        "required": True,
                        "options": [
                            "Mild - limited scaling, minimal erythema",
                            "Moderate - significant scaling/erythema, some impact",
                            "Severe - extensive involvement, significant impact",
                            "Refractory - poor response to standard treatment"
                        ],
                        "output_phrase": "Severity: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: Condition worsens or fails to respond to treatment, develops extensive involvement, significant psychological distress, or signs of secondary infection. Seborrhoeic dermatitis is a chronic relapsing condition - advise patient about long-term maintenance therapy.",
                "questions": [
                    {
                        "id": "sebderm_education",
                        "type": "multi_select",
                        "label": "Patient Education Given",
                        "required": True,
                        "options": [
                            "Leaflet given (DermNet or equivalent)",
                            "Explained - chronic relapsing condition",
                            "Lifestyle factors - stress, sleep, diet",
                            "Skincare routine advice",
                            "Avoid aggressive scrubbing",
                            "All above"
                        ],
                        "output_phrase": "Education: {value}"
                    },
                    {
                        "id": "sebderm_scalp_treatment",
                        "type": "multi_select",
                        "label": "Scalp Treatment",
                        "required": False,
                        "options": [
                            "Nizoral shampoo (ketoconazole) 2-4x/week → maintenance 2-weekly",
                            "Vichy Dercos shampoo (selenium 1% + salicylic acid 1%)",
                            "Stieprox shampoo (ciclopirox)",
                            "Betacap (betamethasone) scalp application - if inflamed",
                            "Dermovate scalp application - if severe",
                            "Tea tree oil shampoo (alternative)",
                            "None"
                        ],
                        "output_phrase": "Scalp tx: {value}"
                    },
                    {
                        "id": "sebderm_face_treatment",
                        "type": "multi_select",
                        "label": "Face/Chest Treatment",
                        "required": False,
                        "options": [
                            "Nizoral cream (ketoconazole) - if no inflammation",
                            "Daktarin cream (miconazole) - less irritant option",
                            "Canesten cream (clotrimazole) - less irritant option",
                            "Canesten HC (clotrimazole + hydrocortisone) - if inflamed x 2 weeks",
                            "Eumovate cream - if very inflamed (max 2 days)",
                            "Protopic 0.1% (tacrolimus) - steroid-sparing, 4 weeks then maintenance",
                            "Terbinafine 1% cream - if refractory, daily x 7-14 days",
                            "None"
                        ],
                        "output_phrase": "Face tx: {value}"
                    },
                    {
                        "id": "sebderm_trunk_treatment",
                        "type": "multi_select",
                        "label": "Trunk/Flexural Treatment",
                        "required": False,
                        "options": [
                            "Nizoral cream",
                            "Canesten HC - if inflamed",
                            "Eumovate - if very inflamed (max 2 days)",
                            "Selsun shampoo (selenium) - apply to dry skin, leave 15 minutes",
                            "Protopic 0.1% - steroid-sparing",
                            "None"
                        ],
                        "output_phrase": "Trunk tx: {value}"
                    },
                    {
                        "id": "sebderm_ocular",
                        "type": "multi_select",
                        "label": "Ocular/Eyelid Treatment",
                        "required": False,
                        "options": [
                            "Clean eyelids with cooled boiled water/cotton wool",
                            "Artificial tears - liberally through the day",
                            "Lubricating ointment - nocte if needed",
                            "None needed"
                        ],
                        "output_phrase": "Ocular tx: {value}"
                    },
                    {
                        "id": "sebderm_refractory",
                        "type": "multi_select",
                        "label": "Refractory Case Options",
                        "required": False,
                        "options": [
                            "Terbinafine 1% cream daily x 7-14 days",
                            "Selsun shampoo weekly (apply to dry skin 15 minutes)",
                            "Oral itraconazole (specialist)",
                            "Phototherapy (specialist)",
                            "Low-dose oral isotretinoin (specialist)",
                            "None"
                        ],
                        "output_phrase": "Refractory tx: {value}"
                    },
                    {
                        "id": "sebderm_steroid_taper",
                        "type": "toggle",
                        "label": "Steroid Tapering Plan Explained?",
                        "required": False,
                        "output_phrase": "Steroid taper: {value}"
                    },
                    {
                        "id": "sebderm_maintenance",
                        "type": "textarea",
                        "label": "Maintenance Plan",
                        "required": False,
                        "placeholder": "e.g., Nizoral shampoo 2-weekly, Protopic twice weekly, avoid triggers",
                        "output_phrase": "Maintenance: {value}"
                    },
                    {
                        "id": "sebderm_referral",
                        "type": "single_select",
                        "label": "Referral Plan",
                        "required": True,
                        "options": [
                            "No referral needed",
                            "Dermatology (routine) - if refractory",
                            "Dermatology (urgent) - if severe/atypical",
                            "Ophthalmology - if significant ocular involvement",
                            "None"
                        ],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "sebderm_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "Review in 4 weeks (treatment response)",
                            "Review in 8 weeks",
                            "Review in 3 months (if stable)",
                            "As needed",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "sebderm_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, lifestyle advice, psychological impact",
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
    seed_seborrhoeic_dermatitis()