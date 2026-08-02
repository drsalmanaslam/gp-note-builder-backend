from app.database import SessionLocal
from app.models import User, Template, Category

def seed_vaginal_discharge():
    db = SessionLocal()
    
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin found!")
        db.close()
        return

    title = "Vaginal Discharge"
    existing = db.query(Template).filter(Template.title == title).first()
    if existing:
        db.delete(existing)
        db.commit()

    template = Template(
        title=title,
        description="Assessment of vaginal discharge covering bacterial vaginosis, candidiasis, trichomoniasis, STI screening, and red flags for PID/cervicitis per BASHH guidelines.",
        category="Women's Health",
        content={"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "vd_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., 5 days"},
                    {"id": "vd_colour", "type": "single_select", "label": "Colour", "required": True, "options": ["White/creamy", "Grey/off-white", "Yellow/green", "Blood-stained", "Clear/mucoid"]},
                    {"id": "vd_consistency", "type": "single_select", "label": "Consistency", "required": True, "options": ["Thin/watery", "Thick/curdy (cottage cheese)", "Frothy", "Mucoid/stretchy"]},
                    {"id": "vd_odour", "type": "single_select", "label": "Odour", "required": True, "options": ["None", "Fishy (especially after sex)", "Foul/offensive", "Yeasty"]},
                    {"id": "vd_itch", "type": "toggle", "label": "Itching?", "required": True},
                    {"id": "vd_irritation", "type": "toggle", "label": "Vulval Irritation/Soreness?", "required": True},
                    {"id": "vd_dysuria", "type": "toggle", "label": "Dysuria?", "required": False},
                    {"id": "vd_dyspareunia", "type": "toggle", "label": "Dyspareunia (Painful Sex)?", "required": False},
                    {"id": "vd_abdo_pain", "type": "toggle", "label": "Abdominal/Pelvic Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Pelvic pain + discharge = ?PID. Examine for cervical motion tenderness, adnexal tenderness. Swabs + antibiotics urgently.", "red_flag_negative": ""},
                    {"id": "vd_fever", "type": "toggle", "label": "Fever/Malaise?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Fever + discharge = ?ascending infection/PID. Urgent assessment needed.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Risk Factors & Sexual History",
                "section_type": "history",
                "questions": [
                    {"id": "vd_sexual_activity", "type": "toggle", "label": "Sexually Active?", "required": True},
                    {"id": "vd_new_partner", "type": "toggle", "label": "New Sexual Partner? (<3 months)", "required": False},
                    {"id": "vd_multiple_partners", "type": "toggle", "label": "Multiple Partners?", "required": False},
                    {"id": "vd_condoms", "type": "single_select", "label": "Condom Use", "required": False, "options": ["Always", "Sometimes", "Never", "Not applicable"]},
                    {"id": "vd_previous_sti", "type": "toggle", "label": "Previous STI?", "required": True},
                    {"id": "vd_partner_symptoms", "type": "toggle", "label": "Partner Has Symptoms?", "required": False},
                    {"id": "vd_antibiotics", "type": "toggle", "label": "Recent Antibiotics? (Candida risk)", "required": True},
                    {"id": "vd_douching", "type": "toggle", "label": "Vaginal Douching / Scented Products?", "required": True},
                    {"id": "vd_iucd", "type": "toggle", "label": "IUCD/Coil in Situ?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: IUCD + discharge + pain = ?PID/actinomycosis. Low threshold for removal.", "red_flag_negative": ""},
                    {"id": "vd_menstrual", "type": "text", "label": "LMP & Cycle Regularity", "required": False, "placeholder": "e.g., Regular 28-day cycle, LMP 2 weeks ago"},
                    {"id": "vd_pregnancy", "type": "toggle", "label": "Possibility of Pregnancy?", "required": True},
                    {"id": "vd_postmenopausal", "type": "toggle", "label": "Postmenopausal? (Atrophic vaginitis)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "vd_abdo_exam", "type": "single_select", "label": "Abdominal Examination", "required": False, "options": ["Normal", "Suprapubic tenderness", "Lower abdominal tenderness", "Rebound/guarding - RED FLAG", "Not examined"]},
                    {"id": "vd_speculum", "type": "toggle", "label": "Speculum Examination Performed?", "required": False},
                    {"id": "vd_discharge_appearance", "type": "single_select", "label": "Discharge on Examination", "required": False, "options": ["Thin, grey-white, adherent to walls (BV)", "Thick, white, curdy (Candida)", "Frothy, yellow-green (Trichomonas)", "Mucopurulent (Cervicitis)", "Normal physiological", "Not examined"]},
                    {"id": "vd_cervix", "type": "single_select", "label": "Cervical Appearance", "required": False, "options": ["Normal", "Friable/contact bleeding (Cervicitis)", "Strawberry cervix (Trichomonas)", "Not examined"]},
                    {"id": "vd_bimanual", "type": "single_select", "label": "Bimanual Findings", "required": False, "options": ["Normal", "Cervical motion tenderness (PID)", "Adnexal tenderness/mass (PID/TOA)", "Not examined"]},
                    {"id": "vd_swabs", "type": "multi_select", "label": "Swabs Taken", "required": False, "options": ["High vaginal swab (HVS)", "Endocervical swab (NAAT - Chlamydia/Gonorrhoea)", "Trichomonas swab", "BV swab", "None"]}
                ]
            },
            {
                "title": "Assessment & Differential",
                "section_type": "assessment",
                "differentials": [
                    "Bacterial Vaginosis (BV) - fishy odour, thin grey discharge, pH >4.5, clue cells",
                    "Vulvovaginal Candidiasis (Thrush) - thick white discharge, itch, pH <4.5",
                    "Trichomoniasis - frothy yellow-green discharge, strawberry cervix, pH >5",
                    "Chlamydia/Gonorrhoea - mucopurulent discharge, friable cervix",
                    "Pelvic Inflammatory Disease (PID) - discharge + pelvic pain + fever",
                    "Atrophic Vaginitis (postmenopausal) - thin discharge, dryness, pH >5",
                    "Foreign Body (retained tampon) - foul-smelling discharge",
                    "Physiological discharge - clear/white, no odour, no symptoms"
                ],
                "questions": [
                    {"id": "vd_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Bacterial Vaginosis", "Vulvovaginal Candidiasis (Thrush)", "Trichomoniasis", "Chlamydia/Gonorrhoea", "Pelvic Inflammatory Disease", "Atrophic Vaginitis", "Physiological discharge - reassure", "Mixed infection"]},
                    {"id": "vd_severity", "type": "single_select", "label": "Severity", "required": True, "options": ["Mild - no systemic symptoms", "Moderate - significant symptoms", "Severe - systemic features/complicated"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately or attend A&E if: severe abdominal pain, fever >38°C, heavy bleeding, or feeling very unwell. BV: Metronidazole 400mg BD for 7 days (or 2g stat if adherence concern). Avoid alcohol during and 48h after metronidazole. Thrush: Clotrimazole pessary 500mg stat + clotrimazole cream (or fluconazole 150mg PO stat). Trichomoniasis: Metronidazole 2g stat (or 400mg TDS 7 days). Partner notification and treatment essential for Trichomoniasis and STIs. Refer to GUM clinic for contact tracing. Condoms until treatment complete. Test of cure for Trichomoniasis at 4 weeks.",
                "questions": [
                    {"id": "vd_treatment", "type": "multi_select", "label": "Treatment", "required": True, "options": ["Metronidazole 400mg BD 7 days (BV)", "Metronidazole 2g stat (BV/Trichomonas)", "Clotrimazole pessary + cream (Thrush)", "Fluconazole 150mg PO stat (Thrush)", "Doxycycline 100mg BD 7 days (Chlamydia)", "Ceftriaxone 500mg IM (Gonorrhoea)", "Refer GUM clinic", "Refer gynaecology (PID/complex)", "Reassurance only - physiological"]},
                    {"id": "vd_analgesia", "type": "toggle", "label": "Analgesia Advised?", "required": False},
                    {"id": "vd_partner_notification", "type": "toggle", "label": "Partner Notification/Treatment Discussed?", "required": True},
                    {"id": "vd_sti_screen", "type": "toggle", "label": "Full STI Screen Offered? (HIV, Syphilis, Hep B/C)", "required": True},
                    {"id": "vd_contraception", "type": "toggle", "label": "Contraception Discussed?", "required": False},
                    {"id": "vd_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Return if symptoms persist 1 week, GUM clinic for STI screen, TOC at 4 weeks if Trichomonas"}
                ]
            }
        ]},
        is_public=True,
        created_by=admin.id
    )
    
    db.add(template)
    db.commit()
    print(f"✅ Created: {title}")
    db.close()

if __name__ == "__main__":
    seed_vaginal_discharge()