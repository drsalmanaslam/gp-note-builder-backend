from app.database import SessionLocal
from app.models import User, Template, Category

def seed_gastroenteritis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Gastroenterology").first()
    if not category: category = Category(name="Gastroenterology"); db.add(category); db.commit()

    t = {
        "title": "Gastroenteritis Assessment",
        "description": "Focused assessment for gastroenteritis covering dehydration assessment, medication holds, stool testing criteria, and school/work exclusion advice.",
        "category": "Gastroenterology",
        "content": {"sections": [
            {
                "title": "Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "ge_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Vomiting for 3 days, now resolved, with ongoing diarrhoea"},
                    {"id": "ge_vomiting", "type": "single_select", "label": "Vomiting", "required": True, "options": ["Present - ongoing", "Present - resolved", "Not present"]},
                    {"id": "ge_vomiting_duration", "type": "text", "label": "Vomiting Duration", "required": False, "placeholder": "e.g., 3 days"},
                    {"id": "ge_diarrhoea_frequency", "type": "number", "label": "Diarrhoea Episodes (per day)", "required": True, "placeholder": "e.g., 3"},
                    {"id": "ge_stool_character", "type": "multi_select", "label": "Stool Characteristics", "required": True, "options": ["Blood present - RED FLAG", "Mucus present", "Neither present"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bloody diarrhoea = ?bacterial dysentery, IBD, ischaemic colitis. Send stool culture.", "red_flag_negative": ""},
                    {"id": "ge_abdo_pain", "type": "single_select", "label": "Abdominal Pain", "required": True, "options": ["Mild, now resolved", "Ongoing pain", "No pain"]},
                    {"id": "ge_exposure", "type": "multi_select", "label": "Exposure History", "required": True, "options": ["Meals out / takeaway", "Foreign travel", "Sick contacts (household/work)", "None of the above"]}
                ]
            },
            {
                "title": "Hydration Assessment",
                "section_type": "history",
                "questions": [
                    {"id": "ge_dry_mouth", "type": "toggle", "label": "Mouth Feels Dry?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Dry mouth = dehydration. Assess further (skin turgor, CRT, urine output).", "red_flag_negative": ""},
                    {"id": "ge_urine_output", "type": "text", "label": "Urine Output Today", "required": True, "placeholder": "e.g., 3 times or reduced"},
                    {"id": "ge_postural", "type": "toggle", "label": "Dizziness on Standing?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Postural dizziness = significant dehydration. Consider admission if elderly/frail.", "red_flag_negative": ""},
                    {"id": "ge_neuro", "type": "multi_select", "label": "Neurological Symptoms", "required": False, "options": ["Headache", "Visual problems", "Gait disturbance", "None present"]},
                    {"id": "ge_urinary", "type": "multi_select", "label": "Urinary Symptoms", "required": False, "options": ["Dysuria", "Frequency", "Neither present"]}
                ]
            },
            {
                "title": "Medication Review",
                "section_type": "history",
                "questions": [
                    {"id": "ge_meds_hold", "type": "multi_select", "label": "Medications to Consider Holding (If Dehydrated)", "required": True, "options": ["Diuretics", "Metformin", "Nitrofurantoin", "SGLT2 Inhibitors (Dapagliflozin/Empagliflozin)", "ACE Inhibitors (Ramipril/Lisinopril)", "ARBs (Losartan/Candesartan)", "NSAIDs", "Not on any of these"]
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ge_vitals", "type": "text", "label": "Vital Signs", "required": True, "placeholder": "e.g., HR 90, Temp 36°C, SpO2 99%"},
                    {"id": "ge_ent", "type": "multi_select", "label": "ENT Examination", "required": False, "options": ["Tympanic membranes normal B/L", "Pharynx normal", "No lymphadenopathy", "No coryza", "Abnormal finding"]},
                    {"id": "ge_hydration_exam", "type": "multi_select", "label": "Hydration Assessment", "required": True, "options": ["Mucous membranes moist", "Eyes not sunken", "Skin turgor normal", "CRT normal (<2 sec)", "Signs of dehydration present - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Clinical dehydration = consider admission for IV fluids. Especially elderly/children.", "red_flag_negative": ""},
                    {"id": "ge_abdo", "type": "single_select", "label": "Abdominal Examination", "required": True, "options": ["Epigastric tenderness on deep palpation only, BS present, no masses", "RLQ tenderness - ?appendicitis", "Guarding/rigidity - RED FLAG", "Mass palpated"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Guarding/rigidity = acute abdomen. Urgent surgical assessment.", "red_flag_negative": ""},
                    {"id": "ge_urine_dip", "type": "single_select", "label": "Urine Dipstick", "required": False, "options": ["Normal", "Abnormal (specify)", "Not performed"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Viral Gastroenteritis (most common)",
                    "Bacterial Gastroenteritis (Campylobacter, Salmonella, Shigella)",
                    "C. difficile Colitis (recent antibiotics/hospitalisation)",
                    "Inflammatory Bowel Disease (bloody diarrhoea, systemic symptoms)",
                    "Appendicitis (RLQ pain, guarding)",
                    "Urinary Tract Infection (dysuria, frequency)",
                    "Medication Side Effect (metformin, antibiotics)"
                ],
                "questions": [
                    {"id": "ge_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Gastroenteritis - mild/moderate", "Gastroenteritis - dehydration requiring management", "Alternative diagnosis suspected"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: unable to tolerate oral fluids, severe abdominal pain, bloody diarrhoea, high fever, signs of dehydration (dizziness, reduced urine, dry mouth). Push oral fluids - small frequent sips. Handwashing advice. Delayed script: Imodium/Arret PRN (if diarrhoea persists without fever/blood), Cyclizine PRN (if nausea). Hold diuretics/ACEi/ARBs/NSAIDs/SGLT2i if dehydrated. School/work exclusion: 48 hours after last episode of diarrhoea/vomiting. Food handlers, healthcare workers, education staff MUST be excluded. Stool sample if: persistent >7 days, bloody, recent antibiotics/hospitalisation, or public health concern.",
                "questions": [
                    {"id": "ge_fluids", "type": "toggle", "label": "Push Oral Fluids Advised?", "required": True},
                    {"id": "ge_hygiene", "type": "toggle", "label": "Handwashing Advice Given?", "required": True},
                    {"id": "ge_symptomatic", "type": "multi_select", "label": "Symptomatic Medication (Delayed Script)", "required": False, "options": ["Imodium / Arret (Loperamide) PRN", "Cyclizine PRN (nausea)", "None"]},
                    {"id": "ge_meds_hold_action", "type": "multi_select", "label": "Medications Held", "required": False, "options": ["Diuretic held", "ACE Inhibitor held", "ARB held", "NSAID held", "SGLT2i held", "Metformin held", "Not applicable"]},
                    {"id": "ge_stool", "type": "single_select", "label": "Stool Sample (Molecular Enterics)", "required": False, "options": ["Sent", "May need - not yet sent", "Not indicated"]},
                    {"id": "ge_ocp", "type": "toggle", "label": "Ova, Cysts & Parasites? (3 samples over 10 days - if indicated)", "required": False},
                    {"id": "ge_exclusion_group", "type": "multi_select", "label": "School/Work Exclusion Group", "required": False, "options": ["Child attending school/nursery", "School/nursery teacher", "Food handler", "Healthcare worker", "Not applicable"]},
                    {"id": "ge_exclusion_advised", "type": "toggle", "label": "48 Hours Post-Last Episode Exclusion Advised?", "required": False},
                    {"id": "ge_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if red flags, review with stool results, or routine follow-up"}
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
    seed_gastroenteritis()