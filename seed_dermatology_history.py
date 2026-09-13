from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_dermatology_history():
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
        "title": "Dermatology History & Examination",
        "description": "Comprehensive dermatology history and examination template. The vast majority of skin problems in GP can be diagnosed by taking a comprehensive history.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History of the Lesion or Rash",
                "section_type": "history",
                "questions": [
                    {
                        "id": "derm_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Itchy red rash on both arms for 2 weeks",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "derm_onset",
                        "type": "single_select",
                        "label": "Onset",
                        "required": True,
                        "options": ["Sudden", "Gradual", "Acute", "Chronic", "Recurrent"],
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "derm_duration",
                        "type": "text",
                        "label": "Duration",
                        "required": True,
                        "placeholder": "e.g., 2 weeks",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "derm_periodicity",
                        "type": "single_select",
                        "label": "Periodicity",
                        "required": False,
                        "options": ["Constant", "Intermittent", "Episodic", "Seasonal", "Cyclical"],
                        "output_phrase": "Periodicity: {value}"
                    },
                    {
                        "id": "derm_site_onset",
                        "type": "text",
                        "label": "Site of Onset",
                        "required": True,
                        "placeholder": "e.g., Started on forearms, now spreading to trunk",
                        "output_phrase": "Site of onset: {value}"
                    },
                    {
                        "id": "derm_spread",
                        "type": "single_select",
                        "label": "Spread",
                        "required": False,
                        "options": ["Localised", "Spreading", "Generalised", "Improving", "Static"],
                        "output_phrase": "Spread: {value}"
                    },
                    {
                        "id": "derm_distribution",
                        "type": "textarea",
                        "label": "Distribution",
                        "required": True,
                        "placeholder": "e.g., Symmetrical, extensor surfaces, flexural, dermatomal, sun-exposed areas",
                        "output_phrase": "Distribution: {value}"
                    },
                    {
                        "id": "derm_symptoms",
                        "type": "multi_select",
                        "label": "Associated Symptoms",
                        "required": True,
                        "options": ["Itching", "Pain", "Burning", "Bleeding", "Discharge", "Swelling", "Numbness", "None"],
                        "output_phrase": "Symptoms: {value}"
                    },
                    {
                        "id": "derm_aggravating",
                        "type": "multi_select",
                        "label": "Aggravating Factors",
                        "required": False,
                        "options": ["Heat", "Cold", "Sunlight", "Stress", "Certain foods", "Contact with irritants", "Medications", "Exercise", "None"],
                        "output_phrase": "Aggravating: {value}"
                    },
                    {
                        "id": "derm_relieving",
                        "type": "multi_select",
                        "label": "Relieving Factors",
                        "required": False,
                        "options": ["Emollients", "Topical steroids", "Antihistamines", "Cooling", "Avoiding triggers", "None"],
                        "output_phrase": "Relieving: {value}"
                    },
                    {
                        "id": "derm_evolution",
                        "type": "textarea",
                        "label": "Evolution / Progression",
                        "required": False,
                        "placeholder": "e.g., Started as small patch, now larger and more inflamed",
                        "output_phrase": "Evolution: {value}"
                    }
                ]
            },
            {
                "title": "Previous History & Family History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "derm_previous_skin_conditions",
                        "type": "multi_select",
                        "label": "Previous Dermatological Conditions",
                        "required": False,
                        "options": ["Eczema/Atopic dermatitis", "Psoriasis", "Acne", "Rosacea", "Fungal infection", "Contact dermatitis", "Urticaria", "Vitiligo", "None"],
                        "output_phrase": "Previous skin conditions: {value}"
                    },
                    {
                        "id": "derm_autoimmune",
                        "type": "multi_select",
                        "label": "Autoimmune Conditions",
                        "required": False,
                        "options": ["Lupus", "Rheumatoid arthritis", "Thyroid disease", "Inflammatory bowel disease", "Type 1 diabetes", "None"],
                        "output_phrase": "Autoimmune: {value}"
                    },
                    {
                        "id": "derm_hereditary",
                        "type": "multi_select",
                        "label": "Hereditary Conditions",
                        "required": False,
                        "options": ["Ichthyosis", "Epidermolysis bullosa", "Neurofibromatosis", "Tuberous sclerosis", "None"],
                        "output_phrase": "Hereditary: {value}"
                    },
                    {
                        "id": "derm_family_history",
                        "type": "textarea",
                        "label": "Family History of Skin Conditions",
                        "required": False,
                        "placeholder": "e.g., Mother has eczema, father has psoriasis",
                        "output_phrase": "Family history: {value}"
                    }
                ]
            },
            {
                "title": "Medications",
                "section_type": "history",
                "questions": [
                    {
                        "id": "derm_medications_oral",
                        "type": "textarea",
                        "label": "Oral Medications",
                        "required": False,
                        "placeholder": "e.g., Ramipril, atorvastatin, lithium, beta-blockers",
                        "output_phrase": "Oral meds: {value}"
                    },
                    {
                        "id": "derm_medications_topical",
                        "type": "textarea",
                        "label": "Topical Medications",
                        "required": False,
                        "placeholder": "e.g., Betnovate cream, Daktarin, emollients",
                        "output_phrase": "Topical meds: {value}"
                    },
                    {
                        "id": "derm_medications_otc",
                        "type": "textarea",
                        "label": "OTC Medications / Creams",
                        "required": False,
                        "placeholder": "e.g., Hydrocortisone 1%, E45, Sudocrem",
                        "output_phrase": "OTC meds: {value}"
                    },
                    {
                        "id": "derm_medications_others",
                        "type": "textarea",
                        "label": "Medications Applied to Others in Household",
                        "required": False,
                        "placeholder": "e.g., Using partner's topical steroid - risk of peri-orofacial dermatitis",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Inadvertent topical steroid use from others - consider peri-orofacial dermatitis.",
                        "red_flag_negative": "",
                        "output_phrase": "Household meds: {value}"
                    },
                    {
                        "id": "derm_recent_medication_changes",
                        "type": "toggle",
                        "label": "Recent Medication Changes?",
                        "required": False,
                        "output_phrase": "Recent changes: {value}"
                    }
                ]
            },
            {
                "title": "Allergies",
                "section_type": "history",
                "questions": [
                    {
                        "id": "derm_allergies_medication",
                        "type": "textarea",
                        "label": "Medication Allergies",
                        "required": False,
                        "placeholder": "e.g., Penicillin, NSAIDs",
                        "output_phrase": "Medication allergies: {value}"
                    },
                    {
                        "id": "derm_allergies_contact",
                        "type": "multi_select",
                        "label": "Contact Allergies / Sensitivities",
                        "required": False,
                        "options": ["Nickel", "Latex", "Fragrances", "Preservatives", "Hair dye", "Cosmetics", "None"],
                        "output_phrase": "Contact allergies: {value}"
                    },
                    {
                        "id": "derm_allergies_food",
                        "type": "textarea",
                        "label": "Food Allergies",
                        "required": False,
                        "placeholder": "e.g., Nuts, shellfish, eggs",
                        "output_phrase": "Food allergies: {value}"
                    }
                ]
            },
            {
                "title": "Social History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "derm_occupation",
                        "type": "text",
                        "label": "Occupational History",
                        "required": False,
                        "placeholder": "e.g., Healthcare worker, construction, hairdresser",
                        "output_phrase": "Occupation: {value}"
                    },
                    {
                        "id": "derm_sports_hobbies",
                        "type": "text",
                        "label": "Sports & Hobbies",
                        "required": False,
                        "placeholder": "e.g., Swimming, gardening, contact sports",
                        "output_phrase": "Sports/hobbies: {value}"
                    },
                    {
                        "id": "derm_animal_contact",
                        "type": "multi_select",
                        "label": "Animal Contacts",
                        "required": False,
                        "options": ["Dogs", "Cats", "Birds", "Rodents", "Farm animals", "None"],
                        "output_phrase": "Animal contact: {value}"
                    },
                    {
                        "id": "derm_travel",
                        "type": "text",
                        "label": "Travel History",
                        "required": False,
                        "placeholder": "e.g., Recent travel to tropical regions",
                        "output_phrase": "Travel: {value}"
                    },
                    {
                        "id": "derm_smoking",
                        "type": "single_select",
                        "label": "Smoking Status",
                        "required": False,
                        "options": ["Non-smoker", "Ex-smoker", "Current smoker"],
                        "output_phrase": "Smoking: {value}"
                    },
                    {
                        "id": "derm_alcohol",
                        "type": "single_select",
                        "label": "Alcohol Intake",
                        "required": False,
                        "options": ["None", "Within guidelines", "Excess (>14 units/week)"],
                        "output_phrase": "Alcohol: {value}"
                    },
                    {
                        "id": "derm_sexual_health",
                        "type": "single_select",
                        "label": "Sexual Health History",
                        "required": False,
                        "options": ["Not relevant", "Relevant - consider STI screen", "Known STI", "Declined to discuss"],
                        "output_phrase": "Sexual health: {value}"
                    }
                ]
            },
            {
                "title": "Psychological Stress",
                "section_type": "history",
                "questions": [
                    {
                        "id": "derm_stress_current",
                        "type": "single_select",
                        "label": "Current Stress Levels",
                        "required": False,
                        "options": ["Low", "Moderate", "High", "Severe"],
                        "output_phrase": "Stress: {value}"
                    },
                    {
                        "id": "derm_stress_impact",
                        "type": "textarea",
                        "label": "Impact of Skin Presentation on Psychological Wellbeing",
                        "required": False,
                        "placeholder": "e.g., Embarrassed, avoiding social situations, affecting work",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Significant psychological impact - consider psychological support, dermatology referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Psychological impact: {value}"
                    },
                    {
                        "id": "derm_stress_triggers",
                        "type": "toggle",
                        "label": "Stress Identified as Trigger for Skin Condition?",
                        "required": False,
                        "output_phrase": "Stress as trigger: {value}"
                    }
                ]
            },
            {
                "title": "Systematic Enquiry",
                "section_type": "history",
                "questions": [
                    {
                        "id": "derm_joint_pains",
                        "type": "multi_select",
                        "label": "Joint Pains (indicating arthropathy)",
                        "required": False,
                        "options": ["No joint pain", "Small joints (hands/feet)", "Large joints (knees/hips)", "Axial (spine)", "Morning stiffness", "Swelling/tenderness"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Joint pain - consider psoriatic arthritis, refer rheumatology.",
                        "red_flag_negative": "",
                        "output_phrase": "Joint pains: {value}"
                    },
                    {
                        "id": "derm_weight_loss",
                        "type": "toggle",
                        "label": "Weight Loss?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Weight loss - consider malignancy, systemic disease.",
                        "red_flag_negative": "",
                        "output_phrase": "Weight loss: {value}"
                    },
                    {
                        "id": "derm_systemic_symptoms",
                        "type": "multi_select",
                        "label": "Other Systemic Symptoms",
                        "required": False,
                        "options": ["Fever", "Night sweats", "Fatigue", "Malaise", "Lymphadenopathy", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Systemic symptoms - consider systemic disease, malignancy.",
                        "red_flag_negative": "",
                        "output_phrase": "Systemic symptoms: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "derm_general",
                        "type": "single_select",
                        "label": "General Appearance",
                        "required": True,
                        "options": ["Well", "Unwell", "Systemically unwell"],
                        "output_phrase": "General: {value}"
                    },
                    {
                        "id": "derm_lesion_description",
                        "type": "textarea",
                        "label": "Lesion Description (morphology)",
                        "required": True,
                        "placeholder": "e.g., Erythematous, scaly plaques with silvery scale, well-demarcated",
                        "output_phrase": "Lesion: {value}"
                    },
                    {
                        "id": "derm_distribution_exam",
                        "type": "textarea",
                        "label": "Distribution (examination)",
                        "required": True,
                        "placeholder": "e.g., Symmetrical, extensor surfaces, flexural, dermatomal",
                        "output_phrase": "Distribution: {value}"
                    },
                    {
                        "id": "derm_site",
                        "type": "multi_select",
                        "label": "Sites Involved",
                        "required": True,
                        "options": ["Scalp", "Face", "Trunk", "Arms", "Legs", "Hands", "Feet", "Nails", "Mucous membranes", "Flexures", "Genitalia", "Other"],
                        "output_phrase": "Sites: {value}"
                    },
                    {
                        "id": "derm_mucous_membranes",
                        "type": "single_select",
                        "label": "Mucous Membrane Involvement",
                        "required": False,
                        "options": ["None", "Oral", "Genital", "Ocular", "Multiple sites"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Mucous membrane involvement - consider erythema multiforme, SJS/TEN, pemphigus.",
                        "red_flag_negative": "",
                        "output_phrase": "Mucous membranes: {value}"
                    },
                    {
                        "id": "derm_nails",
                        "type": "textarea",
                        "label": "Nail Examination",
                        "required": False,
                        "placeholder": "e.g., Pitting, onycholysis, discolouration, thickening",
                        "output_phrase": "Nails: {value}"
                    },
                    {
                        "id": "derm_lymph_nodes",
                        "type": "single_select",
                        "label": "Lymph Node Examination",
                        "required": False,
                        "options": ["Normal", "Palpable - non-tender", "Palpable - tender", "Not assessed"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Lymphadenopathy - consider malignancy, infection.",
                        "red_flag_negative": "",
                        "output_phrase": "Lymph nodes: {value}"
                    },
                    {
                        "id": "derm_dermoscopic",
                        "type": "textarea",
                        "label": "Dermoscopic Findings (if performed)",
                        "required": False,
                        "placeholder": "e.g., Pigment network, vascular patterns",
                        "output_phrase": "Dermoscopy: {value}"
                    },
                    {
                        "id": "derm_red_flags_exam",
                        "type": "multi_select",
                        "label": "Red Flag Features on Examination",
                        "required": False,
                        "options": [
                            "Asymmetry",
                            "Border irregularity",
                            "Colour variation",
                            "Diameter >6mm",
                            "Evolving lesion",
                            "Ulceration",
                            "Bleeding",
                            "Induration",
                            "None"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: {value} - consider malignancy, urgent dermatology referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Red flag features: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Eczema/Atopic dermatitis",
                    "Psoriasis",
                    "Contact dermatitis (irritant/allergic)",
                    "Fungal infection (tinea, candidiasis)",
                    "Bacterial infection (impetigo, cellulitis)",
                    "Viral exanthem",
                    "Drug eruption",
                    "Urticaria",
                    "Rosacea",
                    "Acne vulgaris",
                    "Skin malignancy (BCC, SCC, melanoma)",
                    "Autoimmune (lupus, dermatomyositis)",
                    "Vasculitis"
                ],
                "questions": [
                    {
                        "id": "derm_clinical_impression",
                        "type": "textarea",
                        "label": "Clinical Impression",
                        "required": True,
                        "placeholder": "e.g., Likely plaque psoriasis, moderate severity",
                        "output_phrase": "Impression: {value}"
                    },
                    {
                        "id": "derm_severity",
                        "type": "single_select",
                        "label": "Severity",
                        "required": True,
                        "options": ["Mild", "Moderate", "Severe", "Life-threatening (SJS/TEN)"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Severe/life-threatening - urgent dermatology/ED referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Severity: {value}"
                    },
                    {
                        "id": "derm_diagnosis",
                        "type": "single_select",
                        "label": "Working Diagnosis",
                        "required": False,
                        "options": [
                            "Eczema/Atopic dermatitis",
                            "Psoriasis",
                            "Contact dermatitis",
                            "Fungal infection",
                            "Bacterial infection",
                            "Viral exanthem",
                            "Drug eruption",
                            "Urticaria",
                            "Rosacea",
                            "Acne",
                            "Skin malignancy suspected",
                            "Autoimmune",
                            "Vasculitis",
                            "Other",
                            "Uncertain - refer"
                        ],
                        "output_phrase": "Diagnosis: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return/urgent if: Lesion changes (size, shape, colour, bleeding, ulceration), new systemic symptoms (fever, weight loss, joint pain), mucous membrane involvement, rapidly spreading rash, or significant psychological impact. If malignancy suspected, urgent dermatology referral.",
                "questions": [
                    {
                        "id": "derm_investigations",
                        "type": "multi_select",
                        "label": "Investigations Requested",
                        "required": False,
                        "options": [
                            "Skin swab (bacterial/fungal)",
                            "Skin scrape (fungal)",
                            "Bloods (FBC, CRP, ESR, autoimmune screen)",
                            "Patch testing",
                            "Skin biopsy",
                            "Dermoscopy",
                            "None"
                        ],
                        "output_phrase": "Investigations: {value}"
                    },
                    {
                        "id": "derm_treatment",
                        "type": "multi_select",
                        "label": "Treatment",
                        "required": False,
                        "options": [
                            "Emollients",
                            "Topical steroid",
                            "Topical antifungal",
                            "Topical antibiotic",
                            "Oral antihistamine",
                            "Oral antibiotic",
                            "Oral antifungal",
                            "Oral steroid",
                            "Phototherapy",
                            "None"
                        ],
                        "output_phrase": "Treatment: {value}"
                    },
                    {
                        "id": "derm_referral",
                        "type": "single_select",
                        "label": "Referral Plan",
                        "required": True,
                        "options": [
                            "No referral needed",
                            "Dermatology (routine)",
                            "Dermatology (urgent - ?malignancy)",
                            "Rheumatology (if joint involvement)",
                            "Allergy/immunology",
                            "None"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Urgent dermatology referral required - ?malignancy.",
                        "red_flag_negative": "",
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "derm_patient_education",
                        "type": "multi_select",
                        "label": "Patient Education Given",
                        "required": False,
                        "options": [
                            "Condition explanation",
                            "Trigger avoidance",
                            "Emollient use",
                            "Medication application technique",
                            "Sun protection",
                            "Psychological support",
                            "All above"
                        ],
                        "output_phrase": "Education: {value}"
                    },
                    {
                        "id": "derm_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "No follow-up needed",
                            "Review in 2 weeks",
                            "Review in 4 weeks",
                            "Review in 3 months",
                            "As needed",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "derm_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, lifestyle advice, shared decision-making",
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
    seed_dermatology_history()