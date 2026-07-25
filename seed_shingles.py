from app.database import SessionLocal
from app.models import User, Template, Category

def seed_shingles():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Shingles / Herpes Zoster Assessment",
        "description": "Focused assessment for herpes zoster with antiviral treatment, red flags for ophthalmic/otic involvement, and post-herpetic neuralgia counselling.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "hz_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Burning/stinging rash on right side of abdomen for 1 day"},
                    {"id": "hz_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 58"},
                    {"id": "hz_duration_onset", "type": "single_select", "label": "Duration Since Rash Onset", "required": True, "options": ["<72 hours (antivirals effective)", "72-96 hours (consider antivirals)", ">96 hours (antivirals less benefit)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: <72 hours = antivirals most effective. Start immediately.", "red_flag_negative": ""},
                    {"id": "hz_prodrome", "type": "multi_select", "label": "Prodromal Symptoms", "required": True, "options": ["Itching", "Burning/stinging pain", "Tingling", "Mild myalgia", "Headache", "Malaise", "None"]},
                    {"id": "hz_dermatome", "type": "single_select", "label": "Dermatome Affected", "required": True, "options": ["T1-T8 (Upper trunk)", "T9-T12 (Lower trunk/abdomen)", "Cervical (neck/arm)", "Lumbar (lower back/leg)", "Sacral", "Trigeminal - V1 (ophthalmic) - RED FLAG", "Trigeminal - V2/V3", "Geniculate (Ramsay Hunt) - RED FLAG"]}
                ]
            },
            {
                "title": "RED FLAGS - Ophthalmic & Otic",
                "section_type": "history",
                "questions": [
                    {"id": "hz_eye_involvement", "type": "toggle", "label": "Eye Involvement? (Redness, pain, visual change, vesicles on nose)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ophthalmic zoster (V1) = URGENT ophthalmology same-day. Risk of corneal scarring, uveitis, vision loss. Hutchinson's sign (nasal tip vesicle) = high risk.", "red_flag_negative": ""},
                    {"id": "hz_hutchinson_sign", "type": "toggle", "label": "Hutchinson's Sign? (Vesicle on tip/side of nose)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hutchinson's sign positive = nasociliary nerve involvement. High risk of ocular involvement. Urgent ophthalmology.", "red_flag_negative": ""},
                    {"id": "hz_ear_involvement", "type": "toggle", "label": "Ear Involvement? (Pain, vesicles in/around ear, hearing loss, facial weakness)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ramsay Hunt syndrome (herpes zoster oticus) = URGENT ENT. Risk of facial nerve palsy, hearing loss.", "red_flag_negative": ""},
                    {"id": "hz_facial_weakness", "type": "toggle", "label": "Facial Weakness / Droop?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Facial weakness + ear vesicles = Ramsay Hunt. Urgent ENT + antivirals + steroids.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Disseminated & CNS",
                "section_type": "history",
                "questions": [
                    {"id": "hz_disseminated", "type": "toggle", "label": "Multi-Dermatomal / Disseminated Rash?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Disseminated zoster (>1 dermatome or >20 lesions outside primary dermatome) = ?immunocompromised. Urgent assessment + IV antivirals.", "red_flag_negative": ""},
                    {"id": "hz_neck_stiffness", "type": "toggle", "label": "Neck Stiffness / Photophobia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Meningism = ?VZV meningitis/encephalitis. Emergency admission.", "red_flag_negative": ""},
                    {"id": "hz_confusion", "type": "toggle", "label": "Confusion / Altered Mental State?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Confusion = ?VZV encephalitis. Emergency admission.", "red_flag_negative": ""},
                    {"id": "hz_immunocompromised", "type": "toggle", "label": "Immunocompromised? (Chemotherapy, transplant, HIV, high-dose steroids, biologics)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunocompromised + zoster = high risk disseminated disease. Urgent specialist assessment. IV antivirals may be needed.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hz_lesions", "type": "single_select", "label": "Lesion Morphology", "required": True, "options": ["Erythematous plaques + clustered vesicles", "Vesicles only", "Pustular", "Crusted (late stage)", "Bullous/haemorrhagic"]},
                    {"id": "hz_unilateral", "type": "toggle", "label": "Strictly Unilateral? (Does not cross midline)", "required": True},
                    {"id": "hz_dermatome_exam", "type": "toggle", "label": "Confined to Single Dermatome?", "required": True},
                    {"id": "hz_secondary_infection", "type": "toggle", "label": "Secondary Bacterial Infection? (Cellulitis, purulence)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Secondary infection = antibiotics (Flucloxacillin) + monitor closely.", "red_flag_negative": ""},
                    {"id": "hz_necrosis", "type": "toggle", "label": "Deep Tissue Necrosis?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Necrotising infection = surgical emergency.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Herpes Zoster (Shingles) - Single Dermatome",
                    "Disseminated Zoster (RED FLAG)",
                    "Ophthalmic Zoster (RED FLAG)",
                    "Ramsay Hunt Syndrome (RED FLAG)",
                    "Herpes Simplex Virus (HSV) Infection",
                    "Contact Dermatitis",
                    "Cellulitis (if secondary infection)",
                    "Post-Herpetic Neuralgia (PHN)"
                ],
                "questions": [
                    {"id": "hz_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Herpes Zoster - uncomplicated", "Herpes Zoster - ophthalmic (URGENT)", "Herpes Zoster - Ramsay Hunt (URGENT)", "Herpes Zoster - disseminated (URGENT)", "Herpes Zoster with secondary infection"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: rash spreads near eyes/ears, becomes red/hot/purulent (secondary infection), severe neurological symptoms (confusion, neck stiffness, severe headache), or disseminated rash develops. Contagious until ALL vesicles have crusted over (typically 2-4 weeks). Cover lesions with non-adherent dressing. Strictly avoid contact with: pregnant women (non-immune to VZV), immunocompromised individuals, and neonates. Post-herpetic neuralgia (PHN): risk up to 30% despite antivirals. Pain persisting >4 weeks after rash healing = PHN. Treatment options: Amitriptyline 10-25mg nocte, Gabapentin/Pregabalin, topical Capsaicin, Lidocaine patches. Refer pain clinic if refractory.",
                "questions": [
                    {"id": "hz_antiviral", "type": "single_select", "label": "Antiviral Prescribed", "required": True, "options": ["None (not indicated)", "Aciclovir 800mg 5x daily for 7 days", "Valaciclovir 1000mg TDS for 7 days", "Famciclovir 500mg TDS for 7 days", "IV antivirals (hospital)"]},
                    {"id": "hz_analgesia", "type": "multi_select", "label": "Analgesia", "required": False, "options": ["Paracetamol regular", "Ibuprofen (if not CI)", "Co-codamol", "Amitriptyline (neuropathic + PHN prevention)", "Gabapentin/Pregabalin", "None"]},
                    {"id": "hz_infection_control", "type": "toggle", "label": "Infection Control Advised? (Cover lesions, avoid at-risk contacts)", "required": True},
                    {"id": "hz_phn_counselled", "type": "toggle", "label": "Post-Herpetic Neuralgia Counselling Given?", "required": True},
                    {"id": "hz_ophthalmology_referral", "type": "toggle", "label": "Ophthalmology Referral? (If ophthalmic zoster)", "required": False},
                    {"id": "hz_ent_referral", "type": "toggle", "label": "ENT Referral? (If Ramsay Hunt)", "required": False},
                    {"id": "hz_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1 week if not improving, sooner if red flags"}
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
    seed_shingles()