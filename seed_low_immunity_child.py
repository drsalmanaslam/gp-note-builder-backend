from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_low_immunity_child():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: 
        category = Category(name="Paediatrics")
        db.add(category)
        db.commit()

    t = {
        "title": "Child Recurrent Infections / ?Immunodeficiency",
        "description": "Practical GP assessment for children presenting with recurrent infections or parental concern about 'low immunity', including red flags, growth, and investigation pathways.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "History of Infections",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Recurrent chest infections, parent worried about low immunity",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "childimmunity_age_onset",
                        "type": "text",
                        "label": "Age at Onset of Infections",
                        "required": True,
                        "placeholder": "e.g., From 2 years old, increasing frequency",
                        "output_phrase": "Age onset: {value}"
                    },
                    {
                        "id": "childimmunity_frequency",
                        "type": "text",
                        "label": "Frequency of Infections (per year)",
                        "required": True,
                        "placeholder": "e.g., 8-10 URTIs per year",
                        "output_phrase": "Frequency: {value}"
                    },
                    {
                        "id": "childimmunity_infection_type",
                        "type": "multi_select",
                        "label": "Type/Site of Infections",
                        "required": True,
                        "options": [
                            "URTI (colds/sore throat)",
                            "Otitis media",
                            "Sinusitis",
                            "Tonsillitis",
                            "Pneumonia",
                            "UTI",
                            "Skin infection/abscess",
                            "Diarrhoea",
                            "Thrush (oral/genital)",
                            "Other"
                        ],
                        "output_phrase": "Infection type: {value}"
                    },
                    {
                        "id": "childimmunity_pneumonia_count",
                        "type": "number",
                        "label": "Number of Pneumonias (lifetime)",
                        "required": False,
                        "placeholder": "e.g., 2",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Recurrent pneumonia - consider immunodeficiency, foreign body, structural lung disease.",
                        "red_flag_negative": "",
                        "output_phrase": "Pneumonia episodes: {value}"
                    },
                    {
                        "id": "childimmunity_severity",
                        "type": "textarea",
                        "label": "Severity / Complications",
                        "required": False,
                        "placeholder": "e.g., Hospital admissions, IV antibiotics, sepsis, PICU stay",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Severe infections requiring PICU/IV antibiotics - consider immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "Severity: {value}"
                    },
                    {
                        "id": "childimmunity_antibiotic_response",
                        "type": "single_select",
                        "label": "Response to Antibiotics",
                        "required": True,
                        "options": ["Good response", "Partial response", "Poor response - consider ?immunodeficiency", "Variable"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Poor response to antibiotics - consider immunodeficiency, resistance, or unusual organism.",
                        "red_flag_negative": "",
                        "output_phrase": "Antibiotic response: {value}"
                    },
                    {
                        "id": "childimmunity_unusual_organisms",
                        "type": "text",
                        "label": "Unusual/Opportunistic Organisms",
                        "required": False,
                        "placeholder": "e.g., Aspergillus, Pneumocystis, atypical mycobacteria",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unusual/opportunistic organisms - strongly suggests immunodeficiency, refer Paediatric Immunology.",
                        "red_flag_negative": "",
                        "output_phrase": "Unusual organisms: {value}"
                    },
                    {
                        "id": "childimmunity_recovery",
                        "type": "single_select",
                        "label": "Complete Recovery Between Infections?",
                        "required": True,
                        "options": ["Yes - full recovery", "No - persistent symptoms", "Not sure"],
                        "output_phrase": "Recovery: {value}"
                    },
                    {
                        "id": "childimmunity_persistent_infection",
                        "type": "toggle",
                        "label": "Persistent Infection Despite Treatment?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Persistent infection despite treatment - consider immunodeficiency, structural cause.",
                        "red_flag_negative": "",
                        "output_phrase": "Persistent infection: {value}"
                    }
                ]
            },
            {
                "title": "Growth and Development",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_birth_history",
                        "type": "textarea",
                        "label": "Birth History",
                        "required": False,
                        "placeholder": "e.g., Term, normal delivery, no NICU stay",
                        "output_phrase": "Birth history: {value}"
                    },
                    {
                        "id": "childimmunity_weight_centile",
                        "type": "text",
                        "label": "Weight Centile",
                        "required": False,
                        "placeholder": "e.g., 25th centile",
                        "output_phrase": "Weight: {value}"
                    },
                    {
                        "id": "childimmunity_height_centile",
                        "type": "text",
                        "label": "Height/Length Centile",
                        "required": False,
                        "placeholder": "e.g., 50th centile",
                        "output_phrase": "Height: {value}"
                    },
                    {
                        "id": "childimmunity_growth_trajectory",
                        "type": "single_select",
                        "label": "Growth Trajectory",
                        "required": True,
                        "options": ["Following centile", "Crossing centiles downwards - RED FLAG", "Crossing centiles upwards", "Uncertain"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Faltering growth/crossing centiles downwards - consider immunodeficiency, malabsorption, chronic infection.",
                        "red_flag_negative": "",
                        "output_phrase": "Growth trajectory: {value}"
                    },
                    {
                        "id": "childimmunity_failure_to_thrive",
                        "type": "toggle",
                        "label": "Failure to Thrive / Poor Weight Gain?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Failure to thrive - consider immunodeficiency, GI pathology, chronic infection.",
                        "red_flag_negative": "",
                        "output_phrase": "Failure to thrive: {value}"
                    },
                    {
                        "id": "childimmunity_development",
                        "type": "single_select",
                        "label": "Development Appropriate for Age?",
                        "required": True,
                        "options": ["Yes - appropriate", "No - concerns", "Not assessed"],
                        "output_phrase": "Development: {value}"
                    },
                    {
                        "id": "childimmunity_appetite",
                        "type": "single_select",
                        "label": "Appetite",
                        "required": False,
                        "options": ["Good", "Poor", "Variable"],
                        "output_phrase": "Appetite: {value}"
                    },
                    {
                        "id": "childimmunity_diarrhoea",
                        "type": "toggle",
                        "label": "Chronic Diarrhoea / Vomiting?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Chronic diarrhoea/vomiting - consider immunodeficiency, malabsorption, IBD.",
                        "red_flag_negative": "",
                        "output_phrase": "Chronic diarrhoea: {value}"
                    }
                ]
            },
            {
                "title": "Immunodeficiency Red Flags",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_red_flags",
                        "type": "multi_select",
                        "label": "Immunodeficiency Red Flag Screen",
                        "required": True,
                        "options": [
                            "Persistent/recurrent thrush - RED FLAG",
                            "Recurrent pneumonia - RED FLAG",
                            "Deep/recurrent abscesses - RED FLAG",
                            "Unusual/opportunistic infections - RED FLAG",
                            "Persistent infection despite treatment - RED FLAG",
                            "Poor response to antibiotics - RED FLAG",
                            "Persistent lymphadenopathy - RED FLAG",
                            "Hepatosplenomegaly - RED FLAG",
                            "Failure to thrive - RED FLAG",
                            "None"
                        ],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: {value} - urgent paediatric/immunology assessment required.",
                        "red_flag_negative": "",
                        "output_phrase": "Red flags: {value}"
                    }
                ]
            },
            {
                "title": "Social / Environmental History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_creche",
                        "type": "toggle",
                        "label": "Attends Crèche / School?",
                        "required": False,
                        "output_phrase": "Crèche/school: {value}"
                    },
                    {
                        "id": "childimmunity_siblings",
                        "type": "text",
                        "label": "Siblings / Household Exposure",
                        "required": False,
                        "placeholder": "e.g., 2 siblings, both have frequent infections",
                        "output_phrase": "Household: {value}"
                    },
                    {
                        "id": "childimmunity_smoking",
                        "type": "toggle",
                        "label": "Passive Smoke Exposure?",
                        "required": False,
                        "output_phrase": "Passive smoking: {value}"
                    },
                    {
                        "id": "childimmunity_travel",
                        "type": "text",
                        "label": "Recent Travel",
                        "required": False,
                        "placeholder": "e.g., Tropical/subtropical, specific countries",
                        "output_phrase": "Travel: {value}"
                    }
                ]
            },
            {
                "title": "Past Medical History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_chronic_disease",
                        "type": "textarea",
                        "label": "Chronic Disease",
                        "required": False,
                        "placeholder": "e.g., Asthma, congenital heart disease, cystic fibrosis",
                        "output_phrase": "Chronic disease: {value}"
                    },
                    {
                        "id": "childimmunity_previous_hospitalisations",
                        "type": "textarea",
                        "label": "Previous Significant Infections / Hospitalisations",
                        "required": False,
                        "placeholder": "e.g., Bronchiolitis, pneumonia, meningitis",
                        "output_phrase": "Previous hospitalisations: {value}"
                    },
                    {
                        "id": "childimmunity_asplenia",
                        "type": "toggle",
                        "label": "Asplenia / Splenectomy?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Asplenia - risk of encapsulated organisms, ensure vaccinations and antibiotic prophylaxis.",
                        "red_flag_negative": "",
                        "output_phrase": "Asplenia: {value}"
                    },
                    {
                        "id": "childimmunity_other_conditions",
                        "type": "textarea",
                        "label": "Other Relevant Conditions",
                        "required": False,
                        "placeholder": "e.g., Allergies, eczema",
                        "output_phrase": "Other conditions: {value}"
                    }
                ]
            },
            {
                "title": "Medication History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_steroids",
                        "type": "single_select",
                        "label": "Steroids",
                        "required": False,
                        "options": ["No", "Yes - inhaled only", "Yes - systemic", "Yes - previous systemic"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Systemic steroids - immunosuppressed, increased infection risk.",
                        "red_flag_negative": "",
                        "output_phrase": "Steroids: {value}"
                    },
                    {
                        "id": "childimmunity_immunosuppressants",
                        "type": "multi_select",
                        "label": "Immunosuppressant Medications",
                        "required": False,
                        "options": ["Methotrexate", "Azathioprine", "Biologics", "Rituximab", "Other", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Immunosuppressants - increased infection risk, consider specialist advice.",
                        "red_flag_negative": "",
                        "output_phrase": "Immunosuppressants: {value}"
                    },
                    {
                        "id": "childimmunity_other_meds",
                        "type": "textarea",
                        "label": "Other Relevant Medications",
                        "required": False,
                        "placeholder": "e.g., Prophylactic antibiotics",
                        "output_phrase": "Other meds: {value}"
                    }
                ]
            },
            {
                "title": "Vaccinations",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_vaccinations",
                        "type": "toggle",
                        "label": "Routine Vaccinations Up to Date?",
                        "required": True,
                        "output_phrase": "Vaccinations up to date: {value}"
                    },
                    {
                        "id": "childimmunity_bcg",
                        "type": "toggle",
                        "label": "BCG Given?",
                        "required": False,
                        "output_phrase": "BCG: {value}"
                    },
                    {
                        "id": "childimmunity_vaccine_reactions",
                        "type": "text",
                        "label": "Unusual Vaccine Reactions",
                        "required": False,
                        "placeholder": "e.g., Fever, local reaction, allergic response",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unusual vaccine reactions - consider immunodeficiency, consult immunology.",
                        "red_flag_negative": "",
                        "output_phrase": "Vaccine reactions: {value}"
                    }
                ]
            },
            {
                "title": "Family History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "childimmunity_family_immunodeficiency",
                        "type": "toggle",
                        "label": "Family History of Known Immunodeficiency?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Family history of immunodeficiency - consider genetic/primary immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "Family immunodeficiency: {value}"
                    },
                    {
                        "id": "childimmunity_family_recurrent_infections",
                        "type": "toggle",
                        "label": "Family History of Recurrent/Unusual Infections?",
                        "required": False,
                        "output_phrase": "Family recurrent infections: {value}"
                    },
                    {
                        "id": "childimmunity_consanguinity",
                        "type": "toggle",
                        "label": "Consanguinity (Parents Related)?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Consanguinity - increased risk of autosomal recessive immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "Consanguinity: {value}"
                    },
                    {
                        "id": "childimmunity_family_child_deaths",
                        "type": "toggle",
                        "label": "Unexplained Childhood Deaths in Family?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unexplained childhood deaths - consider hereditary immunodeficiency or other genetic conditions.",
                        "red_flag_negative": "",
                        "output_phrase": "Family child deaths: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "childimmunity_general",
                        "type": "single_select",
                        "label": "General Appearance",
                        "required": True,
                        "options": ["Well", "Unwell", "Malnourished/cachectic - RED FLAG", "Well nourished"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Malnourished/cachectic - consider chronic disease, immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "General: {value}"
                    },
                    {
                        "id": "childimmunity_weight",
                        "type": "text",
                        "label": "Weight / Height / Centiles",
                        "required": False,
                        "placeholder": "e.g., Weight 18kg (50th centile), Height 110cm (50th centile)",
                        "output_phrase": "Anthropometry: {value}"
                    },
                    {
                        "id": "childimmunity_growth_development_exam",
                        "type": "textarea",
                        "label": "Growth / Development Assessment",
                        "required": False,
                        "placeholder": "e.g., Developmental milestones appropriate",
                        "output_phrase": "Growth/Dev: {value}"
                    },
                    {
                        "id": "childimmunity_ent",
                        "type": "textarea",
                        "label": "ENT / Ears / Tonsils Examination",
                        "required": False,
                        "placeholder": "e.g., Enlarged tonsils, otitis media, sinus tenderness",
                        "output_phrase": "ENT: {value}"
                    },
                    {
                        "id": "childimmunity_oral",
                        "type": "textarea",
                        "label": "Oral Cavity / Thrush Examination",
                        "required": False,
                        "placeholder": "e.g., Oral thrush, mucosal lesions",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Oral thrush in child >1 year - consider immunodeficiency, HIV.",
                        "red_flag_negative": "",
                        "output_phrase": "Oral: {value}"
                    },
                    {
                        "id": "childimmunity_lymph_nodes",
                        "type": "textarea",
                        "label": "Lymph Node Examination",
                        "required": False,
                        "placeholder": "e.g., Small cervical nodes <1cm, non-tender",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Persistent lymphadenopathy - consider malignancy, HIV, immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "Lymph nodes: {value}"
                    },
                    {
                        "id": "childimmunity_chest",
                        "type": "textarea",
                        "label": "Chest Examination",
                        "required": False,
                        "placeholder": "e.g., Clear, crackles, wheeze",
                        "output_phrase": "Chest: {value}"
                    },
                    {
                        "id": "childimmunity_skin",
                        "type": "textarea",
                        "label": "Skin Examination (abscesses, eczema, rashes)",
                        "required": False,
                        "placeholder": "e.g., Eczema, fungal infections, petechiae",
                        "output_phrase": "Skin: {value}"
                    },
                    {
                        "id": "childimmunity_abdomen",
                        "type": "textarea",
                        "label": "Abdomen Examination",
                        "required": False,
                        "placeholder": "e.g., Hepatosplenomegaly, masses",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Hepatosplenomegaly - consider lymphoma, HIV, TB, storage disease.",
                        "red_flag_negative": "",
                        "output_phrase": "Abdomen: {value}"
                    }
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Normal variation - frequent infections in young children (most common)",
                    "Crèche/school exposure (high infection frequency)",
                    "Atopic disease (asthma, eczema - increased infections)",
                    "Secondary immunodeficiency (malnutrition, HIV, chronic disease)",
                    "Medication-induced immunosuppression",
                    "Primary immunodeficiency (rare - consider if red flags, unusual infections)",
                    "Structural cause (bronchiectasis, chronic sinusitis, anatomical defect)",
                    "Cystic fibrosis (recurrent chest infections)",
                    "HIV infection",
                    "Other genetic/immune conditions"
                ],
                "questions": [
                    {
                        "id": "childimmunity_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Impression",
                        "required": True,
                        "options": [
                            "Likely normal variation - frequent infections in young child",
                            "Secondary immunodeficiency - investigate underlying cause",
                            "Primary immunodeficiency suspected - refer Paediatric Immunology",
                            "Structural cause suspected - consider specialist review",
                            "Red flags present - urgent investigation required",
                            "Uncertain - proceed with initial investigations"
                        ],
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "childimmunity_clinical_suspicion",
                        "type": "single_select",
                        "label": "Clinical Suspicion Level",
                        "required": True,
                        "options": ["Low - reassuring, thriving child", "Moderate - some concern but no red flags", "High - red flags present"],
                        "output_phrase": "Suspicion level: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return/urgent if: Infections become more frequent or severe, fail to respond to treatment, require hospitalisation or IV antibiotics, or unusual infections develop. If red flags develop (failure to thrive, persistent lymphadenopathy, hepatosplenomegaly, unusual infections), attend for urgent review. Parental concern should be taken seriously - if clinical suspicion remains high despite normal tests, refer to Paediatric Immunology.",
                "questions": [
                    {
                        "id": "childimmunity_initial_investigations",
                        "type": "multi_select",
                        "label": "Initial Investigations Requested",
                        "required": False,
                        "options": [
                            "FBC + differential",
                            "U&E / LFT",
                            "CRP / ESR",
                            "Glucose / HbA1c (where appropriate)",
                            "IgG, IgA, IgM",
                            "Microbiology/cultures of current/recurrent infections",
                            "None - reassure and observe"
                        ],
                        "output_phrase": "Investigations: {value}"
                    },
                    {
                        "id": "childimmunity_investigation_results",
                        "type": "textarea",
                        "label": "Investigation Results & Interpretation",
                        "required": False,
                        "placeholder": "e.g., FBC normal, IgG 4.5, IgA 1.2, IgM 0.8, CRP <3",
                        "output_phrase": "Results: {value}"
                    },
                    {
                        "id": "childimmunity_next_steps",
                        "type": "single_select",
                        "label": "Next Steps Based on Results",
                        "required": True,
                        "options": [
                            "Normal & reassuring - reassure and continue routine care",
                            "Normal but red flags remain - refer to Paediatric Immunology",
                            "Abnormal - investigate further as indicated",
                            "Abnormal - refer to Paediatric Immunology",
                            "Abnormal - refer to Paediatrics",
                            "Awaiting results"
                        ],
                        "output_phrase": "Next steps: {value}"
                    },
                    {
                        "id": "childimmunity_specialist_referral",
                        "type": "single_select",
                        "label": "Specialist Referral Plan",
                        "required": False,
                        "options": [
                            "No referral needed",
                            "Refer to Paediatric Immunology",
                            "Refer to Paediatrics (general)",
                            "Refer to Infectious Diseases",
                            "Refer to Respiratory (if recurrent pneumonia)",
                            "Refer to ENT (if sinusitis/otitis)",
                            "Awaiting results before referral"
                        ],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "childimmunity_immunology_considerations",
                        "type": "multi_select",
                        "label": "Paediatric Immunology May Consider (if referred)",
                        "required": False,
                        "options": [
                            "IgG subclasses",
                            "Specific vaccine antibody responses (pneumococcal/tetanus)",
                            "Lymphocyte subsets",
                            "Complement studies",
                            "Neutrophil function testing",
                            "Genetic testing",
                            "Other specialist investigations"
                        ],
                        "output_phrase": "Immunology considerations: {value}"
                    },
                    {
                        "id": "childimmunity_advice_given",
                        "type": "multi_select",
                        "label": "Advice Given to Parents/Carers",
                        "required": False,
                        "options": [
                            "Reassurance - normal variation in childhood",
                            "Hand hygiene",
                            "Avoiding close contact with unwell individuals",
                            "Smoke-free environment",
                            "Healthy diet/nutrition",
                            "Ensure vaccinations up to date",
                            "All above"
                        ],
                        "output_phrase": "Advice: {value}"
                    },
                    {
                        "id": "childimmunity_vaccination_review",
                        "type": "multi_select",
                        "label": "Vaccination Status Checked/Recommended",
                        "required": False,
                        "options": [
                            "Routine vaccinations up to date",
                            "Flu vaccine (annual)",
                            "Pneumococcal vaccine",
                            "COVID-19 vaccines (if eligible)",
                            "Other vaccines as indicated",
                            "Catch-up vaccinations needed"
                        ],
                        "output_phrase": "Vaccinations: {value}"
                    },
                    {
                        "id": "childimmunity_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "No follow-up needed - reassured",
                            "Review in 2-4 weeks for results",
                            "Review in 3 months if symptoms persist",
                            "As needed - parental concern",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "childimmunity_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Parent education, safety-netting discussion, growth monitoring",
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
    seed_low_immunity_child()