from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_melanoma_guideline():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin: print("Admin not found."); db.close(); return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category: category = Category(name="Dermatology"); db.add(category); db.commit()

    t = {
        "title": "Melanoma - National GP Referral Guideline (NCCP 2022)",
        "description": "National NCCP 2022 guideline-based melanoma assessment covering ABCDE criteria, ugly duckling sign, urgent referral indications, and primary care excision advice.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "Presenting Complaint",
                "section_type": "history",
                "questions": [
                    {"id": "mel_presentation", "type": "single_select", "label": "Presenting Complaint", "required": True, "options": ["New pigmented lesion", "Changing pigmented lesion", "Long-standing lesion, now changing", "New pigmented line in nail", "Lesion growing under nail", "Itching lesion", "Bleeding lesion", "Incidental finding - opportunistic assessment"]},
                    {"id": "mel_duration", "type": "single_select", "label": "Lesion Duration", "required": True, "options": ["New", "Long-standing, now changing"]},
                    {"id": "mel_nail", "type": "single_select", "label": "Nail Involvement", "required": False, "options": ["New pigmented line in nail", "Associated nail damage", "Lesion growing under nail", "Not applicable"]}
                ]
            },
            {
                "title": "Risk Factors (NCRI 2017)",
                "section_type": "history",
                "questions": [
                    {"id": "mel_risk_factors", "type": "multi_select", "label": "Risk Factors (>1,000 new cases/year in Ireland, >150 deaths/year)", "required": True, "options": ["Atypical moles", "Large number of moles (>50)", "Fair complexion (fair skin, blue eyes, red/blond hair)", "Previous melanoma or non-melanoma skin cancer", "Immunosuppression", "Family history of melanoma", "History of childhood sunburn", "Sun bed exposure", "Higher socio-economic status", "None identified"], "is_red_flag": True, "red_flag_positive": "RED FLAG: One-third female + one-fifth male melanoma patients diagnosed before age 50. Risk factors increase suspicion.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "ABCDE Lesion Assessment",
                "section_type": "examination",
                "questions": [
                    {"id": "mel_asymmetry", "type": "single_select", "label": "A - Asymmetry", "required": True, "options": ["Asymmetry in two axes present - SUSPICIOUS", "Symmetrical"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Asymmetry = 1 point towards melanoma suspicion.", "red_flag_negative": ""},
                    {"id": "mel_border", "type": "single_select", "label": "B - Border", "required": True, "options": ["Irregular border - SUSPICIOUS", "Regular border"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Irregular border = 1 point towards melanoma suspicion.", "red_flag_negative": ""},
                    {"id": "mel_colour", "type": "single_select", "label": "C - Colour", "required": True, "options": ["At least two different colours within lesion - SUSPICIOUS", "Uniform colour"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Multiple colours = 1 point towards melanoma suspicion.", "red_flag_negative": ""},
                    {"id": "mel_diameter", "type": "single_select", "label": "D - Diameter", "required": True, "options": [">6mm maximum diameter - SUSPICIOUS", "≤6mm"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Diameter >6mm = 1 point towards melanoma suspicion.", "red_flag_negative": ""},
                    {"id": "mel_evolution", "type": "single_select", "label": "E - Evolution / Change", "required": True, "options": ["Lesion evolving / changing - SUSPICIOUS", "Stable, no change"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Changing lesion = most important feature. Urgent referral.", "red_flag_negative": ""},
                    {"id": "mel_ugly_duckling", "type": "single_select", "label": "Ugly Duckling Sign (Looks Different to Other Moles)", "required": True, "options": ["Present - RED FLAG", "Absent"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Ugly duckling sign = urgent referral regardless of other features.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Urgent Referral Indications (Any ONE = Refer)",
                "section_type": "assessment",
                "questions": [
                    {"id": "mel_referral_criteria", "type": "multi_select", "label": "Suspicious Lesion Criteria - URGENT Referral", "required": True, "options": ["Any new or changing pigmented lesion", "Long-standing pigmented lesion changing progressively in shape/size/colour (regardless of age)", "New pigmented line in nail, especially with nail damage, or lesion growing under nail", "Pigmented lesion changed in appearance, or persistently itching or bleeding", "Ugly duckling lesion", "None - lesion not currently suspicious"], "is_red_flag": True, "red_flag_positive": "RED FLAG: ANY ONE of these = URGENT referral to consultant dermatologist or plastic surgeon.", "red_flag_negative": ""}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": [
                    "Suspected Melanoma - URGENT Referral",
                    "Benign Melanocytic Naevus",
                    "Seborrhoeic Keratosis",
                    "Dermatofibroma",
                    "Pigmented Basal Cell Carcinoma",
                    "Solar Lentigo",
                    "Subungual Haematoma (vs Subungual Melanoma)",
                    "Atypical / Dysplastic Naevus"
                ],
                "questions": [
                    {"id": "mel_impression", "type": "single_select", "label": "Clinical Impression", "required": True, "options": ["Suspected Melanoma - URGENT referral indicated", "Benign-appearing pigmented lesion - no referral", "Lesion inadvertently excised - urgent MDT referral required"]}
                ]
            },
            {
                "title": "Management & Referral",
                "section_type": "plan",
                "safety_netting": "Suspicious lesions should NOT be removed in primary care. Refer with lesion INTACT to consultant dermatologist or plastic surgeon. NEVER perform shave excisions or punch biopsies on naevi. Prophylactic excision of naevi without suspicious features should NOT be carried out. If lesion inadvertently excised: urgent referral for MDT follow-up with histopathology. All confirmed melanoma cases must be discussed at melanoma/skin cancer MDT at cancer centre. Advise patient on skin awareness + opportunistic skin check. >1,000 new melanoma cases annually in Ireland (NCRI 2017). One-third female + one-fifth male patients diagnosed before age 50.",
                "questions": [
                    {"id": "mel_biopsy_advice", "type": "single_select", "label": "Biopsy / Excision Advice (NCCP Guideline)", "required": True, "options": ["Referred with lesion INTACT - not excised in primary care", "Advised against prophylactic excision - no suspicious features", "Lesion inadvertently excised - urgent referral for MDT + histopathology"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Do NOT excise suspicious lesions in primary care. Do NOT shave/punch biopsy naevi. Refer intact.", "red_flag_negative": ""},
                    {"id": "mel_referral", "type": "single_select", "label": "Referral to Dermatologist / Plastic Surgeon", "required": True, "options": ["Yes - URGENT referral", "No - reassurance + safety-netting", "Confirmed melanoma - MDT discussion arranged"]},
                    {"id": "mel_education", "type": "toggle", "label": "Skin Awareness + Opportunistic Check Advised?", "required": False},
                    {"id": "mel_followup", "type": "text", "label": "Follow-up Plan", "required": True, "placeholder": "e.g., Referral sent - awaiting appointment, routine surveillance, or MDT pathway"}
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
    seed_melanoma_guideline()