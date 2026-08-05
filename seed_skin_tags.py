from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone

def seed_skin_tags():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "gpclinicaldirector@notebuilder").first()
    if not admin:
        print("Admin not found.")
        db.close()
        return

    category = db.query(Category).filter(Category.name == "Dermatology").first()
    if not category:
        category = Category(name="Dermatology")
        db.add(category)
        db.commit()

    t = {
        "title": "Skin Tags (Acrochordons)",
        "description": "Assessment of skin tags including differentiating from other lesions, red flags for malignancy, and management options including cryotherapy and excision.",
        "category": "Dermatology",
        "content": {"sections": [
            {
                "title": "History",
                "section_type": "history",
                "questions": [
                    {"id": "st_site", "type": "multi_select", "label": "Location", "required": True, "options": ["Neck", "Axillae", "Groin", "Eyelids", "Under breasts", "Trunk", "Other"], "output_phrase": "Sites: {value}"},
                    {"id": "st_symptoms", "type": "multi_select", "label": "Symptoms", "required": True, "options": ["Asymptomatic — cosmetic concern", "Catching on clothing/jewellery", "Bleeding / irritation", "Rapidly growing", "Multiple — increasing in number", "Painful"], "output_phrase": "Symptoms: {value}"},
                    {"id": "st_change", "type": "toggle", "label": "Recent Change in Size / Colour / Shape?", "required": True, "is_red_flag": True, "red_flag_positive": "RED FLAG: Changing lesion = ?skin cancer. Examine carefully. Low threshold for excision + histology if atypical.", "red_flag_negative": "", "output_phrase": "Change: {value}"}
                ]
            },
            {
                "title": "Examination",
                "section_type": "examination",
                "questions": [
                    {"id": "st_appearance", "type": "single_select", "label": "Appearance", "required": True, "options": ["Pedunculated — on stalk (classic skin tag)", "Sessile — flat base (wart/fibroma)", "Hyperpigmented (seborrhoeic keratosis)", "Irregular / atypical"], "is_red_flag": True, "red_flag_positive": "RED FLAG: Irregular/atypical lesion = ?BCC/SCC/melanoma. Excision or dermatology referral.", "red_flag_negative": "", "output_phrase": "Appearance: {value}"},
                    {"id": "st_size", "type": "single_select", "label": "Size", "required": True, "options": ["<5mm", "5-10mm", ">10mm"], "output_phrase": "Size: {value}"}
                ]
            },
            {
                "title": "Assessment",
                "section_type": "assessment",
                "differentials": ["Skin Tag (acrochordon) — benign, pedunculated", "Seborrhoeic Keratosis — stuck-on, waxy, hyperpigmented", "Viral Wart — rough surface, thrombosed capillaries", "Neurofibroma — soft, buttonhole sign", "Molluscum Contagiosum — pearly, umbilicated", "BCC — pearly, telangiectasia, rolled edge", "Melanoma — irregular, changing"],
                "questions": [
                    {"id": "st_diagnosis", "type": "single_select", "label": "Diagnosis", "required": True, "options": ["Benign Skin Tag — reassure / cosmetic removal", "?Atypical — excision + histology", "Seborrhoeic Keratosis — benign", "?Malignancy — 2-week wait dermatology", "Other"], "output_phrase": "Diagnosis: {value}"}
                ]
            },
            {
                "title": "Management Plan",
                "section_type": "plan",
                "safety_netting": "BENIGN TAGS: Reassure — harmless, no treatment needed if asymptomatic. If symptomatic/cosmetic: Cryotherapy (small tags, 1-2 freeze-thaw cycles). Snip excision with scissors + local anaesthetic (larger/pedunculated tags). Hyfrecation/cautery (if available). Recurrence possible. Multiple tags: Associated with obesity, insulin resistance — consider metabolic screening. Do NOT excise if uncertain diagnosis — send for histology. Safety-net: Return if lesion changes, grows rapidly, bleeds, or new concerning lesions appear.",
                "questions": [
                    {"id": "st_treatment", "type": "single_select", "label": "Treatment", "required": True, "options": ["Reassurance — no treatment", "Cryotherapy", "Snip excision", "Excision + histology (?atypical)", "Refer dermatology"], "output_phrase": "Treatment: {value}"},
                    {"id": "st_safety_net", "type": "toggle", "label": "Safety-Net Given? (return if changes/grows/bleeds)", "required": True, "output_phrase": "Safety-net: {value}"},
                    {"id": "st_followup", "type": "text", "label": "Follow-up", "required": False, "placeholder": "e.g., No follow-up needed. Return if concerns.", "output_phrase": "Follow-up: {value}"}
                ]
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
        print(f"✅ Template '{t['title']}' created!")
    db.close()

if __name__ == "__main__":
    seed_skin_tags()