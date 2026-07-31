from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_hyperthyroidism():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Endocrinology").first()
    if not category: category = Category(name="Endocrinology"); db.add(category); db.commit()

    t = {
        "title": "Hyperthyroidism",
        "description": "Focused assessment for hyperthyroidism covering symptom screening, examination, TFT interpretation, carbimazole dosing by age/T4, and safety-netting.",
        "category": "Endocrinology",
        "content": {"sections": [
            {
                "title": "Presenting Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "hyper_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Feeling hot, shaky, and losing weight for 2 months"},
                    {"id": "hyper_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 42"},
                    {"id": "hyper_symptoms", "type": "multi_select", "label": "Presenting Symptoms", "required": True, "options": ["Heat intolerance (hot when others cold)", "Fatigue / exhaustion", "Weight loss", "Anxiety / irritability", "Hand tremor", "Palpitations", "Infrequent menses / menstrual disturbance", "Diarrhoea", "Diaphoresis (excess sweating)", "None"]},
                    {"id": "hyper_duration", "type": "text", "label": "Symptom Duration", "required": True, "placeholder": "e.g., 8 weeks"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "hyper_neck", "type": "multi_select", "label": "Neck Examination", "required": True, "options": ["Goitre", "Lymphadenopathy", "Neither present"]},
                    {"id": "hyper_eye_signs", "type": "multi_select", "label": "Eye Signs", "required": True, "options": ["Loss of eyebrow hair (lateral third)", "Exophthalmos / Proptosis", "Lid lag", "Lid retraction", "None present"]},
                    {"id": "hyper_tremor", "type": "single_select", "label": "Tremor (Hands Outstretched)", "required": True, "options": ["Present", "Absent"]},
                    {"id": "hyper_proximal_myopathy", "type": "toggle", "label": "Proximal Myopathy?", "required": False},
                    {"id": "hyper_reflexes", "type": "single_select", "label": "Reflexes", "required": True, "options": ["Brisk (hyperthyroid)", "Slow-relaxing (hypothyroid)", "Normal"]},
                    {"id": "hyper_skin_hair", "type": "single_select", "label": "Skin / Hair", "required": False, "options": ["Abnormal (warm, moist, fine hair)", "Normal"]},
                    {"id": "hyper_nails", "type": "multi_select", "label": "Nail / Peripheral Signs", "required": False, "options": ["Onycholysis (Plummer's nails)", "Clubbing", "Thyroid acropachy", "None present"]},
                    {"id": "hyper_leg_oedema", "type": "single_select", "label": "Leg Oedema", "required": False, "options": ["Pitting present (high-output HF)", "Absent"]},
                    {"id": "hyper_palmar_erythema", "type": "toggle", "label": "Palmar Erythema?", "required": False}
                ]
            },
            {
                "title": "Investigations & TFT Interpretation",
                "section_type": "assessment",
                "questions": [
                    {"id": "hyper_tsh", "type": "number", "label": "TSH (mU/L)", "required": False, "placeholder": "e.g., 0.01 (NR: 0.4-4.0)"},
                    {"id": "hyper_ft4", "type": "number", "label": "Free T4 (pmol/L)", "required": False, "placeholder": "e.g., 45 (NR: 9-25)"},
                    {"id": "hyper_ft4_category", "type": "single_select", "label": "fT4 Level", "required": False, "options": ["fT4 <50 pmol/L", "fT4 >50 pmol/L", "fT4 normal (<22) - ?subclinical", "Not yet available"]},
                    {"id": "hyper_tft_pattern", "type": "single_select", "label": "TFT Pattern", "required": False, "options": ["TSH low + T4 high = Overt Hyperthyroidism", "TSH <0.27 + T4 normal/low = Subclinical Hyperthyroidism", "TSH low + T4 normal (on replacement) = ?TSHoma", "Awaiting results"]},
                    {"id": "hyper_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["TFTs (TSH + Free T4)", "Coeliac screen (IgA TTG)", "Immunoglobulin levels (IgA)", "Anti-TSH receptor antibodies (endocrine to arrange)", "Thyroid ultrasound (not routine)", "None"]},
                    {"id": "hyper_repeat_tft", "type": "single_select", "label": "Repeat TFT Interval", "required": False, "options": ["2 weeks (if fT4 >50)", "8 weeks (if fT4 <50)", "8 weeks (subclinical - pending endocrine)", "Not applicable"]}
                ]
            },
            {
                "title": "Carbimazole Dosing",
                "section_type": "plan",
                "questions": [
                    {"id": "hyper_carbimazole_dose", "type": "single_select", "label": "Carbimazole Dose (Age + fT4 Matrix)", "required": False, "options": ["<80 years + fT4 <50 → Carbimazole 30mg OD", "<80 years + fT4 >50 → Carbimazole 60mg OD", "≥80 years + fT4 <50 → Carbimazole 5mg OD", "≥80 years + fT4 >50 → Carbimazole 20mg OD", "Not started - subclinical, pending endocrine review", "Not indicated"]},
                    {"id": "hyper_propranolol", "type": "single_select", "label": "Propranolol (Symptom Control)", "required": False, "options": ["Propranolol 10mg QDS (palpitations/anxiety/tremor)", "Not indicated"]}
                ]
            },
            {
                "title": "Impression & Management",
                "section_type": "plan",
                "safety_netting": "STOP Carbimazole and attend for urgent FBC if: pyrexia, sore throat, or mouth ulcers develop (agranulocytosis risk - peak 3 months). Attend A&E if palpitations or fast heart rate. Patient information leaflet: Hyperthyroidism Patient Information. Subclinical hyperthyroidism (TSH <0.27 + T4 normal/low): withhold Carbimazole until hypopituitarism excluded by endocrinology. Repeat TFTs in 8 weeks. Eltroxin monitoring: target TSH 0.4-2.5 mU/L. No dose change if asymptomatic with TSH in upper half of reference range. TSH <0.1 = avoid. TSH 0.1-0.4 = tolerated in younger patients. Low TSH in >60 years = prompt 25mcg reduction (increased osteoporosis + 3-fold AF risk). Persistently high TSH despite Eltroxin = consider coeliac disease or autoimmune gastritis.",
                "questions": [
                    {"id": "hyper_diagnosis", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Overt Hyperthyroidism - GP managed", "Subclinical Hyperthyroidism - endocrine referral", "TSHoma Suspected - urgent endocrine", "Euthyroid - no further action", "Biochemical confirmation pending"]},
                    {"id": "hyper_safety", "type": "multi_select", "label": "Safety-Netting & Education", "required": True, "options": ["Stop Carbimazole + urgent FBC if fever/sore throat/mouth ulcers (agranulocytosis)", "Attend A&E if palpitations or fast heart rate", "Patient information leaflet provided", "Aware of repeat TFT schedule"]},
                    {"id": "hyper_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None - GP managed", "Endocrinology - subclinical hyperthyroidism", "Endocrinology - hypopituitarism workup", "Endocrinology - TSHoma suspected"]},
                    {"id": "hyper_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2 weeks if fT4>50, 8 weeks if fT4<50, with repeat TFTs"}
                ]
            }
        ]},
        "is_public": True
    }

    existing = db.query(Template).filter(Template.title == t["title"], Template.created_by == admin.id).first()
    
    if existing:
        # Update existing template instead of deleting
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    new_t = Template(title=t["title"], description=t["description"], category=t["category"], content=t["content"], is_public=True, created_by=admin.id, version=1)
    db.add(new_t); db.commit()
    print(f"Template '{t['title']}' created with {len(t['content']['sections'])} sections!"); db.close()

if __name__ == "__main__":
    seed_hyperthyroidism()