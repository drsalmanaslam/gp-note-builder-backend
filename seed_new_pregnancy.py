from app.database import SessionLocal
from app.models import User, Template, Category

def seed_new_pregnancy():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "New Pregnancy - Initial Consultation",
        "description": "Comprehensive first pregnancy visit covering confirmation, EDD calculation, supplements, vaccinations, lifestyle advice, miscarriage safety-netting, and antenatal appointment schedule.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Screen First",
                "section_type": "history",
                "questions": [
                    {"id": "np_pv_bleeding", "type": "toggle", "label": "PV Bleeding?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: PV bleeding in pregnancy = attend maternity hospital A&E directly.", "red_flag_negative": ""},
                    {"id": "np_abdo_pain", "type": "toggle", "label": "Abdominal Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Abdominal pain + PV bleeding = ?ectopic. Urgent maternity assessment.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Pregnancy Confirmation & Wellbeing",
                "section_type": "history",
                "questions": [
                    {"id": "np_confirmation", "type": "single_select", "label": "Pregnancy Confirmation", "required": True, "options": ["Positive Home Pregnancy Test", "Positive Clinic hCG", "Both"]},
                    {"id": "np_wellbeing", "type": "single_select", "label": "Patient Wellbeing Regarding Pregnancy", "required": True, "options": ["Happy / Planned", "Ambivalent", "Concerned / Unplanned - Needs Support"]},
                    {"id": "np_lmp", "type": "text", "label": "Last Menstrual Period (LMP)", "required": True, "placeholder": "e.g., 15/05/2026"},
                    {"id": "np_cycle", "type": "single_select", "label": "Cycle Length & Regularity", "required": True, "options": ["Regular 28 Days", "Regular but Longer/Shorter", "Irregular"]},
                    {"id": "np_edd", "type": "text", "label": "Estimated Due Date (EDD) - http://www.nmh.ie/pregnancy/pregnancy-due-date-calculator.54.html", "required": False, "placeholder": "e.g., 20/02/2027"},
                    {"id": "np_gestation", "type": "text", "label": "Estimated Gestational Age", "required": True, "placeholder": "e.g., 6 weeks"},
                    {"id": "np_gp", "type": "text", "label": "Gravida / Para", "required": True, "placeholder": "e.g., G1P0"}
                ]
            },
            {
                "title": "Past History & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "np_pmh", "type": "textarea", "label": "Past Medical History", "required": True, "placeholder": "e.g., Nil significant / Asthma / Diabetes"},
                    {"id": "np_surgical", "type": "textarea", "label": "Past Surgical History", "required": False, "placeholder": "e.g., Nil / Appendicectomy"},
                    {"id": "np_medications", "type": "textarea", "label": "Current Medications", "required": True, "placeholder": "e.g., None / Levothyroxine 75mcg OD"},
                    {"id": "np_smoking", "type": "single_select", "label": "Smoking Status", "required": True, "options": ["Non-Smoker", "Ex-Smoker", "Current Smoker - Advise Cessation"]},
                    {"id": "np_fh_congenital", "type": "toggle", "label": "Family History of Congenital Abnormality?", "required": True},
                    {"id": "np_chickenpox", "type": "toggle", "label": "History of Chickenpox? (VZV Immunity)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: No chickenpox history = check VZV IgG. If non-immune = avoid contact + consider postpartum vaccination.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination & Initial Tests",
                "section_type": "examination",
                "questions": [
                    {"id": "np_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 116/74"},
                    {"id": "np_clinic_hcg", "type": "single_select", "label": "Clinic hCG", "required": False, "options": ["Positive", "Negative", "Not Performed"]}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "questions": [
                    {"id": "np_maternity_bloods", "type": "multi_select", "label": "Maternity Bloods Ordered", "required": False, "options": ["FBC", "Blood Group + Hold", "HIV", "Hepatitis C", "Syphilis Serology", "Rubella IgG", "VZV IgG"]},
                    {"id": "np_msu", "type": "toggle", "label": "MSU - Screen for Asymptomatic Bacteriuria (≥10⁵ Organisms = Treat Even if Asymptomatic)", "required": False}
                ]
            },
            {
                "title": "Supplements",
                "section_type": "plan",
                "questions": [
                    {"id": "np_folic_acid", "type": "single_select", "label": "Folic Acid (Until 12 Weeks)", "required": True, "options": ["Folic Acid 400mcg Daily", "Folic Acid 5mg Daily (High Risk: Coeliac, Diabetes, BMI>30, Anticonvulsants)", "Pregnacare (Combined Multivitamin)", "Not Started - Advise Today"]},
                    {"id": "np_vitamin_d", "type": "toggle", "label": "Vitamin D 10mcg Daily (Throughout Pregnancy + Breastfeeding)?", "required": True}
                ]
            },
            {
                "title": "Vaccinations",
                "section_type": "plan",
                "questions": [
                    {"id": "np_vacc_pertussis", "type": "toggle", "label": "Pertussis (Tdap) - Between 16-36 Weeks?", "required": False},
                    {"id": "np_vacc_influenza", "type": "toggle", "label": "Influenza - Any Time During Pregnancy?", "required": False},
                    {"id": "np_vacc_rsv", "type": "toggle", "label": "RSV (Abrysvo) - CDC 32-36 Weeks During RSV Season?", "required": False}
                ]
            },
            {
                "title": "Lifestyle & Safety Advice",
                "section_type": "plan",
                "safety_netting": "MISCARRIAGE SAFETY-NETTING: Attend maternity hospital A&E directly if PV bleeding occurs at any point in pregnancy. RCOG Healthy Eating in Pregnancy: https://www.rcog.org.uk/globalassets/documents/patients/patient-information-leaflets/pregnancy/pi-healthy-eating-and-vitamin-supplements-in-pregnancy.pdf. EDD Calculator: http://www.nmh.ie/pregnancy/pregnancy-due-date-calculator.54.html. Antenatal appointment schedule: 12w (Hospital), <20w (Hospital), 24w (GP), 28w (GP/Hospital if first preg), 30w (GP), 32w (Hospital), 34w (GP), 36w (Hospital), 37w (GP), 38w (Hospital), 39w (GP), 40w (Hospital). Post-birth: 2w baby check, 6w mother + baby check.",
                "questions": [
                    {"id": "np_lifestyle", "type": "multi_select", "label": "Lifestyle & Safety Advice Given", "required": False, "options": ["Avoid Smoking", "Avoid Soft Cheeses (Listeria)", "Avoid Emptying Cat Litter Trays (Toxoplasmosis)", "Limit Tinned Fish (Mercury)", "Avoid Pâté, High-Dose Vitamin A, Raw Eggs", "Limit Coffee to <2 Cups/Day", "Wash Hands After Nappies/Child's Nose (CMV)", "Gentle Regular Exercise + Pelvic Floor", "Avoid Hot Tubs + Saunas", "Avoid Zika Transmission Countries"]}
                ]
            },
            {
                "title": "Administrative Actions & Plan",
                "section_type": "plan",
                "questions": [
                    {"id": "np_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["New Pregnancy Confirmed - Well", "New Pregnancy - With Concerns", "Red Flags Present - ESCALATE"]},
                    {"id": "np_admin", "type": "multi_select", "label": "Administrative Actions", "required": False, "options": ["New Pregnancy Added to Patient File", "Referred to Local Hospital Antenatal Services", "HSE Mother & Child Scheme Form Completed", "RFP Pregnancy Patient Leaflet Given"]},
                    {"id": "np_followup", "type": "text", "label": "Next Appointment", "required": True, "placeholder": "e.g., 12 weeks - Hospital antenatal clinic"}
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
    seed_new_pregnancy()