from app.database import SessionLocal
from app.models import User, Template, Category

def seed_testicular_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Men's Health").first()
    if not category: category = Category(name="Men's Health"); db.add(category); db.commit()

    t = {
        "title": "Testicular Pain / Scrotal Pain",
        "description": "Emergency-focused assessment for testicular pain with torsion red flags, differential diagnosis, and management.",
        "category": "Men's Health",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    
                    {"id": "tes_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 16", "is_red_flag": True, "red_flag_positive": "RED FLAG: Age <25 (peak 12-18) with acute testicular pain = torsion until proven otherwise.", "red_flag_negative": ""},
                    {"id": "tes_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (seconds-minutes)", "Gradual (hours-days)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden severe onset = torsion until proven otherwise. Refer immediately.", "red_flag_negative": ""},
                    {"id": "tes_duration", "type": "text", "label": "Duration of Pain", "required": True, "placeholder": "e.g., 3 hours", "is_red_flag": True, "red_flag_positive": "RED FLAG: <6 hours = window for testicular salvage. Do NOT delay referral for imaging.", "red_flag_negative": ""},
                    {"id": "tes_side", "type": "single_select", "label": "Side", "required": True, "options": ["Right", "Left", "Bilateral"]},
                    {"id": "tes_trauma", "type": "toggle", "label": "Recent Trauma?", "required": False}
                ]
            },
            {
                "title": "Torsion RED FLAGS - Must Exclude FIRST",
                "section_type": "history",
                "questions": [
                    {"id": "tes_severe_sudden", "type": "toggle", "label": "Sudden SEVERE Pain? (Out of proportion to findings)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sudden severe pain = TESTICULAR TORSION UNTIL PROVEN OTHERWISE. Immediate urology referral/A&E. Do NOT wait for ultrasound.", "red_flag_negative": ""},
                    {"id": "tes_nausea_vomiting", "type": "toggle", "label": "Nausea / Vomiting?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Nausea/vomiting with testicular pain strongly suggests torsion. Refer immediately.", "red_flag_negative": ""},
                    {"id": "tes_previous_torsion", "type": "toggle", "label": "Previous Torsion / Orchiopexy?", "required": False},
                    {"id": "tes_high_riding", "type": "toggle", "label": "High-Riding Testis / Horizontal Lie on Exam?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: High-riding testis with horizontal lie = classic torsion sign. Refer immediately.", "red_flag_negative": ""},
                    {"id": "tes_cremasteric", "type": "toggle", "label": "Absent Cremasteric Reflex on Exam?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent cremasteric reflex = torsion until proven otherwise. Refer immediately.", "red_flag_negative": "Cremasteric reflex present - reassuring but does NOT exclude torsion."},
                    {"id": "tes_prehn_sign", "type": "toggle", "label": "Pain RELIEVED on Elevation? (Prehn's Sign)", "required": False},
                    {"id": "tes_any_suspicion", "type": "toggle", "label": "ANY Clinical Suspicion of Torsion?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: ANY suspicion of torsion = immediate urology referral/A&E. Do NOT delay for imaging if clinically clear. Testicular salvage window is 6 hours.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "tes_fever", "type": "toggle", "label": "Fever?", "required": False},
                    {"id": "tes_dysuria", "type": "toggle", "label": "Dysuria / Urethral Discharge? (STI/UTI)", "required": True},
                    {"id": "tes_urinary_frequency", "type": "toggle", "label": "Urinary Frequency / Urgency?", "required": False},
                    {"id": "tes_swelling_redness", "type": "toggle", "label": "Swelling / Redness / Heat?", "required": False},
                    {"id": "tes_lump", "type": "toggle", "label": "Testicular Lump? (Painless or painful)", "required": False},
                    {"id": "tes_groin_swelling", "type": "toggle", "label": "Groin Swelling? (Possible hernia)", "required": False},
                    {"id": "tes_abdominal_loin_pain", "type": "toggle", "label": "Abdominal / Loin Pain? (Referred renal colic)", "required": False}
                ]
            },
            {
                "title": "Sexual & Past History",
                "section_type": "history",
                "questions": [
                    {"id": "tes_new_partner", "type": "toggle", "label": "New / Multiple Partners? Unprotected Intercourse?", "required": True},
                    {"id": "tes_sti_partner", "type": "toggle", "label": "STI Symptoms in Partner?", "required": False},
                    {"id": "tes_previous_history", "type": "multi_select", "label": "Past History", "required": False, "options": ["Previous torsion/orchiopexy", "Mumps", "UTI/prostatitis", "Recent catheterisation/instrumentation", "Known hernia", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "tes_testis_position", "type": "single_select", "label": "Position of Testis", "required": True, "options": ["Normal lie and height", "High-riding", "Horizontal lie", "Swollen - cannot assess"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal testis position = suspect torsion.", "red_flag_negative": ""},
                    {"id": "tes_cremasteric_exam", "type": "single_select", "label": "Cremasteric Reflex", "required": True, "options": ["Present", "Absent", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Absent cremasteric reflex with acute pain = torsion.", "red_flag_negative": ""},
                    {"id": "tes_swelling", "type": "single_select", "label": "Swelling / Erythema", "required": True, "options": ["None", "Mild swelling", "Significant swelling", "Erythema present"]},
                    {"id": "tes_transillumination", "type": "toggle", "label": "Transillumination Positive? (Hydrocele)", "required": False},
                    {"id": "tes_lymph_nodes", "type": "toggle", "label": "Inguinal Lymphadenopathy?", "required": False},
                    {"id": "tes_hernia", "type": "toggle", "label": "Hernial Orifices Abnormal? (Cough impulse)", "required": False}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Testicular Torsion (EMERGENCY - refer immediately)",
                    "Epididymo-orchitis (STI vs UTI)",
                    "Torsion of Testicular Appendage (Hydatid of Morgagni)",
                    "Hydrocele",
                    "Varicocele",
                    "Inguinal Hernia",
                    "Testicular Tumour (usually painless but can bleed/infarct)",
                    "Referred Pain (Renal colic, nerve entrapment)",
                    "Trauma/Haematoma",
                    "Fournier's Gangrene (rare but life-threatening)"
                ],
                "questions": [
                    {"id": "tes_working_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Suspected TORSION - REFER IMMEDIATELY", "Epididymo-orchitis", "Torsion of appendix testis", "Hydrocele/Varicocele", "Inguinal hernia", "Testicular tumour suspected", "Renal colic (referred pain)", "Uncertain"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "plan",
                "questions": [
                    {"id": "tes_urine_dip", "type": "toggle", "label": "Urine Dip / MSU Sent?", "required": False},
                    {"id": "tes_sti_screen", "type": "toggle", "label": "STI Screen? (Chlamydia/Gonorrhoea NAAT)", "required": False},
                    {"id": "tes_doppler_uss", "type": "toggle", "label": "Doppler USS Testes? (Only if torsion excluded clinically)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT wait for USS if torsion strongly suspected. Refer immediately. USS is for when diagnosis unclear and torsion excluded clinically.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "If torsion suspected: REFER IMMEDIATELY to urology/A&E. Do NOT delay for investigations. Testicular salvage window is 6 hours from onset. If epididymo-orchitis: antibiotics per local guidance (Ceftriaxone + Doxycycline if STI suspected, Ofloxacin or Ciprofloxacin if UTI organism). Analgesia, scrotal support, rest. RED FLAGS - return immediately if: pain suddenly worsens, swelling increases rapidly, fever develops, nausea/vomiting, or any new testicular symptoms. If STI diagnosed: contact tracing, abstain from sex until treatment complete, repeat screen as per guidelines.",
                "questions": [
                    {"id": "tes_emergency_referral", "type": "toggle", "label": "Emergency Urology/A&E Referral? (Torsion suspected)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Suspected torsion = immediate referral. Do not delay. Testicle can be lost within 6 hours.", "red_flag_negative": ""},
                    {"id": "tes_antibiotics", "type": "single_select", "label": "Antibiotics (if epididymo-orchitis)", "required": False, "options": ["None", "Ceftriaxone IM + Doxycycline PO (STI suspected)", "Ofloxacin PO (UTI organism)", "Ciprofloxacin PO (UTI organism)", "Other"]},
                    {"id": "tes_analgesia", "type": "toggle", "label": "Analgesia Prescribed?", "required": False},
                    {"id": "tes_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 48 hours if epididymo-orchitis, or PRN if resolving"}
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
    seed_testicular_pain()