from app.database import SessionLocal
from app.models import User, Template, Category

def seed_otitis_externa():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Otitis Externa",
        "description": "Focused assessment for otitis externa covering malignant otitis red flags, TM perforation-safe topical antibiotics, and practical prescribing tips.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Malignant / Necrotising Otitis Externa",
                "section_type": "history",
                "questions": [
                    {"id": "oe_pain_disproportionate", "type": "toggle", "label": "Pain Out of Proportion to Clinical Findings?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe pain disproportionate to exam = ?MALIGNANT/NECROTISING OTITIS EXTERNA. ESCALATE URGENTLY - ENT same-day.", "red_flag_negative": ""},
                    {"id": "oe_pain_neck_jaw", "type": "toggle", "label": "Pain Extending to Neck or Jaw?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pain beyond ear = ?malignant otitis externa (skull base osteomyelitis). URGENT ENT.", "red_flag_negative": ""},
                    {"id": "oe_cn_involvement", "type": "toggle", "label": "Cranial Nerve Involvement? (Facial weakness, hoarseness, dysphagia)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: CN involvement = malignant otitis externa until proven otherwise. EMERGENCY ENT.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "oe_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Itchy, painful right ear with discharge for 3 days"},
                    {"id": "oe_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 3 days"},
                    {"id": "oe_side", "type": "single_select", "label": "Affected Ear", "required": True, "options": ["Right", "Left", "Both"]},
                    {"id": "oe_symptoms", "type": "multi_select", "label": "Core Symptoms", "required": True, "options": ["Itching", "Irritation of ear canal", "Otalgia (ear pain)", "Otorrhoea (discharge)", "Reduced hearing"]},
                    {"id": "oe_cotton_buds", "type": "toggle", "label": "Use of Cotton Buds / Foreign Objects in Ear?", "required": True},
                    {"id": "oe_swimming", "type": "toggle", "label": "Frequent Swimming?", "required": False},
                    {"id": "oe_diabetes", "type": "toggle", "label": "Diabetes?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Diabetes + otitis externa = higher risk of malignant/necrotising OE. Lower threshold for ENT referral.", "red_flag_negative": ""},
                    {"id": "oe_immunosuppressed", "type": "toggle", "label": "Immunosuppressant Use / Immunocompromised?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Immunocompromised + otitis externa = high risk of severe infection. ENT referral.", "red_flag_negative": ""},
                    {"id": "oe_skin_conditions", "type": "multi_select", "label": "Skin Conditions", "required": False, "options": ["Psoriasis", "Eczema", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "oe_canal_discharge", "type": "toggle", "label": "Discharge Present?", "required": True},
                    {"id": "oe_canal_inflammation", "type": "toggle", "label": "Inflammation / Boggy / Swollen Canal?", "required": True},
                    {"id": "oe_tm_visualised", "type": "single_select", "label": "Tympanic Membrane Visualised?", "required": True, "options": ["Yes - intact", "Yes - perforated", "No - cannot visualise (use non-ototoxic drops)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: If TM cannot be visualised or perforation possible = use SAFE topical agent: Ciprofloxacin (Ciloxan) or Exocin.", "red_flag_negative": ""},
                    {"id": "oe_perichondritis", "type": "toggle", "label": "Perichondritis? (Pinna erythema/swelling beyond canal)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Perichondritis = infection of cartilage. Needs oral antibiotics (Ciprofloxacin) + ENT referral.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Otitis Externa (Bacterial - most common)",
                    "Fungal Otitis Externa (Aspergillus / Candida)",
                    "Chronic Suppurative Otitis Media (CSOM)",
                    "Malignant / Necrotising Otitis Externa (RED FLAG - elderly, diabetic, immunocompromised)",
                    "Perichondritis (RED FLAG)",
                    "Contact Dermatitis of Ear Canal",
                    "Ramsay Hunt Syndrome (vesicles, CN VII involvement)"
                ],
                "questions": [
                    {"id": "oe_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Otitis Externa - Bacterial", "Otitis Externa - ?Fungal", "Suspected Malignant Otitis Externa - URGENT ENT", "Perichondritis - Oral Antibiotics + ENT", "CSOM Suspected"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if no improvement, or if symptoms worsen. Red flags discussed: pain out of proportion, pain extending to neck/jaw, cranial nerve involvement. If TM perforation possible or TM cannot be visualised: use SAFE (non-ototoxic) option - Ciprofloxacin (Ciloxan) 4 drops BD or Exocin. If inflammation present: Betnesol eye/ear/nose drops 2 drops every 3 hours. Alternatives: Betnesol-N, Kenacomb, Kenacomb otic ointment, Genticin, Gentisone HC, Sofradex. If fungal suspected: Canesten drops (unlicensed). Practical tip: list an alternative on the same script (e.g., Ciloxan OR Betnesol-N) as topical ear antibiotics often run short in pharmacies. Paracetamol for pain. Advise against scratching/cleaning ear with cotton buds or objects. If not improving: ear swab + consider oral antibiotics (Ciprofloxacin) or ENT referral for aural toilet.",
                "questions": [
                    {"id": "oe_topical", "type": "single_select", "label": "Topical Treatment (TM Safe if Perforation Possible)", "required": False, "options": ["Ciloxan (Ciprofloxacin) 4 Drops BD - Safe if TM Perforation", "Exocin - Safe if TM Perforation", "Betnesol Eye/Ear/Nose Drops 2 Drops Every 3 Hours", "Betnesol-N", "Kenacomb / Kenacomb Otic Ointment", "Genticin / Gentisone HC", "Sofradex", "Canesten Drops (?Fungal - Unlicensed)"]},
                    {"id": "oe_alternative_listed", "type": "toggle", "label": "Alternative Listed on Script? (Pharmacies Often Short on Ear Drops)", "required": False},
                    {"id": "oe_analgesia", "type": "toggle", "label": "Paracetamol Advised for Pain?", "required": False},
                    {"id": "oe_advice", "type": "toggle", "label": "Avoid Cotton Buds / Scratching / Objects Advised?", "required": True},
                    {"id": "oe_swab", "type": "toggle", "label": "Ear Swab? (If Not Improving - Check Resistance / Fungal)", "required": False},
                    {"id": "oe_oral_abx", "type": "toggle", "label": "Oral Antibiotics? (Ciprofloxacin if severe/perichondritis)", "required": False},
                    {"id": "oe_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP Managed", "ENT - Urgent (Malignant OE / Perichondritis)", "ENT - Routine (Persistent / Aural Toilet)"]},
                    {"id": "oe_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if no improvement in 5-7 days, sooner if red flags"}
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
    seed_otitis_externa()