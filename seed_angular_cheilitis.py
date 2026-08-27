from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_angular_cheilitis():
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
        "title": "Angular Cheilitis Assessment & Management",
        "description": "Comprehensive assessment and treatment guide for angular cheilitis, including swab guidance, predisposing factors, and treatment escalation.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "ac_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Painful cracked corners of mouth for 3 weeks",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "ac_duration",
                        "type": "text",
                        "label": "Duration of Symptoms",
                        "required": True,
                        "placeholder": "e.g., 3 weeks",
                        "output_phrase": "Duration: {value}"
                    },
                    {
                        "id": "ac_onset",
                        "type": "single_select",
                        "label": "Onset",
                        "required": True,
                        "options": ["Sudden", "Gradual", "Recurrent"],
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "ac_symptoms",
                        "type": "multi_select",
                        "label": "Symptoms",
                        "required": True,
                        "options": ["Pain", "Cracking/fissuring", "Bleeding", "Burning", "Itching", "Scaling", "Swelling", "None"],
                        "output_phrase": "Symptoms: {value}"
                    },
                    {
                        "id": "ac_red_flags",
                        "type": "multi_select",
                        "label": "Red Flag Screen",
                        "required": True,
                        "options": [
                            "Unilateral lesion - RED FLAG (reconsider diagnosis)",
                            "Indurated lesion - RED FLAG (consider malignancy)",
                            "Ulcerated/bleeding - RED FLAG",
                            "Persistent >3 weeks despite treatment - RED FLAG",
                            "Atypical appearance - RED FLAG",
                            "None"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: {value} - reconsider diagnosis. Consider swab + specialist referral. Unilateral/indurated/ulcerated = rule out SCC or other pathology.",
                        "red_flag_negative": "",
                        "output_phrase": "Red flags: {value}"
                    },
                    {
                        "id": "ac_previous_treatments",
                        "type": "textarea",
                        "label": "Previous Treatments Tried",
                        "required": False,
                        "placeholder": "e.g., Miconazole 2% cream 2 weeks, no improvement",
                        "output_phrase": "Previous tx: {value}"
                    },
                    {
                        "id": "ac_predisposing_factors",
                        "type": "multi_select",
                        "label": "Predisposing Factors",
                        "required": True,
                        "options": [
                            "Iron deficiency (ferritin low)",
                            "B12/folate deficiency",
                            "Denture wearer / denture stomatitis",
                            "Saliva pooling / angular drooling",
                            "Lip licking habit",
                            "Contact dermatitis (toothpaste/cosmetics)",
                            "Oral candidiasis",
                            "Diabetes",
                            "Immunosuppression",
                            "None identified"
                        ],
                        "output_phrase": "Predisposing factors: {value}"
                    },
                    {
                        "id": "ac_denture_status",
                        "type": "single_select",
                        "label": "Denture Status (if applicable)",
                        "required": False,
                        "options": ["No dentures", "Wears dentures - well-fitting", "Wears dentures - ill-fitting", "Denture stomatitis present"],
                        "output_phrase": "Dentures: {value}"
                    },
                    {
                        "id": "ac_medical_history",
                        "type": "textarea",
                        "label": "Relevant Medical History",
                        "required": False,
                        "placeholder": "e.g., Diabetes, immunosuppression, pernicious anaemia",
                        "output_phrase": "PMH: {value}"
                    },
                    {
                        "id": "ac_medications",
                        "type": "textarea",
                        "label": "Current Medications",
                        "required": False,
                        "placeholder": "e.g., Warfarin, phenytoin, sulfonylureas (caution with miconazole)",
                        "output_phrase": "Medications: {value}"
                    },
                    {
                        "id": "ac_warfarin",
                        "type": "toggle",
                        "label": "On Warfarin? (caution with miconazole interaction)",
                        "required": False,
                        "output_phrase": "Warfarin: {value}"
                    },
                    {
                        "id": "ac_phenytoin",
                        "type": "toggle",
                        "label": "On Phenytoin? (caution with miconazole interaction)",
                        "required": False,
                        "output_phrase": "Phenytoin: {value}"
                    },
                    {
                        "id": "ac_sulphonylurea",
                        "type": "toggle",
                        "label": "On Sulphonylurea? (caution with miconazole interaction)",
                        "required": False,
                        "output_phrase": "Sulphonylurea: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "ac_lesion_description",
                        "type": "textarea",
                        "label": "Lesion Description",
                        "required": True,
                        "placeholder": "e.g., Bilateral fissures at angles of mouth, erythematous, scaling",
                        "output_phrase": "Lesion: {value}"
                    },
                    {
                        "id": "ac_unilateral_bilateral",
                        "type": "single_select",
                        "label": "Unilateral or Bilateral?",
                        "required": True,
                        "options": ["Bilateral", "Unilateral - RED FLAG (reconsider diagnosis)"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unilateral lesion - consider SCC, HSV, or other pathology. Urgent review/dermatology referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Laterality: {value}"
                    },
                    {
                        "id": "ac_induration",
                        "type": "single_select",
                        "label": "Induration/Palpability",
                        "required": True,
                        "options": ["Soft/non-indurated", "Indurated/firm - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Indurated lesion - consider malignancy. Urgent dermatology referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Induration: {value}"
                    },
                    {
                        "id": "ac_ulceration",
                        "type": "single_select",
                        "label": "Ulceration/Bleeding",
                        "required": True,
                        "options": ["No ulceration", "Ulcerated/bleeding - RED FLAG"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Ulcerated/bleeding lesion - consider SCC. Urgent dermatology/oral medicine referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Ulceration: {value}"
                    },
                    {
                        "id": "ac_mouth_exam",
                        "type": "textarea",
                        "label": "Oral Examination",
                        "required": False,
                        "placeholder": "e.g., No oral candidiasis, denture stomatitis present",
                        "output_phrase": "Oral exam: {value}"
                    },
                    {
                        "id": "ac_oral_candidiasis",
                        "type": "toggle",
                        "label": "Oral Candidiasis Present?",
                        "required": False,
                        "output_phrase": "Oral candidiasis: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Angular cheilitis (Candida +/− Staphylococcus)",
                    "Candidal angular cheilitis (most common)",
                    "Bacterial angular cheilitis (Staph aureus, Strep)",
                    "Mixed fungal/bacterial",
                    "Contact dermatitis (toothpaste/cosmetics)",
                    "Nutritional deficiency (iron, B12, folate)",
                    "Lip licker's dermatitis",
                    "Herpes simplex (unilateral/vesicular)",
                    "Squamous cell carcinoma (unilateral, indurated, ulcerated) - RED FLAG",
                    "Actinic cheilitis",
                    "Crohn's disease (uncommon)"
                ],
                "questions": [
                    {
                        "id": "ac_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Impression",
                        "required": True,
                        "options": [
                            "Angular cheilitis - likely fungal (Candida)",
                            "Angular cheilitis - likely bacterial (Staph aureus)",
                            "Angular cheilitis - mixed fungal/bacterial",
                            "Contact dermatitis",
                            "Nutritional deficiency",
                            "Atypical - reconsider diagnosis - RED FLAG",
                            "Malignancy suspected - RED FLAG"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Atypical/malignancy suspected - urgent dermatology/oral medicine referral.",
                        "red_flag_negative": "",
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "ac_severity",
                        "type": "single_select",
                        "label": "Severity",
                        "required": True,
                        "options": ["Mild - minimal symptoms", "Moderate - symptomatic but manageable", "Severe - significantly inflamed/painful", "Refractory - >3 weeks no improvement on treatment"],
                        "output_phrase": "Severity: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return/urgent if: Lesion becomes unilateral, indurated, ulcerated, or bleeding. No improvement despite 3 weeks of appropriate treatment. New systemic symptoms. Unilateral lesions need urgent dermatology referral to rule out SCC. If on warfarin, phenytoin, or sulfonylureas, use miconazole with caution (interaction risk). Avoid repeated antimicrobial courses - swab and refer if refractory.",
                "questions": [
                    {
                        "id": "ac_swab",
                        "type": "toggle",
                        "label": "Swab Performed? (Bacterial culture + sensitivity, fungal culture if Candida suspected)",
                        "required": False,
                        "output_phrase": "Swab: {value}"
                    },
                    {
                        "id": "ac_swab_result",
                        "type": "text",
                        "label": "Swab Results (if available)",
                        "required": False,
                        "placeholder": "e.g., Staph aureus grown, sensitive to flucloxacillin",
                        "output_phrase": "Swab result: {value}"
                    },
                    {
                        "id": "ac_investigations",
                        "type": "multi_select",
                        "label": "Investigations Requested",
                        "required": False,
                        "options": [
                            "FBC",
                            "Ferritin/Iron studies",
                            "B12",
                            "Folate",
                            "Glucose/HbA1c",
                            "None at this time"
                        ],
                        "output_phrase": "Investigations: {value}"
                    },
                    {
                        "id": "ac_treatment_antifungal",
                        "type": "single_select",
                        "label": "Antifungal Treatment (if Candida suspected)",
                        "required": False,
                        "options": [
                            "Miconazole 2% cream - apply thin layer 12-hourly x 10-14 days",
                            "Miconazole + hydrocortisone 1% (Daktacort) - short course, use steroid briefly",
                            "Nystatin cream",
                            "Not indicated",
                            "None"
                        ],
                        "output_phrase": "Antifungal: {value}"
                    },
                    {
                        "id": "ac_treatment_antibacterial",
                        "type": "single_select",
                        "label": "Antibacterial Treatment (if bacterial infection suspected)",
                        "required": False,
                        "options": [
                            "Sodium fusidate 2% cream/ointment - every 6 hours x 7 days",
                            "Mupirocin ointment",
                            "Culture-directed antibiotics",
                            "Not indicated",
                            "None"
                        ],
                        "output_phrase": "Antibacterial: {value}"
                    },
                    {
                        "id": "ac_treatment_combination",
                        "type": "toggle",
                        "label": "Combination (antifungal + antibacterial) prescribed?",
                        "required": False,
                        "output_phrase": "Combination therapy: {value}"
                    },
                    {
                        "id": "ac_treatment_barrier",
                        "type": "multi_select",
                        "label": "Barrier/Symptomatic Treatment",
                        "required": False,
                        "options": [
                            "Petrolatum/Paraffin ointment (regular barrier)",
                            "Zinc oxide cream",
                            "Avoid lip licking",
                            "Avoid irritants (cosmetics, toothpaste)",
                            "None"
                        ],
                        "output_phrase": "Barrier tx: {value}"
                    },
                    {
                        "id": "ac_medication_counselling",
                        "type": "textarea",
                        "label": "Medication Counselling",
                        "required": False,
                        "placeholder": "e.g., Caution if on warfarin - INR monitoring, apply thinly to angles only",
                        "output_phrase": "Counselling: {value}"
                    },
                    {
                        "id": "ac_referral",
                        "type": "single_select",
                        "label": "Referral Plan",
                        "required": True,
                        "options": [
                            "No referral needed",
                            "Dermatology (routine) - if refractory",
                            "Dermatology (urgent) - RED FLAG cases",
                            "Oral Medicine",
                            "Dentistry (denture stomatitis/fit)",
                            "Dietitian (nutritional deficiency)",
                            "None"
                        ],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "ac_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "Review in 2 weeks (treatment response)",
                            "Review in 4 weeks (if stable)",
                            "Review after swab results",
                            "As needed - stable",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "ac_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, lifestyle advice, denture hygiene",
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
    seed_angular_cheilitis()