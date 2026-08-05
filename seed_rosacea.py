from app.database import SessionLocal
from app.models import User, Template, Category
from datetime import datetime, timezone


def seed_rosacea():
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
        "title": "Rosacea",
        "description": "Assessment and management of rosacea. Covers subtypes, triggers, stepped treatment approach, and when to refer dermatology.",
        "category": "Dermatology",
        "content": {
            "sections": [
                {
                    "title": "History & Subtype",
                    "section_type": "history",
                    "questions": [
                        {
                            "id": "rosacea_symptoms",
                            "type": "multi_select",
                            "label": "Symptoms",
                            "required": True,
                            "options": [
                                "Facial flushing / blushing",
                                "Persistent centrofacial erythema",
                                "Papules / pustules (no comedones — unlike acne)",
                                "Telangiectasia (visible blood vessels)",
                                "Burning / stinging sensation",
                                "Rhinophyma (thickened nasal skin)",
                                "Ocular symptoms (dry, gritty, red eyes)"
                            ],
                            "output_phrase": "Symptoms: {value}"
                        },
                        {
                            "id": "rosacea_eye",
                            "type": "toggle",
                            "label": "Ocular Involvement? (gritty eyes, blepharitis, keratitis)",
                            "required": True,
                            "is_red_flag": True,
                            "red_flag_positive": "RED FLAG: Ocular rosacea — risk of keratitis and vision loss. Same-day ophthalmology if corneal involvement (pain, photophobia, reduced vision).",
                            "red_flag_negative": "",
                            "output_phrase": "Ocular: {value}"
                        },
                        {
                            "id": "rosacea_triggers",
                            "type": "multi_select",
                            "label": "Triggers",
                            "required": False,
                            "options": [
                                "Sunlight / UV exposure",
                                "Hot drinks / alcohol",
                                "Spicy foods",
                                "Stress",
                                "Hot baths / sauna",
                                "Exercise",
                                "Cold wind / temperature changes",
                                "Skincare products",
                                "Unknown"
                            ],
                            "output_phrase": "Triggers: {value}"
                        }
                    ]
                },
                {
                    "title": "Examination",
                    "section_type": "examination",
                    "questions": [
                        {
                            "id": "rosacea_pattern",
                            "type": "single_select",
                            "label": "Distribution",
                            "required": True,
                            "options": [
                                "Centrofacial (cheeks, nose, chin, forehead)",
                                "Nose only — ?rhinophyma",
                                "Periorbital / eyelids (ocular dominant)",
                                "Extrafacial (neck, chest)"
                            ],
                            "output_phrase": "Distribution: {value}"
                        },
                        {
                            "id": "rosacea_rhinophyma",
                            "type": "toggle",
                            "label": "Rhinophyma Present? (thickened, bumpy nasal skin)",
                            "required": False,
                            "output_phrase": "Rhinophyma: {value}"
                        }
                    ]
                },
                {
                    "title": "Assessment",
                    "section_type": "assessment",
                    "differentials": [
                        "Rosacea — erythematotelangiectatic",
                        "Rosacea — papulopustular",
                        "Rosacea — phymatous (rhinophyma)",
                        "Rosacea — ocular",
                        "Acne vulgaris (comedones present = acne, not rosacea)",
                        "Seborrhoeic dermatitis",
                        "Lupus erythematosus (butterfly rash)",
                        "Contact dermatitis"
                    ],
                    "questions": [
                        {
                            "id": "rosacea_subtype",
                            "type": "single_select",
                            "label": "Subtype",
                            "required": True,
                            "options": [
                                "Erythematotelangiectatic (flushing, erythema, telangiectasia)",
                                "Papulopustular (papules, pustules, erythema)",
                                "Phymatous (rhinophyma, thickened skin)",
                                "Ocular (eye symptoms dominant)"
                            ],
                            "output_phrase": "Subtype: {value}"
                        }
                    ]
                },
                {
                    "title": "Management Plan",
                    "section_type": "plan",
                    "safety_netting": "General measures: High-factor sunscreen (SPF 30+) daily, avoid triggers, gentle skincare (soap-free cleanser, avoid alcohol-based products). Erythematotelangiectatic: Topical brimonidine gel (Mirvaso) for temporary redness reduction. Papulopustular: First-line — topical ivermectin 1% cream (Soolantra) OD or metronidazole 0.75% gel BD. If no response at 8-12 weeks: add oral tetracycline (doxycycline 40mg MR / lymecycline). Maintenance usually required — condition is chronic. Telangiectasia: Laser/IPL (private or dermatology). Rhinophyma: Dermatology referral for laser/surgery. Ocular: Lubricating drops, lid hygiene. Ophthalmology referral if corneal involvement. Refer dermatology if: diagnostic uncertainty, severe disease, failed oral treatment, or rhinophyma.",
                    "questions": [
                        {
                            "id": "rosacea_treatment",
                            "type": "single_select",
                            "label": "Treatment",
                            "required": True,
                            "options": [
                                "General measures only (sunscreen, trigger avoidance)",
                                "Topical — ivermectin / metronidazole",
                                "Topical + oral tetracycline",
                                "Brimonidine gel for erythema",
                                "Ocular treatment (lubricants, lid hygiene)",
                                "Refer dermatology"
                            ],
                            "output_phrase": "Treatment: {value}"
                        },
                        {
                            "id": "rosacea_sunscreen",
                            "type": "toggle",
                            "label": "Sunscreen / Trigger Avoidance Advised?",
                            "required": True,
                            "output_phrase": "Sunscreen advice: {value}"
                        },
                        {
                            "id": "rosacea_followup",
                            "type": "text",
                            "label": "Follow-up Plan",
                            "required": True,
                            "placeholder": "e.g., Review in 8-12 weeks. If no response to topical, add oral doxycycline.",
                            "output_phrase": "Follow-up: {value}"
                        }
                    ]
                }
            ]
        },
        "is_public": True
    }

    existing = db.query(Template).filter(
        Template.title == t["title"],
        Template.created_by == admin.id
    ).first()

    if existing:
        existing.description = t["description"]
        existing.content = t["content"]
        existing.category = t["category"]
        existing.is_public = t["is_public"]
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        print(f"🔄 Updated: {t['title']}")
    else:
        new_t = Template(
            title=t["title"],
            description=t["description"],
            category=t["category"],
            content=t["content"],
            is_public=True,
            created_by=admin.id,
            version=1
        )
        db.add(new_t)
        db.commit()
        print(f"✅ Template '{t['title']}' created with {len(t['content']['sections'])} sections!")

    db.close()


if __name__ == "__main__":
    seed_rosacea()