from app.database import SessionLocal
from app.models import User, Template, Category

def seed_ankle_oedema():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Cardiovascular").first()
    if not category: category = Category(name="Cardiovascular"); db.add(category); db.commit()

    t = {
        "title": "Ankle Oedema Assessment",
        "description": "Focused assessment for bilateral ankle oedema covering cardiac, venous, renal, and hepatic causes with compression therapy and red flags.",
        "category": "Cardiovascular",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "oed_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Bilateral ankle swelling for 2 months, worse in evenings"},
                    {"id": "oed_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 62"},
                    {"id": "oed_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 months"},
                    {"id": "oed_side", "type": "single_select", "label": "Side", "required": True, "options": ["Bilateral", "Right only - ?DVT RED FLAG", "Left only - ?DVT RED FLAG"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Unilateral swelling = DVT until proven otherwise. Measure calf circumference + urgent Doppler.", "red_flag_negative": ""},
                    {"id": "oed_timing", "type": "single_select", "label": "Timing", "required": True, "options": ["Worse in evening (gravitational/venous)", "Constant throughout day", "Worse in morning (nephrotic/liver)", "No pattern"]},
                    {"id": "oed_pitting", "type": "toggle", "label": "Pitting? (Leaves indentation on pressure)", "required": True}
                ]
            },
            {
                "title": "RED FLAGS - Cardiac & Systemic",
                "section_type": "history",
                "questions": [
                    {"id": "oed_sob", "type": "toggle", "label": "Shortness of Breath?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: SOB + oedema = ?heart failure. Urgent CXR, ECG, NT-proBNP. Cardiology referral.", "red_flag_negative": ""},
                    {"id": "oed_orthopnoea", "type": "toggle", "label": "Orthopnoea? (SOB lying flat)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Orthopnoea = classic heart failure symptom. Urgent cardiac workup.", "red_flag_negative": ""},
                    {"id": "oed_pnd", "type": "toggle", "label": "Paroxysmal Nocturnal Dyspnoea? (Waking gasping for air)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: PND = significant heart failure. Urgent cardiology.", "red_flag_negative": ""},
                    {"id": "oed_chest_pain", "type": "toggle", "label": "Chest Pain?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Chest pain + oedema = ?IHD with heart failure. Urgent assessment.", "red_flag_negative": ""},
                    {"id": "oed_palpitations", "type": "toggle", "label": "Palpitations?", "required": False},
                    {"id": "oed_calf_pain", "type": "toggle", "label": "Unilateral Calf Pain / Tenderness? (DVT)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Calf pain + unilateral swelling = DVT. Urgent Wells score + Doppler.", "red_flag_negative": ""},
                    {"id": "oed_liver_history", "type": "toggle", "label": "Known Liver Disease / Alcohol Excess?", "required": False},
                    {"id": "oed_renal_history", "type": "toggle", "label": "Known Renal Disease / Frothy Urine?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Frothy urine = ?nephrotic syndrome (proteinuria). Check urinalysis + U&E/albumin.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Medications & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "oed_meds_cause", "type": "multi_select", "label": "Medications That Cause Oedema", "required": True, "options": ["Calcium Channel Blockers (Amlodipine)", "NSAIDs", "Pioglitazone", "Gabapentin/Pregabalin", "Corticosteroids", "HRT / Oestrogen", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: CCB-induced oedema common (especially amlodipine). Consider dose reduction or switching class.", "red_flag_negative": ""},
                    {"id": "oed_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
                    {"id": "oed_pmh", "type": "multi_select", "label": "Relevant PMHx", "required": False, "options": ["Hypertension", "Diabetes", "IHD/Heart failure", "CKD", "Liver disease", "DVT/PE", "Varicose veins", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "oed_bp", "type": "text", "label": "Blood Pressure (mmHg)", "required": True, "placeholder": "e.g., 128/84"},
                    {"id": "oed_hr", "type": "number", "label": "Heart Rate (bpm)", "required": True, "placeholder": "e.g., 80"},
                    {"id": "oed_weight", "type": "number", "label": "Weight (kg)", "required": False, "placeholder": "e.g., 74"},
                    {"id": "oed_jvp", "type": "single_select", "label": "JVP", "required": True, "options": ["Normal (not elevated)", "Elevated - RED FLAG", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Elevated JVP = ?right heart failure. Urgent cardiac workup.", "red_flag_negative": ""},
                    {"id": "oed_heart_sounds", "type": "single_select", "label": "Heart Sounds", "required": True, "options": ["HS 1+2 Normal, No Murmurs", "S3 gallop - RED FLAG", "Murmur present", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: S3 gallop = ventricular dysfunction/heart failure. Urgent echo.", "red_flag_negative": ""},
                    {"id": "oed_chest", "type": "single_select", "label": "Chest Auscultation", "required": True, "options": ["Clear B/L", "Crackles (heart failure) - RED FLAG", "Wheeze", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Crackles = pulmonary oedema/heart failure. Urgent CXR + diuretics.", "red_flag_negative": ""},
                    {"id": "oed_extent", "type": "single_select", "label": "Oedema Extent", "required": True, "options": ["Ankles only", "To mid-calf", "To knee", "Above knee / thighs", "Sacral (bedbound)"]},
                    {"id": "oed_pulses", "type": "single_select", "label": "DP + PT Pulses", "required": True, "options": ["B/L present + normal", "Reduced/absent - ?PAD", "Not assessed"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced/absent pulses = ?PAD. ABPI before compression. Compression contraindicated if ABPI <0.8.", "red_flag_negative": ""},
                    {"id": "oed_varicose", "type": "toggle", "label": "Varicose Veins / Venous Changes?", "required": False},
                    {"id": "oed_calf_tenderness", "type": "toggle", "label": "Calf Tenderness? (DVT)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Calf tenderness = ?DVT. Measure circumference + Wells score.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Gravitational / Venous Insufficiency (most common)",
                    "Heart Failure (left/right/biventricular)",
                    "Medication-Induced (CCB, NSAIDs, pioglitazone)",
                    "Nephrotic Syndrome (proteinuria, low albumin)",
                    "Chronic Kidney Disease",
                    "Liver Cirrhosis (low albumin)",
                    "Deep Vein Thrombosis (unilateral)",
                    "Lymphoedema (non-pitting)",
                    "Hypothyroidism (myxoedema)",
                    "Pelvic Mass / Venous Obstruction",
                    "Idiopathic Oedema (women, cyclical)"
                ],
                "questions": [
                    {"id": "oed_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "U&E / eGFR", "LFTs + Albumin", "Fasting Lipids", "Fasting Glucose / HbA1c", "TFTs", "NT-proBNP", "None"]},
                    {"id": "oed_urinalysis", "type": "single_select", "label": "Urinalysis", "required": False, "options": ["Normal", "Proteinuria - RED FLAG", "Haematuria", "Not done"]},
                    {"id": "oed_ecg", "type": "toggle", "label": "12-Lead ECG?", "required": False},
                    {"id": "oed_abpi", "type": "toggle", "label": "ABPI Needed? (Before compression if pulses reduced/PAD risk)", "required": False}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Return immediately if: new shortness of breath, orthopnoea/PND, chest pain, palpitations, or sudden unilateral leg swelling/pain develops. Conservative: regular calf-pump exercises (walking, ankle rotations), avoid prolonged standing/sitting, leg elevation above heart level in evenings. Compression: Class 2 below-knee stockings (safe if pulses normal/ABPI >0.8). Do NOT use compression if ABPI <0.8 or suspected PAD. If CCB-induced: consider dose reduction or switching to alternative antihypertensive. If NT-proBNP elevated or cardiac features: prompt echocardiogram + cardiology referral. Weight monitoring: weigh weekly - 2kg rapid gain = fluid retention.",
                "questions": [
                    {"id": "oed_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Venous insufficiency / gravitational", "?Heart failure - investigating", "Medication-induced oedema", "?Nephrotic syndrome", "?Liver disease", "Lymphoedema", "Uncertain"]},
                    {"id": "oed_compression", "type": "single_select", "label": "Compression Therapy", "required": False, "options": ["None", "Class 1 (light)", "Class 2 below-knee (Mediven CCL2)", "Contraindicated (PAD/ABPI <0.8)"]},
                    {"id": "oed_elevation", "type": "toggle", "label": "Leg Elevation Advised?", "required": False},
                    {"id": "oed_exercise", "type": "toggle", "label": "Calf-Pump Exercises Advised?", "required": False},
                    {"id": "oed_medication_review", "type": "toggle", "label": "Causative Medication Reviewed?", "required": False},
                    {"id": "oed_referral", "type": "single_select", "label": "Referral", "required": False, "options": ["None", "Cardiology (?heart failure)", "Vascular (PAD/ABPI)", "Renal (?nephrotic)", "Echocardiogram"]},
                    {"id": "oed_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2-4 weeks with blood results, sooner if SOB develops"}
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
    seed_ankle_oedema()