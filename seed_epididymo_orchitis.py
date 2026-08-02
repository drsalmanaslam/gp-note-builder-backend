from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_epididymo_orchitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Epididymo-Orchitis - Diagnosis & Management",
        "description": "Focused assessment for epididymo-orchitis covering testicular torsion exclusion, STI vs enteric organism treatment, and testicular tumour screening.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "RED FLAG - Testicular Torsion (Must Exclude FIRST)",
                "section_type": "history",
                "questions": [
                    {"id": "epo_onset", "type": "single_select", "label": "Onset (Torsion = Sudden/Severe; Epididymitis = Gradual Over 1-2 Days)", "required": True, "options": ["Gradual (1-2 Days) - Supports Epididymitis", "Sudden (Hours) - RAISES TORSION CONCERN"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden onset = TORSION until proven otherwise. EMERGENCY urology referral.", "red_flag_negative": ""},
                    {"id": "epo_prehn", "type": "single_select", "label": "Prehn's Sign (Pain Relieved by Lifting Scrotum?)", "required": True, "options": ["Positive (Relieved) - Supports Epididymitis", "Negative (Not Relieved/Worse) - TORSION CONCERN"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Negative Prehn's sign + sudden onset = ?torsion. EMERGENCY.", "red_flag_negative": ""},
                    {"id": "epo_cremasteric", "type": "single_select", "label": "Cremasteric Reflex", "required": True, "options": ["Intact - Supports Epididymitis", "Absent - TORSION CONCERN"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent cremasteric + sudden onset = TORSION. EMERGENCY urology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "epo_side", "type": "single_select", "label": "Side Affected", "required": True, "options": ["Right", "Left", "Bilateral"]},
                    {"id": "epo_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 2 days"},
                    {"id": "epo_scrotal_swelling", "type": "toggle", "label": "Scrotal Swelling?", "required": True},
                    {"id": "epo_urethral_discharge", "type": "toggle", "label": "Urethral Discharge?", "required": True},
                    {"id": "epo_urinary", "type": "multi_select", "label": "Urinary Symptoms", "required": True, "options": ["Dysuria", "Frequency", "Urgency", "None"]},
                    {"id": "epo_systemic", "type": "multi_select", "label": "Systemic Symptoms", "required": True, "options": ["Fever", "Vomiting (Torsion Concern)", "None"]},
                    {"id": "epo_new_partner", "type": "toggle", "label": "Recent New Partner? (STI Risk)", "required": True},
                    {"id": "epo_prostatitis", "type": "multi_select", "label": "Prostatitis Screen", "required": False, "options": ["Pain During Sex", "Perineal Pain", "Haematospermia", "None"]},
                    {"id": "epo_mass_screen", "type": "multi_select", "label": "Testicular Mass/Growth Screen", "required": True, "options": ["Testicles Getting Bigger", "Weight Loss", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Testicular enlargement + weight loss = ?malignancy. Urgent urology.", "red_flag_negative": ""},
                    {"id": "epo_trauma", "type": "toggle", "label": "Recent Trauma? (Injury, Kick, Horse/Bike Riding)", "required": False},
                    {"id": "epo_previous_episodes", "type": "toggle", "label": "Previous Episodes of This Pain?", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "epo_scrotum_erythema", "type": "toggle", "label": "Scrotal Erythema?", "required": False},
                    {"id": "epo_scrotum_oedema", "type": "toggle", "label": "Scrotal Oedema?", "required": False},
                    {"id": "epo_epididymis", "type": "single_select", "label": "Epididymis", "required": True, "options": ["Swollen + Tender - Right", "Swollen + Tender - Left", "Swollen + Tender - Bilateral", "Normal"]},
                    {"id": "epo_prehn_exam", "type": "single_select", "label": "Prehn's Sign on Examination", "required": True, "options": ["Positive (Pain Relieved by Elevation)", "Negative (No Relief / Worse)"]},
                    {"id": "epo_cremasteric_exam", "type": "single_select", "label": "Cremasteric Reflex", "required": True, "options": ["Intact", "Absent - TORSION CONCERN"]},
                    {"id": "epo_testicular_mass", "type": "toggle", "label": "Testicular Mass?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Testicular mass = ?tumour. Urgent urology + tumour markers.", "red_flag_negative": ""},
                    {"id": "epo_lymph", "type": "toggle", "label": "Inguinal Lymph Nodes Palpable?", "required": False},
                    {"id": "epo_urine_dip", "type": "text", "label": "Urine Dipstick Findings", "required": False, "placeholder": "e.g., Leucocytes+, Nitrites-"},
                    {"id": "epo_varicocoele_note", "type": "toggle", "label": "Swelling Resolves on Lying Down? (Suggests Varicocoele, NOT Epididymitis)", "required": False}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Epididymo-Orchitis (STI - Chlamydia/Gonorrhoea - Most Common <35)",
                    "Epididymo-Orchitis (Enteric Organism - Age >35 or No STI Risk)",
                    "Testicular Torsion (RED FLAG - Sudden Onset, Absent Cremasteric, Negative Prehn's)",
                    "Testicular Tumour (Painless Mass, Heaviness, Weight Loss)",
                    "Varicocoele (Resolves Lying Down, Bag of Worms)",
                    "Hydrocoele (Transilluminates)",
                    "Inguinal Hernia (Cough Impulse, Reducible)",
                    "Traumatic Epididymitis"
                ],
                "questions": [
                    {"id": "epo_msu", "type": "toggle", "label": "First-Void Urine (MSU) for Chlamydia, Gonorrhoea, M. Genitalium?", "required": True},
                    {"id": "epo_bloods_sti", "type": "multi_select", "label": "Bloods (STI Screen)", "required": False, "options": ["HIV", "Syphilis", "Hepatitis B", "Hepatitis C (If Higher Risk)"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return if no improvement within 3 days of starting antibiotics. If sudden severe pain, absent cremasteric reflex, or Prehn's sign negative: EMERGENCY urology referral for ?torsion. Reference: antibioticprescribing.ie. STI cause (age <35 or new partner): Doxycycline 100mg BD for 10-14 days. Enteric cause (age >35, no STI risk): Ciprofloxacin 500mg BD for 10 days. Symptomatic: Paracetamol/Ibuprofen, scrotal support, abstinence until treatment complete. If not improving: USS testes to exclude hydrocoele, abscess, infarction. If mass on USS: refer urology + send AFP, beta-hCG, LDH (testicular tumour markers).",
                "questions": [
                    {"id": "epo_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Epididymo-Orchitis - Likely STI (Age <35 / New Partner)", "Epididymo-Orchitis - Likely Enteric (Age >35 / No STI Risk)", "?Testicular Torsion - EMERGENCY UROLOGY", "?Testicular Tumour - Urgent Urology"]},
                    {"id": "epo_antibiotics", "type": "single_select", "label": "Empirical Antibiotics (antibioticprescribing.ie)", "required": False, "options": ["Doxycycline 100mg BD for 10-14 Days (STI Cause)", "Ciprofloxacin 500mg BD for 10 Days (Enteric Cause)", "Not Indicated"]},
                    {"id": "epo_symptomatic", "type": "multi_select", "label": "Symptomatic Treatment", "required": False, "options": ["Paracetamol + Ibuprofen", "Scrotal Support", "Abstinence Until Treatment Complete"]},
                    {"id": "epo_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return in 3 days if no improvement, USS if not resolving"}
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
    seed_epididymo_orchitis()