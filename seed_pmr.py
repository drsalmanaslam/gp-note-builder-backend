from app.database import SessionLocal
from app.models import User, Template, Category

def seed_pmr():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Polymyalgia Rheumatica (PMR) - Diagnosis & Management",
        "description": "Comprehensive PMR assessment covering GCA exclusion, steroid initiation and tapering protocol, monitoring, and bisphosphonate/PPI co-prescribing.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "RED FLAGS - Giant Cell Arteritis (GCA) Exclusion",
                "section_type": "history",
                "questions": [
                    {"id": "pmr_temporal_headache", "type": "toggle", "label": "Temporal Headache?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Temporal headache + PMR symptoms = ?GCA. Urgent rheumatology + temporal artery biopsy.", "red_flag_negative": ""},
                    {"id": "pmr_visual_loss", "type": "toggle", "label": "Visual Loss or Diplopia?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Visual symptoms = ?GCA with risk of blindness. EMERGENCY - same-day ophthalmology + high-dose steroids.", "red_flag_negative": ""},
                    {"id": "pmr_scalp_tenderness", "type": "toggle", "label": "Scalp Tenderness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Scalp tenderness = ?GCA.", "red_flag_negative": ""},
                    {"id": "pmr_jaw_claudication", "type": "toggle", "label": "Pain When Chewing Food or Drinking? (Jaw Claudication)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Jaw claudication = highly specific for GCA. Urgent rheumatology.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "pmr_age", "type": "number", "label": "Age (Must Be >50 Years for PMR Diagnosis)", "required": True, "placeholder": "e.g., 72"},
                    {"id": "pmr_onset", "type": "single_select", "label": "Onset", "required": True, "options": ["Abrupt (Days)", "Subacute (Weeks)"]},
                    {"id": "pmr_duration", "type": "text", "label": "Duration of Symptoms", "required": True, "placeholder": "e.g., >2 weeks"},
                    {"id": "pmr_pain_sites", "type": "multi_select", "label": "Pain Distribution (Bilateral, Symmetrical)", "required": True, "options": ["Shoulder Girdle (Aching)", "Hip Girdle", "Thigh Muscles", "Upper Arms"]},
                    {"id": "pmr_morning_stiffness", "type": "text", "label": "Morning Stiffness Duration", "required": True, "placeholder": "e.g., 45 minutes to loosen out"},
                    {"id": "pmr_turning_bed", "type": "toggle", "label": "Difficulty Turning Over in Bed?", "required": True},
                    {"id": "pmr_better_active", "type": "toggle", "label": "Better When Active for >45 Minutes?", "required": True},
                    {"id": "pmr_fatigue", "type": "toggle", "label": "Feeling Tired / Fatigued?", "required": True},
                    {"id": "pmr_muscles_tender", "type": "toggle", "label": "Muscles Painful to Touch?", "required": False},
                    {"id": "pmr_systemic", "type": "multi_select", "label": "Systemic Symptoms", "required": True, "options": ["Fever / Night Sweats", "Weight Loss", "Recent Weight Gain", "Cold Intolerance", "None"]}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "pmr_shoulder_tenderness", "type": "toggle", "label": "Tenderness on Palpation - Shoulder Girdle?", "required": True},
                    {"id": "pmr_pelvic_tenderness", "type": "toggle", "label": "Tenderness on Palpation - Pelvic Girdle?", "required": True},
                    {"id": "pmr_rom", "type": "single_select", "label": "Range of Movement (Shoulder/Hip)", "required": True, "options": ["Decreased ROM from Pain + Stiffness", "Full ROM", "Restricted - Mechanical"]},
                    {"id": "pmr_temporal_artery", "type": "single_select", "label": "Temporal Artery", "required": True, "options": ["No Tenderness/Thickening - Pulse Normal", "Tender / Thickened - RED FLAG (GCA)"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Abnormal temporal artery = ?GCA. High-dose steroids + urgent rheumatology.", "red_flag_negative": ""},
                    {"id": "pmr_muscle_weakness", "type": "toggle", "label": "Muscle Weakness? (Should Be ABSENT in PMR - If Present Reconsider Diagnosis)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Muscle weakness = NOT typical of PMR. Consider myositis, myopathy, steroid myopathy.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Investigations",
                "section_type": "assessment",
                "differentials": [
                    "Polymyalgia Rheumatica (PMR)",
                    "Giant Cell Arteritis (GCA) - RED FLAG",
                    "Rheumatoid Arthritis (Late-Onset)",
                    "Inflammatory Myositis / Polymyositis",
                    "Fibromyalgia",
                    "Hypothyroidism",
                    "Osteoarthritis (Bilateral Shoulder/Hip)",
                    "Malignancy (Myeloma - Check SPEP)",
                    "Depression"
                ],
                "questions": [
                    {"id": "pmr_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "ESR (Significant if >50 mm/hr)", "CRP", "CK (Normal in PMR)", "Rheumatoid Factor", "Bone Profile", "TFTs", "Fasting Glucose / HbA1c", "Serum Protein Electrophoresis (SPEP)", "Serum Free Light Chains", "ANA"]},
                    {"id": "pmr_urinalysis", "type": "toggle", "label": "Urine Dipstick?", "required": False}
                ]
            },
            {
                "title": "Steroid Initiation & Tapering Protocol",
                "section_type": "plan",
                "safety_netting": "EMERGENCY - attend A&E immediately if: temporal headache, jaw pain when chewing, loss of vision, or any GCA symptoms. Steroid tapering protocol: 15mg Prednisolone daily until symptoms fully controlled (~3 weeks) → 12.5mg daily for 3 weeks → 10mg daily for 4-6 weeks → reduce by 1mg every 4-8 weeks until stopped. Do NOT stop abruptly (adrenal suppression risk). Co-prescribe: Bisphosphonate (Alendronate + Vit D) for bone protection + PPI (Lansoprazole) for gastric protection. Counsel: weight gain, bruising, skin thinning, dyspepsia, muscle weakness. Provide STEROID CARD. Avoid close contact with chickenpox/shingles/measles if non-immune. Follow-up: 1 week to assess response, 3 weeks to review dose + recheck ESR/CRP, then 3-monthly with BP + fasting glucose/HbA1c.",
                "questions": [
                    {"id": "pmr_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["PMR - Confirmed (Clinical + Raised ESR/CRP)", "PMR - Suspected (Awaiting Bloods)", "?GCA - URGENT Rheumatology", "Alternative Diagnosis More Likely"]},
                    {"id": "pmr_steroid_start", "type": "single_select", "label": "Prednisolone Initiation", "required": False, "options": ["Start 15mg OD - Review in 1 Week", "Not Starting - Awaiting Investigations", "GCA Suspected - High-Dose Steroids + Urgent Referral"]},
                    {"id": "pmr_bone_protection", "type": "toggle", "label": "Bisphosphonate (Alendronate + Vit D) Co-Prescribed?", "required": False},
                    {"id": "pmr_ppi", "type": "toggle", "label": "PPI (Lansoprazole) Co-Prescribed for Gastric Protection?", "required": False},
                    {"id": "pmr_counselling", "type": "multi_select", "label": "Patient Counselling Given", "required": False, "options": ["Weight Gain / Bruising / Skin Thinning", "Dyspepsia", "Muscle Weakness", "Steroid Card Provided", "Avoid Chickenpox/Shingles/Measles if Non-Immune"]},
                    {"id": "pmr_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 1 week response, 3 weeks review + ESR/CRP, 3-monthly BP + glucose"}
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
    seed_pmr()