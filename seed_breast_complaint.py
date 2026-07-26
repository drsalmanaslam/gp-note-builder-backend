from app.database import SessionLocal
from app.models import User, Template, Category

def seed_breast_complaint():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Women's Health").first()
    if not category: category = Category(name="Women's Health"); db.add(category); db.commit()

    t = {
        "title": "Breast Complaint - National Breast Cancer GP Referral Guideline (2021)",
        "description": "National guideline-based assessment covering all breast complaint pathways: discrete lump, non-lump complaints, nipple/skin conditions, and mastalgia with clear referral criteria.",
        "category": "Women's Health",
        "content": {"sections": [
            {
                "title": "Presenting Complaint",
                "section_type": "history",
                "questions": [
                    {"id": "bc_pathway_type", "type": "single_select", "label": "Type of Presentation", "required": True, "options": ["Self-detected breast lump (Pathway A)", "Breast complaint other than a discrete lump (Pathway B)", "Mastalgia / breast pain alone (Pathway C)"]}
                ]
            },
            {
                "title": "Clinical Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "bc_exam_findings", "type": "single_select", "label": "Clinical Exam Findings", "required": True, "options": ["Discrete breast lump identified", "No discrete breast lump found", "Other breast complaint identified (non-lump)", "Normal exam"]}
                ]
            },
            {
                "title": "Pathway A - Breast Lump",
                "section_type": "assessment",
                "questions": [
                    {"id": "bc_a1_no_lump", "type": "single_select", "label": "A1: If No Discrete Lump Found on Exam", "required": False, "options": ["Clinical exam normal → Reassure patient", "Consider clinical review at different point in menstrual cycle", "If ongoing concern → Refer to Symptomatic Breast Clinic", "Not applicable"]},
                    {"id": "bc_a2_lump_found", "type": "single_select", "label": "A2: If Discrete Lump Found on Exam", "required": False, "options": ["Refer to Symptomatic Breast Clinic", "Not applicable"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Discrete breast lump = refer to Symptomatic Breast Clinic. If other breast signs also present, also follow Pathway B.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Pathway B - Breast Complaint (Non-Lump)",
                "section_type": "assessment",
                "questions": [
                    {"id": "bc_b1_breast_axilla_refer", "type": "multi_select", "label": "B1: Breast/Axilla - REFER to Symptomatic Breast Clinic", "required": False, "options": ["Breast abscess", "Suspicious axillary lump", "Asymmetric focal nodularity persisting beyond one menstrual cycle", "Image-detected breast abnormality on CT/MRI (report + disk required)", "None of these"]},
                    {"id": "bc_b1_do_not_refer", "type": "multi_select", "label": "B1: Do NOT Refer (Reassure)", "required": False, "options": ["Hidradenitis", "Axillary adiposity", "Gynaecomastia", "Costochondritis / musculoskeletal pain", "None of these"]},
                    {"id": "bc_b2_nipple_refer", "type": "multi_select", "label": "B2: Nipple Conditions - REFER", "required": False, "options": ["Unilateral bloody nipple discharge", "Unilateral spontaneous serous nipple discharge", "New and fixed nipple retraction", "Nipple eczema refractory to topical treatment", "None of these"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Bloody/serous unilateral discharge + new nipple retraction = urgent referral.", "red_flag_negative": ""},
                    {"id": "bc_b2_nipple_no_refer", "type": "multi_select", "label": "B2: Nipple Conditions - Do NOT Refer", "required": False, "options": ["Nipple itch without associated rash", "Non-bloody bilateral nipple discharge", "None of these"]},
                    {"id": "bc_b3_skin_refer", "type": "multi_select", "label": "B3: Skin Conditions - REFER", "required": False, "options": ["Skin dimpling", "Peau d'orange", "Nipple eczema refractory to topical treatment", "Breast abscess", "None of these"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Skin dimpling + peau d'orange = inflammatory breast cancer until proven otherwise. Urgent referral.", "red_flag_negative": ""},
                    {"id": "bc_b3_skin_no_refer", "type": "multi_select", "label": "B3: Skin Conditions - Do NOT Refer", "required": False, "options": ["Nipple itch without associated rash", "Sebaceous cysts", "Skin lesions (benign)", "Hidradenitis", "None of these"]}
                ]
            },
            {
                "title": "Pathway C - Mastalgia (Breast Pain) Alone",
                "section_type": "assessment",
                "questions": [
                    {"id": "bc_c1_other_signs", "type": "toggle", "label": "Other Breast Signs/Symptoms Present?", "required": False, "is_red_flag": True, "red_flag_positive": "RED FLAG: If other signs present = NOT mastalgia alone. Follow Pathway A (lump) or B (other complaint).", "red_flag_negative": ""},
                    {"id": "bc_c2_age", "type": "single_select", "label": "Patient Age", "required": False, "options": ["Under 35 years", "35 years or older"]},
                    {"id": "bc_c3_exam", "type": "single_select", "label": "Clinical Exam", "required": False, "options": ["Normal", "Suspicious findings"]},
                    {"id": "bc_c4_under35_normal", "type": "multi_select", "label": "Management: Under 35 + Normal Exam", "required": False, "options": ["No referral indicated", "Reassure - mastalgia alone is not suggestive of cancer", "Provide mastalgia advice (supportive bra, NSAIDs, evening primrose oil)", "Advise to return if other breast signs/symptoms develop", "Not applicable"]},
                    {"id": "bc_c5_over35_normal", "type": "multi_select", "label": "Management: ≥35 + Normal Exam", "required": False, "options": ["No referral indicated initially", "Reassure + provide mastalgia advice", "If pain persists >3 months → Consider referral for mammography only", "Not applicable"]},
                    {"id": "bc_c6_suspicious", "type": "single_select", "label": "Management: Suspicious Findings (Any Age)", "required": False, "options": ["Refer to Symptomatic Breast Clinic", "Not applicable"]}
                ]
            },
            {
                "title": "Impression & Referral",
                "section_type": "assessment",
                "differentials": [
                    "Normal Breast Examination",
                    "Discrete Breast Lump - Referral Indicated",
                    "Non-Lump Breast Complaint - Referral Indicated",
                    "Non-Lump Breast Complaint - No Referral Needed",
                    "Mastalgia Alone - No Referral (Under 35)",
                    "Mastalgia Alone - Consider Mammography if >3 Months (≥35)",
                    "Suspected Breast Cancer - URGENT Symptomatic Breast Clinic"
                ],
                "questions": [
                    {"id": "bc_impression", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Normal breast exam - reassurance appropriate", "Discrete lump - referral indicated", "Non-lump breast complaint - referral indicated", "Non-lump breast complaint - referral not indicated", "Mastalgia alone - no referral", "Mastalgia alone - mammography referral being considered"]},
                    {"id": "bc_referral", "type": "single_select", "label": "Referral to Symptomatic Breast Disease Clinic", "required": True, "options": ["Yes - Refer now", "No - not indicated at this time", "Deferred - review at different cycle point first"]}
                ]
            },
            {
                "title": "Safety-Netting & Follow-Up",
                "section_type": "plan",
                "safety_netting": "Return immediately if: new lump develops, skin changes (dimpling, peau d'orange), new nipple retraction/discharge (especially bloody or unilateral), or pain persists >3 months (if ≥35, consider mammography). Mastalgia alone with normal exam is NOT suggestive of cancer - reassure. If discrete lump: refer to Symptomatic Breast Clinic. If non-lump complaint with referral criteria: refer. If no referral indicated: safety-net + advise to return if new symptoms develop.",
                "questions": [
                    {"id": "bc_mastalgia_advice", "type": "toggle", "label": "Mastalgia Advice Given? (Supportive bra, NSAIDs, evening primrose oil)", "required": False},
                    {"id": "bc_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., PRN if new symptoms, review at different cycle point, or referral made"}
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
    seed_breast_complaint()