from app.database import SessionLocal
from app.models import User, Template, Category

def seed_eczema():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Eczema / Atopic Dermatitis Assessment",
        "description": "Focused assessment for eczema including severity, triggers, infection red flags, and stepwise management.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "ecz_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Itchy dry rash on arms and legs for 2 weeks"},
                    {"id": "ecz_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 5 (or adult age)"},
                    {"id": "ecz_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., Since infancy / 2 weeks flare"},
                    {"id": "ecz_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Infancy/Childhood", "Adult-onset", "Recent flare"]},
                    {"id": "ecz_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - dry skin, occasional itching", "Moderate - frequent itching, redness", "Severe - widespread, intense itching, sleep disturbance", "Erythrodermic - >90% body"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Erythrodermic/ severe widespread eczema = may need hospital admission. Urgent dermatology referral.", "red_flag_negative": ""},
                    {"id": "ecz_sleep", "type": "toggle", "label": "Sleep Disturbed by Itching?", "required": True},
                    {"id": "ecz_itch_severity", "type": "single_select", "label": "Itch Severity", "required": True, "options": ["Mild", "Moderate", "Severe - scratching constantly"]}
                ]
            },
            {
                "title": "Affected Areas",
                "section_type": "history",
                "questions": [
                    {"id": "ecz_sites", "type": "multi_select", "label": "Affected Areas", "required": True, "options": ["Face", "Neck", "Hands", "Wrists", "Elbow creases (flexural)", "Behind knees (popliteal fossa)", "Trunk", "Scalp", "Eyelids", "Generalised/widespread"]},
                    {"id": "ecz_weeping", "type": "toggle", "label": "Weeping / Oozing / Crusting?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Weeping/crusting = possible secondary bacterial infection (impetiginised eczema). Swab + consider antibiotics.", "red_flag_negative": ""},
                    {"id": "ecz_pustules", "type": "toggle", "label": "Pustules / Yellow Crusts? (Staph infection)", "required": False},
                    {"id": "ecz_cold_sores", "type": "toggle", "label": "Contact with Cold Sores? (Eczema herpeticum risk)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Eczema herpeticum = punched-out lesions, widespread, unwell. EMERGENCY - same-day dermatology/A&E. Antivirals urgent.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Triggers & Aggravating Factors",
                "section_type": "history",
                "questions": [
                    {"id": "ecz_triggers", "type": "multi_select", "label": "Triggers", "required": False, "options": ["Soap/detergents", "Wool/synthetic fabrics", "Heat/sweating", "Stress", "Dust mites", "Pollen", "Pet dander", "Foods (dairy, eggs, nuts)", "None identified"]},
                    {"id": "ecz_seasonal", "type": "single_select", "label": "Seasonal Pattern", "required": False, "options": ["No pattern", "Worse in winter (dry air)", "Worse in summer (sweating/pollen)", "Worse spring/autumn"]},
                    {"id": "ecz_occupation", "type": "toggle", "label": "Occupational Exposure? (Healthcare, hairdressing, cleaning, construction)", "required": False}
                ]
            },
            {
                "title": "Atopic History",
                "section_type": "history",
                "questions": [
                    {"id": "ecz_asthma", "type": "toggle", "label": "Asthma?", "required": True},
                    {"id": "ecz_hayfever", "type": "toggle", "label": "Hay Fever / Allergic Rhinitis?", "required": True},
                    {"id": "ecz_food_allergy", "type": "toggle", "label": "Food Allergies?", "required": False},
                    {"id": "ecz_family_atopy", "type": "toggle", "label": "Family History of Atopy? (Eczema, asthma, hayfever)", "required": False}
                ]
            },
            {
                "title": "Current & Previous Treatments",
                "section_type": "history",
                "questions": [
                    {"id": "ecz_emollients", "type": "toggle", "label": "Using Emollients Regularly?", "required": True},
                    {"id": "ecz_emollient_frequency", "type": "single_select", "label": "Emollient Frequency", "required": False, "options": ["Multiple times daily", "Once daily", "Few times weekly", "Rarely", "None"]},
                    {"id": "ecz_steroids", "type": "single_select", "label": "Topical Steroid Used", "required": False, "options": ["None", "Mild (Hydrocortisone 1%)", "Moderate (Eumovate)", "Potent (Betnovate)", "Very potent (Dermovate)", "Over-the-counter only"]},
                    {"id": "ecz_steroid_response", "type": "single_select", "label": "Response to Steroids", "required": False, "options": ["Good - clears", "Partial - improves but returns", "Poor - minimal improvement", "Not used"]},
                    {"id": "ecz_other_rx", "type": "multi_select", "label": "Other Treatments Tried", "required": False, "options": ["Tacrolimus/Pimecrolimus", "Antihistamines", "Antibiotics", "Phototherapy", "Oral steroids", "Methotrexate", "Dupilumab", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ecz_distribution", "type": "single_select", "label": "Distribution", "required": True, "options": ["Flexural (classic atopic)", "Extensor (infants)", "Face/neck only", "Hands only", "Generalised", "Discoid (coin-shaped)"]},
                    {"id": "ecz_morphology", "type": "multi_select", "label": "Morphology", "required": True, "options": ["Erythema", "Dryness/scaling", "Lichenification (thickened skin)", "Excoriation (scratch marks)", "Papules", "Vesicles", "Weeping/crusting", "Fissures"]},
                    {"id": "ecz_infection_signs", "type": "toggle", "label": "Signs of Infection? (Weeping, yellow crust, pustules)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Clinical infection = swab + antibiotics (Flucloxacillin). If widespread/systemically unwell = admission.", "red_flag_negative": ""},
                    {"id": "ecz_herpeticum", "type": "toggle", "label": "Punched-out Lesions / Eczema Herpeticum?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspected eczema herpeticum = EMERGENCY. Same-day dermatology. IV Aciclovir.", "red_flag_negative": ""},
                    {"id": "ecz_bsa", "type": "single_select", "label": "Body Surface Area Affected", "required": False, "options": ["<10%", "10-30%", "30-50%", ">50%"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Atopic Dermatitis / Eczema",
                    "Contact Dermatitis (irritant/allergic)",
                    "Seborrhoeic Dermatitis",
                    "Discoid Eczema",
                    "Psoriasis",
                    "Fungal Infection (Tinea)",
                    "Scabies",
                    "Impetiginised Eczema (secondary bacterial infection)",
                    "Eczema Herpeticum (EMERGENCY)",
                    "Pompholyx (Dyshidrotic Eczema)",
                    "Varicose Eczema (venous stasis)",
                    "Asteatotic Eczema (dry skin in elderly)"
                ],
                "questions": [
                    {"id": "ecz_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Atopic eczema - mild", "Atopic eczema - moderate", "Atopic eczema - severe", "Infected eczema", "Contact dermatitis", "Seborrhoeic dermatitis", "Suspected eczema herpeticum - EMERGENCY", "Uncertain"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if: skin becomes suddenly worse, develops weeping/crusting/pustules (infection), develops punched-out lesions (eczema herpeticum - emergency), or becomes systemically unwell. Emollient advice: use liberally 3-4 times daily, apply in direction of hair growth, use 250-500g per week. Steroid advice: fingertip unit (1 FTU covers 2 adult palms), use for 5-7 days for flares then step down. No steroid on face without advice (use mild only, max 5 days). Antihistamines for itch at night. Avoid triggers: soap-free washes, cotton clothing, keep nails short, avoid scratching. If moderate-severe: refer dermatology for consideration of phototherapy, systemic therapy, or biologic (Dupilumab).",
                "questions": [
                    {"id": "ecz_plan", "type": "multi_select", "label": "Management", "required": False, "options": ["Emollients - liberal use", "Mild topical steroid (Hydrocortisone)", "Moderate topical steroid (Eumovate)", "Potent topical steroid (Betnovate)", "Topical calcineurin inhibitor (Tacrolimus)", "Antihistamines (sedating for night)", "Antibiotics (Flucloxacillin)", "Swab for MC+S", "Dermatology referral", "Patch testing referral"]},
                    {"id": "ecz_emollient_rx", "type": "text", "label": "Emollient Prescribed", "required": False, "placeholder": "e.g., Epaderm / Doublebase / Cetraben - 500g"},
                    {"id": "ecz_steroid_rx", "type": "text", "label": "Topical Steroid Prescribed", "required": False, "placeholder": "e.g., Hydrocortisone 1% cream BD for 5-7 days"},
                    {"id": "ecz_advice", "type": "toggle", "label": "Emollient + Steroid Technique Explained? (Fingertip units, direction of hair)", "required": False},
                    {"id": "ecz_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2 weeks if flare, or PRN"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing: db.delete(existing); db.commit()
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_eczema()