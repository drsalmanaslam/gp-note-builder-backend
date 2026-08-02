from app.database import SessionLocal
from app.models import Template, User

def seed_itching_pruritus():
    db = SessionLocal()
    
    title = "Generalised Itching / Pruritus"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    
    template = Template(
        title=title,
        description="Assessment of generalised pruritus covering dermatological vs systemic causes, red flags for malignancy, cholestasis, CKD, and stepwise management.",
        category="Dermatology",
        content={
            "sections": [
                {
                    "title": "History of Presenting Complaint",
                    "section_type": "history",
                    "questions": [
                        {"id": "itch_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 6 weeks"},
                        {"id": "itch_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden", "Gradual"]},
                        {"id": "itch_distribution", "type": "multi_select", "label": "Distribution", "required": True, "options": ["Generalised (all over)", "Scalp", "Trunk", "Limbs", "Palms/Soles", "Nocturnal predominance"]},
                        {"id": "itch_severity", "type": "single_select", "label": "Severity (0-10)", "required": True, "options": ["Mild (1-3)", "Moderate (4-6)", "Severe (7-9)", "Unbearable (10)"]},
                        {"id": "itch_rash", "type": "toggle", "label": "Visible Rash?", "required": True},
                        {"id": "itch_rash_description", "type": "text", "label": "Rash Description (if present)", "required": False, "placeholder": "e.g., Erythematous papules on trunk, excoriations"},
                        {"id": "itch_water_contact", "type": "toggle", "label": "Triggered by Water Contact? (Aquagenic)", "required": False},
                        {"id": "itch_exercise", "type": "toggle", "label": "Triggered by Exercise/Heat?", "required": False},
                        {"id": "itch_family", "type": "toggle", "label": "Family Members Also Itching? (?Scabies)", "required": True},
                        {"id": "itch_sleep", "type": "toggle", "label": "Disturbing Sleep?", "required": True}
                    ]
                },
                {
                    "title": "Systemic Red Flag Screen",
                    "section_type": "history",
                    "questions": [
                        {"id": "itch_weight_loss", "type": "toggle", "label": "Unintentional Weight Loss?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weight loss + pruritus = ?malignancy (lymphoma, leukaemia). Urgent CXR, FBC, LDH.", "red_flag_negative": ""},
                        {"id": "itch_night_sweats", "type": "toggle", "label": "Drenching Night Sweats?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Night sweats + pruritus = ?lymphoma (Hodgkin's). Urgent referral.", "red_flag_negative": ""},
                        {"id": "itch_fever", "type": "toggle", "label": "Fevers?", "required": False},
                        {"id": "itch_fatigue", "type": "toggle", "label": "Severe Fatigue?", "required": False},
                        {"id": "itch_jaundice", "type": "toggle", "label": "Jaundice / Dark Urine / Pale Stools?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cholestatic picture = ?PBC, obstruction, drug-induced. Check LFTs urgently.", "red_flag_negative": ""},
                        {"id": "itch_ckd", "type": "toggle", "label": "Known CKD / Renal Disease?", "required": True},
                        {"id": "itch_thyroid", "type": "toggle", "label": "Thyroid Symptoms? (Cold intolerance, weight gain)", "required": False},
                        {"id": "itch_diabetes", "type": "toggle", "label": "Diabetes?", "required": False},
                        {"id": "itch_iron", "type": "toggle", "label": "Iron Deficiency Symptoms? (Pica, restless legs)", "required": False}
                    ]
                },
                {
                    "title": "Drug & Exposure History",
                    "section_type": "history",
                    "questions": [
                        {"id": "itch_new_meds", "type": "toggle", "label": "New Medications? (Opioids, aspirin, ACEi, statins)", "required": True},
                        {"id": "itch_med_list", "type": "text", "label": "List All Medications", "required": True, "placeholder": "e.g., Ramipril 5mg, Atorvastatin 20mg"},
                        {"id": "itch_allergies", "type": "toggle", "label": "Known Allergies / Atopy?", "required": True},
                        {"id": "itch_contacts", "type": "multi_select", "label": "New Contacts/Exposures", "required": False, "options": ["New soaps/detergents", "New clothes", "Pets", "Travel history", "Occupational exposure", "None"]},
                        {"id": "itch_alcohol", "type": "single_select", "label": "Alcohol Intake", "required": True, "options": ["None", "Within limits", "Excess"]}
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {"id": "itch_skin_findings", "type": "single_select", "label": "Skin Findings", "required": True, "options": ["No primary lesion - only excoriations", "Erythematous rash", "Papules/Nodules", "Urticarial wheals", "Vesicles/Bullae", "Xerosis (dry skin)"]},
                        {"id": "itch_lymphadenopathy", "type": "toggle", "label": "Lymphadenopathy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Lymphadenopathy + pruritus = ?lymphoma. Urgent referral.", "red_flag_negative": ""},
                        {"id": "itch_hepatosplenomegaly", "type": "toggle", "label": "Hepatosplenomegaly?", "required": False},
                        {"id": "itch_jaundice_sign", "type": "toggle", "label": "Jaundice on Examination?", "required": False},
                        {"id": "itch_thyroid_exam", "type": "toggle", "label": "Goitre / Thyroid Nodule?", "required": False},
                        {"id": "itch_burrows", "type": "toggle", "label": "Burrows / Web Spaces Affected? (?Scabies)", "required": False}
                    ]
                },
                {
                    "title": "Investigations",
                    "section_type": "assessment",
                    "differentials": [
                        "Xerosis (dry skin - most common cause)",
                        "Eczema / Atopic dermatitis",
                        "Scabies",
                        "Urticaria",
                        "Drug-induced pruritus",
                        "Iron deficiency anaemia",
                        "Cholestasis (PBC, drug-induced)",
                        "CKD-related uraemic pruritus",
                        "Hyperthyroidism / Hypothyroidism",
                        "Diabetes mellitus",
                        "Hodgkin's lymphoma (urgent)",
                        "Polycythaemia vera"
                    ],
                    "questions": [
                        {"id": "itch_bloods", "type": "multi_select", "label": "Blood Tests", "required": False, "options": ["FBC + film", "U&E, eGFR", "LFTs", "TFTs", "Ferritin / Iron studies", "Fasting glucose / HbA1c", "LDH (if ?lymphoma)", "CXR (if ?lymphoma)", "None indicated"]},
                        {"id": "itch_biopsy", "type": "toggle", "label": "Skin Biopsy Required?", "required": False},
                        {"id": "itch_dermatology", "type": "toggle", "label": "Dermatology Referral?", "required": False}
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "Return if: itching becomes unbearable despite treatment, new lumps/bumps appear (especially in neck, armpits, groin), develop jaundice, unexplained weight loss, or drenching night sweats. If systemic cause identified (CKD, cholestasis, iron deficiency): treat underlying condition. General measures: avoid hot showers, use soap substitutes (Dermol, E45), regular emollients, keep nails short, wear cotton clothing.",
                    "questions": [
                        {"id": "itch_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Xerosis / Dry skin", "Eczema", "Scabies", "Drug-induced", "Suspected systemic cause", "Idiopathic - requires investigation", "Suspected malignancy - urgent referral"]},
                        {"id": "itch_treatment", "type": "multi_select", "label": "Treatment", "required": True, "options": ["Emollients (E45, Diprobase)", "Soap substitute", "Topical steroid (e.g., Hydrocortisone 1%)", "Oral antihistamine (Cetirizine 10mg)", "Sedating antihistamine at night (Chlorphenamine)", "Treat scabies (Permethrin 5%)", "Treat underlying cause", "Refer Dermatology"]},
                        {"id": "itch_emollient", "type": "text", "label": "Emollient Prescribed", "required": False, "placeholder": "e.g., Diprobase cream BD, E45 wash for shower"},
                        {"id": "itch_caution", "type": "toggle", "label": "Caution: Avoid prolonged potent steroid without diagnosis", "required": True},
                        {"id": "itch_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Review in 4 weeks with blood results, sooner if red flags develop"}
                    ]
                }
            ]
        },
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_itching_pruritus()