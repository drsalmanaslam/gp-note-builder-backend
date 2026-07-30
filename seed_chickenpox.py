from app.database import SessionLocal
from app.models import User, Template, Category

def seed_chickenpox():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Paediatrics").first()
    if not category: category = Category(name="Paediatrics"); db.add(category); db.commit()

    t = {
        "title": "Chickenpox / Varicella",
        "description": "Focused assessment for varicella zoster infection covering lesion staging, red flags for complications, NSAID avoidance, and infection control.",
        "category": "Paediatrics",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "vz_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Itchy rash on trunk and arms for 2 days, unwell for 10 days"},
                    {"id": "vz_age", "type": "single_select", "label": "Age", "required": True, "options": ["<1 year", "1-2 years", "2-5 years", "6-12 years", "13-18 years", "Adult"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Age ≥12 years = higher risk severe disease. Consider oral Aciclovir within 24h of rash onset.", "red_flag_negative": ""},
                    {"id": "vz_duration_rash", "type": "text", "label": "Duration of Rash", "required": True, "placeholder": "e.g., 2 days"},
                    {"id": "vz_prodrome", "type": "multi_select", "label": "Prodromal Symptoms", "required": True, "options": ["Fever", "Malaise / off-form", "Headache", "Coryza", "Cough", "None"]},
                    {"id": "vz_rash_origin", "type": "single_select", "label": "Rash Started On", "required": True, "options": ["Trunk", "Face", "Arms/legs", "Scalp", "Generalised"]},
                    {"id": "vz_itch_severity", "type": "single_select", "label": "Itch Severity", "required": True, "options": ["Mild", "Moderate", "Severe - scratching constantly"]},
                    {"id": "vz_lesion_stages", "type": "multi_select", "label": "Lesion Types Present", "required": True, "options": ["Papules (red spots)", "Vesicles (fluid-filled blisters)", "Crusts (drying/scabbed)", "All 3 stages (crops)", "Pustules - ?secondary infection"]},
                    {"id": "vz_exposure", "type": "toggle", "label": "Known Chickenpox Contact?", "required": False},
                    {"id": "vz_previous_infection", "type": "toggle", "label": "Previous Chickenpox Infection?", "required": False},
                    {"id": "vz_vaccinated", "type": "toggle", "label": "Varicella Vaccinated?", "required": False}
                ]
            },
            {
                "title": "RED FLAGS - Complications",
                "section_type": "history",
                "questions": [
                    {"id": "vz_spreading_erythema", "type": "toggle", "label": "Spreading Redness / Heat Around Lesions? (Secondary infection)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cellulitis/secondary bacterial infection = antibiotics (Flucloxacillin). If severe = admission.", "red_flag_negative": ""},
                    {"id": "vz_purulent", "type": "toggle", "label": "Purulent Breakdown of Lesions? (Staph/Strep superinfection)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Purulent lesions = bacterial superinfection. Antibiotics + monitor closely.", "red_flag_negative": ""},
                    {"id": "vz_tachypnoea", "type": "toggle", "label": "Tachypnoea / Cough / Breathlessness? (Varicella pneumonia)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Respiratory symptoms = ?varicella pneumonia. URGENT admission. More common in adults/smokers.", "red_flag_negative": ""},
                    {"id": "vz_ataxia", "type": "toggle", "label": "Ataxia / Unsteadiness? (Cerebellar ataxia)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ataxia = ?cerebellar ataxia (benign, self-limiting). Needs paediatric assessment.", "red_flag_negative": ""},
                    {"id": "vz_confusion", "type": "toggle", "label": "Confusion / Drowsiness? (Encephalitis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Confusion/drowsiness = ?varicella encephalitis. EMERGENCY admission.", "red_flag_negative": ""},
                    {"id": "vz_high_fever", "type": "toggle", "label": "Persistent High Fever / Lethargy?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Toxic appearance = ?sepsis/secondary infection. Urgent paediatric assessment.", "red_flag_negative": ""},
                    {"id": "vz_immunocompromised", "type": "toggle", "label": "Immunocompromised? (Chemotherapy, transplant, high-dose steroids, HIV)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunocompromised + chickenpox = EMERGENCY. Same-day hospital for IV Aciclovir.", "red_flag_negative": ""},
                    {"id": "vz_pregnant_contact", "type": "toggle", "label": "Pregnant Contact? (Non-immune, <20 weeks or near term)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pregnant contact = urgent obstetric advice. VZIG may be needed.", "red_flag_negative": ""},
                    {"id": "vz_neonatal_contact", "type": "toggle", "label": "Neonatal Contact? (<1 month)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neonatal exposure = VZIG + paediatric advice. High risk severe disease.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination & Vitals",
                "section_type": "examination",
                "questions": [
                    {"id": "vz_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 110 (NR age-dependent)"},
                    {"id": "vz_rr", "type": "number", "label": "Respiratory Rate (/min)", "required": True, "placeholder": "e.g., 25"},
                    {"id": "vz_temp", "type": "number", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 38.2"},
                    {"id": "vz_lesions", "type": "single_select", "label": "Lesion Distribution", "required": True, "options": ["Trunk predominant", "Generalised (trunk + limbs + face)", "Face/scalp predominant", "Mucous membranes involved"]},
                    {"id": "vz_cellulitis", "type": "toggle", "label": "Spreading Cellulitis?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cellulitis = antibiotics (Flucloxacillin/Co-amoxiclav). Mark extent.", "red_flag_negative": ""},
                    {"id": "vz_chest", "type": "single_select", "label": "Chest Auscultation", "required": False, "options": ["Clear", "Crackles/wheeze - RED FLAG", "Not assessed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Chickenpox (Primary Varicella Zoster)",
                    "Hand, Foot & Mouth Disease (Coxsackie virus)",
                    "Impetigo",
                    "Herpes Zoster (Shingles) - unilateral dermatomal",
                    "Disseminated HSV Infection",
                    "Guttate Psoriasis",
                    "Papular Urticaria (insect bites)",
                    "Secondary Bacterial Superinfection (Staph/Strep)",
                    "Varicella Pneumonia (RED FLAG)",
                    "Varicella Cerebellar Ataxia",
                    "Varicella Encephalitis (RED FLAG)"
                ],
                "questions": [
                    {"id": "vz_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Chickenpox - uncomplicated", "Chickenpox - secondary bacterial infection", "Chickenpox - ?pneumonia (URGENT)", "Chickenpox - ?neurological complication (URGENT)", "Chickenpox - immunocompromised (EMERGENCY)"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: redness/heat/severe swelling develops around blisters (secondary bacterial cellulitis), rapid breathing/cough develops, unsteadiness/ataxia, persistent vomiting, drowsiness/confusion, or persistent high fever >5 days. CRITICAL SAFETY: AVOID ibuprofen/NSAIDs strictly (increased risk of severe invasive Group A Strep infection and necrotising fasciitis). Use PARACETAMOL only for fever/pain. Infectious period: from 2 days before rash until ALL vesicles fully crusted (~5 days after first appearance). Strictly avoid contact with: pregnant women (non-immune), neonates, immunocompromised individuals. NO commercial flights until at least 6 days after last spot appeared (all lesions crusted). Keep nails short, cotton socks on hands at night to reduce scratching. Calamine lotion / Virasoothe / PoxClin for itch. Oral Aciclovir if: age ≥12 (within 24h rash), severe disease, steroids in past 3 months, or immunocompromised.",
                "questions": [
                    {"id": "vz_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Symptomatic relief only", "Calamine / Virasoothe / PoxClin", "Oral antihistamine (Desloratadine/Promethazine)", "Paracetamol for fever", "Oral Aciclovir indicated", "Antibiotics (secondary infection)", "Urgent paediatric admission", "VZIG for contacts"]},
                    {"id": "vz_nsaid_warning", "type": "toggle", "label": "NSAID AVOIDANCE Warning Given? (Ibuprofen contraindicated)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Ibuprofen/NSAIDs STRICTLY contraindicated in chickenpox. Risk of severe invasive GAS/necrotising fasciitis.", "red_flag_negative": ""},
                    {"id": "vz_infection_control", "type": "toggle", "label": "Infection Control Advised? (Avoid pregnant/neonates/immunocompromised, no flights)", "required": True},
                    {"id": "vz_hygiene", "type": "toggle", "label": "Nail Care + Cotton Socks Advised? (Reduce scratching)", "required": False},
                    {"id": "vz_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if resolving, 5-7 days if not crusted"}
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
    seed_chickenpox()