from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_low_immunity_adult():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: 
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Immunology").first()
    if not category: 
        category = Category(name="Immunology")
        db.add(category)
        db.commit()

    t = {
        "title": "Adult Recurrent Infections / ?Immunodeficiency",
        "description": "Practical GP assessment for adults presenting with recurrent infections or concern about 'low immunity', including history, red flags, secondary causes, and investigation pathways.",
        "category": "Immunology",
        "content": {"sections": [
            {
                "title": "History of Infections",
                "section_type": "history",
                "questions": [
                    {
                        "id": "lowimmunity_presenting_complaint",
                        "type": "text",
                        "label": "Presenting Complaint",
                        "required": True,
                        "placeholder": "e.g., Recurrent chest infections, patient worried about low immunity",
                        "output_phrase": "c/o: {value}"
                    },
                    {
                        "id": "lowimmunity_onset",
                        "type": "text",
                        "label": "Onset/Duration of Recurrent Infections",
                        "required": True,
                        "placeholder": "e.g., Past 2 years, increasing frequency",
                        "output_phrase": "Onset: {value}"
                    },
                    {
                        "id": "lowimmunity_frequency",
                        "type": "text",
                        "label": "Frequency of Infections",
                        "required": True,
                        "placeholder": "e.g., 6-8 URTIs per year, 2-3 courses antibiotics",
                        "output_phrase": "Frequency: {value}"
                    },
                    {
                        "id": "lowimmunity_infection_type",
                        "type": "multi_select",
                        "label": "Type/Site of Infections",
                        "required": True,
                        "options": [
                            "URTI (colds/sore throat)",
                            "Sinusitis",
                            "Otitis media",
                            "Tonsillitis",
                            "Pneumonia",
                            "UTI",
                            "Skin infection/abscess",
                            "Fungal infection",
                            "GI infection",
                            "Other"
                        ],
                        "output_phrase": "Infection type: {value}"
                    },
                    {
                        "id": "lowimmunity_severity",
                        "type": "textarea",
                        "label": "Severity / Complications",
                        "required": False,
                        "placeholder": "e.g., Hospital admissions, IV antibiotics, sepsis, ICU stay",
                        "output_phrase": "Severity: {value}"
                    },
                    {
                        "id": "lowimmunity_recovery",
                        "type": "text",
                        "label": "Duration and Recovery Between Episodes",
                        "required": False,
                        "placeholder": "e.g., Full recovery between episodes, symptoms linger 3-4 weeks",
                        "output_phrase": "Recovery: {value}"
                    },
                    {
                        "id": "lowimmunity_antibiotic_response",
                        "type": "single_select",
                        "label": "Response to Antibiotics",
                        "required": True,
                        "options": ["Good response", "Partial response - consider ?resistance", "Poor response - consider ?atypical/immunodeficiency", "Variable"],
                        "output_phrase": "Antibiotic response: {value}"
                    },
                    {
                        "id": "lowimmunity_unusual_organisms",
                        "type": "text",
                        "label": "Unusual/Opportunistic Organisms Isolated",
                        "required": False,
                        "placeholder": "e.g., Aspergillus, Pneumocystis, atypical mycobacteria",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unusual/opportunistic organisms - strongly suggests immunodeficiency, refer Immunology.",
                        "red_flag_negative": "",
                        "output_phrase": "Unusual organisms: {value}"
                    },
                    {
                        "id": "lowimmunity_unusual_sites",
                        "type": "text",
                        "label": "Recurrent Infection at Unusual Sites",
                        "required": False,
                        "placeholder": "e.g., Liver abscess, brain abscess, deep tissue infections",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Recurrent infections at unusual sites - refer Immunology/Haematology.",
                        "red_flag_negative": "",
                        "output_phrase": "Unusual sites: {value}"
                    }
                ]
            },
            {
                "title": "Red Flags & Systemic Symptoms",
                "section_type": "history",
                "questions": [
                    {
                        "id": "lowimmunity_weight_loss",
                        "type": "toggle",
                        "label": "Weight Loss?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unexplained weight loss - consider malignancy, HIV, chronic infection.",
                        "red_flag_negative": "",
                        "output_phrase": "Weight loss: {value}"
                    },
                    {
                        "id": "lowimmunity_fever",
                        "type": "toggle",
                        "label": "Persistent Fever / Night Sweats?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Persistent fever/night sweats - consider malignancy, HIV, TB, autoimmune.",
                        "red_flag_negative": "",
                        "output_phrase": "Fever/night sweats: {value}"
                    },
                    {
                        "id": "lowimmunity_diarrhoea",
                        "type": "toggle",
                        "label": "Chronic Diarrhoea?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Chronic diarrhoea - consider immunodeficiency, IBD, malabsorption.",
                        "red_flag_negative": "",
                        "output_phrase": "Chronic diarrhoea: {value}"
                    },
                    {
                        "id": "lowimmunity_oral_thrush",
                        "type": "toggle",
                        "label": "Persistent/Recurrent Oral Thrush?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Persistent oral thrush - consider HIV, immunodeficiency, diabetes.",
                        "red_flag_negative": "",
                        "output_phrase": "Oral thrush: {value}"
                    },
                    {
                        "id": "lowimmunity_deep_abscess",
                        "type": "toggle",
                        "label": "Recurrent Deep Abscesses?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Recurrent deep abscesses - consider neutrophil dysfunction, chronic granulomatous disease.",
                        "red_flag_negative": "",
                        "output_phrase": "Deep abscesses: {value}"
                    },
                    {
                        "id": "lowimmunity_recurrent_pneumonia",
                        "type": "toggle",
                        "label": "Recurrent Pneumonia?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Recurrent pneumonia - consider antibody deficiency, bronchiectasis, structural lung disease.",
                        "red_flag_negative": "",
                        "output_phrase": "Recurrent pneumonia: {value}"
                    },
                    {
                        "id": "lowimmunity_lymphadenopathy",
                        "type": "toggle",
                        "label": "Lymphadenopathy?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Persistent lymphadenopathy - consider malignancy, HIV, infection.",
                        "red_flag_negative": "",
                        "output_phrase": "Lymphadenopathy: {value}"
                    },
                    {
                        "id": "lowimmunity_other_systemic",
                        "type": "textarea",
                        "label": "Other Systemic Symptoms",
                        "required": False,
                        "placeholder": "e.g., Fatigue, rash, arthralgia, recurrent infections",
                        "output_phrase": "Other symptoms: {value}"
                    }
                ]
            },
            {
                "title": "Past Medical History / Secondary Causes",
                "section_type": "history",
                "questions": [
                    {
                        "id": "lowimmunity_diabetes",
                        "type": "toggle",
                        "label": "Diabetes?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Diabetes - risk factor for infections, check glycaemic control.",
                        "red_flag_negative": "",
                        "output_phrase": "Diabetes: {value}"
                    },
                    {
                        "id": "lowimmunity_ckd",
                        "type": "toggle",
                        "label": "CKD / Renal Disease?",
                        "required": False,
                        "output_phrase": "CKD: {value}"
                    },
                    {
                        "id": "lowimmunity_liver",
                        "type": "toggle",
                        "label": "Liver Disease?",
                        "required": False,
                        "output_phrase": "Liver disease: {value}"
                    },
                    {
                        "id": "lowimmunity_haematological",
                        "type": "toggle",
                        "label": "Haematological / Malignant Disease?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Haematological/malignant disease - consider secondary immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "Haematological: {value}"
                    },
                    {
                        "id": "lowimmunity_hiv",
                        "type": "single_select",
                        "label": "HIV Risk / History",
                        "required": False,
                        "options": ["No risk", "Risk factors present - consider testing", "Known HIV positive", "Unknown"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: HIV risk/positive - offer HIV testing, refer to HIV team.",
                        "red_flag_negative": "",
                        "output_phrase": "HIV: {value}"
                    },
                    {
                        "id": "lowimmunity_asplenia",
                        "type": "toggle",
                        "label": "Asplenia / Splenectomy?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Asplenia - risk of encapsulated organisms, ensure vaccinations and antibiotic prophylaxis.",
                        "red_flag_negative": "",
                        "output_phrase": "Asplenia: {value}"
                    },
                    {
                        "id": "lowimmunity_other_chronic",
                        "type": "textarea",
                        "label": "Other Chronic Disease",
                        "required": False,
                        "placeholder": "e.g., Autoimmune disease, COPD, bronchiectasis",
                        "output_phrase": "Other chronic disease: {value}"
                    }
                ]
            },
            {
                "title": "Medication History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "lowimmunity_steroids",
                        "type": "single_select",
                        "label": "Systemic Steroids",
                        "required": False,
                        "options": ["No", "Yes - current", "Yes - previous", "Inhaled only"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Systemic steroids - immunosuppressed, increased infection risk.",
                        "red_flag_negative": "",
                        "output_phrase": "Steroids: {value}"
                    },
                    {
                        "id": "lowimmunity_immunosuppressants",
                        "type": "multi_select",
                        "label": "Immunosuppressant Medications",
                        "required": False,
                        "options": ["Methotrexate", "Azathioprine", "Mycophenolate", "Cyclosporin", "Biologics", "Rituximab", "Other", "None"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Immunosuppressants - increased infection risk, consider specialist advice.",
                        "red_flag_negative": "",
                        "output_phrase": "Immunosuppressants: {value}"
                    },
                    {
                        "id": "lowimmunity_other_meds",
                        "type": "textarea",
                        "label": "Other Medications",
                        "required": False,
                        "placeholder": "e.g., Proton pump inhibitors (risk of C. diff/aspiration)",
                        "output_phrase": "Other meds: {value}"
                    }
                ]
            },
            {
                "title": "Social / Environmental / Family History",
                "section_type": "history",
                "questions": [
                    {
                        "id": "lowimmunity_smoking",
                        "type": "single_select",
                        "label": "Smoking Status",
                        "required": False,
                        "options": ["Non-smoker", "Ex-smoker", "Current smoker"],
                        "output_phrase": "Smoking: {value}"
                    },
                    {
                        "id": "lowimmunity_alcohol",
                        "type": "single_select",
                        "label": "Alcohol Intake",
                        "required": False,
                        "options": ["None", "Within guidelines", "Excess (>14 units/week)"],
                        "output_phrase": "Alcohol: {value}"
                    },
                    {
                        "id": "lowimmunity_nutrition",
                        "type": "text",
                        "label": "Nutrition/Weight Status",
                        "required": False,
                        "placeholder": "e.g., Weight stable, poor appetite, BMI 22",
                        "output_phrase": "Nutrition: {value}"
                    },
                    {
                        "id": "lowimmunity_occupation",
                        "type": "text",
                        "label": "Occupational Exposure",
                        "required": False,
                        "placeholder": "e.g., Healthcare worker, construction, farming",
                        "output_phrase": "Occupation: {value}"
                    },
                    {
                        "id": "lowimmunity_crowding",
                        "type": "toggle",
                        "label": "Crowding/Household Exposure?",
                        "required": False,
                        "output_phrase": "Household crowding: {value}"
                    },
                    {
                        "id": "lowimmunity_travel",
                        "type": "text",
                        "label": "Recent Travel",
                        "required": False,
                        "placeholder": "e.g., Tropical/subtropical, specific countries",
                        "output_phrase": "Travel: {value}"
                    },
                    {
                        "id": "lowimmunity_family_immunodeficiency",
                        "type": "toggle",
                        "label": "Family History of Known Immunodeficiency?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Family history of immunodeficiency - consider genetic/primary immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "Family immunodeficiency: {value}"
                    },
                    {
                        "id": "lowimmunity_family_recurrent_infections",
                        "type": "toggle",
                        "label": "Family History of Recurrent/Unusual Infections?",
                        "required": False,
                        "output_phrase": "Family recurrent infections: {value}"
                    },
                    {
                        "id": "lowimmunity_family_early_deaths",
                        "type": "toggle",
                        "label": "Family History of Unexplained Early Deaths?",
                        "required": False,
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Unexplained early deaths - consider hereditary immunodeficiency or other genetic conditions.",
                        "red_flag_negative": "",
                        "output_phrase": "Family early deaths: {value}"
                    }
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {
                        "id": "lowimmunity_general",
                        "type": "single_select",
                        "label": "General Appearance",
                        "required": True,
                        "options": ["Well", "Unwell", "Malnourished/cachectic - RED FLAG", "Well nourished"],
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Cachectic/malnourished appearance - consider chronic disease, malignancy, immunodeficiency.",
                        "red_flag_negative": "",
                        "output_phrase": "General: {value}"
                    },
                    {
                        "id": "lowimmunity_bmi",
                        "type": "number",
                        "label": "Weight / BMI",
                        "required": False,
                        "placeholder": "e.g., 24.5",
                        "output_phrase": "BMI: {value}"
                    },
                    {
                        "id": "lowimmunity_ent",
                        "type": "textarea",
                        "label": "ENT / Oral Cavity Examination",
                        "required": False,
                        "placeholder": "e.g., Oral thrush, tonsils, sinus tenderness",
                        "output_phrase": "ENT: {value}"
                    },
                    {
                        "id": "lowimmunity_lymph_nodes_exam",
                        "type": "textarea",
                        "label": "Lymph Node Examination",
                        "required": False,
                        "placeholder": "e.g., No palpable nodes, cervical nodes present, axillary nodes",
                        "is_red_flag": True,
                        "red_flag_positive": "RED FLAG: Persistent lymphadenopathy - consider malignancy, HIV, infection.",
                        "red_flag_negative": "",
                        "output_phrase": "Lymph nodes: {value}"
                    },
                    {
                        "id": "lowimmunity_chest",
                        "type": "textarea",
                        "label": "Chest Examination",
                        "required": False,
                        "placeholder": "e.g., Clear, crackles at bases, wheeze",
                        "output_phrase": "Chest: {value}"
                    },
                    {
                        "id": "lowimmunity_skin",
                        "type": "textarea",
                        "label": "Skin Examination",
                        "required": False,
                        "placeholder": "e.g., Eczema, fungal infections, abscesses, warts",
                        "output_phrase": "Skin: {value}"
                    },
                    {
                        "id": "lowimmunity_abdomen",
                        "type": "textarea",
                        "label": "Abdomen Examination",
                        "required": False,
                        "placeholder": "e.g., Hepatosplenomegaly, masses, tenderness",
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
                    "Frequent infections in otherwise healthy patient (most common)",
                    "Secondary immunodeficiency (diabetes, CKD, liver, HIV, malignancy)",
                    "Medication-induced immunosuppression (steroids, immunosuppressants)",
                    "Primary immunodeficiency (rare - consider if unusual infections, family history)",
                    "Structural cause (bronchiectasis, chronic sinusitis, anatomical defect)",
                    "Nutritional deficiency",
                    "Allergic/atopic predisposition",
                    "Functional/asplenia",
                    "Autoimmune disease with immunodeficiency component",
                    "Chronic infection (TB, HIV, viral hepatitis)"
                ],
                "questions": [
                    {
                        "id": "lowimmunity_diagnosis",
                        "type": "single_select",
                        "label": "Clinical Impression",
                        "required": True,
                        "options": [
                            "Likely normal variation - frequent infections in well patient",
                            "Secondary immunodeficiency - investigate underlying cause",
                            "Medication-induced immunosuppression - review medications",
                            "Primary immunodeficiency suspected - refer Immunology",
                            "Structural cause suspected - consider specialist review",
                            "Red flags present - urgent investigation required",
                            "Uncertain - proceed with initial investigations"
                        ],
                        "output_phrase": "Diagnosis: {value}"
                    },
                    {
                        "id": "lowimmunity_clinical_suspicion",
                        "type": "single_select",
                        "label": "Clinical Suspicion Level",
                        "required": True,
                        "options": ["Low - reassuring clinical picture", "Moderate - some concern but no red flags", "High - red flags or unusual features present"],
                        "output_phrase": "Suspicion level: {value}"
                    }
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return/urgent if: Infections become more frequent or severe, fail to respond to treatment, require hospitalisation or IV antibiotics, or unusual/opportunistic infections develop. If new red flags develop (weight loss, fever, lymphadenopathy, hepatosplenomegaly), attend for urgent review.",
                "questions": [
                    {
                        "id": "lowimmunity_initial_investigations",
                        "type": "multi_select",
                        "label": "Initial Investigations Requested",
                        "required": False,
                        "options": [
                            "FBC + differential",
                            "U&E / LFT",
                            "CRP / ESR",
                            "Glucose / HbA1c",
                            "HIV test (where appropriate)",
                            "IgG, IgA, IgM",
                            "Culture/microbiology of current/recurrent infections",
                            "None - reassure and observe"
                        ],
                        "output_phrase": "Investigations: {value}"
                    },
                    {
                        "id": "lowimmunity_hiv_testing",
                        "type": "toggle",
                        "label": "HIV Test Offered/Performed?",
                        "required": False,
                        "output_phrase": "HIV test: {value}"
                    },
                    {
                        "id": "lowimmunity_investigation_results",
                        "type": "textarea",
                        "label": "Investigation Results & Interpretation",
                        "required": False,
                        "placeholder": "e.g., FBC normal, IgG 4.5, IgA 1.2, IgM 0.8, HbA1c 42",
                        "output_phrase": "Results: {value}"
                    },
                    {
                        "id": "lowimmunity_next_steps",
                        "type": "single_select",
                        "label": "Next Steps Based on Results",
                        "required": True,
                        "options": [
                            "Normal & reassuring - reassure and observe",
                            "Normal but suspicion high - refer to Immunology",
                            "Abnormal - investigate further as indicated",
                            "Abnormal - refer to Haematology",
                            "Abnormal - refer to relevant specialist",
                            "Awaiting results"
                        ],
                        "output_phrase": "Next steps: {value}"
                    },
                    {
                        "id": "lowimmunity_specialist_referral",
                        "type": "single_select",
                        "label": "Specialist Referral Plan",
                        "required": False,
                        "options": [
                            "No referral needed",
                            "Refer to Immunology",
                            "Refer to Haematology",
                            "Refer to Infectious Diseases",
                            "Refer to Respiratory (if recurrent pneumonia)",
                            "Refer to ENT (if sinusitis/otitis)",
                            "Awaiting results before referral"
                        ],
                        "output_phrase": "Referral: {value}"
                    },
                    {
                        "id": "lowimmunity_immunology_considerations",
                        "type": "multi_select",
                        "label": "Immunology Specialist May Consider (if referred)",
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
                        "id": "lowimmunity_advice_given",
                        "type": "multi_select",
                        "label": "Advice Given to Patient",
                        "required": False,
                        "options": [
                            "Reassurance - normal variation",
                            "Smoking cessation",
                            "Moderate alcohol intake",
                            "Healthy diet/nutrition",
                            "Weight management",
                            "Hand hygiene",
                            "Avoiding close contact with unwell individuals",
                            "Vaccinations up to date (including flu, pneumococcal)",
                            "All above"
                        ],
                        "output_phrase": "Advice: {value}"
                    },
                    {
                        "id": "lowimmunity_vaccination",
                        "type": "multi_select",
                        "label": "Vaccination Status Checked/Recommended",
                        "required": False,
                        "options": [
                            "Flu vaccine (annual)",
                            "Pneumococcal vaccine",
                            "COVID-19 vaccines",
                            "Other vaccines as indicated",
                            "All up to date",
                            "Not discussed"
                        ],
                        "output_phrase": "Vaccinations: {value}"
                    },
                    {
                        "id": "lowimmunity_followup",
                        "type": "single_select",
                        "label": "Follow-up Plan",
                        "required": True,
                        "options": [
                            "No follow-up needed - reassured",
                            "Review in 2-4 weeks for results",
                            "Review in 3-6 months if symptoms persist",
                            "As needed - if new symptoms develop",
                            "Specialist follow-up arranged"
                        ],
                        "output_phrase": "Follow-up: {value}"
                    },
                    {
                        "id": "lowimmunity_notes",
                        "type": "textarea",
                        "label": "Additional Notes",
                        "required": False,
                        "placeholder": "e.g., Patient education, lifestyle advice, safety-netting discussion",
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
    seed_low_immunity_adult()