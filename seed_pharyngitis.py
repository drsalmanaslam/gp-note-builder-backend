from app.database import SessionLocal
from app.models import User, Template, Category

def seed_pharyngitis():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "ENT").first()
    if not category: category = Category(name="ENT"); db.add(category); db.commit()

    t = {
        "title": "Pharyngitis / Sore Throat Assessment",
        "description": "Emergency-focused assessment for sore throat with Centor/FeverPAIN criteria, red flags for quinsy/airway compromise, and antibiotic stewardship.",
        "category": "ENT",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                   
                    {"id": "phar_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 22"},
                    {"id": "phar_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Acute (hours-2 days)", "Gradual (days)", "Prolonged (>3 weeks)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Persistent unilateral sore throat >3 weeks + smoker/alcohol/age >45 = exclude malignancy. Urgent ENT.", "red_flag_negative": ""},
                    {"id": "phar_side", "type": "single_select", "label": "Pain Location", "required": True, "options": ["Bilateral", "Unilateral - Right", "Unilateral - Left"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Severe unilateral pain = ?quinsy/peritonsillar abscess. Examine for uvula deviation + trismus.", "red_flag_negative": ""},
                    {"id": "phar_dysphagia", "type": "single_select", "label": "Swallowing", "required": True, "options": ["Normal", "Painful (odynophagia)", "Difficulty swallowing solids", "Difficulty swallowing liquids", "Unable to swallow saliva (drooling)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unable to swallow saliva/drooling = airway concern. Emergency same-day ENT/A&E.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Emergency / Airway / Sepsis",
                "section_type": "history",
                "questions": [
                    {"id": "phar_stridor", "type": "toggle", "label": "Stridor / Noisy Breathing?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Stridor = airway emergency. Call 999/112. Same-day emergency ENT.", "red_flag_negative": ""},
                    {"id": "phar_drooling", "type": "toggle", "label": "Drooling / Unable to Swallow Saliva?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Drooling = airway compromise or severe obstruction. Emergency ENT/A&E.", "red_flag_negative": ""},
                    {"id": "phar_trismus", "type": "toggle", "label": "Trismus (Unable to Open Mouth Fully)?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Trismus + unilateral throat pain = QUINSY (peritonsillar abscess). Same-day ENT referral.", "red_flag_negative": ""},
                    {"id": "phar_hot_potato_voice", "type": "toggle", "label": "Muffled / 'Hot Potato' Voice?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Hot potato voice = quinsy or deep neck space infection. Emergency ENT.", "red_flag_negative": ""},
                    {"id": "phar_neck_swelling", "type": "toggle", "label": "Neck Swelling / Stiffness / Torticollis?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Neck swelling/torticollis = deep neck space infection. Emergency ENT.", "red_flag_negative": ""},
                    {"id": "phar_toxic", "type": "toggle", "label": "Systemically Unwell / Toxic / High Fever / Tachycardia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Toxic appearance with fever = sepsis possible. Same-day assessment + admission if indicated.", "red_flag_negative": ""},
                    {"id": "phar_immunocompromised", "type": "toggle", "label": "On Chemotherapy / DMARDs / Immunosuppressants?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever + sore throat in immunosuppressed/neutropenic = NEUTROPENIC SEPSIS until proven otherwise. Urgent same-day FBC + assessment.", "red_flag_negative": ""},
                    {"id": "phar_rash", "type": "toggle", "label": "Rash? (Scarlet fever - sandpaper rash, strawberry tongue)", "required": False},
                    {"id": "phar_uvula_deviation", "type": "toggle", "label": "Uvula Deviation on Exam?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Uvula deviation + unilateral pain = QUINSY. Same-day ENT for drainage.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Centor / FeverPAIN Criteria",
                "section_type": "history",
                "questions": [
                    {"id": "phar_tonsillar_exudate", "type": "toggle", "label": "Tonsillar Exudate?", "required": True},
                    {"id": "phar_tender_lymph", "type": "toggle", "label": "Tender Anterior Cervical Lymphadenopathy?", "required": True},
                    {"id": "phar_fever_history", "type": "toggle", "label": "Fever >38°C?", "required": True},
                    {"id": "phar_cough_absent", "type": "toggle", "label": "Absence of Cough?", "required": True},
                    {"id": "phar_centor_score", "type": "number", "label": "Centor Score (0-4)", "required": True, "placeholder": "e.g., 3 (≥3 = consider antibiotics)"},
                    {"id": "phar_feverpain_attend", "type": "toggle", "label": "Attended Within ≤3 Days of Onset? (FeverPAIN)", "required": False},
                    {"id": "phar_feverpain_severe", "type": "toggle", "label": "Severe Tonsil Inflammation? (FeverPAIN)", "required": False},
                    {"id": "phar_feverpain_score", "type": "number", "label": "FeverPAIN Score (0-5)", "required": False, "placeholder": "e.g., 4 (≥4 = antibiotics, 2-3 = consider)"}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "phar_cough_coryza", "type": "toggle", "label": "Cough / Coryza? (Suggests viral)", "required": False},
                    {"id": "phar_abdominal_pain", "type": "toggle", "label": "Abdominal Pain? (Common in children with strep)", "required": False},
                    {"id": "phar_joint_pains", "type": "toggle", "label": "Joint Pains?", "required": False},
                    {"id": "phar_fatigue", "type": "toggle", "label": "Prolonged Fatigue? (Glandular fever - teens/young adults)", "required": False}
                ]
            },
            {
                "title": "Past History",
                "section_type": "history",
                "questions": [
                    {"id": "phar_recurrent_tonsillitis", "type": "single_select", "label": "Recurrent Tonsillitis Frequency", "required": True, "options": ["None", "<3 episodes/year", "3-6 episodes/year", "≥7 episodes/year (or ≥5/yr for 2 years) - ENT referral criteria"]},
                    {"id": "phar_rheumatic_fever", "type": "toggle", "label": "History of Rheumatic Fever?", "required": False},
                    {"id": "phar_penicillin_allergy", "type": "toggle", "label": "Penicillin Allergy?", "required": True},
                    {"id": "phar_recent_antibiotics", "type": "toggle", "label": "Recent Antibiotic Use?", "required": False},
                    {"id": "phar_smoking_alcohol", "type": "single_select", "label": "Smoking / Alcohol (if >3 weeks unilateral)", "required": False, "options": ["Non-smoker, minimal alcohol", "Smoker", "Alcohol excess", "Both"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Smoker/alcohol excess + persistent sore throat >3 weeks = 2WW ENT to exclude malignancy.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "phar_temp", "type": "number", "label": "Temperature (°C)", "required": True, "placeholder": "e.g., 38.4"},
                    {"id": "phar_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 98"},
                    {"id": "phar_oropharynx", "type": "single_select", "label": "Oropharynx Examination", "required": True, "options": ["Mild erythema", "Significant erythema", "Tonsillar exudate", "Ulceration", "Membrane", "Candidiasis (white patches)", "Normal"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Membrane or ulceration in immunosuppressed = urgent assessment.", "red_flag_negative": ""},
                    {"id": "phar_tonsil_asymmetry", "type": "toggle", "label": "Tonsil Asymmetry / Unilateral Swelling?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral tonsil swelling = ?quinsy vs tumour. Needs ENT assessment.", "red_flag_negative": ""},
                    {"id": "phar_uvula", "type": "single_select", "label": "Uvula Position", "required": True, "options": ["Midline", "Deviated to Right", "Deviated to Left"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Uvula deviation = QUINSY. Same-day ENT referral.", "red_flag_negative": ""},
                    {"id": "phar_lymph_nodes", "type": "single_select", "label": "Cervical Lymph Nodes", "required": True, "options": ["Normal", "Tender anterior chain", "Significant lymphadenopathy", "Neck swelling/mass"]},
                    {"id": "phar_skin", "type": "toggle", "label": "Rash? (Scarlet fever - sandpaper, strawberry tongue)", "required": False},
                    {"id": "phar_splenomegaly", "type": "toggle", "label": "Splenomegaly? (Glandular fever - avoid contact sports)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Viral Pharyngitis (most common - rhinovirus, adenovirus, coronavirus)",
                    "Group A Streptococcus (GAS) Tonsillitis",
                    "Glandular Fever (EBV) - teens/young adults, prolonged, lymphadenopathy, splenomegaly",
                    "Peritonsillar Abscess (Quinsy) - trismus, uvula deviation, hot potato voice",
                    "Epiglottitis (rare, emergency - stridor, drooling, tripod position)",
                    "Scarlet Fever - GAS + sandpaper rash, strawberry tongue",
                    "Candidiasis (immunocompromised, inhaled steroid use)",
                    "Diphtheria (rare - grey membrane, unvaccinated)",
                    "Oropharyngeal Malignancy (persistent unilateral, smoking/alcohol, age >45)",
                    "Deep Neck Space Infection",
                    "Neutropenic Sepsis (fever + sore throat on chemo/immunosuppressants)",
                    "Gonococcal Pharyngitis (STI risk)"
                ],
                "questions": [
                    {"id": "phar_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Viral pharyngitis", "Streptococcal tonsillitis", "Glandular fever (EBV)", "Quinsy (peritonsillar abscess)", "Scarlet fever", "Candidiasis", "Suspected malignancy", "Neutropenic sepsis concern", "Uncertain"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "phar_throat_swab", "type": "toggle", "label": "Throat Swab? (Not routine - recurrent/atypical/public health)", "required": False},
                    {"id": "phar_monospot_ebv", "type": "toggle", "label": "FBC + Monospot/EBV Serology? (If glandular fever suspected)", "required": False},
                    {"id": "phar_fbc_urgent", "type": "toggle", "label": "Urgent FBC? (If on chemo/immunosuppressants + fever - neutropenic sepsis)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Do not delay FBC in immunosuppressed patient with fever. Neutropenic sepsis is life-threatening.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Viral: supportive - paracetamol/ibuprofen, fluids, rest. Most resolve in 7 days. Antibiotics if Centor ≥3 or FeverPAIN ≥4: Penicillin V 500mg QDS for 10 days (first-line). Clarithromycin if penicillin allergy. AVOID amoxicillin if glandular fever possible (causes widespread maculopapular rash). Quinsy/epiglottitis/airway compromise → emergency same-day ENT/A&E. Recurrent tonsillitis meeting criteria (≥7/year or ≥5/year for 2 years) → routine ENT referral for tonsillectomy. Return immediately if: difficulty breathing, stridor, drooling, unable to swallow, trismus, neck swelling, severe unilateral pain, rash develops, fever persists >3 days despite antibiotics. If glandular fever: avoid contact sports (splenic rupture risk) for at least 4-6 weeks. No alcohol while unwell.",
                "questions": [
                    {"id": "phar_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Supportive - analgesia, fluids (viral)", "Antibiotics - Penicillin V (Centor ≥3/FeverPAIN ≥4)", "Antibiotics - Clarithromycin (penicillin allergy)", "Emergency ENT/A&E referral (quinsy/airway)", "Routine ENT referral (recurrent tonsillitis)", "Safety-net + delayed antibiotic prescription"]},
                    {"id": "phar_antibiotic", "type": "text", "label": "Antibiotic Prescribed + Duration", "required": False, "placeholder": "e.g., Penicillin V 500mg QDS 10 days"},
                    {"id": "phar_avoid_amoxicillin", "type": "toggle", "label": "Avoid Amoxicillin? (If glandular fever possible - rash risk)", "required": False},
                    {"id": "phar_analgesia", "type": "toggle", "label": "Analgesia Advised? (Paracetamol + Ibuprofen)", "required": False},
                    {"id": "phar_contact_sports", "type": "toggle", "label": "Avoid Contact Sports? (If glandular fever - splenomegaly risk 4-6 weeks)", "required": False},
                    {"id": "phar_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if worsening, or 48-72h if antibiotics started"}
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
    seed_pharyngitis()