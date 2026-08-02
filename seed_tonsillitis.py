from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_tonsillitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Tonsillitis",
        "description": "Focused assessment for tonsillitis covering quinsy red flags, Centor/FeverPAIN scoring, Penicillin V prescribing, and recurrent tonsillitis referral criteria.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Complications (Screen First)",
                "section_type": "history",
                "questions": [
                    {"id": "ton_cant_swallow", "type": "toggle", "label": "Unable to Swallow Own Saliva?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to swallow saliva = ?Quinsy/Epiglottitis/Airway compromise. EMERGENCY - same-day ENT/A&E.", "red_flag_negative": ""},
                    {"id": "ton_unwell_faint", "type": "toggle", "label": "Increasingly Unwell - Feeling Faint / Confusion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Systemic toxicity = ?Sepsis. Urgent hospital admission.", "red_flag_negative": ""},
                    {"id": "ton_trismus", "type": "toggle", "label": "Trismus (Difficulty Opening Jaw)? - Quinsy/Peritonsillar Abscess", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Trismus = QUINSY until proven otherwise. Same-day ENT referral.", "red_flag_negative": ""},
                    {"id": "ton_meningism", "type": "toggle", "label": "Signs of Meningism? (Neck Stiffness, Photophobia)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Meningism = ?Deep neck space infection. EMERGENCY admission.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "ton_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Severe sore throat and fever for 2 days"},
                    {"id": "ton_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 2 days"},
                    {"id": "ton_sore_throat", "type": "toggle", "label": "Sore Throat?", "required": True},
                    {"id": "ton_fever", "type": "toggle", "label": "Fever?", "required": True},
                    {"id": "ton_fluid_intake", "type": "single_select", "label": "Fluid Intake", "required": True, "options": ["Normal", "Reduced", "Unable to swallow - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to manage oral fluids = ?need admission for IV fluids + antibiotics.", "red_flag_negative": ""},
                    {"id": "ton_cough", "type": "toggle", "label": "Cough? (Absence = Centor/FeverPAIN Point)", "required": True},
                    {"id": "ton_jaw_opening", "type": "single_select", "label": "Jaw Opening", "required": True, "options": ["Normal", "Trismus (Difficulty Opening) - RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Trismus = QUINSY. Same-day ENT.", "red_flag_negative": ""},
                    {"id": "ton_previous_tonsillectomy", "type": "toggle", "label": "Previous Tonsillectomy?", "required": False},
                    {"id": "ton_recurrent_episodes_1yr", "type": "number", "label": "Number of Episodes in Past Year", "required": False, "placeholder": "e.g., 8 (≥7 = ENT referral)"},
                    {"id": "ton_recurrent_episodes_2yr", "type": "number", "label": "Number of Episodes in Past 2 Years (Per Year)", "required": False, "placeholder": "e.g., 5 (≥5/year = ENT referral)"},
                    {"id": "ton_recurrent_episodes_3yr", "type": "number", "label": "Number of Episodes in Past 3 Years (Per Year)", "required": False, "placeholder": "e.g., 3 (≥3/year = ENT referral)"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "ton_tonsils", "type": "single_select", "label": "Tonsils", "required": True, "options": ["Enlarged + exudate present", "Enlarged - no exudate", "Unilateral bulging - RED FLAG (Quinsy)", "Normal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral bulging = QUINSY. Same-day ENT for drainage.", "red_flag_negative": ""},
                    {"id": "ton_lymph", "type": "toggle", "label": "Jugulodigastric Lymphadenopathy?", "required": True},
                    {"id": "ton_coryza", "type": "toggle", "label": "Coryza?", "required": False},
                    {"id": "ton_tm", "type": "single_select", "label": "Tympanic Membranes", "required": False, "options": ["Normal B/L", "Abnormal"]},
                    {"id": "ton_meningism_exam", "type": "toggle", "label": "Signs of Meningism on Exam?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Meningism present = EMERGENCY. Deep neck space infection.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Severity Scoring",
                "section_type": "assessment",
                "questions": [
                    {"id": "ton_centor_fever", "type": "toggle", "label": "Fever >38°C? (Centor 1pt / FeverPAIN 1pt)", "required": True},
                    {"id": "ton_centor_exudate", "type": "toggle", "label": "Tonsillar Exudate? (Centor 1pt / FeverPAIN 1pt)", "required": True},
                    {"id": "ton_centor_lymph", "type": "toggle", "label": "Tender Anterior Cervical Lymphadenopathy? (Centor 1pt)", "required": True},
                    {"id": "ton_centor_cough_absent", "type": "toggle", "label": "Absence of Cough? (Centor 1pt / FeverPAIN 1pt)", "required": True},
                    {"id": "ton_feverpain_attend", "type": "toggle", "label": "Attended Within 3 Days of Onset? (FeverPAIN 1pt)", "required": False},
                    {"id": "ton_feverpain_inflamed", "type": "toggle", "label": "Severely Inflamed Tonsils? (FeverPAIN 1pt)", "required": False},
                    {"id": "ton_score", "type": "single_select", "label": "Score Result → Action", "required": True, "options": ["Centor ≥3 / FeverPAIN ≥4 → Antibiotics Indicated", "FeverPAIN 2-3 → Back-Up (Delayed) Antibiotic", "FeverPAIN 0-1 → Symptomatic Only, No Antibiotics"]}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Viral Tonsillitis / Pharyngitis (Most Common)",
                    "Streptococcal Tonsillitis (Group A Strep)",
                    "Quinsy / Peritonsillar Abscess (RED FLAG - Unilateral Bulging, Trismus)",
                    "Glandular Fever / EBV (Prolonged, Lymphadenopathy, Splenomegaly)",
                    "Epiglottitis (RED FLAG - Stridor, Drooling)",
                    "Deep Neck Space Infection (RED FLAG)",
                    "Head & Neck Cancer (Age >45, Persistent, Unilateral)",
                    "Gonococcal Pharyngitis"
                ],
                "questions": [
                    {"id": "ton_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Viral Tonsillitis (Symptomatic Only)", "Bacterial Tonsillitis (Antibiotics Indicated)", "Quinsy / Peritonsillar Abscess - URGENT ENT", "Suspected Glandular Fever - ?EBV Serology", "Recurrent Tonsillitis - Meets ENT Referral Criteria"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: unable to swallow saliva, difficulty breathing, trismus (difficulty opening jaw), neck swelling, feeling faint/confused, or symptoms worsen significantly. Red flags discussed. Aware of out-of-hours services. Average recovery time is around 1 week. Antibiotics (if Centor ≥3 or FeverPAIN ≥4): Phenoxymethylpenicillin (Calvepen) 666mg QDS before food for 5 days. Confirm no penicillin allergy. AVOID Amoxicillin if glandular fever possible (widespread rash risk). Symptomatic: Difflam spray, Paracetamol. If symptoms >7 days: consider EBV IgM serology. Age >45 with persistent symptoms: consider head and neck cancer. Recurrent tonsillitis ENT referral criteria: ≥7 episodes in 1 year, ≥5/year for 2 years, or ≥3/year for 3 years.",
                "questions": [
                    {"id": "ton_antibiotic", "type": "single_select", "label": "Antibiotic (If Indicated)", "required": False, "options": ["Phenoxymethylpenicillin (Calvepen) 666mg QDS Before Food for 5 Days", "Clarithromycin (Penicillin Allergy)", "Delayed / Back-Up Prescription", "Not indicated"]},
                    {"id": "ton_penicillin_allergy", "type": "toggle", "label": "Penicillin Allergy?", "required": False},
                    {"id": "ton_avoid_amoxicillin", "type": "toggle", "label": "Avoid Amoxicillin? (If ?Glandular Fever - Rash Risk)", "required": False},
                    {"id": "ton_symptomatic", "type": "multi_select", "label": "Symptomatic Treatment", "required": False, "options": ["Difflam Spray", "Paracetamol", "Ibuprofen (if no CI)"]},
                    {"id": "ton_ebv", "type": "toggle", "label": "EBV IgM Serology? (If Symptoms >7 Days or Atypical)", "required": False},
                    {"id": "ton_ent_referral", "type": "single_select", "label": "ENT Referral", "required": False, "options": ["None", "Routine - Recurrent Tonsillitis Criteria Met", "Urgent - Quinsy / Deep Neck Space Infection", "Urgent - ?Malignancy (Age >45, Persistent)"]},
                    {"id": "ton_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if no improvement in 1 week, sooner if red flags"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        print(f"⏭️  SKIPPED: {title} already exists (ID={existing.id})")
        db.close()
        return
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_tonsillitis()