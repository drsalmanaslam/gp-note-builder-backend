from app.database import SessionLocal
from app.models import User, Template, Category

def seed_lower_back_pain():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Lower Back Pain Assessment",
        "description": "Focused assessment for lower back pain with red flags for cauda equina, fracture, malignancy, and infection.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "Presentation",
                "section_type": "history",
                "questions": [
                    {"id": "lbp_presenting_complaint", "type": "text", "label": "Presenting Complaint", "required": True, "placeholder": "e.g., Lower back pain for 2 weeks"},
                    {"id": "lbp_age", "type": "number", "label": "Age", "required": True, "placeholder": "e.g., 45", "is_red_flag": True, "red_flag_positive": "RED FLAG: Age >50 new onset or age <20 = consider malignancy or inflammatory cause.", "red_flag_negative": ""},
                    {"id": "lbp_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Sudden (acute injury)", "Gradual (days-weeks)", "Insidious (no clear trigger)"]},
                    {"id": "lbp_duration", "type": "text", "label": "Duration", "required": True, "placeholder": "e.g., 2 weeks"},
                    {"id": "lbp_location", "type": "single_select", "label": "Location", "required": True, "options": ["Lower back only", "Lower back + buttock", "Lower back + thigh", "Lower back + below knee", "Bilateral legs"]},
                    {"id": "lbp_radiation", "type": "single_select", "label": "Radiation", "required": False, "options": ["None", "Right leg", "Left leg", "Both legs"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bilateral leg pain/sciatica = possible cauda equina or central disc.", "red_flag_negative": ""},
                    {"id": "lbp_severity", "type": "single_select", "label": "Severity (0-10)", "required": True, "options": ["Mild (1-3)", "Moderate (4-6)", "Severe (7-9)", "Excruciating (10)"]},
                    {"id": "lbp_aggravating", "type": "multi_select", "label": "Aggravating Factors", "required": False, "options": ["Bending forward", "Sitting", "Standing", "Walking", "Coughing/sneezing", "Lying flat", "None"]},
                    {"id": "lbp_relieving", "type": "multi_select", "label": "Relieving Factors", "required": False, "options": ["Lying down", "Standing", "Walking", "Sitting", "Heat", "Analgesia", "None"]}
                ]
            },
            {
                "title": "RED FLAGS - Cauda Equina Syndrome",
                "section_type": "history",
                "questions": [
                    {"id": "lbp_saddle_anaesthesia", "type": "toggle", "label": "Numbness in Saddle Area? (Perineum, genitals, inner thighs)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Saddle anaesthesia = CAUDA EQUINA until proven otherwise. EMERGENCY - same-day MRI + neurosurgery.", "red_flag_negative": "No saddle anaesthesia."},
                    {"id": "lbp_bladder", "type": "single_select", "label": "Bladder Function", "required": True, "options": ["Normal", "Difficulty passing urine", "Loss of bladder sensation", "Urinary incontinence (new onset)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Any bladder dysfunction + back pain = CAUDA EQUINA. Emergency referral.", "red_flag_negative": ""},
                    {"id": "lbp_bowel", "type": "single_select", "label": "Bowel Function", "required": True, "options": ["Normal", "Constipation (new onset)", "Faecal incontinence", "Loss of anal sensation"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bowel dysfunction + back pain = CAUDA EQUINA. Emergency referral.", "red_flag_negative": ""},
                    {"id": "lbp_sexual_dysfunction", "type": "toggle", "label": "New Erectile Dysfunction / Loss of Genital Sensation?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Sexual dysfunction + back pain = possible cauda equina.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "RED FLAGS - Serious Pathology",
                "section_type": "history",
                "questions": [
                    {"id": "lbp_systemic", "type": "multi_select", "label": "Systemic Symptoms", "required": True, "options": ["Fever/chills", "Unexplained weight loss", "Night sweats", "Malaise/fatigue", "None"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Systemic symptoms = possible infection (discitis/osteomyelitis) or malignancy. Urgent investigation.", "red_flag_negative": ""},
                    {"id": "lbp_cancer_history", "type": "toggle", "label": "History of Cancer? (Breast, lung, prostate, thyroid, renal, myeloma)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Cancer history + back pain = spinal metastases until proven otherwise. Urgent MRI.", "red_flag_negative": "No cancer history."},
                    {"id": "lbp_night_pain", "type": "toggle", "label": "Pain That Wakes from Sleep / Prevents Lying Flat?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Nocturnal pain unrelieved by rest = malignancy or infection.", "red_flag_negative": "No night pain."},
                    {"id": "lbp_trauma", "type": "toggle", "label": "Recent Trauma / Fall? (Especially if osteoporosis risk)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Trauma + back pain = possible vertebral fracture.", "red_flag_negative": ""},
                    {"id": "lbp_iv_drug", "type": "toggle", "label": "IV Drug Use / Immunosuppression / Recent Infection?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Risk factors for spinal infection. Urgent investigation.", "red_flag_negative": ""},
                    {"id": "lbp_morning_stiffness", "type": "toggle", "label": "Prolonged Morning Stiffness >30 mins? (Improves with activity)", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: Inflammatory back pain pattern = possible ankylosing spondylitis. Check HLA-B27, CRP, refer rheumatology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Past History & Risk Factors",
                "section_type": "history",
                "questions": [
                    {"id": "lbp_previous_episodes", "type": "toggle", "label": "Previous Episodes of Back Pain?", "required": False},
                    {"id": "lbp_osteoporosis", "type": "toggle", "label": "Osteoporosis / Steroid Use?", "required": False},
                    {"id": "lbp_smoking", "type": "single_select", "label": "Smoking", "required": True, "options": ["Never", "Ex-smoker", "Current"]},
                    {"id": "lbp_occupation", "type": "single_select", "label": "Occupation", "required": False, "options": ["Sedentary/Desk", "Manual labour", "Driving", "Healthcare", "Other"]},
                    {"id": "lbp_meds", "type": "toggle", "label": "On Anticoagulants / Antiplatelets? (Spinal haematoma risk)", "required": False}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "lbp_inspection", "type": "single_select", "label": "Inspection", "required": True, "options": ["Normal", "Scoliosis", "Loss of lumbar lordosis", "Muscle spasm", "Step/deformity"]},
                    {"id": "lbp_slr_right", "type": "single_select", "label": "Straight Leg Raise - Right", "required": False, "options": ["Normal (>70°)", "Reduced (30-70°)", "Severely reduced (<30°)", "Not tested"]},
                    {"id": "lbp_slr_left", "type": "single_select", "label": "Straight Leg Raise - Left", "required": False, "options": ["Normal (>70°)", "Reduced (30-70°)", "Severely reduced (<30°)", "Not tested"]},
                    {"id": "lbp_power", "type": "single_select", "label": "Lower Limb Power (MRC Grade)", "required": False, "options": ["5/5 throughout", "4/5 weakness", "≤3/5 significant weakness", "Not tested"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Significant motor weakness = possible nerve root compression or cauda equina.", "red_flag_negative": ""},
                    {"id": "lbp_sensation", "type": "multi_select", "label": "Sensory Deficit (Dermatomes)", "required": False, "options": ["None", "L2", "L3", "L4", "L5", "S1", "S2-S4 (saddle)"]},
                    {"id": "lbp_reflexes", "type": "single_select", "label": "Reflexes", "required": False, "options": ["Normal", "Reduced knee (L3/4)", "Reduced ankle (S1)", "Brisk/upgoing plantars", "Not tested"]},
                    {"id": "lbp_anal_tone", "type": "single_select", "label": "Anal Tone (PR if cauda equina suspected)", "required": False, "options": ["Normal", "Reduced", "Absent", "Not examined"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Reduced/absent anal tone = CAUDA EQUINA. Emergency.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Non-specific Mechanical Low Back Pain (most common)",
                    "Disc Prolapse with Radiculopathy",
                    "Spinal Stenosis",
                    "Cauda Equina Syndrome (EMERGENCY)",
                    "Vertebral Fracture (osteoporosis/trauma)",
                    "Spinal Infection (Discitis/Osteomyelitis)",
                    "Spinal Metastases / Malignancy",
                    "Ankylosing Spondylitis / Inflammatory Back Pain",
                    "Spondylolisthesis",
                    "Facet Joint Arthropathy",
                    "Sacroliliac Joint Dysfunction"
                ],
                "questions": [
                    {"id": "lbp_diagnosis", "type": "single_select", "label": "Working Diagnosis", "required": True, "options": ["Non-specific mechanical back pain", "Disc prolapse with radiculopathy", "Spinal stenosis", "Suspected cauda equina - EMERGENCY", "Suspected vertebral fracture", "Suspected infection", "Suspected malignancy", "Inflammatory back pain", "Uncertain"]}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "CAUDA EQUINA RED FLAGS - Return immediately/attend A&E if: numbness in saddle area, difficulty passing urine/loss of bladder control, faecal incontinence, weakness in both legs, worsening numbness in legs. Provide cauda equina card/leaflet. For mechanical back pain: remain as active as tolerated, avoid bed rest, regular analgesia (paracetamol + NSAID if not contraindicated). If radiculopathy: consider neuropathic agent (gabapentin/pregabalin/amitriptyline). Physiotherapy referral. If no improvement in 4-6 weeks or red flags develop - review and consider imaging/referral. Fit note if needed.",
                "questions": [
                    {"id": "lbp_plan", "type": "single_select", "label": "Management", "required": True, "options": ["Reassurance + advice + analgesia", "Physiotherapy referral", "Urgent MRI (suspected cauda equina)", "X-ray + routine referral", "Emergency A&E referral", "Routine orthopaedics referral", "Rheumatology referral"]},
                    {"id": "lbp_analgesia", "type": "multi_select", "label": "Analgesia", "required": False, "options": ["Paracetamol", "NSAID (if not contraindicated)", "Codeine/Tramadol", "Gabapentin/Pregabalin (neuropathic)", "Amitriptyline (night)", "Muscle relaxant (short-term)"]},
                    {"id": "lbp_imaging", "type": "single_select", "label": "Imaging", "required": False, "options": ["None indicated", "X-ray lumbar spine", "Urgent MRI (within 48h)", "Emergency MRI (same day)", "CT if MRI contraindicated"]},
                    {"id": "lbp_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2-4 weeks GP review, sooner if red flags"}
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
    seed_lower_back_pain()