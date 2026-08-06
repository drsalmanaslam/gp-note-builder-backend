from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_first_line_bloods():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "GP-Related Topics").first()
    if not category:
        category = Category(name="GP-Related Topics")
        db.add(category)
        db.commit()

    t = {
        "title": "First-Line Bloods by Common GP Presentation",
        "description": "Quick-reference guide for appropriate blood tests by presentation. Adapt to local lab panels and clinical judgement. Not exhaustive; tailor to history and examination.",
        "category": "GP-Related Topics",
        "content": {"sections": [
            {
                "title": "General / Constitutional",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_fatigue", "type": "text", "label": "Fatigue / Tiredness (TATT)", "required": False, "placeholder": "FBC, U&E, LFTs, TFTs, CRP/ESR, HbA1c, ferritin, B12/folate, calcium, coeliac screen (anti-TTG)", "output_phrase": "Fatigue: {value}"},
                    {"id": "bloods_weight_loss", "type": "text", "label": "Unexplained Weight Loss", "required": False, "placeholder": "FBC, U&E, LFTs, TFTs, CRP/ESR, HbA1c, calcium, coeliac screen; consider CA125/PSA only if clinically indicated", "output_phrase": "Weight loss: {value}"},
                    {"id": "bloods_fever", "type": "text", "label": "Fever / Generally Unwell", "required": False, "placeholder": "FBC, CRP, U&E, LFTs, blood cultures (if indicated), consider HIV test", "output_phrase": "Fever: {value}"},
                    {"id": "bloods_well_person", "type": "text", "label": "New Patient / Well-Person Check", "required": False, "placeholder": "FBC, U&E, LFTs, HbA1c, lipid profile, TFTs (if symptomatic)", "output_phrase": "Well-person: {value}"}
                ]
            },
            {
                "title": "Cardiovascular",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_hypertension", "type": "text", "label": "Hypertension — New Diagnosis", "required": False, "placeholder": "U&E, eGFR, HbA1c, lipid profile, urine ACR", "output_phrase": "Hypertension: {value}"},
                    {"id": "bloods_chest_pain", "type": "text", "label": "Chest Pain (Non-Acute, Primary Care)", "required": False, "placeholder": "FBC, U&E, LFTs, lipid profile, HbA1c; troponin only if acute presentation → refer/999", "output_phrase": "Chest pain: {value}"},
                    {"id": "bloods_palpitations", "type": "text", "label": "Palpitations", "required": False, "placeholder": "FBC, U&E, TFTs, magnesium, calcium; consider ECG", "output_phrase": "Palpitations: {value}"},
                    {"id": "bloods_dvt_pe", "type": "text", "label": "Suspected DVT/PE", "required": False, "placeholder": "D-dimer (if Wells score low/moderate), FBC, U&E, LFTs, clotting", "output_phrase": "DVT/PE: {value}"}
                ]
            },
            {
                "title": "Respiratory",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_sob", "type": "text", "label": "Breathlessness (Chronic, Unexplained)", "required": False, "placeholder": "FBC, U&E, LFTs, TFTs, BNP/NT-proBNP; consider D-dimer if PE suspected", "output_phrase": "Breathlessness: {value}"}
                ]
            },
            {
                "title": "Gastrointestinal",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_abdo_pain", "type": "text", "label": "Abdominal Pain (Non-Acute)", "required": False, "placeholder": "FBC, U&E, LFTs, CRP, amylase/lipase; consider coeliac screen", "output_phrase": "Abdominal pain: {value}"},
                    {"id": "bloods_jaundice", "type": "text", "label": "Jaundice", "required": False, "placeholder": "FBC, LFTs (incl. GGT), U&E, clotting, hepatitis serology", "output_phrase": "Jaundice: {value}"},
                    {"id": "bloods_ibd", "type": "text", "label": "Change in Bowel Habit / Suspected IBD", "required": False, "placeholder": "FBC, CRP, ferritin, U&E, LFTs, coeliac screen, faecal calprotectin", "output_phrase": "?IBD: {value}"},
                    {"id": "bloods_diarrhoea", "type": "text", "label": "Diarrhoea (Chronic)", "required": False, "placeholder": "FBC, U&E, LFTs, TFTs, coeliac screen, CRP/ESR, stool culture", "output_phrase": "Diarrhoea: {value}"}
                ]
            },
            {
                "title": "Endocrine / Metabolic",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_diabetes", "type": "text", "label": "Suspected Diabetes", "required": False, "placeholder": "HbA1c, fasting glucose (if indicated), U&E, lipid profile", "output_phrase": "Diabetes: {value}"},
                    {"id": "bloods_thyroid", "type": "text", "label": "Thyroid Symptoms", "required": False, "placeholder": "TFTs (TSH, free T4 +/- free T3); consider thyroid antibodies", "output_phrase": "Thyroid: {value}"},
                    {"id": "bloods_adrenal", "type": "text", "label": "Suspected Addison's / Adrenal Insufficiency", "required": False, "placeholder": "U&E (Na/K), 9am cortisol, glucose", "output_phrase": "Adrenal: {value}"}
                ]
            },
            {
                "title": "Musculoskeletal / Rheumatological",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_joint_pain", "type": "text", "label": "Joint Pain / Suspected Inflammatory Arthritis", "required": False, "placeholder": "FBC, CRP, ESR, rheumatoid factor, anti-CCP, uric acid (if gout suspected)", "output_phrase": "Joint pain: {value}"},
                    {"id": "bloods_gout", "type": "text", "label": "Suspected Gout", "required": False, "placeholder": "Serum uric acid, U&E, FBC", "output_phrase": "Gout: {value}"},
                    {"id": "bloods_pmr_gca", "type": "text", "label": "Suspected PMR / GCA", "required": False, "placeholder": "FBC, ESR, CRP, U&E, LFTs", "output_phrase": "PMR/GCA: {value}"},
                    {"id": "bloods_osteoporosis", "type": "text", "label": "Osteoporosis Risk Assessment", "required": False, "placeholder": "FBC, U&E, LFTs, calcium, phosphate, vitamin D, TFTs", "output_phrase": "Osteoporosis: {value}"}
                ]
            },
            {
                "title": "Neurological / Psychiatric",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_headache", "type": "text", "label": "Headache (Non-Acute)", "required": False, "placeholder": "FBC, ESR/CRP (esp. if >50, consider GCA), U&E, LFTs", "output_phrase": "Headache: {value}"},
                    {"id": "bloods_dementia", "type": "text", "label": "Cognitive Decline / Suspected Dementia", "required": False, "placeholder": "FBC, U&E, LFTs, TFTs, B12/folate, calcium, HbA1c, syphilis serology (per local protocol)", "output_phrase": "Dementia screen: {value}"},
                    {"id": "bloods_depression", "type": "text", "label": "Depression / Anxiety (Baseline Before Medication)", "required": False, "placeholder": "FBC, U&E, LFTs, TFTs; consider HbA1c", "output_phrase": "Depression: {value}"},
                    {"id": "bloods_dizziness", "type": "text", "label": "Dizziness / Suspected Anaemia or Postural Cause", "required": False, "placeholder": "FBC, U&E, glucose", "output_phrase": "Dizziness: {value}"}
                ]
            },
            {
                "title": "Haematological",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_anaemia", "type": "text", "label": "Anaemia (New Finding)", "required": False, "placeholder": "FBC, blood film, ferritin, B12, folate, reticulocyte count, U&E, LFTs; consider haemolysis screen if indicated", "output_phrase": "Anaemia: {value}"},
                    {"id": "bloods_bruising", "type": "text", "label": "Easy Bruising / Bleeding", "required": False, "placeholder": "FBC, clotting screen, LFTs", "output_phrase": "Bruising: {value}"},
                    {"id": "bloods_infections", "type": "text", "label": "Recurrent Infections", "required": False, "placeholder": "FBC with differential, immunoglobulins, HIV test", "output_phrase": "Infections: {value}"}
                ]
            },
            {
                "title": "Renal / Urinary",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_ckd", "type": "text", "label": "Suspected CKD / Renal Impairment", "required": False, "placeholder": "U&E, eGFR, urine ACR, calcium, phosphate, PTH (if advanced)", "output_phrase": "CKD: {value}"},
                    {"id": "bloods_uti", "type": "text", "label": "Recurrent UTIs", "required": False, "placeholder": "U&E, glucose/HbA1c, MSU; consider renal tract imaging referral", "output_phrase": "UTI: {value}"}
                ]
            },
            {
                "title": "Gynaecological",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_menorrhagia", "type": "text", "label": "Menorrhagia / Heavy Menstrual Bleeding", "required": False, "placeholder": "FBC, ferritin, TFTs, coagulation screen (if indicated)", "output_phrase": "Menorrhagia: {value}"},
                    {"id": "bloods_amenorrhoea", "type": "text", "label": "Amenorrhoea / Suspected Menopause", "required": False, "placeholder": "FSH, LH, oestradiol, TFTs, prolactin, pregnancy test", "output_phrase": "Amenorrhoea: {value}"}
                ]
            },
            {
                "title": "Lifestyle / Substance-Related",
                "section_type": "plan",
                "questions": [
                    {"id": "bloods_alcohol", "type": "text", "label": "Alcohol Excess (Screening)", "required": False, "placeholder": "FBC (MCV), LFTs (incl. GGT), U&E, clotting", "output_phrase": "Alcohol: {value}"}
                ]
            },
            {
                "title": "Notes",
                "section_type": "plan",
                "safety_netting": "Always correlate with history, examination, and red flag screening. Consider urine dip/MSU, ECG, and imaging alongside bloods where relevant. Repeat/trend abnormal results before acting on isolated findings where appropriate. Adjust panels per local pathology formulary and ICB guidance.",
                "questions": []
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")
    db.close()

if __name__ == "__main__":
    seed_first_line_bloods()