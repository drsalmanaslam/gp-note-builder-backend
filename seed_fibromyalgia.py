from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_fibromyalgia():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Musculoskeletal").first()
    if not category: category = Category(name="Musculoskeletal"); db.add(category); db.commit()

    t = {
        "title": "Fibromyalgia - Diagnosis & Management",
        "description": "ACR 2016 criteria-based fibromyalgia assessment covering diagnostic triad, differential exclusion, non-pharmacological management, and medication options for severe pain.",
        "category": "Musculoskeletal",
        "content": {"sections": [
            {
                "title": "History - Symptom Duration & Distribution",
                "section_type": "history",
                "questions": [
                    {"id": "fibro_duration", "type": "single_select", "label": "Duration of Symptoms (Must Be ≥3 Months for Diagnosis)", "required": True, "options": ["≥3 Months - Meets Criterion", "<3 Months - Does NOT Meet ACR Criteria"]},
                    {"id": "fibro_pain_regions", "type": "multi_select", "label": "Pain Distribution (Need ≥4 of 5 Regions: Left, Right, Upper, Lower, Axial)", "required": True, "options": ["Bilateral Shoulder/Neck Pain", "Lower Back Pain", "Left Side Pain", "Right Side Pain", "Upper Body Pain", "Lower Body Pain", "Axial Pain"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ≥4/5 regions + ≥3 months = meets ACR pain criterion.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Associated Symptoms",
                "section_type": "history",
                "questions": [
                    {"id": "fibro_fatigue", "type": "toggle", "label": "Intrusive Fatigue?", "required": True},
                    {"id": "fibro_sleep", "type": "toggle", "label": "Sleep Disturbance (Unrefreshing Sleep)?", "required": True},
                    {"id": "fibro_cognitive", "type": "toggle", "label": "Impaired Cognitive Function (Fibro Fog)?", "required": True},
                    {"id": "fibro_physical", "type": "toggle", "label": "Impaired Physical Function?", "required": True},
                    {"id": "fibro_morning_stiffness", "type": "toggle", "label": "Morning Stiffness? (Typically <10 Min if Present)", "required": False},
                    {"id": "fibro_paraesthesiae", "type": "toggle", "label": "Paraesthesiae?", "required": False},
                    {"id": "fibro_subjective_swelling", "type": "toggle", "label": "Subjective Joint Swelling (Without Objective Swelling on Exam)?", "required": False},
                    {"id": "fibro_overwhelmed", "type": "toggle", "label": "Feeling Overwhelmed / Psychological Impact?", "required": True},
                    {"id": "fibro_depression", "type": "multi_select", "label": "Depression Screen (Past Month)", "required": True, "options": ["Low Mood / Hopelessness", "Anhedonia (Little Interest or Pleasure)", "None"]},
                    {"id": "fibro_opioids", "type": "toggle", "label": "Regular Opioid Use? (Can Cause Hyperalgesia - Worsens Pain)", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: High-dose opioids can cause hyperalgesia = worsening pain. Consider tapering.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "fibro_joint_swelling", "type": "toggle", "label": "Objective Joint Swelling or Redness?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Objective joint swelling = NOT fibromyalgia. Reconsider diagnosis (?inflammatory arthritis).", "red_flag_negative": ""},
                    {"id": "fibro_neck_rom", "type": "single_select", "label": "Neck Range of Movement", "required": False, "options": ["Full", "Restricted"]},
                    {"id": "fibro_shoulder_rom", "type": "single_select", "label": "Shoulder Range of Movement", "required": False, "options": ["Full", "Restricted"]},
                    {"id": "fibro_back_rom", "type": "single_select", "label": "Back Range of Movement", "required": False, "options": ["Full", "Restricted"]},
                    {"id": "fibro_tenderness", "type": "toggle", "label": "Tenderness on Palpation at Multiple Sites?", "required": True}
                ]
            },
            {
                "title": "Diagnostic Criteria (ACR 2016) - ALL THREE REQUIRED",
                "section_type": "assessment",
                "questions": [
                    {"id": "fibro_criterion1", "type": "toggle", "label": "Criterion 1: Generalised Pain in ≥4 of 5 Body Regions (Left, Right, Upper, Lower, Axial)?", "required": True},
                    {"id": "fibro_criterion2", "type": "toggle", "label": "Criterion 2: Widespread Pain (WPI) + Associated Symptoms (SSS)?", "required": True},
                    {"id": "fibro_criterion3", "type": "toggle", "label": "Criterion 3: Symptoms Present for ≥3 Months?", "required": True},
                    {"id": "fibro_acr_met", "type": "toggle", "label": "ALL 3 ACR Criteria Met? (Reference: https://www.rcp.ac.uk/guidelines-policy/diagnosis-fibromyalgia-syndrome)", "required": True}
                ]
            },
            {
                "title": "Differential Diagnosis - Exclude",
                "section_type": "assessment",
                "differentials": [
                    "Hypothyroidism",
                    "Rheumatoid Arthritis / Ankylosing Spondylitis / SLE / PMR",
                    "Peripheral Neuropathies",
                    "Medication-Induced Hyperalgesia (High-Dose Opioids)",
                    "Obstructive Sleep Apnoea",
                    "Depression",
                    "Chronic Fatigue Syndrome (Fatigue/Sleep Predominant, Not Pain)",
                    "Vitamin D Deficiency / Osteomalacia",
                    "Multiple Sclerosis"
                ],
                "questions": [
                    {"id": "fibro_excluded", "type": "multi_select", "label": "Differentials Excluded / Screened", "required": True, "options": ["Hypothyroidism (TFTs)", "Inflammatory Arthritis (ESR/CRP, Clinical Exam)", "Peripheral Neuropathy", "Medication Cause Reviewed", "OSA Considered", "Depression Screened", "CFS Distinguished (Fatigue > Pain)"]}
                ]
            },
            {
                "title": "Investigations (Exclude Differentials)",
                "section_type": "assessment",
                "questions": [
                    {"id": "fibro_bloods", "type": "multi_select", "label": "Bloods Ordered", "required": False, "options": ["FBC", "U&E", "ESR / CRP", "LFTs", "TFTs", "HbA1c", "CK"]}
                ]
            },
            {
                "title": "Patient Education",
                "section_type": "plan",
                "questions": [
                    {"id": "fibro_edu_valid", "type": "toggle", "label": "Explained: Fibromyalgia is a Recognised, Valid Syndrome of Unknown Cause?", "required": True},
                    {"id": "fibro_edu_fluctuate", "type": "toggle", "label": "Explained: Symptoms Fluctuate Over Time?", "required": False},
                    {"id": "fibro_edu_qol", "type": "toggle", "label": "Explained: Treatment Focus is Improving Health-Related Quality of Life, NOT Eliminating Pain?", "required": True}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "Fibromyalgia is a recognised, valid syndrome. ACR 2016 criteria: all 3 required for diagnosis. Treatment focus: improving quality of life, not eliminating pain. First-line non-pharmacological: exercise classes (strongest evidence), continue normal activity + remain in workplace with adjustments, CBT (recommended), tai chi. Patient resources: Versus Arthritis, RCP information sheet, NHS fibromyalgia, Flippin' Pain. Medication LAST RESORT for severe pain only: Duloxetine 60-120mg trial 2 months, OR Amitriptyline 10-50mg if sleep prominent. Avoid opioids (cause hyperalgesia). Regular follow-up to assess function + quality of life.",
                "questions": [
                    {"id": "fibro_diagnosis", "type": "single_select", "label": "Impression", "required": True, "options": ["Fibromyalgia - ACR Criteria Met", "Fibromyalgia - Criteria Partially Met, Monitor", "Alternative Diagnosis More Likely", "Differentials Not Yet Excluded"]},
                    {"id": "fibro_non_pharm", "type": "multi_select", "label": "First-Line Non-Pharmacological", "required": False, "options": ["Exercise Classes (Strongest Evidence)", "Continue Normal Activity + Workplace Adjustments", "CBT (Recommended)", "Tai Chi"]},
                    {"id": "fibro_resources", "type": "multi_select", "label": "Patient Resources Given", "required": False, "options": ["Versus Arthritis", "RCP Information Sheet", "NHS Fibromyalgia", "Flippin' Pain"]},
                    {"id": "fibro_medication", "type": "single_select", "label": "Medication (Last Resort - Severe Pain Only)", "required": False, "options": ["Duloxetine 60-120mg - Trial 2 Months", "Amitriptyline 10-50mg (If Sleep Prominent)", "None - Non-Pharmacological Only"]},
                    {"id": "fibro_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., 2 months if medication trial, 3-6 months routine review"}
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
    seed_fibromyalgia()